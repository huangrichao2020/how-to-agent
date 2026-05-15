---
name: a-stock-data-integration-pattern
description: >
  Pattern for integrating simonlin1212/a-stock-data capabilities into FastAPI projects.
  Covers: tagging before integration, creating multi-layer routers, service layer abstraction,
  and API endpoint exposure. Use when adding comprehensive A-share data capabilities to info-hub or ahot-skill.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [a-stock, integration, fastapi, pattern]
    related_skills: [a-stock-data-resilience, info-hub-stock-integration]
---

# A股数据能力集成模式

## 核心原则

1. **先打回滚 tag**：任何大规模集成前必须 `git tag vX.Y.Z-pre-{feature}-integration`
2. **分层架构**：行情层 → 研报层 → 信号层 → 新闻层 → 基础数据层 → 公告层
3. **服务抽象**：在 ahot-skill 中创建 `stock_data_service.py` 作为数据访问层，不直接暴露底层实现
4. **降级链**：akshare → 腾讯HTTP → 返回空（不阻断主流程）

## 集成步骤

### Step 1: 打回滚 Tag

```bash
cd /root/info-hub && git tag v2.0.0-pre-stock-capability-update
cd /root/ahot-skill && git tag v1.5.0-pre-stock-capability-update
```

### 2. 降级策略：同花顺热点 + 腾讯行情补全 (2026-05-14 验证通过)

当东财 `ak.stock_zh_a_spot_em` 接口因反爬或网络问题失效时，采用此方案。

**核心逻辑**：同花顺提供“当日强势股代码列表”（无行情数据） → 腾讯批量补充“成交额/市值/换手率”等关键指标。

```python
def fetch_ths_hot_stocks_with_tencent(date: str = None) -> pd.DataFrame:
    """
    同花顺热点接口 + 腾讯行情补充 — 当日强势股 + 完整行情数据
    """
    from datetime import date as _date
    if date is None:
        date = _date.today().strftime("%Y-%m-%d")
    
    # 1. 获取同花顺强势股代码列表
    url = f"http://zx.10jqka.com.cn/event/api/getharden/date/{date}/orderby/date/orderway/desc/charset/GBK/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.0.0 Safari/537.36"}
    
    def _do_fetch():
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        if data.get("errocode", 0) != 0:
            raise RuntimeError(f"同花顺热点错误: {data.get('errormsg', '')}")
        return data.get("data", [])
    
    try:
        rows = retry_with_backoff(_do_fetch, max_retries=2, base_delay=1)
    except Exception as e:
        print(f"  同花顺热点获取失败: {e}")
        return pd.DataFrame()
    
    if not rows:
        return pd.DataFrame()
        
    codes = [row["code"] for row in rows if row.get("code")]
    if not codes:
        return pd.DataFrame()

    # 2. 通过腾讯接口批量补充行情数据
    tencent_url = "http://qt.gtimg.cn/q=" + ",".join([
        f"{'sh' if c.startswith(('6','9')) else 'sz'}{c}" for c in codes
    ])
    try:
        r2 = requests.get(tencent_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        tencent_data = r2.content.decode("gbk")
    except Exception as e:
        print(f"  腾讯行情补充失败: {e}")
        return pd.DataFrame()

    df_rows = []
    for line in tencent_data.strip().split(";"):
        if "=" not in line: continue
        vals = line.split('"')[1].split("~")
        if len(vals) < 50: continue
        df_rows.append({
            "代码": vals[2],
            "名称": vals[1],
            "最新价": float(vals[3]) if vals[3] else 0,
            "涨跌幅": float(vals[32]) if vals[32] else 0,
            "成交额": float(vals[37]) * 10000 if vals[37] else 0, # 万转元
            "换手率": float(vals[38]) if vals[38] else 0,
            "总市值": float(vals[44]) * 100000000 if vals[44] else 0, # 亿转元
            "成交量": float(vals[36]) if vals[36] else 0,
            "题材归因": next((r.get("reason","") for r in rows if r.get("code")==vals[2]), "")
        })

    df = pd.DataFrame(df_rows)
    print(f"  同花顺+腾讯行情获取成功: {len(df)} 只强势股")
    return df
```

