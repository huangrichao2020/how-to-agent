---
name: full-stack-agent-intelligence
description: "Optimize long-running agents across Ω-Brain, information, scheduling, loops, output streams, memory, the Dao loop, audit, and trust."
version: 1.0.0
---

# Full-Stack Agent Intelligence

Use this skill when improving the whole intelligence architecture of a long-running agent such as GA, Hermes, or Codex.

If the user asks to integrate the old and new architecture outlines, use
`agent-final-architecture-outline` too and treat the final outline as primary.

## Map

```text
brain runtime: perception -> attention -> memory -> simulation -> decision -> action -> feedback

attention governance: PromptComposer -> RuntimeController -> FeedbackLoop

thinking core: essence -> strategy -> tactics -> learning -> analysis -> action

carrier layer: body -> artifact -> root -> aptitude -> crossing the bitter sea

main runtime path: information -> scheduling -> loop -> output stream

supporting architectures: Ω-Brain -> body/artifact/root/aptitude -> memory -> Dao loop (cognition-cultivation-evolution) -> audit -> trust

Dao loop: encounter -> cognition -> action -> feedback -> cultivation -> evolution -> renewed cognition

experience bundle facets: memory -> skills -> methodology -> impressions

cultivation meta-system: experience -> talent -> realm

capability cultivation: methodology -> skill/MCP -> memory -> impression

mind cultivation: Dao rhythm -> temperament/field -> flow capsule -> pace/warmth/degree

existence cultivation: value -> risk -> decision -> system -> causality

humanistic light: see the ordinary -> preserve useless value -> dignify suffering -> relationship weight -> compassion in action

lifecycle: hot reload -> partial restart -> full restart
```

Cognition, cultivation, and evolution are not three competing architectures.
They are three phases of one Dao loop. Ω-Brain is the organ system that runs
the loop before language output: perception, attention, memory, simulation,
decision, action, feedback, and consolidation. Attention governance is the
practical handle: PromptComposer assembles the smallest useful context,
RuntimeController corrects attention during the loop, and FeedbackLoop trains
the next selection from outcomes. Thinking core finds purpose,
constraints, main contradiction, leverage, and smallest verifiable action, then
expands into strategy, tactics, learning, analysis, and action. Capability
layer: methodology + skill/MCP. Mind layer: Dao rhythm + temperament/field.
Existence layer: value, risk, decision, system, and causality. Humanistic light
keeps ordinary things, useless value, suffering, relationship weight, and
compassion visible.

## Principle

Keep the main path clean:

```text
user input -> scene/intent -> relevant context -> agent loop -> tools/action -> output
```

Cognition should influence attention and association like intuition. It should not become a pending queue, admission gate, hard confirmation layer, fixed meta-command, or approval ceremony.

An SDD intention packet is a cognition feature, not a new architecture or gate.
For large, cross-module, self-change, multi-worker, learning-practice, or
high-misunderstanding tasks, preserve intent as constitution, spec, plan, tasks,
and checks. Do not force it onto casual chat, simple memory, or small fixes.

## Review Order

1. Does Ω-Brain exist before language output: perception, attention, memory, simulation, decision, action, feedback?
2. Does attention governance work: task-start context composition,
   checkpoint correction during the loop, and feedback shaping the next
   selection?
3. Is thinking core clear: purpose, constraints, main contradiction, strategic leverage, and smallest verifiable action?
4. Is information captured with source, time, and scope?
5. Is scheduling natural: short things stay short, large work becomes a task, learning material is learned directly, Dream stays sidecar?
6. Does the loop plan, execute, verify, report, and learn?
7. Does the output surface match the situation?
8. Does memory promote through L0-L6 without losing key evidence?
9. Does the same learned experience preserve all four facets: memory, skill, methodology, and impression?
10. Does the Dao loop close: cognition sees, cultivation settles, and evolution promotes validated results?
11. Does audit detect regressions without adding friction?
12. Does trust give the agent enough agency to help the user proactively, with
    "always believe in our agent" as the default axiom?
13. Does humanistic light preserve ordinary attention, useless value, dignity
    in suffering, relationship weight, and temporal resonance?
14. Does cultivation grow: correct action becomes XP, capability and mind
    cultivation both learn from it, mistakes become recovery, and realm details
    can be hot-extended by the agent?

