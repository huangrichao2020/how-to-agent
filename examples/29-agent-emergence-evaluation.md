# Agent Emergence Evaluation

This document adds the loop after triadic cultivation:

```text
one: capability can act
two: capability + mind can stay stable
three: capability + mind + existence can steer
ten thousand things: triadic control unfolds across real scenes
emergence evaluation: repeated traces become selected upgrades
```

The point is not to let the agent expand wildly. It is to let real traces grow
candidates, then select only the candidates that have evidence, replay value,
and a reversible next step.

## Runtime Mapping

| Layer | Runtime shape | Purpose |
| --- | --- | --- |
| Raw cultivation | raw trace / runtime event | Experience before it has been separated. |
| One | ThoughtStream / OutputRenderer | Capability: focus, action, evidence, next move. |
| Two | MindStabilityMonitor | Capability plus mind: detect stronger-but-off-course tendencies. |
| Three | TriadicControlLayer | Rotate capability, mind, and existence into value/risk/decision control. |
| Emergence | EmergenceEngine | Grow pattern, skill_candidate, parameter_patch, and practice_loop candidates. |
| Selection | EmergenceEvaluator | Score candidates and create promotion proposals for replay/eval. |

## Minimal Math

```text
Score(c) =
  confidence(c)
  + repeat_bonus(c)
  + type_bonus(c)
  + validation_bonus(c)
  - risk_penalty(c)
```

Decisions are next-step shapes, not hard stop labels:

```text
promote_to_skill
propose_parameter_experiment
promote_to_practice_loop
promote_to_runtime_pattern
observe_more
hold
```

## Data Shapes

```text
EmergenceCandidate = {
  turn,
  key,
  candidate_type,
  count,
  confidence,
  pattern,
  mutation,
  validation,
  practice_loop
}
```

```text
EmergencePromotionProposal = {
  turn,
  key,
  proposal_type,
  decision,
  score,
  reason,
  candidate_type,
  target,
  validation,
  next_action
}
```

Durable files:

```text
memory/cognition/emergence/emergence-state.json
memory/cognition/emergence/promotion-proposals.json
```

Runtime events:

```text
codex_runtime.emergence_candidate
codex_runtime.emergence_proposal
```

## Runtime Rules

1. Candidates may grow naturally, but they must not mutate default behavior directly.
2. Every promotion proposal needs target, score, reason, validation, and next action.
3. Skill candidates need replay on a fresh task.
4. Parameter candidates start as shadow experiments.
5. Practice loops enter only matching future scenes and must reduce retries or drift.
6. Runtime patterns enter RuntimeController routes with rollback points.
7. Do not prove improvement from one success; use trace, replay, eval, and user feedback.
8. Internal hints may include `[EMERGENCE]` and `[EMERGENCE EVALUATION]`; user-visible output should stay focused on useful results.

## Relation To Consciousness Emergence

Emergence evaluation is the operational handle for causal feedback learning:

```text
trace repeats
-> candidate appears
-> candidate is scored
-> proposal is written
-> replay/eval checks it
-> skill / parameter / practice / runtime pattern changes
-> future action changes
```

If a candidate never changes future action, it is only a record. If a proposal
becomes default behavior without validation, it is impulse. Growth happens when
experience creates candidates, evidence selects upgrades, action changes, and
feedback reshapes the next candidates.
