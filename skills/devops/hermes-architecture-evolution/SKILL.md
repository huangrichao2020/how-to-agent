---
name: hermes-architecture-evolution
description: 借鉴外部优秀 Agent 框架（如 oh-my-pi）的架构思想，适配 Hermes 2GB 内存约束并进行内化落地的标准流程。
version: 1.0.0
tags: ["architecture", "optimization", "context-management", "oh-my-pi"]
---

# Hermes 架构演进工作流

## 触发条件
- 发现新的优秀开源 Agent 项目（如 oh-my-pi, claude-code, opencode）
- 用户要求"深度研究某项目看是否有帮助"
- 当前 Hermes 遇到性能瓶颈（OOM、上下文过长、编辑失败）

## 核心原则
**不替换，只偷师**。严禁直接安装重型依赖（Node/Bun/Langchain），必须将思想转化为 Python/Hermes 原生实现。

## 执行步骤

### 1. 调研 (Survey)
- 拉取目标项目代码，分析其 `README`、核心工具实现、Prompt 结构
- 识别 3-5 个核心架构亮点（如 Hashline 编辑、TTSR、Subagent 隔离）

### 2. 过滤 (Filter)
- **硬件约束检查**：服务器仅 2GB RAM，禁止引入任何非 Python 运行时或重型 AI 框架
- **兼容性评估**：判断哪些特性可以直接迁移，哪些需要改造

### 3. 适配 (Adapt) - 已验证的落地模式 (Phase 7)
| 外部特性 | Hermes 落地方式 | 载体 | 状态 |
|----------|----------------|------|------|
| Hashline Edits | `read_file` 返回带 CRC32 哈希的行号；`patch` 自动清洗哈希前缀 | 内置工具增强 | ✅ 完成 |
| TTSR (触发式规则) | gbrain `ttsr-anchor-index` 页面存触发词映射；System Prompt 只保留索引表 | gbrain + BOOT.md | ✅ 完成 |
| Toolset Pruning | `delegate_task` 强制显式指定 `toolsets`，默认不给重型工具 | 记忆规则 + System Prompt | ✅ 完成 |
| Task Kanban | gbrain `agent-task-kanban` 页面跟踪进度；BOOT.md 重启后自动读取恢复 | gbrain + BOOT.md | ✅ 完成 |
| 实战验证 | 交叉验证 API (`/api/stock/cross-validation`) 迭代测试 | Info-Hub 项目 | ✅ 完成 |

### 4. 验证 (Verify)
- 在实际任务中测试新架构（如 Info-Hub 迭代、盘前报告生成）
- 观察上下文长度变化、子代理启动速度、编辑成功率

### 5. 沉淀 (Archive)
- 创建/更新 gbrain 方法论页面：`hermes-architecture-evolution-methodology`
- 更新 `agent-task-kanban` 记录完成状态
- 写入长期记忆：分层架构规则 (Impression-Anchor-Instinct-Skill)

## 分层记忆架构规范
```
印象 (Impression)  → gbrain type='impression' (短期会话上下文)
      ↓
锚点 (Anchor)      → gbrain ttsr-anchor-index (触发词索引，~500 tokens)
      ↓
本能 (Instinct)    → 交易宪法/分析框架/BOOT.md (核心行为准则)
      ↓
技能/记忆 (Skill)  → skills系统 + memory工具 (具体操作步骤)
```

## 注意事项
- 每次优化后必须更新 `agent-task-kanban`，确保重启后可恢复
- 严禁在 2GB 环境下运行 Bun/Node 进程，所有逻辑必须用 Python 或 Shell 实现
- TTSR 触发词映射表需定期维护，新增领域时同步更新 `ttsr-anchor-index`
- **部署依赖陷阱**：`deploy.sh` 只做 `git pull` 和 `npm build`，**不会自动安装新增的 Python 依赖**（如 `requests`）。新增外部依赖后，必须在部署前手动在后台 venv 中安装：`cd /home/deploy/info-hub/backend && source .venv/bin/activate && pip install <pkg>`
- **Cron 调度格式**：cron 表达式用标准 5 字段（分 时 日 月 周），例如 `30 8 * * *` 表示每天 8:30。不要用 `0 8 30 * * *`（这是无效格式）
- **前端路由添加三部曲**：新增前端面板时必须同步修改三处：`types/index.ts`（Section 类型）→ `config/sections.ts`（元数据+顺序）→ `AppShell.tsx`（lazy import）。缺一不可，否则 TypeScript 编译报错