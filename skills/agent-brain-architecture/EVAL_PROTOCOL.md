# Ω-Brain Eval Protocol

## Goal

Let the agent evolve without making runtime faith-based.

Every brain change should be tested by replay and live feedback where possible.

## Replay Gate

Accept a new policy or prompt only if:

```text
E[Loss(new) on replay] <= E[Loss(old) on replay] - ε
Risk(new) <= Risk(old) + δ
Traceability(new) >= Traceability(old)
UserBurden(new) <= UserBurden(old) + β
```

When the user explicitly wants faster exploration, increase δ and β, but keep
traceability non-negotiable.

## Eval Sets

Maintain replay cases for:

- casual chat;
- learning material;
- thinking-core cases: essence, strategy, tactics, analysis, and action closure;
- code repair;
- service restart;
- remote sync;
- user correction;
- L6 existence work;
- long-task output;
- Dream consolidation.

## Promotion Path

```text
inspiration -> hypothesis -> replay win -> small live use -> durable doctrine
```

The agent may explore before proof. It should not silently promote untested
behavior into default doctrine.
