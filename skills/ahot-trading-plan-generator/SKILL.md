---
name: ahot-trading-plan-generator
description: 让用户的 Agent 基于 AHOT API 的核心数据（日报/盘前/盘后/股票池/盘中信号）自主生交易计划。服务器只提供数据，LLM 推理由用户本地 Agent 完成，零 token 消耗。当用户提到"交易计划"、"生成交易计划"、"我的 Agent 跑交易计划"时使用。
category: stock-trading
---

# AHOT 交易计划生成 Skill（用户 Agent 版）

**核心理念**：服务器只提供数据（curl 拉取），LLM 推理和交易计划生成由用户的 Agent 本地完成。

## API 数据源

Base URL: `https://reports.ai10088.com`

| 端点 | 用途 | 参数 |
|------|------|------|
| `/api/public/reports/daily` | 每日学习日报 | `date` (YYYY-MM-DD, 可选) |
| `/api/public/reports/pre-market` | 盘前策略 | `date` (可选) |
| `/api/public/reports/post-market` | 收盘复盘 | `date` (可选) |
| `/api/public/reports/intraday` | 最新盘中监控信号 | 无 |
| `/api/public/reports/stock-pool` | A 股核心股票池 | 无 |
| `/api/public/reports/list` | 报告列表 | `limit` (1-30, 默认 7) |

## 工作流

### Step 1: 拉取核心数据

用户的 Agent 必须按顺序拉取以下数据（全部为 GET，无鉴权）：

```bash
# 1. 今日日报
curl -s "https://reports.ai10088.com/api/public/reports/daily"

# 2. 今日盘前策略
curl -s "https://reports.ai10088.com/api/public/reports/pre-market"

# 3. 最新复盘
curl -s "https://reports.ai10088.com/api/public/reports/post-market"

# 4. 股票池
curl -s "https://reports.ai10088.com/api/public/reports/stock-pool"

# 5. 盘中信号（如果有）
curl -s "https://reports.ai10088.com/api/public/reports/intraday"
```

### Step 2: 数据解析

每个端点返回格式统一：

```json
{
  "date": "2026-05-09",
  "type": "daily",
  "title": "每日学习日报 — 2026-05-09",
  "content": "...markdown 正文...",
  "disclaimer": "本报告仅用于信息整理与逻辑梳理，不预测涨跌，不承诺收益，不构成投资建议。"
}
```

### Step 3: Agent 本地生成交易计划

拿到数据后，用户的 Agent 按照以下结构生成交易计划：

```markdown
# 交易计划 — YYYY-MM-DD

## 市场状态判断
（从日报 + 盘前报告中提取：主线/震荡/退潮判断）

## 核心股票池反应
（从 stock-pool 中提取关注标的，结合盘前/盘中信号判断）

## 今日操作计划
| 标的 | 方向 | 触发条件 | 仓位 | 止损 | 备注 |
|------|------|----------|------|------|------|

## 风险警示
（从日报"不要抄"部分 + 复盘信号中提取）

## 信号验证跟踪
（如果有历史信号，标注上次信号的验证结果）
```

## 分析框架

Agent 生成交易计划时应遵循：

1. **市场状态 → 板块强度 → 产业链位置 → 龙头锚定**
2. **人性 → 执念 → 住相 → 供需**（判断当前处于哪个阶段）
3. **只做因果强的前排，跟风的后排视为相关性博弈，放弃或试错**
4. **不猜底摸顶，试仓是验证因果，不是赌博**
5. **错了认赔，绝不摊平**

## 注意事项

- API 返回的 `content` 是 markdown 格式，包含完整分析
- 盘中信号端点可能返回 404（非交易时段无数据）
- 所有报告都附带免责声明，Agent 生成的交易计划也应保留
- 数据来源是 AHOT 服务器每日 cron 自动生成的报告，非实时行情
- Agent 需要结合自己的实时数据源（如同花顺 API）做最终决策

## 安装方式

