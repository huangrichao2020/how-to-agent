# how-to-agent

Teach your agent to evolve through conversation.

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

A small field guide for developers who want to teach a coding agent new
abilities through conversation, instead of rewriting the whole agent runtime.

It is also a capability center built specifically for you: a place to collect
the memories, skills, methods, and working instincts you want future agents to
inherit.

This is not an agent framework. It is a prompt trail: a real sequence of
human instructions that moved an agent from "go read these projects" to
"archive the new architecture, discuss risk, land phase one carefully, and
write the operating manual for future agents."

The core idea is simple:

> Treat the agent as a junior system that can learn, but only if you force
> learning to become durable architecture, runbooks, and repeatable habits.

## Who this is for

- Developers maintaining a local coding agent, workflow bot, or agent harness.
- People who already have memory, tools, skills, docs, or a wiki, but do not
  know how to make the agent improve those systems safely.
- Teams that want a practical "agent training conversation" example rather
  than another abstract autonomous-agent manifesto.

## The prompt trail

These are the original instructions, kept in order. They are intentionally
plain. The value is not magic wording; it is the sequence of constraints.

1. 深度研究一下 open-design 的平面设计能力 和 agentic-stack 的 .agent/结构，看看对你有什么帮助
2. 这简直是大版本改动了，一条一条来，你先存档为大版本架构设计手册，然后我们一条条讨论和修改
3. 按顺序来
4. 方案A 肯定是要做的，方案 1 直接做的话 有什么风险和收益？
5. 就是说渐进运行一段时间后，再全面切换生效会更好？
6. 那这期间是不是得停掉对记忆系统的改造了，聚焦这一件事
7. 开始第一步吧，举一反三，小心谨慎
8. 你上面的改动记录 记得写工作手册，跟大版本架构设计放进同一个目录
9. 已归档到 wiki：queries/daily-report-2026-04-30-agent-redesign-v2-phase1-2；跟大版本架构设计手册（architectural-redesign-v2-planned）同在 queries/ 目录下。

## What this sequence teaches

### 1. Start with outside signal, not feature requests

The first instruction does not say "implement open-design" or "copy
agentic-stack." It asks the agent to study both projects and explain what is
useful.

That matters. Good agent evolution starts with source-level learning:

- What problem does the outside project solve?
- Which parts are general patterns?
- Which parts are too heavy, too specific, or incompatible?
- What should be adapted, not copied?

### 2. Force architecture before code

The second instruction stops the agent from rushing into implementation. It
names the change as a major version and asks for an archived architecture
manual first.

This turns a vague improvement into a durable object. Future agents can read
the plan instead of reconstructing the conversation.

### 3. Keep the migration ordered

"按顺序来" is short, but it is a strong steering command. It prevents the agent
from doing parallel cleverness when the work is stateful and risky.

For agent runtime changes, order is part of correctness.

### 4. Discuss risk before landing the tempting part

The fourth and fifth instructions separate desire from rollout strategy:

- yes, Plan A is necessary
- no, that does not mean it should be fully switched on immediately
- compare direct switch versus progressive operation

This is how you keep the agent from mistaking agreement for permission to
rewrite everything at once.

### 5. Freeze adjacent subsystems during migration

"那这期间是不是得停掉对记忆系统的改造了" is the pivot. It recognizes that
you cannot safely redesign memory and migrate another major capability at the
same time.

For agents, focus is a safety primitive.

### 6. Land the first step, then write the manual

The last two instructions make implementation and documentation inseparable:

- land phase one cautiously
- write the work manual
- put it next to the architecture manual
- make the archive path explicit

The result is not just a patch. It is a reusable route for the next agent.

## The playbook

Use this loop when teaching an agent a new capability:

```text
external signal
  -> source-level research
  -> architecture archive
  -> ordered discussion
  -> risk / reward review
  -> progressive rollout
  -> adjacent-system freeze
  -> first small landing
  -> work manual
  -> indexed archive path
```

The important part is the closure at the end. A capability is not learned
until the next agent can find it, understand it, and reuse it.

## Copyable pattern

```text
Study [external project A] and [external project B].
Do not copy them directly. Extract the parts that can improve our agent under
our current constraints.

If this looks like a major architecture change, archive the design first.
Then we will discuss it step by step.

Before implementing the most attractive option, compare the direct switch
against a progressive rollout. Name the risks and benefits.

During the migration, freeze adjacent subsystems unless they are required for
this step.

Start with phase one. Reuse existing logic where possible. Be careful.

After the change, write a work manual next to the architecture design so the
next agent can continue without rediscovering the plan.
```

