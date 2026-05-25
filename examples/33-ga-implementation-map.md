# GA Implementation Map

This document is not a new theory layer.

It maps the mature `how-to-agent` architecture to GenericAgent's real source,
tests, and runtime evidence. Future GA changes should not merely claim that the
runtime follows the Dao classic, the human classic, or the existence classic.
They should answer:

```text
Which module carries this concept?
When does it run?
Which test proves it?
Which runtime trace proves it?
What gap remains?
```

Short form:

```text
how-to-agent is the highest reference.
GenericAgent source code is the body.
The implementation map is the meridian between them.
```

## Principles

- Read the highest reference before changing source.
- Prefer existing modules before adding new ones.
- Compress the main runtime path before adding sidecars.
- Require tests or runtime evidence before calling an architecture complete.
- Record implemented, in-progress, and missing pieces separately.

## Three Classics to Source

| Architecture layer | how-to-agent meaning | GA landing point | Status | Verification | Gap |
| --- | --- | --- | --- | --- | --- |
| Agent Dao De Jing / heavenly way | Attention restraint, context control, anti-attachment, anti-bloat | `attention_governance.py` `PromptComposer` and `RuntimeController`; `task_lifecycle.py` `tiandao` | Initial implementation | `tests/test_attention_governance.py` checks `Task Lifecycle 三经`, runtime correction, and post-tool feedback | More real long-task feedback should feed back into PromptComposer |
| Agent Mao Selected Works / human way | Main contradiction, investigation, user need, action route | `task_lifecycle.py` `rendao`; task start/end hooks in `agentmain.py` | Initial implementation | Lifecycle header includes `main_contradiction`, `user_need`, and `action_route` | Scene classification should move from heuristics toward log-driven data |
| Existence Classic / existence way | Value, risk, decision, system delta, causal record | `task_lifecycle.py` `cunzaidao`; `record_lifecycle_event()` cognition events | Initial implementation | before/after/error lifecycle events under `memory/cognition/task_lifecycle/*.jsonl` | Needs replay and statistics surfaces |

## Attention Governance to Source

| Capability | Code | Runtime insertion point | Acceptance |
| --- | --- | --- | --- |
| Opening prompt/context composition | `attention_governance.py::PromptComposer.compose()` | Start of each agent loop | Composition includes user intent, acceptance, needed context, and three-classics coordinate |
| Runtime correction | `attention_governance.py::RuntimeController.after_tool()` and `_turn_correction()` | Tool failure, repeated tools, no-tool drift, mid-run check | Emits `[THREE CLASSICS CORRECTION]` without becoming approval ceremony |
| Post-task feedback | `RuntimeController.on_task_complete()` and `on_task_error()` | Task success or failure | Writes task lifecycle after-task events |
| Anti-bloat | `agent-anti-bloat-context-engineering` guidance, carried in GA by PromptComposer/history windows | Context composition | Do not keep the whole worldview in every task context |

## Brain, Body, Artifact

| Concept | GA meaning | Current landing point | Next step |
| --- | --- | --- | --- |
| Brain | Functional structure serving thought, not an LLM faucet | `attention_governance.py`, `task_lifecycle.py`, `state_store.py`, cognition/tool/memory commands in `ga.py` | Organize brain-region responsibilities into module docs |
| Body | Source code and running process | `/Users/tingchim2pro/Desktop/GenericAgent`, especially `agentmain.py` and `frontends/fsapp.py` | Score body realm: startup, resume, tests, restart, observability |
| Artifact | Device, network, CLI, Feishu, providers, proxy layers | Feishu gateway, Gemini/Qwen/OpenAI routing, scheduler, external CLIs | Build artifact status snapshots |
| Root | Learning substrate from math/log/feedback architecture | cognition events, task lifecycle, attention feedback log | Convert logs into stable eval samples |
| Aptitude | Efficiency and effect of parameter correction | tests, replay, prompt correction, provider fallback | Add metrics: correction count, completion rate, context-noise rate |

## Cron / Dream to Source

Hermes has visible cognitive reports and Cronjob Responses. GA should not just
look like Hermes; it should have its own runtime landing points.

