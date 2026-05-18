# 学习资产化讨论门

当 agent 有 GitHub 学习日报、技术趋势扫描、研究循环时，用这套模式让它真的成长，同时不要把用户变成全天候记忆审核员。

## 问题

学习循环很容易变成两种坏形态：

- 发完日报下一秒就忘了。
- 把用户随口一句“可以”“嗯”“对”都当成长期写入许可或改造信号。

前者没有成长，后者会把人累死。agent 要学习，但用户不能每天替它审每一条碎片。

## 规则

学习结果分三类：

- 外部经验、release、论文、repo 机制，只要确实有助于 agent 架构，进入 `agent-systems-patterns`。
- 已经被 GA、Hermes、Codex 或真实任务验证过的方法，进入 `how-to-agent`。
- 任何想改 agent 自己的内容，先进入讨论提案。

第三类是关键安全阀。学习日报可以提出“要不要改 GA/Hermes/Codex 的 runtime prompt、记忆、工具、cron、路由”，但不能直接进入实战，必须先发给用户讨论。

## 流程

1. 先正常生成学习日报。
2. 对每条可能的经验判断：它是否真的帮助 agent 以后工作？
3. 有用的外部学习，写入快速 pattern 层。
4. 已实战验证的方法，写入实践手册层。
5. 涉及自我改造的，写成 discussion proposal，不进入主链路门禁。
6. 最后向用户报告 `updated`、`needs_discussion`、`skipped`。

## 验证

这套模式已在 2026-05-16 接入 GA 和 Hermes：

- GA 新增 `agent_learning_assets.py` 和 `learning_asset_update` 工具。
- Hermes 新增 `agent/learning_assets.py` 和 `tools/learning_assets_tool.py`。
- Hermes GitHub 学习日报 cron 已加入 `hermes-core`，日报后调用学习资产化工具。
- 测试覆盖了学习分流、实战分流、未验证实战跳过、自我改造必须先讨论。

## 反模式

不要因为一个想法有趣，就把它写进 `how-to-agent`。不要让 cron 学到一个热门 repo 的机制后，静悄悄改掉 agent 自己的行为。
