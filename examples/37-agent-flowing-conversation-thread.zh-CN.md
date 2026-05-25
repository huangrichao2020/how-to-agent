# Agent 流动对话线程

很多聊天 agent 的连续对话能力差，不是因为模型不懂上下文，而是运行时先把用户消息切碎了。

典型坏味道：

```text
用户第一条：你感觉怎么样
用户第二条：自检一下你源码近期的改动

运行时把第二条当成第一条的“补充”，塞进某个 inbox。
第一条回复直接结束。
第二条没有进入下一轮模型输入。
用户看到：第二条没回。
```

这不是简单的 intent 分类错误，而是事件模型错了。

一句话原则：

```text
同一会话里的每条用户消息，默认都是同一条流动对话线程的一部分。
代码只保证消息不丢、不乱序、不吞完整任务；语义归属交给模型结合上下文判断。
```

## Codex 式处理

Codex 的体感来自一件很朴素的事：

```text
每条新消息都会进入当前线程上下文。
模型重新看：最新消息 + 正在做什么 + 之前说过什么 + 工具状态。
然后判断这是补充、纠偏、追问、新任务，还是插队。
```

代码层不应该把“用户到底指哪件事”写死成一堆关键词。代码层应该提供清晰的工程边界：

- 消息必须入账。
- 消息必须有顺序。
- 运行中来的短补充可以进入当前任务。
- 运行中来的完整新目标要排队，不能吞掉。
- 如果补充已经进入当前任务，当前 loop 收尾前必须再吸收一次。
- 最终回复必须能体现被吸收的用户新消息。

## 四层事件模型

### 1. Raw Message

每条用户消息都先作为事实保存。

推荐字段：

```json
{
  "message_id": "om_...",
  "thread_id": "feishu:chat:...",
  "created_at": 1779660000.0,
  "text": "自检一下你源码近期的改动",
  "attachments": [],
  "quoted_message_id": "",
  "source": "feishu"
}
```

这一层不做语义解释。

### 2. Conversation Thread

同一个聊天窗口是一条持续线程。

线程负责保存最近消息、活跃 run、最近完成 run、引用关系和用户插话。

```json
{
  "thread_id": "feishu:chat:oc_xxx",
  "active_run_id": "run_...",
  "recent_run_ids": ["run_3", "run_2", "run_1"],
  "updated_at": 1779660000.0
}
```

### 3. Conversation Run

run 是一次正在执行或刚结束的工作单元。

```json
{
  "run_id": "run_...",
  "thread_id": "feishu:chat:oc_xxx",
  "status": "running|queued|done|failed",
  "active_goal": "用户当前想完成什么",
  "message_ids": ["om_1", "om_2"],
  "inbox": []
}
```

run 不是“每条消息一个任务”。run 是用户意图在一段时间内的工作现场。

### 4. Run Inbox

运行中插入的新消息进入 inbox，但 inbox 不能变成黑洞。

```json
{
  "item_id": "inbox_...",
  "kind": "supplement|correction|answer",
  "route": "append_to_current",
  "text": "还有，补一下测试",
  "consumed_at": 0
}
```

硬规则：

```text
如果 inbox 有未消费消息，agent loop 不允许在 CURRENT_TASK_DONE 时直接退出。
必须把 inbox 格式化进下一轮模型输入，再让模型重新判断。
```

## 路由不是裁决

路由模块的输出应该叫 hint，不应该叫 verdict。

推荐结构：

```json
{
  "route": "append_to_current|queue_after_current|interrupt_current|resume_previous|new_task",
  "intent": "continue|supplement|correction|new_task|chat|answer",
  "target_frame_id": "frame_...",
  "confidence": 0.82,
  "hard_route": true,
  "evidence": ["当前任务正在运行", "消息像完整新任务"]
}
```

关键字段是 `hard_route`：

- `hard_route=true`：工程动作必须执行，例如中断、排队、并入当前 run。
- `hard_route=false`：只是上下文线索，模型可以推翻。

这能避免两种坏结果：

- 代码过度聪明，把“执行7”当成全新闲聊。
- 代码过度自信，把“自检源码改动”吞成上一句闲聊的补充。

