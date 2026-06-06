---
name: "session-context-overflow-fork-new-strategy"
description: "This skill should be used when the user wants to open a new session window and continue work because the conversation is approaching the context window limit, without losing the main goal and next steps. Trigger phrases include 开启新窗口 / 开一个新会话 / fork 一个新的会话 / fork 一个干净的新会话 / 上下文快满了 / token 太多了 / 上下文要爆了 / 换个新会话继续 / 压缩历史再继续 / 保留主线需求开新会话, and English variants like open a new session window, fork a new session, start a fresh chat, context window almost full, too many tokens, compress history then fork, reduce token waste but keep the main objective, escape Prompt is too long / context_length_exceeded by branching, or carry a compacted summary (main goal + next steps) into a new session via /compact then /fork2 / /fork3 / /branch."
---

# Context-Overflow Fork Strategy

Use this skill when the current session's context is near the window limit and the goal is to continue work in a **new, much smaller session** that keeps the main objective and task thread but drops accumulated token waste.

This is a **composition strategy**, not new machinery. Reuse the existing fork engine, compaction summary, and context-budget signals. Do not build a parallel cloning or summarization path.

## When To Use

- Context usage is high (e.g. user sees a high ctx% in `/context-map` or `/token-budget`, or hits "Prompt is too long" / `context_length_exceeded`).
- The work has a clear main goal but a long, noisy tail (large tool outputs, exploration, dead ends).

### Trigger Keywords (举一反三：覆盖同义说法)

Match these and structurally similar phrasings, not only the exact sentence:

- 中文：开启新窗口 / 开一个新窗口 / 开个新会话 / fork 一个新的会话 / fork 一个干净的新会话 / 复制一份新会话继续 / 上下文快满了 / 上下文要爆了 / 上下文不够了 / token 太多了 / token 浪费 / 历史太长了 / 压缩历史再继续 / 总结一下从新会话继续 / 保留主线需求开新会话 / 带着目标开新会话。
- English: open a new session window / open a new chat / fork a new session / start a fresh session / branch into a clean session / context window almost full / running out of context / too many tokens / history too long / compress history then fork / summarize then continue in a new session / keep the main objective and start fresh.

These map to the same intent: **shrink token usage by moving to a new session while preserving the main goal and the next steps.**

## When NOT To Use

- Plain in-place compaction is enough and the user wants to stay in the same session → use `/compact` (see `compact-lifecycle-reuse`).
- The user wants a full, lossless copy of the conversation → use `/branch` (full-session fork).
- The user only wants the last few rounds, not the whole goal → use `/fork2` / `/fork3` directly (see `session-fork-engine-reuse`).

## Core Idea

Carry the **main line** (原始目的/主线需求 + 下一步) across a session boundary while dropping the token-heavy tail:

```
1. Summarize the main line   → 主线需求(原始目的) + established facts + 下一步要做什么(next steps)
2. Fork into a new session   → fresh session, low token baseline, summary travels with it
3. Resume into the fork      → continue from "下一步", original session stays recoverable
```

The summary is the contract: it must capture **why the work started (主线需求)** and **what to do next (next steps)**, not just the last message. The fork drops accumulated noise; the original session remains resumable as a safety net.

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

1. **Check usage**: run `/context-map` (or `/token-budget`). The percentages below are illustrative user-facing guidance, not constants — for the authoritative "near full" boundary, cross-check `autoCompact.ts` against `getContextWindowForModel()`. As a rough rule of thumb, ~70% means "plan a fork soon" and ~85% means "fork now before forced overflow".
2. **Summarize the handoff explicitly before forking**. The handoff summary must be small but operational:
   - 原始目的 / 主线需求: why this session exists and what outcome matters.
   - 已确认事实: decisions, constraints, files/commands already proven, and rejected hypotheses.
   - 当前状态: what has been completed, what remains unverified, blockers/risks.
   - 下一步要做什么: the immediate next action(s), ordered and concrete.
   - 恢复锚点: original session id / commit id / important file paths if relevant.
