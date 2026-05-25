# Agent Runtime Repair Loop

This note distills GenericAgent changes observed on 2026-05-25.

Use it when an agent runtime has recently changed and you need to turn the
repair work into durable operating knowledge instead of letting it remain as
one-off debugging.

Core rule:

```text
Runtime repair is not complete when the patch works once.
It is complete when the failure mode is named, the live process is verified,
the regression path is covered, and the lesson is archived where the next
agent can find it.
```

## What Changed Recently

Recent GenericAgent commits formed a coherent arc:

| Area | Change | Method lesson |
| --- | --- | --- |
| Feishu rich text | Markdown tables are rendered as proper Feishu rich text | Output surfaces need format-aware rendering, not plain text dumping |
| Task workbench | Task cards now show thinking summaries | Long tasks need visible human-readable progress, not raw tool traces |
| Conversation runtime | Runtime, task runner, lifecycle, smart restart, and hot reload were decoupled | Chat frontends should display work; shared runtime code should own task monitoring |
| Memory docs | Memory and SOP docs were compressed; creative-writing skill was added | Remove stale procedural noise while preserving high-signal skills |
| Lark documents | Provider retries and document creation were hardened | External connectors need explicit retry semantics and tests |

Looking back across a longer recent window, the commits cluster into seven
runtime themes:

| Commit cluster | What it changed | Durable lesson |
| --- | --- | --- |
| Frontend visual gates (`51b5fde`, `04c5078`, `e079616`, `69dbcc9`) | Web presence and motion-video skills were tightened around screenshot/render verification | Visual work is not done until the rendered surface is inspected |
| Cognitive runtime governance (`3200c45` and nearby cognition commits) | Attention governance, cognitive store, dream writeback, token budget, runtime status, and prompt contracts were wired into the loop | Cognition should be observable runtime behavior, not hidden self-talk |
| Runtime evidence ledger (`9414818`, `e5329ed`) | Feishu messages, scheduled context, cognitive events, Rust bridge events, and runtime ledger writes became auditable | Debuggability comes from event evidence, and evidence stores must close resources cleanly |
| Feishu task-flow stabilization (`3f1f392`, `d7dd09e`, `0797457`, `d72888f`) | Raw Feishu intent was preserved, task cards/reactions stabilized, correction follow-ups stayed attached, and plain chat was separated from workbench output | Chat continuity is an event-system contract before it is a prompt problem |
| Local browser and toolchain expansion (`bf90e0f`) | `local_browser_reader.py`, tool schemas, MCP config, loop detection, safe restart skill, and SOP architecture landed together | New tools need schemas, tests, operating notes, and live-environment validation |
| Runtime resilience (`8a39ae9`, `d31a141`) | Stale Rust runtime locks, smart restart, hot reload, lifecycle, and task runner boundaries were separated | Long-running agents need restart boundaries and sidecars that fail cleanly |
| Memory and retrieval (`bfdcb70`, `f8cdfeb`) | MemoryHub episode recall, compressed memory SOPs, and creative-writing skills were updated | Retrieval systems should reduce current-task confusion, not accumulate more text |

This longer view shows the real architecture direction:

```text
output craft
  + conversation continuity
  + event evidence
  + structured cognition
  + restartable runtime boundaries
  + compact durable memory
```

When these move together, the agent starts to feel "alive" not because it has
more prose, but because its process is visible, recoverable, and less likely to
lose the user's latest instruction.

Looking even further back, the 2026-05-17 to 2026-05-19 commits show where
that architecture started:

| Root layer | Representative commits | Method lesson |
| --- | --- | --- |
| Feishu workbench first | `e5a0408`, `789d26b`, `4f672c8`, `03fad96`, `de47907` | Chat agents need an output workbench before long tasks feel trustworthy |
| Cognition as sidecar | `5d484ed`, `e652075`, `38fcf78`, `6fd4a2e`, `dde287d` | Keep cognition visible as a side channel; do not force every ordinary reply through approval ceremony |
| Learning pipeline | `e652075`, `40c7182`, `b3051f9`, `2f904d2` | Learning requests need a direct path, structured artifacts, and practice loops |
| Event substrate | `4cc135b`, `9312eb0`, `5d92357`, `2c74a57`, `e1b3352` | If an agent has many inner states, first make state transitions recordable |
| Hot reload and runtime boundary | `df89283`, `c3cefac` | Frequent runtime evolution needs reload boundaries and predictable sidecar selection |
| Human signal and response tone | `bb5e86b`, `a4c8701`, `061e3ab`, `bf3dd05` | Better agent behavior comes from softer user-facing contracts plus clearer internal evidence |
| Cultivation architecture | `7ee651f`, `eb3f643`, `98366cb`, `da5c21a`, `9e3df52`, `4298340` | Metaphoric architecture is useful only when it maps to tests, tools, and runtime events |

This older layer adds one important caution:

