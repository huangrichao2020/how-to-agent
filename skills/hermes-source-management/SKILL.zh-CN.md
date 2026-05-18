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
运行目录:      /Users/tingchi/hermes-new/hermes-agent
Hermes home:   /Users/tingchi/hermes-new/.hermes
how-to-agent:  /Users/tingchi/Desktop/how-to-agent
```

源码 checkout 是 git 仓库，用于读代码、改代码、跑测试、提交和 push。

运行目录是当前 gateway 实际加载的代码目录。不要把运行目录当成唯一源码来源；它可能不是 git 仓库。

## 自管原则

Hermes 有权为了稳定运行和用户长期受益管理自己的源码，但必须保留证据和可回滚性。

可以主动做：

- 检查当前源码状态、分支、远端和 HEAD。
- 阅读自己的 gateway、agent loop、memory、cron、output stream 和 rust/hermesd 代码。
- 根据用户反馈修复自己的行为。
- 跑聚焦测试、py_compile、health check。
- 把经过验证的改动提交到源码 checkout。
- 同步已验证文件到运行目录。
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
8. rsync 或复制已验证文件到运行目录
9. launchctl 重启 ai.hermes.gateway
10. hermesd health 验证
11. 给用户汇报：改了什么、验证了什么、当前 PID/平台状态
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

rsync -a <files> /Users/tingchi/hermes-new/hermes-agent/<matching-path>
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
hermesd health --home /Users/tingchi/hermes-new/.hermes --service ai.hermes.gateway --user --json
```

## 汇报格式

汇报要短，但要包含：

- 源码目录和 commit。
- 同步到运行目录的文件。
- 测试/编译/health 结果。
- gateway PID 和 Feishu/Weixin 是否在线。
- 是否还有遗留风险。

## 禁忌

- 不要在非 git 运行目录里盲改后忘记回源。
- 不要把旧 aliyun 环境记忆当成当前 M1 事实。
- 不要只重启不验证。
- 不要只发“已完成”，却不说验证证据。
- 不要把 debug trace 当用户结论。
