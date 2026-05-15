---
name: skill-design-template
description: 高质量 Skill 设计模板 — 借鉴 native-feel-skill 结构，用于编写/审查 Hermes Agent Skill。
version: 1.0.0
---

# 高质量 Skill 设计模板

源自 yetone/native-feel-skill 的 SKILL.md 结构分析。

## 结构要素

### 1. Frontmatter（强制）
```yaml
name: 简洁动词-名词-组合
description: "Use when..." 开头 + 触发词 + Do NOT trigger 条件
```

### 2. How to use this skill（使用指南）
分层加载指引，不要一次性 dump 全部内容。格式：
- 从 philosophy 开始
- 匹配问题到具体 reference 文件
- 推荐前运行 decision tree
- 交付前运行 ship readiness check

### 3. The one-paragraph version（一句话版本）
用一段话说清楚这个 skill 解决的核心问题和架构选择。

### 4. Core anti-patterns（核心反模式）
当看到用户做这些事时，立刻停下来反问：
- 格式："Let's just do X" → 为什么错 + 正确做法引用
- 至少 5 条，覆盖最常见的坑

### 5. Output style（输出风格约束）
指导 agent 如何输出：
- 引用具体信条编号
- 给出 trade-off（没有免费午餐）
- 不确定时先跑决策树

## 配套文件结构

```
skill-name/
├── SKILL.md                    # 主文件（上面结构）
├── references/                 # 分层参考资料
│   ├── 01-philosophy.md        # 哲学/原则
│   ├── 02-architecture.md      # 架构细节/API 参考
│   ├── 03-pitfalls.md          # 常见坑
│   └── ...
├── checklists/                 # 检查清单
│   ├── decision-tree.md        # 决策树（适用性判断）
│   └── ship-readiness.md       # 交付检查
└── templates/                  # 模板
```

## 实战案例（已升级 skill）

以下 skill 已按此模板完成升级，可作为参考：
- `a-stock-data` (v4.1.0) — A 股数据获取，含多源降级逻辑
- `self-healing-browser-extractor` (v1.3.0) — 浏览器自愈提取
- `douyin-content-extraction` (v2.2.0) — 抖音图文提取
- `wechat-article-extraction` (v2.0.0) — 微信文章提取
- `a-stock-limit-up-tracker` (v2.1.0) — 涨停板追踪

## 对比我们现有 skill 的差距

| 要素 | native-feel-skill | 我们现有 skill 平均 |
|------|-------------------|-------------------|
| 触发条件 | ✅ 精确（含 Do NOT） | ⚠️ 模糊 |
| 分层加载 | ✅ references 按需加载 | ❌ 全部 dump |
| 反模式 | ✅ 5+ 条具体反模式 | ❌ 几乎没有 |
| 一句话版本 | ✅ 有 | ❌ 没有 |
| Trade-off | ✅ 明确说出代价 | ⚠️ 暗示但不说 |
| 检查清单 | ✅ decision-tree + ship-readiness | ❌ 没有 |

## 吸收动作

1. **新 skill** 按此模板写
2. **高频使用的旧 skill** 逐步升级
3. **每个 skill** 必须有明确的 Do NOT trigger 条件
4. **复杂 skill** 必须有 references 分层 + checklists
