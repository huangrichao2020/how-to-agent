---
name: spec-driven-development-lightweight
description: 轻量级规格驱动开发工作流 — 需求 → 设计 → 任务 → 实现 → 审批。零依赖，纯 Python + Markdown。适合复杂多步骤项目且资源受限环境。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  yao_category: "AI编程"
  hermes:
    tags: [spec, planning, workflow, development, process, lightweight]
    related_skills: [writing-plans, subagent-driven-development, requesting-code-review]
---

# Spec-Driven Development (Lightweight)

## 核心理念

借鉴 `spec-workflow-mcp` 的三阶段结构（需求→设计→任务），但用纯 Python + Markdown 实现，**零外部依赖**。专为 2GB 内存等受限环境设计。

**流程：**
```
需求(Requirements) → 设计(Design) → 任务分解(Tasks) → 实现(Implementation) → 审批(Review)
```

与 `writing-plans` 的区别：
- `writing-plans` 侧重「如何写实施计划」
- `spec-driven-development-lightweight` 侧重「完整的规格生命周期管理」，包含状态追踪、审批流和实现日志归档

## 何时使用

**应该用：**
- 复杂多阶段项目（需要分需求→设计→任务逐步推进）
- 需要人类审批 agent 产出的方案
- 需要追溯实现历史（谁、何时、改了什么、结果如何）
- 资源受限环境（无法运行 Node.js/重型框架）

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

## 核心模块

`~/.hermes/specs/spec_manager.py` 提供以下 API：

### 1. 创建 Spec
```python
from hermes.specs.spec_manager import create_spec

result = create_spec(
    title='用户认证系统',
    requirements='需要支持 JWT 登录、刷新 token...',
    tags=['backend', 'auth'],
)
# result: {'slug': 'user-auth-xxx', 'phase': 'requirements', ...}
```

### 2. 更新阶段
```python
from hermes.specs.spec_manager import update_phase

# 写入设计并自动推进到 tasks
status = update_phase(
    slug='user-auth-xxx',
    phase='design',
    content='## 架构\n- JWT 中间件\n- RBAC 权限',
    action='write'  # write/approve/reject
)
```

### 3. 记录实现日志
```python
from hermes.specs.spec_manager import log_implementation

log_implementation(
    slug='user-auth-xxx',
    task_id='1',
    description='创建 User 模型',
    files_changed=['agent/user_model.py'],
    code_stats={'lines_added': 120},
    result='success',
)
```

### 4. 查询状态
```python
from hermes.specs.spec_manager import get_spec, list_specs

# 查看单个 spec
spec = get_spec('user-auth-xxx')
print(spec['phase'])  # 'implementation'
print(spec['completed_tasks'])  # 5

# 列出所有进行中的 spec
active = list_specs(phase='implementation')
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

## 与其他 Skill 配合

| 阶段 | 推荐 Skill |
|------|-----------|
| 需求收集 | 无（用户提供） |
| 设计 | `writing-plans`（写技术方案） |
| 任务执行 | `subagent-driven-development`（每个任务一个子 agent） |
| 代码审查 | `requesting-code-review` |
| 测试 | `test-driven-development` |

## 实战示例

```python
import sys
sys.path.insert(0, '/root/.hermes/specs')
from spec_manager import create_spec, update_phase, log_implementation, get_spec

# 1. 创建
spec = create_spec('Context Layered Engine', '实现 5 层 Context...', tags=['core'])
slug = spec['slug']

# 2. 设计
update_phase(slug, 'design', '## 架构\nLayeredContextEngine...', action='write')

# 3. 任务
update_phase(slug, 'tasks', '## Tasks\n### Task 1: ...', action='write')

# 4. 实现日志
log_implementation(slug, '1', '创建基类', ['plugins/...'], {'lines_added': 180})

# 5. 查询
final = get_spec(slug)
print(f"Phase: {final['phase']}, Tasks: {final['completed_tasks']}")
```

## 优势对比 (vs spec-workflow-mcp)

| 能力 | spec-workflow-mcp | 本实现 |
|------|-------------------|--------|
| 三阶段结构 | ✅ | ✅ |
| 实现日志 | ✅ | ✅ |
| Web 仪表板 | ✅ | ❌ (不需要) |
| VSCode 插件 | ✅ | ❌ (不需要) |
| 审批流 | Web UI | 飞书/微信对话 |
| 依赖 | Node.js + npm | **零依赖** |
| 内存占用 | ~200MB+ | **忽略不计** |
