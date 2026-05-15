---
name: a-stock-limit-up-tracker
description: "A股涨停板实时追踪与结构化分类技能。从数据源获取涨停数据，按板块分组并识别龙头、身位、跟风股。适用于盘中异动监控及盘后复盘。Trigger: 涨停板/龙头/连板/涨停追踪/盘中监控. Do NOT trigger for 非交易时段查询、个股分析、或非 A 股市场。"
version: 2.1.0
---

# A股涨停板实时追踪与分类

## 一句话版本

自动化追踪 A 股涨停板，按板块分组并识别龙头/身位/跟风股。核心：MX API 获取数据 + reason 字段真实逻辑 + 梯队结构分类。龙头定方向，身位做套利，退潮期空仓。

## 如何使用本技能

1. **先运行决策树**: `checklists/decision-tree.md`
2. **从 philosophy 开始**: 确认核心逻辑和关键原则
3. **按需加载 references**: 匹配问题到数据解析或坑文档
4. **交付前运行**: `checklists/ship-readiness.md`

## 核心反模式（看到这些立刻停下）

- **"直接用行业分类汇报"** → reason 字段才是编辑部人工标注的真实逻辑，优先用 reason
- **"不剔除 ST 股"** → ST 股有独立行情，会误导主线判断
- **"配额耗尽还继续调用"** → 每日 20 次/Key，检查配额再调用
- **"概念字段直接按管道符分割"** → 含顿号会破坏分割，优先提取稳定字段
- **"非交易时段查实时涨停"** → 数据不更新，无意义

## 配套文件

- `references/01-philosophy.md` — 追踪哲学 + 核心逻辑
- `references/02-data-parsing.md` — MX API 数据解析详解
- `references/03-pitfalls.md` — 常见坑（配额/解析/推送）
- `checklists/decision-tree.md` — 运行时机决策树
- `checklists/ship-readiness.md` — 交付前检查清单
