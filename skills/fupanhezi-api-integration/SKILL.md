---
name: fupanhezi-api-integration
description: 复盘盒子 (fupanhezi.com) API 集成指南 — 涨停梯队/题材轮动/消息面/龙虎榜席位数据采集与 Wiki 链构建。适用于 A 股短线分析、题材归因、游资跟踪。
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [a-stock, api, data-collection, wiki]
    related_skills: [a-stock-data, a-stock-limit-up-tracker]
---

# 复盘盒子 API 集成

## 核心能力

复盘盒子提供**无需登录、零鉴权**的 A 股短线数据，是短线分析的第一数据源：

| 端点 | 功能 | 参数 |
|------|------|------|
| `POST /stock/v1/board/zt` | 涨停梯队 | `{"symbol":"", "date":"YYYY-MM-DD", "num":0}` |
| `POST /stock/v1/news/list` | 消息面（分页） | `{"page":1, "pageSize":50}` |
| `POST /stock/v1/board/sub` | 题材细分 | `{"symbol":"板块名", "date":"YYYY-MM-DD"}` |
| `POST /stock/v1/board/sub_stock` | 题材成分股 | `{"code":"", "boardName":"细分名", "date":"YYYY-MM-DD"}` |
| `POST /stock/v1/lhb/seats` | 龙虎榜游资席位 | 无参数 |

## 频控策略（关键）

- **请求间隔 ≥ 5 秒**（防止被封）
- **失败重试 ≤ 2 次**，重试间隔 10 秒
- **每日只采一次**（收盘后 15:30 执行）
- **已有数据不重复采集**（SQLite 去重）

## 数据采集脚本

路径：`/root/hermes-agent/tools/fupan_data/collector.py`

```bash
# 单日采集
python3 collector.py --date 2026-05-14

# 批量回补最近 20 个交易日
python3 collector.py --backfill
```

数据存储：`~/.hermes/data/fupanhezi/fupanhezi.db`（SQLite）

## Wiki 链自动构建

路径：`/root/hermes-agent/tools/fupan_data/build_stock_wiki.py`

为每只涨停股票创建 gbrain 页面，同题材股票互相链接：

```bash
python3 build_stock_wiki.py
```

Cron：每交易日 16:00 自动运行（job: `239f51e85b70`）

## 定时任务

| Job ID | 名称 |  schedule |
|--------|------|-----------|
| `3af4bd5fbcc1` | 复盘盒子每日数据采集 | 每交易日 15:00 |
| `239f51e85b70` | 涨停股票 Wiki 链构建 | 每交易日 16:00 |

## 使用示例

```python
import sqlite3, json

conn = sqlite3.connect('~/.hermes/data/fupanhezi/fupanhezi.db')
c = conn.cursor()

# 获取某日涨停数据
c.execute("SELECT raw_data FROM zt_data WHERE date='2026-05-14'")
row = c.fetchone()
zt_data = json.loads(row[0]).get('data', [])

# 按连板数分组
by_level = {}
for item in zt_data:
    level = item.get('ztlbNum', 0)
    by_level.setdefault(level, []).append(item)
```

## 注意事项

1. **不要频繁调用**：频控是生命线，违反会被封 IP
2. **非交易日返回空数据**：采集前检查是否为交易日
3. **板块名称需精确匹配**：`board/sub` 的 `symbol` 参数必须是完整板块名（如"机器人概念"）
4. **Wiki 同步延迟**：gbrain → wiki 同步每 4 小时运行一次，新建页面可能需要等待