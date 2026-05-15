---
name: amazingdata-ssh-tunnel-integration
description: Integrate AmazingData Market Data API running on a remote Windows machine via SSH tunnel into the info-hub backend. Implements a three-tier fallback chain (Local Tunnel -> Public Relay -> Empty) to ensure high availability in constrained environments.
trigger: When integrating AmazingData data sources, especially when dealing with network isolation or needing a local backup for public APIs.
---

# AmazingData SSH Tunnel Integration

## Context
AmazingData SDK runs on a Windows machine (GA). To access it from the Alibaba Cloud server (info-hub), we use an SSH reverse tunnel. The integration must be resilient to network fluctuations.

## Architecture
1. **Source**: Windows GA runs `amazingdata-market-data` service on port 7713.
2. **Tunnel**: SSH reverse tunnel maps `127.0.0.1:17713` on Alibaba Cloud to `127.0.0.1:7713` on Windows.
3. **Adapter**: `quant_market_service.py` implements a three-tier fallback.

## Implementation Steps

### 1. Configuration
Add the tunnel URL to `backend/services/quant_market_service.py`:
```python
AMAZINGDATA_HTTP_TUNNEL_URL = os.environ.get("AMAZINGDATA_HTTP_TUNNEL_URL", "http://127.0.0.1:17713")
```

### 2. Fallback Logic (`_fetch_amazingdata_kline`)
Implement the following priority:
1. **Local Tunnel**: Try `AMAZINGDATA_HTTP_TUNNEL_URL`. No token required. Fast and stable if tunnel is up.
2. **Public Relay**: If tunnel fails or returns empty, try `AMAZINGDATA_PUBLIC_BASE_URL`. Requires Bearer token.
3. **Empty**: If both fail, return empty list and log warning.

**Code Example**:
```python
async def _fetch_amazingdata_kline(code: str, period: str = "day", ...):
    params = {"code": code.upper(), "period": period}
    endpoint = "/api/v1/trading/daily-bars" if period == "day" else "/api/v1/trading/kline"

    # 1. Local SSH Tunnel (No Token)
    try:
        url = f"{AMAZINGDATA_HTTP_TUNNEL_URL}{endpoint}"
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            payload = resp.json()
            items = payload.get("data", {}).get("items", [])
            if items:
                return _parse_ad_items(code, items)
    except Exception as e:
        logger.debug(f"Tunnel failed: {e}")

    # 2. Public Relay (Token Required)
    token = _load_amazingdata_token()
    if not token: return []
    
    try:
        url = f"{AMAZINGDATA_PUBLIC_BASE_URL}{endpoint}"
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(url, params=params, headers={"Authorization": f"Bearer {token}"})
            resp.raise_for_status()
            return _parse_ad_items(code, resp.json().get("data", {}).get("items", []))
    except Exception as e:
        logger.warning(f"Public relay failed: {e}")
        return []
```

### 3. Health Check Endpoint
Add `/api/quant/amazingdata/source-status` in `routers/quant_market.py` to monitor:
- Tunnel health (`/health` endpoint).
- Public relay health.
- Real-time data verification (e.g., query `000001.SZ`).

## Verification
- Run `curl http://127.0.0.1:17713/health` on the server to confirm tunnel connectivity.
- Use the new endpoint to verify data retrieval: `GET /api/quant/amazingdata/daily-bars?code=000001.SZ`.

## Pitfalls
- **Code Format**: AmazingData API expects codes like `000001.SZ`. Ensure normalization.
- **Timeouts**: Set reasonable timeouts (10-15s) for tunnel requests to avoid hanging the main thread.
- **Empty Responses**: The tunnel might be up but the Windows service might not have data loaded. Always check `items` count before assuming success.

## Rollback
If issues arise, revert `quant_market_service.py` and `quant_market.py` to the previous version using git.