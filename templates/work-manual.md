# Work Manual Template

## What Changed

[Short summary of what was implemented in this phase.]

## Why It Changed

[The problem this solves, the external signal or user request.]

## File Paths

| File | Purpose | Changed? |
|------|---------|----------|
| `path/to/file` | [what it does] | [yes/no/new] |
| `path/to/file2` | | |

## How to Verify

```bash
# Command 1: verify X
# Expected output: Y

# Command 2: verify Z
# Expected output: W
```

## What Remains Paused

| System | Why paused | When to resume |
|--------|-----------|---------------|
| [name] | [reason] | [trigger/phase] |

## Phase Two: What's Next

[Description of the next phase, including which files to touch and what to verify.]

## Rollback

```bash
# If things go wrong:
git reset --hard [tag or commit]
# or
cp /backup/file /original/path/file
# or
[specific config revert]
```

## Archive Path

- Architecture note: [gbrain slug or file path]
- Work manual: [this file's path]
- Wiki URL: [if published]
- Git tag: [rollback point]
