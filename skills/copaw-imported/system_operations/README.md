# 系统操作技能使用说明

## 技能位置
```
/Users/tingchim2pro/.copaw/workspaces/default/skills/system_operations/
```

## 文件结构
```
system_operations/
├── SKILL.md           # 技能说明文档
├── system_ops.sh      # 执行脚本
└── README.md          # 本文件
```

## 使用方法

### 方法一：直接运行脚本
```bash
cd /Users/tingchim2pro/.copaw/workspaces/default/skills/system_operations
./system_ops.sh
```

### 方法二：通过 CoPaw Agent 调用
让 Agent 执行以下命令：
- 重启：`execute_shell_command` with `sudo shutdown -r now`
- 关机：`execute_shell_command` with `sudo shutdown -h now`
- 查看状态：`execute_shell_command` with `uptime` 或 `uname -a`

### 方法三：单命令执行
```bash
# 重启
sudo shutdown -r now

# 关机
sudo shutdown -h now

# 查看运行时间
uptime

# 查看系统信息
uname -a
```

## 安全确认流程

执行高危操作前，脚本会：
1. 显示红色警告信息
2. 要求用户输入 "yes" 进行确认
3. 只有确认后才执行操作

## 注意事项

⚠️ **重要提示**：
1. 需要管理员权限（sudo），可能需要输入密码
2. 重启/关机前请保存所有未保存的工作
3. 确认没有其他用户正在使用系统
4. 建议在非工作时间执行重启操作

## 测试建议

首次使用前，建议先执行以下命令测试：
```bash
# 测试权限
sudo -v

# 查看系统状态（无风险）
uptime
who
```

## 故障排除

### 权限问题
如果提示权限不足，请确保：
- 当前用户有 sudo 权限
- 已正确输入管理员密码

### 脚本无法执行
```bash
# 添加执行权限
chmod +x system_ops.sh
```
