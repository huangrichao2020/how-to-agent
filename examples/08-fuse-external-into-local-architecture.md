# Example 08: Fuse External Essence into Local Architecture

## Background

When an agent has accumulated enough production experience, it should
periodically review external best-practice projects (like `how-to-use-agent`)
and fuse their methodologies into its own architecture. This is not about
copying files — it's about extracting patterns and upgrading local systems.

## Original prompt

```text
你详细学习一下我的 github 的 how-to-use-agent 项目，然后结合你自身架构的精华，更新一版
```

## Developer Intent

This prompt requires the agent to:
1. Deeply study `how-to-use-agent`'s structure and content
2. Compare it with its own architecture (Hermes in this case)
3. Identify gaps: what does `how-to-use-agent` have that Hermes doesn't?
4. Identify strengths: what does Hermes have that `how-to-use-agent` doesn't?
5. Merge both: update `how-to-use-agent` with Hermes patterns, while
   keeping the original methodology intact

## Reusable Pattern

```text
Study [external project] deeply — read all files, understand the structure.

Compare with your own architecture:
- What patterns does it have that you lack? → Adopt them
- What patterns do you have that it lacks? → Contribute them back
- What conflicts exist? → Resolve by choosing the better approach

Update the external project with your strengths:
- Keep its original structure and methodology
- Add new skills/files that represent your unique patterns
- Update README to reflect the combined knowledge
- Maintain consistent style and depth

Commit and push with a clear message explaining the fusion.
```

## What Was Done (2026-05-13)

### Adopted from how-to-use-agent
- **Prompt trail methodology**: The 9-step conversation sequence
- **Consent gate pattern**: Before modifying agent-owned surfaces
- **Progressive rollout > big-bang**: Shadow mode → parallel → switch
- **Archive everything**: Design, migration logs, work manuals

### Contributed from Hermes
- **TTSR memory architecture**: Four-layer hierarchy with trigger injection
- **Self-healing browser**: Agent writes missing helper functions
- **Code Graph**: AST-based dependency analysis for blast radius
- **SysWatch**: System health diagnostics with heuristic anomaly rules
- **Skill evolution telemetry**: Understood → Proficient → Instinct stages
- **Production runtime updates**: Multi-platform gateway, cron scheduler,
  delegation patterns from 2026-05 runs

### New Files Created
- `skills/hermes-ttsr-memory/SKILL.md` — Trigger-based layered memory
- `skills/self-healing-browser/SKILL.md` — Dynamic browser helper writing
- `examples/08-fuse-external-into-local-architecture.md` — This file

### Updated Files
- `README.md` — Architecture principles section + new skills listed
- `README.zh-CN.md` — Chinese version of the same
- `skills/agent-self-evolution/SKILL.md` — Added TTSR integration section
- `skills/production-agent-runtime/SKILL.md` — Added Code Graph, SysWatch,
  self-healing browser, and 2026-05 production patterns

## Verification Checklist

- [x] All existing examples and skills preserved
- [x] New skills match existing style and depth
- [x] README.md and README.zh-CN.md both updated
- [x] Directory tree in README reflects new structure
- [x] No duplicate content — each skill has a distinct purpose
- [x] Content is from real production experience, not theoretical

## Notes for the Next Agent

If continuing to improve this project:
- Consider adding a `skills/architecture-evolution/SKILL.md` for the
  Phase 0→7 architecture evolution methodology
- The `how-to-use-agent` project could benefit from automated testing
  of skill loading patterns
- Consider creating a CLI tool that validates SKILL.md format consistency
