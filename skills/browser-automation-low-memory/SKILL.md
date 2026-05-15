---
name: browser-automation-low-memory
description: "Browser automation on constrained Alibaba Cloud servers (2GB RAM) — avoid OOM, use direct Playwright instead of heavy frameworks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [browser, playwright, automation, low-memory, alibaba-cloud]
    category: devops
---

# Browser Automation on Low-Memory Servers

This skill covers how to run browser automation on Alibaba Cloud Linux 3 with **2GB RAM** where browser-use and similar heavy frameworks trigger OOM kills.

## Environment Facts

- OS: Alibaba Cloud Linux 3 (RHEL/CentOS compatible)
- RAM: 2GB (available ~500MB after MySQL, Nginx, info-hub, hermes gateway)
- Swap: 8GB (two 4GB files: /www/swap + /www/swap2, both in fstab)
- pip mirror: mirrors.aliyun.com (already configured)
- uv mirror: mirrors.aliyun.com (config at ~/.config/uv/uv.toml)
- Playwright browsers: ~/.cache/ms-playwright/ (chromium-1208 + chromium_headless_shell-1208)
- headless shell path: ~/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell

## Critical Findings

### browser-use DOES NOT WORK even with 8GB swap

Three failure modes discovered through trial (Apr 2026):

1. **Extension download timeout** — browser-use auto-downloads uBlock Origin and "I still don't care about cookies" from foreign CDNs. Domestic network: `Network is unreachable`.
   - Fix: `enable_default_extensions=False` in BrowserProfile

2. **Event bus watchdog deadlock** — v0.12.6 uses event-driven watchdog architecture (bubus). `on_BrowserStartEvent` and `on_BrowserLaunchEvent` hang >15s waiting on async event results.
   - Root cause: event bus handler may be awaiting its own result → deadlock

3. **OOM Kill** (fatal) — Even with extensions disabled, the full browser-use stack (event bus + multiple watchdogs + CDP session management) consumes 1GB+ during startup. Kernel kills the python3 process.
   - Evidence: `dmesg` shows `Out of memory: Killed process <pid> (python3) total-rss:1160120kB`

### Direct Playwright WORKS

```python
from playwright.sync_api import sync_playwright
p = sync_playwright().start()
browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
page = browser.new_page()
page.goto('https://example.com')
print(page.evaluate('document.title'))
browser.close()
p.stop()
```

Memory footprint: ~200-300MB vs browser-use's 1GB+.

## Recommended Approach

### For Wiki ingestion / web scraping (the most common use case)

Use **direct Playwright** — no browser-use framework needed:

```python
from playwright.sync_api import sync_playwright
import asyncio

def fetch_page(url, timeout=15000):
    p = sync_playwright().start()
    try:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
        )
        page = browser.new_page()
        page.goto(url, timeout=timeout)
        content = page.content()
        title = page.evaluate('document.title')
        browser.close()
        return {'title': title, 'content': content}
    finally:
        p.stop()
```

### For SPA rendering / dynamic content

```python
def fetch_spa_content(url, wait_selector=None, wait_ms=2000):
    p = sync_playwright().start()
    try:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = browser.new_page()
        page.goto(url)
        if wait_selector:
            page.wait_for_selector(wait_selector, timeout=10000)
        else:
            page.wait_for_timeout(wait_ms)
        content = page.content()
        browser.close()
        return content
    finally:
        p.stop()
```

## Related Skill

For **site-specific extractors + self-healing (agent writes → tests → patches → persists)**:
→ `skill_view self-healing-browser-extractor`

The extractor registry lives at `~/wiki/helpers/browser_helper.py` (via `register_extractor` decorator + `bh.extract(url)` dispatch).

## Pitfalls

- **NEVER use browser-use on this machine** — OOM kill guaranteed
- **Always add `--no-sandbox`** — running as root on Alibaba Cloud
- **Kill stale browser processes** before launching: `pkill -f chromium 2>/dev/null`
- **Check `free -m`** before heavy operations — if available < 300MB, wait or clear caches
- **Set timeouts** — domestic network to foreign sites can hang indefinitely
- **Use `page.evaluate()` not `page.title()`** in some Playwright versions — `.title()` may not exist on the async Page object

## Reusable Helper Tool

A full-featured browser helper is already available at `~/wiki/helpers/browser_helper.py`:

```python
from browser_helper import BrowserHelper

# Basic text extraction
helper = BrowserHelper()
content = helper.fetch("https://example.com")
helper.close()

# Infinite scroll pages
content = helper.fetch_with_scroll("https://news-site.com", scroll_times=3, wait_between=1.0)
helper.close()

# Screenshot
helper.screenshot("https://example.com", "/tmp/shot.png")
helper.close()

# Meta extraction
meta = helper.extract_meta("https://example.com")
helper.close()

# SPA: wait for specific selector
html = helper.get_html("https://spa-site.com", wait_for="#main-content")
helper.close()
```

Tested and verified on Chinese sites (sina.com.cn, news.sina.com.cn) with good results.

## Self-Healing Browser Harness (Agent-Managed Extractors)

已实现 Agent 动态编写 + 自愈的浏览器提取框架。

### 基础设施

文件: `~/wiki/helpers/browser_helper.py`

- **`BrowserHelper`** — Playwright 轻量封装，fetch / screenshot / scroll 等方法
- **`@register_extractor(r"pattern")`** — 装饰器，将提取函数注册到 URL 模式
- **`bh.extract(url)`** — 自动匹配注册器并执行
- **`bh.debug_extract(url)`** — 失败时保留现场（HTML 快照 + 截图 + 错误信息）
- **`test_all_extractors()`** — 一键全量测试，返回 pass/fail
- **Self‑Healing Protocol** — Agent 按「收集现场 → 分析根因 → 生成修补 → 重试验证」循环，最多 3 轮

### Agent 自愈流程

```
1. test_all_extractors() 发现失败
2. debug_extract(url) 获取 HTML + screenshot
3. Agent 分析: 超时? 选择器失效? 反爬? JS 错误?
4. patch() 修复 browser_helper.py
5. test_all_extractors() 验证
6. 失败 → 返回步骤 2，最多 3 轮
```

### 当前注册的提取器

| 提取器 | URL 模式 | 说明 |
|--------|----------|------|
| `extract_baidu_hot_words` | `news\.baidu\.com` | 百度新闻热搜新闻词 |

Agent 可按需添加新的提取器（写函数 → 加 `@register_extractor` → 测试）。

## WeChat Article Extraction (mp.weixin.qq.com)

微信公众号文章有反爬验证码，**不需要用浏览器** — 纯 requests + regex 即可提取。

详见独立 skill: **`wechat-article-extraction`**

关键发现：即使页面显示"环境异常，完成验证"，文章正文仍完整存在于 HTML 的 `rich_media_content` div 中，只是浏览器拒绝渲染。用 `requests` 带移动端 UA 直接 GET 即可拿到全文。

## When to consider upgrading

Even with 8GB swap, browser-use still OOM'd during testing. Swap expansion alone does not make it viable — the event bus + watchdog architecture is fundamentally too heavy. Only consider browser-use again if RAM is upgraded to 4GB+.
