---
name: stock-analyzer-tool-integration
description: 将 A 股分析逻辑封装为 Hermes 原生工具 `stock_analyzer`，集成因果校验、住相探测、供需计算与 Wiki 知识回溯四大引擎。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [stock, trading, tool-integration, wiki-sync]
    category: trading
---

# A 股分析元工具集成 (Stock Analyzer Tool)

## 核心架构：四引擎合一

该工具位于 `/root/hermes-agent/tools/stock_analyzer.py`，通过 `registry.register` 注册为原生工具。

| 引擎 | 功能 | 数据源 | 对应宪法 |
| :--- | :--- | :--- | :--- |
| **Wiki 知识** | 历史记忆回溯，提取实体上下文 | `~/wiki/entities/*.md` | 经验沉淀，不再犯错 |
| **因果校验** | 归因分析（概念/公告） | 百度股市通 API | 因果性 > 相关性 |
| **住相探测** | 阶段判定（连板/分歧） | K 线均线 + 涨停池 | 只做前排，住相破裂即走 |
| **供需计算** | 筹码结构与阻力位 | Info-Hub Parquet 数据 | 供需拐点 + 试仓验证 |

## 实施路径 (2GB 内存适配)

1.  **轻量化设计**：不使用 LangChain，直接调用 `requests` 和 `pandas`。
2.  **依赖处理**：使用 `uv pip install pyarrow --exclude-newer-package pyarrow=false` 绕过阿里云镜像的日期过滤限制。
3.  **自动学习闭环**：
    - 工具支持 `action="learn"` 参数。
    - 当用户确认某只股票的逻辑时，自动更新 Wiki 实体文件并追加时间戳记录。

## 常见陷阱与修复

-   **孤立页问题**：批量生成实体页后，必须运行 Lint 检查并更新 `overview.md` 索引，否则会导致知识库“断链”。
-   **Parquet 读取失败**：在受限环境中，`pyarrow` 安装需指定版本或使用 `exclude-newer-package` 标志。
-   **API 降级**：百度概念接口不稳定时，代码需具备容错能力，不阻断主流程。

## 使用示例

```bash
# 分析个股
python3 -c "from tools.stock_analyzer import StockAnalyzer; print(StockAnalyzer().analyze('002208', '合肥城建'))"

# 注入新知识
python3 -c "from tools.stock_analyzer import StockAnalyzer; sa = StockAnalyzer(); sa.update_entity('002208', '合肥城建', '真实逻辑是长鑫科技存储芯片', 'causality')"
```

## 维护建议

-   定期运行 `wiki_lint` 检查实体库格式。
-   每日盘前通过 Cron Job (`wiki-daily-ingest`) 自动同步报告到 Wiki `raw/` 目录。