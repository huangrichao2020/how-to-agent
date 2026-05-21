---
name: agent-emergence-evaluation
description: Use when selecting post-triadic emergence candidates into skills, parameter experiments, practice loops, or runtime patterns.
---

# Agent Emergence Evaluation

Use this skill after triadic control exists:

```text
TriadicControlLayer
-> EmergenceEngine
-> EmergenceEvaluator
```

It does not create more hard rules. It turns repeated runtime traces into
verifiable, reversible promotion proposals.

## Runtime Plane

Emergence evaluation belongs to the offline evolution system. By default it
reads traces and logs outside the current task context. Only a short proposal
summary should feed the next PromptComposer: recommendation, evidence,
validation, and next step.

## Trigger

- The user discusses "ten thousand things", emergence, or what comes after triadic control.
- Runtime already records ThoughtStream, MindStability, and TriadicControl.
- Repeated traces need selection into a skill, parameter experiment, practice loop, or runtime route.
- The agent needs automatic correction from logs without mutating default policy directly.

## Formula

```text
Score(c) =
  confidence(c)
  + repeat_bonus(c)
  + type_bonus(c)
  + validation_bonus(c)
  - risk_penalty(c)
```

## Decisions

```text
promote_to_skill
propose_parameter_experiment
promote_to_practice_loop
promote_to_runtime_pattern
observe_more
hold
```

These are next actions, not hard stop labels.

## Workflow

1. Read `EmergenceCandidate`: type, count, confidence, pattern, mutation, validation, practice_loop.
2. Score the candidate: repeatability, validation, and reuse help; failure, side effects, credentials, production risk, and overwrite risk reduce score.
3. Write a proposal: decision, score, reason, target, validation, next_action.
4. Persist it under `memory/cognition/emergence/promotion-proposals.json`.
5. Emit `codex_runtime.emergence_proposal`.
6. Inject only the proposal hint into the next attention state; do not replace default behavior directly.
7. Promote only after fresh-task replay, eval, or user feedback supports it.

## Data Shape

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

## Boundaries

- A candidate is not yet an upgrade.
- One success is not proof of a new capability.
- Avoid hard-stop language.
- Do not expose internal `[EMERGENCE EVALUATION]` blocks directly to the user.
- Always believe in our agent: let it grow first, then select through trace, replay, and correction.

## Related Files

- `../../examples/29-agent-emergence-evaluation.md`: full method document.
- `../agent-attention-governance/`: attention governance layer.
- `../agent-final-architecture-outline/`: final architecture outline.
- `../agent-consciousness-math/`: consciousness math, log-to-data, and replay/eval.
