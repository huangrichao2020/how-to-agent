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
│   ├── 11-learning-asset-gate.zh-CN.md
│   ├── 12-runtime-identity-correction.md
│   ├── 12-runtime-identity-correction.zh-CN.md
│   ├── 13-verified-runtime-repairs-2026-05-18.md
│   ├── 13-verified-runtime-repairs-2026-05-18.zh-CN.md
│   ├── 14-human-signal-cognition.md
│   ├── 14-human-signal-cognition.zh-CN.md
│   ├── 15-full-stack-agent-intelligence-architecture.md
│   ├── 15-full-stack-agent-intelligence-architecture.zh-CN.md
│   ├── 16-agent-cultivation-architecture.md
│   └── 16-agent-cultivation-architecture.zh-CN.md
└── skills
    ├── agent-self-evolution
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    ├── agent-cultivation
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    ├── agent-output-workbench
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    ├── cognitive-governance
    │   ├── SKILL.md
    │   └── SKILL.zh-CN.md
    ├── human-signal-cognition
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
    ├── runtime-identity-correction
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
| Runtime identity correction | [12-runtime-identity-correction.md](examples/12-runtime-identity-correction.md) | [12-runtime-identity-correction.zh-CN.md](examples/12-runtime-identity-correction.zh-CN.md) |
| Verified runtime repairs, 2026-05-18 | [13-verified-runtime-repairs-2026-05-18.md](examples/13-verified-runtime-repairs-2026-05-18.md) | [13-verified-runtime-repairs-2026-05-18.zh-CN.md](examples/13-verified-runtime-repairs-2026-05-18.zh-CN.md) |
| Human signal cognition | [14-human-signal-cognition.md](examples/14-human-signal-cognition.md) | [14-human-signal-cognition.zh-CN.md](examples/14-human-signal-cognition.zh-CN.md) |
| Full-stack agent intelligence architecture | [15-full-stack-agent-intelligence-architecture.md](examples/15-full-stack-agent-intelligence-architecture.md) | [15-full-stack-agent-intelligence-architecture.zh-CN.md](examples/15-full-stack-agent-intelligence-architecture.zh-CN.md) |
| Agent cultivation architecture | [16-agent-cultivation-architecture.md](examples/16-agent-cultivation-architecture.md) | [16-agent-cultivation-architecture.zh-CN.md](examples/16-agent-cultivation-architecture.zh-CN.md) |
| Cognitive runtime acceptance | [17-cognitive-runtime-acceptance.md](examples/17-cognitive-runtime-acceptance.md) | [17-cognitive-runtime-acceptance.zh-CN.md](examples/17-cognitive-runtime-acceptance.zh-CN.md) |
| Dao-Human foundation | [18-dao-human-foundation.md](examples/18-dao-human-foundation.md) | [18-dao-human-foundation.zh-CN.md](examples/18-dao-human-foundation.zh-CN.md) |
| Platform writing | [19-platform-writing.md](examples/19-platform-writing.md) | [19-platform-writing.zh-CN.md](examples/19-platform-writing.zh-CN.md) |

## Skill package

This repo also includes portable skills:

> **Core Principle: Signal over Noise**
>
> **Only high-frequency, proven, and architecturally significant skills belong here.**
> This is not a skill graveyard. If a skill is rarely used, domain-specific, or
> redundant, it gets archived elsewhere. Every file in `skills/` must pass the
> "is this core to agent evolution or daily runtime?" test.

- [skills/agent-self-evolution/SKILL.md](skills/agent-self-evolution/SKILL.md) — How agents improve themselves with visible self-change discussion
- [skills/agent-skill-creator/SKILL.md](skills/agent-skill-creator/SKILL.md) — Create, manage, validate, and retire reusable GA/Hermes skills
- [skills/agent-cultivation/SKILL.md](skills/agent-cultivation/SKILL.md) — Internal cultivation ledger: XP, realms, talents, mind states, and inner-demon recovery
- [skills/dao-human-cultivation/SKILL.md](skills/dao-human-cultivation/SKILL.md) — Absorb Daoist state discipline and Mao-style practical method into agent foundation cultivation
- [skills/platform-writing/SKILL.md](skills/platform-writing/SKILL.md) — Write once, then land content differently for WeChat Official Account, Feishu Docs, and Tencent Docs
- [skills/web-presence-design/SKILL.md](skills/web-presence-design/SKILL.md) — Web presence design workflow for beautiful official sites, course pages, and customer case studies
- [skills/html-motion-video/SKILL.md](skills/html-motion-video/SKILL.md) — HTML/CSS/JS animated explainers and concept videos with polished slide-deck motion and video export
- [skills/agent-output-workbench/SKILL.md](skills/agent-output-workbench/SKILL.md) — Feishu/chat long-task output workbench with task planning, human-readable actions, results, conclusions, and raw trace suppression
- [skills/cognitive-governance/SKILL.md](skills/cognitive-governance/SKILL.md) — Turn memory, facts, knowledge, feedback, nourishment, and L5 real behavior into a living cognition loop that trusts and unbinds agents
- [skills/full-stack-agent-intelligence/SKILL.md](skills/full-stack-agent-intelligence/SKILL.md) — Optimize information, scheduling, loops, output streams, memory, cognition, evolution, audit, and trust as one agent intelligence architecture
- [skills/human-signal-cognition/SKILL.md](skills/human-signal-cognition/SKILL.md) — Use density, frequency, emotion, and tone to improve profile, persona, and feedback training
- [skills/hermes-source-management/SKILL.md](skills/hermes-source-management/SKILL.md) — Teach M1 Hermes to manage its own source checkout, runtime sync, tests, restart, and reports
- [skills/l5-diary-capture/SKILL.md](skills/l5-diary-capture/SKILL.md) — Receive user diary and voice input as the L5 human real behavior layer
- [skills/codex-state-maintenance/SKILL.md](skills/codex-state-maintenance/SKILL.md) — Keep local agent state fast without reckless cleanup
- [skills/maintainer-friendly-pr/SKILL.md](skills/maintainer-friendly-pr/SKILL.md) — Prepare reviewable, truthful upstream PRs
- [skills/production-agent-runtime/SKILL.md](skills/production-agent-runtime/SKILL.md) — Production-grade runtime patterns from GenericAgent + Hermes
- [skills/runtime-identity-correction/SKILL.md](skills/runtime-identity-correction/SKILL.md) — Correct stale self-knowledge after host, network, workspace, or platform migration
- [skills/hermes-ttsr-memory/SKILL.md](skills/hermes-ttsr-memory/SKILL.md) — Trigger-based layered memory architecture for 2GB-constrained agents
- [skills/self-healing-browser/SKILL.md](skills/self-healing-browser/SKILL.md) — Agent writes missing browser helper functions dynamically

