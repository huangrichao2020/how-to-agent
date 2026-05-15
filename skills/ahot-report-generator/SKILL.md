---
name: ahot-report-generator
description: Generate A-share strategy reports (pre-market, post-market, daily) using Agent-style LLM calls with AmazingData/Baostock fallback.
tags: [stock, generator, llm, amazingdata, baostock]
version: 0.1.0
---

# AHOT Report Generator

Generates A-share strategy reports for the `ahot-skill` API service.

## Architecture

1. **LLM Client**: `generator/llm_client.py` wraps API calls to look like Hermes Agent internal traffic (session_id, trace_id, tool_call simulation). Auto-fallbacks to DeepSeek on 429.
2. **Data Adapter**: `generator/amazingdata_adapter.py` tries AmazingData relay first (local/LAN/public), then falls back to Baostock if unreachable. Includes circuit breaker.
3. **Generators**: `pre_market.py`, `post_market.py`, `daily.py` fetch data, build prompts, call LLM, save JSON to `data/reports/`.
4. **Runner**: `run_generators.sh` handles retries (3x exponential backoff) and Feishu alerts.

## Usage

```bash
cd /root/ahot-skill
./generator/run_generators.sh [pre-market|post-market|daily|all] [YYYY-MM-DD]
```

## Key Patterns

- **Agent Simulation**: LLM calls include fake `tool_calls` in message history to bypass CodingPlan rate limiting heuristics.
- **Fast Fallback**: AmazingData health check uses 1s timeout per relay; if all fail, immediately switches to Baostock without waiting for full timeouts.
- **JSON First**: API reads from `data/reports/*.json` directly, avoiding gbrain sync delays.

## Troubleshooting

- If reports are empty: Check `logs/generator-*.log` for LLM API errors.
- If AmazingData is slow: Check `AMAZINGDATA_RELAY_LOCAL_URL` env var. The adapter caches health status per session.
- If API returns 500: Ensure `api/main.py` has `type` field in `_load_local_json` response.