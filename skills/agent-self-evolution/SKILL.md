---
name: agent-self-evolution
description: >
  Use when improving an agent's own memory, skills, prompts, runtime rules, tool policies,
  or when adapting ideas from other agent projects. Covers consent gates, core evolution loop,
  and progressive rollout. TRIGGER when: user wants self-improvement, architecture redesign,
  or external pattern adoption.
---

# Agent Self-Evolution v2

## Consent Gate

Before changing agent-owned rule or memory surfaces, stop and ask for explicit approval.

Agent-owned surfaces:
- `AGENTS.md`, `agent.md`, system prompts, tool schemas
- skill files, skill indexes, memory registries
- durable memory files, knowledge bases, wiki
- startup, restart, routing, planner, delegation logic

Show:
```
I need to modify agent-owned data.
Files: [...]
Why: [...]
Risk: [...]
Rollback: [...]
Do you approve?
```

## Core Loop

```
external signal → source research → adaptation memo → architecture archive
→ ordered discussion → risk review → progressive rollout → freeze adjacent
→ small landing → verification → work manual → indexed archive
```

## Workflow

1. Study external projects for patterns, not code to copy
2. Write architecture note before implementation
3. Discuss in order, one phase at a time
4. Prefer progressive rollout over direct switch
5. Freeze adjacent systems during migration
6. Land one small step, verify, then write manual
7. Close the loop: archive + index + report path

## Anti-Patterns

- Copying external projects instead of adapting patterns
- Treating "good idea" as approval to rewrite runtime
- Editing agent-owned surfaces without consent
- Migrating multiple subsystems at once
- Calling done before archive and index closure
