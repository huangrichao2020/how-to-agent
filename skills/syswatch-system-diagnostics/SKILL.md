---
name: syswatch-system-diagnostics
description: "Hermes 原生系统健康诊断工具 — 基于 /proc 采集 + 启发式异常检测。灵感来源：github.com/matthart1983/syswatch。"
categories:
  - devops
  - system
metadata:
  requires:
    bins: []
  notes: "已集成到 hermes-agent/tools/syswatch.py，注册为 tool 'syswatch' (toolset: system)。BOOT.md 已配置重启后自检。"
---

# SysWatch 系统健康诊断

## 何时使用

- 用户询问「服务器状态如何」「有没有异常」
- Gateway 重启后自动执行（BOOT.md 流程）
- 怀疑内存泄漏、swap 压力、磁盘满、CPU 逃逸进程
- 2GB 小内存服务器的日常健康监测

## 核心能力

**数据采集**（/proc 解析，零外部依赖）：
- CPU: load average, usage % (delta-based from /proc/stat)
- Memory: total/used/available, swap used/total
- Processes: PID, name, state, RSS, cumulative CPU jiffies
- Disks: mount points, usage %, available bytes
- History: 60-sample ring buffer at 1Hz tick

**6 个启发式异常检测规则**：

| 规则 | 触发条件 | 严重度 |
|------|---------|--------|
| Swap Thrash | swap 增长 > 100MB (WARN) / > 512MB (CRIT) | WARN/CRIT |
| Runaway Process | 单进程 CPU% > 50% (WARN) / > 90% (CRIT) | WARN/CRIT |
| Disk Full | 挂载点使用率 > 85% (WARN) / > 95% (CRIT) | WARN/CRIT |
| Memory Pressure | RAM 使用率持续 > 85% (WARN) / > 95% (CRIT) | WARN/CRIT |
| High Load | load > 核心数 × 1.5 (WARN) / × 4.0 (CRIT) | WARN/CRIT |
| Zombie Party | 僵尸进程 ≥ 5 (WARN) / ≥ 25 (CRIT) | WARN/CRIT |

## 使用方法

```python
# 作为 Hermes 工具调用
syswatch(mode="insights")   # 异常检测卡片（默认）
syswatch(mode="status")     # 当前系统快照
syswatch(mode="procs")      # 进程列表（Top 15 by RSS）
```

**输出示例**：
```
⚠️ 系统检测到以下异常：

1. 🔴 **runaway process — AliYunDunMonito (pid 182421) 当前 73% CPU**
   - RSS 129.3 MB / 状态 S
   → 建议: 检查该进程是否正常，必要时 kill 或限制 CPU。

2. 🟡 **memory pressure — RAM 89% used over last 6s**
   - 已用 1.6 GB of 1.8 GB (220 MB available)
   - 持续高内存使用可能导致 swap 活动或 OOM kill。
   → 建议: 检查内存占用最高的进程，考虑清理缓存或重启服务。
```

## 技术细节

### CPU 计算（delta-based）

```python
# /proc/PID/stat 返回累计 jiffies，需要两次采样做差
prev_cum = self._prev_proc_cpu.get(pid, current_cum)
delta = current_cum - prev_cum
pct = (delta / jiffies_per_tick) * 100.0  # jiffies_per_tick = CLK_TCK * interval_secs
```

关键点：
- `CLK_TCK` 通常为 100 Hz（`os.sysconf("SC_CLK_TCK")`）
- 第一次采样是 baseline，第二次才开始有有效 delta
- 需要保存累积值（不是百分比）供下次计算

### 进程名解析

`/proc/PID/stat` 的 comm 字段用 `()` 包裹，但可能包含 `)` 本身（如 `(agent@amap/)`）。正确解析：

```python
lparen = content.index("(")
rparen = content.rindex(")")  # 找最后一个 )
name = content[lparen + 1:rparen]
rest = content[rparen + 2:].split()  # rest[0]=state, rest[1]=ppid, ...
```

### 环形历史缓冲区

```python
from collections import deque
self.cpu_history = deque(maxlen=60)  # 60 秒历史
self.swap_history = deque(maxlen=60)
```

用于检测趋势性异常（如 swap 持续增长），而非瞬时毛刺。

## 集成位置

- **文件**: `/root/hermes-agent/tools/syswatch.py`
- **注册**: `tools/syswatch.py` → `registry.register(name="syswatch", toolset="system", ...)`
- **工具集**: `toolsets.py` → `_HERMES_CORE_TOOLS` 包含 `"syswatch"`，`TOOLSETS["system"]` 定义
- **BOOT.md**: `/root/.hermes/BOOT.md` 第 93-102 行配置重启后自检

## 调试陷阱（已踩过的坑）

### 1. Python 类定义陷阱

`ProcTick` 等数据类如果只用类型注解声明属性但不定义 `__init__`，调用方 `ProcTick(pid=x, name=y)` 会静默失败（`object.__init__` 不接受关键字参数）：

```python
# ❌ 错误做法
class ProcTick:
    pid: int = 0       # 这只是在类上定义了属性
    name: str = ""
    mem_rss: int = 0

proc = ProcTick(pid=1, name="test")  # TypeError!

# ✅ 正确做法
class ProcTick:
    def __init__(self, pid=0, name="", ...):
        self.pid = pid
        self.name = name
        self.mem_rss = 0
```

### 2. 进程名解析边界

`/proc/PID/stat` 的 comm 字段用 `()` 包裹，但可能包含 `)` 本身（如 `(agent@amap/)`）。如果用 `content.split()[1].strip("()")` 会得到错误结果：

```python
# ❌ 错误
name = stat_parts[1].strip("()")  # "(agent@amap/)" → "agent@amap)" 尾部 ) 没去掉

# ✅ 正确
lparen = content.index("(")
rparen = content.rindex(")")  # 找最后一个 )
name = content[lparen + 1:rparen]
rest = content[rparen + 2:].split()
```

### 3. CPU 计算：累计值 vs 百分比

`/proc/PID/stat` 的 utime/stime 是累计 jiffies，不是当前 CPU%。需要用两次采样的差值除以 `CLK_TCK × interval_secs`：

```python
clk_tck = os.sysconf("SC_CLK_TCK")  # 通常是 100
jiffies_per_tick = clk_tck * interval_secs
delta = current_cumulative - prev_cumulative
pct = (delta / jiffies_per_tick) * 100.0
```

关键：`_prev_proc_cpu` 必须存储累积 jiffies（不是百分比），否则下一次 delta 计算会得出天文数字。

## 注意事项

1. **首次采样无数据**: 背景线程启动后需要至少 2 次采样才能计算 CPU delta。第一次调用 `syswatch` 可能显示 0% CPU，属正常现象。

2. **权限**: 读取 `/proc` 不需要 root，但某些进程的 `/proc/PID/stat` 可能因权限被跳过（PermissionError 静默忽略）。

3. **2GB 服务器适配**: 
   - Swap 8GB 是常态，swap 使用率 20-30% 不算异常
   - 内存压力阈值设为 85%/95%，比通用系统的 90%/98% 更敏感
   - 进程数通常 100-150，zombie party 阈值 5/25 合理

4. **不要重复报告**: BOOT.md 规定「如果一切正常，跳过（不在汇报中重复 '系统健康'）」，避免噪音。

## 扩展方向

- **腾讯财经实时行情**: 盘中补充实时数据（龙马量化之路架构的第二层）
- **告警推送**: CRIT 级别异常自动推送到飞书/微信
- **历史趋势图**: 导出 history ring 数据生成 sparkline