---
name: syswatch-integration
description: Integrate system health diagnostics into Hermes Agent using the SysWatch tool. Monitors CPU, memory, swap, disk, and processes via /proc, with heuristic anomaly detection.
categories:
  - devops
  - system-operations
metadata:
  yao_category: "AI学习"
  source: "github.com/matthart1983/syswatch (Rust TUI) → Python port"
  date: "2026-05-04"
---

# SysWatch Integration for Hermes Agent

## Overview
SysWatch is a native Hermes tool that provides system health diagnostics by monitoring `/proc` filesystem on Linux. It replaces manual `htop`/`free`/`df` checks with automated anomaly detection.

**Inspiration**: [matthart1983/syswatch](https://github.com/matthart1983/syswatch) — a Rust TUI with 12 tabs and an Insights engine. We ported the core heuristics to Python.

## Tool Usage

```python
# In Hermes agent context
result = syswatch(mode="insights")  # Returns anomaly cards or "✅ 系统健康"
result = syswatch(mode="status")    # Returns current CPU/RAM/Swap/Load summary
result = syswatch(mode="procs")     # Returns top 15 processes by RSS
```

### Response Format (Insights Mode)
```
⚠️ 系统检测到以下异常：

1. 🔴 **runaway process — python (pid 12345) 当前 95% CPU**
   - RSS 389 MB / 状态 S
   → 建议: 检查该进程是否正常，必要时 kill 或限制 CPU。

2. 🟡 **memory pressure — RAM 92% used over last 6s**
   - 已用 1.7 GB / 总计 1.8 GB (可用 150 MB)
   → 建议: 检查内存占用最高的进程，考虑清理缓存或重启服务。
```

## Heuristic Rules (6 Detectors)

| Rule | Trigger | Severity |
|------|---------|----------|
| **Swap Thrash** | Swap grows >100MB (WARN) or >512MB (CRIT) over 30s window | WARN/CRIT |
| **Runaway Process** | Single process CPU >50% (WARN) or >90% (CRIT) sustained | WARN/CRIT |
| **Disk Full** | Mount point usage >85% (WARN) or >95% (CRIT) | WARN/CRIT |
| **Memory Pressure** | RAM usage avg >85% (WARN) or >95% (CRIT) over last 6 ticks | WARN/CRIT |
| **High Load** | Load average >1.5× cores (WARN) or >4× cores (CRIT) | WARN/CRIT |
| **Zombie Party** | 5+ zombie processes (WARN) or 25+ (CRIT) | WARN/CRIT |

## Architecture

- **Collector**: Background thread sampling `/proc/meminfo`, `/proc/stat`, `/proc/loadavg`, `/proc/[pid]/stat` at 1Hz.
- **Ring Buffer**: Bounded history (60 samples) for trend detection.
- **Per-Process CPU Delta**: Tracks cumulative jiffies to compute per-tick CPU % (not instantaneous).
- **Insights Engine**: Pure functions over `(History, Snapshot)` returning sorted anomaly cards.

## File Locations

- Tool: `/root/hermes-agent/tools/syswatch.py`
- Registration: Added to `_HERMES_CORE_TOOLS` in `toolsets.py`
- Toolset: `"system"` (defined in `toolsets.py`)
- BOOT.md Integration: `/root/.hermes/BOOT.md` — runs on every Gateway restart

## When to Use

- **Gateway Restart Hook**: Automatically checks server health after restart.
- **User Query**: "服务器状态如何？" or "有没有异常？"
- **Proactive Monitoring**: Before running heavy tasks, check if swap/memory is under pressure.
- **Debugging**: When a task fails with OOM or timeout, use `syswatch(mode="procs")` to identify resource hogs.

## Pitfalls

1. **Process Name Parsing**: `/proc/PID/stat` name field can contain `)` characters (e.g., `(agent@amap/)`). Must use `rindex(")")` not `split()`.
2. **CPU Calculation**: Must track cumulative jiffies between ticks, not use raw `/proc/stat` values. First tick is baseline; subsequent ticks compute delta.
3. **Singleton Lifecycle**: The collector starts on module import. If reloading during development, ensure old threads are stopped.
4. **2GB Memory Constraint**: SysWatch itself uses <5MB. Avoid adding heavy dependencies (no pandas/numpy in the tool).

## Example: Adding to BOOT.md

```markdown
## 系统健康自检 (SysWatch)

每次重启后，使用 `syswatch` 工具快速检查服务器健康状态。

1. 调用 `syswatch(mode="status")` 获取当前 CPU/内存/swap/load 状态
2. 调用 `syswatch(mode="insights")` 运行启发式异常检测
3. 如果检测到 WARN 或 CRIT 级别的异常，在汇报中列出并建议处理措施
4. 如果一切正常，跳过（不在汇报中重复 "系统健康"）
```

## Testing

```bash
cd /root/hermes-agent && python3 -c "
from tools import syswatch as sw
import time
time.sleep(2)  # Let background thread collect
print(sw._syswatch_handler({'mode': 'insights'}))
"
```