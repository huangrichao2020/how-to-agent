---
name: lark-approval
version: 1.1.0
description: "飞书审批 API：审批实例、审批任务管理。用于查询/撤回/催办审批，同意/拒绝/转交审批任务，以及获取审批实例详情和用户发起列表。"
metadata:
  yao_category: "AI工作"
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli approval --help"
---

# approval (v1.1)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、权限处理**

## 工作流

1. 读取 `../lark-shared/SKILL.md` 确认认证状态和身份类型
2. 根据用户需求选择资源（`instances` 或 `tasks`）和方法
3. 运行 `lark-cli schema approval.<resource>.<method>` 查看参数结构
4. 调用 API，检查返回结果
5. 如遇错误，参照下方异常处理指南

## API Resources

```bash
lark-cli schema approval.<resource>.<method>   # 调用 API 前必须先查看参数结构
lark-cli approval <resource> <method> [flags] # 调用 API
```

> **重要**：使用原生 API 时，必须先运行 `schema` 查看 `--data` / `--params` 参数结构，禁止猜测字段格式。

### instances

- `get` — 获取单个审批实例详情
- `cancel` — 撤回审批实例
- `cc` — 抄送审批实例
- `initiated` — 查询用户的已发起列表

### tasks

- `remind` — 催办审批人
- `approve` — 同意审批任务
- `reject` — 拒绝审批任务
- `transfer` — 转交审批任务
- `query` — 查询用户的任务列表

## 权限表

| 方法 | 所需 scope |
|------|-----------|
| `instances.get` | `approval:instance:read` |
| `instances.cancel` | `approval:instance:write` |
| `instances.cc` | `approval:instance:write` |
| `instances.initiated` | `approval:instance:read` |
| `tasks.remind` | `approval:instance:write` |
| `tasks.approve` | `approval:task:write` |
| `tasks.reject` | `approval:task:write` |
| `tasks.transfer` | `approval:task:write` |
| `tasks.query` | `approval:task:read` |

## 异常处理

### API 错误响应处理

所有 API 调用失败时返回 JSON 错误，常见模式：

```json
{
  "code": 99991672,
  "msg": "permission denied",
  "error": { ... }
}
```

**处理策略**：
- `code=99991672`（权限不足）：检查当前身份（bot/user），参照 `lark-shared` 中的权限不足处理指南
- `code=99991400`（参数错误）：检查 `--data` 格式，运行 `schema` 确认必填字段
- `code=99991404`（资源不存在）：instance_id / task_id 无效或已被删除，告知用户重新确认
- `code=99991429`（频率限制）：等待 2-5 秒后重试，最多 3 次

### 业务异常场景

| 场景 | 表现 | 处理方式 |
|------|------|---------|
| 审批已撤回/已取消 | `cancel` 返回已取消状态 | 告知用户该实例已失效，无需重复操作 |
| 审批已结束（通过/拒绝） | `approve`/`reject` 返回已处理 | 告知用户审批已完成，检查当前状态 |
| 催办对象无权限 | `remind` 失败 | 确认审批任务是否处于待处理状态 |
| 转交目标用户不在审批流 | `transfer` 失败 | 提供可选的转交对象列表或让用户指定 |
| `instances.get` 找不到实例 | 返回空或 404 | 确认 instance_code 格式正确，检查是否属于当前应用 |

### 身份相关注意事项

- **Bot 身份**：只能操作当前应用创建的审批实例，无法查看其他应用的审批
- **User 身份**：可查询用户参与的所有审批（需 `approval:instance:read` scope）
- 操作前确认 `--as` 身份匹配目标操作范围

### 网络/超时异常

- lark-cli 调用超时（30s+ 无响应）：检查网络连接，重试 1 次
- JSON 解析失败：检查 CLI 版本是否最新，建议 `lark-cli --version` 确认

## 实用示例

```bash
# 查询审批实例详情
lark-cli schema approval.instances.get
lark-cli approval instances get --instance_code "xxx"

# 撤回审批
lark-cli approval instances cancel --instance_code "xxx"

# 查询我的待审批任务
lark-cli approval tasks query --status "pending"

# 同意审批任务
lark-cli approval tasks approve --task_id "xxx" --comment "同意"
```