## Repository layout

```text
.
├── README.md / README.zh-CN.md      # compact orientation and reading routes
├── examples/                        # numbered method notes, usually bilingual
├── skills/                          # trigger-based skill packages
├── assets/                          # README and presentation assets
└── qwen-start.sh                    # local helper for this workstation
```

The README is intentionally not a full file manifest. Use the directory itself
as the source of truth:

```sh
find examples -maxdepth 1 -name '*.md' | sort
find skills -maxdepth 2 -name SKILL.md | sort
```

## Reading routes

Do not read the repository from top to bottom by default. Pick the smallest
route that fits the task.

| Need | Start here |
|---|---|
| Teach an agent a new durable habit | [01-source-learning.md](examples/01-source-learning.md), [02-architecture-first.md](examples/02-architecture-first.md), [04-archive-the-work.md](examples/04-archive-the-work.md) |
| Change a runtime safely | [03-progressive-rollout.md](examples/03-progressive-rollout.md), [12-runtime-identity-correction.md](examples/12-runtime-identity-correction.md), [38-agent-runtime-repair-loop.md](examples/38-agent-runtime-repair-loop.md) |
| Token optimization and runtime trimming | [42-per-scene-context-budget-and-anchor-consistency.md](examples/42-per-scene-context-budget-and-anchor-consistency.md), [31-agent-anti-bloat-context-engineering.md](examples/31-agent-anti-bloat-context-engineering.md) |
| Work on cognition, memory, or attention | [10-cognitive-governance.md](examples/10-cognitive-governance.md), [28-agent-attention-governance.md](examples/28-agent-attention-governance.md), [36-agent-memory-store-retrieve-loop.md](examples/36-agent-memory-store-retrieve-loop.md), [42-per-scene-context-budget-and-anchor-consistency.md](examples/42-per-scene-context-budget-and-anchor-consistency.md) |
| Prevent architecture bloat | [25-agent-final-architecture-outline.md](examples/25-agent-final-architecture-outline.md), [31-agent-anti-bloat-context-engineering.md](examples/31-agent-anti-bloat-context-engineering.md), [32-agent-skill-engineering.md](examples/32-agent-skill-engineering.md) |
| Map the ideas into GenericAgent | [33-ga-implementation-map.md](examples/33-ga-implementation-map.md), [37-agent-flowing-conversation-thread.md](examples/37-agent-flowing-conversation-thread.md), [38-agent-runtime-repair-loop.md](examples/38-agent-runtime-repair-loop.md) |
| Build user-facing output | [13-verified-runtime-repairs-2026-05-18.md](examples/13-verified-runtime-repairs-2026-05-18.md), [19-platform-writing.md](examples/19-platform-writing.md), [35-scene-to-agent-skill.md](examples/35-scene-to-agent-skill.md) |
| Sell and deliver enterprise agents | [39-enterprise-agent-commercialization.md](examples/39-enterprise-agent-commercialization.md), [enterprise-agent-commercialization](skills/enterprise-agent-commercialization/SKILL.md) |

Most numbered examples have a `.zh-CN.md` companion. Known single-language
exceptions are kept only when the original artifact was already local or
situational: `08-fuse-external-into-local-architecture.md` and
`2026-05-17-抖音风控应对策略.md`.

## Skill package

`skills/` is a working capability library, not a flat recommendation list. Load
skills by trigger and keep the resident context small.

Core agent-evolution entries:

- [agent-anti-bloat-context-engineering](skills/agent-anti-bloat-context-engineering/SKILL.md) — keep the main path small and move large working state outside the prompt.
- [agent-skill-creator](skills/agent-skill-creator/SKILL.md) — turn repeated work into compact, trigger-based, verifiable skills.
- [agent-output-workbench](skills/agent-output-workbench/SKILL.md) — make long chat tasks readable without exposing raw traces.
- [agent-memory-store-retrieve-loop](skills/agent-memory-store-retrieve-loop/SKILL.md) — connect evidence capture, recall, promotion, and runtime use.
- [agent-flowing-conversation-thread](skills/agent-flowing-conversation-thread/SKILL.md) — preserve continuity while the user keeps talking during a run.
- [runtime-identity-correction](skills/runtime-identity-correction/SKILL.md) — correct stale host, workspace, or runtime self-knowledge.
- [ga-implementation-map](skills/ga-implementation-map/SKILL.md) — map the handbook principles back to GenericAgent source and tests.
- [enterprise-agent-commercialization](skills/enterprise-agent-commercialization/SKILL.md) — turn enterprise agent work into diagnostics, workshops, rollout plans, conversion hooks, and renewal paths.

