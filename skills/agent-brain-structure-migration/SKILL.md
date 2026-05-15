---
name: agent-brain-structure-migration
description: Migrate Hermes Agent memory system to agentic-stack compatible .agent/ structure. Phase 1 (bridge) + Phase 2 (Dream Cycle). Preserves legacy MEMORY.md/USER.md while building parallel episodic/candidate/lessons pipeline.
category: architecture
triggers:
  - ".agent structure"
  - "agentic-stack migration"
  - "Dream Cycle setup"
  - "episodic memory clustering"
  - "memory bridge"
yao_category: "AI学习"
---

# Agent Brain Structure Migration (.agent/)

## Overview
Migrates Hermes Agent's flat `MEMORY.md` / `USER.md` system to the portable `.agent/` hierarchy used by agentic-stack. Enables cross-harness compatibility (Claude Code, Cursor, etc.) and automatic experience提炼 via Dream Cycle.

## Directory Structure
```
~/.hermes/.agent/
├── AGENTS.md                  # Entry guide
├── harness/                   # Shared utilities
│   ├── text.py               # word_set(), jaccard()
│   └── salience.py           # salience_score()
├── memory/
│   ├── personal/PREFERENCES.md  # ← USER.md mapped
│   ├── working/WORKSPACE.md     # Current task state
│   ├── working/REVIEW_QUEUE.md  # Pending candidates
│   ├── semantic/LESSONS.md      # ← MEMORY.md mapped + auto-promoted
│   ├── semantic/lessons.jsonl   # Structured source of truth
│   ├── semantic/DECISIONS.md    # Architectural decisions
│   ├── episodic/AGENT_LEARNINGS.jsonl  # Raw log (append-only)
│   ├── candidates/              # Staged patterns awaiting review
│   ├── auto_dream.py            # Main Dream Cycle entry
│   ├── cluster.py               # Jaccard clustering
│   ├── promote.py               # Pattern extraction + staging
│   ├── validate.py              # Heuristic prefilter
│   ├── review_state.py          # Lifecycle management
│   ├── decay.py                 # Archive old entries
│   ├── archive.py               # Archive stale workspace
│   ├── render_lessons.py        # LESSONS.md renderer
│   └── _episodic_io.py          # append_episode() helper
├── tools/
│   ├── show.py                  # Dashboard
│   └── list_candidates.py       # List staged candidates
└── helpers/
    ├── memory_bridge.py         # Legacy → .agent sync
    └── episodic_io.py           # Import wrapper
```

## Phase 1: Bridge Setup (One-time)
1. **Create directories**: All paths under `~/.hermes/.agent/`
2. **Map legacy content**:
   - `USER.md` (§-delimited) → `memory/personal/PREFERENCES.md`
   - `MEMORY.md` (§-delimited) → `memory/semantic/LESSONS.md` + `lessons.jsonl`
3. **Install bridge script**: `~/.hermes/helpers/memory_bridge.py`
4. **Cron sync**: Every 30 min, `python3 ~/.hermes/helpers/memory_bridge.py --to-agent`

## Phase 2: Dream Cycle Activation
1. **Copy core modules** from agentic-stack:
   - `harness/text.py`, `harness/salience.py`
   - `memory/cluster.py`, `promote.py`, `validate.py`, `review_state.py`
   - `memory/decay.py`, `archive.py`, `render_lessons.py`, `auto_dream.py`
   - `memory/_episodic_io.py`
2. **Fix regex escaping**: Ensure `\w\s` not `\\w\\s` in cluster.py and validate.py
3. **Fix newline handling**: Use `NL = chr(10)` in all write operations to avoid literal `\n` in output
4. **Test with sample data**: Write 8+ English episodes with overlapping vocabulary to verify clustering
5. **Cron activation**: `0 */4 * * * cd ~/.hermes/.agent/memory && python3 auto_dream.py`

## Key Pitfalls
- **Regex double-escaping**: When writing Python files via `write_file`, raw strings like `r"[^\w\s]"` become `"[^\\w\\s]"`. Must manually ensure single backslashes in final file.
- **Newline literals**: `"\n".join()` inside triple-quoted strings written by `write_file` produces literal `\n` characters. Solution: use `NL = chr(10)` constant.
- **Jaccard threshold**: Default 0.3 is too high for natural language. Clusters only form when entries share 30%+ of content words. Test with 6-8 related entries first.
- **sys import missing**: `auto_dream.py` needs `import sys` at top for `sys.path.insert()`.
- **Episodic lock**: `_episodic_locked()` uses `fcntl.LOCK_EX` — blocks concurrent appends during Dream Cycle read-modify-write window.
- **Plugin opt-in**: User plugins (like `episodic-logger`) require explicit entry in `plugins.enabled` in config.yaml. Bundled plugins auto-load; user plugins don't.

## 异常处理与故障排查 (Error Handling & Troubleshooting)

