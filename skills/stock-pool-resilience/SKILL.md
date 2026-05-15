---
name: stock-pool-resilience
description: 盘前股池生成的高可用策略 — 多时间点重试 + 数据源降级 + Key 轮转。确保在阿里云网络波动或 API 配额耗尽时，盘中监控任务仍有数据可用。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [stock, resilience, cron, api-rotation]
    related_skills: [a-stock-realtime-monitor-fallback, tencent-market-data-adapter]
---

# 盘前股池高可用机制

## 核心痛点
盘中监控 DAG 依赖 `pool_YYYYMMDD.json`。若 08:20 单次执行因网络超时（东财接口）或配额耗尽失败，全天监控将瘫痪。

## 解决方案：三层防护

### 1. 多时间点自动重试 (Cron)
设置三个不同时间点的 Cron Job，脚本内部自带“幂等性”检查：
- **08:20** - 首次尝试
- **08:40** - 第一次重试
- **09:00** - 第二次重试（开盘前最后机会）

**脚本逻辑**：启动时先检查 `~/.hermes/stock_monitor/pool_{today}.json` 是否存在。若存在则直接退出，避免重复计算和 API 浪费。

### 2. 四级数据源降级链路 (2026-05-14 升级)

在 `scripts/stock_monitor/prepare_pool.py` 中实现多级切换：
1. **首选**：同花顺热点接口 (`zx.10jqka.com.cn`)。获取当日强势股代码及题材。
   - *优势*：零鉴权，响应快，直接锁定资金关注点。
   - *缺陷*：缺少市值/成交额等数值字段。
2. **补全**：腾讯行情接口 (`qt.gtimg.cn`)。批量补充上述代码的实时行情。
   - *逻辑*：解析 GBK 响应，提取 `总市值`、`成交额`、`换手率`。
3. **备选**：东财全市场 (`ak.stock_zh_a_spot_em`)。**现状**：反爬严重，常报 `RemoteDisconnected`，仅作为最后兜底。
4. **终极兜底**：复制最近交易日股池。若所有接口均失败，自动寻找 `pool_{yesterday}.json` 并复制。

> ⚠️ **关键修复**：原脚本中腾讯/同花顺函数被硬编码为返回空 DataFrame，已修复为“同花顺取码 + 腾讯补数”的组合模式，解决了字段缺失导致的过滤失效问题。

### 3. API Key 轮转 (Key Rotation)
针对东财接口的每日配额限制（20次/Key），使用 `tools/eastmoney_key_rotator.py`：
- 维护 3 个 Key (`mkt_EMpsA...`, `mkt_fTAwI...`, `mkt_wGWUn...`)。
- 每次请求前调用 `get_available_key()`，自动选择当日未达限额的 Key。
- 计数文件存储在 `~/.hermes/eastmoney_usage.json`。

## 实施步骤

1. **修改脚本**：在 `prepare_pool.py` 顶部增加文件存在性检查。
2. **配置 Cron**：
   ```bash
   # 示例：每交易日 08:20, 08:40, 09:00 运行
   20 8 * * 1-5 cd /root/hermes-agent && source .env && python scripts/stock_monitor/prepare_pool.py
   40 8 * * 1-5 cd /root/hermes-agent && source .env && python scripts/stock_monitor/prepare_pool.py
   0 9 * * 1-5 cd /root/hermes-agent && source .env && python scripts/stock_monitor/prepare_pool.py
   ```
3. **验证降级**：手动断开网络或模拟东财超时，观察日志是否打印 `[降级] 使用腾讯行情接口...`。

## 常见陷阱
- **幂等性缺失**：如果不检查文件是否存在，多次 Cron 会并发拉取历史指标，导致服务器 CPU/内存飙升（2GB 环境下极易 OOM）。
- **Key 计数重置**：`eastmoney_usage.json` 中的 `last_reset` 字段必须与系统日期比对，否则跨天后不会自动清零计数。