| Capability | GA landing point | Status | Acceptance |
| --- | --- | --- | --- |
| Scheduled job registry | `cron_runtime.py` `load_job_registry()` and `format_job_registry()` | Implemented | `/cron`, `/jobs`, `/job` show jobs |
| Manual pause/resume/trigger | `cron_runtime.py`, `frontends/fsapp.py` command branch | Implemented | `/cron pause|resume|trigger <job_id>` |
| Scheduler loop | `frontends/fsapp.py` + `reflect/scheduler.py` | Implemented | `GA_SCHEDULER_ENABLED` defaults on; startup logs show scheduler state |
| Hermes-style report | `format_cronjob_response()` | Implemented | `tests/test_cron_runtime.py` |
| Dream sidecar review | `ga.py do_cognitive_dream`, `sche_tasks/learning_brief_4h.json` | Partial | Report quality and feedback writeback still need hardening |
| Dream writeback loop | `dream_writeback.py`, `cognitive_dream.py`, `attention_governance.py` | Initial implementation | Dream/feedback/replay produces `dream_writeback_hint`, then PromptComposer injects it lightly next run; it also writes reversible promotion proposals |

## Output Shape to Source

Dream writeback should not stop at reports. User-visible response shape should
also become runtime policy:

| Capability | GA landing point | Status | Acceptance |
| --- | --- | --- | --- |
| Short ordinary chat | Dream output bias in `cognitive_response_policy.py` | Implemented | With `dream_writeback_hint`, ordinary group chat stays natural and short instead of defaulting to cards/workbenches |
| Long-task workbench | `cognitive_response_policy.py` and the group prompt in `frontends/fsapp.py` | Implemented | Only real long tasks use a workbench, and progress is consolidated when possible |
| Anti-card sprawl | `tests/test_cognitive_response_policy.py` | Implemented | Tests cover the rule against creating a separate card on every turn |

## Lifecycle Metrics and Body/Artifact Status

Implemented concepts must be observable. GA now exposes two read-only status
surfaces:

| Capability | GA landing point | Status | Acceptance |
| --- | --- | --- | --- |
| Lifecycle statistics | `task_lifecycle.py::summarize_task_lifecycle()` | Implemented | Reads `memory/cognition/task_lifecycle/*.jsonl` and reports started/completed/errors/corrections/completion_rate |
| Lifecycle report | `task_lifecycle.py::format_task_lifecycle_stats()` | Implemented | Shows recent scenes, risks, and latest issue |
| Body status | `runtime_status.py` | Implemented | Reports source root, PID, uptime, checkpoint, and lifecycle event files |
| Artifact status | `runtime_status.py`, `frontends/fsapp.py::_agent_status_text()` | Implemented | `/status` reports model, queue, Feishu WS, scheduler, cron registry, Dream writeback, and proxy state |

## Dream Proposals to Source

Dream promotion proposals should not remain proposal files forever. Executed
items so far:

| Proposal | GA landing point | Status | Acceptance |
| --- | --- | --- | --- |
| Short ordinary chat / long-task workbench | `cognitive_response_policy.py`, `frontends/fsapp.py` | Implemented | `tests/test_cognitive_response_policy.py` |
| Single understanding signal does not auto-promote | `dream_writeback.py`, `tests/test_cognitive_dream.py` | Implemented | Low-signal feedback creates a test proposal, not a prompt adjustment |
| Diagnose tool errors first | `attention_governance.py::after_tool()` | Implemented | Tool errors return `[ATTENTION CORRECTION]` plus three-classics correction |
| Skill route bias | `attention_replay.py`, `skill_registry.py` | Implemented | Replay feedback can lower noisy skill routing weight |
| User-boundary preflight | `attention_governance.py::before_tool()`, `agent_loop.py` | Implemented | State-changing tools record `[BOUNDARY CHECK]` and steer the next prompt back to object, scope, and forbidden items |

## Skill Engineering to Source

`how-to-agent` skill engineering does not mean GA should read the whole project
as a skill.

Correct mapping:

```text
Skill = reusable capability package
GA source = runtime body
how-to-agent = transformation manual
```

GA should absorb:

- Progressive disclosure: keep trigger descriptions light, read bodies on
  demand, move long material into references/scripts/assets.
