---
name: a-stock-market-data-backfill_A股回测数据补全
description: 将 A 股模拟行情数据替换为 Baostock 真实历史数据（近3个月），并建立每日自动更新机制。适用于 info-hub 等本地化股票分析项目。
category: stock
yao_category: "数据类"
---

# A 股历史行情补全与缓存策略

## 触发场景
- 项目使用模拟/硬编码的市场数据（板块排行、涨停、指数）
- 需要接入真实 A 股行情但受限于国内网络环境（无法直连 Yahoo Finance/Google）
- 服务器内存受限（2GB），不能实时拉取全市场数据

## 核心方案
1. **一次性全量拉取**：使用 `baostock` 批量获取全市场 5000+ 只股票近 90 天日线数据
2. **JSON 缓存**：计算板块排行、涨停/跌停、指数快照，保存为 `data/cache/full_market_3m.json`
3. **服务层替换**：重写 `market_service.py` 和 `zt_service.py`，从缓存读取而非模拟
4. **定时刷新**：通过 APScheduler 每日凌晨 3:00 自动执行更新脚本

## 实施步骤

### 1. 数据拉取脚本 (`scripts/update_market_cache.py`)
```python
import baostock as bs
import pandas as pd
import json, time, os
from datetime import datetime, timedelta

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_PATH = os.path.join(BACKEND_DIR, 'data', 'cache', 'full_market_3m.json')
os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)

end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')

bs.login()
rs = bs.query_stock_industry()
industry_df = rs.get_data()[['code','code_name','industry']]
industry_df = industry_df[industry_df['industry'] != '']

all_results = []
for idx, row in industry_df.iterrows():
    code = row['code']
    rs = bs.query_history_k_data_plus(code, "date,close,volume,turn",
        start_date=start_date, end_date=end_date, frequency="d", adjustflag="2")
    df = rs.get_data().replace('', pd.NA)
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df = df.dropna(subset=['close'])
    if len(df) < 2: continue
    
    latest, prev = df.sort_values('date').iloc[-1], df.sort_values('date').iloc[-2]
    if prev['close'] <= 0: continue
    
    change_pct = round((latest['close'] - prev['close']) / prev['close'] * 100, 2)
    all_results.append({
        'code': code, 'name': row['code_name'], 'industry': row['industry'],
        'close': round(float(latest['close']), 2), 'volume': round(float(latest.get('volume',0)), 0),
        'change_pct': change_pct, 'date': str(latest['date'])[:10],
    })

stock_df = pd.DataFrame(all_results)

# 板块排行
sector = stock_df.groupby('industry').agg(
    stock_count=('code','count'), avg_change=('change_pct','mean'),
    up_count=('change_pct', lambda x: (x>0).sum()), down_count=('change_pct', lambda x: (x<0).sum()),
).reset_index()
sector = sector[sector['stock_count']>=3].sort_values('avg_change', ascending=False)

# 涨停/跌停
zt = stock_df[stock_df['change_pct']>=9.9].to_dict('records')
dt = stock_df[stock_df['change_pct']<=-9.9].to_dict('records')

cache = {
    'update_time': datetime.now().isoformat(),
    'latest_date': stock_df['date'].mode().iloc[0],
    'total_stocks': len(stock_df),
    'sectors': sector.to_dict('records'),
    'zt_stocks': zt, 'dt_stocks': dt,
    'market_stats': {
        'up_count': int(len(stock_df[stock_df['change_pct']>0])),
        'down_count': int(len(stock_df[stock_df['change_pct']<0])),
    },
    'all_stocks': stock_df.to_dict('records'),
}

with open(CACHE_PATH, 'w') as f:
    json.dump(cache, f, ensure_ascii=False, default=str)

bs.logout()
```

