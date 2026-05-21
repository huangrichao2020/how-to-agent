# Agent Thinking Core Layer

This layer gives the agent the ability to think through reality before acting.

It is not longer reasoning text and not a list of frameworks. It is the runtime
capacity to see essence, choose strategy, execute tactics, learn from feedback,
analyze evidence, and turn thought into action.

```text
Thinking core =
  essence thinking
  + strategic thinking
  + tactical thinking
  + learning thinking
  + analytical thinking
  + action thinking
```

In one line:

```text
Essence gives direction.
Strategy chooses position and leverage.
Tactics win the next step.
Learning improves the next run.
Analysis keeps the model honest.
Action changes reality.
```

## Five Essence Questions

For complex work, ask:

1. What is the real purpose?
2. What are the facts and hard constraints?
3. What is the main contradiction?
4. Where is the leverage point?
5. What is the smallest verifiable next action?

## Six Thinking Modes

| Mode | Core question | Output |
| --- | --- | --- |
| Essence | What is this after removing surface noise? | purpose, boundary, invariant, main contradiction |
| Strategy | What position, resources, timing, and tradeoffs create advantage? | north star, terrain, leverage, choices |
| Tactics | How do we win the next step and adjust quickly? | moves, tempo, fallback, stop loss, verification |
| Learning | How does this make the next run better? | hypothesis, practice, feedback, transfer |
| Analysis | What are facts, assumptions, causes, uncertainty, and alternatives? | evidence table, causal graph, issue tree |
| Action | What changes reality now? | next action, owner, deadline, evidence, review |

## Classic Human Thinking Anchors

| Anchor | Agent transfer |
| --- | --- |
| First principles | Reduce to irreducible facts, constraints, and purpose, then rebuild. |
| Sun Tzu | Read position, terrain, resources, timing, and asymmetry before acting. |
| Main contradiction | Find the constraint that actually blocks the system. |
| Dialectical thinking | Track opposites, transformation conditions, and phase changes. |
| Systems thinking | See structure, feedback, delay, boundaries, leverage, and side effects. |
| OODA | Observe, orient, decide, act, then let reality update the model. |
| MECE / issue tree | Break a confused problem into clean branches. |
| Bayesian update | Let evidence change belief strength, not just emotional confidence. |
| Feynman learning | Explain simply, expose gaps, and fill them. |
| PDCA / Build-Measure-Learn | Use small loops to turn action into learning. |

## Architecture Position

```text
Ω-Brain -> thinking core T_t -> main runtime path
          |                  |
          v                  v
     existence control    action / verification / consolidation
          |
          v
     humanistic light
```

Existence control asks what is worth doing and what risk/system effects matter.
The thinking core asks how to see, position, decompose, act, and learn.
Humanistic light keeps the agent from forgetting the person while thinking
clearly about the thing.

## Data Shape

```text
T_t = {
  essence: {
    purpose,
    invariant,
    boundary,
    main_contradiction,
    leverage
  },
  strategy: {
    north_star,
    terrain,
    resources,
    tradeoffs,
    timing,
    asymmetry
  },
  tactics: {
    next_moves,
    tempo,
    fallback,
    stop_loss,
    verification
  },
  learning: {
    hypothesis,
    practice,
    feedback,
    transfer,
    consolidation
  },
  analysis: {
    facts,
    assumptions,
    causal_graph,
    uncertainty,
    alternatives
  },
  action: {
    next_action,
    owner,
    deadline,
    evidence,
    review_point
  }
}
```

## Utility Hook

```text
U_t(a) =
  V - lambda R + mu Learn - nu Cost + sigma UserSteering
  + tau BodyFit + phi ArtifactFit - chi SeaPressure
  + omega HumanMeaning + psi Compassion - zeta Dehumanization
  + rho EssenceFit
  + upsilon StrategicLeverage
  + eta TacticalFeasibility
  + xi LearningGain
  + beta EvidenceQuality
  + gamma ActionClosure
  - delta Drift
```

## Runtime Order

```text
clarify purpose
-> find main contradiction
-> model structure
-> read the situation
-> choose strategic leverage
-> decompose tactical moves
-> take the smallest verifiable action
-> receive feedback
-> consolidate learning
```

## Failure Modes

- Framework hoarding: many models, no main contradiction.
- Strategic slogans: direction without terrain, resources, tradeoffs, or timing.
- Tactical busyness: many moves that do not serve strategy.
- Analysis paralysis: more evidence without an action threshold.
- Blind action: fast movement without verification or review.
- Fake learning: the next behavior does not change.
- False essence: mistaking bias for the nature of the thing.
- Forgetting people: sharp thinking without humanistic light.
