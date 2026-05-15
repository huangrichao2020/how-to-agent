---
name: llm-wiki-integration
description: 将 LLM Wiki Agent (SamurAIGPT/llm-wiki-agent) 深度集成到 Hermes Agent 原生工具集的标准流程。涵盖依赖处理、工具注册及自动化管线配置。
version: 1.0.0
author: Hermes Agent
category: devops
---

# LLM Wiki Agent 深度集成指南

本技能记录了将 `llm-wiki` 从单纯的 Skill 升级为 Hermes 原生工具（Native Tool）的实战经验。

## 核心挑战与解决方案

### 1. 依赖管理陷阱 (2GB 内存环境)
在阿里云 2GB 环境下，使用 `uv pip install networkx` 时遇到 `exclude-newer` 过滤导致包不可用的问题。
- **根因**：Hermes 的 `uv.toml` 设置了全局 `exclude-newer` 以保证稳定性，但 `networkx` 最新版被过滤。
- **解决**：指定旧版本安装 `uv pip install "networkx<3.4"`，或在脚本中移除对 `networkx` 的强依赖（如 `health.py` 是纯确定性的，无需该库）。

### 2. 工具化封装 (Tool Registration)
原始脚本基于命令行参数 (`argparse`)，无法直接被 Agent 调用。
- **动作**：
  - 迁移至 `hermes-agent/tools/wiki_health.py`。
  - 引入 `from tools.registry import registry`。
  - 定义 `_handler` 函数并调用 `registry.register()`。
  - **关键点**：必须解耦 `REPO_ROOT`，改为支持 `wiki_path` 参数或 `WIKI_PATH` 环境变量。

### 3. 自动化管线 (Cron Integration)
Wiki 的价值在于“自动沉淀”。
- **建议方案**：创建一个 Cron Job，每日扫描 `~/wiki/raw/` 目录下的新文件，自动触发 `ingest` 流程。
- **回滚计划**：在执行大规模 ingest 前，执行 `cp -r ~/wiki ~/wiki.bak.$(date +%F)`。

## 验证步骤

1. **发现测试**：运行 `python3 -c "from tools.registry import discover_builtin_tools; print('tools.wiki_health' in discover_builtin_tools())"`。
2. **功能测试**：调用 `wiki_health()` 工具，确认能正确识别空文件和索引不同步项。

## 避坑指南

- **不要手动改 `index.md`**：所有索引更新必须由 Agent 在 ingest 流程中完成，否则会导致 `index_sync` 检查报错。
- **Health vs Lint**：`health` 是零 LLM 调用的结构检查，适合每次会话启动时运行；`lint` 涉及语义分析，成本高，建议每 10-15 次 ingest 后运行一次。