---
name: fupanhezi-data-pipeline
description: 复盘盒子 (fupanhezi.com) API 数据采集管线。获取 A 股涨停梯队、题材轮动、消息面及游资席位数据，用于短线/中线分析的第一数据源。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  yao_category: "A股数据"
  hermes:
    tags: [a-stock, data-collection, fupanhezi]
    related_skills: [a-stock-data, a-stock-market-analysis-framework]
---

# 复盘盒子数据采集管线

## 核心能力

从 `fupanhezi.com` 采集以下四类核心数据：
1. **涨停梯队** (`/stock/v1/board/zt`)：当日所有涨停股票的连板数、涨停原因、游资标记。
2. **消息面** (`/stock/v1/news/list`)：按重要性排序的财经新闻及关联题材标签。
3. **题材轮动** (`/stock/v1/board/sub` + `/stock/v1/board/sub_stock`)：板块细分题材及成分股列表。
4. **游资席位** (`/stock/v1/lhb/seats`)：全市场 110+ 知名游资营业部映射表。

## 频控与稳定性策略

- **请求间隔**：默认 5 秒（`REQUEST_INTERVAL = 5`），防止触发 429 限流。
- **重试机制**：失败自动重试 2 次，重试间隔递增（10s, 20s）。
- **本地缓存**：使用 SQLite (`~/.hermes/data/fupanhezi/fupanhezi.db`)，已有日期不重复采集。
- **分页限制**：消息面最多采 3 页（150 条），题材轮动只采 TOP 5 板块。

## 脚本路径

- **主脚本**: `/root/hermes-agent/tools/fupan_data/collector.py`
- **数据存储**: `~/.hermes/data/fupanhezi/fupanhezi.db`

## 使用方法

### 1. 单日采集
```bash
cd /root/hermes-agent/tools/fupan_data
python3 collector.py --date 2026-05-14
```

### 2. 批量回补（最近 20 个交易日）
```bash
python3 collector.py --backfill
```

### 3. 定时任务
Cron job `3af4bd5fbcc1`：每周一至周五 15:00 自动采集。

## 数据库 Schema

| 表名 | 字段 | 说明 |
|------|------|------|
| `zt_data` | date, raw_data, collected_at, status | 涨停梯队（按日期唯一） |
| `news_data` | date, raw_data, collected_at, status | 消息面（按日期唯一） |
| `board_data` | date, board_name, raw_data, collected_at, status | 板块细分（联合主键） |
| `lhb_seats` | collected_at, raw_data, status | 龙虎榜席位（一次性） |
| `trade_dates` | date, collected_at | 交易日列表 |

## Python 查询示例

```python
import sqlite3, json

conn = sqlite3.connect('~/.hermes/data/fupanhezi/fupanhezi.db')
c = conn.cursor()

# 查询某日涨停数据
c.execute("SELECT raw_data FROM zt_data WHERE date='2026-05-14'")
row = c.fetchone()
zt_list = json.loads(row[0]).get('data', []) if row else []
print(f"涨停数: {len(zt_list)}")

# 查询某日消息面
c.execute("SELECT raw_data FROM news_data WHERE date='2026-05-14'")
row = c.fetchone()
news_list = json.loads(row[0]).get('data', []) if row else []
print(f"消息数: {len(news_list)}")

conn.close()
```

## 注意事项

1. **频控必须遵守**：API 有频率限制，违反会被封 IP
2. **非交易日无数据**：周末/节假日调用返回空数组
3. **板块采集控制量**：默认只采 TOP 3-5 板块，防止超时
4. **龙虎榜席位只需采一次**：静态数据，不随日期变化

## 相关方法论

- [[market-daily-report-methodology]] — 市场复盘报告
- [[market-structure-report-methodology]] — 市场结构报告
- [[portfolio-analysis-report-methodology]] — 持仓分析报告

## API 端点清单

| 端点 | 方法 | 参数示例 | 用途 |
|------|------|----------|------|
| `/stock/v1/trade-date/latest` | POST | `{"endDate":"", "num":1}` | 获取最新交易日 |
| `/stock/v1/board/zt` | POST | `{"symbol":"", "date":"2026-05-14", "num":0}` | 涨停梯队详情 |
| `/stock/v1/news/list` | POST | `{"page":1, "pageSize":50}` | 消息面列表 |
| `/stock/v1/board/sub` | POST | `{"symbol":"机器人概念", "date":"2026-05-14"}` | 板块细分题材 |
| `/stock/v1/board/sub_stock` | POST | `{"code":"", "boardName":"减速器", "date":"..."}` | 细分题材成分股 |
| `/stock/v1/lhb/seats` | POST | `{}` | 游资席位表 |

## 数据应用

在 `a-stock-data` skill 中，复盘盒子已被设为**优先级 0** 的数据源，直接支撑：
- **市场风格判断**：通过涨停家数和连板高度识别妖股抱团或机构趋势。
- **板块强度分析**：通过题材轮动数据定位资金进攻方向。
- **龙头锚定**：通过涨停梯队和游资席位确认身位龙和资金属性。

## 避坑指南

1. **非交易日处理**：调用前先用 `trade-date/latest` 校验，否则返回空数据。
2. **ResultCode 类型**：部分接口返回 `"0"` (string)，部分返回 `0` (int)，代码需统一用 `str()` 比较。
3. **板块名称匹配**：`board/sub` 的 `symbol` 必须传准确的板块全称（如“机器人概念”而非“机器人”）。
4. **SQLite Schema 变更**：增加新字段时需删除旧 `.db` 文件重建，或手动执行 `ALTER TABLE`。
5. **News API 分页**：`news/list` 必须用 POST 且带 `page/pageSize` 参数，GET 会报 404。
6. **频控红线**：实测间隔低于 3s 极易触发 429，建议保持 5s 以上。
7. **微信文章反爬**：公众号主页有强反爬，浏览器自动化易超时。盘前早报已切换为复盘盒子消息面数据源。
7. **盘中数据为空**：15:00 收盘前采集当日数据可能返回空数组，属于正常现象。