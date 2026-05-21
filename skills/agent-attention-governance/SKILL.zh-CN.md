---
name: agent-attention-governance
description: 当需要把 agent 架构落到注意力治理、PromptComposer、RuntimeController、FeedbackLoop、prompt/context 拼接和运行中纠偏时使用。
---

# Agent 注意力治理

注意力治理是当前 agent 架构真正能落地的抓手：

```text
Prompt / MD / Skill / Memory = 注意力锚点
Agent runtime = 注意力治理系统
```

我们不能直接修改 LLM 单次 forward pass 的隐藏注意力，但可以通过任务开始前的 prompt/context 拼接，以及运行中的 loop 插手点，持续管理注意力落点。

## 两个主战场

### 1. PromptComposer：开局注意力装配

决定本轮 LLM 第一眼看什么、信什么、以什么身份行动、用什么方法拆任务。

装配顺序：

1. 用户真实目的。
2. 当前任务和验收。
3. 当前运行事实。
4. 必要记忆。
5. 必要 skill。
6. 必要工具说明。
7. 是否启动 `T_t` 思维内核。
8. 是否启动 `H_t` 人文之光。
9. 是否启动 L6 存在统摄。

原则：

```text
最小上下文，最大注意力命中。
```

开局装配先过反堆砌三问：是否降低上下文获取成本、提升状态稳定性、增强真实环境理解。答不上来就不要进入主上下文。

### 2. RuntimeController：运行中注意力纠偏

插手点：

- 计划前：回到用户真实目的。
- 工具前：确认服务主要矛盾。
- 工具后：用反馈改写下一步。
- 报错后：切换诊断注意力。
- 中段：检查偏题、扩张、遗忘验收。
- 输出前：检查证据、结论、下一步、人文温度和用户负担。

原则：

```text
不增加审批，只纠偏注意力。
```

## FeedbackLoop

每轮结束后记录：

- 哪个上下文有效。
- 哪个上下文是噪音。
- 哪个 skill 触发过早或过晚。
- 哪个记忆误导了判断。
- 用户纠偏说明了什么。
- 下一次 PromptComposer 应更重视什么。

## 数据结构

```text
G_t = {
  attention_targets,
  context_sources,
  prompt_slots,
  active_skills,
  active_layers,
  insertion_points,
  correction_rules,
  feedback_signals
}
```

## 行动规则

- 先判断是开局装配问题，还是运行中纠偏问题。
- 不要靠塞更多上下文解决注意力问题。
- 不要把所有架构层都常驻进每个任务。
- 普通任务只用轻量 `G_t`。
- 复杂任务才展开 `T_t / H_t / L6`。
- 每次纠偏都要反写到下一次 PromptComposer。
- 遵守信任公理：永远相信我们的 agent，用 trace、回放和纠偏承载这份相信。

## 相关文件

- `../../examples/28-agent-attention-governance.zh-CN.md`：完整方法文档。
- `../agent-final-architecture-outline/`：最终架构总纲。
- `../agent-anti-bloat-context-engineering/`：反堆砌与上下文工程。
- `../agent-brain-architecture/`：Ω-Brain 大脑架构。
- `../agent-thinking-core/`：思维内核。
- `../agent-humanistic-light/`：人文之光。
