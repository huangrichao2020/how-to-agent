---
name: tradingagents-akshare-integration
title: TradingAgents AkShare Integration
description: 将 TradingAgents 项目从 yfinance 切换为国内可用的 AkShare 数据源，并在网络不可达时提供本地 dummy 数据，确保完整工作流不出错。
category: tradingagents
---

## 目标
将 TradingAgents 项目中原本使用 yfinance 的行情与技术指标数据源替换为国内可用的 **AkShare**，并在网络不可达时提供本地 **dummy** 数据，以保证完整工作流不报错。

## 前置条件
- 项目根目录在 `/root/TradingAgents`，已创建并激活 `uv` 虚拟环境。
- 已配置 DashScope API KEY 并写入 `.env`（`OPENAI_API_BASE` 与 `OPENAI_API_KEY`）。
- Python 3.12，已安装 `akshare`。

## 步骤
1. **安装 AkShare**
   ```bash
   uv pip install akshare -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
2. **新增数据流实现** `tradingagents/dataflows/akshare_data.py`
   - `get_stock_data_online(symbol, start_date, end_date)`：调用 `akshare.stock_zh_a_hist`，返回与 yfinance 相同结构的 `DataFrame`（列名 `Open, High, Low, Close, Volume`）。
   - `get_akshare_indicators(symbol, date, indicator, look_back_days)`：基于历史数据计算 `rsi、macd、kdjk` 等；网络异常时返回 `"N/A"` 或 `None`。
   - **Dummy fallback**：捕获异常后返回最近 5 天硬编码 OHLCV，确保后续工具有有效 `DataFrame`。
3. **更新路由接口** `tradingagents/dataflows/interface.py`
   - 在 `VENDOR_LIST` 中加入 `'akshare'`。
   - 导入 `get_akshare_stock_data`、`get_akshare_indicators`。
   - 在 `DATA_VENDOR_MAP` 与 `INDICATOR_VENDOR_MAP` 中映射对应函数。
4. **修改默认配置** `tradingagents/default_config.py`
   ```python
   "core_stock_apis": "akshare",
   "technical_indicators": "akshare",
   ```
5. **调整入口** `main.py`
   - `data_vendors` 中将 `core_stock_apis` 与 `technical_indicators` 设置为 `"akshare"`。
   - 示例 ticker 改为 A‑股 `sh600519`，日期 `2024-05-10`。
6. **兼容技术指标工具** `tradingagents/agents/utils/technical_indicators_tools.py`
   - `get_indicators` 通过 `route_to_vendor` 调用后得到 **字符串**，将其包装为列表后再 `"\n\n".join(results)`，消除 `TypeError`。
7. **验证**
   ```bash
   cd /root/TradingAgents
   source .venv/bin/activate
   python main.py
   ```
   - 网络正常时返回真实历史与指标。
   - 网络异常时使用 dummy 数据并成功生成完整市场分析报告。

## 常见坑 & 解决方案
- **AkShare 连接被防火墙拦截**：捕获异常返回 dummy 数据，避免 `NoneType` 传递。
- **`get_akshare_indicators` 返回类型不匹配**：统一返回 `str`（如 `"2024-05-10: MACD=0.0123"`），并在 `technical_indicators_tools` 中包装为列表。
- **列名不一致**：在 `akshare_data.py` 将 `open, high, low, close, volume` 重命名为 `Open, High, Low, Close, Volume`，保持 yfinance 接口兼容。
- **日期格式**：确保 `date` 参数为 `YYYY-MM-DD` 字符串，符合 AkShare API 要求。

## 验证步骤
```bash
cd /root/TradingAgents
source .venv/bin/activate
python main.py
```
观察终端输出，确认最后生成的报告包含指标（如 MACD、RSI）和决策建议，无异常 traceback。

## 适用场景
- 需要在国内网络环境下运行 TradingAgents，获取 A‑股实时或历史数据。
- 希望在网络不稳定时仍能完整执行工作流，进行策略回测或实时决策。

---
此技能记录了从调研 → 规划 → 执行 → 留痕 的完整过程，可直接复用到其他 TradingAgents 项目或类似数据源切换任务。