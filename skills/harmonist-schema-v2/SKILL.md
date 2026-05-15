---
name: harmonist-schema-v2
description: Harmonist Schema-v2 agent interoperability protocol. Use structured YAML frontmatter envelopes for GA/Hermes and cross-machine agent communication; supports request/result/query/report/interrupt/ack, evidence-backed outputs, safety flags, and gent-mesh-style duplex transport. Trigger when coordinating with another agent, delegating work, reporting results, handoff, interop, frontmatter protocol, Schema-v2, GA local, Hermes cloud, agent mesh.
version: 1.0.0
yao_category: "AI编程"
---

# Harmonist Schema-v2 Interoperability

Use this when GA talks to another agent, delegates work across machines, accepts output from Hermes, or prepares a handoff that another agent must parse reliably.

Schema-v2 is a structured frontmatter contract: every cross-agent message starts with YAML frontmatter and then carries human-readable markdown. The frontmatter is the source of truth for routing, input, output, status, and verification; the markdown body is explanation only.

## Why

Pure text handoffs are fragile. Agents may summarize away constraints, miss output shape, or confuse "done" with "in progress". Schema-v2 keeps the coordination state parseable while still letting humans read the body.

## Envelope

Every message MUST use this shape:

```markdown
---
schema: harmonist.schema-v2
kind: request | result | query | report | interrupt | ack
id: msg_20260427_001
session: task_or_thread_id
from:
  agent: ga-local
  runtime: GenericAgent
  host: mac
to:
  agent: hermes-cloud
  runtime: Hermes
  host: aliyun
capability: github.pr_review | code.audit | browser.task | general
status: queued | running | blocked | done | failed
priority: low | normal | high | urgent
created_at: "2026-04-27T00:00:00+08:00"
expects:
  output_schema: brief | patch | evidence_report | question_answer | custom
  max_turns: 3
  deadline: null
transport:
  channel: feishu | ssh | file | mesh | http
  reply_to: "same-session"
lineage:
  parent: null
  ancestors: []
safety:
  may_write_files: false
  may_run_commands: true
  may_restart_services: false
  secrets_allowed: false
---

Markdown body for human context.
```

Required fields: `schema`, `kind`, `id`, `session`, `from.agent`, `to.agent`, `capability`, `status`, `created_at`, `expects.output_schema`, and `safety`.

## Request Template

```markdown
---
schema: harmonist.schema-v2
kind: request
id: msg_YYYYMMDD_HHMMSS_ga_001
session: <stable-task-id>
from:
  agent: ga-local
  runtime: GenericAgent
  host: mac
to:
  agent: hermes-cloud
  runtime: Hermes
  host: aliyun
capability: <domain.action>
status: queued
priority: normal
created_at: "<iso8601>"
expects:
  output_schema: evidence_report
  max_turns: 3
  deadline: null
transport:
  channel: feishu
  reply_to: same-thread
lineage:
  parent: null
  ancestors: []
safety:
  may_write_files: false
  may_run_commands: true
  may_restart_services: false
  secrets_allowed: false
---

## Task

<one concrete task>

## Inputs

- <paths, URLs, issue IDs, commands, or screenshots>

## Constraints

- <hard constraints>

## Acceptance

- <what must be true before returning done>
```

## Result Template

```markdown
---
schema: harmonist.schema-v2
kind: result
id: msg_YYYYMMDD_HHMMSS_hermes_001
session: <same-session>
from:
  agent: hermes-cloud
  runtime: Hermes
  host: aliyun
to:
  agent: ga-local
  runtime: GenericAgent
  host: mac
capability: <same-capability>
status: done
priority: normal
created_at: "<iso8601>"
result:
  summary: "<one-line outcome>"
  changed_files: []
  commands_run: []
  evidence:
    tests: []
    links: []
    logs: []
  open_questions: []
  next_actions: []
lineage:
  parent: <request-id>
  ancestors: [<request-id>]
safety:
  wrote_files: false
  ran_commands: true
  restarted_services: false
  exposed_secrets: false
---

## Outcome

<short explanation>

## Evidence

<only evidence that actually happened>

## Notes

<risks, blockers, or handoff details>
```

## Status Semantics

- `queued`: accepted but not started.
- `running`: started and has partial evidence.
- `blocked`: needs user or peer input; include `result.open_questions`.
- `done`: acceptance criteria met; include verification evidence.
- `failed`: cannot complete; include cause and next recoverable step.

Do not mark `done` if tests, commands, PR creation, deployment, or user-visible verification were skipped. Use `blocked` or `failed` honestly.

## Transport Guidance

Schema-v2 is transport independent. Pick the narrowest reliable channel:

- Same machine: file handoff under `temp/schema-v2/<session>/`.
- GA local -> Hermes cloud: Feishu message or `ssh aliyun` file push is the simplest current path.
- Hermes cloud -> GA local: Feishu reply is preferred because GA already receives Feishu; use file pull only for large artifacts.
- Real-time duplex: use a mesh transport inspired by `gent-mesh`: JSON frames with `id/session/type/from/to/payload/ts`, WebSocket streaming, heartbeat, and SSH reverse tunnels when the cloud machine cannot directly connect to the Mac.

When using mesh, the Schema-v2 markdown goes inside the frame `payload`:

```json
{
  "id": "frame_001",
  "session": "task_001",
  "type": "task_assign",
  "from": "ga-local",
  "to": "hermes-cloud",
  "payload": "---\\nschema: harmonist.schema-v2\\nkind: request\\n...",
  "ts": 1770000000000
}
```

## Validation Checklist

Before sending:

- Frontmatter parses as YAML.
- `schema` equals `harmonist.schema-v2`.
- `id` is unique in the session.
- `session` is stable across the task.
- `to.agent` names the real peer.
- `safety` truthfully states allowed actions.
- Body includes task, inputs, constraints, and acceptance for requests.
- Results include commands/evidence actually produced.
- No raw secrets, access tokens, cookies, or private keys are in frontmatter or body unless the user explicitly asked and `secrets_allowed: true`.

## Operating Rule

If a peer sends unstructured text for a cross-agent task, first normalize it into a Schema-v2 `request` or `result`, then continue. This creates a durable boundary between human phrasing and machine coordination.
