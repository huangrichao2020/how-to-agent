---
name: agent-enhancements
description: Hermes Agent 三模块增强系统 —— 权限管控 + 防死循环 + 类型化记忆。参考 Mercury Agent 架构设计，针对 Hermes Agent 的最小侵入集成。
version: 1.1.0
yao_category: "AI编程"
---

# Agent Enhancements 三模块系统

## 状态

| 模块 | 文件 | 状态 | 说明 |
|------|------|------|------|
| Permissions | `agent/permissions.py` | ✅ 已由 Hermes 内置 | Hermes 已有完整的高危指令黑名单 + 审批流（`tools/approval.py`），无需重复实现 |
| **LoopDetector** | **`agent/loop_detector.py`** | **✅ 已实现** | 5 层循环检测，已集成到 `run_agent.py` |
| SecondBrain | `agent/second_brain.py` | ❌ 未实现 | 暂缓 — 现有 memory 工具稳定运行，直接换 SQLite 风险太高 |

## 模块 1: Permissions

**设计原则**: 只拦截黑名单，其余全部放行。不审批、不卡脖子。

### 内置黑名单（~30 条）

- `sudo *` — 特权提升
- `rm -rf /` 系列 — 文件系统破坏
- `mkfs *`, `dd if=*` — 磁盘格式化
- `:(){:|:&};:` — Fork bomb
- `shutdown *`, `reboot *`, `halt *` — 系统控制
- Windows 破坏命令（del, format, reg delete 等）

### 自定义规则

编辑 `~/.hermes/permissions.yaml`:
```yaml
blocked_commands:
  - pattern: "curl * | sh"
    reason: "pipe to shell is dangerous"
  - pattern: "pip install *"
    reason: "package installation requires review"
```

### API

```python
from agent.permissions import check_tool_permission

# 检查权限
decision = check_tool_permission('terminal', {'command': 'sudo apt install'})
if not decision.allowed:
    print(decision.reason)  # → Command blocked: matches "sudo *" (privilege escalation)

# 运行时添加规则
from agent.permissions import get_permission_engine
engine = get_permission_engine()
engine.add_custom_rule('pip install *', 'no auto install')
```

## 模块 2: LoopDetector（✅ 已实现）

**设计原则**: 旁路监控，只读不写，发现循环发信号。

**文件**: `agent/loop_detector.py`

**集成点**（已在 `run_agent.py` 中）:
1. `AIAgent.__init__()` → `self._loop_detector = ToolCallLoopDetector()` (1614-1618 行)
2. `_invoke_tool()` 完成后 → `self._loop_detector.record(...)` (8518-8524 行)
3. 顺序执行路径 → `self._loop_detector.record(...)` (9006-9012 行)
4. API call 前 → `loop_warning = self._loop_detector.detect()` → 注入警告 (9748-9768 行)

### 5 层检测

| 层级 | 检测内容 | 阈值 | 结果 |
|------|---------|------|------|
| 1 | 同一 tool + 同参数连续重复 | ≥ 3 次（read_file=8, search_files=6, browser_snapshot=5, browser_scroll=5） | hard abort |
| 2 | 同一 tool 连续失败（不同参数） | ≥ 3 次 | hard abort |
| 3 | 连续 assistant response 文本相似 | Jaccard ≥ 0.7 × 3 | soft warning |
| 4 | 连续 thinking 不调 tool | ≥ 5 次 | soft warning |
| 5 | 总调用数绝对上限 | ≥ 50 | hard abort |

### API

```python
from agent.loop_detector import ToolCallLoopDetector

detector = ToolCallLoopDetector()

# 每次 tool 执行后记录
detector.record('read_file', {'path': '/tmp/x'}, failed=False)
detector.record('terminal', {'command': 'bad'}, failed=True)

# 检测循环（在 API call 前调用）
result = detector.detect()
if result.is_loop:
    if result.is_hard:
        # 硬中断 — 注入警告到 messages
        messages.append({"role": "user", "content": result.injectable_warning})
    elif result.is_soft:
        # 软警告 — 也可选择注入

# 新对话开始重置
detector.reset()
```

## 模块 3: SecondBrain

**设计原则**: 类型化记忆，自动合并/冲突解决/衰减，FTS5 + LIKE 双引擎检索。

### 10 种记忆类型

identity, preference, goal, project, habit, decision, constraint, relationship, episode, reflection

### 核心机制

- **自动合并**: overlap ≥ 0.74 时合并已有记录
- **冲突解决**: 同类型矛盾 → confidence 高者胜
- **自动修剪**: active 21 天未见 → dismissed；durable 120 天无强化 → confidence 衰减
- **分级管理**: active（短期）/ durable（长期），强化 3+ 次自动升级

### API

```python
from agent.second_brain import SecondBrain

sb = SecondBrain()

# 存储候选记忆（自动合并/冲突解决）
sb.store_candidates([{
    'type': 'preference',
    'summary': '用户偏好简洁中文回复',
    'confidence': 0.8,
    'importance': 0.7,
    'durability': 0.9,
}])

# 检索相关记忆（注入 prompt）
context = sb.retrieve_relevant('中文回复')
# → "Relevant context from memory:\n- [preference] 用户偏好简洁中文回复"

# 定期维护（建议每小时调用一次）
sb.consolidate(throttle_seconds=3600)

# 概览
summary = sb.get_summary()  # {'total': 5, 'by_type': {'preference': 2, ...}}
```

## 集成点（run_agent.py）

1. **`__init__`** → 初始化三模块（try/except 包裹，失败不影响启动）
2. **`_invoke_tool`** → 权限检查（前置拦截）
3. **`_execute_tool_calls_concurrent`** → LoopDetector.record（旁路监控）
4. **API call 前** → LoopDetector 警告注入 + SecondBrain 记忆检索注入
5. **对话结束** → SecondBrain 异步存储 + LoopDetector 重置

## 配置

- `~/.hermes/permissions.yaml` — 自定义黑名单
- `~/.hermes/memory/second_brain.db` — SQLite 记忆数据库（自动创建）
