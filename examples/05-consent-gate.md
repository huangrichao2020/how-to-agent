# Example 05: Consent Gate

## Scenario

The agent has completed phase one of an architecture migration. The next step requires
modifying `AGENTS.md` and updating the skill index.

## Wrong behavior

```text
Great, I've updated AGENTS.md and the skill index. Everything should work now.
```

## Right behavior

```text
Phase one is verified and working. Phase two requires modifying agent-owned surfaces.

Files:
- ~/.hermes/skills/my-skill/SKILL.md (rewrite)
- skills_index.json (add entry)

Why:
- Enable the new routing pattern for future agents

Risk:
- If the skill schema is wrong, the agent may misroute requests
- Old skill references may break

Rollback:
- git reset --hard v1.5.0-pre-migration
- Restore skills_index.json from backup

Do you approve these changes?
```

## Key rule

Never treat "continue" or "go ahead" as consent for modifying agent-owned data.
The agent must name the files, explain the risk, and give a rollback path.
The user must say "yes", "approved", or something equally explicit.
