---
name: a-stock-realtime-monitor-fallback
description: A股盘中实时监控脚本的 API 故障回退方案。当东财 API (push2.eastmoney.com) 不可达时，自动切换至腾讯行情接口 (qt.gtimg.cn)。
category: stock
---

# A 股盘中监控 API 回退方案

## 触发条件
- `realtime_monitor.py` 运行时出现 "Remote end closed connection without response" 或东财 API 超时。
- 服务器网络环境受限（如阿里云部分节点对东财 push2 接口有拦截）。

## 核心逻辑
将 `fetch_quotes` 函数从东财批量接口切换为腾讯单行文本接口。

### 1. 接口对比
| 特性 | 东财 (原方案) | 腾讯 (回退方案) |
| :--- | :--- | :--- |
| **URL** | `push2.eastmoney.com/.../ulist.np/get` | `qt.gtimg.cn/q=sh600519,sz000001` |
| **格式** | JSON | 纯文本 (GBK 编码, `v_shxxxx="..."`) |
| **字段** | `f2`(价), `f3`(涨跌幅) 等 | `~` 分隔的第 3, 32, 31 位等 |
| **优势** | 字段全，含主力流向 | 连通性极好，延迟低 |

### 2. 代码实现 (`scripts/realtime_monitor.py`)
```python
def fetch_quotes(stocks: list[dict]) -> dict:
    """使用腾讯行情接口获取实时数据"""
    codes_str = ",".join(
        f"{'sh' if s['code'].startswith(('6','9')) else 'sz'}{s['code']}"
        for s in stocks
    )
    url = f"https://qt.gtimg.cn/q={codes_str}"
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://finance.qq.com/",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("gbk") # 注意：腾讯返回 GBK
    except Exception as e:
        logger.error("腾讯API请求失败: %s", e)
        return {}

    quote_map = {}
    for line in raw.strip().split(";"):
        if "=" not in line: continue
        _, value = line.split("=", 1)
        parts = value.strip('"').split("~")
        if len(parts) < 40: continue
        
        code = parts[2].zfill(6)
        quote_map[code] = {
            "f2": float(parts[3]),      # 最新价
            "f3": float(parts[32]),     # 涨跌幅%
            "f15": float(parts[33]),    # 最高
            "f16": float(parts[34]),    # 最低
            "f184": float(parts[37]),   # 成交额(万)
            # ... 其他字段映射见脚本
        }
    return quote_map
```

## 验证步骤
1. 运行 `python3 scripts/realtime_monitor.py --once`。
2. 观察日志：`采集 52/53 只` 即为成功。
3. 检查数据库：`sqlite3 data/realtime_monitor.db "SELECT COUNT(*) FROM snapshots WHERE ts LIKE '2026-05-11%';"`。

## 注意事项
- 腾讯接口不提供“主力净流入”(`f62`)，脚本中默认置 0。
- 腾讯接口的成交额单位是“万”，与东财一致，无需换算。
- 必须使用 `decode("gbk")`，否则中文股票名会乱码。