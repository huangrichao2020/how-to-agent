---
name: tradingagents-baostock-local-cache
title: TradingAgents Baostock Local Cache Integration
description: 将 TradingAgents 项目对接 Baostock 数据源，通过全量 Dump 脚本将 A 股历史日线数据落盘为本地 Parquet 缓存，实现 0 延迟、0 频率限制的技术分析工作流。
category: tradingagents
---

## 目标
解决 AkShare/yfinance 在国内网络环境不稳定或存在频率限制的问题。通过 **Baostock** 稳定拉取 A 股历史数据并缓存至本地 `data/historical/*.parquet`，在 TradingAgents 中实现 `local_cache` 数据源。

## 前置条件
- 项目根目录在 `/root/TradingAgents`。
- Python 环境已安装 `baostock` 和 `pyarrow`：
  ```bash
  uv pip install baostock pyarrow -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

## 步骤

1. **全量/增量 Dump 脚本** `dump_all_stocks.py`
   - 使用 `baostock.login()` 登录（**无需 API Key**）。
   - 调用 `bs.query_stock_basic()` 获取全量代码列表，过滤出主板股票（`sh.60xxxx`, `sz.00xxxx`, `sz.30xxxx`）。
   - **增量更新逻辑**：检查已有 Parquet 文件的最新日期，仅下载从该日期到今天的增量数据。若无文件则全量下载。
   - 循环调用 `bs.query_history_k_data_plus(..., frequency="d", adjustflag="2")` 拉取前复权日线数据。
   - 将每只股票的数据合并/保存为 `data/historical/{code.replace('.','_')}.parquet`。
   - 包含 `time.sleep(0.02)` 防止被服务端限流。
   - **每日凌晨 02:00** 通过 Cron 任务自动运行增量更新。

2. **新增数据流实现** `tradingagents/dataflows/local_cache_data.py`
   - 定义 `DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "historical")`（注意路径层级）。
   - `_find_file(symbol)`: 兼容 `sh.600000`, `600000.SH`, `sh600000` 等多种格式，查找本地 Parquet 文件（统一转为小写文件名）。
   - `get_stock_data_online(symbol, start_date, end_date)`: 读取 Parquet，按日期过滤，返回索引为 `date`、列名为小写的 `DataFrame`。
   - `get_local_indicators(symbol, indicator, curr_date, look_back_days)`: 返回字符串格式结果，支持以下**用户定制化指标**：
     - **25 日均线 (MA25)**：输出 `MA25=xxx, 趋势:向上 (关注)` 或 `趋势:向下 (观望)`。
       - **核心逻辑**：仅当 `MA25(t) > MA25(t-1)` 时判定为向上。**此指标是选股过滤器，仅“向上”的标的值得进一步分析**。
     - **MACD (6, 13, 6)**：
       - **自定义参数**：EMA(6), EMA(13), Signal(6)。比默认的 (12,26,9) 更敏感，适合短线。
       - 输出格式：`DIF=xxx, DEA=xxx, MACD=xxx`。
     - **5 日成交量均线 (Vol MA 5)**：`VolMA5=xxx`
     - **60 日成交量均线 (Vol MA 60)**：`VolMA60=xxx`

3. **更新路由接口** `tradingagents/dataflows/interface.py`
   - 在 `VENDOR_LIST` 中加入 `'local_cache'`。
   - 导入 `local_cache_data` 中的 `get_stock_data_online` 和 `get_local_indicators`。
   - 在 `VENDOR_METHODS['get_stock_data']` 和 `VENDOR_METHODS['get_indicators']` 中注册 `'local_cache'`。

4. **修改默认配置** `main.py`
   - `config["data_vendors"]` 中将 `core_stock_apis` 与 `technical_indicators` 设置为 `"local_cache"`。
   - 示例 ticker 使用 `sh.600000` 或 `sh.600519`。

## 常见坑 & 解决方案
- **DATA_DIR 路径层级**：`local_cache_data.py` 位于 `dataflows/` 下，因此 `DATA_DIR` 必须指向 `../../data/historical`，否则找不到文件。
- **Baostock 登录/登出**：必须在脚本开头 `bs.login()`，结尾 `bs.logout()`，否则并发或多次调用可能失败。
- **Ticker 格式匹配**：Baostock 使用 `sh.600000`，而 TradingAgents 可能传入 `600000.SH` 或 `sh600000`。`_find_file` 必须包含完善的格式转换逻辑（统一转为小写 `sh_600000.parquet`）。
- **指标返回类型**：TradingAgents 的 `technical_indicators_tools.py` 会将多个指标结果用 `\n\n`.join(results) 拼接，因此每个指标调用必须返回 **字符串**，绝不能返回 DataFrame 或 Dict。
- **MACD 参数**：用户要求使用 **(6, 13, 6)** 而非默认的 (12, 26, 9)，实现时使用 `ewm(span=N, adjust=False)`。
- **新闻/基本面**：本地缓存不提供新闻数据。分析个股时，应结合 Web Search / 同花顺 / 东方财富 等外部技能获取新闻与基本面信息。

## 定时任务配置
Cron Job ID: `f83705aa960d`
- 调度: `0 2 * * *`（每日 02:00）
- 执行命令: `cd /root/TradingAgents && source .venv/bin/activate && python dump_all_stocks.py`
- 行为：自动检测已有数据日期，仅增量拉取最新交易日数据。

## 验证步骤
```bash
cd /root/TradingAgents
source .venv/bin/activate
python main.py
```
观察输出应包含成功的 `get_stock_data` 和 `get_indicators` 调用，并最终生成完整的分析报告。

## 跨项目复用 (Info-Hub 模式)
这套引擎已被成功复用到用户的正式项目 `info-hub` (`huangrichao2020/info-hub`) 中。
- **数据共享**：通过软链将 `TradingAgents/data/historical` 挂载到 `info-hub/backend/data/historical`，实现一份数据多处读取（约 4700 只股票，2.6GB）。
- **异步调度集成**：在 FastAPI 项目中，通过 `APScheduler` (AsyncIOScheduler) 替代独立 Cron，利用 `loop.run_in_executor` 运行同步的 Baostock 抓取逻辑。
- **API 路由**：通过 `/api/stock/analysis/{symbol}` 提供查询，通过 `/api/stock/scan/ma25-up` 提供全市场 MA25 趋势向上的股票扫描。

## 适用场景
- 需要对 A 股进行高频技术分析，但受限于外部 API 频率限制。
- 构建离线回测或研究环境，要求数据加载极快且稳定。
- 为任何 FastAPI 或 Python 后端提供即插即用的本地 A 股日线引擎。
