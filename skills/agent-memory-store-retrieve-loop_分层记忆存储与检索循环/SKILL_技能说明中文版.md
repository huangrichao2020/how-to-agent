---
name: agent-memory-store-retrieve-loop_分层记忆存储与检索循环
description: 当需要设计、清理或改造 agent 记忆系统，统一原始记录、事件现场、结构化认知、技能晋升、dream 反写和运行时取记忆闭环时使用。
---

# Agent 记忆存取闭环

这个 skill 用来防止 agent 记忆系统越做越散。

核心判断：

```text
没有取用协议的记忆，只是仓库；不是大脑。
```

## 分层

运行时按这条链路设计：

```text
L0 原始记录
-> L1 事件现场
-> L2 印象/反馈
-> L3 结构化认知
-> L4 技能/方法
-> Dream 复盘
-> Runtime 取用
```

## 每条记忆必须回答

- 为什么要存？
- 属于哪一层？
- 未来什么时候应该被想起？
- 想起后本轮行为应该有什么不同？

答不上最后一问，就不要进 prompt。

## 字段原则

### L0 原始记录

保留 `time/source/actor/scope/text/attachments/links/hash`。

不要解释，不要总结。

### L1 事件现场

保留 `type/subject/timeline/source_refs/current_status/resume_hint/last_good_output_ref/last_correction_ref`。

用于隔天继续、翻原文、恢复旧任务。

### L3 结构化认知

保留 `object/kind/claim/evidence_refs/use_when/do_next/confidence/freshness/scope/contradictions/last_validated_at`。

重点是 `use_when` 和 `do_next`。

### L4 技能/方法

保留 `skill_name/trigger/steps/tests/rollback`。

稳定经验必须能执行、能测试、能回滚。

## 取记忆协议

- 详细新需求：少取旧记忆，避免污染。
- 短句、继续、纠错、时间指向：先取事件现场和原文。
- 偏好、关系、语气、懂我：取 preference / identity / nourishment / feedback。
- 代码、运维、运行状态：取 procedure / runtime ledger / recent failures。
- 反复失败：取 feedback_distill / dream_writeback / runtime_protocols。

## 清理旧机制

清理时按角色，不按文件年龄。

- 只写不取：降级 archive 或停止 live 写入。
- 重复取用：接入统一 MemoryHub。
- 无 schema 的长期认知：迁移到结构化层。
- 无 trigger/tests/rollback 的技能：只算方法笔记，不算 runtime skill。
- dream 报告如果不反写 runtime，只算报告，不算修炼闭环。

## GA 改造落点

GenericAgent 应收敛为：

```text
MemoryHub
  -> raw evidence readers
  -> episode/worksite recall
  -> structured cognition retrieval
  -> feedback and dream writeback
  -> runtime context pack
```

先统一取用入口，再标记 legacy surface，再迁移数据，最后删代码。

## 相关文件

- `../../examples/36-agent-memory-store-retrieve-loop_分层记忆存储与检索循环.zh-CN.md`
- `../agent-brain-architecture_Ω大脑架构与感知决策/`
- `../agent-anti-bloat-context-engineering_上下文防膨胀工程/`
- `../agent-attention-governance_注意力治理与提示词编排/`
