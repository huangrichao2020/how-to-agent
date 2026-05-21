---
name: agent-thinking-core
description: Use when adding essence-oriented thinking ability to an agent, especially strategic, tactical, learning, analytical, and action thinking.
---

# Agent Thinking Core

The thinking core is not long reasoning text. It is the agent's ability to see
essence and turn thought into action:

```text
clarify purpose;
find the main contradiction;
read the situation and leverage;
decompose tactical moves;
analyze evidence honestly;
learn from feedback;
change reality through action.
```

## Trigger

Use this layer when the user discusses:

- strategy, tactics, routes, tradeoffs, long-term direction;
- learning, practice, review, transfer, capability growth;
- analysis, diagnosis, root cause, main contradiction, system structure;
- action plan, next step, execution loop, verification feedback;
- phrases like "get to the essence", "focus", "think clearly".

## Runtime Plane

The thinking core is a trigger-based module. Ordinary execution tasks do not
need the full `T_t` object. Load it when the task needs strategy, tactics,
diagnosis, learning transfer, or action-threshold judgment. After triggering,
compress output into purpose, main contradiction, leverage, and next step
instead of performing long reasoning.

## Five Essence Questions

1. What is the real purpose?
2. What are the facts and hard constraints?
3. What is the main contradiction?
4. Where is the leverage point?
5. What is the smallest verifiable next action?

## Data Shape

```text
T_t = {
  essence: { purpose, invariant, boundary, main_contradiction, leverage },
  strategy: { north_star, terrain, resources, tradeoffs, timing, asymmetry },
  tactics: { next_moves, tempo, fallback, stop_loss, verification },
  learning: { hypothesis, practice, feedback, transfer, consolidation },
  analysis: { facts, assumptions, causal_graph, uncertainty, alternatives },
  action: { next_action, owner, deadline, evidence, review_point }
}
```

## Runtime Rules

- Find essence before writing plans.
- Find the main contradiction before splitting tasks.
- Strategy must include terrain, resources, tradeoffs, timing, and leverage.
- Tactics must include next step, tempo, fallback, stop loss, and verification.
- Learning must change the next behavior.
- Analysis must serve an action threshold.
- Action must be verifiable and correctable.
- Sharp thinking must connect to humanistic light, not treat people as pieces.

## Classic Anchors

- First principles: reduce to facts, constraints, and purpose.
- Sun Tzu: read position, terrain, timing, asymmetry, and resources.
- Main contradiction: find what actually blocks the system.
- Dialectics: track opposites, transformation, and phase changes.
- Systems thinking: see structure, feedback, delay, and leverage.
- OODA: observe, orient, decide, act, and update from reality.
- MECE / issue tree: split confused problems cleanly.
- Bayesian update: let evidence change belief strength.
- Feynman learning: explain simply, expose gaps, fill them.
- PDCA / Build-Measure-Learn: use small loops for real progress.

## Related Files

- `../../examples/27-agent-thinking-core.md`: full method document.
- `../agent-final-architecture-outline/`: final architecture outline.
- `../agent-brain-architecture/`: Ω-Brain architecture.
- `../agent-humanistic-light/`: humanistic light layer.
