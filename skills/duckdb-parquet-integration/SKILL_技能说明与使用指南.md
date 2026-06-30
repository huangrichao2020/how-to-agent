---
name: duckdb-parquet-integration
version: 1.0.0
description: Integrate DuckDB as a high-performance query layer over existing Parquet files in info-hub. Achieves ~19x speedup for full-market scans without data migration.
metadata:
  requires:
    bins: ["uv"]
    python_packages: ["duckdb", "pandas", "pyarrow"]
---

# DuckDB + Parquet Integration Skill

## When to use
- You need to accelerate full-market scanning or aggregation queries on large Parquet datasets.
- You want to avoid migrating existing Parquet storage to a new database format.
- You are working in a constrained environment (e.g., 2GB RAM) where pandas loops are too slow or memory-intensive.

## Core Insight
DuckDB can directly query Parquet files using SQL (`read_parquet('path/*.parquet')`). It leverages columnar storage and vectorized execution, outperforming pandas loops by **10-20x** for scan/aggregation tasks while maintaining low memory usage.

## Step-by-step Integration

### 1. Install Dependencies
```bash
uv pip install duckdb pandas pyarrow
```

### 2. Verify Data Structure
Ensure your Parquet files have consistent schemas. DuckDB infers schema from the first file it reads.
```python
import duckdb
# Check schema of a sample file
print(duckdb.query("DESCRIBE SELECT * FROM read_parquet('sample.parquet')").fetchall())
```

### 3. Implement Query Wrapper
Create a helper function in your project (e.g., `info-hub/backend/utils/duckdb_helper.py`):

```python
import duckdb
import pandas as pd
import os

DATA_DIR = "/root/info-hub/backend/data/historical"

def duckdb_query(sql: str) -> pd.DataFrame:
    """
    Execute SQL query against Parquet files in DATA_DIR.
    Use {data_dir} placeholder in SQL for portability.
    """
    final_sql = sql.replace("{data_dir}", DATA_DIR)
    try:
        return duckdb.query(final_sql).df()
    except Exception as e:
        print(f"DuckDB Error: {e}")
        return pd.DataFrame()

# Example: Full market scan for bullish candles
def get_bullish_stocks(date_from: str = "2025-01-01") -> pd.DataFrame:
    return duckdb_query(f"""
        SELECT 
            filename(code) as code, 
            date, 
            close, 
            open 
        FROM read_parquet('{DATA_DIR}/*.parquet')
        WHERE close > open 
        AND date >= '{date_from}'
    """)
```

### 4. Performance Tuning Tips
- **Glob Patterns**: Use `*.parquet` for all files or `sh_*.parquet` for subsets.
- **Column Pruning**: Only `SELECT` columns you need. DuckDB skips reading unused columns.
- **Filter Pushdown**: Put `WHERE` clauses inside the SQL to let DuckDB filter during read.
- **Aggregations**: Use `GROUP BY` in SQL instead of pandas `groupby()` for massive speedups.

## Pitfalls
- **Schema Mismatch**: If some Parquet files have different columns, DuckDB may fail. Ensure uniform schema across the directory.
- **Memory Spikes**: While efficient, loading huge result sets into pandas (`df()`) can still spike memory. Use `fetchone()` or `fetchmany()` for streaming if needed.
- **Path Issues**: Use absolute paths in `read_parquet()` to avoid working-directory confusion.

## Benchmark Reference (Alibaba Cloud 2GB RAM)
- **Dataset**: 4786 Parquet files (~77MB total)
- **Full Market Scan**: Pandas ~9.3s vs DuckDB ~0.49s (**19x faster**)
- **Aggregation (200 files)**: Pandas ~707ms vs DuckDB ~54ms (**13x faster**)

## Related Skills
- `a-stock-market-data-backfill_A股回测数据补全`: For updating the underlying Parquet data.
- `info-hub-stock-integration`: For integrating this query layer into the FastAPI backend.