---
name: amazingdata-relay-integration
description: 在阿里云服务器上通过 SSH 隧道集成 Windows AmazingData SDK。解决内网隔离、Token 认证及 relay 500 错误排查。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [amazingdata, ssh-tunnel, windows-bridge, stock-data]
    related_skills: [stock-monitoring-automation, tencent-market-data-adapter]
---

# AmazingData Relay 集成指南

## 核心架构
```
[阿里云 Hermes] --(SSH Tunnel)--> [Windows Relay (127.0.0.1:17713)] --(SDK)--> [银河证券/AmazingData]
```

## 配置步骤

### 1. SSH 隧道建立 (Windows 侧)
在 Windows 上运行 SSH 客户端或 frp，将本地 `7713` 端口映射到阿里云的 `17713`：
```bash
ssh -R 17713:127.0.0.1:7713 user@aliyun-server-ip
```

### 2. 阿里云环境配置
修改 `/root/hermes-agent/.env`：
```ini
AMAZINGDATA_RELAY_LOCAL_URL=http://127.0.0.1:17713
AMAZINGDATA_PUBLIC_RELAY_TOKEN=<你的 Token>
```

### 3. 适配器使用
使用 `tools/amazingdata_adapter.py` 进行数据获取，它内置了重试和格式标准化：
```python
from tools.amazingdata_adapter import get_kline, is_available

if is_available():
    # 获取上证指数日线
    data = get_kline("000001.SH", "20260501", "20260512", "day")
```

## 故障排查

| 现象 | 根因 | 解决方案 |
|------|------|----------|
| `127.0.0.1:17713` 不通 | SSH 隧道断开 | 检查 Windows SSH 进程或 frp 状态 |
| `401 Unauthorized` | Token 过期 | 在 Windows AmazingData 客户端重新生成 Token |
| `500 Internal Server Error` | SDK 未登录/后端崩溃 | **最常见**。确保 Windows 上 AmazingData 客户端已登录账户 `15300003409` |
| `Timeout` | 网络波动 | 适配器已内置 3 次重试，若仍失败则降级到东财/腾讯 |

## 关键约束
- **SDK 必须登录**：Relay 只是转发层，底层依赖 Windows 上的 AmazingData SDK 保持登录态。
- **日期格式**：API 要求 `begin_date` 和 `end_date` 为整数（如 `20260512`），适配器会自动转换。
- **内存限制**：不要在阿里云服务器直接安装 AmazingData SDK（需 Windows 环境），必须走隧道。