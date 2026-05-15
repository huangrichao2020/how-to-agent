---
name: cron-gbrain-persistence
description: 将 Hermes Agent cron job 的输出自动持久化到 gbrain，实现跨会话检索和 wiki SPA 自动同步。
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Cron Job → Gbrain 持久化工作流

当用户要求"定时任务输出加入当前会话"或"冷启动后知道之前 cron 发了什么"时使用本技能。

## 核心问题
Cron job 在独立 session 运行，输出推送到飞书/短信后，主会话的对话历史**不会自动同步**。重启 Gateway 或新开 session 时，agent 不知道 cron 刚发了什么。

## 解决方案架构

```
cron job 运行
    ├─ 生成报告内容
    ├─ mcp_gbrain_put_page → 写入 gbrain 页面（长期记忆）
    └─ 发送飞书/短信（用户手机看到）
         ↓
任何会话中：mcp_gbrain_query("关键词") → 检索到所有历史输出
         ↓
gbrain_sync.py (每4小时) → 导出到 ~/wiki/gbrain-sync/
         ↓
publish_static_wiki.py → 重建 pages.json + index.html
         ↓
Wiki SPA 自动包含新页面（section: gbrain-sync）
```

## 实施步骤

### 1. 创建 gbrain 归档页面
使用 `mcp_gbrain_put_page` 创建一个类型为 `archive` 的页面，用于累积 cron 输出。

```python
mcp_gbrain_put_page(
    slug="cron-daily-learning-brief",
    content="""---
title: Cron 每日学习日报归档
type: archive
tags: [cron, learning-brief]
---

# Cron 每日学习日报归档

定时任务输出的长期记忆归档。
"""
)
```

### 2. 更新 Cron Job Prompt
在 cron job prompt 中加入"必须执行：写入 gbrain"指令。

```markdown
**必须执行：写入 gbrain 长期记忆**
在发送飞书报告之前，使用 mcp_gbrain_put_page 将本次日报写入 gbrain 页面 'cron-daily-learning-brief'：
1. 先用 mcp_gbrain_get_page 读取现有内容
2. 在现有内容顶部追加新条目
3. 只保留最近 7 天的条目，删除更早的
4. 写入完成后再发送飞书报告
```

### 3. 配置 gbrain → Wiki 自动化
修改 `~/wiki/helpers/gbrain_sync.py`，在同步完成后自动触发 wiki 重建：

```python
# 在 sync() 函数末尾添加
publish_script = WIKI_DIR / "helpers" / "publish_static_wiki.py"
if publish_script.exists():
    subprocess.run([sys.executable, str(publish_script)], capture_output=True, text=True, timeout=30)
```

### 4. 安装 CJK 字体（服务器环境）
确保 headless Chromium 能正确渲染中文：

```bash
yum install -y google-noto-sans-cjk-ttc-fonts \
               google-noto-serif-cjk-ttc-fonts \
               wqy-microhei-fonts
fc-cache -fv
```

## Active-Run Steering（运行时干预）

如果需要让 cron job 在运行中接收外部指令，使用 **gbrain 干预队列**模式：

1. 创建干预队列页面 `cron-intervention-queue`
2. 在 cron prompt 中加入"检查干预指令"步骤
3. 用户通过修改 gbrain 页面发送指令
4. Cron job 读取并执行，完成后更新 status

这比修改 agent loop 加 inbox 机制更轻量，纯 prompt 层实现。

## 验证清单

- [ ] gbrain 页面可被 `mcp_gbrain_query` 检索到
- [ ] gbrain_sync.py 每4小时自动运行（cron job_id 记录）
- [ ] Wiki SPA 页面可通过 `https://domain/wiki/#/page/<slug>` 访问
- [ ] 中文字符无豆腐块（fc-list :lang=zh 有输出）

## 常见陷阱

1. **不要写 hook 扫描文件** — 最初尝试在 gateway 加 `agent:start` hook 扫描 cron 输出目录，太笨重且增加每次请求延迟。gbrain 持久化是正解。
2. **gbrain 页面格式** — 必须用 `mcp_gbrain_put_page` 写入，不要用 `write_file` 直接改 Postgres 数据。
3. **Wiki 重建时机** — 必须在 gbrain_sync 完成后立即触发，否则新页面要等下次同步才出现。
4. **重复页面** — 手动复制 gbrain 页面到 wiki queries/ 会导致重复，应依赖 gbrain-sync 自动同步。

## 相关技能

- `gbrain-wiki-sync`: gbrain → Wiki 同步机制
- `agent-brain-structure-migration`: .agent/ 内存架构迁移