# Self-Healing Browser Harness

**Inspired by:** browser-use/browser-harness

**Core Concept:**
Instead of relying on a rigid framework for browser automation, maintain a `browser_helpers.py` script that evolves during the session. The agent writes, tests, and patches helper functions dynamically.

**Workflow:**
1. **Task Analysis**: Break down the user's web task into steps (e.g., "login", "upload", "scrape").
2. **Check Helpers**: Look for existing functions in `browser_helpers.py`.
3. **Write Missing Logic**:
   - If a function is missing or incomplete, use `browser_vision` or `browser_snapshot` to understand the page.
   - Write robust Python code (using Playwright/Selenium) into `browser_helpers.py`.
   - *Self-healing*: If the script throws an error (e.g., element not found), catch it, re-inspect the page, and patch the code immediately.
4. **Execute**: Run the helper. Verify results visually.

**When to use:**
- Complex multi-step web tasks.
- Tasks involving dynamic/obfuscated selectors where standard record-and-replay fails.
- Long-running automation where UI changes are expected.