**避坑指南**：
- **字段缺失**：同花顺热点接口只返回 `id, name, code, reason, date, market`，必须通过腾讯接口补全 `总市值` 和 `成交额`，否则下游 `(总市值 > 20亿)` 过滤会清空所有数据。
- **真实因果**：软件自动分类的行业（如“房地产”）往往是误导。必须提取同花顺的 `reason` 字段（如“间接持有长鑫科技”）作为真实炒作逻辑。
```python
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(tags=["A股全栈数据"])

# Layer 1: 行情层
@router.get("/quote/tencent")
def tencent_quote(codes: str = Query(...)): ...

# Layer 2: 研报层
@router.get("/research/eastmoney")
def eastmoney_reports(code: str = Query(...)): ...

# ... 其他层级
```

注册到 `main.py`:
```python
from routers import a_stock_data
app.include_router(a_stock_data.router, prefix="/api/stock", tags=["A股全栈数据"])
```

### Step 3: 创建 Service Layer (ahot-skill)

文件：`generator/stock_data_service.py`

```python
"""轻量级数据服务层，复用 a-stock-data 能力"""
import requests
from datetime import datetime

def get_tencent_quote(codes: list[str]) -> dict:
    """腾讯实时行情 — 轻量HTTP"""
    try:
        # ... implementation
    except Exception as e:
        logger.warning(f"腾讯行情失败: {e}")
        return {}  # 降级：返回空，不阻断
```

暴露 API 端点：
```python
from generator.stock_data_service import get_stock_snapshot, get_market_snapshot

@app.get("/api/public/stock/snapshot")
def api_stock_snapshot(code: str = Query(...)):
    return get_stock_snapshot(code)
```

### Step 4: 验证与提交

```bash
# 验证路由注册
cd /root/info-hub && python3 -c "
from routers.a_stock_data import router
print(f'Routes: {len(router.routes)}')
for r in router.routes:
    print(f'  {\"|\".join(r.methods)} {r.path}')
"

# 提交
git add -A && git commit -m "feat: integrate a-stock-data capability"
git push origin main
```

### Step 5: 重启服务

```bash
# info-hub
cd /root/info-hub/backend && bash start.sh restart

# ahot-skill
systemctl restart ahot-api.service

# 健康检查
curl http://127.0.0.1:8001/api/health
curl http://127.0.0.1:8002/health
```

## 避坑指南

1. **不要直接复制 SKILL.md**：SKILL.md 是给 AI 助手用的指令集，需要转换为 FastAPI router
2. **降级链必须完整**：每个数据源调用都要有 `try-except`，失败时返回空或默认值
3. **代码归一化**：股票代码统一用 `_normalize_code()` 处理（去掉 SH/SZ/BJ 前缀）
4. **市场前缀映射**：6/9开头→sh，8开头→bj，其他→sz
5. **腾讯字段校准**：索引 43 是振幅不是 PB，PB 在索引 46（网上很多教程写错）

## 端点清单

| 层级 | 端点数量 | 示例路径 |
|------|---------|---------|
| L1 行情 | 3 | `/api/stock/quote/tencent` |
| L2 研报 | 2 | `/api/stock/research/eastmoney` |
| L3 信号 | 7 | `/api/stock/signal/hot-stocks` |
| L4 新闻 | 2 | `/api/stock/news/cls` |
| L5 基础 | 2 | `/api/stock/fundamentals/mootdx` |
| L6 公告 | 1 | `/api/stock/announcement/cninfo` |

总计：17 个 info-hub 端点 + 5 个 ahot-skill 端点

## 回滚方法

```bash
cd /root/info-hub && git reset --hard v2.0.0-pre-stock-capability-update
cd /root/ahot-skill && git reset --hard v1.5.0-pre-stock-capability-update
```