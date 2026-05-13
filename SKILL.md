---
name: how-to-use-agent-v2
description: >
  Guide for evolving an agent through conversation. Covers source-level learning,
  architecture-first design, progressive rollout, consent gates, and durable archival.
  TRIGGER when: user wants the agent to learn from external projects, self-evolve,
  redesign architecture, or establish a repeatable improvement process.
  DO NOT TRIGGER when: user wants a simple code fix, feature addition, or bug report.
version: 2.0.0
author: huangrichao2020 (adapted from how-to-use-agent + Hermes architecture)
---

# How to Use Agent v2

## Core Loop

```
external signal
  → source-level research (adaptation memo)
  → architecture archive (gbrain page or wiki)
  → ordered discussion
  → risk / reward review
  → progressive rollout
  → freeze adjacent systems
  → first small landing
  → verification
  → work manual
  → indexed archive path
```

## Step 1: Source Learning

Study external projects for patterns, not code to copy.

Return an **adaptation memo**:
- what problem the external project solves
- which design patterns are useful here
- which parts are too heavy or incompatible
- the smallest safe local experiment
- files or modules likely affected

```text
Good output shape:
Pattern: [what the other project does well]
Why it matters here: [current weakness]
Adaptation: [smaller local version]
Do not copy: [heavy dependency, wrong abstraction]
First experiment: [one small change or design doc]
```

## Step 2: Architecture Before Code

If the change touches memory, tools, prompts, runtime, startup, or delegation:

1. Write an **architecture note** before implementation:
   - current problem
   - target behavior
   - migration phases
   - risks and rollback
   - what must stay unchanged
   - acceptance checks

2. Store it as a durable artifact (gbrain page, wiki, or file under `queries/`).

## Step 3: Discuss in Order

Do not implement everything at once. Walk through the plan one phase at a time.

Use direct language:
- "This is phase one."
- "This part should wait."
- "This needs user approval because it changes agent-owned data."

## Step 4: Prefer Progressive Rollout

For risky agent changes, compare:
- direct full switch
- shadow mode / parallel run
- progressive rollout

Prefer progressive rollout when old and new behavior can coexist.

## Step 5: Freeze Adjacent Systems

During a migration, pause unrelated work on neighboring systems.
**Focus is a safety mechanism.**

## Step 6: Land One Small Step

- reuse existing logic when possible
- keep integration points small
- preserve existing data unless deletion is approved
- add cheap verification
- keep rollback obvious
- avoid broad refactors

## Consent Gate

**Before modifying agent-owned surfaces, stop and ask for explicit approval.**

Agent-owned surfaces include:
- `AGENTS.md`, `agent.md`, `CLAUDE.md`, system prompts
- tool schemas, permission policies, connector policies
- skill files, skill indexes, memory registries
- durable memory files, knowledge bases, wiki
- startup, restart, routing, planner, delegation logic

When approval is needed, show:
```
I need to modify agent-owned data.

Files/surfaces:
- ...

Why:
- ...

Risk:
- ...

Rollback:
- ...

Do you approve?
```

Do not treat "continue" as consent. Do not delete memory without naming what is lost.

## Step 7: Write the Work Manual

After landing a phase, write a short manual next to the architecture note:
- what changed
- why it changed
- how to verify it
- what remains paused
- what phase two should do
- exact file paths and commands for the next agent

## Step 8: Close the Loop

The task is not done when files are edited. It is done when the next agent can find and reuse the result.

**Closure checklist:**
- [ ] architecture note exists
- [ ] work manual exists
- [ ] indexes/manifests updated
- [ ] verification evidence recorded
- [ ] archive path reported to user

## Failure Escalation

Never retry blindly:
1. **1st failure**: Read the error output. Understand why.
2. **2nd failure**: Probe environment (processes, files, permissions, network).
3. **3rd failure**: Deep analysis → switch strategy or ask user.

## Anti-Patterns

- Do not copy external projects — adapt patterns
- Do not treat "good idea" as approval to rewrite runtime
- Do not edit agent-owned surfaces without consent
- Do not migrate multiple subsystems at once
- Do not call it done before archive and index closure
- Do not let completed work live only in chat history
