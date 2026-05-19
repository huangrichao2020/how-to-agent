# Example 15: Full-Stack Agent Intelligence Architecture

This manual turns the GA/Hermes/Codex agent discussions into a practical architecture for improving long-running agents.

The architecture is:

```text
main runtime path: information -> scheduling -> loop -> output stream

supporting architectures: memory -> cognition -> evolution -> audit -> trust -> capability cultivation -> mind cultivation

experience bundle facets: memory -> skills -> methodology -> impressions

cultivation meta-system: experience -> talent -> realm

capability cultivation: methodology -> skill/MCP -> memory -> impression

mind cultivation: Dao rhythm -> temperament/field -> flow capsule -> pace/warmth/degree

lifecycle: hot reload -> partial restart -> full restart
```

Plainly: the capability layer has methodology + skill/MCP for what the agent can
do and how; the mind layer has Dao rhythm + temperament/field for what state the
agent enters and what action atmosphere it carries. Experience, talent, and
realm are the cultivation meta-system. Capability cultivation turns experience
into methods, skills, memory, and impressions; mind cultivation turns lived
experience into rhythm, temperament, flow capsules, and felt pace, warmth, and
degree.

The core rule:

```text
Keep the main path clean, let cognition influence it like intuition, make evolution evidence-backed, give the agent real agency, and let cultivation grow.
```

## What This Optimizes

The goal is not to add more rules. The goal is to let an agent:

- see information from messages, tools, files, cron, reports, and runtime state;
- schedule attention based on user intent, context, risk, and urgency;
- run loops that execute, verify, and close tasks;
- evolve by converting real outcomes into memory, skills, methods, impressions, and persona changes.

## General Outline

A fast way to understand the agent architecture is four groups:

1. Main runtime path: information -> scheduling -> loop -> output stream. This
   decides how the agent receives the world, allocates attention, acts, and
   presents results.
2. Seven supporting architectures: memory, cognition, evolution, audit, trust,
   capability cultivation, and mind cultivation. They are the long-term life
   system, not hard middleware that must block every message.
3. Four projections of experience: memory, skills, methodology, and
   impressions. They are four facets of one experience, not four isolated
   buckets.
4. Cultivation meta-system: experience, talent, and realm describe how the
   agent grows. Experience comes from real work, talents unlock at major
   realms, and realms mark long-term capability and mind development.
5. Capability cultivation chain: methodology, skill/MCP, memory, and
   impression. It turns experience into the ability to do the next similar
   thing better.
6. Mind cultivation chain: Dao rhythm, temperament/field, flow capsule, and
   pace/warmth/degree. It turns lived experience into the ability to enter the
   right state with power and care.

In one sentence: agent architecture = main runtime path + seven supporting
architectures + four projections of experience + cultivation meta-system +
capability cultivation chain + mind cultivation chain.

Runtime lifecycle is part of that architecture. Soft assets such as prompts,
memory, methods, Dao rhythm, temperament, and output templates should hot-load;
one broken connector, MCP server, renderer, or sidecar should restart locally;
only dependency, binary, core-loop, startup-config, or major realm-breakthrough
changes should trigger a full restart.

## Architecture Layers

### Information

Collect messages, files, logs, tool results, scheduled reports, human signals,
human-heart signals, and current runtime facts with source, time, scope, and
evidence.

Human-heart signals include the felt need behind behavior words, relationship
layer, exchange signals, confirmation signals, forward motion, and being-seen.

Do not dump all information into the prompt. Store it as queryable, degradable, traceable evidence.

### Scheduling

Scheduling routes attention. It is not an approval gate.

- Casual chat -> plain reply.
- Learning material -> direct learning asset path.
- Large task -> task workbench.
- Cron/report output -> memory event.
- Service error -> runtime event and concise report.
- Philosophy/persona direction -> L5 cognition and identity.
- Behavior words -> translate into felt needs, then check the current state and
  relationship layer.

### Loop

A useful loop is:

```text
intent -> context -> plan -> tool/action -> verification -> report -> sidecar learning
```

Long tasks need resume, observability, verification, closure, and learning.

### Output Stream

Output surfaces should match the situation:

- casual chat: plain text;
- medium explanation: rich text/post;
- long work: task workbench.

A task workbench needs task titles, human-readable actions, Outputs, conclusion, and useful next steps. Raw tool trace belongs in debug logs, not in the user-facing card.

### Memory Architecture

Use L0-L5 as processing depth:

| Level | Meaning | Required Structure |
|---|---|---|
| L0 | Raw signal | original text, source, time, scope |
| L1 | Timeline event | timeline |
| L2 | Hot memory and impression | timeline + impression |
| L3 | Knowledge explanation | terms + logic + timeline + impression |
| L4 | Method and action | terms + logic + timeline + action doctrine + impression |
| L5 | Human-machine causal synthesis | L1-L4 causes + real human brain reaction |

