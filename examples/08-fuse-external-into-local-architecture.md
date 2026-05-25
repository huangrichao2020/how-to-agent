# Example 08: Fuse External Essence into Local Architecture

## Background

When an agent has accumulated enough production experience, it should
periodically review external best-practice projects (like `how-to-agent`)
and fuse their methodologies into its own architecture. This is not about
copying files — it's about extracting patterns and upgrading local systems.

## Original prompt

```text
你详细学习一下我的 github 的 how-to-agent 项目，然后结合你自身架构的精华，更新一版
```

## Developer Intent

This prompt requires the agent to:
1. Deeply study `how-to-agent`'s structure and content
2. Compare it with its own architecture (Hermes in this case)
3. Identify gaps: what does `how-to-agent` have that Hermes doesn't?
4. Identify strengths: what does Hermes have that `how-to-agent` doesn't?
5. Merge both: update `how-to-agent` with Hermes patterns, while
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

Status note: this file records the original fusion pass. Some contributed skill
names below were later consolidated or renamed during cleanup; treat them as
historical paths unless the directory still exists in `skills/`.

### Adopted from how-to-agent
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
- Historical path: `skills/hermes-ttsr-memory/SKILL.md` — now represented by
  the trigger-based memory and anti-bloat material in the current agent skills.
- Historical path: `skills/self-healing-browser/SKILL.md` — now represented by
  `skills/self-healing-browser-extractor/SKILL.md`.
- `examples/08-fuse-external-into-local-architecture.md` — This file

### Updated Files
- `README.md` — Architecture principles section + new skills listed
- `README.zh-CN.md` — Chinese version of the same
- Historical path: `skills/agent-self-evolution/SKILL.md`
- Historical path: `skills/production-agent-runtime/SKILL.md`

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
- The `how-to-agent` project could benefit from automated testing
  of skill loading patterns
- Consider creating a CLI tool that validates SKILL.md format consistency
