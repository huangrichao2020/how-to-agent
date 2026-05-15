---
name: ahot-skill-productization
description: 将 Hermes Agent 每日生成的 A 股策略报告产品化为独立 REST API + Skill 的标准流程。适用于将已有的定时任务输出（如盘前/盘中/盘后报告）通过 FastAPI 对外提供，支持第三方 Agent 安装 Skill 后自动拉取。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  yao_category: "AI思考"
  hermes:
    tags: [productization, api, skill, stock-report]
---

# AHOT Skill 产品化工作流

## 核心思路

将 cron 生成的 Markdown 报告通过 **独立 FastAPI 服务** 暴露为 REST API，配合 Nginx 反向代理和 GitHub Skill 仓库，实现：
1. 用户注册获取 API Key（二期）
2. 第三方 Agent 安装 SKILL.md 后自动调用 API
3. 合规声明：不预测涨跌、不承诺收益

## 架构设计

```
reports.ai10088.com (Nginx)
    ↓ proxy_pass
127.0.0.1:8002 (ahot-skill/api/main.py — 独立 FastAPI)
    ↓ 读取
~/wiki/gbrain-sync/*.md  (cron → gbrain → sync 导出)
~/.hermes/cron/output/*/  (cron 原始输出兜底)
```

**关键原则**：
- **独立项目**：不耦合 info-hub 后端，自包含 FastAPI 应用
- **数据源复用**：直接读取 gbrain-sync 导出的 Markdown，无需额外数据库
- **systemd 托管**：开机自启，崩溃自动重启

## 实施步骤

### 1. 创建独立 API 服务

```bash
mkdir -p /root/ahot-skill/api
cd /root/ahot-skill/api

# requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic==2.9.0
EOF

# main.py — 完整代码见 api/main.py
# 核心端点：
# GET /api/public/reports/daily?date=YYYY-MM-DD
# GET /api/public/reports/pre-market?date=YYYY-MM-DD
# GET /api/public/reports/post-market?date=YYYY-MM-DD
# GET /api/public/reports/intraday
# GET /api/public/reports/stock-pool
# GET /api/public/reports/list?limit=N
```

**数据读取逻辑**：
1. 优先从 `~/wiki/gbrain-sync/{slug}.md` 读取（gbrain-sync.py 每 4h 导出）
2. 兜底从 `~/.hermes/cron/output/*/` 扫描匹配日期的 .md 文件
3. 正则提取标题、日期、正文，限制 12000 字符

### 2. systemd 服务配置

```ini
# /etc/systemd/system/ahot-api.service
[Unit]
Description=AHOT A股策略报告 API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/ahot-skill/api
ExecStart=/root/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8002 --workers 1
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable ahot-api
sudo systemctl start ahot-api
sudo systemctl status ahot-api  # 验证 active (running)
```

### 3. Nginx 反向代理

```nginx
# /www/server/panel/vhost/nginx/reports.ai10088.com.conf
server {
    listen 80;
    server_name reports.ai10088.com;

    add_header Access-Control-Allow-Origin * always;
    add_header Access-Control-Allow-Methods "GET, POST, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Authorization, Content-Type" always;

    if ($request_method = 'OPTIONS') {
        return 204;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8002/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 30s;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8002/docs;
        proxy_set_header Host $host;
    }

    root /www/wwwroot/reports.ai10088.com;
    index index.html;
}
```

```bash
nginx -t && nginx -s reload
```

### 4. DNS 配置

在阿里云 DNS 添加 A 记录：
- 主机记录：`reports`
- 记录值：服务器 IP（如 120.26.32.59）
- TTL：10 分钟

### 5. GitHub Skill 仓库

```bash
cd /root/ahot-skill
git init
git remote add origin git@github.com:huangrichao2020/ahot-skill.git
git branch -m main

# 创建 SKILL.md（参考 aihot skill 格式）
# 创建 README.md
# 创建工作手册.md、交接手册.md

git add -A
git commit -m "init: ahot-skill productization"
git push origin main
```

**SKILL.md 核心内容**：
- 触发关键词："今天A股怎么样"、"盘前策略"、"收盘复盘"等
- API 端点说明 + curl 示例
- 合规声明：**每条报告必须附带免责声明**

### 6. 落地页

```html
<!-- /www/wwwroot/reports.ai10088.com/index.html -->
<!DOCTYPE html>
<html lang="zh">
<head>
    <title>AHOT — A股策略报告 API</title>
</head>
<body>
    <h1>📊 AHOT — A 股策略报告 API</h1>
    <div class="disclaimer">
        ⚠️ 本报告仅用于信息整理与逻辑梳理，不预测涨跌，不承诺收益，不构成投资建议。
    </div>
    <!-- API 端点表格 + 安装 Skill 指引 -->
</body>
</html>
```

## 验证清单

```bash
# 1. API 健康检查
curl http://localhost:8002/health

# 2. 报告列表
curl http://localhost:8002/api/public/reports/list | python3 -m json.tool

# 3. Nginx 代理
curl http://reports.ai10088.com/api/public/reports/list

# 4. systemd 状态
sudo systemctl status ahot-api

# 5. DNS 解析
dig reports.ai10088.com
```

## 常见陷阱

| 问题 | 原因 | 解决 |
|------|------|------|
| 端口冲突 (Errno 98) | 旧进程未杀死 | `kill $(lsof -t -i:8002)` 或停止 background 进程 |
| API 返回 404 | gbrain-sync 未运行 | `python3 ~/wiki/helpers/gbrain_sync.py` 手动触发 |
| systemd 启动失败 | Python 路径错误 | 确认 `which python` 路径与 ExecStart 一致 |
| Nginx 502 | 后端未启动 | `sudo systemctl restart ahot-api` |
| DNS 未生效 | 缓存 TTL | 等待 10-30 分钟，或本地 `/etc/hosts` 测试 |

## 合规要点

1. **免责声明**：每条报告底部必须附带"不预测涨跌、不承诺收益、不构成投资建议"
2. **不提供买卖指令**：只给分析框架和观察方向
3. **数据来源透明**：标注"基于公开市场数据和逻辑分析"
4. **不承诺收益**：避免任何暗示稳赚的话术

## 二期规划

- [ ] 用户注册/登录 + API Key 管理（SQLite users/api_keys 表）
- [ ] 订阅分层（免费试用 → 月度付费）
- [ ] Web 端浏览报告页面（Vite SPA）
- [ ] 定时推送（飞书/微信 webhook）
- [ ] 认证中间件（Bearer Token 校验）