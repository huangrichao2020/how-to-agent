---
name: ahot-api-maintenance
description: AHOT A股策略报告 API 的维护、修复与功能扩展指南。涵盖非交易日兜底逻辑、HTML/Markdown 混合解析、以及 SQLite 用户系统的维护。
category: stock-trading
---

# AHOT API 维护指南

**项目路径**: `/root/ahot-skill`
**服务名**: `ahot-api.service` (端口 8002)

## 核心架构

1. **数据源优先级**: 
   - `data/reports/*.json` (Generator 生成的结构化 JSON，最高优先级)
   - `~/wiki/gbrain-sync/*.md` (Cron 同步的 Markdown/HTML 报告，兜底)
   - `~/.hermes/cron/output/*/` (原始 Cron 输出目录，用于回溯)

2. **个性化系统**: 
   - SQLite (`data/ahot_users.db`) 存储用户、持仓和个性化报告。
   - 支持截图解析持仓（调用 Vision API）。

## 关键维护点

### 1. 非交易日兜底逻辑
当请求当天（如周日）无数据时，API 应自动回溯返回最近一个有数据的日期，而不是报 404。

**实现位置**: `api/main.py` 中的 `_find_latest_available_date` 函数。
- 遍历过去 7 天，检查 `cron/output` 或 `local json` 是否存在对应日期的报告。
- **注意**: 必须在 `get_daily`, `get_pre_market`, `get_post_market` 三个端点中统一应用此逻辑。

### 2. 混合内容解析 (_extract_report)
Cron 生成的报告可能是 Markdown，也可能是包含 Frontmatter 的 HTML。

**处理逻辑**:
```python
def _extract_report(raw: str) -> dict:
    # 1. 检测 HTML
    if '<!DOCTYPE html>' in raw or '<html' in raw[:200]:
        # 正则提取 <title>, <h1>, <body> 内容
        ...
    # 2. 处理 Markdown
    else:
        # 移除 --- frontmatter ---
        # 提取第一个 # 标题和日期
        ...
```

### 3. HTML 报告解析与 Wiki 渲染问题
**现象**：
1. API 返回的日报内容为空或报错。
2. Wiki SPA 页面显示的是 HTML 源码（如 `&lt;div&gt;`）而非渲染后的样式。

**根因**：
- **API 端**：cron 生成的报告是 HTML 格式，但 `_extract_report` 只处理 Markdown，导致无法提取日期和标题。
- **Wiki 端**：`publish_static_wiki.py` 的 `md_to_html` 函数检测不到无 `<!DOCTYPE>` 头的 HTML 片段（cron 报告通常被 frontmatter 包裹），对其执行了 `html.escape()`，导致标签被转义。

**修复方案**：
1. **API 端 (`api/main.py`)**：在 `_extract_report` 中增加 HTML 分支检测。
   ```python
   if '<!DOCTYPE html>' in raw or '<html' in raw[:200]:
       # 提取 title/h1 和 body 内容
       ...
   ```
2. **Wiki 端 (`wiki/helpers/publish_static_wiki.py`)**：在 `md_to_html` 开头增加对 `<div`/`<h1` 等标签的检测，直接返回原字符串。
   ```python
   stripped = markdown.strip()
   if stripped.startswith('<div') or stripped.startswith('<h1'):
       return markdown # 不转义
   ```

### 4. 常见故障排查

| 现象 | 可能原因 | 解决方案 |
|------|----------|----------|
| 接口返回 500 | `_extract_report` 解析失败 | 检查 `journalctl -u ahot-api` 查看具体报错；确认 gbrain 文件是否为空或格式损坏 |
| 注册接口报错 "Invalid HTTP request" | URL 中包含未编码的中文 | 提醒调用方对 `name` 参数进行 URL Encode |
| 盘前/复盘数据缺失 | Generator 脚本未运行或失败 | 检查 `generator/run_generators.sh` 的执行日志；手动触发生成 |

### 4. 部署与重启
```bash
# 修改代码后
systemctl daemon-reload
systemctl restart ahot-api

# 验证健康
curl http://localhost:8002/health
```

## 扩展建议
- **股票池更新**: 目前股票池数据较旧（2026-04-13），需定期手动或通过 Cron 更新 `~/wiki/entities/stock-pool.md`。
- **缓存优化**: 当前每次请求都读取文件系统，若 QPS 增加，可考虑引入简单的内存缓存（TTL 5分钟）。