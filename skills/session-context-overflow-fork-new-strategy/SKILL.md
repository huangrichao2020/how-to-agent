---
name: "session-context-overflow-fork-new-strategy"
description: "This skill should be used when the conversation is approaching the context window limit and the user wants to start a fresh, low-token session without losing the main goal and task, including requests like 上下文快满了 fork 一个新会话, compress history then fork, reduce token waste but keep the main objective, escape Prompt is too long / context_length_exceeded by branching, or carry a compacted summary into a new session via /fork2 or /branch."
---

# Context-Overflow Fork Strategy

Use this skill when the current session's context is near the window limit and the goal is to continue work in a **new, much smaller session** that keeps the main objective and task thread but drops accumulated token waste.

This is a **composition strategy**, not new machinery. Reuse the existing fork engine, compaction summary, and context-budget signals. Do not build a parallel cloning or summarization path.

## When To Use

- Context usage is high (e.g. user sees a high ctx% in `/context-map` or `/token-budget`, or hits "Prompt is too long" / `context_length_exceeded`).
- The user says things like: 上下文快满了 / fork 一个干净的新会话 / 压缩历史再继续 / 保留主干目标但减少 token。
- The work has a clear main goal but a long, noisy tail (large tool outputs, exploration, dead ends).

## When NOT To Use

- Plain in-place compaction is enough and the user wants to stay in the same session → use `/compact` (see `compact-lifecycle-reuse`).
- The user wants a full, lossless copy of the conversation → use `/branch` (full-session fork).
- The user only wants the last few rounds, not the whole goal → use `/fork2` / `/fork3` directly (see `session-fork-engine-reuse`).

## Core Idea

Combine three existing capabilities into one manual flow:

```
1. Compact the trunk     → structured summary (user goal, facts, open questions)
2. Fork into new session → fresh session, low token baseline
3. Resume into the fork  → keep working, original stays recoverable
```

The summary preserves the main goal; the fork drops the token-heavy tail; the original session remains resumable as a safety net.

## Reuse Map (verify before relying)

- Context budget / usage signal
  - `src/services/compact/contextBudget.ts` — token budget estimation against `getContextWindowForModel()`.
  - `src/services/compact/autoCompact.ts` — threshold logic for "near full".
  - `src/utils/context.ts` — `getContextWindowForModel()` is the single source of truth for window size (including small third-party windows and Codex model-level windows). Trust this over hardcoded numbers.
  - User-facing surfaces: `/context-map`, `/token-budget`.

- Trunk summary (the part that preserves the goal)
  - `src/services/compact/compact.ts` — `compactConversation()` returns `CompactionResult` with `summaryMessages`, `messagesToKeep`, `boundaryMarker`, and pre/post token counts.
  - `src/commands/compact/compact.ts` — reference for how `/compact` orchestrates summary + `setMessages`.
  - The summary is structured around: user goal, established facts, disproved hypotheses, open questions. This is exactly the "main trunk" to carry forward.

- Fork into a new low-token session
  - `src/commands/branch/forkEngine.ts` — `createFork()`, `takeLastRounds()`, `deriveFirstPrompt()`, `getUniqueForkName()`.
  - `src/commands/branch/forkRecentCommand.ts` — `runRecentForkCommand()` shared partial-fork command path used by `/fork2`, `/fork3`.
  - Invariants (new sessionId, parent-chain reset, `forkedFrom` provenance, content-replacement carry-forward, `context.resume`) are documented in `session-fork-engine-reuse` — follow them; do not reinvent.

## Manual Workflow (trigger: manual, user-initiated)

Default thresholds are advisory; the user decides when to act.

1. **Check usage**: run `/context-map` (or `/token-budget`). Treat ~70% as "plan a fork soon", ~85% as "fork now before forced overflow".
2. **Compact the trunk in place first**: run `/compact`. This produces the structured goal/facts/open-questions summary and trims the token-heavy tail.
3. **Fork the compacted state into a fresh session**:
   - If the compacted history is already short, `/fork2` (last 2 rounds) or `/fork3` (last 3 rounds) usually captures the summary message plus the active thread, because the compact summary becomes the surviving lead message.
   - For a wider safety margin, `/fork2 --last N` to include more of the compacted rounds.
4. **Resume into the fork**: the fork commands auto-resume; the new session starts at a low token baseline carrying the goal summary.
5. **Original stays recoverable**: the fork command prints `claude -r <originalSessionId>`. Keep it until the new session is confirmed healthy.

### Why compact-then-fork (ordering matters)

- Compacting first means the surviving rounds already contain the structured goal summary, so the partial fork carries the trunk, not raw noise.
- Forking first then compacting would copy the token-heavy tail into the new session before shrinking it — more waste, weaker goal preservation.

## Design Rules

- Manual-first: do not auto-execute a destructive fork. Surface usage and recommend; let the user run it.
- Reuse `compactConversation()` for the summary and `forkEngine` for the clone. Never hand-roll a "summarize + copy messages" path.
- Preserve the main goal explicitly: the carried-forward content must include the compact summary's user-goal / open-questions section, not just the last user message.
- Keep the original session resumable; never delete the source transcript as part of this flow.
- Respect user naming: forked session titles still go through `getUniqueForkName()` / `saveCustomTitle()` (suffix like `(Fork2)`).
- Trust `getContextWindowForModel()` for thresholds; do not assume 200K. Small third-party windows and Codex 1M windows both flow through it.

## If This Graduates To A Command

If a future task wants a one-shot `/forkc` (compact-then-fork) command:

- Build it as a thin wrapper that calls `compactConversation()` then `runRecentForkCommand()` (or `createFork({ lastRounds })`), following `session-fork-engine-reuse` invariants and `slash-command-creation-reuse` registration steps.
- Do not duplicate transcript cloning or summarization logic; orchestrate the existing pieces.
- Verify the real path: `bun test src/commands/branch/forkEngine.test.ts`, `bun run dev:restore-check`, then a live run that forks a long session and confirms the new session's token baseline drops while the goal summary survives.

## Related Skills

- `session-fork-engine-reuse` — fork engine internals and invariants.
- `compact-lifecycle-reuse` — compaction hooks, thresholds, and overflow recovery.
- `slash-command-creation-reuse` — if this ever becomes a slash command.
