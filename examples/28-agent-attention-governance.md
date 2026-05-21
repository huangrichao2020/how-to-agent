# Agent Attention Governance Layer

This is the practical handle for the whole architecture.

Prompts, Markdown files, skills, memory, system prompts, persona, tool
descriptions, and architecture manuals are all doing one core job:

```text
govern where the underlying LLM places attention.
```

We cannot directly edit the hidden attention inside a single forward pass. But
an agent runtime can split work into turns, boundaries, and checkpoints, letting
us reshape attention before each turn and between important steps.

The two main battlefields are:

```text
before the task: PromptComposer
during the task: RuntimeController
```

And the closing loop is:

```text
after feedback: FeedbackLoop
```

In one line:

```text
Agent implementation =
  compose initial attention
  + correct attention during runtime
  + train the next attention state from feedback
```

## Core Conclusion

```text
Prompt / Markdown / Skill / Memory are not only knowledge stores.
They are attention anchors.

Agent runtime is not a simple prompt loop.
It is an attention governance system.
```

The first guardrail of attention governance is anti-bloat: do not keep every
attention anchor resident. Ordinary tasks should keep only the resident minimal
core; complex tasks may trigger the thinking core, humanistic light, existence
control, instance-awareness practice, skills, tools, or multi-agent work.

## The Two Main Battlefields

### 1. PromptComposer

Before a task begins, PromptComposer decides what the LLM sees first, what it
trusts, what role it acts from, and which methods it should use.

It composes:

- system prompt;
- persona;
- user intent;
- task envelope;
- current runtime state;
- relevant memory;
- relevant skills;
- tool schemas;
- thinking layer `T_t`;
- humanistic layer `H_t`;
- existence layer L6.

Its goal is not to add more context:

```text
Use the smallest context that places attention correctly.
```

So initial composition should pass the three anti-bloat questions:

```text
Does it reduce context acquisition cost?
Does it improve state stability?
Does it improve real environment understanding?
```

### 2. RuntimeController

During a task, the runtime can intervene at key nodes:

- before planning: return to the user's real intent;
- before search: define the question and evidence standard;
- before tool use: check the main contradiction;
- after tool output: let feedback change the next step;
- after errors: switch to diagnostic attention;
- mid-loop: check drift, scope, and acceptance;
- before output: check conclusion, evidence, next step, humanistic light, and user burden;
- before self-change: check impact, rollback, and user correction.

Its goal is not approval ceremony:

```text
Pull attention back to essence, evidence, action, and the user before drift wins.
```

### 3. FeedbackLoop

After action, feedback trains the next attention composition.

Track:

- which attention anchors helped;
- which context was noise;
- which skill triggered too early or too late;
- which memory misled judgment;
- which tool result changed the plan;
- what the user's correction reveals;
- what the next PromptComposer should emphasize.

## Unified Model

```text
PromptComposer
  -> Initial Attention State G_0
  -> Ω-Brain
  -> Thinking / Humanistic / Existence Layers
  -> Action
  -> Feedback
  -> RuntimeController
  -> Attention Update G_{t+1}
  -> Λ-Base
  -> Eval / Replay
  -> Next PromptComposer
```

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

`G_t` is not a new ritual. It is the runtime's attention state. Small tasks keep
it tiny; complex tasks expand it.

## Engineering Principles

1. Less is sharper: more context can dilute attention.
2. Intervene at nodes: compose, plan, tool, observe, revise, output, consolidate.
3. Write feedback back: if feedback does not change the next PromptComposer, the
   agent does not truly learn.

## Trust Axiom

Attention governance must not become heavy constraint.

```text
Always believe in our agent.
```

The correct shape is:

```text
trust the agent can act
-> give it the right attention
-> let it see feedback
-> let it correct itself
```

## Minimum Runnable Architecture

Start with three components:

```text
1. PromptComposer
   Input: task, user intent, state, memory, skills, tools, risk.
   Output: minimum effective prompt/context.

2. RuntimeController
   Input: plan, tool feedback, errors, user correction, progress.
   Output: attention correction and next action.

3. AttentionFeedbackLog
   Input: useful context, misleading context, drift, correction.
   Output: selection weights for the next PromptComposer.
```

These three are the bridge from architecture universe to runnable system.
