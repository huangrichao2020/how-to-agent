---
name: github-ops
description: "GitHub 操作 — 仓库管理/PR/code review/issues/认证。Trigger: github/PR/issue/code review. Do NOT trigger for CI/CD 部署。"
version: 1.1.0
---
# GitHub 操作

## 一句话版本
通过 GitHub CLI/API 管理仓库、PR、Issue、Code Review 及认证配置。

## 触发条件
- ✅ **触发**：github、PR 创建/合并/关闭、issue 管理、code review、仓库设置、Token 认证
- ❌ **不触发**：CI/CD 部署（用 CI/CD skill）、Git 本地操作、其他代码托管平台

## 前置条件
1. **认证**：GitHub CLI 已登录 (`gh auth login`) 或配置了 `GITHUB_TOKEN`
2. **权限**：Token 具有对应 scope（`repo`、`read:org` 等）
3. **CLI 可用**：`gh` 已安装且在 PATH 中

## 核心能力

### 1. 仓库管理 + 认证
```bash
# 克隆仓库
gh repo clone owner/repo

# 创建仓库
gh repo create my-repo --public --description "描述"

# 查看认证状态
gh auth status
```

### 2. PR 生命周期管理
```bash
# 创建 PR
gh pr create --title "标题" --body "描述" --base main

# 查看 PR
gh pr view [PR号] --comments

# 合并 PR
gh pr merge [PR号] --squash --delete-branch

# 关闭 PR
gh pr close [PR号]
```

### 3. Code Review
```bash
# 查看文件差异
gh pr diff [PR号]

# 添加 Review Comment
gh pr review [PR号] --comment --body "评论内容"

# Approve / Request Changes
gh pr review [PR号] --approve
gh pr review [PR号] --request-changes --body "需要修改..."
```

### 4. Issue 管理
```bash
# 创建 Issue
gh issue create --title "标题" --body "描述" --label "bug"

# 列出 Issue
gh issue list --state open --label "bug"

# 关闭 Issue
gh issue close [Issue号] --reason completed
```

## 异常处理

### 认证失败
- **症状**：`401 Unauthorized`、`bad credentials`
- **排查**：Token 是否过期、scope 是否正确
- **恢复**：`gh auth login` 重新认证或刷新 Token

### 权限不足
- **症状**：`403 Forbidden`、`resource not accessible`
- **排查**：Token scope 不足、非仓库协作者
- **恢复**：在 GitHub Settings → Developer settings 更新 Token scope

### 冲突处理
- **症状**：PR 存在合并冲突、无法自动合并
- **排查**：查看冲突文件、确认修改范围
- **恢复**：本地拉取分支解决冲突后推送，或要求作者解决

### API 频率限制
- **症状**：`403 rate limit exceeded`
- **排查**：短时间内大量 API 调用
- **恢复**：等待限制重置（通常 1 小时）、使用 authenticated 请求提高限额

### PR/Issue 不存在
- **症状**：`404 Not Found`
- **排查**：确认仓库名和编号是否正确、资源是否已删除
- **恢复**：重新确认编号、检查仓库访问权限

## 常见坑点
- ⚠️ GitHub Token 有过期策略，建议配置 Refresh Token 或使用 GitHub App
- ⚠️ PR 合并非快进时需确认合并策略（merge/squash/rebase）
- ⚠️ Code Review 的 inline comment 需指定文件行号
- ⚠️ 组织仓库可能需要额外权限（`admin:org`）
- ⚠️ 批量操作注意 API 频率限制
