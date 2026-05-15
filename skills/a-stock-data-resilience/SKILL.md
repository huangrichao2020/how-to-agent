---
name: a-stock-data-resilience
description: A股数据源高可用策略 — 多时间点重试 + 双数据源降级 + Key轮转。确保在阿里云网络波动或API配额耗尽时仍能获取行情和生成股池。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [a-stock, data-source, resilience, fallback]
    related_skills: [stock-monitoring-automation, tencent-market-data-adapter]
---

# A股数据源高可用策略（2026-05-14 升级）

## 核心原则
- **三级数据源架构**：同花顺热点（主）→ 东财全市场（降）→ 腾讯行情（备）
- **多时间点重试**：08:20, 08:40, 09:00 三次尝试，避开网络波动高峰
- **兜底机制**：所有数据源失败时，复制最近交易日股池文件

## 根因分析（2026-05-14 排查结果）

| 数据源 | 实际状态 | 根因 |
|--------|---------|------|
| **东财** | ❌ 不通 | `ak.stock_zh_a_spot_em()` 返回 `RemoteDisconnected` — 东财对批量拉取全市场行情的接口做了反爬限制 |
| **腾讯** | ✅ 可用但被禁用 | 脚本里 `fetch_tencent_market_data()` 被硬编码为直接返回空 DataFrame，根本没调用 |
| **同花顺** | ✅ 可用但被禁用 | 脚本里 `fetch_iwencai_market_data()` 被硬编码为直接返回空 DataFrame，根本没调用 |

**核心问题**：降级逻辑失效。腾讯和同花顺函数体被改成了直接返回空，导致东财失败后直接进入兜底。

## 修复方案

### 1. 新增同花顺热点接口作为主数据源
```python
def fetch_ths_hot_stocks(date: str = None) -> pd.DataFrame:
    """同花顺热点接口 — 当日强势股 + 题材归因"""
    from datetime import date as _date
    if date is None:
        date = _date.today().strftime("%Y-%m-%d")
    
    url = f"http://zx.10jqka.com.cn/event/api/getharden/date/{date}/orderby/date/orderway/desc/charset/GBK/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.0.0 Safari/537.36"}
    
    def _do_fetch():
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        if data.get("errocode", 0) != 0:
            raise RuntimeError(f"同花顺热点错误: {data.get('errormsg', '')}")
        return data.get("data", [])
    
    rows = retry_with_backoff(_do_fetch, max_retries=2, base_delay=1)
    # ... 数据处理逻辑
```

**优势**：零鉴权，~73ms 响应，返回约146只强势股，天然过滤了非活跃股。

### 2. 调整数据源优先级
```python
# 旧逻辑：东财 → 腾讯 → 同花顺
# 新逻辑：同花顺热点 → 东财全市场 → 腾讯行情

df_all = None

# 1. 优先使用同花顺热点接口（当日强势股）
print("获取当日强势股（同花顺热点数据源）...")
try:
    df_all = fetch_ths_hot_stocks()
    if len(df_all) > 0:
        print(f"  同花顺热点获取成功: {len(df_all)} 只")
    else:
        df_all = None
except Exception as e:
    print(f"  同花顺热点获取失败: {e}")
    df_all = None

# 2. 降级到东财全市场数据
if df_all is None or len(df_all) == 0:
    print("尝试获取全市场实时行情（东财数据源）...")
    try:
        df_all = retry_with_backoff(ak.stock_zh_a_spot_em)
        print(f"  东财数据获取成功: {len(df_all)} 只")
    except Exception as e:
        print(f"  东财数据获取失败: {e}")
        
        # 3. 最后降级到腾讯
        print("尝试降级到腾讯行情接口...")
        try:
            df_all = fetch_tencent_market_data()
            # ...
```

### 3. 验证结果
- ✅ 同花顺热点：146只强势股，73ms响应
- ✅ 腾讯行情：HTTP 200，数据正常返回
- ❌ 东财全市场：连接被远端关闭

**结论**：同花顺热点接口稳定性最高，应作为盘前股池的主数据源。

## 核心问题
阿里云服务器（国内）访问金融API常遇：
1. **网络超时**：东财/雪球接口偶尔 `RemoteDisconnected`
2. **配额耗尽**：MX API/问财免费版每日限额低
3. **单次失败即瘫痪**：盘中监控依赖盘前股池，股池生成失败则全天无数据

## 解决方案架构

### 1. 多时间点自动重试 (Cron Layer)
不要只跑一次 `08:00`，改为三次机会：
- `08:20` - 第一次尝试
- `08:40` - 第二次尝试（若文件已存在则跳过）
- `09:00` - 第三次尝试（开盘前最后机会）

**实现要点**：
- 脚本启动时检查 `pool_YYYYMMDD.json` 是否存在，存在则直接退出（幂等性）
- 每个 Cron Job 独立运行，互不干扰

### 2. 数据源降级链 (Fallback Chain)
按稳定性从高到低排列：
1. **首选**：东财 Akshare (`ak.stock_zh_a_spot_em`) — 数据最全，但易被封。
2. **备选**：同花顺 iwencai OpenAPI — 需配置 `IWENCAI_API_KEY`，走专用通道。
3. **兜底**：加载最近交易日股池 — 当所有网络不可用时，复制 `pool_YYYYMMDD.json` 为今日文件，保证监控流程不中断。

**实现要点**：
- 在 `prepare_pool.py` 中增加 `.env` 自动加载逻辑。
- 实现 `fetch_iwencai_market_data()` 并处理 SSL 验证（`verify=False`）。
- 在主流程中加入 `try-except` 降级逻辑，确保即使网络全断也能产出文件。

### 3. API Key 轮转 (Tool Layer)
针对有配额的 API（如 MX API、问财）：
- 维护 `key_usage.json` 记录每个 Key 的当日调用次数
- 达到阈值（如 20 次）自动切换到下一个 Key
- 3 个 Key 轮流用，将可用窗口扩大 3 倍

## 关键脚本路径
- 股池生成：`/root/hermes-agent/scripts/stock_monitor/prepare_pool.py`
- Key 轮转：`/root/hermes-agent/tools/eastmoney_key_rotator.py`
- 涨停追踪：`/root/hermes-agent/scripts/ztb_tracker.py`

## 避坑指南
1. **不要硬编码单一 Key**：一旦封禁或耗尽，整个系统停摆
2. **不要忽略“文件已存在”检查**：否则多次重试会重复拉取历史指标，浪费时间和配额
3. **腾讯接口解析**：腾讯返回的是 `v_sh600000="..."` 格式，需用正则提取，不要直接用 `pd.read_csv`
4. **AmazingData 慎用**：银河证券 SDK 依赖 Windows 环境且网络极不稳定，仅作为离线备份，不要作为实时数据源

## 验证方法
- 手动删除今日股池文件：`rm ~/.hermes/stock_monitor/pool_*.json`
- 运行 `python scripts/stock_monitor/prepare_pool.py`
- 观察日志是否出现 `[降级]` 字样或 Key 切换提示