# Example 06: Handoff-First Local Maintenance

[English](06-handoff-first-local-maintenance.md) · [简体中文](06-handoff-first-local-maintenance.zh-CN.md)

Some agent improvements are not new runtime features. They are local state
hygiene: sessions, logs, worktrees, caches, and metadata slowly grow until the
agent feels slow or fragile.

The useful lesson from `keep-codex-fast` is not "delete old data." It is:

> Make handoffs first. Archive, do not delete. Apply only after a safe report.

## Source Studied

- `keep-codex-fast`: https://github.com/vibeforge1111/keep-codex-fast
- `heat-on-content`: unresolved by exact public GitHub and npm searches during
  this pass. Treat it as an unknown source until the user provides a link.

The second line matters. A learning agent should preserve uncertainty instead
of inventing a pattern from a name.

## Developer Intent

The user wanted the agent to study external projects, but clarified that the
main target was the agent's own learning.

That changes the output shape:

- do not clone the project into the local runtime
- do not install a cleanup tool by default
- extract the operating habit
- write the habit into the capability library
- keep unresolved sources visible

## What The Agent Should Learn

### 1. Report Before Mutating

The first pass should be inspect-only.

For local agent state, a report should answer:

- how large the active session store is
- which sessions or logs dominate the size
- whether stale worktrees exist
- whether old runtime metadata is bloated
- whether config paths point at missing locations
- whether live agent or dev processes are still running

The report is the decision surface. It is not a prelude to automatic cleanup.

### 2. Handoff Before Archive

Old active chats may still contain useful project state. Before moving them
out of the hot path, write a short handoff:

- project or task name
- current status
- important files and branches
- commands that verified the state
- open risks
- a reactivation prompt for a future agent

If a conversation has no handoff, archiving it may make the next agent faster
but less capable.

### 3. Back Up Before Apply

Mutating local agent state should require a backup and an obvious restore path.

Prefer:

- timestamped backup directories
- manifests describing every moved file
- restore scripts or exact restore commands
- a post-apply verification report

Avoid:

- deletion as the first cleanup move
- mutating live state while the agent app is running
- silent metadata repair
- cleaning credentials, tokens, or private config unless explicitly requested

### 4. Archive, Move, Or Rotate Instead Of Delete

Cleanup should reduce hot-path load while preserving history.

Good moves:

- move old sessions to an archive area
- move stale worktrees out of active discovery paths
- rotate logs with manifests
- prune only clearly dead generated or derived files

Deletion should be rare, explicit, and reversible in practice.

### 5. Metadata Repair Is A Separate Permission

Some slowness can come from oversized local display metadata, such as thread
title or preview fields. Repairing that metadata is not the same as deleting a
transcript, but it still changes agent-owned state.

Treat it as an optional repair step:

- explain what metadata will be trimmed
- say that transcripts remain intact
- back up first
- ask for explicit approval

### 6. Recurrence Should Default To Reports

A weekly or biweekly maintenance reminder is useful. Automatic mutating
cleanup is much riskier.

The safe default is:

```text
Run an inspect-only local state maintenance report.
Summarize what is large, stale, risky, or safe to archive.
Do not move, delete, trim, or repair anything unless I explicitly approve it.
```

## Reusable Version

```text
Study [local-state maintenance project].

Extract the operating habit, not the tool implementation.

For our agent, turn the lesson into a handoff-first maintenance workflow:
inspect-only report first, then handoffs for old active work, then backup,
then archive or rotate instead of delete, then post-apply verification.

If metadata repair is suggested, separate it from normal maintenance and ask
for explicit approval.

If any named source cannot be resolved, record exactly that uncertainty and do
not invent lessons from the name.
```

## Completion Test

The lesson is learned only when the next agent can answer:

- Where is the maintenance skill?
- What is the default non-mutating command or workflow?
- What must be backed up before apply?
- Which work needs a handoff before archive?
- Which source was unresolved and needs a link?

If those answers live only in chat, the agent has not learned it yet.
