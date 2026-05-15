---
name: gbrain-sync
description: "gbrain ↔ Wiki 同步机制 — 从 Postgres 导出页面到 Markdown 并自动推送到 GitHub，触发 SPA 重建。Trigger: gbrain同步/wiki同步/页面发布. Do NOT trigger for 非 gbrain 的 wiki 操作。"
version: 1.0.0
---
# gbrain 同步
## 一句话版本
gbrain → Wiki SPA 同步机制：导出页面到 Markdown → 自动 git push → 触发 publish_static_wiki.py 重建。

## 核心流程
1. `~/wiki/helpers/gbrain_sync.py` 每4小时导出 gbrain 页面到 ~/wiki/gbrain-sync/
2. 自动 git push
3. 触发 `publish_static_wiki.py` 重建 SPA pages.json
4. 页面立即可在 https://www.ai10088.com/wiki/#/page/<slug> 访问

## 配置
- Cron job_id: 05461bed8695
- 已安装 CJK 字体解决中文渲染
