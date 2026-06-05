# 阿里 OCR 方法论 → GA 自改 Code Review Skill

## Purpose

从 alibaba/open-code-review ⭐2667 提取6条核心设计思想：deterministic+LLM混合、7专用工具、按文件分块审查、结构化输出、session持久化、每语言规则。适配到GA Python自改场景，产出5步审查流程+重启前检查清单+prompt模板。

## Proven By

temp/skills/self-mod-code-review.md (229行) | temp/open-code-review/STUDY_NOTES.md | repo: alibaba/open-code-review

## Reusable Procedure



## When To Use

Use when a future agent faces the same practical situation.

## Guardrails

Treat this as a living method: use judgment, adapt to the current repo/runtime, and update after real feedback.

## Sources

- https://github.com/alibaba/open-code-review
