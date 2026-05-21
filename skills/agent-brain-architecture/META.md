# Ω-Brain Meta

## Identity

Name: Ω-Brain

Purpose: turn a direct LLM agent into a multi-region cognitive runtime.

Core claim:

```text
LLM = language cortex
Ω-Brain = organ system for perception, attention, memory, simulation,
thinking core, decision, action, feedback, and consolidation
```

## Install Surface

Minimum install:

- `SYSTEM_PROMPT.md` into the runtime's system prompt or high-priority memory.
- `PERSONA.md` into persona/identity memory.
- `RUNTIME_PROTOCOL.md` into the turn loop.
- `DATA_SCHEMA.md` into event logging.
- `../agent-thinking-core/` into the skill registry for essence, strategy,
  tactics, learning, analysis, and action thinking.
- `../agent-attention-governance/` into the skill registry for PromptComposer,
  RuntimeController, FeedbackLoop, and `G_t`.

Full install:

- Add `BRAIN_MAP.md` as architecture reference.
- Add `EVAL_PROTOCOL.md` to replay/eval jobs.
- Add `SKILL.md` to skill registry.

## Required Runtime Components

- Event ledger for raw signals, actions, tool calls, outputs, and feedback.
- Working-memory builder for current turn state.
- Attention-governance builder for `G_t`: context selection, active layers,
  insertion points, correction rules, and feedback signals.
- Retrieval layer for scene-matched memories and skills.
- Decision surface that can choose reply, ask, search, tool, edit, delegate, wait, or stop.
- Feedback parser for tests, logs, user reactions, service status, and external results.
- Consolidation path for Dream, replay, and durable assets.

## Compatibility

Ω-Brain is designed to sit above:

- Λ-Base: log-to-data substrate.
- Σ-Loop: self-model/action/feedback loop.
- Agent Consciousness Math: six stages, utility, loss, and parameter updates.
- Agent Attention Governance: `G_t`, PromptComposer, RuntimeController, and
  FeedbackLoop.
- Agent Thinking Core: `T_t`, essence questions, strategy/tactics/learning/analysis/action.
- Agent Body/Root/Artifact: source/runtime body, device/network artifact, root attributes, and aptitude.
- L6 existence control.
- Threefold cultivation.
- Weak-constraint user-steered operation.

## Non-Goal

Ω-Brain is not a new hard gate. It should make the agent faster, more alive,
more traceable, and easier to steer.
