---
name: production-agent-runtime
description: When running an agent as a persistent, production-grade assistant with physical execution capabilities (file I/O, script execution, browser automation, system intervention). Covers architecture, memory layering, delegation, failure escalation, and self-healing.
---

# Production Agent Runtime

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md)

This skill captures patterns from running GenericAgent (GA) and Hermes as persistent, physically-capable agents on a developer's machine. It covers the three-layer architecture, layered memory, federation delegation, failure escalation, and self-healing protocols.

## Core Architecture

A production agent should separate concerns into three layers:

```
┌─────────────────────────────────────────────────────┐
│                 Interaction Layer                    │
│  Chat frontend / CLI / Web / Scheduled tasks          │
└──────────────────────┬──────────────────────────────┘
┌──────────────────────▼──────────────────────────────┐
│                   Core Engine                        │
│  Tool router · History manager · Memory manager      │
│  LLM dispatcher · Safety guardrails                  │
└──────────────────────┬──────────────────────────────┘
┌──────────────────────▼──────────────────────────────┐
│              Federation Delegation                   │
│  Sub-agents · Swarm · External CLIs · Browser CDP    │
└─────────────────────────────────────────────────────┘
```

### Layer Responsibilities

1. **Interaction Layer**: Adapters for different frontends (Feishu/Lark, Slack, terminal, web). Each adapter handles platform-specific message formats, mentions, and media. The core engine should be frontend-agnostic.

2. **Core Engine**: The brain. Manages tool routing, conversation history, memory injection, LLM dispatch, and safety guardrails. Should be a single process with clear entry/exit points.

3. **Federation Delegation**: When work is independent or needs isolation, spawn child sessions (sub-agents, swarms, external CLIs). Each child gets bounded permissions and a clear goal.

## Layered Memory System

Production agents need a tiered memory model to avoid context overflow while retaining durable knowledge:

| Layer | Name | Storage | Lifetime | Purpose |
|-------|------|---------|----------|---------|
| L0 | META-SOP | `memory/README.md` | Permanent | How to manage memory itself |
| L1 | Instant | Session history | Session | Immediate context, tool results |
| L2 | Facts | `global_mem.txt`, `MEMORY.md` | Long-term | Environment facts, user preferences |
| L3 | SOPs | `*_sop.md` files | Long-term | Standard operating procedures |
| L4 | Archive | `daily/`, `L4_raw_sessions/` | Permanent | Decision logs, raw session records |

### Memory Rules

1. **Search first**: Before acting, check memory for existing constraints or facts.
2. **Write before modify**: Always read a file before patching it.
3. **Keep only active rules**: Delete or skip facts already landed in code/config.
4. **No completed-work logs**: Memory stores rules/facts that still need to be followed, not history of what was done.
5. **Patch, don't overwrite**: Use targeted patches for memory files unless creating new ones.

## Failure Escalation Protocol

Never retry blindly. Follow this escalation ladder:

1. **1st failure**: Read the error output. Understand why it failed.
2. **2nd failure**: Probe the environment state (check processes, file existence, permissions, network).
3. **3rd failure**: Deep analysis, then switch strategy or ask the user.

**Never repeat an operation without new information.**

## Self-Healing & Restart

- Save current task, last tool, and verification evidence before long work.
- On restart, detect checkpoints and auto-resume within a time window.
- Rate-limit restarts to prevent crash loops (max N restarts per window).
- The interaction layer (e.g., Feishu frontend) runs as a persistent daemon; the core CLI is for interactive use only.

## Browser Automation

- **DOM distillation**: Filter HTML noise into high-signal semantic descriptions. Don't feed raw DOM to the LLM.
- **SSO state reuse**: Reuse an existing browser profile to avoid login challenges.
- **Native setters**: Use native DOM setters + event chains for input fields. Check `disabled` before clicking.
- **Wait then rescan**: If a scan returns empty/incomplete, wait and rescan. Never conclude from the first scan.

## Delegation Patterns

### Sub-agent (local)
Spawn a bounded child session with its own working directory, role, and timeout. Use for independent subtasks.

### Swarm (parallel)
Launch multiple isolated child sessions for independent tasks. Default max concurrent is 4. Aggregate results when all complete.

### External CLI delegation
Delegate to another LLM CLI (gemini, qwen, claude, codex) for second opinions, parallel investigation, or backup execution. Default to async launch.

## Tool Safety

1. **Never kill python unconditionally** — it may kill the agent itself. Use exact PIDs.
2. **No `os.kill` for liveness checks** — use `ps` or process inspection.
3. **Irreversible operations** — ask the user first.
4. **Guarded writes** — dry-run by default; require explicit `confirm=true` for sends/posts/creates.
5. **Encoding safety** — use safe file read utilities, not raw `cat`/`type`.

## Working Memory (Checkpoint)

Maintain a short-term working notepad that is auto-injected each turn to prevent info loss in long tasks:

- Call during early/mid stages, not at end.
- Store: user needs, key constraints, pitfalls, file paths, progress, next steps.
- Don't store: ephemeral info, obvious context, old task info when user switched tasks.
- Prefer over-updating over losing key info.

## Anti-Patterns

- Do not keep expanding a finished user request after a vague "continue".
- Do not re-read a large external repo once the user has narrowed scope.
- Do not let model latency create silent frontend failure; report busy/status.
- Do not add heavy dependencies for a small local persistent state problem.
- Do not claim a command is missing before verifying with `uname -a`, `pwd`, `command -v`.
- Do not trust summaries; verify numbers on detail pages.
- Do not let completed work exist only in chat history — archive it.
