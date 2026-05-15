---
name: cron-output-to-wiki-persistence
description: 将定时任务（cron job）的输出自动持久化到 gbrain 和 Wiki SPA，确保跨会话可检索、网页可访问。
version: 1.0.0
author: Hermes Agent
license: Private
---

# Cron Output to Wiki Persistence

当用户要求"定时任务消息加入当前会话"或"cron 输出持久化"时使用本技能。

## 核心问题

Cron job 在独立 session 运行，输出推送到飞书后，主会话的对话历史**不会自动同步**。用户问"今天学了什么"时，agent 不知道 cron 刚发了什么。

## 解决方案架构

```
cron job 运行
    ├─ 生成报告内容
    ├─ mcp_gbrain_put_page → 写入 gbrain 页面（长期记忆）
    └─ 发送飞书/其他渠道（用户手机看到）
         ↓
gbrain_sync.py (每4小时 cron)
    ├─ Postgres → ~/wiki/gbrain-sync/*.md
    └─ 自动触发 publish_static_wiki.py → 重建 pages.json + index.html
         ↓
Wiki SPA 自动包含 gbrain-sync 页面
    → 任何会话可通过 mcp_gbrain_query 检索
    → 网页端 https://www.ai10088.com/wiki/#/page/<slug> 可访问
```

## 实施步骤

### Step 1: Cron Job Prompt 更新

在 cron job prompt 中加入"必须执行：写入 gbrain 长期记忆"指令：

```markdown
**必须执行：写入 gbrain 长期记忆**
在发送飞书报告之前，使用 mcp_gbrain_put_page 将本次日报写入 gbrain 页面 'cron-daily-learning-brief'：
1. 先用 mcp_gbrain_get_page 读取现有内容
2. 在现有内容顶部追加新条目
3. 只保留最近 7 天的条目，删除更早的
4. 写入完成后再发送飞书报告
```

### Step 2: gbrain_sync.py 自动化

`~/wiki/helpers/gbrain_sync.py` 末尾已添加自动触发 wiki 重建：

```python
# 始终触发 Wiki SPA 重建，让 gbrain 页面自动出现在网页上
publish_script = WIKI_DIR / "helpers" / "publish_static_wiki.py"
if publish_script.exists():
    result = subprocess.run(
        [sys.executable, str(publish_script)],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        print(f"  wiki 重建: {result.stdout.strip()}")
```

### Step 3: 验证

```bash
# 手动触发一次同步
python3 ~/wiki/helpers/gbrain_sync.py

# 检查 gbrain 页面是否在 wiki SPA 中
python3 -c "
import json
data = json.load(open('/www/wwwroot/www.ai10088.com/wiki/pages.json'))
gbrain = [p for p in data if p['section'] == 'gbrain-sync']
print(f'gbrain-sync pages: {len(gbrain)}')
"
```

## 关键设计决策

| 决策 | 理由 |
|------|------|
| **用 gbrain 而非直接写 wiki markdown** | gbrain 有版本控制、content_hash、自动去重；wiki 只是静态展示层 |
| **gbrain_sync 自动触发 wiki 重建** | 避免手动操作，确保 gbrain 页面一出现就在网页上可见 |
| **不修改 gateway hooks** | 最初尝试过 `agent:start` hook 扫描 cron 输出文件，太笨重；gbrain 方案更干净 |
| **program.md 范式分离指令与执行** | cron job prompt 读取 `/root/.hermes/programs/*.md`，改指令不用动 cron 配置 |

## 相关文件

- Cron job: `~/.hermes/cron/jobs.json`（通过 `cronjob` 工具管理）
- gbrain sync: `~/wiki/helpers/gbrain_sync.py`
- Wiki publish: `~/wiki/helpers/publish_static_wiki.py`
- Program files: `/root/.hermes/programs/*.md`

## 注意事项

- gbrain 页面类型建议用 `type: archive`（归档类）或 `type: research`（调研类）
- Wiki SPA 有 basic auth 保护，需要 huangrichao 账号密码
- `publish_static_wiki.py` 用 `rglob('*.md')` 扫整个 `~/wiki/`，gbrain-sync 目录自动被包含