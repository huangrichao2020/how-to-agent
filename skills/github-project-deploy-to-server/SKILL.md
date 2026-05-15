---
name: github-project-deploy-to-server
description: Take a GitHub project from repo inspection to build, server deployment, restart, and smoke verification. Use for user requests to run GitHub projects on remote servers.
version: 1.1.0
author: Local custom install
license: Private
---

# GitHub Project Deploy To Server

Use this skill when the user wants Hermes to pull a GitHub project, run it locally or remotely, and deploy it onto a server.

## Objective

Move from repository URL to live service safely and pragmatically.

## Default workflow

1. **Inspect the repository first**
   - README for setup/deployment instructions
   - package.json / pyproject.toml / Cargo.toml / docker-compose.yml
   - Environment requirements (.env.example, requirements.txt, Gemfile, etc.)
   - Startup commands documented in scripts or CI config
2. **Identify the real runtime contract**
   - Build command (if any)
   - Run command (dev vs production)
   - Ports the service listens on
   - Persistent data paths (databases, uploads, caches)
   - Required secrets (API keys, database URLs, tokens)
3. **Run the narrowest local verification available**
   - Quick syntax/config check before full build
   - `--dry-run` or `--version` flags when available
4. **Prepare the server**
   - Install missing system deps (apt/yum/apk as appropriate)
   - Create `.env` files from templates or `.env.example`
   - Create service wrapper (pm2/systemd/supervisor as appropriate)
5. **Deploy incrementally**
   - Sync only what is needed (git clone or rsync)
   - Run build on server or transfer pre-built artifacts
   - Start/restart the service
   - Verify: logs, process table, open ports, and one live smoke path
6. **Leave a handoff**
   - Startup command
   - Restart command
   - Log path
   - Config path
   - Rollback hint

## 异常处理 (关键)

### 预检失败
- **Repo 不存在或不可访问**：验证 URL 格式，检查是否为 private repo，尝试 `git ls-remote` 测试
- **README 缺失**：查找 CI 配置 (.github/workflows/) 推断构建流程，检查是否有 Dockerfile
- **依赖冲突**：优先使用项目锁定的版本 (lock files)，必要时用 venv/conda 隔离

### 构建失败
- **Node.js 版本不匹配**：检查 `.nvmrc` 或 `engines` 字段，安装对应版本
- **Python 依赖安装失败**：检查是否有二进制依赖需要系统包 (如 `libpq-dev`, `build-essential`)
- **编译型语言失败**：确认系统工具链完整 (`gcc`, `make`, `rustc` 等)
- **内存不足**：Node 构建设 `--max-old-space-size`，Rust/C++ 设 `CARGO_BUILD_JOBS=1`

### 启动失败
- **端口冲突**：用 `ss -tlnp` 检查，必要时换端口或 kill 占用进程
- **缺少环境变量**：对比 `.env.example` 逐个补全，必填项不得留空
- **权限问题**：确保运行用户有读写权限，`chown`/`chmod` 数据目录
- **超时/无响应**：检查是否卡在等待外部服务 (DB, Redis, 第三方 API)

### 远程服务器问题
- **SSH 连接失败**：检查密钥、安全组、防火墙；使用 `aliyun-bash` / `aliyun-cmd` 替代原生 SSH
- **scp/rsync 中断**：增加 `-o ServerAliveInterval=30` 参数；大文件考虑 rsync 断点续传
- **远程命令执行失败**：避免嵌套引号问题，使用 helper wrappers 而非手工拼接 SSH 命令

### 回滚策略
- **部署前**：记录当前运行版本 (git commit hash / 二进制版本)
- **部署失败时**：恢复旧版本目录/容器，重启旧服务
- **Smoke 测试失败**：立即回滚，记录错误日志，不强行上线
- **数据迁移回滚**：如有数据库迁移，准备逆向迁移脚本

## Operating rules

- Prefer actual live verification over documentation claims.
- Do not claim deployment success until process + log + smoke path all pass.
- For remote aliyun work, prefer helper wrappers such as `aliyun-bash` and `aliyun-cmd` instead of brittle nested SSH quoting.
- If the repo is modern and container-friendly, consider Docker; otherwise choose the simplest native deployment path.
- **Always have a rollback plan before deploying.**
- **Log all commands and their output** — the user should be able to reproduce or debug later.

## Good final deliverable

The user should get:

- Where the project is deployed (server IP, path, port)
- How it starts (exact command)
- How to restart it
- How to check logs (path and command)
- How to verify it is alive (smoke test URL or command)
- How to rollback to previous version
- What secrets/env vars are in use (masked)
