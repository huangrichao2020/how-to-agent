# Agent Skill Engineering

A skill may look like a Markdown prompt on the surface, but its core is not a
prompt.

A prompt is a one-off conversation instruction. A skill is a cross-session,
discoverable, on-demand, executable, versioned capability package.

One line:

```text
A prompt tells knowledge to the model.
A skill places operating knowledge in the file system so the agent can read,
grep, and execute it on demand.
```

## Four Shifts

### 1. Text To File-System Object

A prompt is text that must enter context to work.

A skill is a folder:

```text
skill-name/
├── SKILL.md
├── SKILL.zh-CN.md
├── references/
├── scripts/
└── assets/
```

It can be managed with git, reviewed, diffed, copied, installed, indexed, and
retired.

### 2. Full Context To Progressive Disclosure

Skills should load in three levels:

```text
level 1: metadata
  name + description
  for discovery and triggering

level 2: SKILL.md
  compact procedure
  read only after trigger

level 3: references / scripts / assets
  long docs, deterministic scripts, templates
  read or run only when needed
```

Resident context stays small; long material remains zero-cost until needed.

### 3. Pure Generation To Script Determinism

LLMs are good at judgment, explanation, tradeoffs, and composition. They are not
reliable at deterministic, repeated, format-sensitive operations.

Move these into `scripts/`:

- sorting, aggregation, validation, conversion;
- document, spreadsheet, PDF, image, or video structure operations;
- API parameter validation, batching, retry, and pagination;
- output size, file integrity, schema, lint, and tests;
- anything code can compute exactly.

Principle:

```text
Let the model handle creativity and tradeoffs.
Let scripts handle determinism and validation.
Script source does not need to enter context; script output does.
```

### 4. Temporary Instruction To Durable Capability Asset

A skill survives across conversations, tools, and agents. It is not "how to
answer this time"; it is "how to do this class of work in the future".

Good skill candidates usually:

- repeat often;
- need team or cross-agent sharing;
- contain fragile steps or known traps;
- benefit from deterministic scripts;
- involve external tools, file formats, or APIs;
- need maintenance and versioning.

Poor skill candidates:

- one-off facts;
- temporary emotional wording;
- needs clear enough for one sentence;
- private raw logs, keys, credentials;
- unvalidated ideas.

## Skill Admission Gate

Before creating a skill, ask:

1. Will this workflow repeat?
2. Does it need team, cross-session, or cross-agent sharing?
3. Does it contain steps that must run consistently?
4. Can scripts reduce uncertainty?
5. Does it reduce context cost better than a prompt?

If mostly no, use a prompt, memory entry, or ordinary document.

## Description Is The Trigger

The `description` is not brochure copy. It is the discovery mechanism.

A good description says:

- what the skill does;
- when to use it;
- likely user phrases;
- what not to confuse it with.

Too broad means false triggers. Too narrow means missed recall.

## Keep The Main File Short

`SKILL.md` should not become a long prompt.

It should contain:

- core stance;
- key triggers;
- a 5-8 step workflow;
- necessary prohibitions;
- when to read references;
- when to run scripts;
- output and verification contracts.

Move long background, full API notes, examples, templates, and scoring rubrics
into `references/`, `scripts/`, and `assets/`.

## Safety Boundary

Once a skill can run scripts, it has a larger attack surface than a prompt.

Check:

- trusted source;
- whether `scripts/` read or write sensitive paths;
- whether scripts download or execute extra code;
- whether they access keys, tokens, cookies, browser config, or private logs;
- whether user data leaves the machine;
- least privilege and auditable output.

Default rules:

```text
Do not install untrusted skills.
Do not run scripts you do not understand.
Do not store secrets in skills.
Return only necessary script output, not private dumps.
```

## Boundaries With Other Layers

| Object | Good for | Not good for |
| --- | --- | --- |
| Prompt | one-off task constraints | durable methods, deterministic scripts |
| Memory | facts, preferences, experience summaries | long procedures, executable tools |
| Skill | reusable operating methods, scripts, templates | one-off facts, private raw material |
| RAG | external knowledge and fact fragments | the procedure itself |
| MCP/API | connecting external systems | the method for using those systems well |
| Script | deterministic execution and validation | fuzzy judgment and value tradeoffs |

## Minimal Hint

```text
[SKILL ENGINEERING CHECK]
- Is this a one-off prompt or a cross-session capability asset?
- Should only the description stay resident?
- Is the main SKILL.md short enough?
- What belongs in references / scripts / assets?
- Which steps require deterministic scripts?
- Does this skill create security, permission, or privacy risk?
[/SKILL ENGINEERING CHECK]
```

The essence of a skill is not "prompt in a file". It is turning agent capability
into a discoverable, executable, maintainable software package.