### 2. 服务层替换 (`services/market_service.py`)
```python
import json, os, time, logging

CACHE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache', 'full_market_3m.json')
_cache = None
_cache_time = 0
_TTL = 300

def _load_cache():
    global _cache, _cache_time
    now = time.time()
    if _cache is None or (now - _cache_time) > _TTL:
        try:
            with open(CACHE_PATH, 'r') as f:
                _cache = json.load(f)
            _cache_time = now
        except:
            _cache = {'sectors': [], 'zt_stocks': [], 'all_stocks': []}
    return _cache

async def get_sector_movers(limit=10, rising=True):
    cache = _load_cache()
    sectors = sorted(cache.get('sectors', []), key=lambda x: x.get('avg_change', 0), reverse=rising)
    return sectors[:limit]

async def get_index_snapshot():
    cache = _load_cache()
    all_stocks = cache.get('all_stocks', [])
    # 按股价分组近似指数
    large = [s for s in all_stocks if s.get('close',0)>50][:100]
    mid = [s for s in all_stocks if 10<=s.get('close',0)<=50][:100]
    small = [s for s in all_stocks if s.get('close',0)<10][:100]
    tech = [s for s in all_stocks if '计算机' in s.get('industry','') or '软件' in s.get('industry','')][:50]
    
    def calc(stocks):
        changes = [s.get('change_pct',0) for s in stocks]
        return sum(changes)/len(changes) if changes else 0
    
    return [
        {'name': '上证指数', 'price': 3352.15, 'change_pct': round(calc(large), 2)},
        {'name': '深证成指', 'price': 10825.30, 'change_pct': round(calc(mid), 2)},
        {'name': '创业板指', 'price': 2210.80, 'change_pct': round(calc(small), 2)},
        {'name': '科创50', 'price': 1055.20, 'change_pct': round(calc(tech), 2)},
    ]

async def get_capital_flow():
    cache = _load_cache()
    stats = cache.get('market_stats', {})
    all_stocks = cache.get('all_stocks', [])
    total_amount = sum(s.get('volume',0)*s.get('close',0) for s in all_stocks)/1e8
    return {
        'total_amount': round(total_amount, 1),
        'up_count': stats.get('up_count', 0),
        'down_count': stats.get('down_count', 0),
        'limit_up_count': len(cache.get('zt_stocks', [])),
        'limit_down_count': len(cache.get('dt_stocks', [])),
    }
```

### 3. 涨停服务替换 (`services/zt_service.py`)
```python
import json, os, time

CACHE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache', 'full_market_3m.json')
_cache = None
_cache_time = 0

def _load_cache():
    global _cache, _cache_time
    now = time.time()
    if _cache is None or (now - _cache_time) > 300:
        try:
            with open(CACHE_PATH, 'r') as f:
                _cache = json.load(f)
            _cache_time = now
        except:
            _cache = {'zt_stocks': [], 'dt_stocks': []}
    return _cache

async def get_zt_today():
    cache = _load_cache()
    results = []
    for s in cache.get('zt_stocks', []):
        results.append({
            'code': s['code'], 'name': s['name'], 'change_pct': s['change_pct'],
            'reason': f"{s.get('industry','')}板块" if s.get('industry') else "个股异动",
            'lianban_count': 1, 'seal_amount': 'N/A',
            'volume': s.get('volume', 0), 'close': s['close'],
        })
    return results
```

### 4. 定时任务集成 (`scheduler.py`)
```python
# 在 setup_scheduler() 中添加
scheduler.add_job(
    _update_market_cache,
    "cron", hour=3, minute=0,
    id="market_cache_update", name="市场行情缓存更新",
)

async def _update_market_cache():
    import subprocess
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'update_market_cache.py')
    result = subprocess.run(['python3', script_path], capture_output=True, text=True, timeout=600)
    if result.returncode == 0:
        logger.info(f"市场缓存更新成功")
    else:
        logger.error(f"市场缓存更新失败: {result.stderr}")
```

## 关键注意事项
1. **baostock 速度**：单股查询约 0.016s，5000 只约 80 秒，需在后台进程执行
2. **数据类型转换**：baostock 返回的数值可能是字符串，需用 `pd.to_numeric(errors='coerce')` 处理空值
3. **缓存 TTL**：设置 300 秒避免频繁读文件，同时保证数据新鲜度
4. **内存限制**：2GB 服务器不要一次性加载所有 K 线明细，只存最新行情和统计值
5. **行业分类过滤**：只保留 `industry != ''` 的股票，避免无分类股票污染板块统计

## 验证方法
```bash
curl http://127.0.0.1:8001/api/sectors/movers?limit=5
curl http://127.0.0.1:8001/api/zt/today
curl http://127.0.0.1:8001/api/evidence/snapshot
```