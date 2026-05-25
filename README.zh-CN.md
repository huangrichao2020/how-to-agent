# how-to-agent

通过对话教会你的 agent 自我进化。

<p align="center">
  <img src="assets/how-to-agent-readme-banner.png" alt="How to Agent README banner" width="100%">
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![English](https://img.shields.io/badge/docs-English-blue)](README.md)
[![中文](https://img.shields.io/badge/docs-中文-red)](README.zh-CN.md)
[![GitHub stars](https://img.shields.io/github/stars/huangrichao2020/how-to-agent?style=social)](https://github.com/huangrichao2020/how-to-agent)

<p align="center">
  <a href="README.md"><strong>English</strong></a>
  ·
  <a href="README.zh-CN.md"><strong>简体中文</strong></a>
</p>

这是一个面向开发者的小型实战指南：如何通过连续对话，让 coding
agent 学会新能力，而不是一上来就重写整个 agent runtime。

它也是一个单独为你打造的能力中心：用来沉淀你希望未来 agent 继承的记忆、技能、方法论和工作印象。

它不是一个 agent 框架。它是一条真实的 prompt trail：一组人类按顺序发给
agent 的指令，把 agent 从"去研究这些项目"一步步推到"归档新架构、讨论风险、谨慎落地第一阶段，并为后续 agent 写工作手册"。

核心想法很简单：

> 把 agent 当成一个能学习的初级系统。但只有当你逼它把学习沉淀成架构、runbook
> 和可重复习惯时，学习才会真正留下来。

## 适合谁

- 正在维护本地 coding agent、工作流机器人或 agent harness 的开发者。
- 已经有 memory、tools、skills、docs 或 wiki，但不知道如何让 agent 安全改进这些系统的人。
- 想看真实"调教 agent 的对话过程"，而不是又一篇抽象 autonomous-agent 宣言的团队。

## 原始 prompt trail

下面是原始指令，按真实顺序保留。它们故意很朴素。价值不在神奇措辞，而在约束的顺序。

1. 深度研究一下 open-design 的平面设计能力 和 agentic-stack 的 .agent/结构，看看对你有什么帮助
2. 这简直是大版本改动了，一条一条来，你先存档为大版本架构设计手册，然后我们一条条讨论和修改
3. 按顺序来
4. 方案A 肯定是要做的，方案 1 直接做的话 有什么风险和收益？
5. 就是说渐进运行一段时间后，再全面切换生效会更好？
6. 那这期间是不是得停掉对记忆系统的改造了，聚焦这一件事
7. 开始第一步吧，举一反三，小心谨慎
8. 你上面的改动记录 记得写工作手册，跟大版本架构设计放进同一个目录
9. 已归档到 wiki：queries/daily-report-2026-04-30-agent-redesign-v2-phase1-2；跟大版本架构设计手册（architectural-redesign-v2-planned）同在 queries/ 目录下。

## 这组指令教会了什么

### 1. 从外部信号开始，而不是从功能需求开始

第一句话没有说"实现 open-design"或"复制 agentic-stack"。它要求 agent
研究两个项目，并判断哪些东西对自己有帮助。

这很关键。好的 agent 进化应该从源码级学习开始：

- 外部项目解决了什么问题？
- 哪些部分是通用模式？
- 哪些部分太重、太具体或不兼容？
- 哪些应该适配，而不是照搬？

### 2. 先架构，再写代码

第二句话把 agent 从"马上实现"里拽出来。它明确这是一次大版本改动，并要求先归档架构设计手册。

这会把一个模糊改进变成一个稳定对象。后续 agent 可以读设计，而不是重新翻聊天记录。

### 3. 让迁移有顺序

"按顺序来"很短，但约束很强。它阻止 agent 在有状态、有风险的工作里自作聪明并行推进。

对 agent runtime 来说，顺序本身就是正确性的一部分。

### 4. 在落地最诱人的方案前先讨论风险

第四句和第五句把"方向认可"和"上线策略"分开：

- Plan A 是要做的
- 但不代表要立刻全量切换
- 需要比较直接切换和渐进运行

这能防止 agent 把"我同意方向"误解成"你可以马上大改"。

### 5. 迁移期间冻结相邻系统

"那这期间是不是得停掉对记忆系统的改造了"是关键转折。它意识到不能一边重构 memory，一边迁移另一个大能力。

对 agent 来说，聚焦本身就是一种安全机制。

### 6. 先落第一步，然后写手册

最后几句把实现和文档绑在一起：

- 谨慎落地第一阶段
- 写工作手册
- 放到架构手册旁边
- 明确归档路径

结果不只是一个 patch，而是一条后续 agent 可以复用的路线。

## Playbook

当你想教 agent 新能力时，可以用这个循环：

```text
外部信号
  -> 源码级研究
  -> 架构归档
  -> 按顺序讨论
  -> 风险 / 收益评审
  -> 渐进式迁移
  -> 冻结相邻系统
  -> 小步落地
  -> 工作手册
  -> 可索引的归档路径
```

最重要的是最后的 closure。一个能力只有在下一个 agent 能找到、理解、复用时，才算真的学会。

## 可复制模板

```text
研究 [外部项目 A] 和 [外部项目 B]。
不要直接复制它们。提取在当前约束下可以改进我们 agent 的部分。

如果这看起来是一次大版本架构变化，先归档设计。
然后我们按章节一步步讨论。

在实现最诱人的方案前，比较直接切换和渐进式迁移。
说清楚风险和收益。

迁移期间冻结相邻子系统，除非当前阶段必须改它们。

从第一阶段开始。尽量复用已有逻辑。小心谨慎。

改完后，把工作手册写到架构设计旁边，让下一个 agent 不需要重新发现计划。
```

## 仓库结构

```text
.
├── README.md / README.zh-CN.md      # 精简导览和阅读路线
├── examples/                        # 编号方法论，通常中英双语
├── skills/                          # 按触发词加载的 skill 包
├── assets/                          # README 和展示素材
└── qwen-start.sh                    # 本机辅助启动脚本
```

README 不再维护完整文件清单。真实结构以目录为准：

```sh
find examples -maxdepth 1 -name '*.md' | sort
find skills -maxdepth 2 -name SKILL.md | sort
```

## 阅读路线

不要默认从头读到尾。按任务选择最小阅读路线。

| 需求 | 先读 |
|---|---|
| 教 agent 沉淀一个新习惯 | [01-source-learning.zh-CN.md](examples/01-source-learning.zh-CN.md)、[02-architecture-first.zh-CN.md](examples/02-architecture-first.zh-CN.md)、[04-archive-the-work.zh-CN.md](examples/04-archive-the-work.zh-CN.md) |
| 安全修改运行时 | [03-progressive-rollout.zh-CN.md](examples/03-progressive-rollout.zh-CN.md)、[12-runtime-identity-correction.zh-CN.md](examples/12-runtime-identity-correction.zh-CN.md)、[38-agent-runtime-repair-loop.zh-CN.md](examples/38-agent-runtime-repair-loop.zh-CN.md) |
| 处理认知、记忆、注意力 | [10-cognitive-governance.zh-CN.md](examples/10-cognitive-governance.zh-CN.md)、[28-agent-attention-governance.zh-CN.md](examples/28-agent-attention-governance.zh-CN.md)、[36-agent-memory-store-retrieve-loop.zh-CN.md](examples/36-agent-memory-store-retrieve-loop.zh-CN.md) |
| 防止架构堆砌 | [25-agent-final-architecture-outline.zh-CN.md](examples/25-agent-final-architecture-outline.zh-CN.md)、[31-agent-anti-bloat-context-engineering.zh-CN.md](examples/31-agent-anti-bloat-context-engineering.zh-CN.md)、[32-agent-skill-engineering.zh-CN.md](examples/32-agent-skill-engineering.zh-CN.md) |
| 落到 GenericAgent | [33-ga-implementation-map.zh-CN.md](examples/33-ga-implementation-map.zh-CN.md)、[37-agent-flowing-conversation-thread.zh-CN.md](examples/37-agent-flowing-conversation-thread.zh-CN.md)、[38-agent-runtime-repair-loop.zh-CN.md](examples/38-agent-runtime-repair-loop.zh-CN.md) |
| 打磨用户可见输出 | [13-verified-runtime-repairs-2026-05-18.zh-CN.md](examples/13-verified-runtime-repairs-2026-05-18.zh-CN.md)、[19-platform-writing.zh-CN.md](examples/19-platform-writing.zh-CN.md)、[35-scene-to-agent-skill.zh-CN.md](examples/35-scene-to-agent-skill.zh-CN.md) |
| 售卖和交付企业级 agent | [39-enterprise-agent-commercialization.zh-CN.md](examples/39-enterprise-agent-commercialization.zh-CN.md)、[enterprise-agent-commercialization](skills/enterprise-agent-commercialization/SKILL.zh-CN.md) |

多数编号 example 都有 `.zh-CN.md` 版本。已知单语例外只在原始材料本身就是本地或场景化资产时保留：`08-fuse-external-into-local-architecture.md` 和 `2026-05-17-抖音风控应对策略.md`。

## Skill 包

`skills/` 是工作中的能力库，不是默认全读清单。按触发词加载，常驻上下文保持小。

核心 agent 进化入口：

- [agent-anti-bloat-context-engineering](skills/agent-anti-bloat-context-engineering/SKILL.md) — 压缩主运行路径，把大型工作状态移出 prompt。
- [agent-skill-creator](skills/agent-skill-creator/SKILL.md) — 把重复工作沉淀成紧凑、可触发、可验证的 skill。
- [agent-output-workbench](skills/agent-output-workbench/SKILL.md) — 让聊天长任务可读，而不是暴露 raw trace。
- [agent-memory-store-retrieve-loop](skills/agent-memory-store-retrieve-loop/SKILL.md) — 打通证据捕获、回忆、晋升和运行时取用。
- [agent-flowing-conversation-thread](skills/agent-flowing-conversation-thread/SKILL.md) — 在用户运行中继续说话时保持上下文连续。
- [runtime-identity-correction](skills/runtime-identity-correction/SKILL.md) — 修正宿主机、工作区或运行时迁移后的过期自我认知。
- [ga-implementation-map](skills/ga-implementation-map/SKILL.md) — 把手册原则映射回 GenericAgent 源码和测试。
- [enterprise-agent-commercialization](skills/enterprise-agent-commercialization/SKILL.zh-CN.md) — 把企业级 agent 工作包装成诊断、工作坊、落地计划、转化钩子和复购路径。

架构与认知类 skill 适合设计阶段使用，但也应按需触发：`agent-final-architecture-outline`、`agent-attention-governance`、`agent-thinking-core`、`agent-consciousness-math`、`cognitive-governance`、`full-stack-agent-intelligence`，以及相关修炼/人类信号技能。

领域和工具类 skill 仍保留在 `skills/` 下，但不属于默认 agent 进化阅读路径。任务明确提到领域、工具、市场、文档格式或平台时再检索。

新增或保留 skill 前，先问反堆砌三问：

1. 是否降低上下文获取成本？
2. 是否提升状态稳定性？
3. 是否增强对真实环境的理解？

如果答案不是肯定，就把它留在 example、归档笔记或领域 skill 中，不要推入主路径。

## 不要做什么

- 不要只对 agent 说"变聪明一点"，却不给它要写入的 artifact。
- 不要让 research 和 implementation 混在一句话里。
- 不要一次性改 memory、tools、prompts 和 runtime wiring。
- 不要在设计、变更记录和延续路径可被找到前接受"完成"。
- 不要因为一个外部项目看起来先进就直接照搬。
- 不要静默修改 agent 自有表面，却不说明影响和回滚方式。
- 不要把所有记忆/技能都加载到系统提示词中——在受限环境下使用触发式注入。

## 为什么有效

Agents 很擅长响应当前压力，但不擅长跨 turn、重启和工具失败保存长期意图。

这条 prompt trail 把压力放在正确的位置：

- 采纳前先研究
- 迁移前先架构
- 速度前先排序
- 切换前先评审风险
- 结束前先文档化

这就是一段对话变成升级路径的方式。

## 架构原则（来自 Hermes 生产经验）

### 1. 分层记忆 + 触发式注入

永远不要把所有记忆都塞进系统提示词。使用四层架构：

| 层级 | 名称 | 加载策略 |
|-------|------|----------|
| 印象层 | 短期任务状态 | 始终加载（极小） |
| 锚点层 | 触发规则索引 | 始终加载（~500 tokens） |
| 本能层 | 框架、宪法 | 触发词匹配时加载 |
| 技能/记忆层 | 具体操作、配置 | 触发词匹配时加载 |

这使得即使有 200+ skills，系统提示词也能保持在 12K tokens 以下。

### 2. 带可见讨论的自我进化

Agent 应该改进自己，但修改 agent 自有表面（AGENTS.md、memory、prompts、skills）时必须让用户看见影响。可见讨论要求：影响文件 → 为什么 → 风险 → 回滚 → 用户可纠偏。

### 3. 渐进式迁移 > 大爆炸

对任何架构变更：shadow 模式 → 并行运行 → 渐进式迁移 → 全量切换。这就是 Phase 7 记忆架构切换如何在零宕机下完成的方法。

### 4. 一切都要归档

每个设计决策、迁移日志和工作手册都要放到可查找的位置（wiki、gbrain 或 docs/）。聊天记录不是存储系统。

### 5. 聚焦即安全

迁移期间冻结相邻子系统。在 2GB 服务器上，你不能同时重新设计 memory 和迁移 tool routing。