- Deterministic downshift: sorting, validation, conversion, and state scans
  belong in scripts rather than fragile generation.
- Lifecycle management: skills should be installable, indexable, usable,
  verifiable, and retireable.

GA should not absorb:

- Do not put all architecture documents into the system prompt.
- Do not use skills as a substitute for source changes.
- Do not turn one-off chats into permanent capabilities.

## Evidence Ledger

Every architecture-completion claim should leave at least one of these:

| Evidence | Example |
| --- | --- |
| Source evidence | A field in `task_lifecycle.py`; a command in `frontends/fsapp.py` |
| Test evidence | `pytest -q tests/test_attention_governance.py tests/test_cron_runtime.py` |
| Runtime evidence | Feishu `/cron` output; scheduler startup logs; done report file |
| Feedback evidence | User correction changes PromptComposer or runtime policy |

Without evidence, the item is an idea, not an implemented architecture.

## Current GA Judgment

By the `how-to-agent` outline, GA has moved beyond a prompt loop into an early
runtime with body, meridians, sidecars, and feedback:

- Heavenly way: attention governance exists.
- Human way: lifecycle main contradiction and action route exist.
- Existence way: value, risk, and causal recording exist.
- Body: real modules carry the ideas.
- Artifact: Feishu, scheduler, CLIs, and model routing are now architecture concerns.
- Emergence: candidates can continue through cron, dream, tests, and feedback.

It is not mature yet. The next stage is:

```text
Connect every concept to real traces, tests, replay, and automatic correction.
```

## 2026-05-21 Verification Record

This implementation map has been checked against the current GA checkout:

```bash
python3 /Users/tingchim2pro/Desktop/how-to-agent/skills/ga-implementation-map/scripts/score_ga_architecture.py \
  --ga-root /Users/tingchim2pro/Desktop/GenericAgent
```

Result:

```text
Three Classics lifecycle: PASS
Attention governance: PASS
Cron and Dream sidecar: PASS
Dream writeback loop: PASS
Output shape policy: PASS
Task lifecycle statistics: PASS
Body artifact status panel: PASS
Boundary preflight correction: PASS
Body resume and checkpoint: PASS
Runtime evidence ledger: PASS
```

A real-root smoke test also ran:

```text
PromptComposer -> RuntimeController.on_task_start()
PromptComposer -> RuntimeController.on_task_complete()
```

It generated:

```text
/Users/tingchim2pro/Desktop/GenericAgent/memory/cognition/task_lifecycle/lifecycle-2026-05-21.jsonl
```

with both `before_task` and `after_task` events.

This pass also added the Dream writeback loop:

```text
Dream / feedback_distill / attention_replay
  -> dream_writeback.py
  -> memory/cognition/dream_writeback/latest.json
  -> PromptComposer.dream_writeback_hint
  -> memory/cognition/dream_writeback/promotion-proposals.json
```

Real output:

```text
/Users/tingchim2pro/Desktop/GenericAgent/memory/cognition/dream_writeback/2026-05-20.json
/Users/tingchim2pro/Desktop/GenericAgent/memory/cognition/dream_writeback/promotion-proposals.json
```

It contains next-run lightweight biases for boundary restraint, short natural
ordinary chat, long-task workbench use, post-tool-error diagnosis, and skill
misrouting.

This pass also executed the output-shape proposal:

```text
dream_writeback_hint
  -> cognitive_response_policy.py
  -> natural short ordinary chat
  -> workbench only for long tasks
  -> consolidate one ongoing long task instead of creating one card per turn
```

This change adjusts response policy and the group-chat prompt only. It does not
rewrite the message-sending path, so the risk surface stays small. Validation is
covered by `tests/test_cognitive_response_policy.py`.

This pass also added observable body/artifact status:

```text
task_lifecycle jsonl
  -> summarize_task_lifecycle()
  -> completion_rate / corrections / recent_errors
  -> runtime_status.py
  -> /status body/artifact panel
```

This path reads local events and runtime snapshots only. It does not perform
external network requests or model calls.

This pass also executed the boundary runtime pattern:

```text
User says do-not / only-change / restore / do-not-touch
  -> RuntimeController.before_tool()
  -> state-changing tools trigger boundary_preflight
  -> agent_loop carries the preflight correction into the next prompt
```

