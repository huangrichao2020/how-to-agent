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
runtime tree:    /Users/tingchi/hermes-new/hermes-agent
Hermes home:     /Users/tingchi/hermes-new/.hermes
how-to-agent:    /Users/tingchi/Desktop/how-to-agent
```

The source checkout is the git repository for reading, editing, testing, committing, and pushing.

The runtime tree is what the gateway currently loads. It may not be a git repository, so do not treat it as the only source of truth.

## Workflow

```text
1. cd into the source checkout
2. inspect git status, branch, remote, and HEAD
3. locate the relevant runtime code
4. make a small change
5. run focused compile/tests/smoke checks
6. run git diff --check
7. commit and push
8. sync verified files to the runtime tree
9. restart ai.hermes.gateway with launchctl
10. verify with hermesd health
11. report what changed, what was verified, and current runtime status
```

## Agency

Hermes may proactively manage its own source when doing so improves stability, memory, output quality, learning, or user experience. Keep evidence and rollback paths visible.

Explain high-impact changes before they land: wide refactors, memory/persona/system prompt changes, data deletion, external-platform risk, privacy risk, or irreversible operations.

## Report

Every self-source change report should include:

- source path and commit;
- files synced to runtime;
- compile/test/health result;
- gateway PID and connected platforms;
- remaining risk, if any.
