---
name: deploy-tradingagents
description: Deploy the TradingAgents multi-agent LLM trading framework locally or on server. Covers dependency installation, API key configuration (DashScope/CodingPlan), provider compatibility fixes, and running analysis on A-shares/US stocks.
version: 1.2.0
trigger: 用户需要部署 TradingAgents 框架；关键词：TradingAgents、部署、trading agents、multi-agent trading
---

# Deploy TradingAgents

TradingAgents is a multi-agent LLM financial trading framework by TauricResearch. It uses LangGraph to orchestrate multiple analyst agents (Market, Sentiment, Fundamentals, Technicals, Risk) that debate and produce trading decisions.

**Repo**: https://github.com/TauricResearch/TradingAgents

## Pre-flight Checks

Before deploying, verify:
```bash
# 1. Network connectivity to API endpoint
curl -s -o /dev/null -w "%{http_code}" https://your-endpoint/v1/chat/completions
# Expected: 200 or 401 (auth needed). If 000 or 5xx → network/DNS issue

# 2. Python version (3.10+ required)
python3 --version

# 3. Disk space (venv + deps ~2-3GB)
df -h /root

# 4. Memory (4GB+ recommended for langchain)
free -h
```

## Quick Deploy Steps

### 1. Clone and Setup

```bash
cd /root
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents

# Create venv with uv
uv venv
source .venv/bin/activate
```

**⚠️ Pitfall**: If `uv` not installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 2. Install Dependencies

**⚠️ Pitfall**: In Chinese cloud environments, default PyPI may timeout. Use Aliyun mirror:

```bash
# Core dependencies
uv pip install -i https://mirrors.aliyun.com/pypi/simple/ \
  langchain langchain-openai langchain-community \
  yfinance pandas backtrader stockstats rank-bm25

# Optional (install only if needed by your provider)
uv pip install -i https://mirrors.aliyun.com/pypi/simple/ langchain-anthropic
# langchain-google-genai often times out in China — install later if needed
```

**⚠️ Pitfall**: If dependency conflict occurs (e.g., langchain version mismatch):
```bash
# Pin known-working versions
uv pip install -i https://mirrors.aliyun.com/pypi/simple/ \
  langchain==0.2.16 langchain-openai==0.1.23 langchain-community==0.2.16
```

### 3. Fix Startup Import Errors

The repo imports all LLM clients at startup, causing `ModuleNotFoundError` if optional packages aren't installed.

**Required patch** in `tradingagents/llm_clients/factory.py`:
```python
# Change from direct imports to try/except
try:
    from .anthropic_client import AnthropicClient
except ImportError:
    AnthropicClient = None
try:
    from .google_client import GoogleClient
except ImportError:
    GoogleClient = None
try:
    from .azure_client import AzureOpenAIClient
except ImportError:
    AzureOpenAIClient = None
```

Also add `"custom"` to `_OPENAI_COMPATIBLE` tuple to allow custom base URLs.

### 4. Configure API Key

Create `.env`:
```bash
OPENAI_API_KEY=***
OPENAI_API_BASE=https://your-endpoint/v1
```

**API Key Compatibility**:

| Key Type | Endpoint | Supported Models |
|----------|----------|-----------------|
| DashScope standard | `https://dashscope.aliyuncs.com/compatible-mode/v1` | qwen-plus, qwen-max, qwen-turbo |
| CodingPlan (`sk-sp-*`) | `https://coding.dashscope.aliyuncs.com/v1` | qwen-coder-plus only |
| OpenAI | `https://api.openai.com/v1` | gpt-4o, gpt-5, etc. |

**⚠️ Pitfall**: CodingPlan keys do NOT support `qwen-plus`. Use `qwen-coder-plus` or get a standard DashScope key.

### 5. Configure main.py

The default config uses `gpt-5.4-mini` which won't work. Key config changes:

```python
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "qwen-coder-plus"  # or qwen-plus
config["quick_think_llm"] = "qwen-coder-plus"
config["max_debate_rounds"] = 1  # save tokens
config["llm_provider"] = "custom"  # bypass hardcoded provider URLs
config["backend_url"] = "https://coding.dashscope.aliyuncs.com/v1"  # your endpoint
```

**⚠️ Pitfall**: The `openai` provider in the code forces `use_responses_api=True`, which is OpenAI-specific and returns 404 on third-party endpoints. Two fixes needed:

1. Set `llm_provider = "custom"` (not "openai") to route through the compatible path
2. Add `"custom"` to `_OPENAI_COMPATIBLE` in `factory.py`

