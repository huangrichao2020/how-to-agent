---
name: code-graph-analysis
description: "基于 Python AST 的轻量级代码依赖分析系统。用于 Code Review、爆炸半径分析、Bug 根因定位。零重型依赖，2GB 服务器可用。"
trigger: "当需要进行 Code Review、代码审计、影响范围分析、重构评估、Bug 根因定位时触发"
yao_category: "AI编程"
---

# Code Graph - 代码知识图谱分析

基于 Python AST 的轻量级代码依赖分析系统，零重型依赖。

## 快速启动

```python
import sys
sys.path.insert(0, "/root/hermes-agent")
from agent.code_graph.builder import CodeGraphBuilder

builder = CodeGraphBuilder("/root/项目路径")
builder.build()  # 构建/增量更新
```

## 核心操作

### 1. 爆炸半径分析
```python
radius = builder.get_blast_radius(["修改的文件.py"])
# 返回影响的节点和文件列表
```

### 2. 节点上下文
```python
context = builder.get_node_context("文件:函数名:L行号")
# 返回 called_by（谁调用）和 calls（调用了谁）
```

### 3. 统计信息
```python
stats = builder.get_stats()
# total_nodes, total_edges, indexed_files, by_type
```

## CLI 使用

```bash
cd ~/hermes-agent
python3 -m agent.code_graph.cli build --project /root/info-hub
python3 -m agent.code_graph.cli stats --project /root/hermes-agent
python3 -m agent.code_graph.cli blast --files run_agent.py
python3 -m agent.code_graph.cli context --node "file:func:L10"
```

## 已覆盖项目

| 项目 | 节点 | 边 | 文件 |
|------|------|----|------|
| hermes-agent | 9,308 | 24,127 | 350 |
| info-hub | 249 | 854 | 37 |
| agchk | 196 | 624 | 43 |
| TradingAgents | 322 | 457 | 52 |
| wiki | 113 | 212 | 9 |

## 工作流

1. **Code Review 前**: 先 build 增量更新图谱
2. **分析变更**: 用 get_blast_radius 找出影响范围
3. **深度审查**: 对核心节点用 get_node_context 获取调用链
4. **输出报告**: 汇总变更 + 影响文件 + 建议检查点

## 注意事项

- 仅支持 Python 文件（.py）
- 数据库在各项目根目录下的 code_graph.db
- 增量更新基于 MD5 比对，文件未变则跳过
- 2GB 服务器可用，无重型依赖