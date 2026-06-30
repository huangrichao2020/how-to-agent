---
name: lark-cli
description: "飞书 CLI 全覆盖 — 消息/文档/表格/日历/任务/审批/通讯录/云空间/知识库/妙记/视频会议/OKR/画板/电子表格/幻灯片/事件/组织架构。Trigger: 飞书/lark/发消息/建文档/查日历. Do NOT trigger for 非飞书平台操作。"
version: 1.1.0
---
# 飞书 CLI (lark-cli)

## 一句话版本
通过 lark-cli 操作飞书全平台能力，覆盖 IM/文档/表格/日历/审批/通讯录/云空间等 20+ 模块。

## 触发条件
- ✅ **触发**：飞书/lark、发消息、建文档、查日历、审批操作、通讯录查询、云空间管理
- ❌ **不触发**：非飞书平台操作（如钉钉/企业微信）、通用文件操作、邮件操作

## 前置条件
1. **认证**：确保已配置飞书 App ID/Secret 或 Access Token
2. **权限**：对应模块的 API 权限已开通（如 `im:message`、`docx:document`）
3. **CLI 可用**：`lark-cli` 已安装且路径在 PATH 中

## 核心模块

### IM 消息
```bash
# 发送消息
lark-cli message send --chat-id "oc_xxx" --text "Hello" --msg-type text

# 发送富文本
lark-cli message send --chat-id "oc_xxx" --content file.json --msg-type interactive
```

### 文档 (Docx)
```bash
# 创建文档
lark-cli docx create --folder-token "xxx" --title "标题"

# 编辑文档（通过 DocxXML 块操作）
lark-cli docx block append --document-id "xxx" --block-type text --content "内容"
```

### 电子表格 & 多维表格 (Base)
```bash
# 创建电子表格
lark-cli sheet create --folder-token "xxx" --title "表格名"

# 多维表格记录操作
lark-cli base record create --app-token "xxx" --table-id "xxx" --fields file.json
```

### 日历
```bash
lark-cli calendar event create --calendar-id "primary" --start "2026-01-15T10:00:00+08:00" --end "2026-01-15T11:00:00+08:00" --summary "会议"
```

### 审批
```bash
# 创建审批实例
lark-cli approval instance create --approval-code "xxx" --user-id "xxx" --form-data file.json

# 查询审批任务
lark-cli approval task list --user-id "xxx" --status pending
```

### 通讯录
```bash
lark-cli contact user get --user-id "xxx"
lark-cli contact department list --dept-id "0"
```

## 异常处理

### 认证失败
- **症状**：`401 Unauthorized`、`token expired`
- **排查**：检查 App ID/Secret 配置、Token 是否过期
- **恢复**：重新获取 Token `lark-cli auth refresh` 或重新配置凭证

### 权限不足
- **症状**：`403 Forbidden`、`no permission`
- **排查**：飞书开放平台检查对应 API 权限是否已开通
- **恢复**：在飞书后台申请对应权限，等待审批通过

### 频率限制
- **症状**：`429 Too Many Requests`
- **排查**：超出 API 调用频率限制
- **恢复**：降低请求频率，使用指数退避重试（基础间隔 1s）

### 资源不存在
- **症状**：`404 Not Found`（文档/群/用户 ID 错误）
- **排查**：确认资源 ID 是否正确、资源是否已被删除
- **恢复**：重新获取正确的资源 ID

### 消息发送失败
- **症状**：消息未送达、chat_id 无效
- **排查**：确认机器人是否在目标群中、chat_id 格式是否正确
- **恢复**：将机器人添加到目标群、使用正确的 chat_id 格式（`oc_` 开头为群聊，`ou_` 开头为用户）

## 常见坑点
- ⚠️ 飞书 Token 有效期有限，需定期刷新或使用 Refresh Token 机制
- ⚠️ 不同模块的权限需分别开通，单一权限不覆盖所有模块
- ⚠️ 文档编辑使用 DocxXML 格式，非纯文本，需注意块结构
- ⚠️ 审批表单字段需严格匹配审批模板定义，否则创建失败
- ⚠️ 批量操作注意频率限制，建议每批间隔 ≥1s
