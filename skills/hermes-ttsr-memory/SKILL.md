---
name: hermes-ttsr-memory
description: Trigger-based layered memory architecture (TTSR) for constrained agents. Keeps system prompt under 12K tokens with 200+ skills by loading memory on trigger word match. Four-layer hierarchy: Impression → Anchor → Instinct → Skill/Memory.
---

# Hermes TTSR Memory Architecture

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md)

Use this skill when designing memory systems for agents running on
resource-constrained environments (2GB RAM, limited context budget). TTSR
stands for **Trigger-based Skill & Rule** injection — the system prompt only
loads an anchor index, and matching trigger words inject corresponding content.

## The Problem

Loading all memory, skills, and configuration into the system prompt causes:

- Context overflow (128K token limits exceeded with 200+ skills)
- Degraded reasoning quality (too much noise in context)
- Slow token generation (longer prompts = slower responses)
- Wasted tokens on irrelevant information

## The Solution: Four-Layer Hierarchy

| Layer | Name | Content | Load Strategy | Size |
|-------|------|---------|---------------|------|
| 0 | Impression | Short-term task state, kanban | Always loaded | ~500 tokens |
| 1 | Anchor | Trigger rule index (keyword → page) | Always loaded | ~500 tokens |
| 2 | Instinct | Frameworks, constitutions, analysis methods | Load on trigger match | Variable |
| 3 | Skill/Memory | Specific operations, API configs, env facts | Load on trigger match | Variable |

### How It Works

1. **System prompt always contains**: Impression layer + Anchor index
   (~1000 tokens total)
2. **Trigger word matching**: When user input contains words that match anchor
   entries, inject the corresponding Instinct or Skill page
3. **Release after use**: Once the task is complete, the injected content is
   no longer in context

### Anchor Index Format

```markdown
# TTSR Anchor Index

## Instinct Triggers
| Trigger Words | Page | Purpose |
|---------------|------|---------|
| 股票, A股, 交易, 板块 | trading-constitution | 交易宪法 |
| 架构, 设计, 重构 | deep-work-layers | L0-L5 分层框架 |

## Skill Triggers
| Trigger Words | Skill | Purpose |
|---------------|-------|---------|
| docker, 部署, 容器 | vite-spa-deploy | SPA 部署 |
| 爬取, 抖音, 公众号 | web-scraping-methodology | 内容提取 |
```

## Implementation Rules

### 1. Memory Content Guidelines

- **Declarative facts, not instructions**: "User prefers concise responses"
  ✓ vs "Always respond concisely" ✗
- **Active rules only**: Remove facts that have landed in code/config
- **No completed-work logs**: Memory is for facts that still matter, not
  history of what was done

### 2. Skill Management

- **Create skill when**: Complex task succeeded (5+ tool calls), errors
  overcome, user-corrected approach worked
- **Patch skill immediately**: If you used a skill and found it outdated,
  fix it now
- **Delete when obsolete**: Skills that aren't maintained become liabilities

### 3. Evolution Tracking

Skills evolve through three stages:

1. **Understood** → Read the skill, understood the concept
2. **Proficient** → Successfully used in 3+ tasks
3. **Instinct** → Behavior changed automatically without loading

When a skill reaches Instinct level:
- Condense it into the anchor index as a trigger rule
- Or promote to an Instinct page (always-available framework)

### 4. Task State Board

For tasks with 3+ steps, maintain a task kanban:

```markdown
| Task ID | Description | Status | Current Step | Notes | Updated |
|---------|-------------|--------|--------------|-------|---------|
| T-001   | ...         | ...    | ...          | ...   | ...     |
```

Update immediately when status changes. Read at session start.

## Migration from Flat Memory

If migrating from a flat `MEMORY.md` file:

1. **Parse existing entries** with the `§` delimiter (or similar)
2. **Categorize**: preferences → Impression, lessons → Skill/Memory,
   frameworks → Instinct
3. **Build anchor index**: Extract trigger words from each entry
4. **Create bridge script**: Sync old format to new during parallel operation
5. **Progressive cutover**: Run both systems in parallel for ~1 week, then
   switch the injection source

## Context Budget Math

For a 2GB server agent:

- System prompt: ~1000 tokens (Impression + Anchor)
- On trigger match: +2000-5000 tokens (specific Instinct/Skill)
- Total per turn: ~3000-6000 tokens (well within 128K limit)
- Without TTSR: ~50K+ tokens (all 200+ skills loaded)

## Anti-Patterns

- Loading all skills into system prompt "just in case"
- Using imperative phrasing in memory ("Always do X")
- Keeping completed work logs in memory
- Not updating skills when they are found outdated during use
- Skipping the anchor index — without it, TTSR doesn't work
