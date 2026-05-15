---
name: webhook-deploy-trigger
description: Webhook-based CI/CD deployment trigger — GitHub Actions POSTs to server endpoint, server validates secret and runs deploy.sh asynchronously.
category: devops
---

## Webhook 部署模式

替代 SSH 反向连接的 CI/CD 方案，适用于云服务器屏蔽非标 SSH 端口或海外 IP 连接不稳定的场景。

### 架构

```
GitHub Actions (push main) → HTTP POST /api/deploy → 后端校验 Secret → 异步执行 deploy.sh
```

### 后端接口要求

```python
@app.post("/api/deploy")
async def trigger_deploy(request: Request):
    payload = await request.json()
    if payload.get("secret") != os.environ["DEPLOY_SECRET"]:
        raise HTTPException(403, "Unauthorized")
    # 异步执行 deploy.sh
    subprocess.Popen(["bash", "deploy.sh"], stdout=open("/tmp/deploy.log", "w"))
    return {"status": "triggered", "version": get_version()}
```

### GitHub Actions 配置

```yaml
- name: Trigger Deploy
  run: |
    curl -X POST ${{ secrets.SERVER_URL }}/api/deploy \
      -H "Content-Type: application/json" \
      -d '{"secret": "${{ secrets.DEPLOY_SECRET }}"}'
```

### GitHub Secrets

| 名称 | 说明 |
|------|------|
| `SERVER_URL` | 网站地址（Nginx 代理到后端） |
| `DEPLOY_SECRET` | Webhook 校验密钥（随机字符串） |

### 验证步骤

1. Push 代码到 main
2. 检查 Actions 状态为 success
3. curl 验证 `/api/version` 返回新 commit
4. 查看 `/tmp/deploy.log` 确认构建完整

## deploy.sh 部署脚本特性（Info-Hub 模式）

后端部署脚本 (`/home/deploy/info-hub/deploy.sh`) 包含以下步骤：
1. `git fetch origin main && git reset --hard origin/main` — 全量覆盖本地代码
2. 写入 `version_info.json` 到后端目录
3. `npm install && npm run build` — 构建前端
4. 前端文件复制到 `/www/wwwroot/info-hub/`
5. **重启后端 uvicorn 进程**（先 kill 旧进程再启动新的）
6. `nginx -s reload` — 重载 Nginx

### 依赖陷阱

⚠️ **`deploy.sh` 不会自动安装 Python 新依赖**。它只做 git pull 和 npm build。
新增的 Python 依赖（如 `requests`）在部署后会导致 500 错误：

```
ModuleNotFoundError: No module named 'requests'
```

**解决办法**：在部署前手动安装：
```bash
cd /home/deploy/info-hub/backend
source .venv/bin/activate
pip install <package-name>
```

或者在 `deploy.sh` 的开头添加自动安装逻辑。

## 手动远程部署（SSH 模式）

当 webhook 不可用时（如网络断开），可通过 SSH 远程手工部署：
```bash
ssh -p 33 deploy@120.26.32.59 "cd /home/deploy/info-hub && git pull && bash deploy.sh"
```

### 常见问题

- **403 Unauthorized**: Secret 不匹配，检查 GitHub Secrets 与后端代码
- **部署未生效**: 检查 `/tmp/deploy.log`，确认 `deploy.sh` 执行无报错
- **Nginx 未重载**: 确认 `deploy` 用户有 `sudo nginx -s reload` 权限