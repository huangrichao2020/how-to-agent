# system_operations - 系统操作技能

## 功能说明
本技能用于执行系统级别的操作，包括高危操作（重启、关机）和系统状态查询。所有操作均通过本地终端执行。

## 使用场景
- 系统重启 / 关机
- 查看系统状态（运行时间、负载、磁盘、内存）
- 检查当前是否有其他用户/进程在运行

## 安全提示
⚠️ **高危操作警告**：重启和关机将终止所有运行中的进程，未保存数据将丢失！
- 执行前必须确认：无其他用户在线、无关键任务运行、数据已保存
- 建议通过 `who` 和 `ps aux` 先检查系统状态
- 高危操作前必须进行二次确认

## 执行流程（含安全检查）

### Step 1: 系统状态预检
在执行任何高危操作前，先运行以下检查：
```bash
# 检查当前登录用户
who

# 检查系统负载
uptime

# 检查磁盘空间
df -h /

# 检查内存使用
free -h

# 检查关键后台进程（示例：数据库、web服务器）
ps aux | grep -E "(nginx|mysql|postgres|redis)" | grep -v grep
```

### Step 2: 用户确认
向用户展示预检结果，并请求二次确认：
> ⚠️ 即将执行 [重启/关机] 操作。当前系统状态：[summary]。确认继续？

### Step 3: 执行操作
用户确认后执行对应命令（见下方命令表）。

### Step 4: 结果验证
- 命令成功：返回执行结果
- 命令失败：记录错误信息，尝试替代方案（见异常处理）

## 支持的操作命令

| 操作 | Linux 命令 | macOS 命令 | 说明 |
|------|-----------|-----------|------|
| 重启 | `sudo shutdown -r now` | `sudo shutdown -r now` | 立即重启 |
| 延迟重启 | `sudo shutdown -r +5 "Scheduled restart"` | 同左 | 5分钟后重启，给用户保存时间 |
| 关机 | `sudo shutdown -h now` | `sudo shutdown -h now` | 立即关机 |
| 取消关机 | `sudo shutdown -c` | `sudo shutdown -c` | 取消已计划的关机/重启 |
| 查看系统信息 | `uname -a` | `uname -a` | 内核版本、架构等 |
| 查看运行时间 | `uptime` | `uptime` | 运行时长、负载 |
| 查看登录用户 | `who` | `who` | 当前在线用户 |
| 查看磁盘 | `df -h` | `df -h` | 磁盘使用情况 |
| 查看内存 | `free -h` | `vm_stat` | 内存使用情况 |

## 异常处理

### 常见错误及应对策略

| 错误场景 | 可能原因 | 应对策略 |
|---------|---------|---------|
| `sudo: command not found` | 未安装 sudo 或非 sudoers | 切换 root 用户：`su -`，或提示用户配置 sudoers |
| `shutdown: Not owner` | 权限不足 | 检查当前用户：`whoami`，确认 sudo 权限 |
| 命令执行超时 | 系统卡死 | 使用 `timeout 10 command` 包装，超时后尝试 `sudo reboot -f`（强制重启） |
| 有其他用户在线 | 多人环境 | 通过 `wall "System will restart in 5 minutes"` 广播通知 |
| 关键进程未关闭 | 服务未优雅停止 | 先 `systemctl stop <service>` 停止服务，再执行重启 |

### 降级方案
如果标准 `shutdown` 命令不可用：
```bash
# 备选重启方案（按安全程度排序）
sudo systemctl reboot          # 方式1：systemd（推荐）
sudo reboot                     # 方式2：直接 reboot
sudo reboot -f                  # 方式3：强制重启（不优雅停止服务）
echo 1 | sudo tee /proc/sys/kernel/sysrq && echo b | sudo tee /proc/sysrq-trigger  # 方式4：内核级（最后手段）
```

### 取消操作
如果用户反悔或发现异常：
```bash
sudo shutdown -c   # 取消已计划的关机/重启
```

## 注意事项
- 本技能需要管理员权限（sudo）
- 生产环境建议设置维护窗口，避免业务高峰期操作
- 所有高危操作应在操作日志中记录（时间、操作人、原因）
- 虚拟化/容器环境中，优先通过管理平台操作而非直接系统命令
