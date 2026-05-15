---
name: social-media-extraction
description: "Extract content from Chinese social media platforms (WeChat, Douyin, Xiaohongshu, Zhihu) using a tiered strategy: HTTP+regex → Cookie injection → Playwright → Vision."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [scraping, social-media, wechat, douyin, xiaohongshu, extraction]
    category: data-science
---

# Social Media Content Extraction

Tiered extraction strategy for Chinese social media platforms.
**Core principle**: Use the cheapest method that works. Browser is the last resort.

## Tier Strategy

| Tier | Method | Speed | Resource | Platforms |
|------|--------|-------|----------|-----------|
| L1 | `requests` + regex | ~0.5s | Minimal | WeChat, Zhihu (basic), Jianshu |
| L1.5 | `requests` + Cookie injection | ~0.5s | Minimal | Xiaohongshu (needs `web_session` cookie) |
| L2 | Playwright headless | ~5-10s | Chromium RAM | Douyin, Xiaohongshu (no cookie), SPA |
| L3 | Vision/OCR + screenshot | ~15s | High | Complete lockdown/Captcha pages |

## Platform-Specific Patterns

### WeChat Official Accounts (公众号) — Tier 1
**Insight**: Captcha blocks frontend rendering, but HTML body contains full text in `rich_media_content`.

```python
import requests, re
from html import unescape

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5)...',
    'Referer': 'https://mp.weixin.qq.com/',
}
resp = requests.get(url, headers=headers)
html = resp.text

# Title: OG title > JS var > <title>
# Content: rich_media_content region
content_match = re.findall(
    r'class="rich_media_content[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL
)
text = content_match[0].replace('<br/>', '\n').replace('<p>', '').replace('</p>', '\n')
text = re.sub(r'<[^>]+>', '', unescape(text))
text = re.sub(r'\n\s*\n', '\n', text).strip()
```

### Xiaohongshu (小红书) — Tier 1.5 or Tier 2
**Insight**: Alibaba Cloud / datacenter IPs are flagged "IP at risk". Needs cookie injection OR Playwright with residential proxy.

**Cookie injection (L1.5)**:
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    'Cookie': f'web_session={USER_COOKIE}',
    'Referer': 'https://www.xiaohongshu.com/explore',
}
resp = requests.get(url, headers=headers)
# OG tags contain title, desc, images
# __INITIAL_STATE__ contains full JSON data (noteDetailMap)
```

**Playwright (L2)**:
```python
page.goto(url, wait_until='domcontentloaded')
time.sleep(3)  # JS render
# Scroll for lazy-loaded content
for _ in range(3):
    page.evaluate('window.scrollBy(0, window.innerHeight)')
    time.sleep(1)
```

### Douyin (抖音) — Tier 2
**Insight**: Heavy SPA, JS renders everything. Short links need redirect following.

```python
page.goto(url, wait_until='domcontentloaded')
time.sleep(3)
content = page.evaluate("""
    () => {
        ['script','style','nav','footer','header'].forEach(
            tag => document.querySelectorAll(tag).forEach(el => el.remove())
        );
        return (document.querySelector('main') || document.body).innerText.trim();
    }
""")
```

## Workflow

1. **Detect platform** from URL domain
2. **Try L1**: `requests` + regex for OG tags/content
3. **If blocked** → Ask user for Cookie → Try L1.5
4. **If no cookie** → Playwright headless (L2)
5. **If still blocked** → Screenshot + Vision analysis (L3)
6. **On success** → Extract title, author, content, images → Store to wiki

## Pitfalls

- **Never start Playwright for WeChat** — L1 regex is 10x faster and more reliable
- **Xiaohongshu IP blocks** — Datacenter IPs get "IP at risk" 300012 errors. Cookie injection is the workaround without proxy
- **Cookie expiry** — `web_session` cookies expire. When they fail, ask user for a fresh one
- **JSON extraction** — `__INITIAL_STATE__` in Xiaohongshu is valid JSON embedded in script. Extract carefully (brace matching)
- **Anti-scraping headers** — Always use realistic User-Agent + Referer
- **Short URLs** — Follow redirects before parsing (Douyin `v.douyin.com/xxx`)
