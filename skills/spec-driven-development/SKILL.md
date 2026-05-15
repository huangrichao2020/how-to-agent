---
name: spec-driven-development
description: 轻量级规格驱动开发工作流 — 需求 → 设计 → 任务 → 实现 → 审批。零依赖，纯 Markdown + JSON。适合复杂多步骤项目。
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  yao_category: "AI编程"
  hermes:
    tags: [spec, planning, workflow, development, process]
    related_skills: [writing-plans, subagent-driven-development, requesting-code-review]
---

# Spec-Driven Development

## 核心理念

借鉴 spec-workflow-mcp 的三阶段结构，但用纯 Python + Markdown 实现，零外部依赖。

**流程：**
```
需求(Requirements) → 设计(Design) → 任务分解(Tasks) → 实现(Implementation) → 审批(Review)
```

与 `writing-plans` 的区别：
- `writing-plans` 侧重「如何写实施计划」
- `spec-driven-development` 侧重「完整的规格生命周期管理」，包含审批流和实现日志

## 何时使用

**应该用：**
- 复杂多阶段项目（需要分需求→设计→任务逐步推进）
- 需要人类审批 agent 产出的方案
- 需要追溯实现历史（谁、何时、改了什么、结果如何）

**不需要用：**
- 简单单步任务（直接干就行）
- 已有明确实施方案的小改动（用 `writing-plans` 就够了）

## 存储位置

所有 spec 存在 `~/.hermes/specs/<slug>/` 下：
```
specs/
├── user-auth-1714384000/
│   ├── requirements.md    # 需求文档
│   ├── design.md          # 技术方案
│   ├── tasks.md           # 任务分解
│   ├── status.json        # 状态和进度
│   ├── review.md          # 审批反馈
│   └── logs/              # 实现日志
│       ├── 1_1.json
│       ├── 1_2.json
│       └── 2_1.json
└── ...
```

## 使用步骤

### Step 1: 创建 Spec（需求阶段）

用户提供需求后，调用 `spec_manager.create_spec()`：

```python
# 通过 execute_code 或终端调用
python3 -c "
from hermes.specs.spec_manager import create_spec
result = create_spec(
    title='用户认证系统',
    requirements='需要支持 JWT 登录、刷新 token、权限分级...',
    tags=['backend', 'auth'],
    metadata={'requester': 'user'}
)
print(result)
"
```

### Step 2: 设计阶段

Agent 产出技术方案后，调用 `update_phase(slug, "design", content)`：

```markdown
# 设计要点

## 架构
- JWT 认证中间件
- Token 存储：HTTP-only cookie
- 权限：RBAC 三级（admin/user/guest）

## 技术栈
- Python: PyJWT, Flask-JWT-Extended
- 数据库：SQLite (已有 hermes_state.py)
```

状态自动推进到 `tasks`。

### Step 3: 任务分解

将设计分解为可执行任务，调用 `update_phase(slug, "tasks", content)`：

```markdown
## Tasks

### Task 1: 创建 User 模型
- 文件: `agent/user_model.py`
- 字段: id, email, password_hash, role

### Task 2: 实现 JWT 登录接口
- 文件: `gateway/auth_endpoints.py`
- 接口: POST /auth/login → {token, refresh_token}

### Task 3: 实现权限中间件
- 文件: `gateway/auth_middleware.py`
- 装饰器: @require_role('admin')
```

状态自动推进到 `implementation`。

### Step 4: 实现 + 日志

每完成一个任务，记录实现日志：

```python
from hermes.specs.spec_manager import log_implementation

log_implementation(
    slug='user-auth-1714384000',
    task_id='1',
    description='创建 User 模型和 CRUD 操作',
    files_changed=['agent/user_model.py', 'tests/test_user.py'],
    code_stats={'lines_added': 120, 'lines_removed': 0, 'files_count': 2},
    result='success',
    notes='所有测试通过'
)
```

### Step 5: 审批

Agent 完成所有任务后，用户审查并决定 approve 或 reject：

```python
from hermes.specs.spec_manager import update_phase

update_phase(
    slug='user-auth-1714384000',
    phase='review',
    content='实现质量良好，JWT 刷新逻辑需要加强',
    action='approve'  # 或 'reject'
)
```

## 查询状态

```python
from hermes.specs.spec_manager import get_spec, list_specs

# 查看单个 spec
spec = get_spec('user-auth-1714384000')
print(f"阶段: {spec['phase']}")
print(f"进度: {spec['completed_tasks']}/{spec['total_tasks']}")

# 列出所有进行中的 spec
active = list_specs(phase='implementation')
```

## 与其他 Skill 配合

