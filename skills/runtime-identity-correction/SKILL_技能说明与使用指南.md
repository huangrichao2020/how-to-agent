---
name: runtime-identity-correction
description: Correct stale agent self-knowledge after host, network, workspace, or platform migration.
---

# Runtime Identity Correction

Use this skill when an agent reasons from an old machine or old deployment
context, for example:

- It mentions Aliyun, VPS, Linux, 2GB RAM, old package mirrors, or old network
  limits after moving to a Mac or another host.
- It uses old service paths, restart commands, process managers, or account
  names.
- It keeps diagnosing current failures with historical constraints.

## Core Rule

Current runtime facts outrank historical environment memories.

Do not fix this with a one-line prompt reminder. Fix the active self-knowledge
sources that the runtime can retrieve.

## Steps

1. Verify facts from the current machine:
   - hostname
   - OS and architecture
   - memory budget
   - active workspace paths
   - gateway/service manager
   - network/proxy state

2. Search active injection sources:
   - `.agent/memory/semantic/lessons.jsonl`
   - rendered files like `LESSONS.md`
   - wiki/gbrain self pages
   - operating manuals and handoff docs
   - runtime prompt/context assembler inputs
   - recent cache files if the bug persists

3. Replace stale current-environment claims.

4. Re-scope old facts as historical:

   ```text
   This applies only when operating the old remote host via ssh <host>.
   It is not a current runtime constraint.
   ```

5. Add one strong correction memory that says:
   - where the agent currently runs
   - what must be checked first
   - exactly when old environment knowledge applies

6. Keep immutable history intact:
   - Do not edit old audit logs.
   - Do not rewrite historical sessions.
   - Do not delete evidence unless the user explicitly asks.

7. Move scratch backups out of active retrieval paths.

8. Restart the gateway/runtime if context may already be loaded.

9. Re-search for stale phrases before declaring done.

## Stale Phrase Examples

- `Alibaba Cloud Linux`
- `2GB RAM`
- `mirrors.aliyun.com`
- `Google API unreachable`
- `curl timeout`
- old `/root/...` paths after moving to `/Users/...`
- old `systemctl` restart instructions after moving to `launchctl`

## Done Condition

The active memory/wiki/manual sources should state the current runtime clearly,
and old environment knowledge should be explicitly scoped to the old host.
