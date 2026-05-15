---
name: codebase-inspection
description: Inspect and analyze codebases using pygount for LOC counting, language breakdown, and code-vs-comment ratios. Use when asked to check lines of code, repo size, language composition, or codebase stats.
category: code-analysis
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [LOC, Code Analysis, pygount, Codebase, Metrics, Repository]
    related_skills: [github-repo-management]
prerequisites:
  commands: [pygount]
---

# Codebase Inspection with pygount

Analyze repositories for lines of code, language breakdown, file counts, and code-vs-comment ratios using `pygount`.

## When to Use

- User asks for LOC (lines of code) count
- User wants a language breakdown of a repo
- User asks about codebase size or composition
- User wants code-vs-comment ratios
- General "how big is this repo" questions

## 执行步骤

1. 确认 pygount 已安装：`pip install pygount`（如未安装见下方异常处理）
2. 进入目标仓库目录
3. 选择合适的 `--folders-to-skip` 参数排除依赖目录
4. 执行 pygount 命令并获取结果
5. 解读输出中的语言分布、代码行数、注释比例
6. 如遇到错误进行兜底处理

## Prerequisites

```bash
# 示例：安装 pygount
pip install --break-system-packages pygount 2>/dev/null || pip install pygount
```

## 1. Basic Summary（常用示例）

Get a full language breakdown with file counts, code lines, and comment lines:

```bash
cd /path/to/repo
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  .
```

**注意：** Always use `--folders-to-skip` to exclude dependency/build directories, otherwise pygount will crawl them and take a very long time or hang.

## 2. Common Folder Exclusions（示例）

Adjust based on the project type:

```bash
# Python 项目
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JavaScript/TypeScript 项目
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"

# 通用
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"
```

## 3. Filter by Specific Language（示例）

```bash
# 只统计 Python 文件
pygount --suffix=py --format=summary .

# 只统计 Python 和 YAML
pygount --suffix=py,yaml,yml --format=summary .
```

## 4. Detailed File-by-File Output（示例）

```bash
# 默认格式显示每个文件的详细统计
pygount --folders-to-skip=".git,node_modules,venv" .

# 按代码行数排序（通过管道传递给 sort）
pygount --folders-to-skip=".git,node_modules,venv" . | sort -t$'\t' -k1 -nr | head -20
```

## 5. Output Formats（示例）

```bash
# Summary 表格（推荐）
pygount --format=summary .

# JSON 输出（程序化使用）
pygount --format=json .

# 管道友好格式
pygount --format=summary . 2>/dev/null
```

## 6. Interpreting Results

The summary table columns:
- **Language** — detected programming language
- **Files** — number of files of that language
- **Code** — lines of actual code (executable/declarative)
- **Comment** — lines that are comments or documentation
- **%** — percentage of total

Special pseudo-languages:
- `__empty__` — empty files
- `__binary__` — binary files (images, compiled, etc.)
- `__generated__` — auto-generated files (detected heuristically)
- `__duplicate__` — files with identical content
- `__unknown__` — unrecognized file types

## 异常处理 / Error Handling

| 错误场景 | 原因 | 解决方案 |
|---------|------|---------|
| `pygount: command not found` | pygount 未安装 | 运行 `pip install pygount` 或 `pip install --break-system-packages pygount` |
| `Permission denied` | 无权限读取某些目录 | 添加 `--folders-to-skip` 排除受限目录；或使用 `sudo`（谨慎） |
| 执行超时 / 长时间无响应 | 依赖目录太大 | 添加更多排除项：`--folders-to-skip=".git,node_modules,venv,..."`；或指定 `--suffix` 限制语言范围 |
| `Error: No such file or directory` | 路径不存在 | 先用 `cd` 确认目标目录存在；使用绝对路径 |
| 结果为空 / 零行统计 | 仓库为空或排除过多 | 检查 `--suffix` 是否误过滤；去掉排除项重新执行 |
| `MemoryError` | 仓库过大 | 使用 `--suffix` 按语言分段统计；或改用 `cloc` 作为替代 |
| `Error reading file` 编码问题 | 文件编码不兼容 | pygount 会自动跳过无法读取的文件，忽略即可 |

**兜底策略 / Fallback：**
- pygount 不可用 → 回退到 `cloc`（`apt install cloc`）或 `tokei`（`cargo install tokei`）
- 简单行数统计 → 直接使用 `wc -l` 命令
- 目录太大 → 逐个子目录分别统计后汇总

## Pitfalls（注意事项）

1. **始终排除 .git, node_modules, venv** — 不加 `--folders-to-skip` 会扫描所有依赖目录，可能耗时数分钟甚至卡死
2. **Markdown 显示 0 代码行** — pygount 将 Markdown 全部归类为注释，这是预期行为
3. **JSON 文件统计偏低** — pygount 对 JSON 的统计较保守，精确行数请用 `wc -l`
4. **大型 monorepo** — 建议用 `--suffix` 指定语言范围，不要全量扫描
5. **禁止在没有排除项的情况下对生产环境仓库执行** — 可能导致高负载
6. **注意区分代码行和注释行** — pygount 的统计是启发式的，可能会有少量误差
