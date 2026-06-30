---
name: cognitive-project-builder_认知项目构建器
description: Use when turning a user's domain keywords, key concepts, lived experience, opinions, scenarios, mistakes, and case fragments into a complete cognitive project: methodology, terminology, models, coaching system, scenario cases, and reusable skill. Trigger on 认知项目, 认知体系, 教练体系, 场景案例分析, 方法论演化, 从经验到 skill, 关键词/关键概念/实际心得/场景沉淀.
---

# Cognitive Project Builder

Use this skill when the user wants to build a durable domain cognition project
from their own experience rather than a generic research summary.

One-line principle:

```text
The user supplies experience density; the agent supplies structure.
```

For the full Chinese method, read:

```text
references/cognitive-project-methodology.zh-CN.md
```

## Core Workflow

1. Collect seeds: domain, keywords, key concepts, lived lessons, opinions,
   actual scenarios, common misjudgments, desired coaching behavior.
2. Extract sharp fragments: repeated terms, pain points, high-energy one-liners,
   failure patterns, and distinctions.
3. Name concepts: turn vague feelings into stable terms the project can reuse.
4. Build models: state machine, stages, signal table, formulas, red lines,
   decision checks.
5. Coachify: define diagnosis order, evidence reading, strengths, risks, next
   actions, scripts, persona/strategy, and review metrics.
6. Caseify: anonymize real scenes into fixed case files.
7. Package: create `README`, `SKILL_技能说明与使用指南.md`, `SKILL_技能说明中文版.md`, `methodology/`,
   `references/`, and `cases/`.
8. Iterate: every new scenario should refine, split, or add a module/case.

## Output Shape

```text
Domain seed:
User keywords:
Key concepts:
High-energy maxims:
Core models:
Coaching workflow:
Case list:
Project file plan:
Next sampling questions:
```

## Anti-Patterns

- Do not build an encyclopedia when the user has no lived seeds.
- Do not erase the user's sharp wording in favor of bland terminology.
- Do not leave insight as slogans; turn it into model + coach + case.
- Do not expose raw private logs or identifiable people.
- Do not declare the system complete before cases have tested it.