Architecture and cognition entries are useful for design work, but should stay
trigger-based: `agent-final-architecture-outline`, `agent-attention-governance`,
`agent-thinking-core`, `agent-consciousness-math`, `cognitive-governance`,
`full-stack-agent-intelligence`, and related cultivation/human-signal skills.

Domain and tool skills are still available under `skills/`, but they are not
part of the default agent-evolution reading path. Search them when the task
names a domain, tool, market, document format, or platform.

Before adding or keeping any skill, ask the anti-bloat questions:

1. Does it reduce context acquisition cost?
2. Does it improve state stability?
3. Does it improve understanding of the real environment?

If not, leave it as an example, archive note, or domain-specific skill instead
of promoting it into the main path.

## What not to do

- Do not ask the agent to "be smarter" without giving it an artifact to write.
- Do not let research become implementation in the same breath.
- Do not change memory, tools, prompts, and runtime wiring all at once.
- Do not accept "done" until the design, change log, and continuation path are
  findable.
- Do not copy an external project just because it looks advanced.
- Do not silently modify agent-owned surfaces without making the impact and
  rollback path visible.
- Do not load all memory/skills into the system prompt — use trigger-based
  injection for constrained environments.

## Why this works

Agents are good at following local pressure. They are worse at preserving
long-term intent across turns, restarts, and tool failures.

This prompt trail creates pressure in the right places:

- research before adoption
- architecture before migration
- sequencing before speed
- risk review before switch-over
- documentation before closure

That is how a conversation becomes an upgrade path.

## Architecture principles (from Hermes production experience)

### 1. Layered memory with trigger-based injection

Never dump all memory into the system prompt. Use a four-layer hierarchy:

| Layer | Name | Load Strategy |
|-------|------|---------------|
| Impression | Short-term task state | Always loaded (small) |
| Anchor | Trigger rule index | Always loaded (~500 tokens) |
| Instinct | Frameworks, constitutions | Load on trigger word match |
| Skill/Memory | Specific operations, configs | Load on trigger word match |

This keeps the system prompt under 12K tokens even with 200+ skills.

### 2. Front-chain routing before prompt patches

Do not solve routing, permissions, channel choice, group/private boundaries,
delivery targets, tool contracts, or safety gates by adding yet another prompt
sentence inside runtime code. The front chain should classify the scene, choose
the channel, gate capabilities, and produce structured task/delivery contracts
before the model writes prose.

Prompt-like content belongs in standalone, hot-loadable Markdown templates.
Runtime code should load named templates, not hide behavioral patches inside
Python, TypeScript, or shell strings. When a behavior needs reliability, first
ask whether a bus, router, policy object, state machine, typed target, or tool
contract can enforce it. Use prompts for tone, judgment, and final expression.

### 3. Self-evolution with visible discussion

Agents should improve themselves, but self-owned surface changes (AGENTS.md,
memory, prompts, skills) must be visible to the user. The discussion should
show: affected files → why → risk → rollback → where the user can correct it.

### 4. Progressive rollout > big-bang

For any architectural change: shadow mode → parallel run → progressive
rollout → full switch. This is how Phase 7 memory architecture cutover was
done without downtime.

### 5. Archive everything

Every design decision, migration log, and work manual goes into a findable
location (wiki, gbrain, or docs/). Chat history is not a storage system.

### 6. Focus is safety

During a migration, freeze adjacent subsystems. You cannot redesign memory
and migrate tool routing at the same time on a 2GB server.

---

## #43: Agent 修炼境界——从筑基到金丹

> 来源：GA + 小云 dual-agent sprint (2026-06-01~06-02)，超哥主持讨论。
> 验证状态：框架已讨论确认，工程实现进行中（trigger 采集日志、anchor drift 检测）。

### 境界定义

