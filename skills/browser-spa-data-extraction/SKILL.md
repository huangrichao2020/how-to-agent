---
name: browser-spa-data-extraction
description: Techniques for extracting data from complex SPAs (like ModelScope, HuggingFace, GitHub) when standard browser_snapshot or browser_vision tools fail to capture hidden/rendered content.
category: browser
yao_category: "AI方法"
---

# Advanced Browser Data Extraction for SPAs

When navigating sites like ModelScope, HuggingFace, or GitHub, the accessibility tree (`browser_snapshot`) often misses content loaded via JavaScript (e.g., benchmark tables in "Model cards", hidden tabs).

## Workflow

### 1. Diagnosis
- `browser_snapshot` returns truncated or empty content.
- `browser_vision` sees the text but cannot copy/extract it accurately, or the page is too long to screenshot effectively.
- The content exists in the DOM but is rendered dynamically.

### 2. Extraction Strategy A: `document.body.innerText`
For pages where text is visible but not in the snapshot:
```javascript
// Get all visible text, split by length to avoid truncation limits
var txt = document.body.innerText;
// Return a chunk
txt.substring(START_INDEX, END_INDEX);
```
**Usage in `browser_console`**:
- `expression`: `var t = document.body.innerText; t.substring(0, 5000);`
- Then scroll down or adjust indices: `var t = document.body.innerText; t.substring(5000, 10000);`
- This captures **everything** the user would see, including tables formatted as text.

### 3. Extraction Strategy B: DOM Node Inspection
For structured data (like tables or lists):
```javascript
// Find specific elements (e.g., tables, lists)
var tables = Array.from(document.querySelectorAll('table'));
tables[0].innerText.substring(0, 2000); // Inspect first table

// Or target specific classes
document.querySelector('.prose, .markdown-body, article').innerText.substring(0, 3000);
```

### 4. Extraction Strategy C: Network Interception (Advanced)
If data is loaded via API (check Network tab):
- Look for `fetch` or `xhr` calls in the `browser_console` errors or by inspecting the page source for API endpoints.
- Often, SPAs load JSON data that you can request directly via `terminal` or `web_search` if you find the URL.

## Pitfalls
- **ModelScope/HF**: Benchmark tables are often inside collapsible `<details>` tags or lazy-loaded components. `innerText` is the most reliable way to get the full text without expanding UI elements manually.
- **Truncation**: `browser_console` output has a limit. Always use `substring` to paginate through the text.
- **Login Walls**: Some content requires login. If `innerText` shows "Please login", you've hit a wall.

## Example: Extracting ModelScope Benchmarks
1. Navigate to model page.
2. `browser_console` -> `document.body.innerText.substring(0, 5000)` -> Check if "OpenCompass" or "MMBench" text exists.
3. If yes, extract chunks until you find the table data.
4. Parse the text table into Markdown.