---
name: ahot-api-productization
description: 将内部 Cron 报告产品化为公开 REST API + Skill 的标准流程。适用于将已有的定时任务输出（如盘前/盘中/复盘报告）封装为可订阅的 API 服务，并配套 GitHub Skill 仓库供第三方 Agent 安装。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  yao_category: "DevOps"
  hermes:
    tags: [api, productization, skill, nginx, fastapi]
---

# AHOT API 产品化工作流

将内部生成的策略报告（Cron Job 输出）转化为对外公开的 REST API，并提供标准化的 Skill 供其他 AI Agent 调用。

## 核心架构

```
┌─────────────────────────────────────────────┐
│              你的服务器 (2GB)                 │
│                                             │
│  FastAPI Backend (port 8001)                │
│  ├── /api/public/reports/* (公开 API)       │
│  └── SQLite (可选：用户/API Key/订阅管理)     │
│                                             │
│  Cron Jobs (已运行)                          │
│  ├── 盘前早报 → ~/.hermes/cron/output/...   │
│  ├── 收盘复盘 → gbrain-sync/...             │
│  └── 每日日报 → gbrain-sync/...             │
│                                             │
│  Nginx Reverse Proxy                        │
│  └── reports.yourdomain.com → localhost:8001│
└─────────────────────────────────────────────┘
         ↑ API Key 认证 (二期)          ↑ 浏览器访问
    第三方 Agent 安装 Skill             用户本人浏览
```

## 实施步骤

### 第一步：创建 GitHub 私有 Skill 仓库

```bash
gh repo create username/ahot-skill --private \
  --description "A 股策略报告 API — 盘前/盘中/盘后/选股，合规信息整理"
cd ahot-skill && git init && git branch -m main
```

### 第二步：编写 SKILL.md

参考 `aihot` skill 的结构，重点包含：
- **合规声明**：每份报告底部必须附带"不预测涨跌、不承诺收益"免责声明
- **注册流程**：用户如何获取 API Key
- **端点列表**：清晰的 API 路径和参数说明
- **错误处理**：401/403/404/429 的处理建议
- **输出格式规范**：禁止暴露基础设施细节（端点路径、raw 参数等）

### 第三步：后端 API 实现 (FastAPI)

在现有 FastAPI 项目中新增 router：

```python
# routers/aihot_reports.py
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path

router = APIRouter(prefix="/api/public/reports", tags=["reports"])

REPORTS_DIR = Path.home() / ".aihot" / "reports"

@router.get("/pre-market")
def get_pre_market(date: str = Query(None)):
    # 从 cron 输出或 gbrain-sync 目录读取 markdown
    # 返回结构化 JSON + 免责声明
    pass
```

**关键点**：
- 报告数据源优先从 `gbrain-sync` 目录读取（已同步的 markdown）
- 其次从 `~/.hermes/cron/output` 读取原始 cron 输出
- 所有响应必须包含 `"disclaimer"` 字段

### 第四步：Nginx 配置二级域名

```nginx
server {
    listen 80;
    server_name reports.yourdomain.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8001/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /www/wwwroot/reports.yourdomain.com;
        index index.html;
    }
}
```

### 第五步：落地页与文档

创建简单的 HTML 落地页，包含：
- 合规声明（醒目位置）
- 快速开始指南（curl 示例）
- API 端点表格
- GitHub Skill 仓库链接

### 第六步：推送 Skill 到 GitHub

```bash
cd ahot-skill
git add -A
git commit -m "init: ahot-reports skill"
git push origin main
```

## 合规红线

1. **每条报告必须附带免责声明**："本报告仅用于信息整理与逻辑梳理，不预测涨跌，不承诺收益，不构成投资建议。"
2. **不提供买卖指令**：只有分析框架和观察方向
3. **不提供实时行情数据**：只有逻辑分析
4. **用户协议明确风险告知**

## 关键经验总结（2026-05-10）

### 1. Wiki HTML 渲染修复
Cron 生成的 HTML 报告在 Wiki SPA 中会被 `html.escape()` 转义。需在 `wiki/helpers/publish_static_wiki.py` 的 `md_to_html` 中增加检测：
```python
if stripped.startswith('<div') or stripped.startswith('<h1'):
    return markdown  # 直接返回原 HTML
```

### 2. LLM 快速失败机制
个性化报告生成依赖 LLM。若 Key 失效，应在 `generator/llm_client.py` 启动时校验，并在 API 层捕获 `RuntimeError` 返回 503，避免静默超时（默认超时从 120s 降至 60s）。

### 3. Skill 分发路径配置
Nginx `alias` 指向 `/root` 目录会因权限问题返回 403。应通过 FastAPI 静态文件端点提供 `install.sh` 和 `SKILL.md`，并由 Nginx 反向代理到 `127.0.0.1:8002`。

### 4. 非交易日数据兜底
公开报告接口需实现 `_find_latest_available_date`，当请求日期无数据时自动回溯最近 7 天内的有效数据。

## 常见陷阱

- **不要硬编码报告路径**：使用 `Path.home()` 动态定位
- **不要忘记 CORS 头**：Nginx 需配置 `Access-Control-Allow-Origin`
- **不要暴露 API Key**：Skill 中只展示获取方式，不展示真实 Key
- **不要高频轮询**：报告每天生成一次，前端应缓存结果
- **二级域名证书**：不能复用一级域名证书，需申请通配符 `*.ai10088.com`（certbot + dns-aliyun）
- **systemd 端口冲突**：启动前检查端口是否被占用
- **Nginx MIME type**：`.md` 文件默认下载，需配置 `/skill` 指向 HTML 展示页

## 验证清单

- [ ] `curl reports.yourdomain.com/api/public/reports/list` 返回 JSON
- [ ] `curl reports.yourdomain.com/api/public/reports/pre-market` 返回带 disclaimer 的报告
- [ ] GitHub 仓库可见且 SKILL.md 格式正确
- [ ] Nginx 配置通过 `nginx -t` 测试
- [ ] DNS 解析生效（`dig reports.yourdomain.com`）