| 阶段 | 推荐 Skill |
|------|-----------|
| 需求收集 | 无（用户提供） |
| 设计 | `writing-plans`（写技术方案） |
| 任务执行 | `subagent-driven-development`（每个任务一个子 agent） |
| 代码审查 | `requesting-code-review` |
| 测试 | `test-driven-development` |

## Prompt 模板

### 创建 Spec
```
创建一个 spec：
标题：[项目名称]
需求：[详细描述]
标签：[tag1, tag2]
```

### 推进到设计
```
基于需求文档，产出技术方案并更新到设计阶段。
```

### 推进到任务
```
将设计方案分解为可执行任务列表，每个任务明确文件路径和预期输出。
```

### 完成实现
```
所有任务已完成，记录实现日志并请求审批。
```

## 状态机

```
requirements (active)
    ↓ write/approve
design (active)
    ↓ write/approve
tasks (active)
    ↓ write/approve
implementation (active)
    ↓ 所有任务完成
review (active)
    ↓ approve
[completed]
    ↓ reject
[返回上一阶段]
```

## 异常处理与故障排查

### spec_manager 模块不可用

| 错误现象 | 原因 | 解决方案 |
|----------|------|----------|
| `ModuleNotFoundError: hermes.specs.spec_manager` | spec_manager 未安装或路径错误 | 检查 `~/.hermes/specs/` 目录是否存在；确认 Hermes 已正确初始化 specs 子系统 |
| 函数调用报 `AttributeError` | 版本不兼容，API 已变更 | 使用 `dir(spec_manager)` 查看可用函数；参考最新版本文档 |

### 阶段推进失败

- **`update_phase` 报错**：检查 phase 名称是否拼写正确（`requirements` → `design` → `tasks` → `implementation` → `review`）
- **阶段跳过**：不允许跳过中间阶段。如果用户要求直接进入实现，必须先补齐 requirements 和 design
- **状态不一致**：如果 `status.json` 与实际文件不匹配，手动编辑 `status.json` 修正 phase 字段
- **重复创建同名 slug**：使用 `list_specs()` 检查是否已存在同名 spec，避免覆盖

### 任务分解问题

- **任务粒度过大**：单个任务应聚焦单一文件或功能点，超过 200 行代码的任务需进一步拆分
- **任务依赖冲突**：如果 Task B 依赖 Task A 的产出，确保 A 先完成并在 B 的描述中明确标注依赖关系
- **遗漏任务**：使用设计文档中的架构图/接口列表逐一对照，确保每个组件都有对应任务

### 实现日志异常

- **`log_implementation` 失败**：确认 slug 对应的目录存在；检查 `logs/` 子目录权限
- **文件路径错误**：`files_changed` 中的路径必须是相对于项目根目录的路径，不要用绝对路径
- **result 字段无效**：只能是 `success`、`partial`、`failed` 三者之一
- **重复记录**：同一 `task_id` 可能被多次记录（重试场景），在查询时取最新一条

### 审批回退处理

- **reject 后的处理流程**：
  1. 读取 `review.md` 中的 reject 反馈
  2. 确定需要返回的阶段（通常是 `implementation` 或 `tasks`）
  3. 更新 `status.json` 的 phase 字段回退到对应阶段
  4. 修正问题后重新推进，在 review.md 中追加新的审批记录
- **多次 reject**：如果同一 spec 被 reject 超过 2 次，建议回退到 `design` 阶段重新评估方案可行性

### 并发与冲突

- **多 agent 同时操作同一 spec**：使用文件锁或检查 `status.json` 的 `last_modified` 时间戳避免冲突
- **spec 长时间未推进**：如果 implementation 阶段超过 24 小时无更新，主动通知用户确认是否继续

### 常见坑点

- **slug 命名规范**：使用 `kebab-case` + 时间戳（如 `user-auth-1714384000`），不要用中文或空格
- **status.json 是单一可信源**：所有阶段查询都应读取 `status.json`，不要依赖文件是否存在来判断阶段
- **需求变更处理**：如果用户在实现阶段提出新需求，不要直接修改 `requirements.md`，而是在 `review.md` 中记录变更请求，完成后创建新 spec
- **与 `writing-plans` 的边界**：简单单步计划用 `writing-plans`，需要多阶段推进+审批追溯的用本技能

### 降级方案

- 如果 `spec_manager` 完全不可用，直接手动管理 Markdown + JSON 文件，遵循相同的目录结构和命名规范
- 如果无法记录实现日志，至少在 `tasks.md` 中用注释标记每个任务的完成状态
- 对于不需要人类审批的自动化场景，可以跳过 `review` 阶段，实现完成后直接标记 completed
