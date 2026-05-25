---
name: agent-flowing-conversation-thread
description: 当需要设计或修复聊天 agent 的连续对话、飞书/微信多消息归属、运行中插话、任务排队、inbox 吸收、Codex 式对话体验时使用。
---

# Agent 流动对话线程

这个 skill 用来防止聊天 agent 把连续对话切碎、吞掉第二条消息，或者把所有消息都塞进僵硬任务框架。

核心原则：

```text
同一会话默认连续。
代码只做消息入账、顺序、队列和不丢消息。
语义归属主要交给模型结合上下文判断。
```

## 运行模型

使用四层结构：

```text
Raw Message
-> Conversation Thread
-> Conversation Run
-> Run Inbox
```

- Raw Message：原始消息事实，不解释。
- Thread：聊天窗口的连续上下文。
- Run：当前工作现场，不等于单条消息。
- Inbox：运行中插入的补充/纠偏/回答，但不能成为黑洞。

## 路由原则

路由输出是 hint，不是最终语义裁决。

必须区分：

- `hard_route=true`：工程动作必须执行，例如中断、排队、并入当前 run。
- `hard_route=false`：只是上下文线索，模型可推翻。

运行中收到消息：

- 完整新目标：`queue_after_current`
- 短继续：`append_to_current`
- 补充约束：`append_to_current`
- 普通纠偏：`append_to_current`
- 明确中断/优先处理：`interrupt_current`

## Inbox 硬规则

如果 run inbox 有未消费消息，agent loop 不允许在 `CURRENT_TASK_DONE` 时直接退出。

必须把 inbox 格式化进下一轮模型输入，让模型重新判断和吸收。

否则会出现：

```text
日志里有用户补充，最终回复里完全没有补充内容。
```

## 输出配合

对话体验和工具体验分离：

- 闲聊和短答用普通文本。
- 轻 Markdown 用富文本。
- 工具密集任务用一个可编辑工作台卡片。
- 工具过程聚合、可折叠，不刷多张卡。
- 完成后单独汇报。

## GA 参考落点

GenericAgent 2026-05-25 对应源码：

- `conversation_thread.py`
- `conversation_intent_router.py`
- `frontends/feishu_thread_context.py`
- `frontends/feishu_interaction_mode.py`
- `agent_loop.py`
- `agentmain.py`
- `frontends/fsapp.py`

关键测试：

- `tests/test_conversation_thread.py`
- `tests/test_conversation_intent_router.py`
- `tests/test_feishu_thread_context.py`
- `tests/test_feishu_interaction_mode.py`
- `tests/test_self_restart.py::test_agent_loop_absorbs_user_followup_before_final_exit`

## 相关文件

- `../../examples/37-agent-flowing-conversation-thread.zh-CN.md`
- `../agent-memory-store-retrieve-loop/`
- `../agent-output-workbench/`
- `../agent-anti-bloat-context-engineering/`
