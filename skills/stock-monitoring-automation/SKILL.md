---
name: stock-monitoring-automation
description: 自动化 A 股盘中监控与推送系统。基于 AmazingData 中继 + Baostock 数据源，实现盘前高辨识度股池筛选及盘中实时信号捕捉。
tags: [stock, automation, cron, amazingdata, baostock, feishu]
---

# Stock Monitoring Automation (A股监控自动化)

## 数据源选择

| 数据源 | 用途 | 可用性 |
|--------|------|--------|
| **AmazingData 中继** | 盘中实时行情、1分钟K线 | ✅ 2026-05-05 已恢复 |
| **Baostock Parquet** | 历史日线数据（2021年起） | ✅ 本地 4786 只股票已缓存 |
| AKShare | 兜底（连接不稳定） | ⚠️ 阿里云环境经常断连 |

### AmazingData 架构
```
阿里云服务器 → www.ai10088.com/amazingdata (中继) → Windows 客户端 101.230.159.234:8600 (同花顺)
```
- 中继端点：`https://www.ai10088.com/amazingdata`
- 鉴权：Bearer Token（存于 `AMAZINGDATA_PUBLIC_RELAY_TOKEN`）
- 支持周期：`day`, `week`, `month`, `min1`, `min5`, `min15`, `min30`, `min60`
- Token 加载：`source <(grep AMAZINGDATA ~/.hermes/.env 2>/dev/null)`

### AmazingData 诊断流程
当怀疑 amazingdata 不可用时，按此链路排查：
1. `curl -sL -w "%{http_code}" https://www.ai10088.com/amazingdata` → **301** 正常（Nginx 重定向）
2. `curl -sL https://www.ai10088.com/amazingdata/ -H "Authorization: Bearer $TOKEN"` → **401** 服务在线，鉴权正常
3. `curl -sL "https://www.ai10088.com/amazingdata/api/v1/trading/daily-bars?code=000001&period=day&lookback_days=3" -H "Authorization: Bearer $TOKEN"` → **200** 完全可用，返回数据

**状态码含义**：
- **301**：Nginx 正常，服务存在
- **401**：服务进程正常，但 Windows 上游可能离线（中继只能回应鉴权，数据请求会超时）
- **500**：服务崩溃或上游连接失败
- **200+空items**：服务正常，数据区间无交易日（如假期）
- **超时**：Windows 客户端离线，中继卡死在上游连接

## 核心逻辑
在 2GB 内存限制下，利用 `amazingdata` 和 `cronjob` 实现轻量级、分钟级的 A 股机会扫描。

### 1. 盘前股池准备 (`prepare_pool.py`)
*   **运行时间**：交易日 08:00 AM
*   **目标**：从全市场筛选 80-120 只主板高辨识度股票。
*   **筛选标准**：
    *   **板块过滤**：剔除科创(688)、创业(300/301)、北交(8/4)、ST。
    *   **活跃度**：取成交额前 2000 名。
    *   **换手率**：2% - 20%（确保有人气但非极端投机）。
    *   **市值**：> 20亿（剔除微盘股风险）。
*   **指标计算**：为每只票预计算 MA5, MA20, 近5日高低点，存入 `~/.hermes/stock_monitor/pool_YYYYMMDD.json`。

### 2. 盘中信号监控 (`check_signals.py`)
*   **运行频率**：交易日 09:30-15:00，每 30 分钟一次（可使用本次探明的 amazingdata 轮询）。
*   **信号定义**：
    *   **📉 低吸信号**：跌幅 -3% ~ -6% + 现价在 MA20 ±3% 附近。逻辑：强势股情绪错杀或良性回踩。
    *   **🚀 龙头信号**：涨幅 > 8% + 量比 > 1.5。逻辑：资金合力抢筹，主升浪确认。
*   **防骚扰**：使用 `signals_log.json` 记录当日已推送代码，避免重复提醒。

## 部署步骤

### 1. 安装依赖
```bash
# 主要数据源
source /root/info-hub/backend/.venv/bin/activate
pip install baostock pandas pyarrow httpx

# 兜底（可选，连接不稳定）
pip install --break-system-packages akshare
```

### 2. 创建脚本
将 `scripts/stock_monitor/prepare_pool.py` 和 `check_signals.py` 放入项目目录。

### 3. 配置 Cron Job
使用 `cronjob` 工具创建两个任务：
*   **盘前准备**：`schedule="0 8 * * 1-5"`, `deliver="feishu"`
*   **盘中监控**：`schedule="*/30 9-14 * * 1-5"`, `deliver="feishu"` (注意设置 timeout=120s)

## 盘中实时 1 分钟数据轮询

### 技术验证
AmazingData 中继支持 `period=min1` 的 K 线查询：
```bash
TOKEN="${AMAZINGDATA_PUBLIC_RELAY_TOKEN}"
curl -sL "https://www.ai10088.com/amazingdata/api/v1/trading/kline?code=000001&period=min1&begin_date=20260505&end_date=20260505" -H "Authorization: Bearer $TOKEN"
```

返回格式（已验证 200 OK）：
```json
{
  "data": {
    "code": "000001",
    "period": "min1",
    "items": [
      {"trade_date": "...", "open": ..., "high": ..., "low": ..., "close": ..., "volume": ...}
    ]
  }
}
```

### 实时轮询脚本实现思路
```python
import httpx, os, time, sqlite3
from datetime import datetime

TOKEN = os.environ["AMAZINGDATA_PUBLIC_RELAY_TOKEN"]
BASE = "https://www.ai10088.com/amazingdata"
CODES = ["000001", "000002", "..."]  # 股票池 50-100 只
INTERVAL = 60  # 1 分钟

while True:
    now = datetime.now()
    if 9 <= now.hour < 15:  # 盘中
        for code in CODES:
            r = httpx.get(f"{BASE}/api/v1/trading/kline", 
                params={"code": code, "period": "min1", ...},
                headers={"Authorization": f"Bearer {TOKEN}"})
            # 落盘 SQLite / Parquet
        time.sleep(INTERVAL)
    else:
        time.sleep(60)  # 盘外低频心跳
```

适合配合 `background=true` 的终端进程运行，或在 cron 中每 1-5 分钟调用一次脚本。

## 避坑指南
1.  **AKShare 版本问题**：阿里云镜像可能因 `exclude-newer` 策略导致安装失败，建议使用 `pip install --break-system-packages akshare` 绕过 uv 限制。
2.  **超时控制**：盘中扫描 120 只股票的历史数据较慢，务必在 cron 命令中加 `timeout 120`，防止进程堆积。
3.  **内存限制**：不要一次性拉取全市场 5000+ 只股票的日线历史，先缩小范围再补指标。
4.  **AmazingData 超时**：如果请求超时（30s+ 无响应），Windows 客户端大概率离线。先诊断（见上），不要重试。
5.  **Baostock 增量 dump**：在 `info-hub/backend/services/stock_engine/dump_service.py`，每天 02:00 自动增量更新。手动补全历史：`start_date="2018-01-01"`（约 40 分钟跑完 4900+ 只）。
6.  **假期数据**：节假日请求 amazingdata 会返回 `count=0, items=[]`，这不是故障。

## 扩展建议
*   若需更精细的"打板"监控，可缩短扫描间隔至 5 分钟，并增加"封单额"判断。
*   若需"板块联动"分析，可在 `prepare_pool` 阶段增加行业标签，监控时优先推送板块内首个启动的票。