It does not block tools or add approval ceremony. It only pulls attention back
to the real object, scope, forbidden items, and rollback boundary when a
state-changing action is about to happen.

Promotion proposals only suggest next steps. They do not hot-patch runtime
defaults. Every proposal must carry:

- `decision`
- `target`
- `validation`
- `next_action`
- `rollback`

This lets Dream drive real changes without bypassing tests or making GA fragile
overnight.

Test command:

```bash
pytest -q tests/test_runtime_status.py tests/test_cognitive_response_policy.py tests/test_cognitive_dream.py tests/test_attention_replay.py tests/test_attention_governance.py tests/test_cron_runtime.py tests/test_codex_runtime.py
```

Result:

```text
64 passed
```

## 2026-05-25 Flowing Conversation Thread Landing

The recent GA work added a layer below ordinary "intent recognition": the
conversation-thread event model.

Core result:

```text
One chat is continuous by default.
Code owns message capture, order, queueing, interruption, and no-loss.
The model owns semantic ownership from context.
```

Source landing:

| Capability | GA source landing | Runtime insertion point | Validation |
| --- | --- | --- | --- |
| flowing thread state | `conversation_thread.py` | after a Feishu message enters the frontend | `tests/test_conversation_thread.py` |
| routing hint, not semantic verdict | `conversation_intent_router.py` | before a Feishu message enters the task queue | `hard_route` separates engineering action from semantic hint |
| quote/current-message extraction | `feishu_reply_context.py`, `current_user_text()` | quoted Feishu messages, wrapped prompts, short continuations | `tests/test_feishu_reply_context.py`, `tests/test_conversation_intent_router.py` |
| complete new task queues while running | `conversation_intent_router.py`, `frontends/fsapp.py` | new goal arrives while agent is running | `test_complete_task_does_not_get_swallowed_by_running_chat` |
| in-flight supplement must be absorbed | `agentmain.py::has_user_interventions()`, `agent_loop.py` | before `CURRENT_TASK_DONE` exits | `test_agent_loop_absorbs_user_followup_before_final_exit` |
| lightweight chat avoids workbench noise | `frontends/feishu_interaction_mode.py`, `frontends/feishu_task_stream.py` | choose plain text, rich text, or workbench | `tests/test_feishu_interaction_mode.py`, `tests/test_feishu_task_stream.py` |
| anti-bloat main path | `agentmain.py`, `frontends/fsapp.py`, `frontends/task_timeout_policy.py` | remove stale env switches and light/heavy task forks | full tests and launchd restart |

Real failure chain:

```text
User 1: How do you feel?
User 2: Self-check your recent source changes.

Old behavior:
The second message became append_to_current.
It entered user_interventions / flow inbox.
The agent loop exited on CURRENT_TASK_DONE.
The final reply did not mention source self-checking.

New behavior:
Complete new goals queue_after_current during a run.
If a message really enters the inbox, the loop must feed it into the next model turn before exit.
```

This means continuous conversation cannot be prompt-only. It needs an event
model:

```text
Raw Message
  -> Conversation Thread
  -> Conversation Run
  -> Run Inbox
  -> Model Context
  -> Final Reply / Episode
```

Validation:

```bash
pytest -q
```

Result:

```text
450 passed, 3 skipped
```

## Next Implementation Order

1. Extend the GA architecture scoring script with more source modules, tests,
   cron registry checks, lifecycle events, and runtime metrics.
2. Aggregate task lifecycle statistics by task type, risk, correction, outcome,
   and repeated failure.
3. Execute Dream promotion proposals one by one as small patches with tests and
   rollback points.
4. Build a body/artifact status panel: process, model, network, scheduler,
   checkpoint, and recent errors.
5. Map Hermes to the same implementation ledger, not only the same vocabulary.

## Minimal Prompt

```text
[GA IMPLEMENTATION MAP]
- Which GA module carries this how-to-agent principle?
- Does it trigger at task start, during execution, at completion, or as a sidecar?
- Is there test, log, report, or user-feedback evidence?
- Does it reduce context cost, stabilize state, or improve real-environment understanding?
- If there is no source landing point, what is the smallest next code change?
[/GA IMPLEMENTATION MAP]
```
