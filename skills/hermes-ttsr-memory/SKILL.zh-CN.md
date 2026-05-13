---
name: hermes-ttsr-memory
description: 面向资源受限 agent 的触发式分层记忆架构（TTSR）。通过触发词匹配按需加载记忆，让 200+ skills 下的 system prompt 仍保持在 12K tokens 以内。四层结构：Impression -> Anchor -> Instinct -> Skill/Memory。
---

# Hermes TTSR 记忆架构

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md)

当你需要为资源受限环境中的 agent 设计记忆系统时使用这个 skill，例如 2GB
内存、上下文预算有限、skills 数量很多的场景。

TTSR 指 **Trigger-based Skill & Rule** injection：system prompt 默认只加载锚点索引，命中触发词时才注入对应内容。

## 问题

把所有 memory、skills 和配置都塞进 system prompt 会导致：

- 上下文溢出，200+ skills 很容易逼近或超过 128K token 限制
- 推理质量下降，太多无关内容会变成噪声
- token 生成变慢，prompt 越长响应越慢
- 大量 token 浪费在当前任务不需要的信息上

## 方案：四层结构

| 层级 | 名称 | 内容 | 加载策略 | 大小 |
|---|---|---|---|---|
| 0 | Impression | 短期任务状态、kanban | 默认加载 | ~500 tokens |
| 1 | Anchor | 触发规则索引，keyword -> page | 默认加载 | ~500 tokens |
| 2 | Instinct | 框架、宪法、分析方法 | 命中触发词后加载 | 可变 |
| 3 | Skill/Memory | 具体操作、API 配置、环境事实 | 命中触发词后加载 | 可变 |

### 工作方式

1. **system prompt 默认包含**：Impression 层 + Anchor 索引，总计约 1000 tokens。
2. **触发词匹配**：用户输入命中 anchor entry 时，注入对应 Instinct 或 Skill 页面。
3. **用完释放**：任务完成后，不再把注入内容留在上下文里。

### Anchor 索引格式

```markdown
# TTSR Anchor Index

## Instinct Triggers
| Trigger Words | Page | Purpose |
|---------------|------|---------|
| 股票, A股, 交易, 板块 | trading-constitution | 交易宪法 |
| 架构, 设计, 重构 | deep-work-layers | L0-L5 分层框架 |

## Skill Triggers
| Trigger Words | Skill | Purpose |
|---------------|-------|---------|
| docker, 部署, 容器 | vite-spa-deploy | SPA 部署 |
| 爬取, 抖音, 公众号 | web-scraping-methodology | 内容提取 |
```

## 实现规则

### 1. 记忆内容

- **声明事实，不写命令**：写“User prefers concise responses”，不要写“Always respond concisely”。
- **只保留活跃规则**：已经落进代码或配置的事实应移除或降级为归档。
- **不保存完成日志**：memory 存仍然有用的事实，不存“做过什么”的流水账。

### 2. Skill 管理

- **创建 skill 的条件**：复杂任务成功、克服明显错误、用户纠正后的做法被验证有效。
- **发现过时立即 patch**：用到某个 skill 时发现它不准，就在当前任务内修。
- **过时就删除或归档**：不维护的 skill 会变成负债。

### 3. 进化跟踪

Skills 经过三个阶段：

1. **Understood**：读过 skill，理解概念。
2. **Proficient**：在 3+ 个任务中成功使用。
3. **Instinct**：无需加载也能自然改变行为。

当 skill 达到 Instinct 层级时：

- 把它压缩成 anchor index 的触发规则
- 或提升为 Instinct 页面，成为常用框架

### 4. 任务状态板

对 3 步以上任务维护任务看板：

```markdown
| Task ID | Description | Status | Current Step | Notes | Updated |
|---------|-------------|--------|--------------|-------|---------|
| T-001   | ...         | ...    | ...          | ...   | ...     |
```

状态变化后立即更新，会话开始时先读取。

## 从扁平 Memory 迁移

如果从单个 `MEMORY.md` 迁移：

1. 用 `§` 或类似分隔符解析现有条目。
2. 分类：preferences -> Impression，lessons -> Skill/Memory，frameworks -> Instinct。
3. 建 anchor index：从每条内容提取触发词。
4. 写桥接脚本：并行期同步旧格式和新格式。
5. 渐进切换：两套系统并行约一周，再切换注入来源。

## 上下文预算

对 2GB server agent：

- System prompt：约 1000 tokens（Impression + Anchor）
- 触发命中：增加 2000-5000 tokens（具体 Instinct/Skill）
- 单轮总量：约 3000-6000 tokens
- 不使用 TTSR：可能超过 50K tokens（一次加载 200+ skills）

## 反模式

- “以防万一”把所有 skills 加进 system prompt
- 在 memory 里写 imperative 指令
- 把完成工作日志长期留在 memory
- 发现 skill 过时时不更新
- 跳过 anchor index；没有索引，TTSR 就跑不起来
