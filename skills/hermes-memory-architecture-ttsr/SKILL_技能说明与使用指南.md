---
name: hermes-memory-architecture-ttsr
category: architecture
description: Hermes Agent 分层记忆架构与 TTSR（触发式规则注入）优化方案。用于在 2GB 内存约束下最大化上下文效率，实现“印象-锚点-本能-技能”四层管理。
yao_category: "AI学习"
---

# Hermes 分层记忆架构与 TTSR 优化

## 1. 核心痛点
在 2GB 内存的阿里云服务器上，全量加载 System Prompt（BOOT.md + 所有 Skills）会导致：
- **OOM 风险**：长对话或多子代理并发时内存溢出。
- **推理延迟**：过长的上下文拖慢模型响应。
- **干扰增加**：无关规则占据注意力，导致模型执行不精准。

## 2. 四层记忆架构 (Impression-Anchor-Instinct-Skill)

### L1: 印象 (Impression)
- **载体**: gbrain `type='impression'` 页面。
- **内容**: 短期会话状态、用户当前情绪、最近任务进度。
- **生命周期**: 随会话结束或任务完成而归档/过期。

### L2: 锚点 (Anchor) - TTSR 核心
- **载体**: gbrain 页面 `ttsr-anchor-index`。
- **内容**: 轻量级索引表（~500 tokens），包含：触发词 | 加载目标 | 类型 | 说明。
- **作用**: System Prompt 中**仅保留此表**。模型通过匹配触发词决定是否需要加载更深层的规则。

### L3: 本能 (Instinct)
- **载体**: 核心分析框架、交易宪法、BOOT.md、决策逻辑。
- **内容**: 决定“怎么做”的底层逻辑（如：人性/供需框架、三共振原则）。
- **加载方式**: 当锚点匹配到相关触发词（如“股票”、“大盘”）时，动态注入。

### L4: 技能/记忆 (Skill/Memory)
- **载体**: `skills` 目录下的 `.md` 文件 + `memory` 工具存储的持久化事实。
- **内容**: 具体操作步骤、API 用法、环境配置、项目约定。
- **加载方式**: 任务明确需要时，通过 `skill_view` 或 `memory` 检索加载。

## 3. TTSR (Trigger-Based Rule Injection) 实施流程

1. **初始化**: Gateway 启动时，System Prompt 只包含 L2 锚点索引表和 L1 印象摘要。
2. **监测**: 每一轮对话前，检查用户输入是否包含锚点表中的“触发词”。
3. **注入**: 
   - 若匹配（如用户问“A股走势”），自动读取并注入对应的 L3 本能（交易宪法）和 L4 技能（行情查询 skill）。
   - 若不匹配，保持极简上下文。
4. **释放**: 任务完成后，注入的详细规则不再保留在后续对话的历史中（依靠模型自身的短期记忆或重新触发）。

## 4. 关键触发器映射示例

| 触发词 | 加载目标 | 类型 |
|--------|----------|------|
| `股票/大盘/A股` | `a-stock-market-analysis-framework`, `trading-methodology-complete-system` | 本能 |
| `抖音/截图` | `douyin-content-extraction-methodology` | 技能 |
| `部署/重启` | `BOOT.md`, `hermes-agent-upgrade` | 本能 |
| `patch/编辑` | `Hashline Edit Pattern` | 技能 |
| `子代理/delegate` | `Delegate Task Toolset Pruning` | 规则 |

## 5. 收益验证
- **上下文节省**: 日常对话减少 30%~50% 的 System Prompt 占用。
- **稳定性**: 2GB 内存下支持更长的对话历史和更多的子代理并发。
- **精准度**: 模型只在需要时看到详细规则，减少了“幻觉”和指令冲突。

## 6. 维护建议
- **新增规则时**: 必须先在 `ttsr-anchor-index` 中添加触发词映射，而不是直接塞进 BOOT.md。
- **定期清理**: 检查 gbrain 中的 impression 页面，归档过期的短期状态。