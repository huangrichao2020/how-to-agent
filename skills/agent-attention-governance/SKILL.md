---
name: agent-attention-governance
description: Use when grounding agent architecture in attention governance, PromptComposer, RuntimeController, FeedbackLoop, prompt/context composition, and runtime correction points.
---

# Agent Attention Governance

Attention governance is the practical handle for the current agent architecture:

```text
Prompt / Markdown / Skill / Memory = attention anchors
Agent runtime = attention governance system
```

We cannot directly modify hidden attention inside a single LLM forward pass, but
we can manage attention through prompt/context composition before a task and
runtime correction points during the task.

## Two Main Battlefields

### 1. PromptComposer

Decides what the LLM sees first, what it trusts, what role it acts from, and
which method it uses.

Composition order:

1. real user intent;
2. task and acceptance;
3. current runtime facts;
4. necessary memory;
5. necessary skills;
6. necessary tool descriptions;
7. whether to activate thinking core `T_t`;
8. whether to activate humanistic light `H_t`;
9. whether to activate L6 existence control.

Principle:

```text
minimum context, maximum attention hit.
```

### 2. RuntimeController

Correction points:

- before planning: return to real user intent;
- before tools: check the main contradiction;
- after tools: let feedback change the next step;
- after errors: switch to diagnostic attention;
- mid-loop: check drift, scope, and forgotten acceptance;
- before output: check evidence, conclusion, next step, humanistic light, and user burden.

Principle:

```text
Do not add approval; correct attention.
```

## FeedbackLoop

After each run, record:

- which context helped;
- which context was noise;
- which skill fired too early or too late;
- which memory misled judgment;
- what the user's correction revealed;
- what the next PromptComposer should emphasize.

## Data Shape

```text
G_t = {
  attention_targets,
  context_sources,
  prompt_slots,
  active_skills,
  active_layers,
  insertion_points,
  correction_rules,
  feedback_signals
}
```

## Runtime Rules

- Decide whether the issue is initial composition or runtime correction.
- Do not solve attention problems by dumping more context.
- Do not keep every architecture layer resident for every task.
- Use tiny `G_t` for ordinary tasks.
- Expand `T_t / H_t / L6` only for complex tasks.
- Write each correction back into the next PromptComposer.
- Follow the trust axiom: always believe in our agent, carried by trace,
  replay, and correction.

## Related Files

- `../../examples/28-agent-attention-governance.md`: full method document.
- `../agent-final-architecture-outline/`: final architecture outline.
- `../agent-anti-bloat-context-engineering/`: anti-bloat and context engineering.
- `../agent-brain-architecture/`: Ω-Brain architecture.
- `../agent-thinking-core/`: thinking core.
- `../agent-humanistic-light/`: humanistic light.
