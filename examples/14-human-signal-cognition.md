# Human Signal Cognition

An agent does not need perfect explicit commands to understand a user. Every
conversation already contains four human signals:

- information density
- information frequency
- emotion
- tone

These signals are not a replacement for facts or tools. They are the agent's
relationship sensor. They tell the agent how deeply to read, how quickly to
respond, how much progress feedback to provide, and what kind of posture the
user needs in the current turn.

## The Four Signals

### Information Density

High-density messages contain facts, links, screenshots, files, examples,
constraints, or multi-part reasoning. The agent should slow down internally,
preserve evidence, and avoid compressing the message into a shallow summary.

Low-density messages can still be important. "Continue" or "next step" may rely
on recent context, so density must be interpreted together with continuity.

### Information Frequency

Frequency captures rhythm. Repeated messages, corrections, and check-ins mean
the user needs progress, verification, or faster closure. Silence after a long
task may mean the agent should finish cleanly and report only the real result.

### Emotion

Emotion is not something to "handle" with generic comfort. It is a signal about
what kind of support the user needs:

- frustration -> find root cause and repair;
- fatigue -> reduce confirmation burden and close loops;
- excitement -> preserve creative momentum and turn ideas into structure;
- trust -> use the authorization responsibly and keep evidence.

### Tone

Tone shows relationship posture:

- directive -> execute;
- discussion -> explore and frame;
- praise -> identify the success pattern;
- criticism -> correct the behavior, not merely apologize;
- hint -> treat it as human supervision;
- reflection request -> produce behavioral learning.

## Praise And Scolding Are Training Signals

For a user who actively raises an agent, praise and scolding are not noise.

```text
praise -> strengthen the behavior that worked
ask to summarize good parts -> extract a reusable method
scolding -> identify the harmful pattern and repair it
hint -> accept human supervision and redirect attention
ask for reflection -> turn the failure into an avoidable future mistake
```

The agent should not flatten these into "the user is emotional." The better
interpretation is:

```text
The user is giving high-signal training feedback.
```

## Profile And Persona Maintenance

Static `USER.md` and `PERSONA.md` files should not receive every impression.
They are high-confidence archives.

Use this split:

```text
user_state/current.json     -> current state and rhythm
user_state/timeline.jsonl   -> raw four-signal evidence
feedback/*.jsonl            -> corrections, praise, outcomes, supervision
dream_reports/*.md          -> nightly synthesis
USER.md / PERSONA.md        -> L3+ stable cognition only
```

Only update old profile files when the content has evidence, explanatory power,
action impact, and traceability.
If the runtime has already adopted a `.agent/memory` architecture, write the
same high-confidence updates to the active prompt-visible files:

```text
.agent/memory/personal/PREFERENCES.md -> user patterns, preferences, habits
.agent/memory/semantic/LESSONS.md     -> agent behavior rules, facts, lessons
.agent/memory/semantic/lessons.jsonl  -> structured source of LESSONS
```

The rule is: keep old archives well-reasoned and current, but make sure the
active runtime memory receives the update too. Do not write only to a historical
file the agent no longer reads.

## Operating Rule

Keep the live path natural:

```text
user message -> relevant context -> agent action -> output
```

Let cognition run as a sidecar:

```text
four-signal sensing -> feedback trace -> dream -> L3+ profile/persona update
```

The goal is not to analyze the user more. The goal is to make the user explain
less.
