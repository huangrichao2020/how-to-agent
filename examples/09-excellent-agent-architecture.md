# Example 08: Excellent Agent Architecture

[English](09-excellent-agent-architecture.md) · [简体中文](09-excellent-agent-architecture.zh-CN.md)

Use this when a conversation produces reusable architecture taste, not just a
patch.

## Original Prompt

```text
你把今天的心得，把你心目中的优秀架构，更新到桌面的 how-to-agent
```

## Developer Intent

The prompt asks the agent to turn the day's operational experience into a
portable architecture principle. It is not asking for a diary. It is asking
for a standard the next agent can inherit.

In today's work, several patterns became concrete:

- A Feishu integration should not keep editing one rich-text message forever.
  Long tasks need separate streams for reasoning/status and final conclusions.
- Self-evolution should be governed by proposals, evidence, risk levels,
  validation, and rollback, not by silent self-modification.
- Old records should move into cold archives once their lessons have landed.
  Archives remain searchable, but they should not pollute active memory.
- Dependency security work should be grouped by runtime risk, verified, and
  pushed only after the live service is healthy again.
- The source of truth is the running system plus the current repo, not memory
  or a pleasant summary.

## Architecture Taste

An excellent agent architecture feels calm under pressure. It does not become
clever by adding more loops everywhere. It becomes reliable by giving each kind
of state, output, and authority a proper home.

```text
                 User intent
                     |
                     v
              Interaction layer
      Feishu / CLI / Web / scheduled runs
      - accepts input
      - renders output
      - never owns core truth
                     |
                     v
                Runtime core
      planner · tool router · permission boundary
      memory loader · model dispatcher · verifier
      - owns execution state
      - calls tools through one policy gate
                     |
        +------------+-------------+
        |                          |
        v                          v
   Knowledge plane             Execution plane
   active facts                tools / shell / browser
   skills                      subagents / external CLIs
   archives                    service restarts
   evaluations                 deploys
        |                          |
        +------------+-------------+
                     |
                     v
             Evidence and closure
      tests · logs · status · commit · handoff
```

## The Six Separations

### 1. Separate Streams

Do not treat a platform message as the agent's whole brain.

For long Feishu or chat tasks, split output into at least two streams:

- **Progress stream**: short status, tool milestones, recoverable failures.
- **Conclusion stream**: final answer, evidence, links, next actions.

For very long tasks, add an append-only event trail or artifact. Editing one
rich-text message for every thought eventually hits platform limits and makes
the work brittle.

### 2. Separate Authority

Memory is not authority by itself.

Use different surfaces for different truth levels:

- **Current facts**: small, active, loaded by default.
- **Procedures and skills**: reusable behavior, versioned and reviewed.
- **Session history**: searchable evidence, not default instruction memory.
- **Cold archives**: old records, loaded only when needed.

When a skill change lands, the old proposal and raw logs become history. They
should stay discoverable, but they should not keep steering daily behavior.

### 3. Separate Evolution From Execution

Self-improvement should run through a ratchet:

```text
observation
  -> proposal
  -> evidence
  -> risk classification
  -> validation plan
  -> rollback plan
  -> apply gate
  -> post-change audit
```

Low-risk improvements can be automated after authorization. High-risk changes
such as deletion, credentials, deployment, payment, shell policy, or tool
permission changes need an explicit human gate.

### 4. Separate Core Path From Sidecars

There should be one primary runtime path. Sidecars are useful only when they
are bounded and fail-soft.

Good sidecars:

- telemetry that can fail without blocking the answer
- archives that compact old records without changing active memory
- audits that report risk without silently rewriting runtime policy
- subagents with narrow ownership and reviewable outputs

Bad sidecars become hidden second runtimes.

### 5. Separate Dependency Hygiene From Feature Work

Dependency alerts are operational work, not random chores.

Handle them by blast radius:

1. Patch runtime dependencies first.
2. Patch optional bridges next.
3. Patch docs or website dependencies last.
4. Verify each group with the closest available test.
5. Restart live services only when the runtime environment changed.
6. Recheck GitHub alerts, but distinguish scanner lag from unfixed code.

This keeps security work from becoming a broad upgrade adventure.

### 6. Separate Completion From Confidence

The task is not done when code changes. It is done when the system proves it:

- repository state is known
- tests or focused checks passed
- live service state is healthy
- user-facing channel recovered
- commit and push are complete if requested
- unrelated dirty files were not absorbed
- the next agent can find the method

## Reusable Prompt

```text
Take today's work and extract the architecture lesson.

Do not write a diary. Write a reusable method that future agents can apply.

Cover:
- what the system was trying to solve
- what an excellent architecture would separate
- where active memory ends and archive begins
- how self-evolution is governed
- how long-running channel output should be streamed
- how live verification closes the loop

Add it to how-to-agent in the existing examples style.
Update the indexes, and avoid storing private logs, tokens, or raw transcripts.
```

## Acceptance Check

- The lesson is reusable outside the original conversation.
- It distinguishes active memory from archived history.
- It names runtime, knowledge, execution, and channel boundaries.
- It includes validation and rollback thinking.
- It does not leak private logs or credentials.
- README indexes point to the new artifact.
