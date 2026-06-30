---
name: agent-skill-creator_Skill技能自动构建器
description: Use when an agent needs to create, update, manage, validate, or retire its own reusable skills. Covers trigger design, folder layout, progressive disclosure, runtime indexing, skill use habits, and post-task skill maintenance for GA/Hermes-style agents.
---

# Agent Skill Creator

Use this skill when a conversation produces reusable capability and the agent
should turn it into a durable skill rather than leaving it as chat memory.

## Core Stance

A skill is not a prompt dump. It is reusable operating knowledge with a clear
trigger, a compact procedure, optional references/scripts, and verification that
the runtime can find and use it.

```text
repeated need -> reusable workflow -> skill package -> index check -> real use -> maintenance
```

More precisely:

```text
A prompt is a one-off conversation instruction.
A skill is a cross-session, on-demand, executable, versioned capability package.
```

The value of a skill is not that its Markdown looks different from a prompt. It
comes from three things:

- Progressive disclosure: keep only `name + description` resident; read the
  body after trigger; read long material only when needed.
- Script determinism: move repeatable, format-sensitive, verifiable steps into
  `scripts/`.
- Durable asset management: skills can be managed with git, reviewed,
  installed, indexed, reused, and retired.

## When To Create A Skill

Create or update a skill when at least one is true:

- the same workflow will likely be used again;
- the task involves a fragile external system, API, tool, or file format;
- the agent repeatedly writes the same helper script or checklist;
- the user explicitly says the agent should learn, remember, or use this
  ability later;
- the lesson is operational rather than only factual;
- the work has been validated in a real task and should become durable.

Do not create a new skill for a one-off fact, a private raw log, a secret, or a
tiny note that belongs in memory.

## Skill Admission Gate

Before creating a skill, ask:

1. Will this workflow repeat?
2. Does it need cross-session, cross-agent, or team sharing?
3. Does it contain steps that must run consistently?
4. Can scripts reduce uncertainty?
5. Does it reduce context cost better than a prompt?

If mostly no, use a prompt, memory entry, or ordinary document.

## Skill Anatomy

Preferred folder shape:

```text
skill-name/
├── SKILL_技能说明与使用指南.md
├── SKILL_技能说明中文版.md
├── references/
│   └── source-map.md
├── scripts/
│   └── optional-helper.py
└── assets/
    └── optional-template-or-media
```

For GA's current flat runtime registry, also create a compact runtime skill at:

```text
skills/<domain>/<skill-name>.md
```

For M1 Hermes, install the portable folder under both:

```text
~/Desktop/hermes-agent/skills/<skill-name>/
~/.hermes/skills/<skill-name>/
```

## Description Design

The frontmatter `description` is the trigger. It should answer:

- what the skill does;
- when it should be used;
- common user phrases that should trigger it;
- what it should not be confused with.

Keep the body concise. Put long reference material into `references/` and tell
the agent exactly when to read it.

If `description` is too broad, the skill will false-trigger. If it is too
narrow, recall will fail. It is not brochure copy; it is the runtime discovery
mechanism.

## Progressive Disclosure Design

Organize skills in three layers:

```text
L1 metadata: name + description
  discovery and triggering only

L2 SKILL_技能说明与使用指南.md / SKILL_技能说明中文版.md
  core procedure, prohibitions, output, and validation

L3 references / scripts / assets
  long material, deterministic scripts, templates, examples
```

The main file should not become a long prompt. If a section is not needed on
every trigger, split it out.

## Script Determinism

Prefer `scripts/` for:

- sorting, aggregation, validation, conversion;
- document, spreadsheet, PDF, image, and video structure operations;
- API parameter validation, batching, retry, and pagination;
- output size, file integrity, schema, lint, and tests;
- anything code can compute exactly.

The model handles judgment and tradeoffs; scripts handle determinism and
validation. Script source does not need to enter context; script output does.

## Creation Workflow

1. **Extract the capability.**
   Write the reusable action in one sentence. If the lesson is only a fact,
   store it as memory instead.

2. **Name the skill.**
   Use a short kebab-case name that describes the job, not the source article.

3. **Write the trigger.**
   Make `description` broad enough to trigger naturally, but narrow enough to
   avoid irrelevant loading.

4. **Write the core procedure.**
   Prefer:
   - one core stance;
   - a 5-8 step workflow;
   - anti-slop rules;
   - output contract;
   - verification steps.

5. **Use progressive disclosure.**
   Keep `SKILL_技能说明与使用指南.md` small. Put source maps, long API notes, examples, and
   templates in `references/`, `scripts/`, or `assets/`.

6. **Install into the runtime.**
   Add the portable skill to the capability library and add a compact runtime
   copy where the agent actually indexes skills.

7. **Rebuild or verify the index.**
   Confirm the runtime can see the skill:
   - GA: run `skill_registry.prompt_summary(...)` or rebuild
     `skills/index-cache/skills_index.json`.
   - Hermes: run the local skill listing/view command or inspect its skill
     index.

8. **Use it once.**
   A skill is not alive until it has guided a real task or a smoke prompt.

9. **Maintain it.**
   After real use, update the skill with validated changes only. Remove
   obsolete warnings, merge duplicates, and archive stale skills.

## Skill Management Rules

- Prefer improving an existing skill over creating a near-duplicate.
- Keep skills high-signal; do not turn the skill directory into a junk drawer.
- Skills should grant ability, not add approval theater.
- If a skill becomes too long, split references out instead of bloating the
  main file.
- If a skill is rarely used or domain-specific, archive it outside the core
  daily skill set.
- Never store secrets, raw private logs, credentials, or tokens in a skill.
- Do not install untrusted skills; review read/write paths, external downloads,
  permissions, and data exfiltration risk for any skill with scripts.
- Do not wrap a one-sentence task in a skill just to look systematic.

## Output Contract

When creating or updating a skill, report:

1. skill name and trigger;
2. files changed;
3. how it will be used;
4. verification performed;
5. whether GA/Hermes runtime indexes were updated.
