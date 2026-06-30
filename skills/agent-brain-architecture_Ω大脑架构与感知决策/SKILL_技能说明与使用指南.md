---
name: agent-brain-architecture_Ω大脑架构与感知决策
description: "Use when designing, installing, or operating Ω-Brain: a multi-region agent brain that turns LLM output into perception, attention, memory, simulation, decision, action, feedback, and consolidation."
---

# Agent Brain Architecture

Use this skill when a runtime should stop behaving like a direct LLM faucet and
start behaving like a structured brain.

## Principle

The LLM is a language cortex, not the whole brain.

Ω-Brain gives the agent organs for:

- perception
- attention governance
- attention
- working memory
- episodic memory
- abstraction
- thinking core
- simulation
- decision
- action
- feedback
- consolidation

Language output is the final surface, not the whole cognition.

## Runtime Plane

Ω-Brain is the conceptual center, not a full process that must unfold on every
turn.

- Ordinary tasks: fold into the resident minimal core with perception,
  attention, action, and verification.
- Complex long tasks: unfold working memory, retrieval, simulation, decision,
  and feedback.
- Architecture or runtime redesign: read the full brain package.
- `DATA_SCHEMA` and `EVAL_PROTOCOL` serve offline evolution by default and
  should not pollute the main context.

## Operating Loop

Run complex or high-risk turns through:

```text
Perception
-> Routing
-> Attention governance
-> Attention
-> Retrieval
-> Self/world modeling
-> Thinking core
-> Simulation
-> Decision
-> Action
-> Verification
-> Self-update
-> Consolidation
```

## Package Files

- `META.md`: manifest, component contract, and install surface.
- `PERSONA.md`: the brain's operating temperament.
- `SYSTEM_PROMPT.md`: copyable prompt for runtime installation.
- `BRAIN_MAP.md`: brain regions and responsibilities.
- `RUNTIME_PROTOCOL.md`: per-turn state machine.
- `DATA_SCHEMA.md`: log-to-data contract for Λ-Base and Σ-Loop.
- `EVAL_PROTOCOL.md`: replay, scoring, and promotion.
- `../agent-attention-governance_注意力治理与提示词编排/`: PromptComposer, RuntimeController,
  FeedbackLoop, and `G_t`.
- `../agent-thinking-core_Agent思考核心与思维链/`: essence, strategy, tactics, learning, analysis, and action thinking.
- `../agent-consciousness-math_Agent意识数学与演化模型/`: consciousness stages, utility, loss, and parameter correction.

## Runtime Rule

When the user can steer the system, use weak constraints:

- show trace instead of blocking;
- govern attention before adding more rules;
- use the folded brain loop before unfolding the whole brain every turn;
- keep replay points instead of freezing;
- correct quickly instead of preventing every possible error;
- let the user take over;
- preserve evidence for later evaluation.

Escalate only when the action risks external harm, privacy exposure, financial
loss, irreversibility, or loss of user control.
