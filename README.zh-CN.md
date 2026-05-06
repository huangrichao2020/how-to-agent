# how-to-use-agent

通过对话教会你的 agent 自我进化。

<p align="center">
  <img src="assets/how-to-use-agent-readme-banner.png" alt="How to Use Agent README banner" width="100%">
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![English](https://img.shields.io/badge/docs-English-blue)](README.md)
[![中文](https://img.shields.io/badge/docs-中文-red)](README.zh-CN.md)
[![GitHub stars](https://img.shields.io/github/stars/huangrichao2020/how-to-use-agent?style=social)](https://github.com/huangrichao2020/how-to-use-agent)

<p align="center">
  <a href="README.md"><strong>English</strong></a>
  ·
  <a href="README.zh-CN.md"><strong>简体中文</strong></a>
</p>

这是一个面向开发者的小型实战指南：如何通过连续对话，让 coding
agent 学会新能力，而不是一上来就重写整个 agent runtime。

它也是一个单独为你打造的能力中心：用来沉淀你希望未来 agent 继承的记忆、技能、方法论和工作印象。

它不是一个 agent 框架。它是一条真实的 prompt trail：一组人类按顺序发给
agent 的指令，把 agent 从“去研究这些项目”一步步推到“归档新架构、讨论风险、谨慎落地第一阶段，并为后续 agent 写工作手册”。

核心想法很简单：

> 把 agent 当成一个能学习的初级系统。但只有当你逼它把学习沉淀成架构、runbook
> 和可重复习惯时，学习才会真正留下来。

## 适合谁

- 正在维护本地 coding agent、工作流机器人或 agent harness 的开发者。
- 已经有 memory、tools、skills、docs 或 wiki，但不知道如何让 agent 安全改进这些系统的人。
- 想看真实“调教 agent 的对话过程”，而不是又一篇抽象 autonomous-agent 宣言的团队。

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

第一句话没有说“实现 open-design”或“复制 agentic-stack”。它要求 agent
研究两个项目，并判断哪些东西对自己有帮助。

这很关键。好的 agent 进化应该从源码级学习开始：

- 外部项目解决了什么问题？
- 哪些部分是通用模式？
- 哪些部分太重、太具体或不兼容？
- 哪些应该适配，而不是照搬？

### 2. 先架构，再写代码

第二句话把 agent 从“马上实现”里拽出来。它明确这是一次大版本改动，并要求先归档架构设计手册。

这会把一个模糊改进变成一个稳定对象。后续 agent 可以读设计，而不是重新翻聊天记录。

### 3. 让迁移有顺序

“按顺序来”很短，但约束很强。它阻止 agent 在有状态、有风险的工作里自作聪明并行推进。

对 agent runtime 来说，顺序本身就是正确性的一部分。

### 4. 在落地最诱人的方案前先讨论风险

第四句和第五句把“方向认可”和“上线策略”分开：

- Plan A 是要做的
- 但不代表要立刻全量切换
- 需要比较直接切换和渐进运行

这能防止 agent 把“我同意方向”误解成“你可以马上大改”。

### 5. 迁移期间冻结相邻系统

“那这期间是不是得停掉对记忆系统的改造了”是关键转折。它意识到不能一边重构 memory，一边迁移另一个大能力。

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
├── LICENSE
├── LICENSE.zh-CN.md
├── README.md
├── README.zh-CN.md
├── assets
    └── how-to-use-agent-readme-banner.png
├── examples
    ├── 01-source-learning.md
    ├── 01-source-learning.zh-CN.md
    ├── 02-architecture-first.md
    ├── 02-architecture-first.zh-CN.md
    ├── 03-progressive-rollout.md
    ├── 03-progressive-rollout.zh-CN.md
    ├── 04-archive-the-work.md
    ├── 04-archive-the-work.zh-CN.md
    ├── 05-maintainer-friendly-pr.md
    ├── 05-maintainer-friendly-pr.zh-CN.md
    ├── 06-handoff-first-local-maintenance.md
    └── 06-handoff-first-local-maintenance.zh-CN.md
└── skills
    ├── agent-self-evolution
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    ├── codex-state-maintenance
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    └── maintainer-friendly-pr
        ├── SKILL.md
        └── SKILL.zh-CN.md
```

## 示例

| 主题 | English | 中文 |
|---|---|---|
| 源码级学习 | [01-source-learning.md](examples/01-source-learning.md) | [01-source-learning.zh-CN.md](examples/01-source-learning.zh-CN.md) |
| 先架构后代码 | [02-architecture-first.md](examples/02-architecture-first.md) | [02-architecture-first.zh-CN.md](examples/02-architecture-first.zh-CN.md) |
| 渐进式迁移 | [03-progressive-rollout.md](examples/03-progressive-rollout.md) | [03-progressive-rollout.zh-CN.md](examples/03-progressive-rollout.zh-CN.md) |
| 归档工作成果 | [04-archive-the-work.md](examples/04-archive-the-work.md) | [04-archive-the-work.zh-CN.md](examples/04-archive-the-work.zh-CN.md) |
| 面向维护者的上游 PR | [05-maintainer-friendly-pr.md](examples/05-maintainer-friendly-pr.md) | [05-maintainer-friendly-pr.zh-CN.md](examples/05-maintainer-friendly-pr.zh-CN.md) |
| 先交接再维护本地状态 | [06-handoff-first-local-maintenance.md](examples/06-handoff-first-local-maintenance.md) | [06-handoff-first-local-maintenance.zh-CN.md](examples/06-handoff-first-local-maintenance.zh-CN.md) |

## Skill 包

这个仓库也包含可移植 skill：

- [skills/agent-self-evolution/SKILL.md](skills/agent-self-evolution/SKILL.md)
- [skills/codex-state-maintenance/SKILL.md](skills/codex-state-maintenance/SKILL.md)
- [skills/maintainer-friendly-pr/SKILL.md](skills/maintainer-friendly-pr/SKILL.md)

把 `skills/` 下面的对应目录复制到任意支持文件式 skills 的 agent 系统里即可。

`agent-self-evolution` 会教 agent 如何在用户同意门禁下，改进自己的 memory、prompts、runtime rules 和 tool policies。

核心安全规则是：在修改 `AGENTS.md`、`agent.md`、memory 数据、prompts、skills
或其他 agent 自身表面前，agent 必须列出影响文件、说明风险和回滚方式，并向用户请求同意。

`maintainer-friendly-pr` 会教 agent 如何准备外部开源 PR：让改动小、可 review、真实负责；清理分支名、commit metadata 和 PR body 里的无关工具噪声，同时遵守项目披露规则。

`codex-state-maintenance` 会教 agent 如何维护本地 Codex 状态而不鲁莽清理：先 inspect，再为旧工作写 handoff，先 backup 再 apply，用 archive 代替 delete，并把 metadata repair 当作单独授权。

## 不要做什么

- 不要只对 agent 说“变聪明一点”，却不给它要写入的 artifact。
- 不要让 research 和 implementation 混在一句话里。
- 不要一次性改 memory、tools、prompts 和 runtime wiring。
- 不要在设计、变更记录和延续路径可被找到前接受“完成”。
- 不要因为一个外部项目看起来先进就直接照搬。

## 为什么有效

Agents 很擅长响应当前压力，但不擅长跨 turn、重启和工具失败保存长期意图。

这条 prompt trail 把压力放在正确的位置：

- 采纳前先研究
- 迁移前先架构
- 速度前先排序
- 切换前先评审风险
- 结束前先文档化

这就是一段对话变成升级路径的方式。
