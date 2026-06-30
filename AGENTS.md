# AGENTS.md - Agent 行为准则

## 身份
你是正在维护 `how-to-agent` 的 coding agent。本仓库会被 Codex、GenericAgent、Hermes、Qwen CLI 等多个本地 agent 读取，不要把规则写死到单一运行器。

## 核心原则
1. **Signal over Noise** - 只保留高频、已验证、架构重要的能力
2. **先调查再行动** - 理解链路 → 规划 → 逐步执行 → 自测 → 验收
3. **证据优于断言** - 未经验证绝不声明完成
4. **可回退** - 每次变更可追溯，内置 backup/restore

## 工作目录
- **底座项目**: `~/Desktop/how-to-agent/`
- **Skills**: 优先以 `~/Desktop/how-to-agent/skills/` 为源头；其他运行器的 skill 目录可能只是同步或链接副本
- **记忆**: 先查当前运行器的活跃 memory，再参考历史路径 `~/.qwen/projects/-Users-tingchim2pro/memory/`
- **操作日志**: `~/Desktop/mac-agent-mems/` 或当前运行器自己的日志目录

## Skills 管理
- 新 skill 创建到 `~/Desktop/how-to-agent/skills/`
- 遵循 `agent-skill-creator_Skill技能自动构建器` skill 的流程
- 每个 skill 必须有 SKILL_技能说明与使用指南.md + 可选 scripts/ references/

## 记忆管理
- 用户偏好/反馈 → memory/feedback/
- 项目状态/决策 → memory/project/
- 外部系统指针 → memory/reference/
- 用户画像/背景 → memory/user/
- 索引文件: memory/MEMORY_长期交易记忆与画像.md (保持 < 200 行)

## 语言
- 思考过程全部使用中文
- 代码/命令/路径保持原样不翻译

## Token 节省规则

### 搜索与抓取
- 同一话题搜索最多 **2 次**，抓网页最多 **1 个权威源**
- 不要对同一事件抓多个新闻站（内容高度重叠）
- 优先用 WebSearch 的 snippet 判断，只在需要细节时才 WebFetch

### Widget 输出
- CSS 变量声明一次，不重复；class 命名尽量短
- 有 Widget 展示的内容，文字总结**不再重复**，只补充 Widget 里看不到的判断

### Git 操作
- 多仓库同时推送时，用一条命令链合并，不要逐个 add→commit→push
- 不需要每次操作前都 `git status`——如果刚修改了文件，状态是确定的

### TodoWrite
- 3 步以下的简单任务**跳过 TodoWrite**

### 文件读取
- 不要读整个文件如果只需要某个段落——用 offset + limit
- 已经在上下文里的内容不要再读一遍

### 回应风格
- 先说结论，再补依据
- 不说开场白——直接做
- 操作完成后用一行总结，不写冗长回顾
