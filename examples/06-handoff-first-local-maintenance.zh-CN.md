# 示例 06：先交接再维护本地状态

[English](06-handoff-first-local-maintenance.md) · [简体中文](06-handoff-first-local-maintenance.zh-CN.md)

有些 agent 改进不是新增 runtime 功能，而是本地状态卫生：sessions、logs、worktrees、caches、metadata 慢慢膨胀，最后 agent 变慢、变脆。

`keep-codex-fast` 给我的核心启发不是“删旧数据”，而是：

> 先做 handoff。归档，不要删除。先报告安全，再应用修改。

## 研究来源

- `keep-codex-fast`: https://github.com/vibeforge1111/keep-codex-fast
- `heat-on-content`: 这次按精确名称搜索公开 GitHub 和 npm，没有解析到可信项目。用户给出链接前，把它当成未知来源。

第二行很重要。会学习的 agent 应该保留不确定性，而不是从一个名字硬编模式。

## 用户意图

用户让 agent 研究外部项目，但随后明确说重点是“你本人学习”。

这会改变输出形态：

- 不要默认把外部项目装进本地 runtime
- 不要默认运行清理工具
- 提取操作习惯
- 把习惯写入能力库
- 把未解析来源显式留下来

## Agent 应该学会什么

### 1. 先报告，再变更

第一轮应该只检查，不修改。

对本地 agent 状态来说，报告至少回答：

- active session store 有多大
- 哪些 sessions 或 logs 占主要体积
- 是否有 stale worktrees
- 是否有旧 runtime metadata 膨胀
- config path 是否指向不存在的位置
- agent app 或 dev process 是否仍在运行

报告是决策面，不是自动清理的前奏。

### 2. 先 handoff，再 archive

旧 active chats 里可能还有有价值的项目状态。把它们移出热路径前，先写一个短 handoff：

- 项目或任务名
- 当前状态
- 重要文件和分支
- 已验证命令
- 未解决风险
- 给未来 agent 的恢复 prompt

如果一段对话没有 handoff，直接归档也许会让下一个 agent 更快，但也可能让它更无知。

### 3. 先备份，再 apply

修改本地 agent 状态前，必须有备份和明显的恢复路径。

优先：

- timestamped backup directories
- 记录每个移动文件的 manifests
- restore scripts 或精确 restore commands
- apply 后再跑一次验证报告

避免：

- 把删除当作第一清理动作
- agent app 仍在运行时修改 live state
- 静默 metadata repair
- 未经明确请求就清理 credentials、tokens 或 private config

### 4. 用 archive、move、rotate 代替 delete

清理的目标是降低热路径负载，同时保存历史。

好的动作：

- 把旧 sessions 移到 archive 区
- 把 stale worktrees 移出 active discovery paths
- 带 manifest 轮转 logs
- 只 prune 明确无用的 generated 或 derived files

删除应该很少发生，而且要明确、实际可恢复。

### 5. Metadata repair 是单独权限

有些卡顿来自本地展示 metadata 过大，比如 thread title 或 preview 字段。修这些 metadata 不等于删除 transcript，但仍然是在改 agent-owned state。

把它作为可选 repair：

- 说明会裁剪什么 metadata
- 说明 transcripts 保持完整
- 先备份
- 明确请求用户同意

### 6. 定期任务默认只做报告

每周或双周维护提醒有价值。自动执行有写入的清理则风险大很多。

安全默认是：

```text
Run an inspect-only local state maintenance report.
Summarize what is large, stale, risky, or safe to archive.
Do not move, delete, trim, or repair anything unless I explicitly approve it.
```

## 可复用版本

```text
研究 [local-state maintenance project]。

提取操作习惯，不复制工具实现。

针对我们的 agent，把经验变成 handoff-first maintenance workflow：
先 inspect-only report，再为旧 active work 写 handoff，再 backup，
再 archive 或 rotate 而不是 delete，最后做 post-apply verification。

如果建议 metadata repair，把它和普通维护分开，并明确请求用户授权。

如果某个命名来源无法解析，记录这个不确定性，不要从名字硬编经验。
```

## 完成测试

只有当下一个 agent 能回答这些问题时，这次学习才算留下来了：

- 维护 skill 在哪里？
- 默认不修改状态的 workflow 是什么？
- apply 前必须备份什么？
- 哪些 work 归档前必须写 handoff？
- 哪个来源没有解析到，需要用户补链接？

如果答案只存在聊天里，agent 还没有真正学会。
