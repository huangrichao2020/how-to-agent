---
name: github-ci-auto-deploy
description: Set up continuous auto-deployment from GitHub to a remote server via SSH. Push to main triggers build + deploy + restart + version display.
version: 1.0.0
author: Hermes (CoPaw)
license: Private
---

# GitHub CI Auto-Deploy via SSH

Set up push-to-main automatic deployment to a Linux server without Docker or PaaS. GitHub Actions SSHes into the server, runs a deploy script, and version info appears on the live site.

## Workflows

### Method 1: SSH Push (Default)

#### 1. Authentication
Set up a dedicated SSH key for CI on the server. Store private key in GitHub Secrets as DEPLOY_KEY, along with SERVER_HOST and SERVER_USER.

#### 2. deploy.sh
Root-level script handling:
- Git pull (fetch + reset)
- Change detection to skip unnecessary steps
- Version metadata written to JSON
- Dependency installation
- Frontend build and static file copy
- Backend process restart with PID management
- Health check with retries
- Nginx reload

#### 3. deploy.yml
Trigger on push to main + manual dispatch. Use checkout v4 with full history (fetch-depth: 0) for git tag resolution. Use `appleboy/ssh-action` or `webfactory/ssh-agent` + native `ssh` to run `deploy.sh`.

Required secrets: SERVER_HOST, SERVER_USER, DEPLOY_KEY, optionally SERVER_PORT.

### Method 2: Webhook Pull (For Aliyun/Cloud blocks)
**Use when**: GitHub Actions IPs (US ranges) cannot SSH into domestic cloud servers (Aliyun/Tencent block non-standard ports or overseas IPs), or when exposing SSH ports to 0.0.0.0/0 is unacceptable.

#### 1. Backend Webhook Endpoint (`main.py` / `FastAPI`)
```python
from fastapi import FastAPI, Request
import asyncio, os

app = FastAPI()

@app.post("/api/deploy")
async def trigger_deploy(request: Request):
    # 1. Validate secret
    secret = os.environ.get("DEPLOY_SECRET", "your-secret-here")
    if request.headers.get("X-Deploy-Secret") != secret:
        return {"status": "error", "message": "Unauthorized"}
    
    # 2. Async deploy script execution
    async def run_deploy():
        try:
            proc = await asyncio.create_subprocess_exec(
                "bash", "/path/to/deploy.sh",
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            # Log last 1000 chars
        except Exception as e:
            print(f"Deploy failed: {e}")
    asyncio.create_task(run_deploy())
    return {"status": "triggered"}
```

#### 2. CI Workflow (`.github/workflows/deploy.yml`)
Simplifies to an HTTP POST request:
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Deploy
        run: |
          curl -s -X POST "${{ secrets.SERVER_URL }}/api/deploy" \
            -H "X-Deploy-Secret: ${{ secrets.DEPLOY_SECRET }}"
```
**Required Secrets**: `SERVER_URL` (e.g., `https://example.com/api`), `DEPLOY_SECRET`.

### Version API & Frontend
Backend endpoint reads deploy-time version JSON, returns version/commit/date. Frontend displays on load.

## Pitfalls

- **Non-root deploy user (recommended)**: Create dedicated `deploy` user with restricted sudo for nginx reload only. Set `SERVER_USER: deploy` in GitHub Secrets.
- **fetch-depth: 0** mandatory for `git describe` in Actions
- **SSH Port Security Groups**: On Alibaba Cloud/Aliyun, custom SSH ports (e.g., 33) must be explicitly opened in the ECS Security Group for GitHub runners (0.0.0.0/0 or specific IP ranges). **If blocked, the CI will fail with timeout/auth errors, and `sshd` logs will show no incoming connections.** Alternative: use a Webhook-based pull approach if port 22/33 cannot be exposed.
- **TypeScript Strict Mode failures**: `npm run build` in CI may fail due to strict `tsconfig` settings (`noUnusedLocals`, `noUnusedParameters`) even if the app runs in dev. Set these to `false` for CI or fix unused variables.
- **SSH Port ≠ 22**: 宝塔 servers often use custom SSH ports (e.g. 33). Always add `SERVER_PORT` secret and pass to ssh-action. Use `webfactory/ssh-agent` + native `ssh` for more reliable debugging logs than `appleboy/ssh-action` if connections fail silently.
- **venv absolute paths break on copy**: `bin/pip` and `bin/activate` hardcode original directory. After moving project, rebuild: `rm -rf .venv && python3 -m venv .venv && pip install -r requirements.txt`
- **nginx path on 宝塔**: `/usr/bin/nginx` symlinks to `/www/server/nginx/sbin/nginx`. Sudoers must match the actual executable path.
- **git safe.directory**: After changing project ownership, run `git config --global --add safe.directory /path/to/project`
- **requirements.txt completeness**: All runtime deps (pandas, numpy, baostock, pyarrow) must be listed. Missing deps cause silent import failures at runtime.
- Nginx subpath deployments need full prefix in try_files
- Backend restart: kill, sleep, force-kill fallback, then health check
- Vite base flag must match deployment subpath
- No hardcoded credentials

## Verification

Health endpoint OK, version endpoint returns JSON, frontend shows version, Actions green, server git log matches.
