---
name: lark-event
version: 1.1.0
description: "飞书事件订阅：通过 WebSocket 长连接实时监听飞书事件（消息、通讯录变更、日历变更、审批、任务等），输出 NDJSON 到 stdout，支持 compact Agent 友好格式、正则路由、文件输出。当用户需要实时监听飞书事件、构建事件驱动管道、或调试事件订阅时使用。"
metadata:
  yao_category: "AI工作"
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli event --help"
---

# event (v1)

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) 了解认证、权限处理和安全规则。

## 概述

`lark-cli event` 通过 WebSocket 长连接实时接收飞书开放平台推送的事件，支持 24+ 种事件类型（IM、通讯录、日历、审批、任务、云文档等）。

**核心特性：**
- WebSocket 长连接，自动重连（SDK 内置）
- NDJSON 输出，适合管道处理
- `--compact` 模式：Agent 友好，扁平化结构，提取可读内容
- 正则路由：按事件类型分发到不同目录
- 单实例锁：防止同一应用多个连接导致事件分流

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`lark-cli event +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+subscribe`](references/lark-event-subscribe.md) | 通过 WebSocket 长连接订阅飞书事件（只读，NDJSON 输出）；bot-only；支持 compact 格式、正则路由、文件输出 |

## 常用命令速查

```bash
# 订阅所有已注册事件（catch-all 模式，24 种常见类型）
lark-cli event +subscribe

# 仅订阅特定事件类型
lark-cli event +subscribe --event-types im.message.receive_v1

# 订阅多种事件类型
lark-cli event +subscribe --event-types im.message.receive_v1,calendar.calendar.event.changed_v4

# 客户端正则过滤（SDK 接收后再过滤）
lark-cli event +subscribe --filter "^im\\."

# Agent 友好格式（解析内容，去除噪声字段）
lark-cli event +subscribe --event-types im.message.receive_v1 --compact --quiet

# 美化 JSON 输出
lark-cli event +subscribe --json

# 将每个事件写入文件
lark-cli event +subscribe --output-dir ./events

# 按正则路由到不同目录
lark-cli event +subscribe \
  --route '^im\\.message=dir:./im/' \
  --route '^contact\\.=dir:./contacts/'

# 预览配置，不实际连接
lark-cli event +subscribe --dry-run
```

## 输出格式

### 默认（原始 NDJSON）
每行一个事件，包含所有字段（schema、token、tenant_key 等）。

### `--compact`（Agent 友好）
扁平化键值输出，提取语义字段：
- IM 消息事件：深度处理，解析 `content` 双层 JSON，提取 `sender_id`、`chat_id`、`message_type` 等
- 非 IM 事件：通用处理器，保留所有原始字段，注入 `type`、`event_id`、`timestamp`

**Agent 管道应始终使用 `--compact --quiet`。**

## 支持的事件类型

| 分类 | 事件类型 | 所需 Scope |
|------|---------|-----------|
| IM | `im.message.receive_v1` | `im:message:receive_as_bot` |
| IM | `im.chat.member.bot.added_v1` | `im:chat:readonly` |
| IM | `im.chat.updated_v1` | `im:chat:readonly` |
| 通讯录 | `contact.user.created_v3` | `contact:user.base:readonly` |
| 日历 | `calendar.calendar.event.changed_v4` | `calendar:calendar:readonly` |
| 审批 | `approval.approval.updated` | `approval:approval:readonly` |
| 任务 | `task.task.update_tenant_v1` | `task:task:readonly` |
| 云文档 | `drive.notice.comment_add_v1` | `drive:drive:readonly` |

> 完整列表见 [飞书事件列表](https://open.feishu.cn/document/server-docs/event-subscription-guide/event-list)

## 异常处理与故障排查

| 异常场景 | 原因 | 解决方案 |
|----------|------|---------|
| **连接失败** | App ID/Secret 未配置 | 先运行 `lark-cli config init` 完成配置 |
| **收不到事件** | 开放平台未配置事件订阅 | 在飞书开放平台控制台 → 事件与回调 → 订阅方式 → 选择"使用长连接接收事件" |
| **收不到特定类型事件** | 未添加对应事件类型 | 在开放平台添加所需事件类型并开通对应权限 |
| **权限不足** | 缺少对应 scope | 检查事件所需的 scope，在开放平台开通 |
| **事件分流/丢失** | 多个 `+subscribe` 进程同时运行 | 单实例锁会阻止第二个进程；如使用 `--force` 强制启动，事件会被随机分流到各连接 |
| **compact 模式解析失败** | 消息内容为非标准格式 | compact 处理器会尝试解析，失败时返回原始内容；检查消息类型是否被支持 |
| **WebSocket 断开** | 网络波动 | SDK 内置自动重连，无需手动干预 |
| **Ctrl+C 后无统计输出** | 进程被 SIGKILL 而非 SIGINT | 使用 `Ctrl+C`（SIGINT）正常退出，会打印事件总数统计 |

## 平台侧配置清单

使用事件订阅前，**必须**在飞书开放平台完成以下配置：

1. 进入应用 → 事件与回调
2. 订阅方式选择 **"使用长连接接收事件"**
3. 添加所需事件类型（如 `im.message.receive_v1`）
4. 开通对应权限（如 `im:message:receive_as_bot`）
5. 发布应用版本使配置生效

## 注意事项

- **事件必须在开放平台配置** — CLI 无法动态订阅未配置的事件类型
- `--event-types` 控制 SDK 注册的事件类型，未注册的类型即使服务器推送也会被静默丢弃
- `--filter` 是纯客户端正则过滤，不影响 SDK 注册
- `--force` 跳过单实例锁，**不安全**：服务器会随机分流事件到各连接
- 身份固定为 **bot-only**，使用 App ID + App Secret 建立 WebSocket 连接
- 回复消息使用 `lark-cli api ... --as bot`，无需用户登录

## 参考

- [lark-im](../lark-im/SKILL.md) — 消息收发命令
- [lark-shared](../lark-shared/SKILL.md) — 认证与全局参数
- 完整 subscribe 文档：[references/lark-event-subscribe.md](references/lark-event-subscribe.md)
