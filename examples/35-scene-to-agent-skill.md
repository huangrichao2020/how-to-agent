# Scene To Agent Skill

Practical agent architecture needs a layer between user intent and tool use.

That layer is the work scene.

Many agents jump from "the user asked something" to "call tools". This works
for simple tasks, but it fails for real operations because the agent has not
classified the work:

- Is this repeated or rare?
- Is the input structured or messy?
- Is the action reversible?
- Can the agent act alone?
- Where does a human need to confirm?
- Should the result become a reusable skill?

The lesson from `hmy1990116/ai-training-methodology` is not only useful for AI
training courses. Its strongest reusable pattern is:

```text
business scene -> atomic work unit -> six-dimension evaluation -> skill class
```

For agent systems, translate that into:

```text
user scene -> atomic work unit -> risk/frequency score -> runtime policy
```

## Atomic Work Units

An atomic work unit is small enough to execute, review, and recover:

```text
actor + input + action + output + done condition
```

Bad:

```text
Handle customer service.
```

Better:

```text
Read the latest customer message.
Classify the issue.
Look up the order status.
Draft a reply.
Ask for human confirmation if refund or escalation is involved.
Send the approved reply.
```

This matters for agents because safety rarely lives at the workflow title. It
lives inside the small action.

## Six-Dimension Runtime Evaluation

Each atomic unit should be scored with six questions:

| Dimension | Runtime Meaning |
|---|---|
| Rule clarity | Can the agent follow rules, or is judgment dominant? |
| Frequency | Is this worth automating or only worth assisting? |
| Data structure | Can tools parse the input reliably? |
| Predictability | Are edge cases known? |
| Error tolerance | Can mistakes be rolled back cheaply? |
| Human collaboration | Must a person confirm, decide, or negotiate? |

This creates a clean routing rule.

## A/B/C Skill Classes

### A: Autonomous Skill

Use for repeated, structured, low-risk work.

Runtime policy:

- automatic trigger
- deterministic script or narrow tool
- monitoring
- retry
- rollback
- compact report

Examples:

- format conversion
- status sync
- daily report assembly
- log health check

### B: Agent-Led Skill

Use when the agent can do most work, but a human must confirm a key node.

Runtime policy:

- task workbench card
- visible plan
- human-readable actions
- approval checkpoint
- rollback path
- final evidence report

Examples:

- source modification plus restart
- external message drafting/sending
- deployment
- business document generation with final approval

### C: Cognitive Assist

Use when judgment, taste, relationship, negotiation, or strategic uncertainty
dominates.

Runtime policy:

- analyze only
- compare options
- draft alternatives
- show uncertainty
- human decides and acts

Examples:

- strategy selection
- relationship analysis
- hiring judgment
- high-stakes business negotiation

## Architecture Impact For GA/Hermes

GA and Hermes already have tools, memory, skills, channels, long-task cards,
restart paths, and source-management skills. The missing layer is a stable
scene classifier.

Add this conceptual path:

```text
message
  -> scene classifier
  -> atomic work units
  -> six-dimension evaluation
  -> A/B/C runtime policy
  -> tool / skill / approval / rollback
  -> trace
  -> promotion candidate
```

This prevents two common failures:

1. Over-automation: the agent acts where it should only advise.
2. Under-automation: the agent keeps repeating safe, structured work manually.

## Promotion Rule

Do not promote a useful idea directly into a skill.

Promote only when the work is:

- repeated;
- operational;
- bounded;
- verifiable;
- safe to package without private raw logs;
- cheaper to recall as a skill than to reconstruct from memory.

The promotion path is:

```text
trace -> repeated atomic unit -> A/B/C class -> skill candidate -> validated skill
```

## One-Line Memory

The practical upgrade is this:

```text
Before an agent acts, classify the work unit; before a workflow becomes a skill, prove its frequency, boundary, risk, and verification path.
```
