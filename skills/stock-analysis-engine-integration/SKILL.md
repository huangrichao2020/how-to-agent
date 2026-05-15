---
name: stock-analysis-engine-integration
description: Methodology for integrating a multi-engine A-share analysis tool into Hermes Agent. Covers causality validation, phase detection, supply/demand calculation, and Wiki knowledge synthesis.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [stock, trading, engine, integration]
    category: trading
---

# Stock Analysis Engine Integration

This skill documents the architecture and implementation of the `stock_analyzer` tool, designed to embody the "Trading Constitution" (Causality > Correlation) in code.

## Core Architecture: Four-Engine Model

The analyzer is not a simple data fetcher; it is a logic processor composed of four distinct engines:

| Engine | Function | Trading Constitution Mapping | Data Source |
| :--- | :--- | :--- | :--- |
| **1. Causality** | Identifies the "Why" (Concepts, News) | Causality > Correlation | Baidu/THS APIs |
| **2. Phase** | Identifies the "When" (Trend, Sentiment) | Market State / Leader Anchor | Limit-up Ladder / MAs |
| **3. Supply/Demand** | Identifies the "How much" (Volume, Support) | Supply/Demand Inflection Point | K-line Parquet / Tencent |
| **4. Wiki Knowledge** | Synthesizes historical context | Experience Accumulation | Local Wiki Entities |

## Implementation Steps

### 1. Tool Registration
Create `tools/stock_analyzer.py`. It must use `registry.register` to become a native Hermes tool.
- **Handler**: Orchestrates the four engines.
- **Schema**: Requires `code` (e.g., '002208') and optional `name`.

### 2. Wiki Knowledge Engine
- **Path**: `~/wiki/entities/`.
- **Logic**: Search for files matching `{code}-{name}.md`. Extract frontmatter and body summary.
- **Purpose**: Prevents repeating past mistakes (e.g., remembering that "Hefei Urban Construction" is actually a storage chip play, not real estate).

### 3. Causality & Phase Engines
- **Causality**: Use heuristic keywords (e.g., "涨价", "重组") or API calls to score the strength of the driver.
- **Phase**: Compare Price vs MA5/MA20 to determine if the stock is in Acceleration, Consolidation, or Decline.

### 4. Handling 2GB Memory Constraints
- **Avoid**: Heavy dependencies like `langchain` or `pandas` for simple tasks.
- **Use**: Direct `requests` for APIs and `pyarrow` (already installed) for reading local Parquet K-line data from `info-hub`.

## Troubleshooting

- **Parquet Error**: If `pyarrow` is missing, install via `uv pip install pyarrow`.
- **API Timeout**: Baidu/THS APIs may timeout on Alibaba Cloud. Implement `timeout=5` and fallback logic.
- **Orphan Pages**: After generating entity files, run `wiki_lint` or update `overview.md` to ensure new entities are linked.

## Usage Example

```python
from tools.stock_analyzer import StockAnalyzer
analyzer = StockAnalyzer()
res = analyzer.analyze('002208', '合肥城建')
print(res['final_conclusion'])
```

**Output:** "Strong Causality + Uptrend. Watch for breakout. (Wiki notes: Indirectly holds Changxin Tech...)"