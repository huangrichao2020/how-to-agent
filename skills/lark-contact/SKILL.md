---
name: lark-contact
version: 1.1.0
description: "飞书通讯录：查询组织架构、人员信息和搜索员工。获取当前用户或指定用户的详细信息、通过关键词搜索员工（姓名/邮箱/手机号）。当用户需要查看个人信息、查找同事 open_id 或联系方式、按姓名搜索员工、查询部门结构时使用。"
metadata:
  yao_category: "AI工作"
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli contact --help"
---

# contact (v1.1)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、权限处理**

## 工作流

1. 读取 `../lark-shared/SKILL.md` 确认认证状态和身份类型（bot vs user）
2. 根据用户需求选择操作：
   - **搜索员工** → 用 `+search-user` shortcut
   - **获取指定用户信息** → 用 `+get-user` shortcut
   - **获取当前用户信息** → 用 `+get-user`（不传 `--user-id`）
3. 如有需要，先搜索获取 `open_id`，再调用 `+get-user` 获取详情
4. 检查返回结果，处理可能的异常情况

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`lark-cli contact +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+search-user`](references/lark-contact-search-user.md) | 搜索员工（按姓名/邮箱/手机号，结果按亲密度排序） |
| [`+get-user`](references/lark-contact-get-user.md) | 获取用户信息（不传 user_id 获取自己；传 user_id 获取指定用户） |

## 异常处理

### 认证与权限异常

| 错误 | 原因 | 处理方式 |
|------|------|---------|
| 401 Unauthorized | Token 过期或未认证 | 运行 `lark-cli auth login --scope "contact:contact:readonly"` 重新授权 |
| 403 Forbidden (41050) | 组织架构可见范围限制 | Bot 身份需在开发者后台开通 `contact:contact:readonly` scope；User 身份需管理员调整可见范围 |
| 403 Forbidden | 应用未开通通讯录权限 | 引导用户前往飞书开发者后台开通对应 scope |

### 查询结果异常

| 场景 | 表现 | 处理方式 |
|------|------|---------|
| 搜索结果为空 | `+search-user` 返回空列表 | 确认关键词拼写，建议用户换用其他关键词（如用邮箱代替姓名） |
| 找到多个匹配 | 返回多条结果 | 展示所有结果，让用户选择目标用户；或建议缩小搜索范围 |
| 用户已离职/被禁用 | `+get-user` 返回 404 或特殊状态 | 告知用户该账号状态异常，建议联系 HR 或管理员 |
| `--user-id` 格式错误 | 参数校验失败 | 确认 user_id_type 匹配（open_id 以 `ou_` 开头，union_id 以 `on_` 开头） |
| 分页返回 `has_more=true` | 结果未完全返回 | 继续传 `page_token` 获取下一页，不要盲目调大 `page_size`（最大 200） |

### 身份差异注意事项

- **Bot 身份**：受应用可见范围限制，只能查到应用可见范围内的员工
- **User 身份**：受组织架构可见范围限制，只能看到自己能看到的人
- 如果搜索结果为空，尝试切换身份（`--as user` / `--as bot`）再试

### 网络/超时异常

- CLI 调用超时（30s+）：重试 1 次，检查网络连接
- JSON 解析失败：检查 CLI 版本，运行 `lark-cli --version` 确认

## 实用示例

```bash
# 搜索员工（找到 open_id）
lark-cli contact +search-user --query "张三"

# 获取指定用户详情
lark-cli contact +get-user --user-id ou_xxx

# 获取当前用户自己的信息
lark-cli contact +get-user

# 表格输出方便阅读
lark-cli contact +get-user --user-id ou_xxx --table

# 获取下一页搜索结果
lark-cli contact +search-user --query "张三" --page-size 50 --page-token <PAGE_TOKEN>
```
