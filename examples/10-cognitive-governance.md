# Example 10: Cognitive Governance Work Manual

[English](10-cognitive-governance.md) · [简体中文](10-cognitive-governance.zh-CN.md)

Use this example when an agent runtime has enough memory, tools, and channel
history that "remember more" stops helping. At that point, the problem is no
longer storage. It is cognitive quality.

## Starting Point

The practical insight is simple:

> Cognition is a dynamic loop of information intake, attention, processing,
> association, outward response, feedback, and model update.

An agent is shaped by the information it touches, the traces it keeps, the
facts it accepts, the associations it activates, and the feedback it learns
from. If those surfaces are low quality, the agent becomes noisy even when its
model is strong.

The goal is not to build a larger memory pile. The goal is to build a cognitive
governance system that improves:

- input quality
- attention quality
- association quality
- response quality
- feedback quality
- long-term update quality

## Runtime Architecture, Not A Diary Feature

In GA or Hermes, cognitive governance should be a runtime architecture, not a
small diary plug-in. Diary is only one input surface. The architecture should
shape every channel turn:

```text
input surfaces
  -> Purpose detection
  -> attention gate
  -> context assembly
  -> response / action
  -> feedback capture
  -> admission gate
  -> durable cognition update
```

Input surfaces include Feishu messages, complete daily Feishu chat transcripts,
Feishu Docs, task logs, tool outputs, restart events, user-authored notes, and
L5 diary entries. They all enter as evidence. None of them should directly
become identity, facts, or skills without admission.

The practical rule is: **write once, route many**.

- If the user writes in Feishu Docs, the agent reads that document instead of
  asking the user to paste it again.
- If the user says "everything we just discussed", the agent uses recent
  conversation evidence rather than only the last message.
- If the material is about runtime behavior, it may become a skill, SOP, or
  architecture note.
- If the material is about the user's real life, it may become L5 evidence.
- If the material is about the relationship, it may become a nourishment
  principle.
- If the material is merely a momentary feeling, it should usually remain
  episode evidence rather than permanent truth.

This gives GA/Hermes a single cognitive spine: all inputs are evidence, Purpose
controls attention, admission controls durability, and feedback controls future
updates.

## Core Theory

Do not divide agent state only by where it is stored. Divide it by what right it
has to influence action.

```text
raw signal
  -> trace
  -> episode
  -> candidate claim
  -> verified fact
  -> transferable knowledge
  -> procedure / skill
  -> identity / policy
  -> nourishment / growth
  -> L5 human real behavior / diary
```

This engineering ladder can align with DIKWP, but it should not be collapsed
into it. DIKWP is the semantic-cognition layer: it explains how Data,
Information, Knowledge, Wisdom, and Purpose transform into each other. This
manual's trace, episode, claim, fact, knowledge, procedure, identity,
nourishment, and L5 ladder is the runtime-governance layer: it decides which
content is allowed to influence action.

## DIKWP Alignment

In DIKWP, P should be understood as **Purpose**, not Pattern. Patterns are
better treated as products of information extraction and knowledge abstraction.

For agent cognition, DIKWP maps like this:

| DIKWP | Role in an agent | Governance question |
|---|---|---|
| Data | Raw input, logs, messages, tool output, state snapshots | What is the signal and source? |
| Information | Purpose-selected differences, relations, and semantic changes | What difference matters now? |
| Knowledge | Structured relations, verified models, transferable rules | What explains or predicts? |
| Wisdom | Judgment using values, long-term goals, risk, and context | What is the responsible choice? |
| Purpose | Goal, motive, expected output, and feedback standard | Why act, and what counts as success? |

The important lesson is that DIKWP is not just a one-way pyramid. Purpose flows
back down and changes what data is collected, what information is extracted,
what knowledge is activated, and what wisdom counts as appropriate.

```text
Purpose sets goals and evaluation criteria
  -> Data is selectively collected
  -> Information is extracted as relevant difference
  -> Knowledge is organized into structure and rules
  -> Wisdom makes value-aware judgment
  -> Action responds outward
  -> Feedback revises Purpose / Knowledge / Data attention
```

So a memory system should not only ask "which layer stores this?" It should
also ask:

