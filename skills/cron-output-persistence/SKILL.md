---
name: cron-output-persistence
description: Persist scheduled cron job outputs to gbrain for cross-session retrieval and automatic context injection.
version: 1.0.0
author: Hermes Agent
license: Private
yao_category: "工具类"
---

# Cron Output Persistence Pattern

Use this skill when you want the results of a recurring cron job (like daily learning briefs, market analysis, or system health checks) to be available in future sessions without re-running the task.

## Why?
By default, cron jobs deliver output to a platform (e.g., Feishu/Telegram) but **do not** enter the agent's long-term memory or session context. This leads to "amnesia" where the agent forgets what it discovered overnight.

## The Solution: gbrain Persistence
Instead of complex gateway hooks or file-scanning mechanisms, have the cron job itself write a structured summary to a dedicated gbrain page immediately after generating its output.

### Implementation in Cron Prompt
Add this instruction to your cron job prompts:
```markdown
**Persistence Requirement:**
After generating your report, use `mcp_gbrain_put_page` to append a summary to the gbrain page 'cron-{slug}'.
- Read existing content first with `mcp_gbrain_get_page`.
- Prepend your new entry with a header: `## YYYY-MM-DD HH:MM`.
- Include: Core Changes, Key Takeaways, and Action Items.
- Trim old entries if the page exceeds ~500 lines.
```

### Retrieval
In any session, use `mcp_gbrain_query` or `mcp_gbrain_get_page` to retrieve past outputs.
Example: `mcp_gbrain_get_page(slug='cron-daily-learning-brief')`

## Why NOT Gateway Hooks? (Anti-pattern)
We tested a `cron-broadcast` hook that fired on every `agent:start` event to scan cron output files and inject them into the system prompt. It was **reverted** because:
1. **Overhead**: Scanning files on every user message adds latency.
2. **Complexity**: Merging dynamic context into system prompts can cause prompt bloat and confusion.
3. **Simplicity**: Explicit gbrain retrieval is more predictable, searchable, and keeps the core loop clean.

**Rule:** If a cron job produces valuable insights, it should write them to gbrain itself. The agent retrieves them when needed via `mcp_gbrain_query`.

## Program.md Integration
For research-oriented cron jobs (like daily stock analysis), separate the instructions from the cron configuration using a `program.md` file.
1. Create `/root/.hermes/programs/{name}-program.md` with data sources, rules, and output format.
2. Update the cron prompt to read this file first: "Step 1: Read `/root/.hermes/programs/...` and follow its instructions."
3. This allows you to update research logic without touching the cron job configuration.

## Context Injection (BOOT.md - Optional)
If you want startup awareness without manual retrieval, add a step to `~/.hermes/BOOT.md`:
```markdown
## Load Recent Cron Outputs
1. Use `mcp_gbrain_get_page` to read `cron-{slug}`.
2. If today's entry exists, summarize the "Core Changes" into the startup report.
```