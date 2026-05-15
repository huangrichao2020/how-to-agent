---
name: agent-self-evolution-ratchet
description: Automated daily skill evolution using 8-dimension scoring and ratchet mechanism. Triggers at 17:00 Beijing time daily cron, or when user requests skill optimization. Ensures skills monotonically improve — changes only kept if score increases.
trigger: Daily 17:00 cron (`0 17 * * *`), or manual request to evolve skills.
version: 1.3.0
---

# Agent Self-Evolution Ratchet

Automated daily skill evolution system. Each day, the 3 lowest-scoring skills are evaluated and improved. Changes are only kept if the score increases — the **ratchet principle**.

## Core Logic

1. **Scoring**: Run `skill_evolution.py` to score all skills on 8 dimensions (100 pts total).
2. **Selection**: Auto-select 3 lowest-scoring skills from `/root/.hermes/skills/`.
3. **Mutation**: Generate improved SKILL.md targeting weakest dimensions.
4. **Ratchet**: Score ↑ → Keep (write file + report); Score ↓/→ → Revert (discard changes).
5. **Report**: Daily report at 17:00 to Feishu. User reviews post-factum.

## 8-Dimension Scoring

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Trigger Precision | 15 | Accurate invocation, no false positives/negatives |
| Workflow Clarity | 15 | Steps unambiguous, directly executable |
| **Exception Handling** | **10** | Covers common failure scenarios with fallbacks |
| Tool Accuracy | 10 | Commands/APIs up-to-date and verified |
| Conciseness | 10 | No redundancy, token-efficient |
| **Real Performance** | **25** | **Actual success rate > Written beauty** |
| Architecture Fit | 10 | Category/refs logical, no conflicts with other skills |
| Self-Description | 5 | Trigger/Input/Output clear in frontmatter |

## Execution Steps

### Step 1: Run scoring script
```bash
python3 /root/wiki/helpers/skill_evolution.py
```

### Step 2: Read generated report
```bash
cat /root/wiki/queries/skill-evolution-daily.md
```

### Step 3: Identify lowest 3 skills, improve their SKILL.md files
- Read original SKILL.md and backup to `/tmp/skill-backup/`
- Analyze weakest dimension from scoring output
- Generate improved version targeting that dimension
- Re-score both versions to compare

### Step 4: Apply ratchet check
- If new score > original score → write improved SKILL.md, increment version
- If new score ≤ original score → discard changes, keep original

### Step 5: Publish and report
```bash
python3 ~/wiki/helpers/publish_static_wiki.py
```

**Cron**: `0 17 * * *` (Beijing time 17:00 daily)

## Exception Handling & Recovery

### Script Execution Failures

| Scenario | Symptom | Recovery |
|----------|---------|----------|
| `skill_evolution.py` crashes | Non-zero exit code, traceback in output | Check logs at `/root/wiki/helpers/`; verify Python env has required packages; retry once |
| Script timeout (>5min) | No output after extended wait | Kill process; reduce number of skills scored in one batch; check disk I/O |
| No skills found | Empty scoring list | Verify `/root/.hermes/skills/` directory exists and contains SKILL.md files |
| All skills score > 80 | No low-skill candidates | Skip evolution; report "系统健康，无需优化" |

### File Operation Errors

| Scenario | Symptom | Recovery |
|----------|---------|----------|
| SKILL.md not found | FileNotFoundError for selected skill | Remove from today's list; pick next lowest-scored skill |
| File permission denied | PermissionError on write | Check file ownership (`ls -l`); fix with `chmod` if needed |
| Concurrent modification | File changed during edit | Use file locking; re-read before writing; abort if conflict detected |
| Disk full | No space left on device | Clean old wiki artifacts; check `/tmp` and logs |

### Scoring Inconsistencies

| Scenario | Symptom | Recovery |
|----------|---------|----------|
| Score drops after improvement | New version scored lower than original | **Ratchet rule: revert immediately.** Keep original, log failure reason for next iteration |
| Identical scores | No improvement or regression | Treat as failure; revert. The skill needs a different improvement approach next time |
| Score anomaly (sudden jump >20pts) | Possible scoring bug | Flag for manual review; do not auto-commit; verify dimensions individually |

### Reporting Failures

| Scenario | Symptom | Recovery |
|----------|---------|----------|
| Feishu webhook fails | HTTP error or timeout | Retry once with 10s delay; if still failing, save report locally for next run to resend |
| Feishu API rate limited | 429 Too Many Requests | Wait 60s then retry; queue report for delayed delivery |
| Wiki publish fails | `publish_static_wiki.py` error | Report evolution results anyway; wiki publish can be retried separately |

### Safety Guards

- **Never modify files other than SKILL.md** — this skill only touches `**/SKILL.md` files
- **One skill at a time** — each modification is isolated for traceability
- **Always compare before writing** — diff original vs improved; only write if score ↑
- **Maintain version history** — increment `version` field in frontmatter when changes are kept
- **Backup before overwrite** — keep a copy of the original in `/tmp/skill-backup/` for 24h

## 示例 (Practical Examples)

### 示例 1: 改进异常处理薄弱的 Skill
```
原版: 无异常处理章节 (评分: 2/10)
改进: 添加脚本失败、文件操作错误的异常处理表和恢复步骤
结果: 异常处理评分 → 10/10, 总分 +5
```

### 示例 2: 改进工作流不清晰的 Skill
```
原版: 描述模糊，无编号步骤 (评分: 5/15)
改进: 添加编号执行步骤，附带具体命令
结果: 工作流清晰度 → 15/15, 总分 +10
```

## 避坑指南 (Pitfalls)

- ⚠️ **禁止仅凭分数编辑** — 改进后的内容必须实际上更优秀
- ⚠️ **注意不要添加填充内容** 来刷分；质量优先于数量
- ⚠️ **注意编码问题** — SKILL.md 可能包含中文字符；始终使用 `encoding='utf-8'`
- ⚠️ **避免破坏已有触发条件** — 如果 skill 有特定触发条件，保留它们
- ⚠️ **不要过度优化** — 评分 85+ 的 skill 可能无需进一步改动；聚焦最低分

## Ratchet Flowchart

```
[Start 17:00] → score_all() → sort by score
    ↓
[Pick lowest 3] → for each skill:
    ↓
read SKILL.md → identify weakest dimension → generate improved version
    ↓
score(original) vs score(improved)
    ↓
improved > original? ──YES──→ write SKILL.md → increment version → log ✅
    │
    NO
    ↓
discard changes → log ⚠️ (no improvement)
    ↓
[next skill] → ... → [all done]
    ↓
publish_wiki() → send Feishu report → [End]
```
