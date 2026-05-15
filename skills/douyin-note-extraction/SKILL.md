---
name: douyin-note-extraction
version: 1.1.0
description: Extract full text content from Douyin multi-image notes (图文作品). Handles login popups, image flipping, and OCR via vision AI. Optimized for Alibaba Cloud server environment with anti-bot evasion.
metadata:
  yao_category: "AI方法"
  requires:
    bins: ["python3"]
  categories:
    - social-media
    - data-extraction
---

# Douyin Note Extraction Workflow (Server-Optimized)

## When to use
- User provides a `v.douyin.com` short link or `douyin.com/note/...` URL.
- User wants the full text content of a multi-image note.
- Running on constrained servers (e.g., Alibaba Cloud 2GB RAM) where heavy dependencies are not available.

## Step-by-step Execution

### 1. Resolve Short Link
Use `requests` to resolve `v.douyin.com` redirects to the full `douyin.com/note/{id}` URL.
```python
import requests
r = requests.get(short_url, allow_redirects=True, timeout=10, headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
})
full_url = r.url
```

### 2. Navigate & Clean DOM
1. `browser_navigate(full_url)`
2. **Critical**: Hide login popups via JS before any visual inspection. Douyin aggressively blocks unauthenticated users with modals that obscure content.
   ```javascript
   ['.disturb-login-panel', '.douyin_login_new_class', '.comment-input-un-login-container', 'div[class*="login"]', 'div[role="dialog"]', '[aria-modal="true"]', '.web-login-modal'].forEach(s => {
     document.querySelectorAll(s).forEach(el => { el.style.display = 'none'; });
   });
   ```
3. If the modal persists, identify it by bounding box (width > 300, height > 300, top < 100) and force-hide via `browser_console`.

### 3. Detect Multi-Image Structure
- Use `browser_console` to count unique content images (`img[src*="douyinpic"]`).
- If > 1 image, it's a multi-image note.
- Check for page indicators (e.g., "1/2", "2/2") in the snapshot or via vision.

### 4. Flip & Extract Loop
For each image (1 to N):
1. **Extract**: Call `browser_vision` with question: "这是第X张。请完整提取图片上所有文字，包括标题、正文等。忽略UI元素。"
2. **Flip**: Press `ArrowRight` key (`browser_press`) to move to the next image.
3. **Wait**: Allow ~1s for transition.
4. **Repeat** until the last page is reached.

### 5. Expand Text Content
- If the post has a "展开" (Expand) button, click it via `browser_click` to reveal the full caption/text.
- Extract the expanded text from the DOM or via vision if it's rendered as an image.

### 6. Compile & Summarize
- Aggregate all extracted text.
- Remove UI noise (nav bars, sidebars, recommended videos).
- Present the core content clearly, including author, date, and tags.

## Pitfalls
- **Login Popups**: Must be hidden via JS before `browser_vision`, otherwise OCR reads garbage or fails. On servers, Douyin often shows a "IP at risk" or login wall immediately.
- **Image Count**: Don't assume single image. Always check for multiple slides.
- **Text Overlap**: Vision AI might read sidebar text. Explicitly ask for "core content" or "main image text".
- **Network**: Douyin anti-bot is aggressive. If `browser_navigate` fails, retry once. On Alibaba Cloud, IP blocking is common; consider using mobile endpoints or proxies if available.
- **Server Constraints**: Do not use heavy tools like `langchain`. Stick to `requests`, `browser_*` tools, and `vision_analyze`.

## Example Output Format
**作者**：{Name} · {Date}
**文案**：{Caption}

### 图文内容
**第1张**
{Text}

**第2张**
{Text}
...

**核心总结**
{One-sentence takeaway}
{One-sentence takeaway}