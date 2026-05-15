---
name: lark-im
version: 1.1.0
description: 飞书即时通讯：收发消息和管理群聊。发送和回复消息、搜索聊天记录、管理群聊成员、上传下载图片和文件（支持大文件分片下载）、管理表情回复。当用户需要发消息、查看或搜索聊天记录、下载聊天中的文件、查看群组成员时使用。
metadata:
  yao_category: "AI工作"
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli im --help"
---

# 飞书即时通讯 (IM)

**⚠️ CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、权限处理。**

## 前置检查

```bash
# 确认 CLI 可用
lark-cli --version

# 确认认证有效（读取 lark-shared 中的认证信息）
lark-cli auth check 2>/dev/null || echo "⚠️ 认证可能已过期"
```

## 核心概念

| 资源 | ID 格式 | 说明 |
|------|---------|------|
| Chat（群聊） | `oc_xxx` | 群聊或私聊对话 |
| Message（消息） | `om_xxx` | 单条消息，支持文本、卡片、图片、文件等 |
| Thread（回复串） | `om_xxx` 或 `omt_xxx` | 消息下的回复线程 |
| Reaction（表情回复） | emoji | 消息上的表情反应 |

### 资源关系

```
Chat (oc_xxx)
├── Message (om_xxx)
│   ├── Thread (reply thread)
│   ├── Reaction (emoji)
│   └── Resource (image / file / video / audio)
└── Member (user / bot)
```

## 身份与 Token 映射

| 身份 | Token 类型 | 权限范围 |
|------|-----------|----------|
| `--as user` | `user_access_token` | 取决于用户自身对目标聊天/消息/资源的访问权限 |
| `--as bot` | `tenant_access_token` | 取决于机器人是否在群内、应用可见范围、availability |

**同一 API 用不同身份调用可能结果不同**：owner/admin 状态、群成员身份、租户边界等会针对当前调用者检查。

### 机器人身份下发送者名称解析

当使用 `--as bot` 获取消息时，发送者名称可能显示为 `open_id` 而非名称。

**原因**：应用的可见范围未覆盖消息发送者。
**解决**：在飞书开发者控制台调整应用可见范围，或使用 `--as user` 获取消息。

## 快捷命令（Shortcuts）—— 优先使用

```bash
lark-cli im +<verb> [flags]
```

| Shortcut | 说明 |
|----------|------|
| `+chat-create` | 创建群聊 |
| `+chat-messages-list` | 列出聊天中的消息 |
| `+chat-search` | 按关键词搜索群聊 |
| `+chat-update` | 更新群名称或描述 |
| `+messages-mget` | 批量获取消息（最多 50 条） |
| `+messages-reply` | 回复消息（支持线程回复） |
| `+messages-resources-download` | 下载消息中的图片/文件（支持大文件分片） |
| `+messages-search` | 跨聊天搜索消息 |
| `+messages-send` | 发送消息到群聊或私聊 |
| `+threads-messages-list` | 列出线程中的消息 |

## API 调用

```bash
lark-cli schema im.<resource>.<method>   # 必须先查看参数结构
lark-cli im <resource> <method> [flags] # 调用 API
```

> **重要**：使用原生 API 时，必须先运行 `schema` 查看 `--data` / `--params` 参数结构。

## 标准工作流

### 工作流 1：发送消息到群聊

```
步骤 1: 确认 chat_id
  → 如果已知: 直接使用
  → 如果未知: lark-cli im +chat-search --name "群名关键词"
  → 验证: lark-cli im +chat-messages-list --chat-id <oc_xxx> --limit 1

步骤 2: 选择消息类型
  → 纯文本: --content-type text --content "消息内容"
  → 富文本: --content-type post --content '{"zh_cn": {...}}'
  → 卡片: --content-type interactive --content '{"config": {...}}'

步骤 3: 发送
  lark-cli im +messages-send --chat-id <oc_xxx> --content-type text --content "Hello"

步骤 4: 验证发送成功
  → 检查返回值中的 message_id (om_xxx)
  → 如果返回错误，见下方错误处理
```

### 工作流 2：查看/搜索聊天记录

```
步骤 1: 定位目标聊天
  lark-cli im +chat-search --name "关键词"

步骤 2: 查看最近消息
  lark-cli im +chat-messages-list --chat-id <oc_xxx> --limit 20

步骤 3: 搜索特定消息
  lark-cli im +messages-search --query "搜索关键词" [--chat-id <oc_xxx>]

步骤 4: 获取消息详情（如有需要）
  lark-cli im +messages-mget --message-ids "om_xxx,om_yyy"
```

