---
name: hermes-os-evolution
description: Evolutionary roadmap and implementation patterns for Hermes Agent OS architecture.
category: devops
version: 1.2.0
metadata:
  tags: [hermes, os-architecture, context-compression, impression-pointer, vfs, capabilities]
---

# Hermes Agent OS Evolution

This skill documents the completed and planned architecture evolution of Hermes Agent, mapping OS concepts to Agent components.

**Origin**: "Architectural Internalization" — mapping external OS concepts (Linux Kernel) to Agent internals to solve context and scalability issues.

## Completed Phases (Roadmap)

### Phase 0: Syscall Audit
- **File**: `model_tools.py`
- **Feature**: Unified `handle_function_call` hook writing to `~/.hermes/logs/syscall_audit.jsonl`.

### Phase 1: Capabilities (Seccomp-lite)
- **File**: `tools/registry.py`
- **Feature**: `ToolEntry` now has a `permissions` dict (fs, net, exec).

### Phase 2: Process Management (SIGTERM)
- **File**: `tools/delegate_tool.py`
- **Feature**: `_active_delegations` registry. `cancel_child_agent()` sets `_interrupt_requested`.

### Phase 3: CFS Scheduler
- **File**: `model_tools.py`
- **Feature**: 5-level `_TOOL_PRIORITY` (P0 Root -> P4 Preemptible).

### Phase 4: VFS Semantic Mounts
- **File**: `tools/file_tools.py`
- **Feature**: `read_file` supports URIs: `wiki://`, `skill://`, `history://`.

### Phase 5: Seccomp Log Rotation
- **File**: `tools/security.py`
- **Feature**: Auto-rotate `syscall_audit.jsonl` when > 10MB.

### Phase 6: Impression-Pointer Memory (Current State)
- **File**: `agent/impression_page.py`, `agent/context_compressor.py`
- **Feature**: Replaces naive LRU Page Tables with **Semantic Impressions**.
- **Architecture**:
  - **ImpressionPage**: `topic_anchor` + `semantic_hash` + `pointer_ref`.
  - **States**: `IN_MIND` (Injected in prompt) -> `SUBCONSCIOUS` (Faded but retrievable) -> `FORGOTTEN` (Deleted).
  - **Mechanism**:
    1. **Encoding**: Extracts anchors/hashes during compression.
    2. **Recall**: Fuzzy matching on `semantic_hash` + `topic_anchor`.
    3. **Page Fault**: If query matches a `SUBCONSCIOUS` impression, triggers `swap_in()` to fetch details.
  - **Pitfall**: Chinese characters in `semantic_hash` require character-level intersection for matching, not word-splitting.

### Phase 6.5: Agchk Self-Audit Integration
- **Repo**: `huangrichao2020/agchk`
- **Feature**: Added `os_architecture.py` scanner to detect these exact patterns.
- **Usage**: Run `.venv/bin/agchk audit /root/hermes-agent` to verify implementation.

## Implementation Guidelines

### 1. Impression-Pointer Integration
When modifying `context_compressor.py`:
- Use `ImpressionTable.decay_all()` before pruning.
- Inject `table.get_active_snippets()` into the summary message.
- Do not store raw text in the table; store the `pointer_ref` (e.g., `session_turns:10-15`) and fetch details on demand.

### 2. VFS Mounts
To add new mounts (e.g. `github://`):
- Add `elif _scheme == "github":` block in `read_file_tool` (before the final `else`).
- Return JSON result matching `read_file` schema (`content`, `total_lines`).
- `history://` is already implemented to call `session_search_tool`.

### 3. CFS Priority
New tools must be added to `_TOOL_PRIORITY` in `model_tools.py` with a priority level 0-4.

## Verification
Run `test_impression.py` to verify the Impression lifecycle (Encoding -> Reasoning -> Decay -> Page Fault -> Forgetting).

## Exception handling & rollback procedures

**Phase implementation failures:**
- If a new phase breaks existing functionality → revert the specific file change via `git checkout <file>` and re-test. Never leave a broken state in production.
- If `test_impression.py` fails after a change → check the `semantic_hash` generation first. Chinese character hashing is the most common failure point; ensure character-level intersection is used, not word-splitting.

**Impression-Pointer edge cases:**
- If `decay_all()` produces NaN or infinity values → clamp impression scores to [0.0, 1.0] range. A score of 0.0 means fully forgotten; do not delete the row immediately (keep for audit trail).
- If `get_active_snippets()` returns empty during context injection → trigger a page fault scan on `SUBCONSCIOUS` impressions before falling back to full session replay. Log the event for debugging.
- If `pointer_ref` format changes (e.g. from `session_turns:10-15` to `session_turns:10-20`) → the old pointer becomes a dangling reference. Implement pointer versioning or add a fallback search by `topic_anchor`.

**VFS Mount failures:**
- If a URI scheme handler throws (e.g. `wiki://` page doesn't exist) → return a structured error JSON `{"error": "not_found", "uri": "wiki://..."}`  rather than a raw Python traceback. This prevents the agent from hallucinating content.
- If `history://` calls `session_search_tool` and the search returns nothing → respond with "No matching history entries found for query: X" instead of empty results.

**Seccomp log rotation:**
- If rotation fails (file locked or permission error) → truncate in-place rather than rotating. Log a warning. Never let audit logging stop entirely.
- If `syscall_audit.jsonl` grows faster than expected (>10MB/day) → check for infinite tool-call loops. This is a symptom of a higher-level agent bug, not a logging issue.

**CFS Priority anomalies:**
- If a new tool is added without a `_TOOL_PRIORITY` entry → it defaults to P4 (lowest). Explicitly assign a priority; silent defaults cause debugging confusion.
- If multiple tools compete for P0 → this indicates an architecture problem. P0 should be reserved for safety-critical operations only (e.g. interrupt handling).

**Agchk verification failures:**
- If `agchk audit` reports missing patterns → verify the file paths referenced in the phase documentation still exist. File renames or moves break the scanner. Update both the skill doc and the scanner config.
- If the scanner reports false positives → check that the pattern regex in `os_architecture.py` matches the actual code style. The scanner is a best-effort tool; manual verification is the ground truth.

**Rollback checklist (when a phase goes wrong):**
1. `git status` — identify changed files
2. `git diff` — review changes before reverting
3. `git checkout <file>` — revert specific files
4. Re-run the relevant test (`test_impression.py`, `agchk audit`)
5. If tests pass → document the failure mode in this skill for future reference
6. If tests still fail → escalate to full `git reset --hard` on the hermes-agent repo