---
name: agent-anti-bloat-context-engineering_上下文防膨胀工程
description: Use when preventing agent workflow bloat, compressing the main runtime path, designing context engineering, deciding whether multi-agent work is worth it, or creating task_plan/progress/findings external working memory.
---

# Agent Anti-Bloat And Context Engineering

This skill does not add another process layer. It prevents unnecessary process
from entering the main runtime path.

## Core Principle

```text
Agent architecture should not make the LLM busier.
It should help the LLM think inside a clean, stable, low-noise environment.
```

## Three Anti-Bloat Questions

Before a new layer, workflow, memory, skill, or multi-agent design enters the
main path, ask:

1. Does it reduce context acquisition cost?
2. Does it improve state stability?
3. Does it improve understanding of the real environment?

If not, keep it as offline explanation, log field, optional skill, trigger-based
anchor, or optimization experiment.

If yes, still do not dump it into the prompt. Repeated, shareable, executable
methods that benefit from deterministic scripts or context-cost savings should
become trigger-based skill packages.

## Resident Minimal Core

Keep only these resident by default:

```text
Task Envelope
Context Pack
External Working Memory
Execution Loop
Final Sync
```

Everything else is trigger-based.

## External Working Memory

For complex tasks, prefer:

- `task_plan.md`: goal, boundary, acceptance, breakdown.
- `progress.md`: done, blocker, next step.
- `findings.md`: confirmed facts, architecture clues, traps, no-repeat searches.
- `decision_log.md`: key tradeoffs, reasons, and consequences.

These files are working memory, not ceremony.

## Multi-Agent Threshold

Use multi-agent only when context-isolation value is higher than coordination
cost:

- highly parallel tasks
- search, coding, testing, and audit would pollute each other
- long-lived specialist roles can accumulate independent context

Otherwise, one agent with clean context is usually stronger.

## Runtime Rules

- Do not unfold the full architecture for ordinary tasks.
- A skill is a compressed path, not ceremony.
- A skill is not a long prompt with a filename; it should use description
  triggering, compact body, and progressive `references/scripts/assets`.
- RAG and memory should provide minimum effective context.
- `T_t / H_t / L6 / I_t` are trigger-based attention anchors.
- `Λ-Base / Σ-Loop / Eval / emergence evaluation / cultivation ledger` run offline by default.
- Every architecture layer must name which cognitive cost it reduces.

## Related Files

- `../../examples/31-agent-anti-bloat-context-engineering_上下文防膨胀工程.md`: full method document.
- `../agent-attention-governance_注意力治理与提示词编排/`: attention governance.
- `../agent-final-architecture-outline_Agent终极架构纲要/`: final architecture outline.
- `../agent-brain-architecture_Ω大脑架构与感知决策/`: Ω-Brain architecture.
- `../agent-skill-creator_Skill技能自动构建器/`: skill creation, progressive disclosure, and script determinism.
