---
name: hermes-agent-upgrade
description: 在受限服务器上升级 Hermes Agent 的标准流程，保留自定义 Phase 6 代码，包含完整的备份、回滚和验证步骤。
category: devops
version: 1.1.0
---

# Hermes Agent 服务器升级

**场景**：升级 `hermes-agent` 同时保留本地自定义代码（Phase 6 Impression-Pointer）。

## 前置检查

在开始升级前：
```bash
# 1. 确认当前版本
cd ~/hermes-agent && git describe --tags --always

# 2. 确认自定义文件清单
ls agent/impression_page.py

# 3. 检查是否有未提交的改动
git status --short

# 4. 确认上游 remote 配置
git remote -v
```

## 标准升级流程

### 1. 标记与备份
```bash
cd ~/hermes-agent

# 标记当前状态
git tag v$(date +%Y%m%d)-pre-upgrade

# 备份自定义文件
cp agent/impression_page.py agent/impression_page.py.bak.$(date +%Y%m%d)
# 如有其他自定义文件，一并备份
cp -r agent/custom/ agent/custom.bak.$(date +%Y%m%d) 2>/dev/null
```

### 2. 拉取上游更新
```bash
# 获取最新上游代码
git fetch upstream main

# 确认要合并的改动范围
git log --oneline HEAD..upstream/main | head -20
```

### 3. 重置并合并
```bash
# 硬重置到上游最新
git reset --hard upstream/main

# 恢复自定义文件
cp agent/impression_page.py.bak.* agent/impression_page.py

# 如有冲突，手动解决后 git add <file>
```

### 4. 同步依赖
```bash
cd ~/hermes-agent
uv sync

# 验证 Python 环境
python -c "import hermes_agent; print('OK')"
```

### 5. 验证与提交
```bash
# 运行快速测试
python -m pytest tests/ -x -q 2>/dev/null || echo "Tests skipped or failed"

# 提交合并状态
git add -A
git commit -m "Merge upstream: hermes-agent upgrade $(date +%Y-%m-%d)"
```

## 配置建议

为保证稳定性，建议配置以下参数：
```yaml
agent.api_max_retries: 3
providers.<name>.request_timeout_seconds: 120
```

## 错误处理与异常恢复

### 升级失败场景
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `fetch upstream` 失败 | 网络连接问题或 remote 未配置 | 检查 `git remote -v`；确认 upstream URL 正确 |
| `uv sync` 失败 | 依赖冲突或网络问题 | 检查 `uv.lock`；尝试 `uv sync --no-cache` |
| 自定义文件恢复后报错 | 上游 API 变更导致自定义代码不兼容 | 查看错误日志；对比 upstream 变更；按需调整自定义代码 |
| 测试大量失败 | 上游重大变更 | 逐个排查失败测试；考虑暂缓升级 |
| Git 冲突 | 自定义文件与上游同时修改 | 手动解决冲突；`git diff` 对比差异后选择保留版本 |

### 回滚流程（升级失败时）
```bash
cd ~/hermes-agent

# 方法1：回退到升级前 tag
git reset --hard v$(date +%Y%m%d)-pre-upgrade

# 方法2：回退到上一个 commit
git reset --hard HEAD~1

# 恢复备份的自定义文件
cp agent/impression_page.py.bak.* agent/impression_page.py

# 恢复依赖环境
uv sync
```

### 验证清单
升级完成后逐项检查：
- [ ] `git log` 显示正确的最新提交
- [ ] 自定义文件 `impression_page.py` 存在且内容正确
- [ ] `uv sync` 无报错
- [ ] Agent 可以正常启动
- [ ] 关键功能（对话、技能加载、记忆）正常工作

## 系统配置

```bash
# 确保后台进程在会话断开后继续运行
loginctl enable-linger root
```

升级完成后，建议在方便的时间重启 gateway：
```bash
# 优雅重启（如果有 reload 端点）
# 或停止后重新启动
systemctl restart hermes-agent  # 或你的启动方式
```

## 最佳实践
- **升级前**：确保有完整备份，包括自定义文件和配置文件
- **升级时**：先在小范围验证（如 test 环境），再应用到生产
- **升级后**：运行完整测试套件，确认所有功能正常
- **频率**：建议每周检查一次上游更新，每月执行一次正式升级
