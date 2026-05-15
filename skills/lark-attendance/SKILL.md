---
name: lark-attendance
version: 1.0.0
description: "飞书考勤打卡：查询自己的考勤打卡记录"
metadata:
  yao_category: "AI工作"
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli attendance --help"
---

# attendance (v1)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、权限处理**

## 默认参数自动填充规则

调用任何 API 时，以下参数 **必须自动填充，禁止向用户询问**：

| 参数 | 固定值 | 说明                                 |
|------|--------|------------------------------------|
| `employee_type` | `"employee_no"` | `employee_type`始终等于`"employee_no"` |
| `user_ids` | `[]`（空数组） | `user_ids`始终等于`[]`                 |

### 填充示例

当构建 `--params` 参数时，自动注入上述字段：
- `employee_type` 保持 `"employee_no"` 不变

当构建 `--data` 参数时，自动注入上述字段：
```json
{
  "user_ids": [],
  ...用户提供的参数
}
```

> **注意**：`user_ids` 数组保持为空[]，`employee_type` 保持 `"employee_no"` 不变。

## API Resources

```bash
lark-cli schema attendance.<resource>.<method>   # 调用 API 前必须先查看参数结构
lark-cli attendance <resource> <method> [flags]  # 调用 API
```

> **重要**：使用原生 API 时，必须先运行 `schema` 查看 `--data` / `--params` 参数结构，不要猜测字段格式。

### user_tasks

- `query` — 查询用户考勤打卡记录

## 权限表

| 方法 | 所需 scope |
|------|-----------|
| `user_tasks.query` | `attendance:task:readonly` |

## 错误处理与异常恢复

### 常见问题
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `command not found` | `lark-cli` 未安装 | 安装 lark-cli 并确认 PATH 配置 |
| `authentication failed` | token 过期或无效 | 重新认证：参考 `lark-shared/SKILL.md` |
| `permission denied` | 缺少 `attendance:task:readonly` scope | 确认应用已授权考勤读取权限 |
| 查询结果为空 | 指定日期范围内无打卡记录 | 扩大日期范围；确认 employee_no 正确 |
| 参数校验失败 | 缺少必填字段或日期格式错误 | 先用 `schema` 查看参数结构；日期格式为 `YYYY-MM-DD` |
| 返回多个用户数据 | 未正确设置 `user_ids` | 保持 `user_ids` 为空数组 `[]`，系统自动使用当前用户 |

### 安全操作规范
- **仅查询**：此技能只支持查询，不支持修改打卡记录
- **日期范围**：建议一次查询不超过 31 天，避免数据量过大
- **参数自动填充**：`employee_type` 和 `user_ids` 必须按规则自动填充，不要向用户询问


