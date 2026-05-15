---
name: lark-okr
version: 1.1.0
description: 飞书 OKR：管理目标与关键结果。查看和编辑 OKR 周期、目标（Objective）、关键结果（Key Result）、对齐关系、量化指标。当用户需要查看或创建 OKR、管理目标和关键结果、查看对齐关系时使用。
metadata:
  yao_category: "AI工作"
  requires:
    bins: [ "lark-cli" ]
  cliHelp: "lark-cli okr --help"
---

# 飞书 OKR

**⚠️ CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、权限处理。**

## 触发条件

**适用场景**（当用户提到以下关键词时触发本 skill）：
- "OKR" / "目标" / "关键结果" / "key result"
- "OKR 周期" / "okr period" / "okr cycle"
- "创建目标" / "编辑 OKR" / "对齐 OKR"
- "量化指标" / "indicator"

**不触发**：
- 用户说"绩效" / "考核" → 不属于 OKR 模块，需另行处理

## 前置检查

```bash
# 确认 CLI 可用
lark-cli --version

# 确认认证有效
lark-cli auth check 2>/dev/null || echo "⚠️ 认证可能已过期"
```

## 操作流程

### 步骤 1: 获取 OKR 周期列表

```bash
lark-cli okr +cycle-list
```

- 可按时间筛选周期
- 确认用户有权限查看的周期

### 步骤 2: 查看周期详情（目标和关键结果）

```bash
lark-cli okr +cycle-detail --cycle-id <cycle_id>
```

- 获取特定周期中所有目标和关键结果的内容
- 如需富文本格式说明，参考 [ContentBlock 富文本格式](references/lark-okr-contentblock.md)

### 步骤 3: 执行具体操作

根据用户需求，选择对应的 API 资源和方法。使用原生 API 前**必须**先运行 schema 查看参数结构：

```bash
lark-cli schema okr.<resource>.<method>   # 必须先查看参数结构
lark-cli okr <resource> <method> [flags] # 调用 API
```

## 快捷命令（Shortcuts）—— 优先使用

```bash
lark-cli okr +<verb> [flags]
```

| Shortcut | 说明 |
|----------|------|
| `+cycle-list` | 获取用户的 OKR 周期列表，可按时间筛选 |
| `+cycle-detail` | 获取特定 OKR 周期中所有目标和关键结果的内容 |

## 格式说明

- [`ContentBlock 富文本格式`](references/lark-okr-contentblock.md) — Objective/KeyResult/Notes 字段使用的富文本格式
- [`OKR 业务实体`](references/lark-okr-entities.md) — OKR 实体结构、定义和关系
- **强烈建议** 在操作 OKR 前阅读业务实体文档

## 示例与用法

**示例 1 — 查看我的 OKR 周期：**
```bash
lark-cli okr +cycle-list
```

**示例 2 — 查看某周期的全部目标和关键结果：**
```bash
lark-cli okr +cycle-detail --cycle-id "xxx"
```

**示例 3 — 创建新目标：**
```bash
lark-cli schema okr.cycle.objectives.create  # 先查看参数
lark-cli okr cycle.objectives create --cycle-id "xxx" --data '{"..."}'
```

## 异常处理与兜底策略

### 常见问题

| 错误 | 原因 | 兜底方案 |
|------|------|---------|
| `command not found` | `lark-cli` 未安装 | 安装 lark-cli 并确认 PATH 配置 |
| `authentication failed` | token 过期或无效 | 重新认证：参考 `lark-shared/SKILL.md` |
| `cycle not found` | 周期 ID 无效或无权限查看 | 使用 `+cycle-list` 确认有效周期 ID |
| `objective not found` | 目标 ID 无效或已被删除 | 确认 objective_id；使用 `cycle.objectives.list` 查找 |
| `key_result not found` | 关键结果 ID 无效 | 确认 key_result_id；使用 `objective.key_results.list` 查找 |
| `position overlap` | 位置值重复 | 确保同一周期/目标下所有位置值唯一 |
| `weight sum != 1` | 权重总和不等于 1 | 调整权重使其总和严格等于 1.0 |
| `alignment rejected` | 对齐到自己的目标或周期不重叠 | 检查对齐规则：不能自对齐；周期时间必须有重叠 |
| 参数校验失败 | 缺少必填字段或格式错误 | 先用 `schema` 查看参数结构，不要猜测字段 |
| `permission denied` | 缺少对应 scope | 检查权限表，确认应用已授权 `okr:okr.content:writeonly` |
| 请求超时 | 网络不稳定或服务端响应慢 | 重试 3 次，每次间隔 5 秒；仍失败则提示用户检查网络 |

### 安全操作规范
- **删除前**：确认目标/关键结果不再需要；可先获取详情备份
- **更新权重/位置**：必须同时修改所有项，不能只改单个
- **创建对齐**：确认周期时间重叠，且不是对齐自己的目标
- **修改前**：先读取当前状态，避免覆盖他人改动

## API 资源速览

| 资源 | 方法 | 说明 |
|------|------|------|
| cycles | `list` | 批量获取用户周期 |
| cycles | `objectives_position` | 更新周期下全部目标的位置（必须同时修改所有，不允许重叠） |
| cycles | `objectives_weight` | 更新周期下全部目标的权重（总和必须 = 1） |
| cycle.objectives | `create`, `list` | 创建/获取目标 |
| objectives | `get`, `patch`, `delete` | 获取/更新/删除目标 |
| objectives | `key_results_position` | 更新关键结果位置（必须同时修改所有，不允许重叠） |
| objectives | `key_results_weight` | 更新关键结果权重（总和必须 = 1） |
| objective.key_results | `create`, `list` | 创建/获取关键结果 |
| key_results | `get`, `patch`, `delete` | 获取/更新/删除关键结果 |
| alignments | `get`, `delete` | 获取/删除对齐关系 |
| objective.alignments | `create`, `list` | 创建/获取对齐关系（不能对齐自己的目标；周期时间必须重叠） |
| indicators | `patch` | 更新量化指标 |
| *.indicators.list | — | 获取目标/关键结果的量化指标 |
| categories | `list` | 批量获取分类 |

## 权限速查表

| 操作类型 | Scope |
|----------|-------|
| 读取 (get/list) | `okr:okr.content:readonly` / `okr:okr.period:readonly` / `okr:okr.setting:read` |
| 写入 (create/patch/delete) | `okr:okr.content:writeonly` |

## 注意 / Pitfalls

- **注意**：所有写入操作（create/patch/delete）需要 `okr:okr.content:writeonly` 权限
- **注意**：位置和权重更新是原子操作——必须同时提交所有项
- **注意**：对齐关系有严格约束：不能自对齐，周期必须有重叠
- **注意**：富文本字段使用 ContentBlock 格式，不是纯文本
- **坑**：`objectives_position` 和 `objectives_weight` 不允许只修改单个项，必须一次性提交全部项
- **坑**：创建对齐时如果周期时间不重叠会被拒绝，需先确认周期时间范围
- **坑**：Objective/KeyResult/Notes 等字段是 ContentBlock 格式，直接传纯文本会导致格式错误
