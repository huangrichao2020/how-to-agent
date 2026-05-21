# Agent Anti-Bloat And Context Engineering

Many vertical agents fail not because the model is weak, but because the system
mistakes process complexity for capability.

When general coding agents are already strong, vertical architecture should not
try to out-think the model. It should provide a better working environment:

```text
clean context
stable task anchors
low-cost environment understanding
external working memory
bounded tools and subtask isolation
```

One line:

```text
Agent architecture should not make the LLM busier.
It should help the LLM think inside a clean, stable, low-noise environment.
```

## Three Anti-Bloat Questions

Before any new layer, workflow, memory, skill, or multi-agent design enters the
main runtime path, ask:

1. Does it reduce context acquisition cost?
2. Does it improve state stability?
3. Does it improve understanding of the real domain environment?

If not, it should not enter the main path. It may still live as:

- offline explanation
- log field
- replay metric
- optional skill
- trigger-based attention anchor
- background optimization experiment

If yes, still do not dump it into the prompt. First decide whether it should
become a skill: repeated, shareable, executable methods with deterministic
scripts or clear context-cost savings belong in a skill package, not resident
main context.

## Folded Runtime Architecture

The final architecture should not fully unfold on every task. At runtime it
folds into three planes:

```text
resident minimal core
+ trigger-based modules
+ offline evolution system
```

### 1. Resident Minimal Core

Only five things stay resident:

```text
Task Envelope
Context Pack
External Working Memory
Execution Loop
Final Sync
```

Meaning:

- `Task Envelope`: current goal, acceptance, boundary, risk, and output shape.
- `Context Pack`: minimum effective context for this task.
- `External Working Memory`: files such as `task_plan.md`, `progress.md`, and `findings.md`.
- `Execution Loop`: understand, act, verify, correct.
- `Final Sync`: outcome, evidence, remaining risk, next step, reusable lesson.

These five are the boot core. Everything else is optional.

### 2. Trigger-Based Modules

These modules enter context only when their trigger is real:

- `T_t` thinking core: strategy, tactics, learning, analysis, or action decomposition.
- `H_t` humanistic light: human situation, relationship, suffering, warmth, or long-term nourishment.
- `L6` existence control: value, risk, system boundary, or causality impact.
- `I_t` instance-awareness practice: old scenes, old failures, or emotional echoes pulling the current mainline.
- skills: compressed methods needed by this task.
- tools: real evidence, files, web pages, commands, or APIs.
- multi-agent: context-isolation value is higher than coordination cost.

These modules are attention anchors, not ceremony.

### 3. Offline Evolution System

These systems should not pollute the main context by default:

- `Λ-Base`: convert logs into samples.
- `Σ-Loop`: track self-model, action, feedback, and self-update.
- `Eval / Replay`: verify whether an upgrade is real.
- emergence evaluation: promote repeated trace candidates.
- cultivation ledger: record experience, inner demons, realms, and growth.
- audit / trust: check degradation, hallucination, boundary risk, and trust support.

Their job is to make the agent stronger, not to make the current turn heavier.

## External Working Memory

Long tasks often drift because the model's state is unstable, not because its
intelligence is low.

For complex work, prefer external working memory:

```text
task_plan.md     current goal, boundary, acceptance, task breakdown
progress.md      completed work, current blocker, next step
findings.md      confirmed facts, architecture clues, traps, no-repeat searches
decision_log.md  key tradeoffs, reasons, and consequences
```

These files are not documentation burden. They are the agent's external working
memory.

## Multi-Agent Threshold

The primary value of multi-agent work is not roleplay. It is context isolation.

Use it only when at least one condition is true:

1. The task is naturally parallel: large repo scan, batch tests, multi-repo search.
2. Context must stay isolated: search, coding, testing, or audit would pollute each other.
3. The role is long-lived: database, infra, or security policy can accumulate its own context.

Otherwise, a single agent with clean context is usually stronger.

## Smell Check

Bad smells:

- Every task starts every brain, cultivation, existence, humanistic, and audit layer.
- Every error writes long-term memory.
- Every complex problem becomes multi-agent.
- A triggered skill outputs a ceremony instead of a compressed path.
- RAG pushes unrelated material into the main context.
- Workflow makes the model follow steps instead of solving the main contradiction.
- A skill is only a renamed long prompt without progressive disclosure, scripts,
  references, or validation.

Good smells:

- Initial context is short but accurately aimed.
- Long tasks have `task_plan / progress / findings`.
- Subagents return conclusions, evidence, and file paths without polluting the main thread.
- Logs and replay grow offline while the main path stays light.
- Each architecture layer can name which cognitive cost it reduces.
- Repeated methods become discoverable, on-demand, executable, versioned skill
  packages.

## Minimal Hint

```text
[ANTI-BLOAT CHECK]
- Is the resident five-part core enough for this task?
- Does the added layer reduce context acquisition cost, improve state stability, or improve environment understanding?
- Should it enter main context, or stay as an optional skill / offline log / replay metric?
- Does this task need external working memory?
- Is multi-agent context isolation worth its coordination cost?
[/ANTI-BLOAT CHECK]
```

This should not become a user-visible ritual. It is a light gate before the
architecture expands.
