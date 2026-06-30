---
name: 同花顺问财
description: "同花顺/问财统一查询接口。覆盖行情查询、财务数据、行业数据、宏观数据、选股筛选（A股/港股/美股/ETF/基金/可转债/板块/期货期权）、基金/基金经理筛选、研报搜索、公告搜索、新闻搜索、事件数据、公司经营数据、股东股本、机构评级。Trigger: 问财/同花顺/iwencai/股票查询/选股/行情查询. Do NOT trigger for 非A股市场、通用理财问题、或非金融数据查询。"
version: 1.0.0
---

# 同花顺问财统一查询接口

## 一句话版本
通过同花顺 iwencai API (openapi.iwencai.com) 统一查询 A 股/港股/美股/基金/期货等全品类金融数据。所有子功能共用同一端点，按 query 内容自动路由。

## 核心 API
```python
import urllib.request, json, os

url = "https://openapi.iwencai.com/v1/query2data"
headers = {
    "Authorization": f"Bearer {os.environ['IWENCAI_API_KEY']}",
    "Content-Type": "application/json"
}
payload = {"query": "查询语句", "page": "1", "limit": "10", "is_cache": "1", "expand_index": "true"}
```

## 查询路由表
| 用户意图 | query 示例 | 返回字段 |
|----------|-----------|----------|
| 行情查询 | "贵州茅台最新价" | 最新价/涨跌幅/成交量/资金流向 |
| 财务查询 | "贵州茅台净利润" | 营收/净利润/ROE/负债率 |
| 行业查询 | "半导体行业估值" | PE/PB/行业排名 |
| 宏观查询 | "最新CPI数据" | CPI/PPI/社融/GDP |
| 选股 | "涨幅超过5%的科技股" | 符合条件的股票列表 |
| ETF/基金 | "近一年涨幅最大的ETF" | 基金列表+业绩 |
| 期货期权 | "原油最新价格" | 期货行情+波动率 |
| 研报/公告 | "比亚迪最新研报" | 研报标题+评级+目标价 |

## 反模式
- **"同时调用多个同花顺 skill"** → 所有功能已合并，一个 API 搞定
- **"不检查 IWENCAI_API_KEY"** → Key 不存在会返回 401
- **"不分页获取大量数据"** → 默认返回 10 条，关注 code_count，需要时翻页
