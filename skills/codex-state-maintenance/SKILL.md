---
name: codex-state-maintenance
description: Use when Codex or a local coding agent feels slow, bloated, or hard to resume because sessions, logs, worktrees, metadata, or config paths have grown stale. Also use when adapting local-state maintenance ideas such as keep-codex-fast.
---

# Codex State Maintenance

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md)

Use this skill to keep local agent state fast, recoverable, and easy for the
next agent to understand.

The principle is:

```text
Inspect first. Handoff before archive. Back up before apply. Archive instead
of delete.
```

## When To Use

Use this skill when:

- Codex or another local agent feels slow to start or search.
- Active sessions, logs, worktrees, caches, or metadata have grown large.
- The user asks to clean, archive, compact, speed up, or repair local agent
  state.
- You are studying a maintenance project such as `keep-codex-fast` and need to
  turn the lesson into local operating behavior.

Do not use it as permission to mutate local state immediately.

## Default Workflow

### 1. Start Inspect-Only

The first run is always a report.

Check and summarize:

- active and archived session sizes
- largest sessions or logs
- stale worktrees
- old generated caches
- oversized thread metadata
- config entries pointing at missing paths
- live Codex, agent, editor, or dev-server processes

Do not move, delete, trim, or repair anything in this step.

### 2. Identify Work That Needs Handoff

Before archiving old active work, create or update a handoff note when the
conversation still contains useful state.

A handoff should include:

- project path
- branch and git status
- current goal
- what was already verified
- remaining risks
- exact reactivation prompt

If you cannot write a useful handoff, do not archive that work silently.

### 3. Ask Before Mutating Agent-Owned State

Before applying changes, show:

```text
I can apply local state maintenance now.

Planned changes:
- ...

Backup:
- ...

Rollback:
- ...

Will not touch:
- credentials, tokens, private config, transcripts not listed above

Do you approve?
```

Do not treat vague continuation as approval.

### 4. Back Up Before Apply

Before any write:

- create a timestamped backup
- record a manifest of moved or changed files
- write restore commands or a restore script
- avoid applying while Codex or the target agent is actively writing state

If the agent app is running, prefer to stop at the report and tell the user
what needs to be closed before apply.

### 5. Archive Or Rotate Instead Of Delete

Prefer reversible operations:

- move old sessions to archive
- move stale worktrees out of active search paths
- rotate large logs
- prune generated caches only when clearly safe

Deletion requires explicit user approval and a clear explanation of what will
be lost.

### 6. Treat Metadata Repair Separately

Metadata repair, such as trimming oversized title or preview fields, is not
normal cleanup.

Before doing it:

- explain the exact metadata affected
- say whether transcripts remain intact
- back up the database or state file first
- request explicit approval for this repair step

## Recurring Maintenance

For recurring jobs, default to report-only:

```text
Run an inspect-only local agent state maintenance report.
Summarize large, stale, risky, and safe-to-archive items.
Do not move, delete, trim, or repair anything unless the user explicitly
approved that mutation for this run.
```

Avoid scheduling automatic mutating cleanup unless the user clearly asks for
that risk.

## Unknown Sources

If the user names an external project and you cannot resolve it:

- record the exact names searched
- say which registries or hosts were checked
- do not infer a lesson from the name alone
- ask for a link when the source matters

## Completion Checklist

Before saying the task is complete:

- inspect-only report was produced or a reason is given
- handoff-needed work was identified
- no mutation happened without approval
- backup and restore path exist for any apply step
- changed files or archives are listed
- post-apply verification was run when changes were made
- unresolved external sources are marked as unresolved