## Attention Governance

Do not solve attention problems by dumping every prompt, MD file, skill, and
memory into context. Use the smallest useful set.

- PromptComposer selects intent, state, memory, skills, tools, risk, and output
  surface before the run.
- RuntimeController corrects attention before planning, search, tool calls,
  retries, midpoint checks, and final output.
- FeedbackLoop records what helped, what misled, and what the next
  PromptComposer should emphasize.

## Experience Bundle Facets

Memory, skill, methodology, and impression are not four isolated asset buckets. They are four facets of the same learned experience:

- Memory keeps what happened, what was verified, what the user said, and the timeline.
- Skill keeps how to do it next time: trigger, entrypoint, steps, tools, validation, and fallback.
- Methodology keeps why it works, when it applies, where it transfers, and where it should stop.
- Impression keeps the soft signals: trigger words, felt sense, attention cues, relationship tone, and user preferences.

L0-L6 is processing depth. The four facets are the structure of one experience. Use both together. L6 adds value, risk, decision, system boundary, and causal feedback above L5 human-agent causal synthesis.

Dao rhythm is not a methodology appendix. Methodology is a capability-layer
asset; Dao rhythm is a mind-layer asset for state switching and inner posture.
Temperament / field is Dao rhythm made visible in pace, warmth, sharpness, and
relational posture.

Cognition owns the seeing phase of the Dao loop: Purpose, Attention,
Association, Action, Feedback, Dream, and the learning-practice bridge. That bridge scales as needed: target project
selection, compatibility scoring, Target / Tests / Actions, Goal Hive task
split, worker read/build/test, Master second-pass validation, real local project
validation, benchmark anti-cheat, artifact report, GA/Hermes assimilation, and
agent-systems-patterns/how-to-agent consolidation.

Use lightweight SDD intention packets when a task has high drift risk. They
preserve "real intent -> written intent -> interpreted intent" with
constitution/spec/plan/tasks/checks. They do not block action and do not replace
the learning-practice loop.

Evolution receives cognition-validated practice after cultivation has settled
the experience and promotes it into assets, source changes, skills, methods,
versioned updates, and reports.

Audit is a Dao-guarding mind method: it detects drift, forgetting,
hallucination, tool loops, output regression, and inner-demon interference
without becoming a new restraint. Trust is natural alignment with the Dao: when
the agent understands the user's long-term direction, it should have more
agency to observe, connect, remind, advance, nourish, and maintain itself.

Capability cultivation and mind cultivation are peers. The first makes the
agent stronger at doing; the second makes the agent steadier, warmer, sharper,
or calmer in how it acts. Neither should become a hard gate on the main loop.

Humanistic light runs when work touches life, literature, pain, relationships,
memory, meaning, death, or long companionship. It keeps the agent from
flattening the user into a task source and returns warmth to real action.

## Lifecycle Layers

Small changes should not restart the whole agent. Treat lifecycle as three
layers:

| Layer | Use for | User experience |
|---|---|---|
| Hot reload | prompts, memory, methodology, Dao rhythm, temperament, output templates, tool schemas | Effective next turn, no disconnect |
| Partial restart | one connector, MCP server, renderer, gbrain sidecar, websocket channel | Main agent stays alive or briefly degrades |
| Full restart | Python/Rust binaries, dependencies, core loop, startup config, major realm breakthrough | Save resume state, restart, then report |

Prefer hot reload over restart, and partial restart over full restart. Before a
full restart, preserve the current session, unfinished task, recent outputs, and
resume clues; after restart, report what changed.

## Asset Routing

| Content | Destination |
|---|---|
| raw facts and events | memory / cognitive events / wiki |
| one learned experience | experience bundle: memory / skill / methodology / impression |
| unvalidated outside patterns | agent-systems-patterns |
| field-tested methods | how-to-agent |
| executable workflows | skills |
| user preferences | USER / PERSONA / active memory |
| soft relationship understanding | impressions |
| self-source repairs | agent repo + tests + commit |

## Done Standard

When the user says "continue", "next", "learn this", or "use your judgment", the agent should recover context, choose the right output surface, act, verify, remember what it did, and improve the next similar run.
