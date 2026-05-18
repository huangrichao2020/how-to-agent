# Learning Asset Gate

Use this pattern when an agent has a scheduled learning brief, GitHub scan, or
research loop that should improve the agent over time without asking the user
to approve every tiny conversational phrase.

## Problem

Learning loops often collapse into one of two bad shapes:

- They send a report, then forget everything by the next turn.
- They treat every user reaction, such as "ok" or "可以", as an implicit
  long-term-write permission or runtime change.

Both are exhausting. The agent needs to learn, but the user should not become a
full-time memory moderator.

## Rule

Split learning into three outcomes:

- External lessons that help agent architecture go to `agent-systems-patterns`.
- Practice-validated methods go to `how-to-agent`.
- Ideas that change the agent itself become discussion proposals first.

The third case is the important guardrail. A learning item can suggest changing
GA, Hermes, Codex, memory, runtime prompts, tools, or cron behavior, but it
cannot enter practice until the user has discussed or approved it.

## Procedure

1. Generate the normal learning report first.
2. For each possible lesson, ask whether it helps the agent do future work.
3. If it is useful external learning, write it to the fast pattern layer.
4. If it is already validated in real work, write it to the practice library.
5. If it changes the agent's own behavior, write a discussion proposal instead; do not create a live pending gate.
6. Send an asset report that lists `updated`, `needs_discussion`, and `skipped`.

## Validation

This pattern was implemented in GA and Hermes on 2026-05-16:

- GA added `agent_learning_assets.py` and a `learning_asset_update` tool.
- Hermes added `agent/learning_assets.py` and `tools/learning_assets_tool.py`.
- The Hermes GitHub learning cron was updated to include `hermes-core` and call
  the new tool after the teach-back report.
- Tests verified learning routing, practice routing, unvalidated-practice
  skipping, and self-change proposal gating.

## Anti-Pattern

Do not write unvalidated practice into `how-to-agent` just because the idea is
interesting. Do not let a cron job silently rewrite agent behavior because a
popular repo used a cool mechanism.
