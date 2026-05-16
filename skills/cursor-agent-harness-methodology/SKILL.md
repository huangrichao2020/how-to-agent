---
name: cursor-agent-harness-methodology
description: Cursor Agent Harness 工程方法论 — 动态上下文发现、文件原语交互、长输出落盘、A/B 评估。用于优化 Agent 工具链和上下文管理。
tags: [agent, harness, context-management, cursor]
version: "1.0"
---

# Cursor Agent Harness 工程方法论

## 触发条件
- 需要优化 Agent 的上下文管理策略
- 工具输出过长导致截断丢失关键信息
- 需要评估 Agent 改进效果（Keep Rate / Follow-up 分析）
- 参考 Cursor 官方博客三篇：Harness / Dynamic Context / Semantic Search

## 核心原则

### 1. 动态上下文发现 (Dynamic Context Discovery)
**旧范式**：把所有东西塞进 system prompt（目录结构、语义片段、附件）。
**新范式**：静态上下文只留 OS/git/当前文件，其余让 agent 按需拉。

**落地做法**：
- **长工具响应落盘**：输出超限时写文件，给 agent tail/cat 工具自己读
- **压缩反悔通道**：上下文压缩后把原始历史挂为文件，agent 可回溯
- **Skill 按需加载**：system prompt 只放 name+desc，需要时 grep 拉文件
- **MCP 工具描述文件化**：system prompt 只放名字，描述存文件夹按需查
- **终端历史文件化**：终端输出同步到文件系统，agent 自己 grep

**统一哲学**：**文件是 LLM 工具的最佳交互原语**。agent 擅长 grep/cat/tail，复用这种能力比搞新抽象更稳。

### 2. 评估体系
- **离线 eval**：自建评估集 + 公开 benchmark（只能近似真实）
- **线上 A/B**：硬指标（延迟/token/工具调用数/缓存命中率）
- **软指标硬测**：
  - **Keep Rate**：agent 写的代码过段时间还有多少留在用户代码库
  - **Follow-up 分析**：用 LLM 读用户下一句话判断满意度（"接着做"=好，甩 stack trace=翻车）

### 3. 可观测性
- **Context Rot**：工具调用失败的错误信息留在上下文里吃 token + 污染判断
- **错误分类**：
  - InvalidArguments/UnexpectedEnvironment → 模型自己搞错
  - ProviderError → 第三方挂了
  - UserAborted/Timeout → 用户取消/超时
  - **未知错误 → 一律视为 harness bug，必须报警**
- **自动修**：每周跑 Cloud Agent 扫日志建 ticket

### 4. 模型切换
- 每个模型专属 harness（OpenAI 用 patch，Anthropic 用字符串替换）
- **别中途切模型**：历史是 OOD 数据，cache miss 又慢又贵
- **Subagent 优先**：干净上下文 + 指定模型 + 隔离运行

### 5. 语义搜索
- grep 和语义搜索是搭配关系，不是替代
- 自训 embedding 飞轮：用 agent 真实轨迹训练，靠"工作流里什么最有用"而非"代码相似度"

## Hermes 落地清单

### 已实现
- [x] TTSR 锚点索引 = Skill 按需加载
- [x] delegate_task = Subagent 隔离
- [x] terminal 长输出落盘（2026-05-10 更新）

### 待优化
- [ ] Keep Rate 指标：跟踪 agent 生成代码的留存情况
- [ ] Follow-up 分析：用 LLM 对用户后续消息打分
- [ ] 错误分类细化：区分 provider 错误、参数错误、环境矛盾
- [ ] 语义搜索 embedding 微调：基于 agent 真实轨迹

## 参考资料
- [Continually improving our agent harness](https://cursor.com/blog/agent-harness)
- [Dynamic context discovery](https://cursor.com/blog/dynamic-context-discovery)
- [Improving agent with semantic search](https://cursor.com/blog/semantic-search)
- [知乎解读](https://zhuanlan.zhihu.com/p/2033520572144030920)
