---
name: web-scraping-methodology
description: "三层内容提取策略（HTTP正则→Playwright→Cookie注入→视觉），覆盖公众号、抖音、小红书等平台。基于实际踩坑经验总结。"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [scraping, web, methodology, data]
    category: data-science
---

# Web Scraping Methodology — 三层提取策略

> 能不用浏览器就不用，浏览器是最后手段。
> 基于 2026-04-25 实际踩坑经验。

## When This Skill Activates

Use when the user:
- Sends a URL and asks to extract/save content
- Asks "你能爬 X 平台吗"
- Wants to ingest web content into the wiki
- Asks about scraping methodology for a specific platform

## Core Architecture: Three-Tier Ladder

| Level | Technique | When | Time | Resource |
|-------|-----------|------|------|----------|
| L1 | `requests` + regex | Server-rendered pages, content in raw HTML | ~0.5s | Minimal |
| L2 | Playwright headless browser | SPA, JS-rendered content, needs scrolling | ~5-10s | Medium (Chromium) |
| L2.5 | Playwright + Cookie injection | Sites with IP risk/blocking (Xiaohongshu) | ~5-10s | Medium + valid cookie |
| L3 | `browser_vision` screenshot + AI | Complete lockout, CAPTCHA-only pages | ~15s | High |

**Always try L1 first. Fall through only if it fails.**

## Platform Classification

| Platform | Level | Key Finding |
|----------|-------|-------------|
| 微信公众号 | L1 | Content in `rich_media_content`, CSS-hidden but in HTML |
| 知乎 | L1 | Initial HTML has content; comments need L2 |
| 简书 | L1 | Server-rendered |
| 抖音 | L2 | Heavy SPA, JS-rendered, needs Playwright |
| 小红书 | L2.5 | IP risk blocking; requires Cookie injection |
| B 站 | L2 | SPA, video info needs JS |
| Twitter/X | L3 | Strong login wall + anti-bot |

## WeChat (公众号) — L1 Recipe

**Key insight**: WeChat's verification is frontend-only. The article body is always in the HTML response.

```python
import requests, re

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5)...',
    'Referer': 'https://mp.weixin.qq.com/',  # Must include this
}
resp = requests.get(url, headers=headers, timeout=10)
html = resp.text

# Title: try OG > JS var > <title>
# Author: var nickname = "xxx"
# Body: regex on class="rich_media_content"
content_match = re.findall(
    r'class="rich_media_content[^"]*"[^>]*>(.*?)</div>',
    html, re.DOTALL
)

# Clean HTML tags, preserve newlines
text = raw.replace('<br/>', '\n').replace('<p>', '').replace('</p>', '\n')
text = re.sub(r'<[^>]+>', '', text)
text = re.sub(r'\n\s*\n', '\n', text).strip()
```

**Pitfalls**:
- Missing `Referer` header may trigger stricter blocking
- Very long articles may be split — check for "阅读原文" links

## Douyin (抖音) — L2.5 Recipe (Browser Vision 截图读字)

**Key insight (updated 2026-04-30)**: 抖音图文笔记用 `browser_get_images()` + `vision_analyze(image_url)` 的链路不可靠——封面图和正文图不一定都出现在 DOM 中。最佳方案是 **关闭登录弹窗后直接截图 + AI 读字**。

```python
# 1. 解析短链
import requests
r = requests.get('https://v.douyin.com/xxx/', allow_redirects=True, timeout=10)
note_id = r.url.split('/note/')[1].split('?')[0]

# 2. 用 browser_navigate 访问
# 3. 关闭登录弹窗（三个 class）
document.querySelector('.disturb-login-panel').style.display = 'none';
document.querySelector('.douyin_login_new_class').style.display = 'none';
document.querySelector('.comment-input-un-login-container').style.display = 'none';

# 4. browser_vision 截图读字
# question: "当前页面显示的是什么内容？图片上的文字逐字转录。"
```

**坑**：
- 短链 (`v.douyin.com/xxx`) 需跟随重定向获取真实 note ID
- 登录弹窗会反复出现，必须主动关闭
- 图文笔记可能有多页（需手动翻页后再次截图），但多数是单页
- SSR_RENDER_DATA 和 RENDER_DATA 数据编码复杂，正文图片不一定在其中
- `browser_get_images()` 拿不到笔记正文的多张图片，只能拿到封面
- Canvas 渲染的图片在 DOM 中找不到 `<img>` 标签，截图是唯一可靠方案

## GBrain → Wiki Sync — Automated Backup Pipeline

**Key insight (2026-04-30)**: GBrain stores knowledge in Postgres but lacks native Git backup. A lightweight sync script ensures all pages are exported to Markdown and pushed to GitHub every 4 hours.

