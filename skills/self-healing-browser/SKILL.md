---
name: self-healing-browser
description: Self-healing browser extraction workflow. Agent dynamically writes/patches browser helper functions during tasks instead of using rigid frameworks. Covers DOM distillation, anti-bot bypass, vision AI integration, and WeChat/Douyin article extraction.
---

# Self-Healing Browser Extractor

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md)

Use this skill when the agent needs to extract content from websites that have
anti-bot mechanisms, dynamic rendering, or complex interaction requirements.

## Core Philosophy

**Agent writes missing functions.**

Instead of rigid browser automation frameworks that require upfront design
for every scenario, maintain a `browser_helpers.py` module that the agent
dynamically writes and patches during tasks. When a new anti-bot mechanism
is encountered, the agent writes a new function to handle it.

## Architecture

```
┌─────────────────────────────────────────────┐
│           Agent Decision Layer               │
│  Analyzes page, decides extraction strategy  │
└──────────────────┬──────────────────────────┘
┌──────────────────▼──────────────────────────┐
│        browser_helpers.py (writable)         │
│  - extract_wechat_article()                  │
│  - close_login_popup()                       │
│  - bypass_cloudflare()                       │
│  ... (agent adds functions as needed)        │
└──────────────────┬──────────────────────────┘
┌──────────────────▼──────────────────────────┐
│        Playwright / Selenium (engine)        │
│  Chromium browser, headless or headed        │
└─────────────────────────────────────────────┘
```

## Workflow

### 1. Navigate and Snapshot

```python
browser_navigate(url)
# Returns initial snapshot with interactive elements and ref IDs
```

### 2. Handle Anti-Bot Mechanisms

Common patterns the agent should recognize and handle:

- **Login popups**: Set display='none' on popup overlay elements
- **CAPTCHAs**: Use vision AI to read the challenge
- **Cookie walls**: Accept or dismiss cookie consent banners
- **Cloudflare challenges**: Wait for JS challenge to complete

### 3. Extract Content

For dynamic content:

1. **Snapshot first**: Get accessibility tree with element refs
2. **Identify content area**: Find the main content container
3. **Extract**: Use the appropriate helper function
4. **Verify**: Check extracted content makes sense

### 4. Write Missing Functions

When encountering a new pattern:

```python
# Agent writes a new function into browser_helpers.py
def extract_new_site_pattern(page):
    # Implementation based on current page analysis
    pass
```

## Platform-Specific Patterns

### WeChat Articles

```python
def extract_wechat_article(url):
    # Bypass verification by targeting rich_media_content area
    # Regex extraction from the rendered HTML
    # Returns: title, author, content, publish_date
```

### Douyin Notes

1. Short link → resolve redirect via requests
2. Navigate with browser_navigate
3. Close three login popup classes:
   - `.disturb-login-panel`
   - `.douyin_login_new_class`
   - `.comment-input-un-login-container`
4. Use browser_vision for screenshot + AI text reading
5. **Do NOT**: take direct screenshots (may be blank), write Playwright
   directly (timeout), rely on browser_get_images (misses body images)

### SPA Data Extraction

- Use `browser_console` with JavaScript expressions to inspect DOM state
- Wait for async content to render before snapshotting
- Scroll to trigger lazy-loaded content

## Vision AI Integration

When text snapshots are insufficient:

```python
browser_vision(question="What does this CAPTCHA say?")
# Returns: AI analysis + screenshot_path
```

Use for:
- CAPTCHA solving
- Visual verification challenges
- Complex layout understanding
- Image-based content extraction

## Anti-Patterns

- **Do NOT write Playwright scripts directly** — timeouts are common
- **Do NOT take direct screenshots** — they may be blank or miss content
- **Do NOT rely on browser_get_images for body content** — it returns
  page images, not rendered article images
- **Do NOT use rigid frameworks** — they break on new anti-bot patterns
- **Do NOT retry the same approach** — if it failed once, write a new
  helper function

## Helper Function Template

```python
def extract_<site>_<content_type>(page):
    """
    Extract <content_type> from <site>.

    Anti-bot handling:
    - <specific mechanism>

    Returns:
    - <structured data>
    """
    # Implementation
    pass
```

## Verification Checklist

After extraction:
- [ ] Content length is reasonable (not empty, not truncated)
- [ ] Title matches expected page
- [ ] Key data points are present
- [ ] No error messages in extracted text
- [ ] Helper function is saved to browser_helpers.py for reuse
