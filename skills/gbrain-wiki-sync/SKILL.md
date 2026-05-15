---
name: gbrain-wiki-sync
description: "gbrain → Wiki 同步机制：从 Postgres 导出页面到 Markdown 并自动推送到 GitHub"
version: 1.0.0
created: 2026-04-30
tags: [gbrain, wiki, sync, backup, cron]
---

# GBrain → Wiki 同步

将 gbrain 数据库（Postgres）中的所有页面增量同步到 `~/wiki/gbrain-sync/` 目录，并自动 git commit + push。

## 触发条件

- 定时任务：每 4 小时运行一次（cron job_id: `05461bed8695`）
- 手动请求："同步 gbrain 到 wiki"、"备份 gbrain 数据"

## 核心流程

### 1. 脚本位置

```bash
python3 ~/wiki/helpers/gbrain_sync.py
```

### 2. 工作原理

1. **读取配置**：从 `~/.gbrain/config.json` 获取 Postgres 连接串
2. **JSON 输出**：使用 `SELECT json_agg(row_to_json(t)) FROM (...) t` 避免分隔符冲突（compiled_truth 中可能包含 `|||`）
3. **增量同步**：基于 `content_hash` 比对，无变更跳过 git
4. **清理逻辑**：gbrain 中删除的页面会自动从 sync 目录移除
5. **Git 自动化**：自动 add/commit/push，commit msg 含日期和变更数

**关键实现细节**：
- 不使用 `|||` 分隔符（内容中可能出现导致解析错误）
- `.sync_state.json` 记录上次同步的 hash，已加入 `.gitignore`
- 支持 `--dry-run` 预览和 `--skip-git` 只导出
2. **获取页面**：通过 `psql` 执行 SQL 查询，以 JSON 格式返回所有页面（slug, type, title, content_hash, compiled_truth, frontmatter, timeline, updated_at）
3. **增量检测**：对比本地 `.sync_state.json` 中的 content_hash，只导出有变更的页面
4. **文件生成**：为每个页面生成 Markdown 文件，路径为 `gbrain-sync/{slug}.md`，包含 frontmatter 和正文
5. **Git 操作**：如果有变更，执行 `git add -A && git commit && git push`
6. **状态保存**：更新 `.sync_state.json` 记录最新哈希

### 3. 输出结构

```
~/wiki/gbrain-sync/
├── .sync_state.json          # 上次同步的内容哈希映射
├── index.md                  # 索引页
├── entities/
│   ├── hermes-agent.md
│   └── ...
├── concepts/
│   ├── darwin-skill.md
│   └── ...
├── queries/
│   └── wiki-learning-workflow.md
└── ...
```

### 4. 参数

| 参数 | 说明 |
|------|------|
| `--dry-run` | 只预览变更，不写入文件 |
| `--skip-git` | 只导出文件，不执行 git 操作 |

## 关键设计决策

### 为什么用 psql + JSON 而不是 Python ORM？

- **零依赖**：不需要安装 psycopg2 或 SQLAlchemy
- **轻量**：服务器只有 2GB RAM，避免重型库
- **可靠**：psql 是系统自带工具，稳定性高

### 为什么用 content_hash 做增量？

- gbrain 的 `content_hash` 字段在每次页面内容变更时自动更新
- 比对哈希比比对全文快得多
- 避免不必要的 git commit

### 为什么单独存 .sync_state.json？

- 跟踪哪些页面已同步过
- 检测已删除的页面（gbrain 中不存在但 sync 目录有的），自动清理
- 不污染 git 历史（已加入 .gitignore）

## 故障排查

### psql 连接失败

检查 `~/.gbrain/config.json` 中的 `database_url` 是否正确：
```json
{
  "engine": "postgres",
  "database_url": "postgresql://gbrain:PASSWORD@127.0.0.1:5432/gbrain"
}
```

### Git push 失败

检查网络连接和 SSH key 配置：
```bash
cd ~/wiki && git remote -v  # 应显示 git@github.com:...
ssh -T git@github.com       # 测试连通性
```

### 页面内容为空

检查 gbrain 数据库中是否有数据：
```bash
psql "DATABASE_URL" -c "SELECT count(*) FROM pages"
```

## Cron 任务

当前配置：每 4 小时运行一次
```
job_id: 05461bed8695
schedule: every 240m
```

查看状态：
```bash
hermes cron list | grep gbrain
```

## 相关

- [[wiki-learning-workflow]] — Wiki 学习工作流
- [[gbrain]] — GBrain 知识图谱引擎