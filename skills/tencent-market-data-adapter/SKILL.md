---
name: tencent-market-data-adapter
description: 在受限环境（阿里云、无 Token、东财/雪球 API 失效）下，使用腾讯行情接口获取 A 股实时数据。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  yao_category: "数据类"
  hermes:
    tags: [stock, data, adapter, tencent]
---

# 腾讯行情数据适配器 (Tencent Market Data Adapter)

## 适用场景
- 东方财富 `akshare` 接口被 Ban 或连接超时。
- 雪球 API 需要复杂 Token 验证。
- 服务器内存受限（2GB），无法运行重型爬虫框架。
- 需要获取：指数行情、个股价格、涨跌幅、量比、买卖盘压力。

## 核心优势
1. **无需 Token**：直接 HTTP GET 请求。
2. **极速稳定**：阿里云直连 `qt.gtimg.cn` 毫秒级响应。
3. **轻量解析**：正则提取 GBK 编码文本，无重型依赖。

## 接口地址
`http://qt.gtimg.cn/q={codes}`
- `codes`: 逗号分隔的代码列表，如 `sh600519,sz000001`。

## 字段映射 (以 `~` 分割)
| 索引 | 含义 | 说明 |
| :--- | :--- | :--- |
| 1 | 名称 | 股票/指数名称 |
| 3 | 最新价 | 当前价格 |
| 32 | 涨跌幅 | 百分比数值 (e.g., 1.5 表示 +1.5%) |
| 49 | 量比 | 衡量成交量活跃度 |
| 7 | 外盘 | 主动买入成交量 |
| 8 | 内盘 | 主动卖出成交量 |
| 36 | 成交额 | 单位：万元 |

## 资金流向替代方案
由于腾讯不提供“主力净流入”，使用 **(外盘 - 内盘)** 作为买卖意愿指标：
- **正值**：买方占优（抢筹）。
- **负值**：卖方占优（抛压）。

## Python 实现示例

```python
import requests
import re

class TencentMarketData:
    BASE_URL = "http://qt.gtimg.cn/q="
    
    INDICES = {
        "上证指数": "sh000001",
        "深证成指": "sz399001",
        "创业板指": "sz399006",
        "科创50": "sh000688",
        "沪深300": "sh000300",
        "黄金ETF": "sh518880",
        "原油LOF": "sz161129"
    }

    def get_quotes(self, codes):
        if not codes: return {}
        code_list = list(codes.values()) if isinstance(codes, dict) else codes
            
        url = self.BASE_URL + ",".join(code_list)
        try:
            r = requests.get(url, timeout=10)
            r.encoding = 'gbk'
            results = {}
            
            for line in r.text.split(';'):
                match = re.search(r'v_(sh|sz)(\d+)="([^"]+)"', line)
                if match:
                    code = match.group(2)
                    f = match.group(3).split('~')
                    if len(f) > 40:
                        results[code] = {
                            "code": code,
                            "name": f[1],
                            "price": float(f[3]),
                            "change_pct": float(f[32]),
                            "volume_ratio": float(f[49]),
                            "outer": int(f[7]), # 外盘
                            "inner": int(f[8]), # 内盘
                        }
            return results
        except Exception as e:
            print(f"Error: {e}")
            return {}
```

## 避坑指南
- **编码问题**：必须设置 `r.encoding = 'gbk'`，否则中文乱码。
- **板块数据**：腾讯不支持直接获取“行业板块排名”。如需板块强度，请通过计算股池中属于该板块的个股平均涨幅来间接推导。
- **并发限制**：单次请求建议不超过 60 只股票，避免 URL 过长或服务器拒绝。