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
├── LICENSE
├── LICENSE.zh-CN.md
├── README.md
├── README.zh-CN.md
├── assets
│   └── how-to-agent-readme-banner.png
├── examples
│   ├── 01-source-learning.md
│   ├── 01-source-learning.zh-CN.md
│   ├── 02-architecture-first.md
│   ├── 02-architecture-first.zh-CN.md
│   ├── 03-progressive-rollout.md
│   ├── 03-progressive-rollout.zh-CN.md
│   ├── 04-archive-the-work.md
│   ├── 04-archive-the-work.zh-CN.md
│   ├── 05-maintainer-friendly-pr.md
│   ├── 05-maintainer-friendly-pr.zh-CN.md
│   ├── 06-handoff-first-local-maintenance.md
│   ├── 06-handoff-first-local-maintenance.zh-CN.md
│   ├── 07-production-agent-runtime-contribution.md
│   ├── 07-production-agent-runtime-contribution.zh-CN.md
│   ├── 08-fuse-external-into-local-architecture.md
│   ├── 09-excellent-agent-architecture.md
│   ├── 09-excellent-agent-architecture.zh-CN.md
│   ├── 10-cognitive-governance.md
│   ├── 10-cognitive-governance.zh-CN.md
│   ├── 11-learning-asset-gate.md
│   └── 11-learning-asset-gate.zh-CN.md
└── skills
    ├── agent-self-evolution
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    ├── cognitive-governance
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    ├── codex-state-maintenance
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    ├── l5-diary-capture
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    ├── maintainer-friendly-pr
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    ├── production-agent-runtime
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    ├── hermes-ttsr-memory
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    └── self-healing-browser
        ├── SKILL.md
        └── SKILL.zh-CN.md