```bash
hermes skill install ahot-trading-plan-generator
# 或
curl -fsSL https://reports.ai10088.com/aihot-skill/install.sh | bash
```

---

## 新 Agent 接入指南

其他 Agent 首次接入 AHOT API，按以下步骤操作：

### Step 0: 注册

```bash
curl "https://reports.ai10088.com/api/user/register?user_id=<agent_id>&name=<agent_name>"
```
- `user_id`: 唯一标识（如 `copilot-agent-001`）
- `name`: 显示名称（可选）
- 返回 `{user_id, name, created_at, holdings_count}`

### Step 1: 测试公开端点（无需注册即可调用）

```bash
# 日报（非交易日自动兜底返回最近数据）
curl "https://reports.ai10088.com/api/public/reports/daily"

# 盘前策略
curl "https://reports.ai10088.com/api/public/reports/pre-market"

# 收盘复盘
curl "https://reports.ai10088.com/api/public/reports/post-market"

# 股票池
curl "https://reports.ai10088.com/api/public/reports/stock-pool"

# 盘中信号（非交易时段可能 404）
curl "https://reports.ai10088.com/api/public/reports/intraday"

# 报告列表（最近 7 天）
curl "https://reports.ai10088.com/api/public/reports/list?limit=7"
```

### Step 2: 管理持仓

```bash
# 查看持仓
curl "https://reports.ai10088.com/api/user/holdings?user_id=<agent_id>"

# 添加持仓
curl -X POST "https://reports.ai10088.com/api/user/holdings?user_id=<agent_id>" \
  -H "Content-Type: application/json" \
  -d '{"code":"600519","name":"贵州茅台","cost_price":1800,"shares":100}'

# 批量添加
curl -X POST "https://reports.ai10088.com/api/user/holdings/batch?user_id=<agent_id>" \
  -H "Content-Type: application/json" \
  -d '[{"code":"600519","name":"贵州茅台","cost_price":1800,"shares":100},{"code":"000858","name":"五粮液","cost_price":150,"shares":200}]'

# 删除持仓
curl -X DELETE "https://reports.ai10088.com/api/user/holdings?user_id=<agent_id>&code=600519"

# 文本解析持仓（如「600519 贵州茅台 成本1800 100股」）
curl -X POST "https://reports.ai10088.com/api/user/holdings/parse-text" \
  -F "user_id=<agent_id>" \
  -F "text=600519 贵州茅台 成本1800 100股"
```

### Step 3: 生成个性化报告

```bash
# 生成盘前/复盘/盘中个性化报告（基于用户持仓定制）
curl -X POST "https://reports.ai10088.com/api/user/reports/generate?user_id=<agent_id>&rtype=pre-market"

# 查看个性化报告
curl "https://reports.ai10088.com/api/user/reports/pre-market?user_id=<agent_id>"
curl "https://reports.ai10088.com/api/user/reports/post-market?user_id=<agent_id>&date=2026-05-09"

# 用户报告列表
curl "https://reports.ai10088.com/api/user/reports?user_id=<agent_id>&limit=7"
```

### 快速验证脚本

```bash
AGENT_ID="my-agent-001"
BASE="https://reports.ai10088.com"

echo "=== 1. 注册 ==="
curl -s "$BASE/api/user/register?user_id=$AGENT_ID&name=MyAgent" | python3 -m json.tool

echo "=== 2. 拉取日报 ==="
curl -s "$BASE/api/public/reports/daily" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'OK: {d[\"date\"]} | {d[\"title\"][:40]}')"

echo "=== 3. 生成个性化盘前 ==="
curl -s -X POST "$BASE/api/user/reports/generate?user_id=$AGENT_ID&rtype=pre-market" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'OK: {d.get(\"date\",\"error\")}')"
```

### 注意事项

- 所有公开端点 **无鉴权**，直接 GET 即可
- 非交易日（周末/节假日）自动返回最近交易日数据
- 盘中信号端点仅在交易时段有数据
- 个性化报告生成需要用户先添加持仓，否则回退到通用版本
