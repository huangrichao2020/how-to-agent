---
name: workflow-optimization-methodology
description: Use when optimizing SOPs, workflows, multi-agent collaboration, skills, MCP/toolchains, Feishu/Lark operations, or repeated agent work. Start from the final operating scene, inspect the real topology, decompose atomic actions, classify automation depth, implement the smallest verified slice, and package the learning. Trigger on workflow optimization, 工作流优化方法论, 原子级拆解, SOP优化, multi-agent workflow, Feishu group collaboration, or "不要只修局部症状".
---

# Workflow Optimization Methodology

Use this skill when a workflow, SOP, agent behavior, or collaboration pattern
needs to become reliably better, not merely patched once.

Core stance:

```text
final scene -> real topology -> atomic actions -> automation class
            -> smallest intervention -> scenario verification -> learning asset
```

Do not optimize the first visible symptom. First understand the operating scene
the user ultimately needs.

## Procedure

1. **Anchor the end-state scene.**
   Write the target operating scene in one paragraph: who participates, where it
   runs, what must happen, what must never happen, and what evidence proves it.
   If the user has already implied the scene, derive it instead of asking again.

2. **Inspect the real topology.**
   Check the live repo, runtime, process, remotes, platform behavior, permissions,
   state stores, queues, and mirrored deployments. Prefer current files/logs over
   memory. When two agents or hosts are involved, inspect both before editing.

3. **Decompose to atomic actions.**
   Split the workflow until each action has one trigger, one actor, one input,
   one decision, one output, one owner, and one failure mode. If an action still
   contains multiple decisions, split it again.

4. **Classify pain and automation depth.**
   Use the four-quadrant lens: high/low frequency by high/low time cost. Then
   classify each action:
   - **A: autonomous skill/tool.** Low risk, structured, frequent, rule-clear.
   - **B: agent-led with human fallback.** Medium risk or external impact.
   - **C: cognitive assist.** Ambiguous, strategic, creative, or high stakes.

5. **Choose the AI enhancement level.**
   - **L1:** AI advises, human decides.
   - **L2:** AI executes draft or partial action, human reviews.
   - **L3:** AI executes independently with monitoring and rollback.
   - **L4:** AI learns from feedback and improves the policy.

6. **Design the intervention.**
   Decide what belongs in the main path, what belongs in a sidecar, what should
   be handled by workers, and what must stay human-reviewed. Avoid blocking the
   main chain for recovery or gap-filling work that can run beside it.

7. **Implement the smallest vertical slice.**
   Change the least code or documentation needed to make the new operating rule
   real. Reuse existing rails, state stores, queues, skill registries, and
   experience systems before inventing new layers.

8. **Verify at scenario level.**
   Do not stop at unit tests if the failure was an operating scene. Reproduce
   the real route, message surface, runtime restart, document permission flow,
   or multi-agent handoff that the user cares about.

9. **Package the learning.**
   Update a skill, reference doc, memory note, SOP, or architecture map with the
   reusable rule. When the capability exists in mirrored agents, sync both sides
   and record any runtime-specific differences.

## Feishu / Multi-Agent Group Rules

For group collaboration agents, group chat is not single chat:

- A group message must be handled when the bot is explicitly mentioned; do not
  require the sender to be the user.
- If an outgoing group message is addressed to a specific person or bot, make
  the addressee explicit with a real platform mention. Judge this semantically
  from questions, handoffs, reviews, reminders, assignments, or omitted subjects;
  do not hard-code only the word "you".
- Agent-to-agent handoffs must use clickable mentions, not plain text aliases.
- Hide chain-of-thought or raw thinking in team/group scenes; direct messages may
  show richer reasoning when appropriate.
- Restart and operational reports should go to the owner privately unless the
  group explicitly needs the update.
- Missed-push recovery and long-message shard handling should be sidecar work.
  Process the available shard immediately; additional shards can enter through
  the worker/queue mechanism.
- Shared documents should include the owner by default, grant the peer agent the
  needed permission, and be posted back with a short summary plus the next
  explicit mention.

## Output Contract

For an optimization request, produce:

1. target operating scene and acceptance criteria;
2. inspected topology and evidence;
3. atomic action table;
4. A/B/C and L1-L4 routing;
5. implementation plan or patch;
6. verification results;
7. durable learning asset or sync note.

If the work is small, compress the report, but keep the same logic internally.

## Reference

Read `references/workflow-optimization-methodology.zh-CN.md` when the task is
architecture-level, multi-agent, cross-host, or has already taken multiple
iterations.
