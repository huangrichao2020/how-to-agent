# GA / Hermes Runtime Notes

This note exists so agents do not confuse a portable skill package with the
runtime location that actually gets indexed.

## GenericAgent

GenericAgent currently indexes Markdown files in:

```text
skills/<domain>/<name>.md
```

Important steps:

1. Add a compact runtime skill file under a relevant domain.
2. If the skill should be highly visible, pin or prioritize its title in
   `skill_registry.py`.
3. Rebuild/inspect the index with `skill_registry.build_index(...)` or
   `skill_registry.prompt_summary(...)`.
4. Check `skills/index-cache/skills_index.json` only as generated evidence; do
   not hand-edit it as source of truth.

## M1 Hermes

Hermes should keep portable skill folders in the source checkout:

```text
~/Desktop/hermes-agent/skills/<skill-name>/
```

The active runtime may also read from:

```text
~/.hermes/skills/<skill-name>/
```

Install to both when the source checkout and runtime skill directory are both
present. Prefer git for source changes, then copy/sync runtime files deliberately
when a restart is not desired.

## Verification

Minimum verification:

- the file exists in source;
- the file exists in the runtime skill location if separate;
- the skill list or prompt summary contains the skill title;
- one smoke task can trigger or explicitly load the skill.