### 工作流 3：回复消息（含线程回复）

```
步骤 1: 获取原消息 ID
  lark-cli im +chat-messages-list --chat-id <oc_xxx> --limit 10

步骤 2: 回复（新线程 or 追加到现有线程）
  → 新线程回复:
    lark-cli im +messages-reply --message-id <om_xxx> --content-type text --content "回复内容"
  → 追加到线程:
    lark-cli im +threads-messages-list --message-id <om_xxx>  # 先查看现有回复
    lark-cli im +messages-reply --message-id <om_xxx> --content-type text --content "追加回复"
```

### 工作流 4：下载聊天中的文件/图片

```
步骤 1: 找到包含文件的消息
  lark-cli im +chat-messages-list --chat-id <oc_xxx> --limit 20
  → 识别消息类型: image / file / video / audio

步骤 2: 下载资源
  lark-cli im +messages-resources-download --message-id <om_xxx> --output-dir ./downloads

步骤 3: 大文件确认
  → 文件 > 8MB 时自动分片下载（8MB/chunk）
  → 检查输出目录中的文件完整性
```

### 工作流 5：创建和管理群聊

```
步骤 1: 创建群聊
  lark-cli im +chat-create --name "群名称" --description "群描述"

步骤 2: 添加成员
  lark-cli im chat.members create --chat-id <oc_xxx> --member-ids "ou_xxx,ou_yyy"

步骤 3: 更新群信息
  lark-cli im +chat-update --chat-id <oc_xxx> --name "新名称"

步骤 4: 移除成员（需要权限）
  lark-cli im chat.members delete --chat-id <oc_xxx> --member-ids "ou_xxx"
```

## 权限速查表

| 方法 | 所需 Scope | 身份 |
|------|-----------|------|
| `chats.create` | `im:chat:create` | bot |
| `chats.get` / `chats.list` | `im:chat:read` | user/bot |
| `chats.update` | `im:chat:update` | user/bot |
| `chat.members.create` / `delete` | `im:chat.members:write_only` | user/bot |
| `messages.delete` | `im:message:recall` | user/bot |
| `messages.forward` / `merge_forward` | `im:message` | bot |
| `messages.read_users` | `im:message:readonly` | bot |
| `reactions.*` | `im:message.reactions:read/write_only` | user/bot |
| `images.create` | `im:resource` | bot |
| `pins.*` | `im:message.pins:read/write_only` | user/bot |

## 错误处理与异常恢复

### 常见问题

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `command not found` | `lark-cli` 未安装 | 安装 lark-cli 并确认 PATH 配置 |
| `authentication failed` | token 过期或无效 | 重新认证：参考 `lark-shared/SKILL.md` |
| `chat not found` | chat_id 无效或机器人不在群内 | 确认 chat_id；使用 `+chat-search` 查找 |
| `permission denied` | 缺少对应 scope | 检查权限表，确认应用已授权对应 scope |
| `message not found` | message_id 无效或已被撤回 | 确认 message_id；注意消息可能已被删除 |
| `resource download failed` | 文件已过期或权限不足 | 检查文件有效期；确认有访问权限 |
| 大文件下载中断 | 网络不稳定 | 使用 `+messages-resources-download` 自动分片（8MB/chunk） |
| 卡片消息解析失败 | 卡片格式未完全支持 | 返回原始事件数据，标注 "card not fully supported" |
| 发送者名称显示 open_id | 机器人可见范围不足 | 调整应用可见范围或使用 `--as user` |

### 身份选择决策树

```
需要操作飞书 IM？
├── 操作自己的消息/聊天 → 使用 --as user
├── 操作机器人所在的群 → 使用 --as bot
├── 需要读取特定用户的消息 → 检查应用可见范围
│   ├── 已覆盖 → --as bot
│   └── 未覆盖 → 使用 --as user 或调整可见范围
└── 跨租户操作 → 确认内部群 + 同租户，否则失败
```

### 安全操作规范
- **发消息前**：确认目标 chat_id 正确，避免发到错误群组
- **删消息前**：确认有撤回权限（仅 bot/群主/管理员可撤回他人消息）
- **拉人入群前**：确认目标用户在应用可用范围内
- **下载文件前**：确认文件未过期，大文件自动分片下载

## 注意事项
- 卡片消息 (`interactive` 类型) 在事件订阅中暂不支持紧凑转换，会返回原始数据
- 发送者名称解析需要机器人可见范围覆盖该用户
- 消息撤回限制：bot 只能撤回自己发送的消息，或作为群主/管理员撤回他人消息
- 群聊操作需要操作者在群内，且内部群需要同租户
