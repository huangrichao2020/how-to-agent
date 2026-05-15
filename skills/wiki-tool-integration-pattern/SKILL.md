---
name: wiki-tool-integration-pattern
description: 将外部 Python 脚本（如 llm-wiki-agent）深度集成到 Hermes Agent 原生工具集的标准化流程。涵盖依赖处理、路径适配、注册机制及孤儿页修复。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wiki, tooling, integration, python]
    category: devops
---

# Wiki 工具集成模式 (Wiki Tool Integration Pattern)

当需要将外部开源项目（如 `SamurAIGPT/llm-wiki-agent`）的工具脚本集成到 Hermes Agent 时，遵循以下流程：

## 1. 环境准备与依赖解决
- **备份**：在修改 `tools/` 目录前，先执行 `cp -r tools tools.bak.$(date +%F)`。
- **依赖安装**：使用 `uv pip install <package>` 在 `.venv` 中安装缺失的库（如 `networkx`）。若遇到 `exclude-newer` 限制，尝试指定旧版本或更新 uv 配置。

## 2. 脚本迁移与适配
- **路径解耦**：原始脚本通常硬编码了 `REPO_ROOT`。必须将其改为参数化（如接收 `wiki_path`），并支持从环境变量 `WIKI_PATH` 读取。
- **注册封装**：创建新的 `tools/wiki_xxx.py`，引入核心逻辑，并使用 `registry.register()` 将其包装为第一类工具。
  ```python
  from tools.registry import registry
  
  def _handler(wiki_path: Optional[str] = None):
      # 调用核心逻辑
      return json.dumps(result, ensure_ascii=False)
  
  registry.register(
      name="wiki_health",
      toolset="research",
      handler=_handler,
      schema={...}
  )
  ```

## 3. 链接逻辑修复 (关键经验)
- **别名解析**：Wiki 常用 `[[Target|Alias]]` 格式。提取链接时必须拆分 `|`，只取 Target 部分进行文件匹配。
- **大小写兼容**：文件系统可能区分大小写，但 Wikilinks 通常不区分。匹配时应统一转为 `lower()`。
- **索引扫描范围**：`overview.md` 等汇总页面包含大量链接，**不应**在统计 inbound links 时被排除，否则会导致其链接的页面被误判为孤儿页。

## 4. 自动化管线 (Cron Ingest)
- **源文件搬运**：编写 `wiki_daily_ingest.py`，定时从 Cron 输出目录搬运 Markdown 报告到 `wiki/raw/articles/`。
- **日志同步**：每次搬运后，必须在 `wiki/log.md` 顶部追加一条 `ingest` 记录，保持健康检查的准确性。

## 5. 孤儿页治理 (Orphan Fix)
- **自动索引**：当发现孤儿页时，不要手动修改每个文件。应在 `overview.md` 底部维护一个 `<!-- AUTO-ORPHAN FIX -->` 区块，动态生成指向所有孤儿页的链接。
- **断链降级**：对于无法修复的断链，脚本应将其替换为纯文本 `(Target)`，避免 Lint 持续报错。

## 6. 验证标准
- 运行 `wiki_health`：确保无空文件、索引同步。
- 运行 `wiki_lint`：确保 Broken Links 和 Orphan Pages 均为 0。