---
name: deep_thinking
version: 1.1.0
description: "CoPaw 深度思考技能：后台自动进行知识回顾、关联和固化，生成思考日记和知识卡片。三阶段处理（Review → Connect → Solidify），支持定时/手动/阈值触发。当用户需要查看思考成果、手动触发思考流程、或查询知识库时使用。"
---

# CoPaw 深度思考技能

## 概述

深度思考技能是 CoPaw 的后台知识处理系统，借鉴 OpenClaw Dream 模式，在后台自动执行记忆优化与知识巩固。

**核心流程：** Review（回顾） → Connect（关联） → Solidify（固化）

## 三阶段处理

| 阶段 | 说明 | 输出 |
|------|------|------|
| **Review** | 整理近期会话，提取关键点，发现重复问题模式 | 会话摘要 |
| **Connect** | 跨会话关联，建立知识图谱，识别高频关键词 | graph.json |
| **Solidify** | 生成知识卡片，提炼可复用知识，建议新技能方向 | 知识卡片 |

## 触发机制

| 触发方式 | 描述 | 默认配置 |
|---------|------|---------|
| **定时触发** | 每日凌晨 3:00 自动执行 | `frequency: daily` |
| **手动触发** | 用户主动请求执行 | `run` 命令 |
| **分阶段执行** | 仅执行某个特定阶段 | `review` / `connect` / `solidify` |

## 使用方式

### 查看结果

```bash
# 查看最新思考日记
cat ~/.copaw/thoughts/$(date +%Y-%m-%d).md

# 查看知识图谱
cat ~/.copaw/knowledge/graph.json | python3 -m json.tool

# 查看知识卡片
ls ~/.copaw/knowledge/cards/

# 列出所有思考日记
ls -lt ~/.copaw/thoughts/
```

### 手动触发

```bash
# 核心脚本路径
SCRIPT=~/.copaw/workspaces/default/skills/deep_thinking/deep_thinking.py

# 查看状态
python3 $SCRIPT status

# 手动触发完整流程
python3 $SCRIPT run

# 仅执行单个阶段
python3 $SCRIPT review      # 仅回顾
python3 $SCRIPT connect     # 仅关联
python3 $SCRIPT solidify    # 仅固化
```

## 输出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 思考日记 | `~/.copaw/thoughts/YYYY-MM-DD.md` | 每日思考记录 |
| 知识图谱 | `~/.copaw/knowledge/graph.json` | 关键词统计与关联关系 |
| 知识卡片 | `~/.copaw/knowledge/cards/` | 高频知识提炼（出现 ≥3 次自动生成） |
| 运行状态 | `~/.copaw/.thinking_state.json` | 当前运行状态 |

## 配置说明

所有配置内置于 `deep_thinking.py` 的 `DEFAULT_CONFIG`，自动优化：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `enabled` | `True` | 是否启用 |
| `frequency` | `daily` | 执行频率 |
| `time` | `03:00` | 执行时间 |
| `recencyHalfLifeDays` | `7` | 近期权重半衰期 |
| `maxAgeDays` | `30` | 最大保留天数 |
| `minConfidence` | `0.6` | 最小置信度阈值 |

**关闭方法：** 将 `DEFAULT_CONFIG["enabled"]` 设为 `False`。

## 异常处理

| 异常场景 | 处理方式 |
|----------|---------|
| **脚本路径变更** | 如果默认路径不存在，使用 `find ~/.copaw -name "deep_thinking.py" 2>/dev/null` 定位实际路径 |
| **思考日记目录不存在** | 首次运行时自动创建 `~/.copaw/thoughts/` 目录 |
| **知识卡片目录不存在** | 首次运行时自动创建 `~/.copaw/knowledge/cards/` 目录 |
| **无会话数据** | Review 阶段无数据时跳过，不生成空日记 |
| **Python 环境缺失** | 确保 `python3` 可用，依赖库需提前安装 |
| **并发执行冲突** | 通过 `.thinking_state.json` 中的锁机制防止重复执行 |
| **配置文件损坏** | 使用 `deep_thinking.py status` 检查配置完整性，损坏时回退到默认值 |

## 注意事项

- **隐私保护：** 所有思考数据本地存储，不上传云端
- **性能：** 后台执行，不影响正常使用
- **可解释性：** 每次思考都有清晰的日志记录
- **老化机制：** 超过 `maxAgeDays` 的旧数据自动清理
- **知识半衰期：** 近期会话权重更高（7 天半衰期）

## 设计参考

- 完整设计文档：`DESIGN.md`（同目录下）
- 详细使用说明：`USAGE.md`（同目录下）
- 灵感来源：OpenClaw Dream 模式（记忆提升 → MEMORY.md）