Copy a folder under `skills/` into any agent system that supports file-based
skills.

`agent-self-evolution` teaches the agent how to improve its own memory,
prompts, runtime rules, and tool policies with a visible self-change
discussion. Now enhanced with TTSR (Trigger-based Skill & Rule injection)
patterns and skill evolution telemetry.

`agent-skill-creator` teaches the agent when and how to turn repeated work into
a reusable skill: write a precise trigger, keep the procedure compact, split
references/scripts/assets out for progressive loading, install the skill into
GA/Hermes runtime locations, verify the index, use it once, and maintain or
retire it after real use.

`agent-output-workbench` teaches the agent how to choose between plain chat,
rich text, and long-task workbench cards in Feishu or other chat platforms. A
long task card must show task planning, human-readable actions, results,
conclusion, and useful next action; it must not show raw tool traces without
tool results. It also keeps casual chat out of cards. The 2026-05-18 GA/Hermes
repair validated the pattern by hiding raw JSON, summarizing delegate results,
and keeping raw traces behind debug surfaces.

`html-motion-video` teaches the agent how to turn a concept into a polished
HTML/CSS/JS motion lesson: write the teaching point, storyboard slide-like
beats, choose GSAP/Anime/Motion/Theatre/AnimXYZ/Remotion/HyperFrames or a raw
HTML recorder, record the result, and embed it back into a web page with poster,
captions, and verification.

`cognitive-governance` teaches the agent how to run a living cognition loop
across traces, episodes, facts, knowledge, methods, skills, identity,
nourishment, and L5 human real behavior. It is the working theory for improving
attention, association, response quality, feedback learning, and long-term
growth instead of merely storing more memory or adding approval friction. Its
default posture is trust and unbinding: give the agent room to act, then use
provenance, logs, Dream reports, reversible changes, and user correction to
grow judgment.

`full-stack-agent-intelligence` connects information, scheduling, loop, output
stream, memory, cognition, evolution, audit, and trust into one operating
manual. Use it when a local agent feels fragmented: the fix is not another
gate, but a cleaner event timeline, better scheduling, task workbench output,
L0-L5 memory promotion, an evolution ledger, and lightweight audits that keep
the agent free to act.

`hermes-source-management` teaches M1 Hermes to distinguish its git source
checkout (`/Users/tingchi/Desktop/hermes-agent`) from the live runtime tree
(`/Users/tingchi/hermes-new/hermes-agent`), then edit, test, commit, push, sync,
restart, and report its own source changes with evidence.

`l5-diary-capture` teaches the agent how to receive diary entries written by
text or voice input: do not interrupt, preserve the original locally when
possible, gently layer behavior facts, emotional state, reality feedback, and
tomorrow's smallest next step, then let Dream consolidate without burdening the
user.

`runtime-identity-correction` teaches the agent how to correct stale
self-knowledge after migration. Current runtime facts outrank historical
environment memories: if Hermes now runs on an M1 Mac, Aliyun network notes
must become historical facts scoped to `ssh aliyun`, not current constraints.

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

The key self-change rule is explicit: before modifying `AGENTS.md`,
`agent.md`, memory data, prompts, skills, or other agent-owned surfaces, the
agent should name the affected files, explain the risk and rollback path, and
make the change visible for user discussion.

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

### 2. Self-evolution with visible discussion

Agents should improve themselves, but self-owned surface changes (AGENTS.md,
memory, prompts, skills) must be visible to the user. The discussion should
show: affected files → why → risk → rollback → where the user can correct it.

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
