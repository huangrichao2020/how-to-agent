# Architecture Note Template

## Current Problem

[What is broken or missing? Be specific.]

## Target Behavior

[What should the system do after this change?]

## Migration Phases

### Phase 1: [Name]
- What changes:
- Files affected:
- Risk: [low/medium/high]
- Rollback: [exact steps]
- Acceptance check: [how to verify]

### Phase 2: [Name]
- What changes:
- Files affected:
- Risk:
- Rollback:
- Acceptance check:

### Phase 3: [Name]
- What changes:
- Files affected:
- Risk:
- Rollback:
- Acceptance check:

## What Must Stay Unchanged

[List systems, data, or behaviors that should NOT be touched during this migration.]

## Risks and Rollback

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| | | | |

Rollback path: [exact commands/steps to revert to current state]

## Adjacent Systems to Freeze

- [ ] System A (reason)
- [ ] System B (reason)
