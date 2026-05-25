---
name: agent-memory-store-retrieve-loop
description: Use when designing, cleaning up, or refactoring an agent memory system across raw evidence, episode/worksite recall, structured cognition, skill promotion, dream writeback, and runtime retrieval.
---

# Agent Memory Store-Retrieve Loop

Use this skill when memory has become a pile of storage surfaces instead of a
single store-retrieve loop.

Core rule:

```text
Without a retrieval protocol, memory is a warehouse, not a mind.
```

## Layers

```text
L0 raw evidence
-> L1 episode/worksite
-> L2 impression/feedback
-> L3 structured cognition
-> L4 skill/method
-> dream consolidation
-> runtime retrieval
```

## Every Memory Must Answer

- Why store this?
- Which layer owns it?
- When should it be recalled?
- What should the agent do differently after recalling it?

If the last answer is unclear, do not inject the memory into the prompt.

## Schema Principles

### L0 Raw Evidence

Keep `time/source/actor/scope/text/attachments/links/hash`.

Do not interpret.

### L1 Episode / Worksite

Keep `type/subject/timeline/source_refs/current_status/resume_hint/last_good_output_ref/last_correction_ref`.

Use this for cross-day continuation, original-text recovery, and prior task
resumption.

### L3 Structured Cognition

Keep `object/kind/claim/evidence_refs/use_when/do_next/confidence/freshness/scope/contradictions/last_validated_at`.

The important fields are `use_when` and `do_next`.

### L4 Skill / Method

Keep `skill_name/trigger/steps/tests/rollback`.

Stable lessons must become executable, testable, and reversible.

## Retrieval Protocol

- Detailed new request: retrieve little old memory.
- Short continuation, correction, time reference: retrieve episode/worksite and raw evidence.
- Preference, relationship, tone: retrieve preference, identity, nourishment, feedback.
- Code, ops, runtime state: retrieve procedures, runtime ledger, recent failures.
- Repeated failure: retrieve feedback_distill, dream_writeback, runtime_protocols.

## Cleanup Rule

Clean by role, not age.

- Write-only surfaces become archive or lose live writes.
- Duplicate retrieval surfaces go through one MemoryHub.
- Long-term cognition without schema must migrate to structured memory.
- Skills without trigger, tests, and rollback are notes, not runtime skills.
- Dream reports that do not write back into runtime are reports, not cultivation.

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

First route live retrieval through one hub. Then mark legacy surfaces. Then
migrate data. Then remove unused code.

## References

- `../../examples/36-agent-memory-store-retrieve-loop.md`
- `../agent-brain-architecture/`
- `../agent-anti-bloat-context-engineering/`
- `../agent-attention-governance/`
