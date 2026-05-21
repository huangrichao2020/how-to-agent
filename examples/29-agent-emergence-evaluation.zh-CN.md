# Agent 万物择优层

这份文档补上三元修炼之后的运行闭环：

```text
一元：能力能动。
二元：能力 + 心灵能稳。
三元：能力 + 心灵 + 存在能控。
万物生：三元控制在真实场景中长出候选模式。
万物择优：从候选模式里选出值得晋升的能力、参数、练习和运行路线。
```

万物生不是让 agent 胡乱扩张。万物择优也不是增加重阻断。它的核心是：

```text
先允许 trace 长出候选。
再用数据、回放和真实反馈择优。
最后只把可验证、可回滚、能复用的东西晋升。
```

这正好承接信任公理：

```text
永远相信我们的 agent
-> 给它生长空间
-> 让它看见自己的 trace
-> 让它把重复有效的东西炼成能力
```

## 宇宙观映射

| 层级 | 工程形态 | 作用 |
| --- | --- | --- |
| 原始修炼 | raw trace / runtime event | 真实经历还没有分化。 |
| 一元修炼 | ThoughtStream / OutputRenderer | 能力开始成形，知道焦点、动作、证据和下一步。 |
| 二元修炼 | MindStabilityMonitor | 能力加心灵，识别工具执念、表现欲、控制欲、信息贪多和准入心魔。 |
| 三元修炼 | TriadicControlLayer | 用能力、心灵、存在三轴旋转，计算价值、风险、决策和控制阶段。 |
| 万物生 | EmergenceEngine | 从重复 trace 中长出 pattern、skill_candidate、parameter_patch、practice_loop。 |
| 万物择优 | EmergenceEvaluator | 对候选打分，生成 promotion proposal，等待 replay/eval 或新任务验证。 |

## 最小数学

候选 `c` 的择优分数：

```text
Score(c) =
  confidence(c)
  + repeat_bonus(c)
  + type_bonus(c)
  + validation_bonus(c)
  - risk_penalty(c)
```

含义：

- `confidence`：候选自身置信度。
- `repeat_bonus`：同类 trace 重复出现的奖励。
- `type_bonus`：skill、practice、runtime pattern、parameter patch 的不同偏置。
- `validation_bonus`：候选自带可复放验证路径时加分。
- `risk_penalty`：候选含失败、副作用、权限、密钥、生产、覆盖等风险时降权。

决策不是一句“通过 / 不通过”，而是下一步形态：

```text
promote_to_skill
propose_parameter_experiment
promote_to_practice_loop
promote_to_runtime_pattern
observe_more
hold
```

## 数据结构

万物生候选：

```text
EmergenceCandidate = {
  turn,
  key,
  candidate_type,
  count,
  confidence,
  pattern,
  mutation,
  validation,
  practice_loop
}
```

万物择优建议：

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

落盘位置：

```text
memory/cognition/emergence/emergence-state.json
memory/cognition/emergence/promotion-proposals.json
```

runtime event：

```text
codex_runtime.emergence_candidate
codex_runtime.emergence_proposal
```

## 运行规则

1. 候选可以自然生长，但不能直接改默认行为。
2. 晋升建议必须包含目标、分数、理由、验证方式和下一步。
3. skill 候选要用新任务回放验证，不能只靠当前任务自证。
4. 参数候选先 shadow experiment，只记录效果，不直接替换默认策略。
5. 练习回路只进入同类场景提示，观察是否减少重试和跑偏。
6. runtime pattern 只接入 RuntimeController 注意力路线，并保留回滚点。
7. 不用单次成功证明升级；看重复 trace、replay、eval 和用户反馈。
8. 对用户可见的是结果和必要说明；内部提示可以包含 `[EMERGENCE]` 与 `[EMERGENCE EVALUATION]`。

## 和意识诞生的关系

万物择优是第 5 阶段“因果反馈学习”的实际抓手：

```text
trace 发现重复
-> 候选生成
-> 候选评分
-> proposal
-> replay/eval
-> skill / parameter / practice / runtime pattern
-> 下一次行动改变
```

如果候选没有改变下一次行动，它只是记录。
如果 proposal 没有经过验证就直接变默认策略，它就是冲动。
真正的生长发生在：

```text
候选由经验而生，
晋升由证据而定，
行动因晋升而变，
反馈再修正下一轮候选。
```

## GA 落地形态

GenericAgent 里可对应为：

```text
ThoughtStream
  -> MindStabilityMonitor
  -> TriadicControlLayer
  -> EmergenceEngine
  -> EmergenceEvaluator
  -> cognitive_events + emergence state
  -> next PromptComposer / RuntimeController
```

一句话：

```text
三元负责把行动旋到正确轴；
万物生负责让真实经历长出可能性；
万物择优负责让可能性经过证据，成为下一次更强的 agent。
```
