# Example 12: Runtime Identity Correction

Agents that move between machines can keep thinking from the old machine.
That is dangerous because environment memories feel like facts: operating
system, network shape, package mirrors, service paths, and restart commands.
Once stale, they quietly poison tool choice and debugging.

This example comes from a Hermes migration: Hermes had already moved from an
Alibaba Cloud server to an M1 Mac, but its active memory still said:

```text
Server: Alibaba Cloud Linux 3, 2GB RAM
Network: Alibaba Cloud in China, Google API unreachable, curl timeout
pip mirror: mirrors.aliyun.com
```

The runtime was healthy on the M1, but the agent kept reasoning as if it still
lived on Aliyun. The fix was not a prompt reminder. The fix was to update every
active self-knowledge source that the agent could retrieve.

## Principle

Current runtime facts outrank historical environment memories.

When an agent changes host, workspace, network, platform account, or execution
model, do a self-identity correction pass before trusting old operational
memories.

## What To Correct

Check the sources that can be injected into the agent loop:

- Active semantic memory, such as `.agent/memory/semantic/lessons.jsonl`.
- Rendered memory views, such as `LESSONS.md`.
- Wiki or gbrain self pages, such as `entities/hermes-agent.md`.
- Operating manuals, handoff docs, and generated workbooks.
- Runtime prompt/context assembler inputs.
- Recent caches that may preserve the old conclusion.

Do not rewrite immutable audit logs or old sessions. They are historical
evidence. Only correct the active sources that influence future reasoning.

## Correction Shape

Use explicit contrast:

```text
Current runtime: M1 Mac / macOS / arm64 / 8GB RAM.
Historical Aliyun server: accessible via ssh aliyun, but not the current host.
Network rule: check the M1 local network and proxy first. Use Aliyun network
experience only when the task explicitly targets ssh aliyun or ssh aliyun2.
```

The contrast matters. If you only add "now on M1" while leaving "Aliyun cannot
reach Google API" nearby, retrieval can still mix both and produce confused
reasoning.

## Playbook

```text
1. Verify the real runtime facts from the machine itself.
2. Search active memory/wiki/manual sources for old host assumptions.
3. Replace stale current-environment claims with current facts.
4. Reframe old environment knowledge as historical and scoped.
5. Add one strong correction memory that names when old knowledge applies.
6. Move scratch backups outside active retrieval paths.
7. Restart the gateway or runtime so cached context is cleared.
8. Re-search active sources for stale terms before declaring done.
```

## Good Output

```text
Hermes currently runs on M1 Mac. Network problems must be diagnosed from the
M1 local network and Fastlink/proxy state first.

Aliyun network notes are historical. Use them only when the task explicitly
targets ssh aliyun or ssh aliyun2.
```

## Bad Output

```text
Hermes runs on M1 now, but Alibaba Cloud cannot reach Google API.
```

This is bad because it keeps the stale fact unscoped. The next retrieval can
still turn it into a current constraint.

## Why This Belongs In Cognition

Self-knowledge is not decoration. It is part of the agent's action policy.
If self-knowledge is stale, the agent will choose the wrong commands, wrong
network assumptions, wrong performance budget, and wrong recovery path.

Cognitive architecture should maintain memory, methods, skills, impressions,
and persona. Runtime identity is the foundation under all five.
