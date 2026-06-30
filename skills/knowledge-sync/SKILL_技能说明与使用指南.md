---
name: knowledge-sync
description: Use when Hermes needs end-of-session knowledge cleanup, handoff preparation, memory/docs/skills reconciliation, stale documentation repair, or when the user says 整理一下, 同步一下, 收尾, 更新记忆, 新人能直接上手. Triggers on session end, explicit user request, or detected knowledge drift. Reconciles Hermes skills, memories, gateway facts, and related project docs against live source-of-truth state.
yao_category: "AI工作"
---

# Knowledge Sync

Inspired by the `neat-freak` pattern from `KKKKhazix/khazix-skills`, but tailored for remote Hermes. The job is to edit the knowledge system, not append logs.

## Core Rule

Be an editor, not a recorder:

- Update stale facts in place.
- Merge duplicates.
- Delete or skip completed-process clutter.
- Use absolute dates.
- Keep volatile state out of durable memory.
- Prefer live files, commands, tests, and gateway state over old notes.

## Universal Habit

Any meaningful work should leave the next agent a usable trail. This is not a
special cleanup mode; it is the default finishing habit.

- Tiny fix: update the nearest existing README, HANDBOOK, skill note, or
  troubleshooting section when future work would otherwise rediscover the same
  fact.
- Runtime or architecture change: update the operator/architecture handoff with
  paths, commands, validation, rollback, and user-visible behavior.
- Cross-machine work: use git as the source-of-truth sync path for git
  checkouts. Push from the edited checkout, pull on the other host, then sync
  only verified files into non-git live runtime directories.
- If no manual is needed, be able to say why: the change was trivial,
  self-evident, or already covered by an existing authoritative doc.

## Hermes Surfaces

Inspect only the relevant subset:

- `/root/.hermes/skills/<name>/SKILL_技能说明与使用指南.md` for reusable procedures.
- `/root/.hermes/memory` or `/root/.hermes/memories` when present.
- `/root/.hermes/gateway_state.json` for Feishu/Weixin/gateway truth.
- `/root/hermes-agent` docs/config only when the runtime repo was touched.
- GA handoff surfaces only when the work crosses GA and Hermes.

## 执行步骤 (Workflow)

### Step 1: 盘点 (Inventory)
1. 列出所有待检查的候选文件，确认其存在和可访问性。
2. 使用 `rg` 或 `grep` 快速扫描是否有过期引用、失效路径。
3. 记录当前 gateway_state.json 和 memory 文件的状态快照。

### Step 2: 映射影响 (Map Impact)
1. **新命令/工具** → 更新对应 skill/runbook。
2. **运行时行为变更** → 更新架构或 operator 文档。
3. **集成行为变更** → 更新集成文档和故障排除指南。
4. **持久化经验教训** → 归档到 curated memory 或 skill，不写入原始日志。
5. **完成一件可复用的事** → 更新工作手册或交接手册，让下次不用重新摸索。

### Step 3: 编辑 (Edit)
1. **先编辑文档**，再编辑 agent 指令，最后更新 memory。
2. 对每个改动：确认源文件存在、路径正确、命令可执行。
3. 合并重复内容，删除过时信息。

### Step 4: 验证 (Verify)
1. 使用 `rg` 验证引用是否存在。
2. 使用 `test -f` 检查文件存在性。
3. 读取 live state（如 gateway_state.json）确认一致性。
4. 报告已修改文件、验证结果、以及故意保留不变的内容。

## 示例 (Examples)

### 示例 1: 更新过期路径
```
原版记忆: "日志位于 /tmp/app.log"
实际检查: 日志已迁移到 /var/log/hermes/app.log
更新: 原地修改为正确路径，删除旧引用
```

### 示例 2: 合并重复 Skill
```
发现: a-stock-market-analysis-framework 和 stock/stock-monitoring-automation 有重叠内容
操作: 保留更完整的版本，在另一个中添加交叉引用
```

### 示例 3: 清理临时状态
```
memory 中包含: "PID 12345 正在运行"
操作: 删除该条目 — 进程状态是瞬时信息，不应写入持久 memory
```

## 避坑指南 (Pitfalls)

- ⚠️ **禁止**将密钥、token、PID、临时路径或瞬时状态写入 memory
- ⚠️ **注意**不要把 memory 变成按时间排序的任务日志
- ⚠️ **注意**除非用户明确要求，否则不要在清理过程中重启 Hermes
- ⚠️ **注意**编辑前先备份 — 如果改动导致问题，可以快速回滚
- ⚠️ **禁止**删除仍在被其他 skill 引用的文件

## 异常处理 (Error Handling)

| 场景 | 症状 | 恢复方案 |
|------|------|----------|
| memory 目录不存在 | FileNotFoundError | 跳过 memory 步骤，继续其他表面的同步 |
| gateway_state.json 损坏 | JSON parse error | 尝试从备份恢复；若无法恢复，跳过该表面并报告 |
| 文件被锁定 | Permission denied | 跳过该文件，记录到报告，等待下次同步重试 |
| 同步过程中 skill 被修改 | 并发冲突 | 使用文件时间戳检测冲突；冲突时保留较新版本，记录冲突 |
| rg/grep 超时 (>30s) | 扫描无响应 | 限制扫描深度 `--max-depth`；减少搜索范围 |
| 回滚失败 | 备份文件也不存在 | 标记为需要人工介入；创建 issue 或报告给下次运行 |

## Do Not

- Do not write secrets, tokens, PIDs, temporary paths, or transient statuses to memory.
- Do not turn memory into a chronological task log.
- Do not restart Hermes as part of cleanup unless the user asked or the changed surface requires it.
- Do not use rsync/scp as the primary synchronization path between two git
  checkouts that share a GitHub remote. Use git first; use file sync only for
  live runtime trees or emergency recovery.
