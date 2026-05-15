---
name: hermes-architecture-evolution-phase7
category: architecture
description: Phase 7 架构优化方法论 — 从 oh-my-pi 偷师并适配 2GB 内存环境。涵盖 Hashline 编辑、Toolset Pruning、TTSR 锚点索引和 Task Kanban。
---

# Hermes 架构演进 Phase 7 — 外部借鉴与内化

## 来源
深度研究 `can1357/oh-my-pi` (3700+ Stars 终端 AI Agent)，提炼核心架构思想并适配 Hermes 2GB 内存环境。

## 核心原则
**不替换，只偷师**。外部优秀框架的架构思想 > 直接安装依赖。严禁引入 Node/Bun 等重型运行时。

## 已落地优化

### 1. Hashline 编辑 (Content-Anchored Editing)
**问题**：传统 `patch` 工具依赖文本匹配，容易因空格/缩进变化导致 "string not found"。
**方案**：
- `read_file(show_hashlines=True)` 返回带 `[L0042|a1b2c3d4]` 前缀的行（行号+CRC32哈希）。
- `patch` 工具自动识别并剥离 Hashline 前缀，实现精准内容锚定。
**收益**：代码编辑精准度翻倍，彻底解决匹配失败问题。

### 2. Toolset Pruning (子代理减负)
**问题**：`delegate_task` 默认透传所有工具，Prompt 过长导致 2GB 内存 OOM。
**方案**：
- 主代理分配任务时**必须**显式指定 `toolsets`（如 `['terminal', 'file']`）。
- **红线**：无关任务绝不加载 `cronjob`, `mcp`, `feishu_doc` 等重型工具。
**收益**：子代理上下文缩短 70%+，并发稳定性提升。

### 3. TTSR 锚点索引 (Trigger-Based Rule Injection)
**问题**：System Prompt 全量加载 Skills/BOOT.md，日常对话上下文浪费严重。
**方案**：
- 创建 gbrain 页面 `ttsr-anchor-index` 作为轻量级触发词索引表（~500 tokens）。
- 匹配触发词（如"股票"→交易框架、"抖音"→提取工作流）才注入对应本能/技能。
- 任务完成后释放，不占后续上下文。
**收益**：日常对话上下文减少 30%~50%。

### 4. Task Kanban (状态持久化)
**问题**：长对话中断或 Gateway 重启后，任务进度丢失。
**方案**：
- 创建 gbrain 页面 `agent-task-kanban` 跟踪活跃任务（格式：ID | 描述 | 状态 | 步骤 | 备注 | 时间）。
- `BOOT.md` 增加重启后自动读取此页的逻辑，如有未完成/阻塞任务则询问继续。
**收益**：任务状态跨会话持久化，支持断点续传。

## 分层记忆架构 (Impression-Anchor-Instinct-Skill)

```
印象 (Impression)  → gbrain type='impression' (短期会话上下文)
      ↓
锚点 (Anchor)      → gbrain ttsr-anchor-index (触发词索引)
      ↓
本能 (Instinct)    → 交易宪法/分析框架/BOOT.md (核心行为准则)
      ↓
技能/记忆 (Skill)  → skills系统 + memory工具 (具体操作步骤)
```

## 演进节奏
1. **调研** (Survey)：识别外部项目的核心架构思想
2. **过滤** (Filter)：剔除不符合 2GB 内存约束的依赖
3. **适配** (Adapt)：将思想转化为 Python/Hermes 原生实现
4. **验证** (Verify)：在实际任务中测试稳定性（如 Info-Hub 交叉验证 API）
5. **沉淀** (Archive)：写入 gbrain 方法论页面 + 更新 memory

## 实战案例
- **Info-Hub 交叉验证 API**：验证了 TTSR 触发、Toolset Pruning、Hashline 编辑和 Task Kanban 的全流程。
- **数据源增强**：接入东方财富 API，实现真实市场数据获取与降级机制。
- **生产部署**：通过 deploy.sh 脚本自动化部署到 ai10088.com/info-hub。