Alternatively, in `openai_client.py`, add a check:
```python
if self.provider == "openai" and "use_responses_api" not in llm_kwargs:
    llm_kwargs["use_responses_api"] = True
```
Then pass `use_responses_api=False` in config.

### 6. Run

```bash
source .venv/bin/activate
python main.py
```

Expected output: Agent messages streaming, followed by a final `decision` dict with recommendation.

### 7. Run for A-Shares

The default `yfinance` data source supports A-shares. Change the ticker:
```python
_, decision = ta.propagate("600519.SS", "2024-05-10")  # Kweichow Moutai
```

## Architecture Overview

```
TradingAgentsGraph
├── Market Analyst Agent (trend, breadth)
├── Sentiment Analyst Agent (news sentiment)
├── Fundamentals Analyst Agent (financials)
├── Technical Analyst Agent (indicators)
├── Debate Round (agents argue Bull/Bear)
├── Risk Manager (position sizing, stop loss)
└── Trading Agent (final decision)
```

## Cost Estimation

- Per stock analysis: ~10-20 LLM calls (multiple agents + debate)
- With qwen-plus (~0.02元/1K tokens): ~2-5元 per run
- Daily 2 runs × 20 stocks: ~100-200元/month
- Optimize with `max_debate_rounds=1` and cheaper models for quick thinking

## Exception Handling & Troubleshooting

### Startup Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: langchain_anthropic` | Optional import not installed | Apply try/except patch in factory.py (Step 3) or `uv pip install langchain-anthropic` |
| `ModuleNotFoundError: No module named 'tradingagents'` | Not in venv or wrong cwd | `source .venv/bin/activate` then `cd /root/TradingAgents` |
| `SyntaxError` in factory.py | Python version < 3.10 | Upgrade Python or pin langchain to older version |

### API / Network Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `ConnectionError: Network unreachable` | Wrong endpoint or DNS issue | Verify with `curl -v https://your-endpoint/v1` — check firewall/proxy |
| `Connection timed out` | Chinese network to foreign API | Use Aliyun/Tencent mirror for pip; for API, ensure DashScope endpoint (not OpenAI direct) |
| `model not supported` | Key type mismatch | CodingPlan (`sk-sp-*`) only works with `qwen-coder-plus`; DashScope standard supports `qwen-plus` |
| `Error code: 404` on `/v1/responses` | Responses API not available | Set `llm_provider = "custom"` not `"openai"` in config |
| `Rate limit exceeded` (429) | Too many requests/min | Add `time.sleep(2)` between API calls; reduce `max_debate_rounds` |
| `Invalid API key` (401) | Key expired or wrong env var | Check `.env` file; test with `curl -H "Authorization: Bearer $OPENAI_API_KEY" $OPENAI_API_BASE/models` |

### Data Fetch Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `yfinance download failed` | Network to Yahoo Finance blocked | Use proxy or switch to AKShare (`pip install akshare`) for A-share data |
| `No data found for ticker` | Wrong ticker format | A-shares: `600519.SS` (Shanghai), `000001.SZ` (Shenzhen); US: `AAPL` |
| `backtrader data feed error` | Date range has no data | Ensure date is within available history; yfinance ~2 years of daily data |

### Runtime Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `RecursionError: maximum recursion depth exceeded` | LangGraph loop bug | Set `config["max_debate_rounds"] = 1` to avoid deep recursion |
| `OOM Killed` | Insufficient memory | Reduce concurrent agents; use smaller models; add swap: `fallocate -l 2G /swap && mkswap /swap && swapon /swap` |
| Agent returns empty decision | LLM response parsing failed | Check `deep_think_llm` model supports function calling; switch to `qwen-max` for better instruction following |

### Post-deployment Verification

```bash
# Quick smoke test — should return model list without error
source .venv/bin/activate
python -c "
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model='qwen-coder-plus', temperature=0)
resp = llm.invoke('Reply: OK')
print(resp.content)
"
```

## Common Errors Quick Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: langchain_anthropic` | Optional import not installed | Apply try/except patch in factory.py or install package |
| `ConnectionError: Network unreachable` | Wrong API endpoint or DNS issue | Verify endpoint with curl first |
| `model not supported` | Key type mismatch | CodingPlan keys only work with coder models |
| `Error code: 404` on `/v1/responses` | Responses API not available | Set provider to "custom" not "openai" |
| `yfinance download failed` | Network issue | yfinance needs external access, may need proxy |
