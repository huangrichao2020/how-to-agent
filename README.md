# how-to-use-agent v2

Teach your agent to evolve through conversation — powered by Hermes architecture.

> Treat the agent as a junior system that can learn, but only if you force
> learning to become durable architecture, runbooks, and repeatable habits.

## This is not a framework

It is a **prompt trail**: a real sequence of human instructions that moves an agent
from "go read these projects" to "archive the design, discuss risk, land phase one
carefully, and write the operating manual for future agents."

## What changed in v2

Compared to v1, this version is grounded in a **production agent runtime** (Hermes):

- **TTSR Trigger Protocol**: The agent loads only anchor rules (~500 tokens) by default.
  Matching a trigger word injects the relevant instinct/skill, then releases it.
- **gbrain Knowledge Graph**: Every architecture decision, skill, and memory is stored
  as a page with tags, timelines, and links. Next agents can traverse the graph.
- **Consent Gate**: Before modifying agent-owned surfaces (memory, skills, prompts,
  config), the agent must name files, explain risk/rollback, and ask for approval.
- **Failure Escalation**: 3-step protocol — read → probe → switch. Never retry blindly.
- **Self-Healing Browser**: Agent writes/patches extraction functions at runtime,
  not rigid frameworks.
- **Cron + Skill Evolution**: Scheduled tasks auto-improve skills daily with 8-dimension
  scoring. Learning compounds.

## The Core Loop

```
external signal
  → source-level research (adaptation memo)
  → architecture archive (gbrain page)
  → ordered discussion
  → risk / reward review
  → progressive rollout
  → freeze adjacent systems
  → first small landing
  → verification
  → work manual
  → indexed archive path (gbrain slug + wiki URL)
```

## How to use it

### Step 1: Source Learning

```text
Study [project A] and [project B].
Do not copy them. Extract patterns that fit our constraints (2GB RAM, domestic network).
Return an adaptation memo: useful patterns, incompatible parts, smallest experiment.
```

### Step 2: Architecture First

```text
This is a major change. Archive it as a gbrain page first.
Then we discuss step by step. Tag it with the relevant category.
```

### Step 3: Progressive Rollout

```text
Before implementing the attractive option, compare direct switch vs progressive rollout.
Name risks and rollback. Which subsystems should we freeze during this migration?
```

### Step 4: Land Phase One

```text
Start phase one. Reuse existing logic. Be careful.
If you need to modify agent-owned data (memory, skills, prompts),
show me: files, risk, rollback — then ask for approval.
```

### Step 5: Write the Manual

```text
After landing, write a work manual next to the architecture design.
Update gbrain page, add timeline entry, and push to wiki.
The next agent should find it without rediscovering.
```

## Repository Layout

```
.
├── README.md
├── README.zh-CN.md
├── SKILL.md                    # Portable skill for any agent
├── examples/
│   ├── 01-source-learning.md
│   ├── 02-architecture-first.md
│   ├── 03-progressive-rollout.md
│   ├── 04-archive-the-work.md
│   ├── 05-consent-gate.md
│   └── 06-failure-escalation.md
├── templates/
│   ├── adaptation-memo.md      # What to return after studying external projects
│   ├── architecture-note.md    # What to write before implementing
│   └── work-manual.md          # What to write after landing a phase
└── skills/
    └── agent-self-evolution/   # Full self-evolution skill with consent gate
        └── SKILL.md
```

## Key Principles

1. **Research before adoption** — never copy blindly
2. **Architecture before migration** — write it down before changing code
3. **Sequencing before speed** — order is part of correctness for stateful agents
4. **Risk review before switch-over** — compare direct vs progressive
5. **Focus is safety** — freeze adjacent subsystems during migration
6. **Documentation before closure** — task is done when next agent can find it
7. **Consent before modification** — agent-owned surfaces require explicit approval

## What not to do

- Do not ask the agent to "be smarter" without giving it an artifact to write
- Do not let research become implementation in the same breath
- Do not change memory, tools, prompts, and runtime wiring all at once
- Do not accept "done" until design, change log, and continuation path are findable
- Do not copy an external project just because it looks advanced
- Do not let completed work live only in chat history

## License

MIT