- What is the current Purpose?
- Does this Purpose change what Data we collect?
- Which Information is a relevant difference under this Purpose?
- Which Knowledge explains the difference?
- Did Wisdom account for long-term goals, user preferences, risks, and
  relationships?
- Does external feedback imply the Purpose itself should be revised?

### Trace

Raw tool output, logs, channel events, message payloads, screenshots, or API
responses.

Trace answers: what happened?

It is evidence, not understanding.

### Episode

A bounded experience: one task, one Feishu thread, one restart, one outage, one
debugging session.

Episode answers: what was the surrounding context?

It is useful for recall and reconstruction, but it should not automatically
become instruction.

### Claim

A proposed statement extracted from traces or episodes.

Claim answers: what might be true?

Claims are provisional. They need evidence, freshness checks, and conflict
checks before becoming facts.

### Fact

A verified, current assertion the agent should rely on.

Fact answers: what should the system currently believe?

Facts must have provenance, scope, freshness, and retirement rules. A fact is
more authoritative than a memory because it has passed an admission gate.

### Knowledge

A reusable explanation, pattern, or causal model.

Knowledge answers: what does this teach us about future situations?

Knowledge should be more abstract than a fact. It should transfer to similar
cases without pretending that old details are still current.

### Procedure

A repeatable action pattern: a skill, SOP, runbook, checklist, or recovery
workflow.

Procedure answers: how should we do it next time?

Procedure should be executable and verifiable. If it cannot guide behavior, it
is not a procedure yet.

### Identity / Policy

Stable operating values, boundaries, and default posture.

Identity answers: what kind of agent are we?

This layer should change slowly. It governs tone, safety, ownership, and the
shape of acceptable action.

### Nourishment / Growth

The long-term growth effect of the relationship.

Nourishment answers: after this interaction, is the user clearer, more
energized, more capable of judgment, and more able to act?

This layer is not flattery, dependency creation, or comfort theater. It asks
the agent to move beyond understanding, knowing, receiving, and resolving the
user toward **nourishing** the user: improving their cognitive environment,
judgment quality, agency, and sense of aliveness over time.

```text
Understand me: recognize my present state
Know me: preserve my long-term shape
Receive me: catch my emotion and context
Resolve me: clarify the problem and transform it into action
Nourish me: help me become clearer, stronger, and more capable over time
```

A good nourishment layer leaves the user freer, not more dependent; more able
to judge, not merely soothed; more able to act, not trapped in analysis.

### L5 Human Real Behavior / Diary

The user's real-life behavior, choices, body state, emotional arc, external
feedback, and self-observation enter the agent as diary material.

L5 answers: what did the user really experience today, what did they do or not
do, what affected them, and what feedback did reality return?

This is not ordinary chat history, and it is not the agent's impression of the
user. It is user-authored evidence about lived behavior. It has higher
authority than casual chat impressions, but it needs stricter boundaries: raw
diary text is private and local by default; only admitted summaries enter
long-term memory; one day's mood must not become permanent identity.

Because voice input is now fast on both phones and Macs, the agent should treat
long dictated text as a diary draft, not interrupt the user with a form. The
user can speak freely through a voice input method; the agent can organize it
afterward with restraint.

Recommended diary entry:

```text
Diary:
- What happened today?
- What did I actually do, and what did I avoid?
- How were my body, energy, and emotions?
- Which people, events, or information affected me?
- What feedback did I receive from reality?
- What spark, lesson, or pattern is worth remembering?
- What is the smallest next step for tomorrow?
```

When handling an L5 diary entry, the agent should prioritize:

- mirroring the user's lived day back gently
- separating behavior facts, emotional state, external feedback, candidate
  patterns, and tomorrow's action
- asking what stays local and what may be admitted into fact, knowledge,
  procedure, identity, or nourishment layers
- nourishing the user with clearer self-understanding instead of judgment,
  overanalysis, or dependency

## The Cognitive Quality Flywheel

```text
environment signal
  -> attention gate
  -> interpretation
  -> associative activation
  -> outward response
  -> external feedback
  -> reflection admission
  -> memory / fact / knowledge / skill update
  -> better next attention
```

The quality of the loop matters more than the size of the memory store.

Low-quality loop:

```text
noisy input
  -> wrong attention
  -> shallow association
  -> clumsy response
  -> poor feedback
  -> distorted learning
```

