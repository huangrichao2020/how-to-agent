---
name: agent-architecture_Agent架构设计与记忆系统-auditor
description: Use when auditing an AI agent architecture, agent runtime, skill/memory/tool system, or self-improvement design. Produces an evidence-based architecture report with score, pass/partial/fail counts, risks, and optimization roadmap. Trigger phrases include architecture audit, agent capability check, self-check architecture ability, score my agent, optimize agent design, GA/Hermes architecture review, memory/skill/tool/runtime audit.
---

# Agent Architecture Auditor

Use this skill to make an AI agent inspect its own architecture instead of only
describing it. The audit must be evidence-based, scored, and action-oriented.

## Core Stance

An agent architecture is good only if it improves real behavior:

```text
clean context -> stable state -> correct action -> verified result -> durable learning
```

Do not reward terminology, ceremony, or self-narration. Reward verified loops,
clear boundaries, retrieval discipline, reliable tools, readable output, and
learning that changes future behavior.

## Required Reference

For a complete scoring rubric, read:

```text
references/architecture-audit-rubric.zh-CN.md
```

Load that reference before writing a formal audit report.

## Workflow

1. **Define scope.** Identify the target agent/repo/runtime, audit question,
   available evidence, and what would count as done.
2. **Collect evidence.** Inspect docs, entry points, runtime traces, tests,
   memory/skill indexes, tool contracts, output surfaces, and recent failures.
   Mark missing evidence instead of guessing.
3. **Map the architecture.** Summarize the main loop, context path, memory path,
   skill/tool path, output path, verification path, and learning path.
4. **Score the rubric.** Use the 12-dimension, 100-point rubric from the
   reference. Count pass, partial, and fail checklist items.
5. **Name contradictions.** Separate real defects from missing docs. Identify
   where the system claims a capability but the runtime evidence does not prove it.
6. **Prioritize fixes.** Use P0/P1/P2:
   - P0: blocks correctness, safety, verification, or durable learning.
   - P1: improves reliability, speed, retrieval, or maintainability.
   - P2: improves polish, ergonomics, or future evolution.
7. **Write the report.** Include score, maturity level, evidence table,
   satisfied/partial/unsatisfied counts, top risks, and a 24h/7d/30d roadmap.

## Output Contract

Formal reports should use this shape:

```markdown
# Agent Architecture Audit

## Verdict
- Score: X/100
- Maturity: ...
- Checklist: pass A / partial B / fail C
- Biggest risk: ...
- Best current strength: ...

## Evidence Map
| Surface | Evidence | What it proves | Gap |

## Scorecard
| Dimension | Weight | Score | Pass | Partial | Fail | Evidence | Priority |

## Findings
### P0
### P1
### P2

## Optimization Roadmap
### 24 hours
### 7 days
### 30 days

## Re-Audit Checklist
```

## Anti-Patterns

- Do not score from vibes when files, logs, or tests can be inspected.
- Do not make every architecture layer resident in the main prompt.
- Do not call a memory system complete if it stores but cannot retrieve.
- Do not call a skill system complete if skills are not discoverable,
  triggerable, and validated in real tasks.
- Do not call an output system complete if it exposes raw tool traces without
  human-readable action/result/conclusion.
- Do not create bureaucracy that slows ordinary tasks.

## Completion Standard

The audit is done when a future agent can read the report and know:

- what works now;
- what is missing or unproven;
- why the score was given;
- which fixes matter first;
- how to re-audit after changes.
