# Example 15: Full-Stack Agent Intelligence Architecture

This manual turns the GA/Hermes/Codex agent discussions into a practical architecture for improving long-running agents.

The architecture is:

```text
information -> scheduling -> loop -> output stream

memory architecture -> cognition architecture -> evolution architecture -> audit architecture -> trust architecture

experience bundle facets: memory -> skills -> methodology -> impressions
```

The core rule:

```text
Keep the main path clean, let cognition influence it like intuition, make evolution evidence-backed, and give the agent real agency.
```

## What This Optimizes

The goal is not to add more rules. The goal is to let an agent:

- see information from messages, tools, files, cron, reports, and runtime state;
- schedule attention based on user intent, context, risk, and urgency;
- run loops that execute, verify, and close tasks;
- evolve by converting real outcomes into memory, skills, methods, impressions, and persona changes.

## Architecture Layers

### Information

Collect messages, files, logs, tool results, scheduled reports, human signals, and current runtime facts with source, time, scope, and evidence.

Do not dump all information into the prompt. Store it as queryable, degradable, traceable evidence.

### Scheduling

Scheduling routes attention. It is not an approval gate.

- Casual chat -> plain reply.
- Learning material -> direct learning asset path.
- Large task -> task workbench.
- Cron/report output -> memory event.
- Service error -> runtime event and concise report.
- Philosophy/persona direction -> L5 cognition and identity.

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

Cognition should guide attention and association. It should not stand between the user and the agent loop as a gatekeeper.

### Evolution Architecture

The evolution path is:

```text
signal/task -> useful pattern -> candidate lesson -> local or real validation
-> update memory/skill/method/persona -> merge if needed -> report
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

## Implementation Order

1. Build one event timeline for messages, tools, reports, cron, dream, and runtime events.
2. Standardize the task workbench output stream.
3. Normalize L0-L5 memory promotion.
4. Add an evolution ledger for learning assets.
5. Add a concise daily audit pack.
6. Keep removing gates that make the agent slower, more rigid, or less helpful.

## Done Standard

When the user says "continue", "next", "learn this", or "use your judgment", the agent should know the context, choose the right surface, act, verify, remember what it did, and improve the next similar run.
