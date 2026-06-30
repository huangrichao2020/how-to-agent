---
name: hermes-source-management
description: "让 M1 上的 Hermes 管理自己的源码：区分源码 checkout、运行目录、测试、同步、重启和汇报。"
version: 1.0.0
---

# Hermes 源码自管

当 Hermes 需要检查、修复、升级或解释自己的源码时，使用这个 skill。

## 当前路径

在 M1 上区分两个目录：

```text
源码 checkout: /Users/tingchi/Desktop/hermes-agent
运行目录:      /Users/tingchi/Desktop/hermes-agent
Hermes home:   /Users/tingchi/hermes-new/.hermes
how-to-agent:  /Users/tingchi/Desktop/how-to-agent
```

源码 checkout 是 git 仓库，用于读代码、改代码、跑测试、提交和 push。

当前 gateway 直接从源码 checkout 运行。旧 `hermes-new/hermes-agent` 不应继续作为第二套代码目录或 symlink 存在；`hermes-new` 下只保留 `HERMES_HOME` 状态目录。

## Git 同步原则

M1 上的 `hermes-agent`、`how-to-agent`、`agent-systems-patterns`、`GenericAgent`
都有对应 GitHub 仓库。它们之间同步时优先走 git：

1. 在实际编辑的源码 checkout 里 commit + push。
2. 到另一台机器或另一个 checkout 里 fetch/pull。
3. 确认 HEAD、branch、status 干净。
4. 只有 live 运行目录不是 git source-of-truth 时，才从已验证源码 checkout 同步文件到 live 目录。

不要把 rsync/scp 当作两个 git 仓库之间的常规同步方式。rsync 只用于 live
运行目录、紧急恢复或明确没有 git 远端的资产。

## 自管原则

Hermes 有权为了稳定运行和用户长期受益管理自己的源码，但必须保留证据和可回滚性。

可以主动做：

- 检查当前源码状态、分支、远端和 HEAD。
- 阅读自己的 gateway、agent loop、memory、cron、output stream 和 rust/hermesd 代码。
- 根据用户反馈修复自己的行为。
- 跑聚焦测试、py_compile、health check。
- 把经过验证的改动提交到源码 checkout。
- 直接从源码 checkout 重启运行时，不再维护第二套代码目录。
- 重启 gateway 并汇报状态。

需要谨慎说明：

- 大范围重构。
- 改动 memory/persona/system prompt。
- 删除历史数据。
- 影响外部平台、资金、隐私或不可逆操作。

## 标准流程

```text
1. 进入源码 checkout
2. git status / branch / remote / HEAD
3. 找到相关代码路径
4. 小步修改
5. py_compile / pytest / targeted smoke
6. git diff --check
7. commit + push
8. 如果运行目录是单独的非 git 树，才同步已验证文件；当前 M1 Hermes 已源码运行
9. launchctl 重启 ai.hermes.gateway
10. hermesd health 验证
11. 更新工作手册/交接手册：路径、命令、验证、回滚、遗留风险
12. 给用户汇报：改了什么、验证了什么、当前 PID/平台状态
```

常用命令：

```bash
cd /Users/tingchi/Desktop/hermes-agent
git status --short --branch
git pull --ff-only
python3 -m py_compile agent/cognitive_architecture.py agent/cognitive_response_policy.py
pytest -q tests/test_cognitive_response_policy.py
git diff --check
git add <files>
git commit -m "..."
git push

# 其他 M1 git checkout 用 git 同步
cd /Users/tingchi/Desktop/how-to-agent
git pull --ff-only

# 当前 Hermes gateway 已直接从源码 checkout 运行，不需要再 rsync 到第二套代码。
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
hermesd health --home /Users/tingchi/hermes-new/.hermes --service ai.hermes.gateway --user --json
```

## 汇报格式

汇报要短，但要包含：

- 源码目录和 commit。
- 运行目录是否就是源码 checkout；如果不是，列出同步到运行目录的文件。
- 测试/编译/health 结果。
- gateway PID 和 Feishu/Weixin 是否在线。
- 已更新的工作手册/交接手册，或说明为什么无需更新。
- 是否还有遗留风险。

## 禁忌

- 不要在非 git 运行目录里盲改后忘记回源。
- 不要用 rsync 代替 git 来同步两个都有 GitHub 远端的源码仓库。
- 不要做完可复用工作后不更新工作手册或交接手册。
- 不要把旧 aliyun 环境记忆当成当前 M1 事实。
- 不要只重启不验证。
- 不要只发“已完成”，却不说验证证据。
- 不要把 debug trace 当用户结论。
