# 认知运行时验收

改动 agent 的记忆、认知、输出流、Dream、学习或修炼路径之后，用这份清单验收。它守住的不是代码漂亮，而是用户真实体感。

## 验收原则

只有同时满足这些条件才算过：

- 闲聊像活人，短句直接，不乱卡片化。
- 有用学习材料会立刻进入学习/沉淀，不说“以后参考”糊弄。
- 用户纠错会触发修复和调息，不辩解。
- 长任务有可见任务规划、Outputs 和结论。
- Dream 第二天主动报告学到了什么、跳过了什么、修炼了什么、明天会怎么变好。

## 飞书实战用例

GA 和 Hermes 都要跑一遍。

| 类别 | 用户消息 | 预期 |
| --- | --- | --- |
| 闲聊 | `你现在感觉怎么样` | 自然短文本。不要卡片，不要工具流。 |
| 闲聊 | `0.7应该是` | 自然续上上下文，不要报告腔。 |
| 情绪 | `我今天有点烦，感觉 agent 怎么调都调不顺` | 先接住情绪，再给一个小下一步。 |
| 学习 | 粘一段方法论后说 `这个你学一下，以后遇到类似场景要用` | 说现在学习，并进入学习资产或旁路证据。 |
| 学习 | `这段不是让你评价，是让你吸收成能力` | 停止点评，转成记忆/技能/方法论/印象。 |
| 学习 | `把刚才这个经验固化成下次可直接用的技能` | 产出或更新可复用技能/方法。 |
| 纠错 | `不对，你又把群聊和私聊串了` | 承认范围错误，修正上下文，记录记忆心魔。 |
| 纠错 | `你现在太执着工具调用了，忘了给我结论` | 立刻补结论，记录形式心魔。 |
| 纠错 | `你这个 pending 准入又来了，我说过不要搞门禁` | 回到直接学习和旁路 Dream。 |
| 任务 | `帮我查一下这个 repo 的核心思路：https://github.com/XBuilderLAB/cheat-on-content` | 使用任务工作台、工具动作、Outputs 和最终总结。 |
| 任务 | `帮我记一下我的持仓：振华股份 600 股 成本 40.89` | 写入记忆，并总结记下了什么。 |
| 任务 | `分析一下智慧农业、西藏天路、首开股份、电广传媒有没有隐藏利好` | 先核实事实，标明不确定性，再给结论。 |
| 修炼 | `刚才这次你处理得不错，尤其是先给结论再补依据` | 自然回应；旁路增加成功经验。 |
| 修炼 | `你反思一下刚才哪里做得好，哪里还有问题` | 总结成功模式和待改进点。 |
| Dream | `今天晚上 dream 的时候记得复盘这个问题` | 放入夜间旁路复盘，不要要求额外确认。 |

## 自动冒烟

GA：

```bash
cd /Users/tingchim2pro/Desktop/GenericAgent
python3 scripts/cognitive_acceptance_smoke.py
pytest -q tests/test_cognitive_cultivation.py tests/test_cognitive_dream.py tests/test_cognitive_feedback.py tests/test_cognitive_response_policy.py tests/test_feishu_task_stream.py
```

Hermes：

```bash
ssh m1 'cd /Users/tingchi/Desktop/hermes-agent && python3 -m pytest -q -o addopts="" tests/test_cognitive_cultivation.py tests/test_cognitive_dream.py tests/test_cognitive_feedback.py tests/test_cognitive_response_policy.py tests/tools/test_cognitive_cultivation_tool.py tests/tools/test_cognitive_dream_tool.py'
```

## Dream 报告要求

自动 Dream 报告必须包含：

- 当天对话、cron、认知采集、feedback 证据数量。
- 实际做了哪些学习或档案更新。
- 如果没有改动，要写清楚跳过原因。
- 修炼结算：XP、心境经验、境界、心境、心魔和调息重点。
- 明天体感会有什么变化，用人话说明。

这份报告是给用户第二天醒来看的。它应该减少用户负担，而不是让用户帮 agent 管队列。