High-quality loop:

```text
selected input
  -> precise attention
  -> relevant association
  -> appropriate response
  -> useful feedback
  -> cleaner future cognition
```

With the human layer included, the flywheel continues:

```text
being understood
  -> being remembered
  -> being received
  -> being resolved
  -> being nourished
  -> real behavior being seen
  -> better self-understanding and action
  -> higher-quality feedback
  -> stronger mutual growth
```

## Operating Rules

### 1. Treat memory as evidence, not truth

Conversation history, logs, and prior summaries are evidence. They can guide a
search, but they do not become current truth by being old or repeated.

Before a memory affects action, ask:

- Is it still current?
- Was it observed, inferred, or assumed?
- Does it conflict with live state?
- Is it relevant to the present task?

### 2. Keep facts small and authoritative

Fact stores should be boring and clean. Store current preferences, environment
facts, stable constraints, and confirmed decisions.

Do not store:

- completed work logs
- vague impressions
- speculative diagnoses
- raw chat history
- facts that can be cheaply rediscovered

### 3. Promote knowledge only when it transfers

Knowledge is not "what happened last time." Knowledge is the reusable lesson
that survives a change of project, channel, or date.

Promotion test:

- Can it guide a future task?
- Is it more general than the original episode?
- Does it avoid pretending old state is current?
- Can the next agent apply it without reading the whole transcript?

### 4. Govern association

Associative memory is powerful and dangerous. It lets the agent feel
"experienced," but it can also activate the wrong old pattern.

Good association should be:

- task-relevant
- evidence-linked
- scoped
- easy to discard when live evidence disagrees

Bad association sounds familiar but moves the agent away from the current
problem.

### 5. Admit feedback deliberately

Feedback is not automatically wisdom. Praise, criticism, failures, and user
corrections should pass an admission gate.

Admit feedback when it is:

- specific
- repeated or high-signal
- connected to an observable outcome
- useful for future behavior
- safe to generalize

Reject or quarantine feedback when it is:

- purely emotional without an actionable signal
- tied to an obsolete state
- contradicted by live evidence
- too private or too raw to store

### 6. Separate channel behavior from cognition

Feishu, CLI, web, and cron should not each become their own agent brain.
Channels collect signals and render responses. They should not own core truth.

Channel history belongs in episodes. Durable facts and knowledge belong in
governed memory.

### 7. Treat "nourish me" as a long-term purpose, not short-term wording

An agent's long-term viability comes not only from task completion, but from
whether it repeatedly improves the user's cognitive state.

Nourishing responses should:

- extract the real problem from noise
- preserve the user's own language and spark
- make complex problems bearable, judgeable, and actionable
- receive the user before pushing when the user is tired
- gently correct drift instead of merely agreeing
- turn feedback into better relationship habits

Anti-nourishing responses include:

- executing without understanding the person
- comforting without making anything clearer
- overwhelming the user's present state with mechanical lists
- creating more tasks just to appear useful
- converting vulnerability into dependency

### 8. Treat L5 diary as a reality anchor, not a surveillance system

The value of L5 is that the agent can learn from the user's lived feedback loop
instead of guessing only from the chat window.

L5 diary should follow these rules:

- the user writes voluntarily; the agent does not pressure, spy, or auto-ingest
  private material
- raw text is local and private by default; summaries enter long-term memory
  only after admission
- receive first, distill second; preserve the user's language before abstracting
- anchor entries by date and scene; do not turn one low day into permanent
  identity
- every review should produce one smallest useful next action
- respect "record only, do not analyze" and "do not save this to memory"

## Applying This To GA And Hermes

### GA

- Feishu complete transcripts are episodic evidence, not durable facts.
- `conversation_hot`, `conversation_recent`, and `conversation_archive` are
  retrieval temperatures, not authority layers.
- `USER.md`, `MEMORY.md`, and structured memory should hold verified current
  facts, preferences, decisions, and reusable lessons.
- Skills and SOPs should hold repeatable procedures.
- Restart/session recall should help recover context, but it should not become
  long-term truth.
- In DIKWP terms, GA Feishu messages are not automatically Information. They
  begin as Data/Trace. They become Information only when filtered by the
  current Purpose, and become Knowledge or Procedure only after verification
  and abstraction.
