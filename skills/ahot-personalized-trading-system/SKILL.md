---
name: ahot-personalized-trading-system
description: 为 AHOT A股策略报告系统添加个性化用户持仓管理与交易计划生成能力。支持截图解析持仓、SQLite 存储、DeepSeek Vision API 识别、以及针对每个用户的盘前/盘中/盘后个性化报告生成。
tags: [ahot, stock, personalized, vision-api, sqlite]
---

# AHOT 个性化交易系统开发指南

## 核心架构

### 1. 数据层 (SQLite)
- **文件**: `generator/database.py`
- **表结构**:
  - `users`: 用户账号 (id, name, api_key)
  - `holdings`: 持仓信息 (user_id, code, name, cost_price, shares)
  - `personalized_reports`: 个性化报告缓存
- **特点**: 零依赖，WAL 模式，适合 2GB 服务器

### 2. 持仓解析器
- **文件**: `generator/holdings_parser.py`
- **功能**:
  - `parse_holdings_image()`: 调用 DeepSeek Vision API 解析券商 APP 截图
  - `parse_holdings_text()`: 正则提取文本格式持仓
- **关键点**: 
  - 使用 `deepseek-v4-flash` 模型进行视觉识别
  - 输出严格 JSON 数组格式，包含 code, name, cost_price, shares

### 3. 个性化报告生成器
- **文件**: `generator/personalized.py`
- **功能**:
  - `generate_pre_market()`: 持仓诊断 + 今日策略 + 大盘判断
  - `generate_post_market()`: 持仓复盘 + 明日计划
  - `generate_intraday()`: 盘中信号监控
- **Prompt 设计**: 
  - 注入用户持仓上下文
  - 结合市场数据 (AmazingData/Baostock)
  - 遵循"交易宪法"框架

### 4. API 端点
- **文件**: `api/main.py`
- **新增路由**:
  ```python
  GET  /api/user/register          # 注册/获取用户
  GET  /api/user/holdings          # 查询持仓
  POST /api/user/holdings          # 添加单条持仓
  POST /api/user/holdings/batch    # 批量添加持仓
  POST /api/user/holdings/parse-image  # 截图解析
  POST /api/user/reports/generate  # 生成个性化报告
  GET  /api/user/reports/{rtype}   # 获取指定报告
  ```

## 关键实现细节

### Nginx 反向代理配置
**问题**: FastAPI 的动态路由 `/api/user/reports/{rtype}` 会拦截 `/api/user/reports/generate`
**解决**: 
1. 在 FastAPI 中确保具体路由 (`/generate`) 定义在动态路由之前
2. Nginx 配置统一代理 `/api/` 到后端，不要拆分 path：
   ```nginx
   location /api/ {
       proxy_pass http://127.0.0.1:8002;  # 注意：不要带 /api/ 后缀
       proxy_read_timeout 120s;
   }
   ```

### Systemd 服务配置
**问题**: Python 模块导入路径问题
**解决**: 
```ini
[Service]
WorkingDirectory=/root/ahot-skill
ExecStart=/path/to/python -c "import sys; sys.path.insert(0, '/root/ahot-skill'); import uvicorn; uvicorn.run('api.main:app', ...)"
Environment=PYTHONPATH=/root/ahot-skill
```
或者创建 site-packages 软链接：
```bash
ln -sf /root/ahot-skill/generator /path/to/site-packages/generator
```

### LLM 调用策略
- **主模型**: DeepSeek `deepseek-chat` (非 reasoning 模型，content 字段正常返回)
- **Fallback**: 百炼 CodingPlan `qwen3.6-plus` (429 限流时自动切换)
- **Vision**: DeepSeek `deepseek-v4-flash` (用于截图解析)

## 部署检查清单

1. [ ] 初始化数据库: `python3 generator/database.py` (自动执行 init_db)
2. [ ] 配置 DeepSeek API Key (环境变量或 auth.json)
3. [ ] 更新 Nginx 配置并 reload
4. [ ] 重启 ahot-api 服务
5. [ ] 测试注册: `curl "https://reports.ai10088.com/api/user/register?user_id=test&name=Test"`
6. [ ] 测试持仓添加: `curl -X POST .../api/user/holdings?user_id=test -d '{"code":"600519",...}'`
7. [ ] 测试报告生成: `curl -X POST .../api/user/reports/generate?user_id=test&rtype=pre-market`

## 常见问题

### 1. 截图解析失败
- 检查 DeepSeek API Key 是否有效
- 确保图片 base64 编码正确（不含 `data:image/...` 前缀）
- Vision API 超时设置为 30s

### 2. 报告生成慢
- 个性化报告需要调用 LLM，单次约 5-10s
- 建议异步生成或增加 timeout

### 3. Nginx 400 Invalid HTTP request
- 检查 `proxy_pass` 是否带了多余的路径后缀
- 确保 FastAPI 路由顺序正确（具体在前，动态在后）