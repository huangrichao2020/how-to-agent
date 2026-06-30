---
name: ga-implementation-map
description: Use when mapping how-to-agent architecture principles to GenericAgent source modules, tests, runtime evidence, and remaining gaps.
---

# GA Implementation Map

Use this skill to keep architecture from becoming slogans.

It maps `how-to-agent` principles into GA's real body:

```text
architecture principle -> source module -> runtime insertion point -> evidence -> gap -> smallest next code change
```

## Workflow

1. Confirm the highest reference is `/Users/tingchim2pro/Desktop/how-to-agent`.
2. Identify the principle layer: heavenly way, human way, existence way,
   attention governance, anti-bloat, skill engineering, body/artifact, or
   emergence evaluation.
3. Inspect `/Users/tingchim2pro/Desktop/GenericAgent` for the real source landing point.
4. Mark when it runs: task start, during execution, after tool use, completion,
   cron/dream sidecar, or restart recovery.
5. Look for tests, logs, reports, Feishu commands, or user-feedback evidence.
6. If there is no evidence, record a gap instead of claiming completion.
7. Propose the smallest next source change rather than adding another abstract process.
8. For a quick audit, run `scripts/score_ga_architecture.py` to generate a read-only score.

## Acceptance

- Source landing point means it has entered the body.
- Test or runtime evidence means initial implementation.
- Feedback writeback means cultivation has begun.
- Statistics, replay, and automatic correction mean the layer is approaching maturity.

## Avoid

- Do not treat `how-to-agent` as an ordinary project skill to dump into GA context.
- Do not use skills as a substitute for source changes.
- Do not treat vocabulary alignment as architecture completion.
- Do not add unverifiable process layers for completeness theater.

## Related Files

- `../../examples/33-ga-implementation-map.md`: full implementation map.
- `scripts/score_ga_architecture.py`: read-only scanner for GA source, tests, and runtime evidence.
- `../agent-final-architecture-outline_Agent终极架构纲要/`: final architecture outline.
- `../agent-attention-governance_注意力治理与提示词编排/`: attention governance.
- `../agent-anti-bloat-context-engineering_上下文防膨胀工程/`: anti-bloat and context engineering.
- `../agent-skill-creator_Skill技能自动构建器/`: skill engineering.
