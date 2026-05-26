# Agent Architecture Auditor

This method turns the how-to-agent architecture canon into a reusable audit
skill. Its job is not to praise an agent's architecture, but to test whether
the architecture changes real behavior.

## Core Formula

```text
good agent architecture =
  clean task envelope
  + minimal effective context
  + stable runtime loop
  + reliable tools and skills
  + verifiable output
  + durable learning
```

## What It Audits

- Task envelope, boundaries, and acceptance criteria.
- Context pack and anti-bloat discipline.
- Attention governance: PromptComposer, RuntimeController, FeedbackLoop.
- Brain loop: perception, attention, memory, simulation, decision, action,
  feedback, consolidation.
- Thinking core: essence, strategy, tactics, learning, action.
- Memory store/retrieve/writeback loop.
- Skill, tool, and MCP architecture.
- Execution, verification, rollback, and reporting.
- Output workbench and human-readable progress.
- Eval, replay, audit, evolution, safety, trust, and humanistic quality.

## Report Shape

The auditor produces:

- score out of 100;
- maturity level;
- pass / partial / fail count;
- evidence map;
- scorecard;
- P0/P1/P2 findings;
- 24h/7d/30d optimization roadmap;
- re-audit checklist.

## Design Note

The strongest audit is not a longer checklist. It is a sharper mirror: it shows
where the agent's claimed architecture is not yet proven by runtime evidence,
then points to the smallest upgrade that would make the next task better.
