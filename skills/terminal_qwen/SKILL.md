---
name: terminal_qwen
description: Use this skill for high-risk operations that require local terminal access. Delegate dangerous commands (kill, sudo, rm -rf, restart services) to local Qwen terminal. | 用于需要本地终端访问的高危操作。将危险命令（kill、sudo、rm -rf、重启服务）委托给本地 Qwen 终端执行。
categories:
  - system
  - security
  - terminal
metadata:
  builtin_skill_version: "1.0"
  copaw:
    emoji: "🖥️"
---

# Terminal Qwen（本地终端代理）

## 什么时候用

当需要执行**高危操作**或**本地系统命令**时，使用本 skill 委托给本地终端的 Qwen 执行。

### 应该使用
- **进程管理**：kill、pkill、restart 服务
- **系统操作**：sudo、chmod、chown
- **危险删除**：rm -rf、删除重要文件
- **服务重启**：重启 CoPaw、nginx、数据库等
- **网络操作**：修改防火墙、端口转发
- **文件写入**：修改系统配置、/etc/ 目录

### 不应使用
- 普通的文件读取（用 read_file 工具）
- 普通的文件写入（用 write_file 工具）
- 普通的目录列表（用 glob_search 工具）
- 普通的代码执行（用 execute_shell_command 工具，但限于安全命令）

---

## 决策规则

1. **判断风险等级**
   - 高危命令 → 使用 terminal_qwen
   - 普通命令 → 可用 execute_shell_command

2. **高危命令定义**
   - `kill`, `pkill`, `killall`
   - `sudo`, `su`
   - `rm -rf`, `shred`
   - `chmod 777`, `chown root`
   - 修改 `/etc/`, `/usr/`, `/System/`
   - 重启服务：`systemctl restart`, `brew services restart`
   - 网络配置：`iptables`, `pfctl`, `firewall-cmd`

3. **使用前必须确认**
   - 操作目标（进程 ID、服务名、文件路径）
   - 操作后果（是否会丢失数据、中断服务）
   - 用户明确同意

---

## 使用方法

### 模式 1：委托执行（推荐）

```markdown
## 🖥️ 需要本地终端执行

我将委托本地 Qwen 终端执行以下命令：

```bash
kill 57153
```

**操作说明**：停止 CoPaw 服务（PID: 57153）

请本地 Qwen 确认并执行。
```

### 模式 2：询问后执行

```markdown
## 🖥️ 需要重启 CoPaw 服务

**高危操作确认**：
- 操作：重启 CoPaw 服务
- 影响：当前会话将中断，需要重新连接
- 命令：`kill <PID> && copaw app --host 127.0.0.1 --port 8088`

是否继续？请本地 Qwen 确认。
```

---

## 命令模板

### 重启 CoPaw

```bash
# 1. 找到进程
ps aux | grep "copaw app" | grep -v grep

# 2. 停止
kill <PID>

# 3. 重启
copaw app --host 127.0.0.1 --port 8088
```

### 停止服务

```bash
# 找到进程
ps aux | grep "<service_name>" | grep -v grep

# 停止
kill <PID>
# 或强制停止
kill -9 <PID>
```

### 删除文件

```bash
# 安全删除（可恢复）
rm <file>

# 危险删除（不可恢复）
rm -rf <directory>
```

### 修改权限

```bash
# 修改文件权限
chmod <mode> <file>

# 修改所有者（需要 sudo）
sudo chown <user>:<group> <file>
```

---

## 安全规则

### 必须确认
1. **操作目标正确** - 确认 PID、文件路径、服务名
2. **用户明确同意** - 高危操作前必须获得确认
3. **后果已说明** - 告知用户可能的影响

### 禁止操作
1. **无确认删除** - 不得直接执行 rm -rf
2. **无确认杀进程** - 不得直接 kill 关键进程
3. **修改系统配置** - /etc/ 目录修改需特别谨慎

### 最佳实践
1. **先查询后操作** - 先用 ps/list 查看，再执行
2. **提供回滚方案** - 告知用户如何恢复
3. **记录操作日志** - 说明执行了什么命令

