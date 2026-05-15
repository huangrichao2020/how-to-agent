---
name: cognitive-governance
description: Use when turning agent conversations, logs, memory, feedback, or diary entries into durable cognition. Separates trace, episode, claim, fact, knowledge, procedure, identity, nourishment, and L5 human real behavior so agents improve attention, association, response, and feedback loops instead of merely storing more memory.
---

# Cognitive Governance

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md)

Use this skill when an agent system needs to decide what to remember, what to
believe, what to generalize, and what to turn into a repeatable behavior.

This is not a storage pattern. It is a cognition-quality pattern.

In a runtime such as GA or Hermes, this must be applied globally, not only when
the user writes a diary. Every channel turn should pass through Purpose
detection, attention gating, context assembly, response/action, feedback
capture, and admission. Diary is only one input surface among Feishu messages,
daily chat transcripts, Feishu Docs, task logs, tool outputs, restart events,
notes, and user-authored real-life records.

Use the principle **write once, route many**: when the user writes in Feishu
Docs, read the document; when the user says "everything we just discussed", use
recent conversation evidence; when the material is about runtime behavior,
route it toward skills/SOPs; when it is about real life, route it toward L5;
when it is about relationship quality, route it toward nourishment.

## Core Principle

Raw events become memories. Verified claims become facts. Reusable
explanations become knowledge. Repeatable actions become skills. Stable values
become identity.

For long-term user relationships, add one more rule: interactions that make the
user clearer, more energized, more capable of judgment, and more able to act
belong to the nourishment layer.

When the user intentionally writes a diary, reviews a day, or uses voice input
to capture real life, treat it as L5 human real behavior. L5 is a reality
anchor, not a casual chat impression; raw text is local and private by default,
and only admitted summaries enter long-term memory.

When aligning with DIKWP, P means Purpose, not Pattern. Patterns are extracted
from Data/Information and stabilized in Knowledge; they should not replace
Purpose.

DIKWP is the semantic-cognition layer:

| DIKWP | Agent meaning | Core question |
|---|---|---|
| Data | Raw signals, logs, messages, tool outputs | What is the signal and source? |
| Information | Purpose-selected differences and relations | What difference matters now? |
| Knowledge | Structures, rules, verified explanations | What explains or predicts? |
| Wisdom | Judgment using values, risk, and long-term goals | What is the appropriate choice? |
| Purpose | Goal, motive, success criterion | Why act, and what counts as good? |

Cognitive governance is the runtime-governance layer: it decides whether a
DIKWP product belongs in trace, episode, claim, fact, knowledge, procedure,
identity, nourishment, or L5 behavior.

## Classification Ladder

| Layer | Question | Examples | Action |
|---|---|---|---|
| Trace | What happened? | logs, tool output, raw messages | Store as evidence or discard |
| Episode | What was the context? | one task, one outage, one chat thread | Save as reconstructive memory |
| Claim | What might be true? | "the user dislikes X" | Keep provisional until checked |
| Fact | What should we currently believe? | active preference, live config | Store with provenance and freshness |
| Knowledge | What pattern transfers? | architecture principle, causal lesson | Write a reusable explanation |
| Procedure | How should we do it next time? | SOP, skill, checklist | Make it executable and verifiable |
| Identity | What kind of agent are we? | tone, boundaries, policy | Change slowly and explicitly |
| Nourishment | Does the user grow from this? | understand me, know me, receive me, resolve me, nourish me | Leave the user clearer and stronger |
| L5 behavior | What happened in the user's real life? | diary, voice dictation, action, avoidance, energy, feedback | Use as a reality anchor; keep raw text local and admit summaries |

## Workflow

1. **State the Purpose.** What is the current goal, success criterion,
   constraint, and feedback signal?
2. **Collect the Data.** Identify whether it came from the user, a tool, a
   log, a channel, a model inference, or external documentation.
3. **Extract Information.** Under the current Purpose, which difference,
   relation, or anomaly matters?
4. **Form candidate Knowledge.** Which structure, rule, or explanation might
   transfer? Is the evidence enough?
5. **Run a Wisdom check.** Did you account for long-term goals, user
   preferences, ethics, safety, relationships, and risk?
6. **Run a Nourishment check.** Will this make the user clearer, more
   energized, more capable of judgment, and more able to act?
7. **Run an L5 check.** Is this a user-authored real-behavior diary? Should the
   raw text stay local and private?
