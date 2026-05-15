---
name: iwencai-api-integration
description: 同花顺问财 (iWencai) API 集成指南，包含 CLI 安装、Key 轮转配置及 Python 调用方法。适用于在受限服务器环境下获取高质量 A 股板块及个股数据。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [stock, api, iwencai, data-source]
    related_skills: [a-stock-market-data-backfill, tencent-market-data-adapter]
---

# 同花顺问财 API 集成

## 核心优势
同花顺问财 API 提供比东财/腾讯更结构化的金融数据，尤其在**板块筛选**、**资金流向**和**自然语言选股**方面表现优异。

## 环境配置

### 1. 安装 CLI
```bash
curl -sSL https://www.iwencai.com/skillhub/static/0.0.4/download_and_install.sh | bash
# 或手动解压：
cd /tmp && unzip iwencai-skillhub-cli.zip && cd iwencai-skillhub-cli && bash iwencai-install.sh
```
CLI 路径通常为：`/root/.local/bin/iwencai-skillhub-cli`

### 2. Key 管理（3 Key 轮转）
在 `.env` 中配置三个 Key 以实现高可用：
```bash
IWENCAI_BASE_URL=https://openapi.iwencai.com
IWENCAI_API_KEY_1=sk-proj-...
IWENCAI_API_KEY_2=sk-proj-...
IWENCAI_API_KEY_3=sk-proj-...
```

### 3. 技能安装
使用 CLI 安装特定技能包（如 `hithink-sector-selector`）：
```bash
/root/.local/bin/iwencai-skillhub-cli install hithink-sector-selector
```

## Python 调用示例

通过执行技能包内的 `cli.py` 脚本进行调用，支持环境变量注入：

```python
import os
import subprocess
import json

def query_iwencai(query: str, limit: int = 10):
    # 简单的 Key 轮转逻辑
    keys = [os.getenv('IWENCAI_API_KEY_1'), os.getenv('IWENCAI_API_KEY_2'), os.getenv('IWENCAI_API_KEY_3')]
    for key in keys:
        if not key: continue
        env = os.environ.copy()
        env['IWENCAI_API_KEY'] = key
        
        cmd = [
            "python3", 
            "/tmp/iwencai-skillhub-cli/skills/hithink-sector-selector/scripts/cli.py",
            "--query", query,
            "--limit", str(limit)
        ]
        
        try:
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"Key failed: {e}")
            continue
    return None
```

## 常见查询指令
- **板块筛选**: "今日涨幅前5的行业板块"
- **个股筛选**: "市值大于500亿且PE小于20的股票"
- **资金流向**: "主力资金净流入前10的板块"

## 注意事项
1. **配额限制**: 免费 Key 有每日调用上限，务必实现轮转机制。
2. **数据延迟**: 盘中数据可能存在分钟级延迟，适合做盘前分析和趋势确认。
3. **降级策略**: 当问财 API 不可用时，应降级回东财 (akshare) 或腾讯行情接口。