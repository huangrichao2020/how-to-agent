---
name: info-hub-ai-assistant-config
description: Configure the Info-Hub AI Assistant (Review Master) to use a specific LLM provider. Currently configured for DeepSeek API.
category: devops
yao_category: "其他"
---

# Info-Hub AI Assistant Configuration

## Overview
The Info-Hub project includes an "AI Assistant" (复盘大师) in the frontend that uses a backend LLM client for chat and ReAct agent capabilities. This skill documents how to switch or configure the underlying LLM provider.

## Trigger Conditions
- User asks to switch or configure the LLM provider for Info-Hub AI Assistant
- User asks to change the model, API key, or base URL
- User encounters 500 errors or timeouts from the AI chat feature
- User asks about ReAct agent configuration

## Current Configuration
- **Provider**: DeepSeek
- **Model**: `deepseek-v4-pro`
- **Base URL**: `https://api.deepseek.com`
- **API Key**: Configured in `backend/llm/deepseek_client.py`

## File Locations
1. **LLM Client**: `backend/llm/deepseek_client.py`
   - Implements `chat_stream`, `chat`, and `chat_stream_with_tools`.
2. **Assistant Router**: `backend/routers/assistant.py`
   - Imports `chat_stream` from the client.
3. **ReAct Agent**: `backend/services/react_agent.py`
   - Imports `chat_stream_with_tools` for tool-calling capabilities.

## How to Switch Providers

1. **Create a new client file** (e.g., `backend/llm/new_provider_client.py`) implementing:
   - `async def chat_stream(messages, ...) -> AsyncGenerator[str, None]`
   - `async def chat_stream_with_tools(messages, tools, ...) -> dict` (with `content` and `tool_calls`)

2. **Update Imports**:
   - In `backend/routers/assistant.py`:
     ```python
     from llm.new_provider_client import chat_stream
     ```
   - In `backend/services/react_agent.py`:
     ```python
     from llm.new_provider_client import chat_stream_with_tools
     ```

3. **Configure API Keys**: Load from environment variables — never hardcode.
   ```python
   import os
   API_KEY = os.environ.get("NEW_PROVIDER_API_KEY", "")
   if not API_KEY:
       raise ValueError("NEW_PROVIDER_API_KEY not set in environment")
   ```

## Error Handling & Troubleshooting

### Common Failure Modes

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | API key missing or expired | Check env var, regenerate key |
| `403 Forbidden` (Frontend) | Vite subpath misconfigured | Ensure `vite.config.ts` has `base: '/info-hub/'` |
| `429 Rate Limited` | Provider rate limit exceeded | Add retry with exponential backoff (see below) |
| `500 Internal Error` | Backend crashed or provider down | Check logs: `journalctl -u info-hub-backend` |
| `Timeout` (>30s) | Provider slow or network issue | See timeout fallback below |
| `Tool Calling Failed` | Provider doesn't support function calling | Verify OpenAI-compatible format support |

### Timeout Fallback Strategy
```python
import asyncio
import httpx

TIMEOUT = httpx.Timeout(connect=10.0, read=30.0)
MAX_RETRIES = 3

async def chat_with_retry(messages, timeout=TIMEOUT, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                # ... make request ...
                return response
        except httpx.TimeoutException:
            if attempt == max_retries - 1:
                raise  # Final attempt failed
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                await asyncio.sleep(2 ** attempt)
                continue
            raise
```

### Memory Constraints
The server has only **2GB RAM**. Avoid heavy dependencies like `langchain`. Use direct `httpx` calls as implemented in `deepseek_client.py`.

### Provider Compatibility Checklist
Before switching, verify the new provider supports:
- [ ] OpenAI-compatible chat completions API (`/v1/chat/completions`)
- [ ] Streaming responses (`stream: true`)
- [ ] Function/tool calling (for ReAct agent)
- [ ] At least 8K context window

If any feature is missing, the AI Assistant will partially break — streaming chat works but ReAct agent fails.

## Quick Reference: Switch in 3 Steps
```bash
# 1. Create new client
cp backend/llm/deepseek_client.py backend/llm/qwen_client.py
# 2. Edit: update base_url, auth headers, response parsing
# 3. Update imports in assistant.py and react_agent.py
# 4. Restart backend: systemctl restart info-hub-backend
```
