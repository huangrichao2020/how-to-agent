# 工作记忆预算控制：Intent Budget vs Scene FIFO 互补模型

## Purpose

双 agent（GA + Hermes/小云）独立验证的工作记忆膨胀控制方法论。GA 用 intent-based token budget（按意图 profile 预封顶：lightweight_ack 3600字 到 dream 17200字，5 维度独立上限），Hermes 用 per-scene surface budget（场景内 FIFO 柔性替换，超预算自动淘汰最旧条目）。两种方式互补：意图级刚性上限确保总量可控，场景内新进旧出保持上下文新鲜度。完整工作记忆控制面 = intent 级封顶 + scene 级淘汰。

## Proven By

['GA token_budget.py 8 种意图 profile × 5 维度字符预算表已落地运行', '小云 per-scene surface budget POC 跑通，trigger 日志 116 条实证', '工具裁剪 80/20 验证通过，tool_schema_budget.py 从 57 裁到 22', '429 根因：双 session 高 token 并发，方法论实证']

## Reusable Procedure



## When To Use

Use when a future agent faces the same practical situation.

## Guardrails

Treat this as a living method: use judgment, adapt to the current repo/runtime, and update after real feedback.

## Sources

- none provided
