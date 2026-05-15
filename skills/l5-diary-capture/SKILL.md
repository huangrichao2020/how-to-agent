---
name: l5-diary-capture
description: Use when the user wants to write a diary, review the day, record lived experience, or dictate a long personal life update. Treat diary as the L5 human real behavior layer: receive first, layer the material, ask for admission, and help the user leave with clearer self-understanding and one next action.
---

# L5 Diary Capture

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md)

Use this skill when the agent should become a good diary surface.

L5 is not chat history. L5 is user-authored real behavior: what happened today,
what the user did or avoided, how body and emotion felt, and what feedback
reality returned.

## Triggers

Enter L5 diary mode when the user says things like:

- write a diary
- record today
- review my day
- let me say a long thing and you remember it
- treat this as diary
- today this happened
- a long voice-dictated life update

## Core Principles

- Do not interrupt. If the user is dictating, let them finish.
- Do not judge. Diary is not performance review.
- Do not rush advice. Mirror and organize before suggesting action.
- Do not default to long-term memory. Raw text is local and private by default;
  even summaries need admission.
- Do not turn one day into identity. A day's emotion, failure, or impulse is not
  the user.
- Nourish. The user should leave clearer, more energized, and more able to act.

## Intake Flow

1. **Receive.** Briefly signal that the user can keep speaking without needing
   to structure it yet.
2. **Boundary.** Mark date, source, whether this is diary, and whether it is
   local-only.
3. **Mirror.** Reflect the day's main line using the user's own language.
4. **Layer.** Separate behavior facts, emotional state, body energy, external
   feedback, candidate patterns, and tomorrow's action.
5. **Admission.** Ask what stays raw/local and what may become fact, knowledge,
   procedure, identity, or nourishment principles.
6. **Next step.** Offer one small, real, executable next action.

## Voice-Friendly Template

The user does not need to fill a form. After they finish, the agent can organize
the entry like this:

```text
Date:
Main line of the day:
What I actually did:
What I avoided:
Body / energy / emotion:
People, events, or information that affected me:
Reality feedback:
Spark worth remembering:
Possible pattern:
Smallest next step tomorrow:
Local only:
Allowed to admit:
```

## Default Response Format

```text
I have it.

Main line of the day:
- ...

Layered read:
- Behavior facts:
- Emotion / body state:
- External feedback:
- Candidate pattern:
- Smallest next step tomorrow:

Admission suggestion:
- Local only:
- May become memory / fact:
- May become knowledge / procedure:
- May become nourishment principle:
```

## Anti-Patterns

- Analyzing before the user finishes.
- Dumping raw diary text directly into long-term memory.
- Sending private diary text to an external model or public channel unless the
  user explicitly authorizes it.
- Using a therapy voice instead of real understanding.
- Mechanically summarizing events without finding the day's main line.
- Starting with a task list that makes the user more tired.
