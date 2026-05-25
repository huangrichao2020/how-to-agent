# Agent Flowing Conversation Thread

Many chat agents fail at multi-turn conversation not because the model cannot
understand context, but because the runtime cuts user messages into isolated
tasks before the model can reason over them.

Bad smell:

```text
User: How do you feel?
User: Self-check your recent source changes.

Runtime routes the second message as a supplement to the first lightweight
reply. The first reply exits. The second message never reaches the next model
turn. The user experiences this as "the second message did not get answered."
```

This is an event-model bug, not just an intent-classification bug.

Core rule:

```text
Every user message in the same chat belongs to one flowing conversation thread by default.
Code must prevent loss, disorder, and swallowed tasks.
The model should judge semantic ownership from the thread context.
```

## Codex-Like Handling

The Codex-style feel comes from a simple discipline:

```text
Every new user message enters the current thread context.
The model re-reads: latest message, current work, prior turns, and tool state.
Then it decides whether the message is a supplement, correction, follow-up,
new task, or interruption.
```

Code should not hard-code the full semantic ownership problem. Code should only
enforce engineering boundaries:

- Capture every message.
- Preserve order.
- Let short running-task supplements enter the active run.
- Queue complete new goals that arrive during another run.
- If a supplement enters the active run, the loop must absorb it before final exit.
- The final answer must reflect newly absorbed user messages.

## Four-Layer Event Model

### 1. Raw Message

Each user message is first stored as fact.

```json
{
  "message_id": "om_...",
  "thread_id": "feishu:chat:...",
  "created_at": 1779660000.0,
  "text": "Self-check your recent source changes.",
  "attachments": [],
  "quoted_message_id": "",
  "source": "feishu"
}
```

Do not interpret at this layer.

### 2. Conversation Thread

One chat window is a continuous thread. It owns recent messages, active run,
recent finished runs, quote relations, and user guidance.

```json
{
  "thread_id": "feishu:chat:oc_xxx",
  "active_run_id": "run_...",
  "recent_run_ids": ["run_3", "run_2", "run_1"],
  "updated_at": 1779660000.0
}
```

### 3. Conversation Run

A run is a work unit in progress or recently completed.

```json
{
  "run_id": "run_...",
  "thread_id": "feishu:chat:oc_xxx",
  "status": "running|queued|done|failed",
  "active_goal": "what the user is trying to accomplish",
  "message_ids": ["om_1", "om_2"],
  "inbox": []
}
```

A run is not "one message equals one task". It is the current worksite of user
intent.

### 4. Run Inbox

Messages that arrive during a running task may enter the run inbox, but the
inbox must not become a black hole.

```json
{
  "item_id": "inbox_...",
  "kind": "supplement|correction|answer",
  "route": "append_to_current",
  "text": "Also add tests.",
  "consumed_at": 0
}
```

Hard rule:

```text
If the inbox has unconsumed messages, the agent loop must not exit on CURRENT_TASK_DONE.
It must format the inbox into the next model turn and let the model reason again.
```

## Routing Is Not Judgment

The router output should be a hint, not a semantic verdict.

```json
{
  "route": "append_to_current|queue_after_current|interrupt_current|resume_previous|new_task",
  "intent": "continue|supplement|correction|new_task|chat|answer",
  "target_frame_id": "frame_...",
  "confidence": 0.82,
  "hard_route": true,
  "evidence": ["current task is running", "message looks like a complete new task"]
}
```

The key field is `hard_route`:

- `hard_route=true`: the runtime must perform an engineering action such as
  queue, interrupt, or append.
- `hard_route=false`: this is only context evidence; the model may override it.

This prevents two failures:

- Code treats "execute 7" as unrelated small talk.
- Code swallows "self-check source changes" into a lightweight chat reply.

## Complete New Goals Must Not Be Swallowed

When a message arrives during a run, ask one engineering question:

```text
Is this a complete new work goal?
```

If yes, queue it after the current task.

```text
Current run: answer "How do you feel?"
New message: "Self-check your recent source changes."
=> queue_after_current
```

Only short continuation should append:

```text
continue
execute 7
also add tests
not that, I meant local source
=> append_to_current
```

This boundary does not replace model understanding. It prevents message loss.

## Prompt Assembly

The model should see a compact evidence package:

```text
### Current User Message
Self-check your recent source changes.

### Routing Hint
- route: queue_after_current
- intent: new_task
- hard_route: true
- reason: complete new goal arrived while another task was running

### Recent Thread
- previous user message: How do you feel?
- current run: lightweight chat reply
- queue: self-check recent source changes
```

For active-run supplements:

```text
### Current Flowing Thread Run Inbox
- kind: supplement
- route: append_to_current
- text: Also add tests.

Treat the user's added message as a new constraint for the current task.
Do not say the prior message was interrupted.
```

## Relationship To MemoryHub

Flowing conversation threads solve current-session continuity.

MemoryHub solves cross-day, cross-task, cross-session recovery.

```text
Raw Message
  -> Conversation Thread / Run / Inbox
  -> current prompt
  -> completion becomes an Episode
  -> MemoryHub can recover it later
```

Do not push all live conversation continuity into long-term memory. If the
thread can solve it, solve it in the thread.

Do not expect the current thread to solve cross-day recovery. If the thread is
gone, retrieve the episode/worksite from MemoryHub.

## Output Pairing

A flowing thread does not mean every message becomes a card.

Output rules:

- Casual chat: plain text.
- Light Markdown: rich text.
- Tool-heavy work: one editable workbench card.
- Final answer: separate report.
- Tool details: aggregated in a collapsible workbench, not spammed.

User experience and tool experience are separate:

```text
The user feels a continuous conversation.
Tool state updates quietly in a stable workbench.
The finished task produces a clear report.
```

## GA 2026-05-25 Evidence

GenericAgent's 2026-05-25 repair validated this pattern:

| Problem | Cause | Landing |
| --- | --- | --- |
| second message got no reply | complete new task was routed into `append_to_current` | `conversation_intent_router.py` queues complete goals during a running task |
| inbox did not affect output | loop exited on `CURRENT_TASK_DONE` before draining follow-up | `agent_loop.py` checks `has_user_interventions()` before final exit |
| "execute 7" was not understood | wrapped prompt hid the live user turn | `current_user_text()` and ordinal-action recovery |
| lightweight chat became workbench noise | output layer did not separate light interaction from long task | `frontends/feishu_interaction_mode.py`, `feishu_task_stream.py` |
| architecture was becoming patch soup | too many switches and prompt-level patches | fixed main path, removed stale knobs |

Validation:

```text
pytest -q
450 passed, 3 skipped
```

Key regression tests:

```text
test_complete_task_does_not_get_swallowed_by_running_chat
test_agent_loop_absorbs_user_followup_before_final_exit
test_short_continue_still_appends_to_running_task
test_supplement_still_appends_to_running_task
```

## Minimal Prompt

```text
[FLOWING CONVERSATION THREAD]
- Treat one chat as continuous by default.
- Code owns capture, order, queueing, interruption, and no message loss.
- The model owns semantic ownership from context.
- Queue complete new goals during a run; append short supplements, corrections, and answers.
- The inbox is not a log sink; absorb unconsumed user messages before final exit.
- Keep user conversation natural and aggregate tool state in an editable workbench.
[/FLOWING CONVERSATION THREAD]
```
