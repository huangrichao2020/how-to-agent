---
name: clawdhub
description: Use the ClawdHub CLI to search, install, update, and publish agent skills from clawdhub.com. Use when you need to fetch new skills on the fly, sync installed skills to latest or a specific version, or publish new/updated skill folders with the npm-installed clawdhub CLI.
version: 1.1.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Skills, CLI, Package Manager, Agent, Registry]
    category: tools
    homepage: https://clawdhub.com
prerequisites:
  commands: [clawdhub, npm]
---

# ClawdHub CLI

Manage agent skills: search, install, update, and publish via the ClawdHub registry.

## 触发条件

当用户需要以下场景时触发此 Skill：
- 搜索并安装新的 agent skills
- 更新已安装的 skills 到最新版本
- 发布/分享自己创建的 skills
- 查看已安装的 skills 列表

## Install CLI

```bash
npm i -g clawdhub
```

Verify installation:
```bash
clawdhub --version
```

## 工作流程

### Step 1: 搜索 Skills

```bash
clawdhub search "postgres backups"
```

### Step 2: 安装 Skill

```bash
# 安装最新版本
clawdhub install my-skill

# 安装指定版本
clawdhub install my-skill --version 1.2.3
```

### Step 3: 更新 Skills

```bash
# 更新单个 skill
clawdhub update my-skill

# 更新到指定版本
clawdhub update my-skill --version 1.2.3

# 更新所有 skills
clawdhub update --all

# 强制更新（忽略本地修改）
clawdhub update my-skill --force
clawdhub update --all --no-input --force
```

### Step 4: 查看已安装列表

```bash
clawdhub list
```

### Step 5: 发布 Skill（需认证）

```bash
# 登录
clawdhub login
clawdhub whoami

# 发布
clawdhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

## 命令参考

| Command | Description |
|---------|-------------|
| `clawdhub search <query>` | Search registry for skills |
| `clawdhub install <slug>` | Install a skill to local `./skills` directory |
| `clawdhub update <slug>` | Update a skill (hash-based match + upgrade) |
| `clawdhub update --all` | Update all installed skills |
| `clawdhub list` | List installed skills |
| `clawdhub login` | Authenticate for publishing |
| `clawdhub whoami` | Show current authenticated user |
| `clawdhub publish` | Publish a skill folder to registry |

## 配置选项

- **默认注册表**: `https://clawdhub.com`（通过 `CLAWDHUB_REGISTRY` 环境变量或 `--registry` 覆盖）
- **默认工作目录**: 当前目录；安装目录：`./skills`（通过 `--workdir` / `--dir` 覆盖）
- **更新机制**: 对本地文件进行 hash 匹配，解析对应版本，除非指定 `--version` 否则升级到最新

## 异常处理

| 场景 | 处理方式 |
|------|---------|
| npm 未安装 | 安装 Node.js + npm：`curl -fsSL https://deb.nodesource.com/setup_lts.x \| bash - && apt install -y nodejs` |
| clawdhub 命令未找到 | 运行 `npm i -g clawdhub` 重新安装，检查 `$PATH` 中是否包含 npm global bin 目录 |
| 网络超时/连接失败 | 检查网络，或使用 `--registry` 指定可用的镜像源 |
| 登录失败 (401/403) | 确认凭据正确，检查网络代理设置 |
| 安装冲突（本地有同名 skill） | 使用 `--force` 强制覆盖，或先重命名本地目录 |
| 发布失败 | 确认已登录（`clawdhub whoami`），检查 slug 是否已被占用 |
| 版本冲突 | 使用 `--version` 指定目标版本，或 `--force` 强制更新 |

## 注意事项（避坑）

- **更新会覆盖本地修改**: `clawdhub update` 基于 hash 匹配，如果本地有修改可能导致冲突，使用 `--force` 前确认是否需要保留本地改动
- **安装目录**: 默认安装到 `./skills`，确保在正确的工作目录下执行
- **无输入模式**: 在自动化脚本中使用 `--no-input` 避免交互式提示阻塞