## 完整新目标不能被吞

运行中收到消息时，先问一个工程问题：

```text
这条消息是不是一个完整的新工作目标？
```

如果是，应该排到当前任务后面，而不是塞进当前回复。

例子：

```text
正在回答：你感觉怎么样
新消息：自检一下你源码近期的改动
=> queue_after_current
```

短补充才进入当前 run：

```text
继续
执行7
还有，补一下测试
不是，我说的是本机源码
=> append_to_current
```

这里的判断只是工程边界，不是代替模型理解用户。

## Prompt 组装

给模型的上下文要长这样：

```text
### 当前用户消息
自检一下你源码近期的改动

### 对话路由线索
- route: queue_after_current
- intent: new_task
- hard_route: true
- reason: 运行中收到完整新目标，排到当前任务后面

### 最近线程
- 上一条用户消息：你感觉怎么样
- 当前 run：轻聊天回复
- 队列：自检源码近期改动
```

如果是运行中补充：

```text
### 当前流动线程 Run Inbox
- kind: supplement
- route: append_to_current
- text: 还有，补一下测试

请把用户追加消息当成当前任务的新约束。不要说上一条被打断。
```

## 与 MemoryHub 的关系

流动对话线程解决的是“当前会话连续性”。

MemoryHub 解决的是“跨天、跨任务、跨会话恢复”。

两者关系：

```text
Raw Message
  -> Conversation Thread / Run / Inbox
  -> 当前轮 prompt
  -> 完成后沉淀为 Episode
  -> MemoryHub 后续可恢复
```

不要把所有连续对话都扔给长期记忆。当前线程能解决的，就在当前线程解决。

不要把跨天恢复只靠当前线程。线程断了，就查 MemoryHub 的 episode/worksite。

## 输出层配合

流动线程不等于每条消息都要卡片化。

输出层规则：

- 闲聊：普通文本。
- 轻 Markdown：富文本。
- 工具密集任务：一个可编辑工作台卡片。
- 最终结论：单独汇报。
- 工具调用详情：聚合在工作台里，可折叠，不刷屏。

对话体验和工具体验要分开：

```text
用户感觉是在连续聊天。
工具状态在后台工作台稳定更新。
完成后有清楚汇报。
```

## GA 2026-05-25 实测落点

GenericAgent 这次改造证明了这个模式：

| 问题 | 根因 | 落点 |
| --- | --- | --- |
| 第二条消息没回 | 完整新任务被 `append_to_current` 吞进运行中 inbox | `conversation_intent_router.py` 增加完整任务边界，运行中 `queue_after_current` |
| 即使进 inbox，回复也没体现 | `agent_loop` 在 `CURRENT_TASK_DONE` 时直接退出，没让 inbox 进入下一轮模型输入 | `agent_loop.py` 在退出前检查 `has_user_interventions()` |
| “执行7”不懂 | 当前用户消息被包装后，路由没有只看 live user turn | `current_user_text()` 和编号动作恢复 |
| 短聊过度工作台 | 输出层没有区分轻互动和长任务 | `frontends/feishu_interaction_mode.py`、`feishu_task_stream.py` |
| 架构越来越乱 | 太多开关和 prompt 级补丁 | 删除环境开关，保留固定清爽主路径 |

验证：

```text
pytest -q
450 passed, 3 skipped
```

关键回归测试：

```text
test_complete_task_does_not_get_swallowed_by_running_chat
test_agent_loop_absorbs_user_followup_before_final_exit
test_short_continue_still_appends_to_running_task
test_supplement_still_appends_to_running_task
```

## 最小提示

```text
[FLOWING CONVERSATION THREAD]
- 默认同一会话连续，不要把每条消息当孤立任务。
- 代码只做消息入账、顺序、队列、中断和不丢消息。
- 语义归属主要交给模型结合上下文判断。
- 完整新目标运行中排队；短补充、纠偏、回答并入当前 run。
- inbox 不是日志黑洞；当前 loop 结束前必须吸收未消费用户消息。
- 对用户保持自然对话，对工具过程使用可编辑工作台聚合。
[/FLOWING CONVERSATION THREAD]
```
