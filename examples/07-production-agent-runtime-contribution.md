# 示例 07：贡献生产级 Agent 运行时 Skill

[English](07-production-agent-runtime-contribution.md) · [简体中文](07-production-agent-runtime-contribution.zh-CN.md)

## 背景

当 agent 在本地作为持久化、物理级执行助手运行一段时间后，会沉淀出架构、记忆、委托、失败处理等方面的实践经验。这些经验值得反向贡献到 `how-to-agent` 项目中，让其他 agent 系统也能受益。

## 原始 prompt

```text
你深度学一下本地桌面的 how-to-agent，把你的精华和远程 hermes 的精华都更新进去
```

## 开发者意图

这句话要求 agent：
1. 先深度理解 how-to-agent 现有的结构和内容
2. 从自身实践（GenericAgent）和远程经验（Hermes）中提炼精华
3. 以符合项目风格的方式反向贡献，而不是简单复制

## 可复用版本

```text
深度研究 how-to-agent 项目的结构和现有 skills。

从你的运行实践中提炼出一个新的 skill，包括：
- 你做得好的架构模式
- 你踩过的坑和反模式
- 可复用的协议和规则

创建对应的 SKILL.md 和 SKILL.zh-CN.md，并更新 README 中的引用。
保持与现有 skill 一致的风格和深度。
```

## 本次贡献内容

Status note: this is a historical example. The original
`skills/production-agent-runtime/` package is no longer a live skill path in
this repository; the useful runtime material has since been folded into
`full-stack-agent-intelligence`, `ga-implementation-map`,
`agent-output-workbench`, `runtime-identity-correction`, and later GA repair
examples.

### 新增文件
- Historical path: `skills/production-agent-runtime/SKILL.md`
- Current related entries: `skills/full-stack-agent-intelligence/`,
  `skills/ga-implementation-map/`, `skills/agent-output-workbench/`,
  `skills/runtime-identity-correction/`

### 更新文件
- `README.md` — 目录树 + Skill package 列表
- `README.zh-CN.md` — 目录树 + 技能包列表 + 简介

### 核心内容
1. **三层架构** — 交互层 → 核心引擎 → 联邦委托
2. **分层记忆系统** — L0-L4 + Second Brain
3. **联邦委托系统** — delegate/swarm/session
4. **失败升级协议** — 1→2→3 次失败策略
5. **自愈与重启协议** — 进程监控 + 自动恢复
6. **工作记忆机制** — Checkpoint 防信息丢失
7. **反模式清单** — 8 条常见错误

## 验收检查

- [x] 新 skill 与当时的现有 skill 风格一致
- [x] 当时同时提供中英文版本
- [x] README.md 和 README.zh-CN.md 当时已更新
- [x] 后续精简时已从 README 默认索引移除旧路径
- [x] 当前可从相关 runtime/cognition skills 继续读取
- [x] 内容提炼自真实运行经验，不是空想

## 给下一个 agent 的提示

如果要继续完善这个 skill：
- 可以添加更多具体的代码示例
- 可以补充不同操作系统下的运行差异
- 可以添加性能调优和监控的最佳实践
