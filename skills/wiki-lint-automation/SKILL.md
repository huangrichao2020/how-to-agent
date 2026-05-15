---
name: wiki-lint-automation
description: Workflow for automating LLM Wiki health and lint checks. Fixes broken links, eliminates orphans via overview indexing, and registers tools into the Hermes agent runtime.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wiki, lint, automation, research]
    category: devops
    related_skills: [llm-wiki]
---

# Wiki Lint Automation

This skill documents the process of integrating `SamurAIGPT/llm-wiki-agent` structural checks into the Hermes Agent native toolset.

## Core Philosophy
- **Health (Deterministic):** Zero LLM calls. Checks for empty files, index sync, and log coverage.
- **Lint (Structural + Semantic):** Checks for orphans, broken links, missing entities, and graph-aware issues.
- **Zero Orphans/Broken Links:** The goal is a fully connected knowledge base. Use `overview.md` as a "catch-all" index to eliminate orphans.

## Implementation Steps

### 1. Tool Registration
Move scripts from `skills/research/llm-wiki/references/` to `tools/`. Register them using `registry.register()`.

**Key Logic for Broken Link Repair:**
- Match `[[Target|Alias]]` format correctly by splitting on `|`.
- If a target doesn't exist, downgrade the link to plain text `(Target)` to prevent false positives in future scans.

**Key Logic for Orphan Elimination:**
- Scan all pages to build an inbound link map.
- Identify pages with zero inbound links.
- Append a full index of these orphans to `overview.md` using the format `[[filename|Display Name]]`.
- Ensure `overview.md` itself is included in the scanning process so its links count toward resolving orphans.

### 2. Dependency Management
- Install `networkx` for graph-aware checks using `uv pip install "networkx<3.4"` (due to `exclude-newer` constraints in the environment).
- Scripts use only Python stdlib (`re`, `json`, `pathlib`) for core checks.

### 3. Cron Integration
Create a cron job to automatically ingest daily reports into the wiki's `raw/articles/` directory.

```python
# Example Cron Job Creation
cronjob(action='create', name='wiki-daily-ingest', schedule='0 8 * * *', prompt='...')
```

## Exception Handling & Pitfalls

### Script Execution Failures
- **File not found:** Before running `health.py` or `lint.py`, verify the wiki path exists and contains `.md` files. If empty, skip and report "wiki directory not initialized".
- **Python dependency missing:** Wrap imports in try/except. If `networkx` unavailable, skip graph-aware checks and log a warning instead of crashing.
- **Encoding errors:** Open all `.md` files with `encoding='utf-8', errors='replace'` to handle malformed content gracefully.
- **Permission denied:** Catch `PermissionError` when writing to wiki files. If read-only, report as read-only mode and skip fixes.

### Alias Parsing
- Original `lint.py` failed to parse `[[Target|Alias]]`, treating the whole string as a filename. Fix: `link.split('|')[0].strip()`.

### Overview Exclusion
- Originally excluded `overview.md` from scanning, making it impossible for it to resolve orphans. Fix: Include it in `_all_wiki_pages()`.

### SCHEMA.md Orphans
- `SCHEMA.md` is a meta-file. Fix: Exclude it from the orphan report.

### Link Repair Safety
- **Backup before repair:** Always create a `.bak` copy before modifying wiki files. Never do in-place repair without backup.
- **Idempotency:** Running lint-fix multiple times should be safe. If a link is already downgraded to `(Target)`, skip it.
- **Rollback on failure:** If fix script crashes mid-run, restore from `.bak` and report partial state.

### Race Conditions
- If the wiki is being written to simultaneously (e.g., ingest + lint), use file locking or sequential execution. Never run `lint.py` during an active ingest.

## Usage
- `wiki_health`: Run structural checks.
- `wiki_lint`: Run deep structural and graph analysis.
- `ingest <file>`: Add new content to the wiki.
