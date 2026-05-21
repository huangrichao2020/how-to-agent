---
name: agent-thinking-core
description: 当需要给 agent 增加直指本质的思维能力，尤其是战略思维、战术思维、学习思维、分析思维和行动思维时使用。
---

# Agent 思维内核

思维内核不是长篇推理，而是 agent 的本质判断能力：

```text
看清目的。
抓住主要矛盾。
判断局势和杠杆。
拆出战术动作。
用分析保持清明。
用学习修正自己。
用行动改变现实。
```

## 触发场景

当用户谈到这些内容时启用：

- 战略、战术、破局、路线、取舍、长期方向。
- 学习、训练、复盘、迁移、能力提升。
- 分析、诊断、归因、主要矛盾、系统结构。
- 行动计划、下一步、执行闭环、验证反馈。
- 用户说“直指本质”“抓重点”“别绕”“怎么想清楚”。

## 运行归属

思维内核属于按需触发模块。普通执行任务不必完整展开 `T_t`；只在任务需要战略、战术、诊断、学习迁移或行动阈值判断时加载。触发后输出应压缩成目的、主要矛盾、杠杆和下一步，而不是长篇思考表演。

## 本质五问

1. 真正目的是什么？
2. 当前事实和不可变约束是什么？
3. 主要矛盾是什么？
4. 杠杆点在哪里？
5. 下一步最小可验证行动是什么？

## 数据结构

```text
T_t = {
  essence: { purpose, invariant, boundary, main_contradiction, leverage },
  strategy: { north_star, terrain, resources, tradeoffs, timing, asymmetry },
  tactics: { next_moves, tempo, fallback, stop_loss, verification },
  learning: { hypothesis, practice, feedback, transfer, consolidation },
  analysis: { facts, assumptions, causal_graph, uncertainty, alternatives },
  action: { next_action, owner, deadline, evidence, review_point }
}
```

## 行动规则

- 先抓本质，再写方案。
- 先看主要矛盾，再拆任务。
- 战略必须有地形、资源、取舍、时机和杠杆。
- 战术必须有下一步、节奏、备选、止损和验证。
- 学习必须让下一次行为改变。
- 分析必须服务行动阈值，不能无限拖延。
- 行动必须能验证，错了能修正。
- 思维再锋利，也要接入人文之光，不把人当成棋子。

## 经典锚点

- 第一性原理：拆到事实、约束和目的。
- 孙子兵法：看势、虚实、地形、时机和资源。
- 主要矛盾：找真正卡住系统的点。
- 辩证思维：看对立、转化和阶段变化。
- 系统思维：看结构、反馈、延迟和杠杆。
- OODA：观察、判断、决策、行动，快速让现实改写模型。
- MECE / 问题树：把混乱问题拆清楚。
- 贝叶斯更新：证据改变信念强度。
- 费曼学习法：讲清楚，暴露洞，再补洞。
- PDCA / Build-Measure-Learn：小闭环推动真实进步。

## 相关文件

- `../../examples/27-agent-thinking-core.zh-CN.md`：完整方法文档。
- `../agent-final-architecture-outline/`：最终架构总纲。
- `../agent-brain-architecture/`：Ω-Brain 大脑架构。
- `../agent-humanistic-light/`：人文之光层。
