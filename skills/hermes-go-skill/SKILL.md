---
name: hermes-go-skill
description: 统一入口技能。用户只需说"开始任务"，自动识别阶段并路由到对应 Skill 组合。
version: "1.0.0"
metadata:
  hermes:
    tags: ["router", "orchestrator", "workflow"]
---

# GO - 统一任务入口

> **核心逻辑**：用户输入一句话 -> 自动识别阶段 -> 加载对应 Skill -> 执行。
> **零运行时**：纯 Markdown 规则，不依赖外部工具。

## 阶段识别规则

根据用户输入关键词匹配阶段：

| 阶段 | 关键词示例 | 加载 Skill 组合 |
|---|---|---|
| **1. 需求 (REQ)** | "写个", "做", "设计", "分析", "调研" | `horizontal-vertical-analysis`, `web-scraping-methodology` |
| **2. 设计 (DES)** | "架构", "方案", "结构", "数据库" | `agent-architecture-upstream-integration`, `software-development` |
| **3. 任务 (TASK)** | "计划", "拆分", "步骤", "todo" | `writing-plans`, `subagent-driven-development` |
| **4. 编码 (CODE)** | "改", "修", "bug", "代码", "写代码" | `autonomous-ai-agents`, `systematic-debugging`, `test-driven-development` |
| **5. 测试 (TEST)** | "测", "运行", "验证", "报错" | `requesting-code-review`, `systematic-debugging` |

## 执行流程

1. **识别阶段**：读取用户输入，匹配上述关键词。
2. **加载 Skill**：调用 `skill_view(name)` 加载对应组合。
3. **反问确认**：向用户确认任务目标、约束条件（如时间、质量要求）。
4. **执行**：按 Skill 指导执行任务。

## 示例

用户："帮我分析一下科创 50"
-> **识别**：阶段 1 (REQ)
-> **加载**：`horizontal-vertical-analysis`
-> **动作**：执行横纵深度研究

用户："帮我写个 API 接口"
-> **识别**：阶段 4 (CODE)
-> **加载**：`autonomous-ai-agents`, `api-design`
-> **动作**：执行编码规范

## 统一入口指令

用户只需发送：
`@hermes-go-skill 开始任务：[你的需求]`

或者直接说：
`开始任务：[你的需求]`
