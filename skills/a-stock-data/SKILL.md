---
name: a-stock-data
description: "Use when the user asks about A-share stock data: quotes, fundamentals, technicals, capital flow, sectors, news. Covers Baostock, Tencent, Eastmoney, AkShare, MX API. Trigger: A股/行情/财报/涨停/板块/资金流. Do NOT trigger for non-A-share markets (US/HK/Crypto), generic finance questions, or trading advice without data context."
version: 4.3.0
---

# A 股全栈数据工具包

## 一句话版本

从 A 股数据获取到结构化的端到端工具包。核心原则：多数据源降级、本地缓存优先、频控严格。数据只是原材料，不做投资决策，除非叠加交易宪法框架。

## 如何使用本技能

1. **先运行决策树**: `checklists/decision-tree.md`
2. **从 philosophy 开始**: 判断数据时效性需求 → 匹配数据源
3. **按需加载 references**: 不要全读，匹配问题到具体文件
4. **交付前运行**: `checklists/ship-readiness.md`

## 数据源优先级（高→低）

| 优先级 | 数据源 | 覆盖 | 可靠性 | 频控 | 备注 |
|--------|--------|------|--------|------|------|
| 1 | 腾讯行情 API | 实时行情 | ⭐⭐⭐⭐⭐ | 无 | 最快最稳，GBK 编码 |
| 2 | 复盘盒子 API | 涨停/板块/消息 | ⭐⭐⭐⭐ | 5s/请求 | `~/.hermes/data/fupanhezi/fupanhezi.db` |
| 3 | MX API (东方财富) | 涨停/资金流 | ⭐⭐⭐ | 20次/天/Key | 用 `mkt_3Y4C...` key |
| 4 | Baostock | 历史K线/财务 | ⭐⭐⭐⭐⭐ | 免费 | Parquet 缓存 |
| 5 | AkShare | 备用数据 | ⭐⭐⭐ | 免费 | 网络不稳定时不可用 |

## 核心反模式（看到这些立刻停下）

- **"直接去东方财富板块 API 拿数据"** → clist/push2 经常空数据。先腾讯，失败再降级
- **"用 yfinance 查 A 股"** → 对 A 股支持极差，经常超时。用腾讯或 Baostock
- **"一次性查全市场 5000+ 股票"** → 2GB 会 OOM。分批 ≤200 只
- **"不设频控连续调用 API"** → MX 每天 20 次，复盘盒子 ≥5s 间隔
- **"用浏览器自动化拿行情"** → 太重，2GB 易崩溃。优先 API
- **"把数据源失败当成没有数据"** → 先降级再确认
- **"在 non-trading hours 查实时行情"** → 9:00 前/15:00 后是昨日收盘

## 配套文件

- `references/01-philosophy.md` — 数据获取哲学 + 时效性矩阵
- `references/02-api-reference.md` — 各数据源 API 详细参考
- `references/03-pitfalls.md` — 常见坑（网络/内存/时间/编码）
- `checklists/decision-tree.md` — 数据源选择决策树
- `checklists/ship-readiness.md` — 交付前检查清单