---

## 工作流程

```
1. 识别高危操作需求
2. 判断是否需要 terminal_qwen
3. 向用户说明操作内容和风险
4. 获得用户确认
5. 委托本地 Qwen 执行
6. 确认执行结果
7. 向用户反馈
```

---

## 示例场景

### 场景 1：重启 CoPaw

**用户**：重启一下 CoPaw

**Agent**：
```markdown
## 🖥️ 需要重启 CoPaw 服务

**操作步骤**：
1. 找到 CoPaw 进程
2. 停止当前进程
3. 重新启动服务

**影响**：当前会话将中断，需要重新连接

我将委托本地 Qwen 执行以下命令：
```bash
ps aux | grep "copaw app" | grep -v grep | awk '{print $2}' | xargs kill
copaw app --host 127.0.0.1 --port 8088
```

请本地 Qwen 确认并执行。
```

### 场景 2：停止占用端口的进程

**用户**：8088 端口被占用了，帮我清理

**Agent**：
```markdown
## 🖥️ 需要清理 8088 端口

**操作步骤**：
1. 查找占用 8088 端口的进程
2. 停止该进程

**命令**：
```bash
lsof -ti:8088 | xargs kill -9
```

**影响**：当前运行的 CoPaw 服务将停止

是否继续？请本地 Qwen 确认。
```

### 场景 3：删除构建缓存

**用户**：清理一下构建缓存

**Agent**：
```markdown
## 🖥️ 需要删除构建缓存

**目标目录**：
- /Users/tingchim2pro/Desktop/CoPaw/console/dist
- /Users/tingchim2pro/Desktop/CoPaw/console/node_modules/.vite

**命令**：
```bash
rm -rf /Users/tingchim2pro/Desktop/CoPaw/console/dist
rm -rf /Users/tingchim2pro/Desktop/CoPaw/console/node_modules/.vite
```

**影响**：需要重新构建前端

是否继续？请本地 Qwen 确认。
```

---

## 与 execute_shell_command 的区别

| 特性 | execute_shell_command | terminal_qwen |
|------|----------------------|---------------|
| 风险等级 | 低 - 中 | 高 |
| 执行位置 | 当前 Agent | 本地终端 Qwen |
| 确认要求 | 工具护栏自动判断 | 必须用户确认 |
| 典型用途 | 查询、读取、简单操作 | kill、sudo、rm -rf、重启 |
| 中断风险 | 低 | 高（可能中断服务） |

---

## 错误处理

### 命令执行失败
```markdown
❌ 命令执行失败

**命令**：`kill 57153`
**错误**：No such process

**可能原因**：
- 进程已经停止
- PID 已变化

**建议**：
1. 重新查询进程：`ps aux | grep "copaw app"`
2. 确认最新 PID
3. 再次尝试
```

### 权限不足
```markdown
❌ 权限不足

**命令**：`sudo systemctl restart nginx`
**错误**：Permission denied

**解决方案**：
- 需要管理员密码
- 或使用 `sudo -i` 提升权限
```

---

## 帮助信息

```bash
# 查看帮助
copaw terminal -h

# 执行命令（需要确认）
copaw terminal exec "<command>"

# 查看历史
copaw terminal history
```

---

## 配置

在 `config.json` 中配置：

```json
{
  "skills": {
    "terminal_qwen": {
      "enabled": true,
      "confirm_before_exec": true,
      "log_all_commands": true,
      "blocked_commands": ["rm -rf /", "mkfs", "dd"]
    }
  }
}
```

---

## 注意事项

1. **本地 Qwen 必须在线** - 否则无法执行
2. **会话可能中断** - 重启服务后会话断开
3. **命令日志** - 所有执行记录在案
4. **权限限制** - 部分命令需要 sudo
5. **平台差异** - macOS/Linux/Windows 命令不同

---

## 未来扩展

- [ ] 支持命令审批流程
- [ ] 支持命令回滚
- [ ] 支持批量操作
- [ ] 支持命令模板库
- [ ] 支持执行结果验证
