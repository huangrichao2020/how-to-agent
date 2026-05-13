# how-to-use-agent

Teach your agent to evolve through conversation.

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
    ├── maintainer-friendly-pr
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    └── production-agent-runtime
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

## Skill package

This repo also includes portable skills:

- [skills/agent-self-evolution/SKILL.md](skills/agent-self-evolution/SKILL.md)
- [skills/codex-state-maintenance/SKILL.md](skills/codex-state-maintenance/SKILL.md)
- [skills/maintainer-friendly-pr/SKILL.md](skills/maintainer-friendly-pr/SKILL.md)
- [skills/production-agent-runtime/SKILL.md](skills/production-agent-runtime/SKILL.md)

Copy a folder under `skills/` into any agent system that supports file-based
skills.

`agent-self-evolution` teaches the agent how to improve its own memory,
prompts, runtime rules, and tool policies with a consent gate.

`production-agent-runtime` distills production-grade experience from GenericAgent and Hermes, covering three-layer architecture, layered memory, federated delegation, failure escalation, and self-healing.

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
