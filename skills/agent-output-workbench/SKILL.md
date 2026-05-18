---
name: agent-output-workbench
description: "Use when designing or debugging Feishu/chat output streams for long agent tasks: progress, tool calls, outputs, task cards, and final conclusions."
version: 1.1.0
---

# Agent Output Workbench

Use this skill when a chat agent feels flat, robotic, or unclear during tool-heavy work, especially in Feishu group or private conversations.

## Principle

Separate the live conversation from the workbench.

Short conversational replies should stay as normal text. Long tool-driven work should become a clear workbench with task planning, tool calls, outputs, and conclusion. Do not put every reply into a card. A card is useful only when the work has structure.

## Output Modes

Choose the lightest surface that matches the job:

| Situation | Surface |
|---|---|
| Casual chat, short answer, feeling check | Plain text |
| Markdown answer with light structure | Rich text / post |
| Long task with tools, files, research, or code | Workbench card |
| Scheduled report or restart report | Compact report card |
| Very long job | Workbench card plus append-only artifact |

## Workbench Shape

A long-task card should contain these sections:

1. Status: running, completed, blocked, or needs user input.
2. Tasks: `Task 1`, `Task 2`, `Task 3`, each with a clear purpose.
3. Actions: human-readable translations of the actual tools used.
4. Results: what each tool produced or changed, not just that it ran.
5. Conclusion: what the user should know now.
6. Next action: only when there is a useful next step.

Minimum card skeleton:

```markdown
## Tasks
1. Gather source material
2. Inspect core files
3. Produce conclusion and next action

## Execution
### Turn 1
**Action**
- Clone or inspect repository
**Result**
- Repository fetched; README and file tree are available for analysis.

### Turn 2
**Action**
- Read `README.md`
**Result**
- Extracted project goal, structure, and operating assumptions.

## Conclusion
...
```

## Progress Stream

Progress should show real state, not decorative noise.

Good progress:

- "Reading README and config."
- "Running targeted test."
- "Restarting gateway, waiting for Feishu websocket."
- "Tool finished: 7 tests passed."

Bad progress:

- Repeating "thinking".
- Dumping raw JSON without summary.
- Showing only tool calls with no results.
- Turning every short reply into a formal card.

## Tool Completion Rule

Every `tool.started` event needs a matching useful completion signal.

At minimum, capture:

- tool name
- duration
- error flag
- result preview
- produced files or changed paths
- verification result when available

If the runtime only records starts and ignores completions, the card will look busy but empty. Fix the event path first, then improve card rendering.

## Trace Translation Rule

Raw traces are for debugging. User-facing cards should translate them.

Examples:

| Raw tool | User-facing action |
|---|---|
| `file_read({"path": ".../USER.md"})` | Read `USER.md` |
| `file_patch({"path": ".../USER.md", ...})` | Update `USER.md` |
| `execute_code({"code": "curl ..."})` | Fetch external or market data |
| `delegate_task({"tasks": [...]})` | Run parallel research on N directions |

Show raw tool traces only behind an explicit debug flag or in a developer log.
Never dump `_runtime_warning`, `original_result`, oversized JSON, or repeated
tool envelopes into a Feishu card.

## Task Planning Rule

Task sections should reflect the actual job, not a generic template.

Common mappings:

- clone, search, web lookup -> "Gather source material"
- `rg`, `find`, `file_read` -> "Inspect core structure"
- `apply_patch`, `file_write` -> "Implement change"
- tests, compile, service status -> "Verify result"
- final answer -> "Summarize conclusion"

If the model already wrote good task headings, preserve them. If not, infer a small task list from the tool sequence.

## Human Tone

The card can be structured without sounding like a machine.

Keep the user-facing conclusion plain:

- Say what changed.
- Say what was verified.
- Say what remains uncertain.
- Avoid making the user inspect raw tool traces unless they need them.

## Verification

After changing an output pipeline, test at least these cases:

- casual multiline chat stays plain text
- lightweight markdown stays rich text/post
- long tool trace becomes workbench card
- card includes task planning, actions, results, and conclusion
- failed tool shows a useful error output
- restart or scheduled report remains compact

Validated production repair, 2026-05-18:

- GA Feishu output stream now consumes tool results and renders human actions
  plus results instead of raw args.
- Hermes Feishu workbench suppresses raw `execute_code` / `delegate_task` JSON
  and summarizes results.
- GA full suite passed `264 passed, 3 skipped`; GA audit scored 100.
- Hermes Feishu output tests passed on the M1 runtime.

## Anti-Pattern

Do not solve weak output by adding more ceremony to the main agent loop. Output structure belongs near the channel renderer and progress event path. Cognition should inform tone, memory, skills, and judgment; it should not block the reply path or hide tool results behind policy layers.
