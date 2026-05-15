---
name: agent-architecture-upstream-integration
description: Methodology for selectively adopting upstream features from the official hermes-agent repository (NousResearch) without breaking local customizations (Phase 6, Impression-Pointer, etc.). Focuses on "logic extraction" over "blind merging".
category: devops
tags: [hermes-agent, architecture, git, integration]
yao_category: "AI方法"
---

# Agent Architecture Upstream Integration

When integrating new features from the official `hermes-agent` upstream, avoid full merges that risk breaking local architectural customizations (e.g., Phase 6 Impression-Pointer, custom memory layers). Instead, use a **"Logic Extraction"** approach.

## Core Principles
1.  **No Blind Merging**: Never `git merge upstream/main` directly if it involves core runtime files (`run_agent.py`, `hermes_state.py`).
2.  **Extract Logic, Not Code**: Identify the *intent* of the upstream change and reimplement it using local architectural patterns.
3.  **Minimal Footprint**: Changes should be as small as possible to reduce future conflict surface.
4.  **深度学习后参考思路自我优化**: 不要 cherry-pick，理解思路后用我们自己的方式实现。

## Integration Workflow

### 0. 前置筛选：值得看吗？

在投入精力分析之前，先判断上游变更是否跟我们有关系。

**值得看的**：
- gateway 稳定性修复（微信去重、连接池、超时处理）
- 浏览器自动化修复（--no-sandbox、反反爬）
- 我们正在用的 provider/平台的 fix
- 工具注册和工具集系统的改进

**跳过的**：
- macOS-only / Windows-only 的修复
- 我们没有的 provider（如 Slack、Signal、WhatsApp、Mattermost、Matrix）
- 我们没有的平台功能（如 Nous OAuth、dashboard、docker 编排）
- 纯文档/测试/CI 变更

**关键判断标尺**：这个 fix 是否能解决我们实际遇到过的问题？如果答案是否定的，直接跳过。

**实践检验**（2026-05-04）：NousResearch 上游 160+ 新提交，逐一筛选后只有 2 个对我们有用（Weixin 内容指纹去重 + Browser no-sandbox），其中 browser 方案我们已自行实现过。选型率约 1%。

## Integration Workflow

### 1. Analyze Upstream Commit
Use `git show <commit_hash>` to understand the scope:
- **Core Runtime**: `run_agent.py`, `cli.py`, `gateway/run.py` -> **Extract Logic**.
- **Tools/Plugins**: `tools/*.py`, `plugins/*` -> **Safe to Merge** (if no conflicts).
- **Docs/Config**: `docs/*`, `config.yaml` -> **Manual Review**.

### 2. Logic Extraction Examples

#### A. Fallback Initialization (Resilience)
- **Upstream**: Adds complex fallback chain logic in `AIAgent.__init__`.
- **Local Adaptation**: 
  - Locate the specific `resolve_provider_client` block in local `run_agent.py`.
  - Insert the fallback iteration logic *only* where the primary resolution fails.
  - Preserve local variable naming and error handling styles.

#### B. Trigram FTS5 (Search Optimization)
- **Upstream**: Replaces entire `hermes_state.py` search logic.
- **Local Adaptation**:
  - Extract only the SQL DDL for `messages_fts_trigram` and its triggers.
  - Append this SQL to the local `FTS_SQL` constant in `hermes_state.py`.
  - Update the `search_messages` method to check for CJK queries and route them to the trigram table if available, falling back to existing local logic otherwise.
  - Write a standalone migration script to backfill existing data.

#### C. Goal Management (Ralph Loop)
- **Upstream**: 500+ line `goals.py` with judge models and state machines.
- **Local Adaptation**:
  - Create a lightweight `goal_manager.py` that uses a simple file-based anchor (`~/.hermes/active_goal.md`).
  - Inject the goal content into the system prompt via `prompt_builder` or `run_agent` assembly logic.
  - Map the `/goal` command to this lightweight manager instead of the heavy upstream module.

### 3. Verification
- **Syntax Check**: `python -m py_compile <modified_file>`
- **Import Test**: Ensure core modules (`run_agent`, `hermes_state`) can be imported without errors.
- **Functional Test**: Run a basic agent turn to verify the new logic doesn't break the conversation loop.

## Common Pitfalls
- **Overwriting Local Hooks**: Upstream changes might remove local hooks (e.g., impression pointer injection). Always diff against local HEAD.
- **Dependency Bloat**: Upstream features might require new heavy dependencies. Evaluate if the feature is worth the memory cost on constrained servers (2GB RAM).
- **State Schema Conflicts**: Database changes (SQLite) must be handled via migration scripts, not direct schema replacement.

## Reference Commands
```bash
# Inspect upstream changes
git fetch upstream
git log upstream/main --oneline -20
git show <commit_hash> --stat

# Extract specific file content from upstream without merging
git show upstream/main:path/to/file.py > /tmp/upstream_version.py
diff path/to/file.py /tmp/upstream_version.py
```