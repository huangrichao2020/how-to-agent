---
name: a-stock-daily-report-generator
category: data-science
description: "Generate A-share daily signal reports using Info-Hub parquet data. Focuses on market structure, supply/demand, and leader anchoring."
version: "1.1"
created: "2026-05-06"
---

# A-Share Daily Report Generator

Generate structured daily market reports based on the "Human Nature/Obsession/Structure/Supply-Demand" framework.

## 触发条件 (Trigger Conditions)
- **触发**: User requests a daily report (e.g., "generate yesterday's report", "生成日报")
- **触发**: User asks for market analysis with specific stock/sector data
- **触发**: Post-market review tasks (盘后复盘)
- **适用**: A-share market data analysis, sector rotation tracking

## Core Workflow

### 步骤 1: Data Extraction (Info-Hub)
Use `execute_code` to read parquet files from `/root/info-hub/backend/data/historical/`.

**Key Metrics to Extract:**
- **Top Gainers:** Sort by `pct_chg` (calculate if missing: `(close - prev_close) / prev_close * 100`)
- **Top Volume/Amount:** Sort by `amount` to identify institutional focus (Capacity Leaders)
- **Market Breadth:** Count stocks with `pct_chg > 0` vs `< 0`

**Code Template (with proper 异常 handling):**
```python
import pandas as pd
import glob, os
import logging

logging.basicConfig(level=logging.INFO)
path = '/root/info-hub/backend/data/historical'

# 异常处理: 检查数据目录是否存在
if not os.path.exists(path):
    raise FileNotFoundError(f"数据目录不存在: {path}")

files = glob.glob(os.path.join(path, '*.parquet'))
if not files:
    raise FileNotFoundError(f"目录中没有 parquet 文件: {path}")

target_date = pd.Timestamp('YYYY-MM-DD')

results = []
error_count = 0
for f in files:
    try:
        code = os.path.basename(f).replace('.parquet', '')
        df = pd.read_parquet(f, columns=['date', 'close', 'amount'])
        # Calculate change
        df['pct_chg'] = df['close'].pct_change() * 100
        
        mask = df['date'] == target_date
        if mask.any():
            row = df[mask].iloc[0]
            results.append({'code': code, 'pct_chg': row['pct_chg'], 'amount': row['amount']})
    except pd.errors.EmptyDataError:
        logging.warning(f"跳过空文件: {f}")
        error_count += 1
    except KeyError as e:
        logging.warning(f"跳过缺少列的文件 {f}: {e}")
        error_count += 1
    except Exception as e:
        logging.warning(f"读取失败 {f}: {e}")
        error_count += 1

df_res = pd.DataFrame(results)

# 异常处理: 检查结果是否为空
if df_res.empty:
    print(f"警告: 未找到 {target_date} 的数据，可能是非交易日")
    print("fallback: 尝试查询前一个交易日的数据")
else:
    print(f"成功读取 {len(df_res)} 只股票，{error_count} 个文件读取失败")
    print("Top Gainers:", df_res.nlargest(10, 'pct_chg'))
    print("Top Amount:", df_res.nlargest(10, 'amount'))
```

### 步骤 2: Analysis Framework (L4 Structure)

**A. Market State Qualitative:**
- **Main Line:** High consecutive boards, sector resonance.
- **Oscillation:** Rapid rotation, high-low switch.
- **Ebb Tide:** Leader broken, money-losing effect.

**B. Sector Supply/Demand:**
- **Supply < Demand:** Capital inflow + Sector resonance → Participate.
- **Supply > Demand:** Capital dispersion + Rapid rotation → Avoid.

**C. Leader Anchoring:**
- **Space Leader:** Highest consecutive boards.
- **Trend Leader:** Rising along MA5/MA10.
- **Capacity Leader:** Highest turnover (Institutional focus).

### 步骤 3: Report Structure

```markdown
# 🐉 Hermes Signal Report | YYYY-MM-DD

## 1. Market State
[Qualitative Judgment]

## 2. Sector Supply/Demand
| Sector | Flow | Status | Sustainability |
|--------|------|--------|----------------|

## 3. Leader Anchoring
- **Capacity Leaders:** [Stocks with highest amount]
- **Trend Leaders:** [Stocks breaking out]

## 4. Strategy
- **Attack:** If [Condition], then [Action]
- **Defend:** If [Condition], then [Action]
```

## 注意 / Pitfalls

1. **注意 — Parquet Schema:** Some files may lack `pct_chg`. Always calculate it from `close` if missing.
2. **注意 — Date Format:** Ensure `pd.Timestamp` matches the parquet date type (usually `datetime64`).
3. **注意 — Performance:** Reading 4000+ files is slow. Optimize by reading only necessary columns (`date`, `close`, `amount`).
4. **注意 — Holiday Check:** Verify the target date is a trading day. If no data is found, check the previous trading day.
5. **注意 — Timeout:** If reading takes >30 seconds, consider pre-filtering files by date pattern or using a cached summary.
6. **坑 — Empty Results:** If df_res is empty after processing all files, the target date is likely a non-trading day. Use fallback to previous trading day.
7. **坑 — 异常 Silently Swallowed:** Never use bare `except: pass` — always log the error for debugging.

## 异常处理 / Fallback Strategy

| 失败场景 | 兜底方案 |
|---------|---------|
| 数据目录不存在 | 提示用户检查 Info-Hub 是否正常运行 |
| 目标日期无数据 | fallback 到前一个交易日 |
| parquet 文件损坏 | 跳过该文件，继续处理其他文件 |
| 读取超时 (>30s) | 使用预缓存的汇总数据 |
| 结果为空 | 检查是否为节假日/周末 |

## Evolution Notes
- **2026-05-06:** Integrated with Info-Hub parquet data. Replaced generic placeholders with real data extraction logic.
- **2026-05-10:** Added comprehensive 异常 handling, fallback strategy, replaced bare `except: pass` with proper error logging.