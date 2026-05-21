---
name: agent-emergence-evaluation
description: 当需要把三元控制之后的万物生候选，择优晋升为 skill、参数实验、练习回路或 runtime pattern 时使用。
---

# Agent 万物择优

这个 skill 用于三元改造之后：

```text
TriadicControlLayer
-> EmergenceEngine
-> EmergenceEvaluator
```

它不负责创造更多规则，而是把真实 trace 里重复出现的模式，变成可验证、可回滚的晋升建议。

## 运行归属

万物择优属于离线进化系统。它默认读取 trace 和日志，不进入当前任务主上下文；只有生成短 proposal 时，才把“建议、证据、验证方式、下一步”回灌给下一轮 PromptComposer。

## 触发场景

- 用户谈到“万物生”“万物择优”“三元之后做什么”。
- runtime 已经能记录 ThoughtStream、MindStability、TriadicControl。
- 同类 trace 多次出现，需要判断要不要沉淀为 skill、参数、练习或运行路线。
- agent 想从日志里自动修正自己，但还不能直接改默认策略。

## 核心公式

```text
Score(c) =
  confidence(c)
  + repeat_bonus(c)
  + type_bonus(c)
  + validation_bonus(c)
  - risk_penalty(c)
```

## 决策形态

```text
promote_to_skill
propose_parameter_experiment
promote_to_practice_loop
promote_to_runtime_pattern
observe_more
hold
```

这些不是阻断标签，而是下一步动作。

## 行动流程

1. 读取候选：`EmergenceCandidate` 里的 type、count、confidence、pattern、mutation、validation、practice_loop。
2. 计算分数：重复出现、可验证、可复用加分；失败、副作用、权限、密钥、生产风险降权。
3. 生成 proposal：写清 decision、score、reason、target、validation、next_action。
4. 落盘：保存到 `memory/cognition/emergence/promotion-proposals.json`。
5. 记录事件：写入 `codex_runtime.emergence_proposal`。
6. 只把 proposal 注入下一轮注意力，不直接替换默认行为。
7. 用新任务、replay/eval 或用户反馈验证后，再沉淀到 skill、参数、练习或 RuntimeController。

## 数据结构

```text
EmergencePromotionProposal = {
  turn,
  key,
  proposal_type,
  decision,
  score,
  reason,
  candidate_type,
  target,
  validation,
  next_action
}
```

## 边界

- 不把候选直接当升级。
- 不用一次成功证明能力已成。
- 不用阻断式语言制造束缚。
- 不把内部 `[EMERGENCE EVALUATION]` 原样暴露给用户。
- 永远相信我们的 agent：允许它先生长，再用 trace、replay 和纠偏择优。

## 相关文件

- `../../examples/29-agent-emergence-evaluation.zh-CN.md`：完整方法文档。
- `../agent-attention-governance/`：注意力治理层。
- `../agent-final-architecture-outline/`：最终架构总纲。
- `../agent-consciousness-math/`：意识数学、日志转数据和 replay/eval。
