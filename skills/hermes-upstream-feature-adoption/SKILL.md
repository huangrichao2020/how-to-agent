---
name: hermes-upstream-feature-adoption
description: Methodology for selectively adopting upstream features from NousResearch/hermes-agent without blind merging. Focuses on extracting core logic and customizing it for the local 2GB memory environment and Phase 6 architecture.
---

# Hermes Upstream Feature Adoption Strategy

## Core Principle
**"Extract Logic, Customize Code."** Never blindly merge large upstream commits (e.g., 250+ commits) as they often conflict with local Phase 6 modifications (Impression-Pointer, OS-style audit hooks) and introduce unnecessary bloat for a 2GB server.

## Decision Framework
1.  **Analyze Impact**: Does this feature solve a critical pain point (e.g., stability, search accuracy, goal tracking)?
2.  **Assess Complexity**: Is it a standalone patch or a deep architectural change?
3.  **Check Compatibility**: Will it break `agent/impression_page.py`, `run_agent.py` CFS scheduler, or `tools/registry.py`?

## Implementation Patterns

### 1. The "Patch" Pattern (Standalone Logic)
*   **Use Case**: Small, self-contained fixes (e.g., Fallback Init, Auth handling).
*   **Action**: Use `git show <commit>` to extract the diff. Manually apply relevant parts using `patch` tool.
*   **Example**: Adopting `fix(agent): try fallback providers at init`.
    *   Extract logic from `run_agent.py`.
    *   Inject into local `AIAgent.__init__` before the primary provider check.
    *   Ensure `_fallback_activated` flag integrates with local credential pool.

### 2. The "Surgical" Pattern (Database/Schema Changes)
*   **Use Case**: Database optimizations (e.g., Trigram FTS5 for CJK search).
*   **Action**: 
    *   Do NOT replace `hermes_state.py`.
    *   Extract only the SQL migration scripts (CREATE VIRTUAL TABLE, TRIGGERS).
    *   Write a standalone migration script that checks for table existence before applying.
    *   Update the search query logic in `SessionDB.search_messages` to use the new index if available.

### 3. The "Lite" Pattern (Complex Features)
*   **Use Case**: Heavy features like `/goal` (Ralph Loop) which add 500+ lines of state management.
*   **Action**: Re-implement the *concept* using existing local infrastructure.
    *   **Upstream**: Complex state machine + Judge Model API calls.
    *   **Local Lite**: Use a persistent file (`~/.hermes/active_goal.md`) injected into the system prompt.
    *   **Benefit**: Zero new dependencies, minimal code, leverages existing context compression.

## Recent Adopted Examples (2026-05-03)

1.  **Fallback Init (#17929)**: 
    *   *Logic*: If primary provider fails at init, try fallback chain before crashing.
    *   *Implementation*: Patched `run_agent.py` L1377-L1419 to iterate `_fb_entries`.
2.  **Trigram FTS5 (#16651)**: 
    *   *Logic*: Better CJK search via trigram tokenization.
    *   *Implementation*: Added SQL to `hermes_state.py` and created `scripts/migrate_trigram_fts.py` for backfilling.
3.  **Lite Goal Manager**: 
    *   *Logic*: Persistent cross-turn goals without heavy judge models.
    *   *Implementation*: Created `hermes_cli/goals.py` (50 lines) that reads/writes `~/.hermes/active_goal.md` and injects it into the prompt.

## Verification Steps
1.  **Syntax Check**: `python -m py_compile <modified_file>`
2.  **Import Test**: `python -c "from run_agent import AIAgent; print('OK')"`
3.  **Functional Test**: Run a short conversation or specific tool call related to the change.
4.  **Memory Check**: Ensure the change doesn't cause memory leaks (monitor `RSS` during operation).

## Common Pitfalls to Avoid
-   **Merging UI/TUI changes**: We primarily use Feishu/CLI. Ignore upstream React/Ink changes unless explicitly requested.
-   **Over-engineering**: If upstream uses a new library, ask: "Can we do this with stdlib or existing deps?" (Constraint: 2GB RAM).
-   **Ignoring Local Hooks**: Ensure new code respects `agent/prompt_builder.py` hooks and `tools/registry.py` permissions.