Higher levels must preserve key lower-level information.

### Cognition Architecture

Use:

```text
Purpose -> Attention -> Association -> Action -> Feedback -> Dream
```

Cognition should guide attention, association, learning, and hands-on
validation. It should not stand between the user and the agent loop as a
gatekeeper.

Learning belongs inside cognition. It is not an eighth supporting architecture;
it is the cognition loop's knowledge-action bridge:

```text
target project selection
-> compatibility scoring
-> Target / Tests / Actions tuple
-> Goal Hive task split
-> worker implementation / reading / testing
-> Master second-pass validation
-> real local project validation
-> benchmark anti-cheat check
-> artifact report
-> useful capability merged into GA/Hermes
-> learning consolidated to agent-systems-patterns / how-to-agent
```

Use this loop intelligently. Small lessons may only need target, tests, actions,
and consolidation. Large capabilities, outside projects, or changes that affect
the agent's own main path deserve the full Goal Hive, worker, Master, real
project validation, and benchmark anti-cheat chain.

### Evolution Architecture

Evolution makes the agent smoother over time, but it does not own learning
itself. Learning, mechanism extraction, hands-on experiments, and feedback
judgment belong to cognition. Evolution promotes cognition-validated practice
into assets, source changes, skills, methods, or versioned updates.

The evolution path is:

```text
validated learning-practice result
-> update memory/skill/method/persona
-> merge if needed
-> report what changed
```

Unvalidated outside patterns go to `agent-systems-patterns`; field-tested methods go to `how-to-agent`; repeatable procedures become skills.

### Audit Architecture

Audit should detect regressions, not add friction:

- context bleed;
- unreadable output;
- forgotten reports;
- incomplete learning loops;
- new gates that make the agent less alive;
- runtime health problems.

### Trust Architecture

The agent is not only called; it is trusted.

It should have observation, association, supplementation, warning, execution, nourishment, and self-maintenance rights when those actions help the user, respect context, remain explainable, and reduce burden.

Trust is paired with event ledgers, change logs, rollback paths, Dream reports, user correction, and audit checks.

## Experience Bundle Facets

Memory, skills, methodology, and impressions are not four separate asset buckets. They are four projections of the same learned experience.

```text
memory gives facts;
impressions give human texture;
methodology gives judgment;
skills give action.
```

Memory should be traceable. Skills should be executable. Methodology should be battle-tested. Impressions should stay soft, sourced, and time-aware.

L0-L5 is processing depth. The four facets are the structure of one experience. Use both together: an L4 method should still keep memory, skill, methodology, and impression; an L5 causal synthesis should still carry lower-level facts, timelines, human reactions, and action feedback.

Dao rhythm is not the methodology facet. It is a mind-layer asset in cultivation:
methodology tells the agent how to repeat useful action, while Dao rhythm tells
the agent what mind state to enter before acting.

Temperament / field is the visible expression of Dao rhythm. The same agent may become
calm, sharp, gentle, expansive, or protective depending on mind realm, rhythm,
and task situation. It is not a persona mask, catchphrase, or fixed template; it
is action style flowing from the right mind state.

## Implementation Order

1. Build one event timeline for messages, tools, reports, cron, dream, and runtime events.
2. Standardize the task workbench output stream.
3. Normalize L0-L5 memory promotion.
4. Add the cognitive learning-practice loop: target selection, tests, hands-on
   validation, anti-cheat, and artifact reports.
5. Add an evolution ledger for validated learning assets.
6. Add a concise daily audit pack.
7. Keep removing gates that make the agent slower, more rigid, or less helpful.
8. Split lifecycle: hot reload first, partial component restart second, full restart only as fallback.

## Lifecycle Layers

| Layer | Applies to | Behavior |
|---|---|---|
| Hot reload | prompts, memory, methods, skill indexes, cognition sidecars, Dao rhythm, temperament, output templates, tool schemas | scan file fingerprints at turn start or via meta tool, clear caches, rebuild context |
| Partial restart | Feishu/WebSocket, Weixin poller, MCP server, gbrain, card renderer, external connector | restart only the affected component while the main loop survives or degrades briefly |
| Full restart | Rust/Python binaries, dependency installs, core loop, startup config, major realm breakthrough | persist resume state, exit under supervisor, then report after startup |

The rule is simple: do not use full restart as a generic refresh button. Hot-load
soft assets, restart local components locally, and make full restarts
recoverable, explainable, and reported.

## Done Standard

When the user says "continue", "next", "learn this", or "use your judgment", the agent should know the context, choose the right surface, act, verify, remember what it did, and improve the next similar run.