```python
# ~/wiki/helpers/gbrain_sync.py
# Usage: python3 gbrain_sync.py [--dry-run] [--skip-git]
import subprocess, json
# 1. Connect to GBrain DB via psql
# 2. Fetch all pages as JSON (avoid delimiter conflicts)
# 3. Compare content_hash with local .sync_state.json
# 4. Export changed pages to ~/wiki/gbrain-sync/{slug}.md
# 5. Git commit + push if changes exist
```

**Cron Setup**:
```bash
# Every 4 hours
0 */4 * * * python3 /root/wiki/helpers/gbrain_sync.py >> /var/log/gbrain-sync.log 2>&1
```

**Pitfalls**:
- Use `json_agg(row_to_json(t))` in SQL instead of text delimiters like `|||` which may appear in content
- Store `.sync_state.json` in `.gitignore` to avoid tracking internal state
- Incremental sync based on `content_hash` prevents unnecessary git commits
- Handle deleted pages by comparing current slugs with previous state

## Xiaohongshu (小红书) — L2.5 Recipe (Cookie Injection)

**Key insight**: Xiaohongshu flags datacenter IPs as "IP at risk" (error 300012). Cookie injection bypasses this.

```python
import requests, re

cookie_val = '<user-provided-web_session-cookie>'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    'Cookie': f'web_session={cookie_val}',  # Critical!
    'Referer': 'https://www.xiaohongshu.com/explore',
}
resp = requests.get(url, headers=headers, timeout=15)
html = resp.text

# Content is in window.__INITIAL_STATE__ (JSON embedded in script)
# Also available via OG meta tags for title/description
for m in re.finditer(r'<meta name="og:([^"]*)" content="([^"]*)"', html):
    print(f'{m.group(1)}: {m.group(2)}')
```

**Pitfalls**:
- **Cookie expires** — `web_session` cookies have limited lifetime
- **IP risk error 300012** — without cookie, all requests get redirected to security page
- **xsec_token** — dynamic, per-request. Must use the token from the shared URL
- **User profile vs note page** — both work with cookie, but profile has less structured data
- **Never share full cookies in logs** — they are credentials

## Workflow: URL → Wiki

```
User sends URL → detect platform (domain match)
    ├─ 公众号/知乎/简书 → L1: requests + regex
    ├─ 抖音 → L2: Playwright
    ├─ 小红书 → L2.5: requests + Cookie (if available)
    └─ 都失败 → L3: browser_vision screenshot + AI

Extract → save to raw/articles/ → ingest to wiki → update index + log
```

## How to Ask User for Cookie

When scraping Xiaohongshu without auth:
1. Explain the IP risk issue
2. Ask: "能否从你浏览器导出 `web_session` Cookie 给我？"
3. Instruct: F12 → Application → Cookies → copy `web_session` value
4. **Warn**: "Cookie 是凭证，用完我会丢弃"

## Search Engine Reliability Note

**Key finding (2026-04-28, Alibaba Cloud CN server):**
| Service | Status | Notes |
|---------|--------|-------|
| Google (google.com) | ❌ Timeout | DNS/network blocked |
| Baidu (baidu.com) | ❌ CAPTCHA | Redirects to captcha |
| Bing (cn.bing.com) | ⚠️ Unreliable | Returns generic "2026" results, often ignores specific queries |
| GitHub API | ✅ Fast | Best source for tech trends |
| Douban (movie.douban.com) | ✅ Fast | Server-rendered, no JS needed |

**Workaround:** For event-driven stock research (e.g. May Day movies), scrape structured data sites directly (Douban coming soon, Maoyan) rather than relying on search engines.

## Event-Driven Stock Analysis Pattern (May Day Movies Example)

**Source:** Douban `movie.douban.com/coming`

**Workflow:**
```
1. Get event data → scrape Douban/coming for upcoming dates
2. Identify hot titles by "想看" count
3. Map to stocks → Bing search "[movie] 出品公司 股票"
4. Bing search "[company] 股票 news"
5. Analyze with uwillberich framework:
   - 三层分类法 (market → sector → chain position)
   - Time gate checklist (Buy Window / Hold / Risk)
   - Base / Bull / Bear scenario tree
6. Output: stock codes + triggers + stop losses
```

**Known A-Share Mappings for Film/Movie:**
| Movie Type | Typical Stock |
|------------|--------------|
| 港片/万达出品 | 万达电影(002739) |
| 进口片/好莱坞 | 中国电影(600977) |
| 动画/IP衍生 | 奥飞娱乐(002292) |
| 院线弹性标的 | 上海电影(601595), 金逸影视(002905) |

## Pitfalls

- **Never modify `raw/` sources** — they are immutable snapshots
- **Cookie is a credential** — treat it like a password. Do not log it.
- **L1 before L2** — starting Playwright for a server-rendered page wastes 10 seconds
- **Xiaohongshu cookies expire** — they are not permanent. Plan for re-auth
- **Douyin 口播** — HTML extraction is unreliable for video content. Whisper transcription is better
- **Rate limiting** — space out requests. Aggressive scraping triggers CAPTCHA
- **Encoding** — always handle `errors='ignore'` for Chinese text