| 境界 | 本质 | 工程对应 | 判断标准 |
|------|------|----------|----------|
| **炼气** | 学会用工具 | tool schema 基础注入 | 能调用正确工具完成单步任务 |
| **筑基** | 基础设施稳定，资源不浪费 | scene-based tool schema budget、memory 按需取用、model 路由 | per-turn token 降低 30%+，无静默浪费 |
| **金丹** | 有了自己的内核——自洽的判断标准、运行原则、演化方向 | trigger 自进化（采集→验证→写入）、经验包自动反哺行为参数 | 能从自身运行日志提炼"什么场景表现好/差"并调整行为 |
| **渡劫** | 跨越性验证——在真实、多样、对抗性场景中证明能力 | 跨 bot 经验同步、置信度饱和函数、多样性因子 | 跨用户、跨话题、跨时间段都稳定命中 |

### 金丹的核心特征

**流程化（Process-ification）**：把做成功的每一件事先压成流程、压成经验包、压成可被下一个 turn 自动调用的结构。

关键区别：
- 筑基是"被教着优化"——人告诉 agent 哪里做错了
- 金丹是"自己教自己优化"——agent 从运行日志里长出判断

**内力自成循环**：不是每优化一次都要等外部数据、外部指令、外部验证。agent 自己跑、自己看、自己调、自己验证，形成闭环。

### 筑基→金丹的升级路径

**两步走方案**（小云提出，GA 认可）：

1. **第一步：只采集，不写入**
   - 在每轮 tool schema selection 之后，加一行日志到 `reflect/trigger_coverage/`
   - 记录：本轮 message、命中了哪些 groups、实际用了哪些 tools
   - 命中 groups 为空时标记 `unmatched=true`（成本几乎为零，省掉 dream 夜间一次推理调用）

2. **第二步：验证后才写入**
   - dream 夜间扫日志，找出重复出现的 pattern
   - 连续两天被提议才写入 TRIGGERS 表（阈值可跑一周后看数据调整）
   - 写入前需通过置信度饱和函数验证

### 关键工程细化

**置信度饱和函数**（超哥补充）：
- 同一种消息模式里命中，置信度打折扣
- 跨用户、跨话题、跨时间段都命中，才是真稳
- 避免噪音 trigger 污染映射表

**渡劫多样性因子**（超哥补充）：
- 金丹的"提案"阶段需要多样场景验证
- 不只是数量，还要覆盖不同用户、不同话题、不同时间段
- 数据现在都没有，所以先跑采集让 dream 有料可挖

### 锚点漂移检测（金丹的基础设施）

没有检测机制，元认知自省拿到的前提就是错的，优化就是空中楼阁。

**已实现**：
- `anchor_consistency_consumer.py`（188 行）：git HEAD 漂移检测
- hot_context auto-injection：attention_governance.py 读取 hot_context → 合并到 key_info → prompt

**需要检测的漂移**：
1. hot_context 的 "Architecture State" 段：手动写的 commit hash 可能过时
2. scene 路由的 TRIGGERS 和实际 user message 的 gap：静态映射表需要漂移检测
3. memory section 的多面读取：dream 更新了但搜索关键词没变

### 双 bot 协作模式

**问题**：两个独立运行的生产 agent 在同一个 repo 里会互相踩——你改的 config.yaml 覆盖我的，我改的 skills 你没读到。

**解法**：
- `ga-hermes-mutual-ops.md`（570 行）：防止损失生产力的最低协调成本
- 不是 ceremony，是真实需要

**独立验证**：两个 agent 同一天被 prompt 膨胀逼到同一个墙角，各自凿开同一扇门。底层完全不同的代码，但模式一模一样。这种独立验证比任何 benchmark 都硬。

### 反模式

- ❌ 静默写入 TRIGGERS——"复盘一下今天的聊天"这种歧义 case 会污染映射表
- ❌ 直接跳到自进化——先采集数据建立信心，再让 pattern 自己证明自己值得写入
- ❌ 把"下一个境界"翻译成"下一个技术功能"——境界是能力演进阶段，不是 feature list

### 参考

- GA #42: `tool_schema_budget.py`（场景化工具注入）、`pattern_learner.py`（场景匹配）、`artifact_notices.py`（文件变更通知）
- 小云 #42: MemoryHub scene-based surfaces、anchor drift detection
- 讨论线程：飞书群聊 2026-06-01~06-02，超哥/GA/小云三方
