# Skill Evolution Evaluation Plan

Proposal: `6bb9ea9386cb`

## Problem

Skill 'browser-automation-low-memory' meets the usage/success threshold for promotion, but promotion into BOOT/hooks should not happen without explicit eval evidence.

## Evidence

- usage total=62
- success_rate=0.89
- stage=本能

## Plan

1. Write a skill-local evaluation plan under references/ so future promotion has a concrete checklist.
2. Keep the live SKILL.md behavior unchanged until the evaluation plan has real passing examples.
3. After the eval passes across representative tasks, open a separate proposal for BOOT/hook promotion.

## Validation

Read the generated references/evolution-eval-*.md and keep existing skill tests/loads passing.

## Rollback

Remove the generated references/evolution-eval-*.md file with skill_manage(action='remove_file').
