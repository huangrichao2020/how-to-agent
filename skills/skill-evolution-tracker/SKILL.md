---
name: skill-evolution-tracker
category: devops
description: "技能演进追踪机制 — 从理解→熟练→本能的三阶段晋升体系"
version: "1.0"
created: "2026-05-06"
---

# 技能演进追踪 (Skill Evolution Tracker)

## 核心理念

来源：抖音图文"进化手册-第026期" —— "一个人最隐蔽的堕落，是看起来很努力"

**核心观点**：真正的能力不是第一次理解时产生的，而是在一次次重复、修正、调用中长进神经系统。

Hermes 有 229 个 skills，但**不是学了就厉害，而是哪些已经长进代码本能**。

## 三阶段模型

| 阶段 | 使用次数 | Hermes 对应 | 特征 |
|------|---------|-------------|------|
| **理解** | 1-10 次 | Skill 文件 | 被动加载，需要用户触发 |
| **熟练** | 10-100 次 | Skill + 修正记录 | 主动加载，成功率提升 |
| **本能** | 100+ 次 | BOOT.md / Hook / 代码 | 自动执行，无需加载 |

## 工具：skill_tracker.py

位置：`~/.hermes/skill_tracker.py`

### API

```python
from skill_tracker import skill_used, skill_failed, get_stats

# 成功使用后调用
skill_used("douyin-content-extraction")

# 失败时调用
skill_failed("douyin-content-extraction", context="弹窗关闭失败")

# 查看统计
stats = get_stats("douyin-content-extraction")
# => {"total": 3, "success_rate": 0.67, "stage": "理解", ...}

# 查看所有 skills 摘要
all_stats = get_stats()
# => {"skills": [...], "total_tracked": N}
```

### 存储格式

`~/.hermes/skill_usage.json`:

```json
{
  "skill-name": {
    "total": 45,
    "success": 38,
    "fail": 7,
    "first_used": 1775408140,
    "last_used": 1777827340,
    "contexts": ["场景1", "场景2"],
    "stage": "熟练"
  }
}
```

## 晋升条件

一个 Skill 从"熟练"晋升为"本能"（写入 BOOT.md/Hook）需要满足：

1. **使用次数 ≥ 50 次**
2. **成功率 ≥ 80%**
3. **阶段为"熟练"或"本能"**

### 衰退检测

- **90 天未使用** → 标记为"衰退"
- **成功率 < 30%** → 需要重写或删除

## 当前状态（2026-05-06）

| Skill | 次数 | 成功率 | 阶段 | 状态 |
|-------|------|--------|------|------|
| browser-automation-low-memory | 62 | 89% | 本能 | ✅ 成熟 |
| a-stock-market-analysis-framework | 45 | 84% | 熟练 | 📈 接近晋升 |
| douyin-content-extraction | 3 | 67% | 理解 | 🌱 成长中 |

## 集成点

### 1. Skill 执行后自动记录

在关键 skill 的执行入口/出口嵌入：

```python
# 在 skill 执行成功后
from skill_tracker import skill_used
skill_used("skill-name")

# 在 skill 执行失败后
from skill_tracker import skill_failed
skill_failed("skill-name", context="具体错误原因")
```

### 2. 定期巡检

每周运行一次衰退检测：

```python
from skill_tracker import find_decay_risks, find_promotion_candidates

# 查找可晋升的 skills
candidates = find_promotion_candidates()
for c in candidates:
    print(f"{c['name']}: {c['total']}次, {c['success_rate']}成功率 → 建议晋升到 BOOT.md")

# 查找衰退 risks
risks = find_decay_risks()
for r in risks:
    print(f"{r['name']}: {r['days_since_use']}天未使用 → 考虑删除")
```

## 哲学

> "理解只是入门，重复才能入骨！"
> 
> 真正的进化不是增加更多知识，而是让正确的模式变成不需要思考的动作。
> 
> **不是学了 229 个 skill 就厉害，而是哪些 skill 已经长进代码本能。**

## 相关文件

- `~/.hermes/skill_tracker.py` — 追踪器实现
- `~/.hermes/skill_usage.json` — 数据存储
- gbrain: `repetition-to-instinct-architecture` — 方法论页面