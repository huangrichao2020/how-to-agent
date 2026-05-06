---
name: codex-state-maintenance
description: 当 Codex 或本地 coding agent 因 sessions、logs、worktrees、metadata、config paths 膨胀而变慢、难恢复时使用。也适用于把 keep-codex-fast 这类本地状态维护项目的经验转成本地操作习惯。
---

# Codex State Maintenance

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md)

使用这个 skill，是为了让本地 agent state 保持快速、可恢复，并且让下一个 agent 容易接手。

原则是：

```text
先检查。先 handoff，再 archive。先 backup，再 apply。archive 代替 delete。
```

## 什么时候使用

这些场景使用本 skill：

- Codex 或其他本地 agent 启动、搜索、恢复上下文变慢。
- active sessions、logs、worktrees、caches 或 metadata 变大。
- 用户要求清理、归档、压缩、提速或修复本地 agent state。
- 你在研究 `keep-codex-fast` 这类维护项目，需要把经验转成本地操作习惯。

不要把它当成可以立即修改本地状态的授权。

## 默认流程

### 1. 第一轮只检查

第一轮永远是报告。

检查并总结：

- active 和 archived sessions 体积
- 最大的 sessions 或 logs
- stale worktrees
- 旧 generated caches
- 膨胀的 thread metadata
- 指向不存在路径的 config entries
- 正在运行的 Codex、agent、editor 或 dev-server processes

这一步不 move、不 delete、不 trim、不 repair。

### 2. 识别需要 handoff 的工作

归档旧 active work 前，如果对话里仍然有有用状态，就先创建或更新 handoff note。

handoff 至少包含：

- project path
- branch 和 git status
- 当前目标
- 已验证内容
- 剩余风险
- 精确 reactivation prompt

如果写不出有用 handoff，不要静默归档这段工作。

### 3. 修改 agent-owned state 前先问

apply 前，按这个结构说明：

```text
我可以开始执行本地状态维护。

计划修改：
- ...

备份：
- ...

回滚：
- ...

不会触碰：
- credentials、tokens、private config、上面未列出的 transcripts

你同意吗？
```

不要把模糊的“继续”当成授权。

### 4. 先 backup，再 apply

任何写入前：

- 创建 timestamped backup
- 记录 moved 或 changed files 的 manifest
- 写 restore commands 或 restore script
- 避免在 Codex 或目标 agent 正在写入状态时 apply

如果 agent app 正在运行，优先停在报告阶段，并告诉用户 apply 前需要关闭什么。

### 5. 用 archive 或 rotate 代替 delete

优先可逆操作：

- 把旧 sessions 移到 archive
- 把 stale worktrees 移出 active search paths
- rotate large logs
- 只在明确安全时 prune generated caches

删除必须有用户明确授权，并说明会失去什么。

### 6. Metadata repair 单独处理

metadata repair，比如裁剪过大的 title 或 preview 字段，不属于普通清理。

执行前：

- 说明影响哪个 metadata
- 说明 transcripts 是否保持完整
- 先备份 database 或 state file
- 单独请求用户批准这个 repair step

## 定期维护

定期任务默认只做 report-only：

```text
Run an inspect-only local agent state maintenance report.
Summarize large, stale, risky, and safe-to-archive items.
Do not move, delete, trim, or repair anything unless the user explicitly
approved that mutation for this run.
```

除非用户明确要求承担风险，不要安排自动执行写入的清理任务。

## 未解析来源

如果用户命名了一个外部项目，但你解析不到：

- 记录搜索过的精确名称
- 说明查过哪些 registry 或 host
- 不要只根据名字推断经验
- 当来源重要时，请用户补链接

## 完成检查

宣布完成前检查：

- 已生成 inspect-only report，或说明为什么没生成
- 已识别需要 handoff 的工作
- 没有未经授权的 mutation
- 如果 apply，已存在 backup 和 restore path
- 已列出 changed files 或 archives
- 如果发生修改，已做 post-apply verification
- 未解析的外部来源已明确标注
