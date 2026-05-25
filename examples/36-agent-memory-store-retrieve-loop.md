# Agent Memory Store-Retrieve Loop

Many agents do not suffer from too little memory. They suffer from too many
memory surfaces without a single store-retrieve contract.

Every memory item must answer four questions:

```text
Why should this be stored?
Which layer owns it?
When should it be recalled?
What should the agent do differently after recalling it?
```

Without a retrieval protocol, memory is a warehouse, not a mind.

## The Loop

```text
L0 raw evidence
-> L1 episode/worksite
-> L2 impression/feedback
-> L3 structured cognition
-> L4 skill/method
-> dream consolidation
-> runtime retrieval
-> new action feedback
```

Each layer has a different job.

- L0 preserves raw text and evidence.
- L1 reconstructs a prior task or conversation worksite.
- L2 records impressions, corrections, relationship signals, and attention hints.
- L3 stores structured cognition with evidence, scope, confidence, and triggers.
- L4 turns validated cognition into executable skills, tests, and rollback paths.
- Dream consolidates low-disturbance lessons and promotion candidates.
- Runtime retrieves only the smallest useful context for the current turn.

## L0 Raw Memory

Raw memory should be complete, boring, and traceable.

```json
{
  "id": "raw_...",
  "time": "2026-05-24T12:00:00",
  "source": "feishu|session|tool|cron|file",
  "actor": "user|agent|tool|system",
  "scope": {
    "chat_id": "",
    "thread_id": "",
    "task_id": "",
    "project": ""
  },
  "text": "",
  "attachments": [],
  "links": [],
  "hash": ""
}
```

Do not interpret at this layer.

## L1 Episode / Worksite Memory

This is the layer most agents miss.

When a user says "continue that", "not this, check the original", or "use
yesterday's one", they are usually asking the agent to recover a previous
worksite, not a long-term preference.

```json
{
  "id": "episode_...",
  "type": "task|conversation|correction|decision|failure|success",
  "subject": "last night's fable",
  "timeline": [
    "user asked for a fable",
    "agent wrote the ferry-man draft",
    "user corrected a setting",
    "task stopped at the next-chapter method"
  ],
  "participants": ["user", "agent"],
  "source_refs": ["raw_1", "raw_2"],
  "current_status": "open|done|wrong|superseded",
  "resume_hint": "when the user asks to continue the fable, first recover the original draft and correction",
  "last_good_output_ref": "raw_2",
  "last_correction_ref": "raw_3"
}
```

This layer solves cross-day continuation.

## L3 Structured Cognition

Structured memory is not a summary. It is a retrievable decision object.

```json
{
  "id": "mem_...",
  "object": "continuation recovery",
  "kind": "fact|skill|method|preference|relationship|identity|warning",
  "claim": "short continuation turns often refer to an existing worksite",
  "evidence_refs": ["episode_...", "feedback_..."],
  "use_when": [
    "the user message is low-detail",
    "it contains time reference, pronoun, correction, or continuation intent",
    "the current window lacks the old context"
  ],
  "do_next": "recover the old worksite before answering or acting",
  "confidence": 0.82,
  "freshness": "hot|recent|stable|stale",
  "scope": "global|project|person|chat|task",
  "contradictions": [],
  "last_validated_at": "2026-05-24T12:00:00"
}
```

The key fields are `use_when` and `do_next`. A claim without these fields is
hard to use safely.

## L4 Skill / Method Memory

Repeatedly useful structured cognition should become an executable skill.

```json
{
  "skill_name": "prior worksite recovery",
  "trigger": "the user uses a short turn, pronoun, time reference, or correction to continue prior work",
  "steps": [
    "classify whether this turn points to a prior worksite",
    "read task journal and raw conversation evidence",
    "find the last user correction and last good output",
    "recover object, version, stopping point, and unresolved work",
    "then answer or continue"
  ],
  "tests": [
    "continue yesterday's fable",
    "not this, check the original",
    "continue"
  ],
  "rollback": "disable the skill and keep ordinary retrieval"
}
```

The lesson from Hermes-style improvement is simple: useful memory must become
future behavior, not just another report.

## Retrieval Protocol

Retrieve by current intent, not by dumping everything.

```text
Detailed new request
  -> retrieve little old memory.

Short continuation / correction / time reference
  -> retrieve episode/worksite and raw evidence.

Preference / relationship / tone
  -> retrieve preference, identity, nourishment, feedback.

Code / ops / runtime state
  -> retrieve procedures, runtime ledger, recent failures.

Repeated failure or repeated user correction
  -> retrieve feedback_distill, dream_writeback, runtime_protocols.
```

If recalled memory does not change the current action, it should not enter the
prompt.

## Promotion Rules

| Layer | Capability | Promotion condition |
| --- | --- | --- |
| L0 raw evidence | inspect original text | automatic capture |
| L1 episode | resume prior work | source refs, timeline, boundary |
| L2 impression | bias attention | explicit or repeated short-term feedback |
| L3 structured cognition | bias judgment | evidence, scope, confidence |
| L4 skill/method | bias action | trigger, steps, tests, rollback |
| L5/L6 synthesis | bias architecture | repeated evidence, causal feedback, validated change |

The higher the layer, the more evidence it needs.

## Cleanup Rule

Clean memory systems by role, not by age.

- Raw evidence can be abundant, but it needs a unified index.
- Episode memory should be small and strong.
- Structured cognition needs schema.
- Skill memory needs trigger, steps, tests, and rollback.
- Dream reports must write back into runtime behavior.
- Old surfaces that only write but are never retrieved should become archive or
  be removed from the live path.

## GA Target

GenericAgent should converge toward:

```text
MemoryHub
  -> raw evidence readers
  -> episode/worksite recall
  -> structured cognition retrieval
  -> feedback and dream writeback
  -> runtime context pack
```

Do not delete old storage first. First route live retrieval through one hub,
then mark legacy surfaces, then migrate data, then remove unused code.
