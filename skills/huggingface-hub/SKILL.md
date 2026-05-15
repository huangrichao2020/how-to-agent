---
name: huggingface-hub
category: mlops
description: Hugging Face Hub CLI (hf) — search, download, and upload models and datasets, manage repos, query datasets with SQL, deploy inference endpoints, manage Spaces and buckets.
version: 1.1.0
author: Hugging Face
license: MIT
tags: [huggingface, hf, models, datasets, hub, mlops]
---

# Hugging Face CLI (`hf`) Reference Guide

The `hf` command is the modern command-line interface for interacting with the Hugging Face Hub, providing tools to manage repositories, models, datasets, and Spaces.

> **IMPORTANT:** The `hf` command replaces the now deprecated `huggingface-cli` command.

## 触发条件 (Trigger Conditions)
- **触发**: User asks to download, upload, or search Hugging Face models/datasets
- **触发**: User needs to manage HF repos (create, delete, branch, tag)
- **触发**: User wants to query datasets with SQL via DuckDB
- **触发**: User needs to deploy/manage Inference Endpoints or Spaces
- **适用**: Model/dataset operations on Hugging Face Hub, MLOps workflows

## 使用流程 (Workflow)

### 步骤 1: 安装与认证
*   **Installation:** `curl -LsSf https://hf.co/cli/install.sh | bash -s`
*   **Authentication:** `export HF_TOKEN=your_token` or `hf auth login`

### 步骤 2: 搜索与下载
*   Search: `hf models list --search <query>`, `hf datasets list --search <query>`
*   Download: `hf download REPO_ID`

### 步骤 3: 上传与管理
*   Upload: `hf upload REPO_ID` or `hf upload-large-folder REPO_ID LOCAL_PATH`
*   Repo management: `hf repos create/delete/move/branch`

---

## Core Commands

### General Operations
*   `hf download REPO_ID`: Download files from the Hub.
*   `hf upload REPO_ID`: Upload files/folders (recommended for single-commit).
*   `hf upload-large-folder REPO_ID LOCAL_PATH`: Recommended for resumable uploads of large directories.
*   `hf sync`: Sync files between a local directory and a bucket.
*   `hf env` / `hf version`: View environment and version details.

### Authentication (`hf auth`)
*   `login` / `logout`: Manage sessions using tokens from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
*   `list` / `switch`: Manage and toggle between multiple stored access tokens.
*   `whoami`: Identify the currently logged-in account.

### Repository Management (`hf repos`)
*   `create` / `delete`: Create or permanently remove repositories.
*   `duplicate`: Clone a model, dataset, or Space to a new ID.
*   `move`: Transfer a repository between namespaces.
*   `branch` / `tag`: Manage Git-like references.
*   `delete-files`: Remove specific files using patterns.

---

## Specialized Hub Interactions

### Datasets & Models
*   **Datasets:** `hf datasets list`, `info`, and `parquet` (list parquet URLs).
*   **SQL Queries:** `hf datasets sql SQL` — Execute raw SQL via DuckDB against dataset parquet URLs.
*   **Models:** `hf models list` and `info`.
*   **Papers:** `hf papers list` — View daily papers.

### Discussions & Pull Requests (`hf discussions`)
*   Manage the lifecycle of Hub contributions: `list`, `create`, `info`, `comment`, `close`, `reopen`, and `rename`.
*   `diff`: View changes in a PR.
*   `merge`: Finalize pull requests.

### Infrastructure & Compute
*   **Endpoints:** Deploy and manage Inference Endpoints (`deploy`, `pause`, `resume`, `scale-to-zero`, `catalog`).
*   **Jobs:** Run compute tasks on HF infrastructure. Includes `hf jobs uv` for running Python scripts with inline dependencies and `stats` for resource monitoring.
*   **Spaces:** Manage interactive apps. Includes `dev-mode` and `hot-reload` for Python files without full restarts.

### Storage & Automation
*   **Buckets:** Full S3-like bucket management (`create`, `cp`, `mv`, `rm`, `sync`).
*   **Cache:** Manage local storage with `list`, `prune` (remove detached revisions), and `verify` (checksum checks).
*   **Webhooks:** Automate workflows by managing Hub webhooks (`create`, `watch`, `enable`/`disable`).
*   **Collections:** Organize Hub items into collections (`add-item`, `update`, `list`).

---

## Error handling & troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `hf: command not found` | CLI not installed | Run `curl -LsSf https://hf.co/cli/install.sh \| bash -s` |
| `authentication failed` | Token expired or invalid | Run `hf auth login` with a fresh token from huggingface.co/settings/tokens |
| `repository not found` | Repo ID typo or private repo without access | Verify repo ID format (`user/repo-name`); check access permissions |
| `upload failed` / timeout | Large file or network issue | Use `hf upload-large-folder` for resumable uploads |
| `download failed` | Disk full or network issue | Check disk space (`df -h`); use `HF_HUB_ENABLE_HF_TRANSFER=1` for faster downloads |
| `rate limited` | Too many API calls | Wait and retry; consider using `--token` with authenticated requests |
| `duckdb error` on SQL query | Dataset not in parquet format or SQL syntax issue | Verify dataset has parquet files; check SQL syntax |
| Space deployment stuck | Compute quota exceeded or config error | Check HF account quota; verify `requirements.txt` and app config |

### Best practices
- **Always authenticate** before uploading or accessing private repos: `export HF_TOKEN=your_token`
- **Use `--format json`** for scripting and automation
- **Large uploads**: prefer `hf upload-large-folder` over `hf upload` for resumable transfers
- **Cache management**: run `hf cache prune` periodically to free disk space

## Advanced Usage & Tips

### Global Flags
*   `--format json`: Produces machine-readable output for automation.
*   `-q` / `--quiet`: Limits output to IDs only.

### Extensions & Skills
*   **Extensions:** Extend CLI functionality via GitHub repositories using `hf extensions install REPO_ID`.
*   **Skills:** Manage AI assistant skills with `hf skills add`.
