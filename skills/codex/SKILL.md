---
name: codex
description: Delegate coding tasks to OpenAI Codex CLI agent. Use for building features, refactoring, PR reviews, and batch issue fixing. Requires the codex CLI and a git repository.
category: coding-agent
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Codex, OpenAI, Code-Review, Refactoring]
    related_skills: [claude-code, hermes-agent]
---

# Codex CLI

Delegate coding tasks to [Codex](https://github.com/openai/codex) via the Hermes terminal. Codex is OpenAI's autonomous coding agent CLI.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- OpenAI API key configured: `export OPENAI_API_KEY=sk-...`
- **Must run inside a git repository** — Codex refuses to run outside one
- Use `pty=true` in terminal calls — Codex is an interactive terminal app

## 执行步骤

1. 确认环境就绪：检查 Codex 安装和 API Key 配置
2. 选择执行模式：单次（`exec`）或后台（`background=true`）
3. 执行命令并监控进度
4. 处理可能出现的错误或异常
5. 清理临时工作区（如使用了 mktemp）

## One-Shot Tasks（示例）

```bash
# 示例：添加功能
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)

# 示例：临时项目（不需要已有仓库）
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

## Background Mode (Long Tasks)（示例）

```bash
# 示例：后台执行重构任务
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# 返回 session_id

# 监控进度
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# 发送输入（如果 Codex 提问）
process(action="submit", session_id="<id>", data="yes")

# 终止任务
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed but auto-approves file changes in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |

## PR Reviews（示例）

Clone to a temp directory for safe review:

```bash
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## Parallel Issue Fixing with Worktrees（示例）

```bash
# 创建 worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# 并行执行
terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# 监控
process(action="list")

# 提交并创建 PR
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# 清理
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## Batch PR Reviews（示例）

```bash
# 获取所有 PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# 并行 review 多个 PR
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# 发布结果
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## 异常处理 / Error Handling

| 错误场景 | 原因 | 解决方案 |
|---------|------|---------|
| `codex: command not found` | Codex 未安装 | 运行 `npm install -g @openai/codex` |
| `Error: OpenAI API key not configured` | 缺少 API Key | 设置 `export OPENAI_API_KEY=sk-...` 或写入 `.env` |
| 任务超时 / 长时间无响应 | 任务复杂或 Codex 卡住 | 使用 `process(action="kill")` 终止后重试；添加 `--full-auto` 减少交互 |
| `fatal: not a git repository` | 不在 Git 目录中运行 | 使用 `cd $(mktemp -d) && git init && codex exec '...'` |
| 交互式提问无人应答 | 未使用 `--full-auto` 或 `--yolo` | 添加 `--full-auto` 标志；或使用 `process(action="submit")` 发送响应 |
| Token 限制错误 | 任务超出上下文窗口 | 拆分为多个子任务分批执行 |
| 网络错误 | API 调用失败 | 检查网络连接后重试；考虑配置代理 |
| `Error: spawn ENOENT` | 工作目录不存在 | 确保 `workdir` 参数指向有效目录 |

**兜底策略 / Fallback：**
- Codex 持续失败 → 回退到 Claude Code CLI 或手动编码
- 关键任务 → 先在小范围测试（单文件）再全量执行
- 并行任务中某个失败 → 单独重试失败项，不影响其他任务

## 注意事项 / Pitfalls

1. **始终使用 `pty=true`** — Codex 是交互式终端应用，无 PTY 会挂起
2. **必须要有 Git 仓库** — Codex 拒绝在非 Git 目录运行。临时项目用 `mktemp -d && git init`
3. **使用 `exec` 做单次任务** — `codex exec "prompt"` 运行后自动退出
4. **`--full-auto` 适合构建** — 在沙箱内自动批准文件变更
5. **长任务用后台模式** — `background=true` + `process` 工具监控
6. **不要干扰运行中的 Codex** — 用 `poll`/`log` 监控，耐心等待
7. **并行执行是安全的** — 可同时运行多个 Codex 进程
8. **注意 API 费用** — Codex 调用会消耗 API 额度，长任务成本较高
9. **禁止在敏感仓库使用 `--yolo`** — 该模式跳过所有安全检查
