---
name: amazingdata-integration
description: "AmazingData 集成 — SSH 隧道 + 中继 API 连接。Trigger: AmazingData/行情中继/Windows中转. Do NOT trigger for 其他数据源。"
version: 1.1.0
---
# AmazingData 集成

## 一句话版本
通过 SSH 隧道将 Windows 端的 AmazingData SDK 安全中继到阿里云服务器，解决内网隔离问题。

## 触发条件
- ✅ **触发**：AmazingData、行情中继、Windows 中转、AmazingData 连接/断开、SSH 隧道状态
- ❌ **不触发**：其他数据源（如 Baostock、AkShare、复盘盒子）、通用网络问题

## 架构概览
```
[阿里云 ECS] ←SSH 隧道→ [Windows 中转机] ←本地调用→ [AmazingData SDK]
```

## 工作流
1. **检查 SSH 隧道状态**：确认阿里云 → Windows 的隧道是否正常
2. **验证中继端口**：确认映射端口（默认 8080）可访问
3. **测试 AmazingData 连接**：发送测试请求验证数据通路
4. **数据采集/查询**：通过中继调用 AmazingData API
5. **异常恢复**：检测到断连时自动重连

## 关键配置
- **SSH 隧道**：`ssh -R 8080:localhost:8080 user@windows-host`
- **中继服务**：Windows 端运行 HTTP 中继服务暴露 SDK
- **超时设置**：请求超时 10s，连接超时 5s

## 异常处理

### SSH 隧道断开
- **症状**：连接超时、Connection refused
- **排查**：
  1. `ps aux | grep ssh` 检查隧道进程是否存在
  2. `netstat -tlnp | grep 8080` 检查端口监听
  3. Windows 端 SSH 服务是否正常运行
- **恢复**：重启隧道 `ssh -fN -R 8080:localhost:8080 user@windows-host`
- **预防**：配置 `ServerAliveInterval 60` + `ServerAliveCountMax 3` 自动保活

### AmazingData SDK 无响应
- **症状**：中继返回 502/504、数据为空
- **排查**：
  1. Windows 端中继服务进程是否正常
  2. AmazingData SDK 是否已登录/授权过期
  3. 查看中继服务日志确认具体错误码
- **恢复**：重启中继服务 → 重连 SDK → 重新登录（如需要）

### 数据延迟/超时
- **症状**：请求超过 10s 无响应
- **排查**：网络延迟（SSH 隧道 + 中继双重转发）、Windows 负载过高
- **恢复**：缩短查询范围、增加超时重试（最多 3 次，指数退避）

## 常见坑点
- ⚠️ SSH 隧道断开后不会自动恢复，需配合 autossh 或 systemd service 实现持久化
- ⚠️ AmazingData SDK 有调用频率限制，批量查询需加间隔（建议 ≥1s）
- ⚠️ 中继服务需设置访问白名单，避免暴露到公网
- ⚠️ Windows 端休眠/锁屏可能导致 SDK 断开，确保电源设置不休眠

## 监控指标
- SSH 隧道连通性（ping / 端口探测，每 60s）
- 中继服务健康检查（GET /health）
- 请求成功率 & 平均响应时间
