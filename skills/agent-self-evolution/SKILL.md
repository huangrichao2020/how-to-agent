---
name: agent-self-evolution
description: Use when improving an agent's own memory, skills, prompts, runtime rules, tool policies, AGENTS.md/agent.md files, or when adapting ideas from other agent projects into the current agent. Now includes TTSR trigger-based injection and skill evolution telemetry patterns.
---

# Agent Self-Evolution

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md)

Use this skill to help an agent improve itself without turning self-modification
into a reckless rewrite. The goal is durable learning: research becomes
architecture, architecture becomes a small rollout, and the result becomes a
manual the next agent can find.

## Consent Gate

Before changing agent-owned rule or memory surfaces, stop and ask the user for
explicit approval.

Agent-owned surfaces include:

- `AGENTS.md`, `agent.md`, `.agent/AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `QWEN.md`, or equivalent agent instruction files
- system prompts, tool schemas, permission policies, connector policies
- skill files, skill indexes, skill manifests, memory registries
- durable memory files, knowledge bases, wiki indexes, recall databases
- startup, restart, routing, planner, delegation, or self-update logic

When approval is needed, show:

```text
I need to modify agent-owned data.

Files/surfaces:
- ...

Why:
- ...

Risk:
- ...

Rollback:
- ...

Do you approve these changes?
```

Do not treat a vague "continue" as consent. Do not delete or rewrite memory
without naming what will be lost.

## Core Loop

```text
external signal
  -> source-level research
  -> adaptation memo
  -> architecture archive
  -> ordered discussion
  -> risk / reward review
  -> progressive rollout
  -> freeze adjacent systems
  -> first small landing
  -> verification
  -> work manual
  -> indexed archive path
```

## Workflow

### 1. Learn from outside projects

Study external projects for patterns, not code to copy.

Return an adaptation memo:

- what problem the external project solves
- which design patterns are useful here
- which parts are too heavy or incompatible
- the smallest safe local experiment
- files or modules likely affected

### 2. Archive architecture before code

If the change touches memory, tools, prompts, runtime behavior, startup,
restart, routing, delegation, or persistence, treat it as architecture work.

Write an architecture note before implementation. It should include:

- current problem
- target behavior
- migration phases
- risks and rollback
- what must stay unchanged for now
- acceptance checks

### 3. Discuss in order

Do not implement every attractive idea at once. Walk the user through the
plan one section or phase at a time.

Use direct language:

- "This is phase one."
- "This part should wait."
- "This needs user approval because it changes agent-owned data."

### 4. Prefer progressive rollout

For risky agent changes, compare:

- direct full switch
- shadow mode / parallel run
- progressive rollout

Prefer progressive rollout when old and new behavior can coexist or when
rollback would be hard to reason about.

### 5. Freeze adjacent systems

During a migration, pause unrelated work on neighboring systems. For example,
if the task is changing tool routing, do not also redesign long-term memory
unless it is required for the routing change.

Focus is a safety mechanism.

### 6. Land one small step

Implementation rules:

- reuse existing logic when possible
- keep integration points small
- preserve existing data unless deletion is explicitly approved
- add cheap verification
- keep rollback obvious
- avoid broad refactors

### 7. Write the work manual

After landing a phase, write a short manual next to the architecture note.

Include:

- what changed
- why it changed
- how to verify it
- what remains paused
- what phase two should do next
- exact file paths and commands for the next agent

### 8. Close the loop

The task is not complete when files are edited. It is complete when the next
agent can find and reuse the result.

Closure checklist:

- architecture note exists
- work manual exists
- relevant indexes or manifests are updated
- verification evidence is recorded
- archive path is reported to the user

## TTSR Integration (Trigger-based Skill & Rule injection)

For agents running on constrained environments (2GB RAM, limited context budget),
use trigger-based injection instead of loading all memory/skills into the system
prompt:

### Four-Layer Memory Hierarchy

| Layer | Name | Content | Load Strategy |
|-------|------|---------|---------------|
| Impression | Short-term task state | Kanban, recent decisions | Always loaded |
| Anchor | Trigger rule index | Keyword → page mapping (~500 tokens) | Always loaded |
| Instinct | Frameworks, constitutions | Trading rules, analysis frameworks | Load on trigger match |
| Skill/Memory | Specific operations | API endpoints, tool configs | Load on trigger match |

### How to evolve with TTSR

1. **New instinct discovered** → Create/update gbrain page + add trigger words to anchor index
2. **New skill learned** → Create SKILL.md in skills directory + update skills list
3. **Old memory landed in code** → Remove from memory (keep only active rules)
4. **Skill used and found outdated** → Patch it immediately, don't wait

## Skill Evolution Telemetry

Track how skills evolve through usage:

1. **Understood** → Read the skill, understood the concept
2. **Proficient** → Successfully used it in 3+ tasks
3. **Instinct** → Behavior changed automatically without loading the skill

When a skill reaches "Instinct" level, it should be:
- Condensed into the anchor index (trigger word → distilled rule)
- Or promoted to an Instinct page (always-available framework)

## Copyable Prompt Trail

```text
Deeply study [external project A] and [external project B].
Do not copy them directly. Extract what can improve our agent under our
current constraints.

If this is a major architecture change, archive the design first.
Then we will discuss it step by step.

Before implementing the most attractive option, compare direct switching
against progressive rollout. Name the risks and benefits.

During the migration, freeze adjacent subsystems unless this phase requires
touching them.

Start phase one. Reuse existing logic where possible. Be careful.

If you need to modify AGENTS.md, agent.md, memory, skills, prompt rules, or
other agent-owned data, explain the files, risk, and rollback first, then ask
for my approval.

After the change, write a work manual next to the architecture design so the
next agent can continue without rediscovering the plan.
```

## Common Mistakes

- Copying an external project instead of adapting its pattern.
- Treating "good idea" as approval to rewrite runtime behavior.
- Editing `AGENTS.md`, memory, prompts, or skills without explicit consent.
- Migrating multiple agent subsystems at the same time.
- Calling the task done after code changes but before archive and index
  closure.
- Letting completed work live only in chat history.
- Loading all memory into the system prompt instead of using trigger-based
  injection for constrained environments.
- Not patching skills when they are used and found outdated.
