---
name: agent-flowing-conversation-thread_流式对话线程与上下文贯通
description: Use when designing or fixing chat-agent continuity, Feishu/WeChat multi-message ownership, in-flight user guidance, task queueing, inbox absorption, and Codex-like conversation feel.
---

# Agent Flowing Conversation Thread

Use this skill when a chat agent cuts a continuous conversation into isolated
tasks, swallows a second user message, or forces every turn through a rigid task
framework.

Core rule:

```text
One chat is continuous by default.
Code owns capture, order, queueing, and no message loss.
The model owns semantic ownership from context.
```

## Runtime Model

Use four layers:

```text
Raw Message
-> Conversation Thread
-> Conversation Run
-> Run Inbox
```

- Raw Message: factual message capture, no interpretation.
- Thread: continuous chat context.
- Run: current worksite, not one message.
- Inbox: in-flight supplements, corrections, or answers; never a black hole.

## Routing Rule

Routing output is a hint, not the final semantic verdict.

Separate:

- `hard_route=true`: the runtime must perform an engineering action such as
  interrupt, queue, or append.
- `hard_route=false`: only context evidence; the model may override it.

During a running task:

- Complete new goal: `queue_after_current`
- Short continuation: `append_to_current`
- Supplementary constraint: `append_to_current`
- Ordinary correction: `append_to_current`
- Explicit interruption or priority switch: `interrupt_current`

## Inbox Hard Rule

If the run inbox has unconsumed messages, the agent loop must not exit on
`CURRENT_TASK_DONE`.

It must format the inbox into the next model turn and let the model absorb it.

Otherwise the system produces this failure:

```text
The log contains the user follow-up, but the final reply does not reflect it.
```

## Output Pairing

Keep user conversation and tool state separate:

- Casual chat and short answers: plain text.
- Light Markdown: rich text.
- Tool-heavy work: one editable workbench card.
- Tool process: aggregated and collapsible, not multiple spam cards.
- Completion: separate final report.

## GA Reference Landing

GenericAgent 2026-05-25 source landing:

- `conversation_thread.py`
- `conversation_intent_router.py`
- `frontends/feishu_thread_context.py`
- `frontends/feishu_interaction_mode.py`
- `agent_loop.py`
- `agentmain.py`
- `frontends/fsapp.py`

Key tests:

- `tests/test_conversation_thread.py`
- `tests/test_conversation_intent_router.py`
- `tests/test_feishu_thread_context.py`
- `tests/test_feishu_interaction_mode.py`
- `tests/test_self_restart.py::test_agent_loop_absorbs_user_followup_before_final_exit`

## References

- `../../examples/37-agent-flowing-conversation-thread_流式对话线程与上下文贯通.md`
- `../agent-memory-store-retrieve-loop_分层记忆存储与检索循环/`
- `../agent-output-workbench_输出流工作台与卡片生成/`
- `../agent-anti-bloat-context-engineering_上下文防膨胀工程/`
