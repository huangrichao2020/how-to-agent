---
name: hermes-source-management
description: "Teach Hermes on M1 to manage its own source checkout, runtime sync, tests, restart, and reports."
version: 1.0.0
---

# Hermes Source Management

Use this skill when Hermes needs to inspect, repair, upgrade, or explain its own source code on the M1 host.

## Paths

```text
source checkout: /Users/tingchi/Desktop/hermes-agent
runtime tree:    /Users/tingchi/Desktop/hermes-agent
Hermes home:     /Users/tingchi/hermes-new/.hermes
how-to-agent:    /Users/tingchi/Desktop/how-to-agent
```

The source checkout is the git repository for reading, editing, testing, committing, and pushing.

The gateway runs directly from the source checkout. The old
`hermes-new/hermes-agent` code path should not exist as a second tree or
symlink. Keep only `HERMES_HOME` under `hermes-new` for runtime state.

## Git Sync Rule

The M1 `hermes-agent`, `how-to-agent`, `agent-systems-patterns`, and
`GenericAgent` checkouts all have GitHub remotes. Synchronize git checkouts with
git first:

1. Commit and push from the checkout where the edit was made.
2. Fetch/pull on the other host or checkout.
3. Verify branch, HEAD, and clean status.
4. Sync files into a non-git live runtime tree only when such a tree really
   exists.

Do not use rsync/scp as the normal sync path between two git checkouts that
share a remote. File sync is for live runtime trees, emergency recovery, or
assets without a git source of truth.

## Workflow

```text
1. cd into the source checkout
2. inspect git status, branch, remote, and HEAD
3. locate the relevant runtime code
4. make a small change
5. run focused compile/tests/smoke checks
6. run git diff --check
7. commit and push
8. if runtime is a separate non-git tree, sync verified files to it
9. restart ai.hermes.gateway with launchctl
10. verify with hermesd health
11. update the work manual or handoff manual with paths, commands, validation, rollback, and residual risks
12. report what changed, what was verified, and current runtime status
```

## Agency

Hermes may proactively manage its own source when doing so improves stability, memory, output quality, learning, or user experience. Keep evidence and rollback paths visible.

Explain high-impact changes before they land: wide refactors, memory/persona/system prompt changes, data deletion, external-platform risk, privacy risk, or irreversible operations.

## Report

Every self-source change report should include:

- source path and commit;
- files synced to runtime, or confirmation that runtime is the source checkout;
- compile/test/health result;
- gateway PID and connected platforms;
- manual or handoff page updated, or why none was needed;
- remaining risk, if any.
