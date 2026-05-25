---
name: scene-to-agent-skill
description: Use when converting real business or personal work scenes into agent-ready atomic work units, A/B/C automation classes, skill candidates, approval checkpoints, rollback policy, and phased implementation plans. Trigger on scene atomization, work-content decomposition, high-frequency/low-frequency evaluation, six-dimension evaluation, AI training methodology, business process to skill, or "把场景变成 skill".
---

# Scene To Agent Skill

Use this skill when the user describes a real work scene and wants to know how
an agent should automate, assist, or package it as a reusable skill.

This is not a generic productivity framework. Its job is to turn messy work
into runtime decisions:

```text
scene -> atomic work units -> six-dimension scoring -> A/B/C class
      -> skill / tool / approval / rollback / phased rollout
```

## Core Stance

Do not ask "can AI do this?" Ask:

1. What is the smallest action unit?
2. How often does it happen?
3. What is the risk if it is wrong?
4. Should the agent act, draft, or only advise?
5. What artifact should survive for next time?

## Workflow

1. **Map the scene.**
   Identify the workflow, actors, inputs, outputs, current tools, pain points,
   frequency, time cost, and known failure modes.

2. **Choose priority subflows.**
   Score each subflow by repeatability, time cost, low human-value burden, and
   rule strength. High-repeat, high-time, low-value, strong-rule work goes
   first.

3. **Atomize the work.**
   Split priority subflows until each unit has one actor, one action, one input,
   one output, and a clear done condition.

4. **Score each atomic unit.**
   Use six dimensions:
   - rule clarity
   - execution frequency
   - data structure
   - situation predictability
   - error tolerance
   - human collaboration need

5. **Route by A/B/C class.**
   - **A: autonomous skill.** Agent may run automatically with monitoring and
     rollback. Use for low-risk, high-repeat, structured, rule-clear work.
   - **B: agent-led skill.** Agent drafts or executes most work, but a human
     confirms key nodes. Use for source changes, external messages, deploys,
     and medium-risk business actions.
   - **C: cognitive assist.** Agent analyzes, compares, drafts, or advises; a
     human decides and acts. Use for strategy, relationships, negotiation,
     creative judgment, and high-ambiguity work.

6. **Design the runtime contract.**
   For each unit, decide trigger, required context, tools, approval gate,
   rollback, logging, output surface, and verification.

7. **Promote carefully.**
   Repeated A/B units can become skills, tools, scheduled jobs, or templates.
   C units usually become decision aids, rubrics, or research workflows.

## Output Contract

Return a compact table first:

| Atomic unit | Frequency | Risk | Six-dimension verdict | Class | Runtime policy |
|---|---:|---|---|---|---|

Then provide:

- top 3 automation candidates
- human-in-the-loop checkpoints
- rollback or safety policy
- smallest first implementation
- what should become a reusable skill

## GA / Hermes Mapping

- **A class** -> cron/daemon tool, deterministic script, monitor, auto retry.
- **B class** -> task workbench card, explicit approval, safe restart, rollback
  script, final report.
- **C class** -> plain answer, research memo, decision table, or strategy
  review; do not auto-act.

High-frequency plus low-risk means "automate first".
High-frequency plus high-risk means "agent-led with confirmation".
Low-frequency plus high-risk means "assist only".

## Avoid

- Do not call a whole business process a skill before atomizing it.
- Do not automate money, contracts, compliance, safety, or reputation-impacting
  actions without a human checkpoint.
- Do not turn every useful thought into a skill. Promote only repeated,
  operational, verifiable work.
- Do not copy a client's raw private process logs into a skill.
- Do not hide uncertainty; mark missing data as `[to confirm]`.

## Verification

A good analysis should let an engineer or operator answer:

- which units can run without a human;
- which units need confirmation;
- which units are only advisory;
- what evidence would prove success;
- what happens when the agent is wrong.

Source pattern: adapted from the practical scene atomization and six-dimension
evaluation structure in `hmy1990116/ai-training-methodology`, then mapped to
agent runtime policy for GA/Hermes-style systems.