8. **Classify it.** Use the governance ladder before choosing a storage surface.
9. **Check authority.** User-confirmed, tool-observed, externally sourced, or
   model-inferred are not equal.
10. **Check freshness.** Mark the item as current, historical, unknown, or
   timeless.
11. **Check usefulness.** Keep only items that will improve future attention,
   association, action, or feedback evaluation.
12. **Choose the surface.**
   - trace store for raw evidence
   - episode/session store for context reconstruction
   - fact store for current accepted claims
   - knowledge doc for transferable models
   - skill/SOP for repeatable action
   - identity/policy file for slow-changing values
   - relationship manual for nourishment principles
   - L5 diary store for user-authored real-behavior entries
13. **Write the smallest durable form.** Prefer a short sourced statement over a
   long transcript; raw diary text is not exported by default.
14. **Add a retirement rule.** Decide when the item should expire, be rechecked,
   or be demoted.
15. **Test retrieval.** Make sure the next agent can find it when the trigger
   appears.
16. **Close the feedback loop.** Record how future outcomes should confirm or
   revise Purpose, Knowledge, action strategy, nourishment style, or
   real-behavior rhythm.

## Admission Gate

Before promoting anything into fact, knowledge, procedure, or identity, ask:

- Is there evidence beyond model intuition?
- Does it still apply now?
- Is it specific enough to guide behavior?
- Is it safe to generalize?
- Does it conflict with a newer source of truth?
- Can the agent recover the evidence if challenged?

If the answer is unclear, keep it as a claim or episode, not a fact.

## Runtime Admission Store

For GA/Hermes-style runtimes, implement admission as a two-step protocol:

1. The agent may propose durable cognition by appending a hidden machine block
   to its final response:
   `<cognitive_admission>{"items":[...]}</cognitive_admission>`.
2. The UI layer strips that block from user-visible output and writes the items
   to a pending admission store.
3. Only after the user explicitly says something like "confirm these
   cognitions", "allow admission", "沉淀", or "全部可以" may the runtime promote
   pending items into durable surfaces.

Use these durable surfaces:

- `fact` for current accepted claims with scope and freshness.
- `knowledge` for transferable models.
- `procedure` for repeatable workflows or skills.
- `identity` for slow-changing agent behavior, tone, or policy.
- `nourishment` for "understand me, know me, receive me, resolve me, nourish
  me" principles that should improve future interaction quality.

Never write raw private diary text into these surfaces. Raw L5 material stays
local evidence; only user-approved summaries can be admitted.

Expose the admission store as meta-operations, not as hidden magic:

- `/cognition status` shows pending count and admitted layer counts.
- `/cognition pending` lists the latest pending candidates for the current
  chat/session scope.
- `/cognition admit` promotes the scoped pending candidates after explicit
  user confirmation.
- `/cognition context` shows the admitted cognition that would be injected
  into future turns.
- A `cognitive_store` meta-tool may let the agent inspect `status`, `pending`,
  `context`, and `propose` candidates, but `propose` must only create pending
  records. Promotion remains a user-visible admission act.

## Feedback Handling

Treat feedback as a signal, not an automatic update.

Promote feedback when it is:

- specific
- repeated or high-signal
- tied to observable outcomes
- useful for future behavior
- safe to generalize

Do not promote feedback when it is:

- only emotional with no action signal
- tied to obsolete state
- contradicted by live evidence
- too private or raw for durable storage

## Anti-Patterns

- Saving raw chat as durable truth
- Treating old summaries as current facts
- Loading every memory into active context
- Turning one emotional correction into permanent identity
- Letting channel-specific behavior become core cognition
- Creating a skill before the procedure is repeatable
- Writing knowledge that cannot guide future action
- Stopping at comforting language without making the user clearer or stronger
- Creating a sense of companionship that makes the user more dependent instead
  of freer
- Treating raw diary text as ordinary context that may be exported or exposed
- Turning one day's emotion, failure, or impulse into permanent user identity

## Output Format

When asked to convert a conversation or event into durable cognition, return:

```text
Classification:
- Trace:
- Episode:
- Candidate claims:
- Verified facts:
- Transferable knowledge:
- Procedures / skills:
- Identity / policy:
- Nourishment / growth:
- L5 human real behavior / diary:

Admissions:
- Promote:
- Keep provisional:
- Archive only:
- Reject:

Artifacts to write:
- ...

Retirement / recheck:
- ...
```