```text
Do not confuse inner architecture with user-facing ceremony.
The runtime may have cognition, cultivation, dream, evidence, and practice loops.
The user should mostly feel: it listened, it kept context, it acted, and it reported clearly.
```

In practice, that means internal subsystems should earn their place by changing
observable behavior: better routing, clearer reports, safer restarts, lower
token waste, more faithful memory, or fewer repeated mistakes.

The pattern is not "add more agent magic." It is a repeated cleanup loop:

```text
bad user experience
  -> find the runtime boundary
  -> make the boundary explicit
  -> add a regression test
  -> restart the real service
  -> archive the lesson
```

## Uncommitted Work Observed

The current uncommitted GenericAgent work has two useful threads.

### 1. Safe Self-Restart Repair

Failure:

```text
request_self_restart imported frontends.fsapp to read TEMP_DIR.
But fsapp is the live entrypoint.
Importing it again re-ran module top-level code and hit the singleton lock.
The worker exited before publishing a done event.
Feishu waited until task timeout.
```

Landing:

- `ga.py` now saves restart notices through `parent.temp_dir` or the project
  `temp/` directory.
- It no longer imports the frontend entrypoint from inside the restart tool.
- `tests/test_self_restart.py` now guards against importing `frontends.fsapp`
  during restart notice saving.
- `agentmain.py` expands restart preflight from three files to the actual
  Feishu startup chain: agent loop, fsapp, Feishu renderers, smart restart,
  tool policy, work state, and tool result contract.

Method lesson:

```text
Never import a live process entrypoint from a shared tool path.
Entrypoints acquire locks, start clients, mutate process state, and may exit.
Shared code should receive runtime paths through parent/context objects.
```

### 2. Structured Work State

New files:

- `work_state.py`
- `tool_result_contract.py`
- `tests/test_work_state_contract.py`
- `tests/fixtures/conversation_eval_cases.json`

Purpose:

```text
Give each live task a compact structured state:
goal, known facts, missing info, current plan, decisions, evidence refs,
user steering, next action, stop criteria, and risk level.
```

The agent loop attaches this state to the next model turn and updates it from
normalized tool results.

Why it matters:

- Long chat history is a weak place to recover exact task state.
- Tool results should become state patches, not just opaque text.
- User follow-ups should update explicit steering, not hide in the transcript.
- Regression fixtures should preserve real failures like "execute 7",
  "second message is a new task", and "short answer to previous question."

Method lesson:

```text
For long agent tasks, maintain a small typed work state beside the transcript.
Let the transcript preserve context, but let WorkState carry operational truth.
```

## Repair Checklist

When GA, Hermes, or another local agent starts acting wrong:

1. Check live process state first.

```text
launchctl print ...
ps ...
tail runtime logs
```

Do not start from theory. Confirm whether the process is alive, restarting,
blocked, duplicated, or merely producing bad output.

2. Separate user-facing failure from internal failure.

Examples:

- User sees no reply.
- Runner waited for `done` and timed out.
- Worker thread exited early.
- Restart preflight blocked exit.
- Singleton lock killed a duplicate import.

Each layer needs a different fix.

3. Name the unsafe boundary.

Useful boundary names:

- frontend entrypoint imported as library
- runtime preflight too narrow
- tool result unstructured
- follow-up message swallowed
- rich text rendered as plain text
- workbench showing trace instead of outcome

4. Patch the smallest runtime boundary.

Prefer:

```text
pass dependency through parent/context
extract shared helper module
add typed result contract
expand preflight coverage
queue or absorb message at event boundary
```

Avoid:

```text
importing entrypoints
adding more prompt-only rules
restarting blindly
swallowing exceptions into generic "failed"
```

5. Add the regression before calling it done.

Good tests for runtime agents are often not full E2E tests. They are compact
failure fossils:

```text
this import must never happen
this short user message must route to the prior frame
this complete new task must queue during an active run
this failed tool result must update missing_info and next_action
```

6. Verify the live service.

For a LaunchAgent-backed service, the patch is not done until:

```text
preflight passes
test subset passes
launchctl kickstart succeeds
new PID is visible
startup log shows websocket/client success
no fresh SyntaxError or singleton lock warning appears
```

7. Archive the method.

Put the lesson in a durable place. The next agent should not need to rediscover
the same failure from raw logs.

## Minimal Prompt

```text
[AGENT RUNTIME REPAIR LOOP]
- Start from live evidence: process, supervisor, logs, queue state, current diff.
- Separate user symptom, runner behavior, worker failure, and root boundary.
- Do not import live entrypoints from shared tools; pass paths/context inward.
- Make tool results structured enough to update work state.
- Add regression fossils for real failures, not only happy paths.
- Expand restart preflight to the imported startup chain.
- Restart the real service and verify PID plus startup success before saying done.
- Archive the lesson into how-to-agent or a skill when it generalizes.
[/AGENT RUNTIME REPAIR LOOP]
```
