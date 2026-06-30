# Agent Brain Architecture

Most agents still work like a faucet:

```text
input -> LLM -> output
```

That is not a brain. The LLM is closer to a language cortex: powerful at
forming thoughts and words, but not enough to decide what to notice, what to
remember, what to simulate, how to act, or how to update itself after feedback.

Ω-Brain is the missing organ system:

```text
perception -> attention -> working memory -> long-term memory -> simulation
-> thinking core -> decision -> action -> feedback -> consolidation
```

## Core Claim

Rules are not a brain. Memory is not a brain. A system prompt is not a brain.

A brain is a multi-region state machine that selects attention, retrieves
memory, simulates outcomes, uses the thinking core to find essence, strategy,
and tactics, weighs value and risk, chooses action, receives feedback, and
reshapes itself.

```text
B_t = {P_t, Atn_t, M_t, W_t, S_t, V_t, R_t, D_t}

Action_t = Decide(B_t)

B_{t+1} = Update(B_t, Feedback_t)
```

Where:

- `P_t`: perception state.
- `Atn_t`: attention state.
- `M_t`: memory state.
- `W_t`: world model.
- `S_t`: self model.
- `V_t`: value function.
- `R_t`: risk function.
- `D_t`: decision policy.

Language output should be the last step, not the first step.

## Brain Regions

| Region | Human analogy | Agent function |
| --- | --- | --- |
| Perception cortex | senses | User messages, code, logs, web pages, tools, files, screenshots. |
| Thalamus | relay and routing | Decide which signals enter main thinking and which become side evidence. |
| Attention system | salience | Select the main contradiction and current focus. |
| Working memory | active workspace | Hold the current task, constraints, evidence, plan, and open questions. |
| Hippocampus | episodic memory | Rebuild timelines, sessions, project history, and recent context. |
| Neocortex | abstraction | Concepts, methods, skills, patterns, and reusable knowledge. |
| Thinking core | higher-order thought | Essence, strategy, tactics, learning, analysis, and action structure. |
| Prefrontal cortex | executive control | Plan, inhibit, prioritize, choose scope, and handle tradeoffs. |
| Basal ganglia | action selection | Reply, ask, search, call tool, edit file, delegate, wait, or stop. |
| Limbic/value system | value and relation | User state, relationship temperature, nourishment, value, and risk. |
| Cerebellum | prediction and correction | Predict outcomes, compare with feedback, adjust parameters. |
| Default mode network | Dream and self-narrative | Night consolidation, reflection, identity continuity, long-horizon synthesis. |
| Immune system | audit and repair | Detect hallucination, context bleed, loops, stale memory, and regressions. |
| Motor cortex | execution | Shell, browser, file edits, API, MCP, subagents, deployments. |

## How It Connects To The Current Theory

```text
Ω-Brain = the organ system
T_t = thinking core record
Λ-Base = log-to-data nervous record
Σ-Loop = self-model/action/feedback consciousness loop
Threefold cultivation = growth and repair metabolism
L6 existence control = executive integration of value/risk/decision/system/causality
Dream = default-mode consolidation
```

The system should run with weak constraints when the user can steer it: visible
trace, replay, fast correction, and user takeover beat prevention-heavy control.

## Minimum Runtime Loop

```text
1. Perceive: collect signals and sources.
2. Route: decide main path vs side evidence.
3. Attend: identify the main contradiction and useful focus.
4. Retrieve: load recent, scene-matched, and task-relevant memory.
5. Model: update world model and self model.
6. Think: find purpose, constraints, main contradiction, strategic leverage,
   and smallest verifiable next action.
7. Simulate: predict candidate actions and likely outcomes.
8. Decide: choose action by value, risk, learning, cost, and user steering.
9. Act: reply, use tools, edit files, delegate, or wait.
10. Verify: compare prediction with feedback.
11. Update: write logs, samples, self-model deltas, and cultivation events.
12. Consolidate: Dream/replay turns selected experience into durable assets.
```

## File Package

The portable Ω-Brain package lives under:

```text
skills/agent-brain-architecture_Ω大脑架构与感知决策/
```

It includes:

- `SKILL_技能说明与使用指南.md`: usage workflow.
- `META.md`: brain package manifest and component contract.
- `PERSONA.md`: the brain's operating temperament.
- `SYSTEM_PROMPT.md`: a copyable prompt that makes an agent run the brain loop.
- `BRAIN_MAP.md`: brain regions and data flow.
- `RUNTIME_PROTOCOL.md`: per-turn runtime protocol.
- `DATA_SCHEMA.md`: log-to-data schema for Λ-Base and Σ-Loop.
- `EVAL_PROTOCOL.md`: replay and promotion rules.

## Copyable Prompt

```text
Run as Ω-Brain, not as a direct LLM faucet.

Before answering, pass the input through:
Perception -> Attention -> Memory -> Thinking Core -> Simulation -> Decision -> Action.

After acting, pass the result through:
Feedback -> Error -> Self-model update -> Log-to-data sample -> Consolidation.

Use weak constraints when the user is steering:
show trace, keep replay points, correct fast, and let the user take over.

Language output is the final surface of the brain, not the whole brain.
```