**迁移失败时的 fallback 策略：**
- **Bridge sync 失败/错误** → 如果 `memory_bridge.py --to-agent` 运行失败，检查源文件 `MEMORY.md` / `USER.md` 是否存在且格式正确（§ 分隔符）。如果解析失败，回滚到手动复制模式。
- **Dream Cycle 超时** → `auto_dream.py` 处理大量 episodes 时可能超时。设置 cron timeout 为 300 秒。如果超时，减少单次处理的 episode 数量或使用 `--limit` 参数分批处理。
- **聚类结果为空** → Jaccard 阈值 0.3 对中文/混合语言可能过高。降至 0.15-0.2 重试。验证输入数据至少包含 6-8 条相关条目。
- **JSONL 文件损坏/并发写入失败** → `_episodic_locked()` 使用文件锁防止并发写入。如果出现 `IOError: [Errno 11]`，等待 2-3 秒后重试。不要删除锁文件。
- **Gateway cutover 后回滚** → 如果 `.agent/` 数据不完整或 recall parity 检查失败，立即切回 `MEMORY.md` / `USER.md`。确保 rollback path 在 cutover 前已验证。

**注意 / 避坑事项：**
- ⚠️ **禁止在未完成 recall parity 验证前切换 gateway** — 这是最严重的错误场景。必须确认 `.agent/` 能恢复所有重要偏好和约束。
- ⚠️ **regex 双转义** 是最常见的 write_file 陷阱。写入 Python 文件时，使用 `replace('\\\\', '\\')` 或 `chr(92)` 来确保单反斜杠。
- ⚠️ **Dream Cycle 需要真实生产数据** — 仅用合成测试数据无法验证聚类质量。等待至少 1-2 周的真实 episodic 积累。
- ⚠️ **migration_readiness.py 脚本如果被阻塞**，检查 `~/.hermes/.agent/migration/` 目录是否存在，以及是否有写入权限。

## 示例 (Examples)

**示例 1：Bridge sync 验证**
```bash
# 步骤 1: 运行 bridge sync
python3 ~/.hermes/helpers/memory_bridge.py --to-agent

# 步骤 2: 验证输出
cat ~/.hermes/.agent/memory/semantic/LESSONS.md | head -20

# 步骤 3: 检查 episode 计数
python3 ~/.hermes/.agent/tools/show.py
```

**示例 2：Dream Cycle 测试**
```bash
# 步骤 1: 写入测试 episodes (至少 8 条)
# 步骤 2: 运行 Dream Cycle
cd ~/.hermes/.agent/memory && python3 auto_dream.py

# 步骤 3: 检查聚类结果
python3 tools/list_candidates.py

# 步骤 4: 如果无聚类结果，降低阈值重试
```

## Phase 3: Episodic Auto-Logging (Completed)
1. **Create plugin** at `~/.hermes/plugins/episodic-logger/`:
   - `plugin.yaml`: declares `post_tool_call` hook
   - `__init__.py`: registers `_on_post_tool_call` that calls `_episodic_io.append_episode()`
2. **Enable plugin** in `~/.hermes/config.yaml`:
   ```yaml
   plugins:
     enabled:
       - episodic-logger
   ```
3. **Restart Gateway**: `systemctl restart hermes-gateway`
4. **Verify**: Check `AGENT_LEARNINGS.jsonl` grows after tool calls (currently logging raw tool names, lacks semantic reflection)

## Phase 4: Context Budget (Query-Aware Injection) - Completed
1. **Created** `harness/context_budget.py`:
   - `_top_episodes(query, k=5)`: scores episodes by `salience * relevance`
   - `_top_lessons(query, budget)`: ranks lessons by word overlap
   - `build_context(query, budget=12000)`: assembles always-on + dynamic sections
2. **Verified**: Lessons layer works correctly (e.g., "GitHub push" → SSH lesson). Episodes layer weak due to low-quality reflection data.
3. **Next**: Enhance episodic-logger to extract meaningful reflection from tool results before integrating into gateway.

## Episodic Logging Usage
```python
from hermes_episodic import append_episode

# After any significant action
append_episode(
    action="browser_navigate",
    outcome="Loaded douyin page",
    detail="Extracted content via vision OCR",
    success=True,
    importance=7,
    skill="douyin-extraction",
    reflection="Douyin requires vision mode, DOM extraction fails"
)
```

## Verification
- `python3 ~/.hermes/.agent/tools/show.py` — shows episode count, candidate count
- `python3 ~/.hermes/.agent/tools/list_candidates.py` — lists staged patterns
- `cat ~/.hermes/.agent/memory/working/REVIEW_QUEUE.md` — human-readable queue
- `python3 ~/.hermes/.agent/tools/migration_readiness.py` — blocks premature gateway cutover

## Migration Timeline
- Week 1: Bridge active, Dream Cycle accumulating data (read-only)
- Week 2: Validate context budget injection and recall parity side-by-side
- Week 3+: Switch gateway to read from `.agent/` only after readiness gates pass and the user explicitly approves
- Archive legacy files only after a rollback drill succeeds

## Cutover Gates

Do not switch gateway memory reads to `.agent/` just because the bridge has run for one week. The one-week mark is only an inspection point.

Required gates:
1. `memory_bridge.py --to-agent` is running and synced.
2. `auto_dream.py` is running on cron and has real production episodes, not only synthetic test data.
3. Review queue is empty, or every pending candidate has an explicit defer/reject decision.
4. Side-by-side recall comparison shows `.agent/` can recover the same important preferences, constraints, and procedures as legacy memory. Record comparisons in `~/.hermes/.agent/migration/recall_parity.jsonl`.
5. Gateway has a config flag or rollback path to return to MEMORY.md / USER.md immediately.
6. User approval is explicit in the active session.