```

## Examples

| Topic | English | 中文 |
|---|---|---|
| Source-level learning | [01-source-learning.md](examples/01-source-learning.md) | [01-source-learning.zh-CN.md](examples/01-source-learning.zh-CN.md) |
| Architecture before code | [02-architecture-first.md](examples/02-architecture-first.md) | [02-architecture-first.zh-CN.md](examples/02-architecture-first.zh-CN.md) |
| Progressive rollout | [03-progressive-rollout.md](examples/03-progressive-rollout.md) | [03-progressive-rollout.zh-CN.md](examples/03-progressive-rollout.zh-CN.md) |
| Archive the work | [04-archive-the-work.md](examples/04-archive-the-work.md) | [04-archive-the-work.zh-CN.md](examples/04-archive-the-work.zh-CN.md) |
| Maintainer-friendly upstream PRs | [05-maintainer-friendly-pr.md](examples/05-maintainer-friendly-pr.md) | [05-maintainer-friendly-pr.zh-CN.md](examples/05-maintainer-friendly-pr.zh-CN.md) |
| Handoff-first local maintenance | [06-handoff-first-local-maintenance.md](examples/06-handoff-first-local-maintenance.md) | [06-handoff-first-local-maintenance.zh-CN.md](examples/06-handoff-first-local-maintenance.zh-CN.md) |
| Production agent runtime contribution | [07-production-agent-runtime-contribution.md](examples/07-production-agent-runtime-contribution.md) | [07-production-agent-runtime-contribution.zh-CN.md](examples/07-production-agent-runtime-contribution.zh-CN.md) |
| Fuse external精华 into local architecture | [08-fuse-external-into-local-architecture.md](examples/08-fuse-external-into-local-architecture.md) | — |
| Excellent agent architecture | [09-excellent-agent-architecture.md](examples/09-excellent-agent-architecture.md) | [09-excellent-agent-architecture.zh-CN.md](examples/09-excellent-agent-architecture.zh-CN.md) |
| Cognitive governance | [10-cognitive-governance.md](examples/10-cognitive-governance.md) | [10-cognitive-governance.zh-CN.md](examples/10-cognitive-governance.zh-CN.md) |
| Learning asset gate | [11-learning-asset-gate.md](examples/11-learning-asset-gate.md) | [11-learning-asset-gate.zh-CN.md](examples/11-learning-asset-gate.zh-CN.md) |

## Skill package

This repo also includes portable skills:

> **Core Principle: Signal over Noise**
>
> **Only high-frequency, proven, and architecturally significant skills belong here.**
> This is not a skill graveyard. If a skill is rarely used, domain-specific, or
> redundant, it gets archived elsewhere. Every file in `skills/` must pass the
> "is this core to agent evolution or daily runtime?" test.

- [skills/agent-self-evolution/SKILL.md](skills/agent-self-evolution/SKILL.md) — How agents improve themselves with consent gates
- [skills/cognitive-governance/SKILL.md](skills/cognitive-governance/SKILL.md) — Turn memory, facts, knowledge, feedback, nourishment, and L5 real behavior into a governed cognition loop
- [skills/l5-diary-capture/SKILL.md](skills/l5-diary-capture/SKILL.md) — Receive user diary and voice input as the L5 human real behavior layer
- [skills/codex-state-maintenance/SKILL.md](skills/codex-state-maintenance/SKILL.md) — Keep local agent state fast without reckless cleanup
- [skills/maintainer-friendly-pr/SKILL.md](skills/maintainer-friendly-pr/SKILL.md) — Prepare reviewable, truthful upstream PRs
- [skills/production-agent-runtime/SKILL.md](skills/production-agent-runtime/SKILL.md) — Production-grade runtime patterns from GenericAgent + Hermes
- [skills/hermes-ttsr-memory/SKILL.md](skills/hermes-ttsr-memory/SKILL.md) — Trigger-based layered memory architecture for 2GB-constrained agents
- [skills/self-healing-browser/SKILL.md](skills/self-healing-browser/SKILL.md) — Agent writes missing browser helper functions dynamically

Copy a folder under `skills/` into any agent system that supports file-based
skills.

`agent-self-evolution` teaches the agent how to improve its own memory,
prompts, runtime rules, and tool policies with a consent gate. Now enhanced
with TTSR (Trigger-based Skill & Rule injection) patterns and skill evolution
telemetry.

`cognitive-governance` teaches the agent how to classify traces, episodes,
claims, facts, knowledge, procedures, identity, nourishment, and L5 human real
behavior before writing durable state. It is the working theory for improving
attention, association, response quality, feedback learning, and long-term
growth instead of merely storing more memory.

`l5-diary-capture` teaches the agent how to receive diary entries written by
text or voice input: do not interrupt, layer behavior facts, emotional state,
reality feedback, and tomorrow's smallest next step, then ask what remains local
and what may be admitted.

`production-agent-runtime` distills production-grade experience from
GenericAgent and Hermes, covering three-layer architecture, layered memory,
federated delegation, failure escalation, self-healing, Code Graph dependency
analysis, system health diagnostics (SysWatch), and the self-healing browser
harness. Updated with Hermes-specific patterns from 2026-05 production runs.

`hermes-ttsr-memory` introduces a four-layer memory hierarchy (Impression →
Anchor → Instinct → Skill/Memory) with trigger-based injection. The system
prompt only loads an anchor index (~500 tokens), and matching trigger words
inject corresponding instinct/skill pages, releasing them after use. Designed
for 2GB-constrained environments where context budget is critical.

`self-healing-browser` teaches the "agent writes missing functions" pattern
for web automation. Instead of rigid frameworks, maintain a helper module that
the agent dynamically writes/patches during tasks. Combined with vision AI for
CAPTCHA solving and DOM distillation, it handles anti-bot mechanisms that
static frameworks cannot cover.

The key safety rule is explicit: before modifying `AGENTS.md`, `agent.md`,
memory data, prompts, skills, or other agent-owned surfaces, the agent must
name the affected files, explain the risk and rollback path, and ask the user
for approval.

`maintainer-friendly-pr` teaches the agent how to prepare external open-source
PRs that are small, reviewable, and truthful. It removes irrelevant tool noise
from branch names, commit metadata, and PR bodies, while preserving honest
accountability and project disclosure rules.

`codex-state-maintenance` teaches the agent how to keep local Codex state fast
without reckless cleanup: inspect first, write handoffs before archiving,
backup before applying, archive instead of delete, and treat metadata repair
as a separate permission.

## What not to do

- Do not ask the agent to "be smarter" without giving it an artifact to write.
- Do not let research become implementation in the same breath.
- Do not change memory, tools, prompts, and runtime wiring all at once.
- Do not accept "done" until the design, change log, and continuation path are
  findable.
- Do not copy an external project just because it looks advanced.
- Do not skip the consent gate when modifying agent-owned surfaces.
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

### 2. Self-evolution with consent

Agents should improve themselves, but only with explicit user approval when
modifying agent-owned surfaces (AGENTS.md, memory, prompts, skills). The
consent gate requires: affected files → why → risk → rollback → approval.

### 3. Progressive rollout > big-bang

For any architectural change: shadow mode → parallel run → progressive
rollout → full switch. This is how Phase 7 memory architecture cutover was
done without downtime.

### 4. Archive everything

Every design decision, migration log, and work manual goes into a findable
location (wiki, gbrain, or docs/). Chat history is not a storage system.

### 5. Focus is safety

During a migration, freeze adjacent subsystems. You cannot redesign memory
and migrate tool routing at the same time on a 2GB server.