3. **Use `/compact` when the current history is noisy**. `/compact` produces a structured goal/facts/open-questions summary and trims the token-heavy tail. If the generated compact summary misses the original purpose or next step, add a short explicit handoff note before forking.
4. **Fork the compacted/handoff state into a fresh session**:
   - If the compacted history is already short, `/fork2` (last 2 rounds) or `/fork3` (last 3 rounds) usually captures the summary plus the active thread.
   - But `takeLastRounds()` counts **real user rounds** (`type==='user' && !tool_result`), not post-compact message position. After forking, confirm the new session's lead messages actually contain the handoff summary (main goal + next steps), not just the last prompt.
   - If the handoff summary did not survive, widen with `/fork2 --last N` or `/fork3 --last N` and re-check.
5. **Resume into the fork**: the fork commands auto-resume; the new session starts at a low token baseline carrying the goal summary and next-step plan.
6. **Original stays recoverable**: the fork command prints `claude -r <originalSessionId>`. Keep it until the new session is confirmed healthy.

### Why summarize/compact-then-fork (ordering matters)

- The new session is only as good as the handoff content it receives. Summarize the main line first so the fork carries intent, constraints, and next steps instead of raw noise.
- Compacting first means the surviving rounds are much smaller and more likely to contain the structured goal summary.
- Forking first then compacting copies the token-heavy tail into the new session before shrinking it — more waste, weaker goal preservation, and a higher chance of losing the original purpose.

## Design Rules

- Manual-first: do not auto-execute a destructive fork. Surface usage and recommend; let the user run it.
- Reuse `compactConversation()` for machine-generated summaries and `forkEngine` for the clone. Never hand-roll a "summarize + copy messages" path.
- Preserve the main goal explicitly: the carried-forward content must include the original purpose / main requirement, established facts, open questions, and concrete next steps — not just the last user message.
- Treat the handoff summary as a checklist: if any of 主线需求、当前状态、下一步 is missing, add a short explicit note before forking.
- Verify the fork, not just command success: after resume, confirm the new session can answer "what are we trying to do and what is next?" from its own context.
- Keep the original session resumable; never delete the source transcript as part of this flow.
- Respect user naming: forked session titles still go through `getUniqueForkName()` / `saveCustomTitle()` (suffix like `(Fork2)`).
- Trust `getContextWindowForModel()` for thresholds; do not assume 200K. Small third-party windows and Codex 1M windows both flow through it.

## Handoff Summary Template

Use or adapt this compact handoff note before forking when the automatic compact summary is not obviously enough:

```markdown
## Session Handoff Summary

- 主线需求 / Original goal: <the user's original purpose and success criteria>
- 已完成 / Done: <completed work, important decisions, verified facts>
- 当前状态 / Current state: <where the task stands now, relevant files/commands/session ids>
- 未解决 / Open questions: <unknowns, blockers, rejected paths if important>
- 下一步 / Next steps: <ordered concrete actions for the new session>
- 恢复锚点 / Recovery anchors: <original session id, commit id, branch, docs, issue links>
```

Keep it short enough to save tokens, but complete enough that a fresh session can continue without rereading the old transcript.

## If This Graduates To A Command

If a future task wants a one-shot `/forkc` (compact-then-fork) command:

- Build it as a thin wrapper that calls `compactConversation()` then `runRecentForkCommand()` (or `createFork({ lastRounds })`), following `session-fork-engine-reuse` invariants and `slash-command-creation-reuse` registration steps.
- Do not duplicate transcript cloning or summarization logic; orchestrate the existing pieces.
- Verify the real path: `bun test src/commands/branch/forkEngine.test.ts`, `bun run dev:restore-check`, then a live run that forks a long session and confirms the new session's token baseline drops while the goal summary survives.

## Related Skills

- `session-fork-engine-reuse` — fork engine internals and invariants.
- `compact-lifecycle-reuse` — compaction hooks, thresholds, and overflow recovery.
- `slash-command-creation-reuse` — if this ever becomes a slash command.