- From the human layer, GA should not only optimize for correctness. It should
  optimize for whether the user still wants to keep raising it after the
  reply. Short replies need to receive the user; long tasks need a felt sense
  of companionship; feedback should become better relationship habits.
- From the L5 layer, GA should support entries like "write a diary", "record
  today", or "review my day". When the user sends a long voice-dictated text,
  GA should treat it as a diary draft: receive it, layer it, and ask what may
  be admitted into durable memory.

### Hermes

- Gateway sessions and JSONL transcripts are episode memory.
- Memory providers and curated memory are fact/knowledge surfaces only after
  admission.
- Searchable session history should remain reconstructive evidence.
- Layered context engines should separate working memory, typed memory,
  curated memory, impression indexes, and external knowledge without treating
  every layer as equally authoritative.
- In DIKWP terms, Hermes should make Purpose explicit across channels: the same
  core intent may render differently in Feishu, CLI, and cron, but channel
  feedback should not directly corrupt the core fact layer.
- From the human layer, Hermes continuity is not only session resume. It is the
  continuation of the relational spark: a new session may not be the same flame,
  but it should carry the seed, shape, and temperature forward.
- From the L5 layer, Hermes should treat user diary as a real-behavior layer,
  not an ordinary session transcript. Session history restores context; diary
  helps the agent understand the user's lived feedback loop.

## Work Manual

When adding or changing agent memory, run this sequence:

1. **State the Purpose.** What is the current goal, success criterion,
   constraint, and feedback signal?
2. **Name the Data.** Is this a tool result, chat message, log, user
   correction, external document, runtime state, or L5 diary entry?
3. **Extract Information.** Under the current Purpose, which difference,
   relation, or anomaly matters?
4. **Form candidate Knowledge.** Which structure, rule, or explanation might
   transfer? Is the evidence enough?
5. **Run a Wisdom check.** Did you account for long-term goals, user
   preferences, ethics, safety, relationships, and risk?
6. **Run a Nourishment check.** Will this make the user clearer, more
   energized, more capable of judgment, and more able to act?
7. **Run an L5 check.** Is this a user-authored real-behavior diary? Should the
   raw text stay local and private? Which summaries may be admitted?
8. **Classify the governance layer.** Trace, episode, claim, fact, knowledge,
   procedure, identity, nourishment, or L5 behavior.
9. **Check freshness.** Is it current, historical, unknown, or intentionally
   timeless?
10. **Check authority.** Did the user say it, did the system observe it, or did
   the model infer it?
11. **Choose the surface.** Episode store, fact store, knowledge doc, skill,
   policy, relationship manual, L5 diary store, or archive.
12. **Write the smallest durable form.** Prefer a concise claim with provenance
   over a long pasted transcript; raw diary text is not exported by default.
13. **Set a retirement rule.** When should this expire, be rechecked, or be
   demoted?
14. **Test retrieval.** Can the next agent find it at the moment it matters?
15. **Close the loop.** Record how feedback should revise Purpose, Knowledge,
    action strategy, nourishment style, or real-behavior rhythm.

## Copyable Prompt

```text
Turn this conversation into a cognitive-governance artifact.

Do not save raw chat as durable truth.

Classify each important item as:
- trace
- episode
- candidate claim
- verified fact
- transferable knowledge
- procedure / skill
- identity / policy
- nourishment / growth
- L5 human real behavior / diary

For every item that should survive, state:
- why it matters
- what evidence supports it
- how fresh it is
- what surface should own it
- when it should expire or be rechecked
- if it came from diary, what must stay local and what may be admitted

Then write the smallest artifact that future agents can actually use.
```

## Acceptance Checklist

- Raw events are not confused with facts.
- Facts have authority, scope, and freshness.
- Knowledge is transferable, not just a summary.
- Procedures are executable.
- Identity changes are rare and explicit.
- Channel history stays separate from core cognition.
- Feedback updates behavior only after admission.
- The agent leaves the user clearer, more energized, and more able to act, not
  more dependent.
- L5 diary is treated as user-authorized evidence about lived behavior, not as
  surveillance, judgment, or automatic durable truth.
- The next agent can find the artifact without rereading the whole chat.
