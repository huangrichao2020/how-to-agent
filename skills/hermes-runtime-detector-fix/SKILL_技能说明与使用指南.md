---
name: hermes-runtime-detector-fix
description: Use when the user wants to change or fix a Hermes runtime detector (e.g. looks_like_process_only_reply, route classifier, intent detector) and the live ~/hermes/hermes-agent tree has uncommitted modifications from other work. Combines a self-contained Python demo that proves the fix behavior, with a 7-step WIP-aware patch flow (stash → branch → apply → test → merge → pop).
---

# Hermes Runtime Detector Fix

The Hermes runtime has many text-pattern detectors in
`~/hermes/hermes-agent/run_agent.py` and `gateway/run.py`. Fixing one
of them is dangerous: the live tree is almost always dirty with
uncommitted WIP from other agents or sessions. This skill gives you
a safe, evidence-anchored path.

## When To Use

- "fix `looks_like_process_only_reply` to recognize X"
- "the runtime keeps flagging Y as Z, can you change the detector"
- "update the trigger pattern for skill `foo`"
- any change to a regex / pattern / classifier in the live runtime

## When NOT To Use

- Pure documentation or skill authoring — go to `agent-skill-creator_Skill技能自动构建器`
- New feature in a clean branch — use normal `git checkout -b`
- Runtime config in `~/.hermes/config.yaml` — not a code change
- Code change in a non-runtime repo (e.g. how-to-agent skills) — use
  the normal git flow, no special precautions needed

## Core Stance

**Demo before patch.** Build a self-contained Python file that imports
or re-implements the detector, runs your proposed change against the
existing test cases plus your new cases, and shows a behavior table.
If the table looks right, the patch is small and safe. If the table
fails, you find out in 5 seconds instead of 5 minutes.

```text
1. Read the detector and its tests
2. Write demo.py: import the detector, run a behavior table
3. Verify: existing tests + your new cases pass with the fix
4. ONLY THEN: stash WIP, branch, apply, test, merge, pop stash
```

## The 7-Step WIP-Aware Patch Flow

When the live tree has uncommitted modifications, this is the safe
sequence. The order is load-bearing; do not skip or reorder steps.

```bash
# Step 1: Check WIP exists and record it
cd ~/hermes/hermes-agent
git status --short
# Note all M and ?? files — these are the WIP to preserve

# Step 2: Stash WIP (modified + untracked)
git stash -u
# Verify: git status --short should now be empty (or only gitignored)

# Step 3: Branch from clean main
git checkout -b fix/<short-name>
# e.g. fix/structured-plan-deliverable

# Step 4: Apply patch (via patch tool or write_file)
# - 1-3 file edits, focused
# - Add 1-2 test cases to the existing test file

# Step 5: Run tests
.venv/bin/python -m pytest tests/<path>/<test_file>.py -v
# Must be 100% pass before continuing

# Step 6: Commit + merge to main
git add <files>
git commit -m "fix(<area>): <one-line summary>"
git checkout main
git merge --no-ff fix/<short-name> -m "merge: <summary>"
# --no-ff preserves the branch shape for git log traceability

# Step 7: Pop stash to restore WIP
git stash pop
# If conflict: the WIP file you modified may now collide with the
# merged code. Resolve manually; this is the user's call.
```

### Rollback at any step

| If you fail at step | Rollback |
|---|---|
| 4 (patch bad) | `git checkout -- <file>` or `git stash pop` to abandon |
| 5 (tests fail) | revert patch, re-edit, re-test |
| 6 (commit bad) | `git reset --hard HEAD~1` (only if not pushed) |
| 6 (merge bad) | `git reset --hard <pre-merge-sha>` |
| 7 (stash conflict) | `git stash` to put it back, ask user how to resolve |

## Demo-Before-Patch Pattern

The demo is the load-bearing artifact. It must:

1. **Re-implement or import the detector** — copy the relevant
   function or `from run_agent import looks_like_process_only_reply`.
2. **Define new patterns as separate constants** — keep them
   isolated so the table cleanly shows "OLD vs NEW".
3. **Build a behavior table** with `OLD`, `NEW`, `EXPECTED`,
   `PASS` columns.
4. **Include 3 categories of cases**:
   - **Existing positive**: 3 cases that already pass, must still
     pass with the new code.
   - **The user's exact complaint**: 1 case matching the message
     that motivated the fix. The behavior change MUST be visible.
   - **Edge cases**: 2-3 cases that test the boundary (e.g.
     "options without recommendation", "English vs Chinese").
5. **Print summary**: `OVERALL: PASS` or `OVERALL: FAIL`.

```python
# Template
import re
from run_agent import looks_like_process_only_reply as OLD_fn

def NEW_fn(content):
    # your modified version
    ...

cases = [
    ("existing-1", content, expected_old, expected_new),
    ("user-complaint", content, True, False),  # OLD says process-only, NEW exempts
    ("edge-1", content, expected_old, expected_new),
    ...
]
for name, content, exp_old, exp_new in cases:
    old = OLD_fn(content)
    new = NEW_fn(content)
    print(f"{name:30} OLD={old!r:>5} NEW={new!r:>5} OK={'✓' if (old==exp_old and new==exp_new) else '✗'}")
```

The demo file is the **evidence artifact**. Save it next to your
patch file (e.g. `~/Desktop/xhs-output/runtime-detector-demo.py`)
and reference it in the conversation.

## Anti-Patterns To Avoid

- **Do not edit `run_agent.py` directly with WIP in the tree.**
  You will tangle your change with someone else's; restoring the WIP
  becomes a 30-minute merge resolution.
- **Do not skip the demo and "just try it".** If the fix has a
  bug, you find out from a real Hermes warning in production —
  too late to debug cleanly.
- **Do not over-generalize the patterns.** A 2-line regex that
  matches the user's exact case is better than a 10-line regex
  that "covers all structured plans". Coverage can grow later.
- **Do not push origin/main automatically.** The branch's main may
  have 5+ other unpushed commits from previous work. Pushing is
  the user's call, not yours.
- **Do not pop the stash until merge is on main.** If you pop
  early and then `git checkout main`, you may have to re-stash
  manually.

## Output Contract

For a "fix the runtime detector" task, deliver:

1. **demo.py** — the self-contained behavior table, showing OLD vs
   NEW with explicit PASS/FAIL.
2. **patch.md** — exact code snippets (old → new) for each edit,
   with line numbers and a copy-pasteable diff.
3. **Tests** — added to the existing test file, not a new file.
4. **Git chain** — feature commit + merge commit on main, both
   verified.
5. **Test result** — `5 passed in 5.79s` or equivalent, with no
   regressions.
6. **Rollback path** — explicit instructions for `git revert` or
   `git reset` to undo.

## Real Examples

- **process-only-reply detector** — 2026-06-09 fix:
  - `looks_like_process_only_reply` was flagging "3 方案 + 推荐"
    as process-only when it should be a deliverable
  - Added 2 pattern constants + 1 helper function + 1 exemption line
  - 5 tests pass: 3 old + 2 new
  - Branch: `fix/structured-plan-deliverable` → merged to main
  - See `~/Desktop/xhs-output/process-only-reply-patch.md` for the
    full patch file with all 3 edits and the demo

## Related Skills

- `agent-skill-creator_Skill技能自动构建器` — when you discover a reusable methodology
  (this skill was created via that flow)
- `hermes-rustification-pattern` — when the change is about
  tightening existing runtime code (not detector patterns)
- `morphling-workflow-absorption` — when adapting a pattern from
  another project into the Hermes runtime
