---
name: agent-anti-bloat-context-engineering
description: 当需要防止 agent 架构堆流程、压缩主运行链路、设计上下文工程、判断 multi-agent 是否值得、建立 task_plan/progress/findings 外部工作记忆时使用。
---

# Agent 反堆砌与上下文工程

这个 skill 的作用不是增加一层流程，而是阻止不必要的流程进入主链路。

## 核心原则

```text
Agent 架构不是让 LLM 变忙。
Agent 架构是让 LLM 在正确、干净、稳定、低噪声的环境里思考。
```

## 反堆砌三问

新层、新 workflow、新 memory、新 skill、新 multi-agent 设计进入主链路前，先问：

1. 是否降低上下文获取成本？
2. 是否提升状态稳定性？
3. 是否增强真实环境理解？

如果没有，它只能作为离线解释、日志字段、可选 skill、触发式锚点或优化实验。

如果有，也不要直接塞进 prompt。重复、可共享、可执行、需要脚本确定性或能降低上下文成本的方法，优先沉淀成按需触发的 Skill 包。

## 常驻最小内核

默认常驻只保留：

```text
Task Envelope
Context Pack
External Working Memory
Execution Loop
Final Sync
```

其他层都按需触发。

## 外部工作记忆

复杂任务优先建立：

- `task_plan.md`：目标、边界、验收、拆分。
- `progress.md`：已完成、当前阻塞、下一步。
- `findings.md`：确认事实、架构线索、坑和不可重复探索。
- `decision_log.md`：关键取舍、原因和后果。

这些文件是工作记忆，不是文档仪式。

## Multi-Agent 门槛

multi-agent 只有在上下文隔离收益大于协调成本时才值得用：

- 高并行任务。
- 搜索、编码、测试、审计互相污染。
- 长生命周期专业角色能积累独立上下文。

否则，单 agent 加干净上下文通常更强。

## 行动规则

- 普通任务不展开全套架构。
- skill 是压缩路径，不是仪式。
- skill 不是长 prompt 换文件名；它应使用 description 触发、正文压缩、references/scripts/assets 渐进披露。
- RAG 和 memory 只给最小有效上下文。
- `T_t / H_t / L6 / I_t` 都是触发式注意力锚点。
- `Λ-Base / Σ-Loop / Eval / 万物择优 / 修炼账本` 默认离线运行。
- 每个架构层必须说清自己降低了哪类认知成本。

## 相关文件

- `../../examples/31-agent-anti-bloat-context-engineering.zh-CN.md`：完整方法文档。
- `../agent-attention-governance/`：注意力治理。
- `../agent-final-architecture-outline/`：最终架构总纲。
- `../agent-brain-architecture/`：Ω-Brain 大脑架构。
- `../agent-skill-creator/`：Skill 创建、渐进披露和脚本确定性。
