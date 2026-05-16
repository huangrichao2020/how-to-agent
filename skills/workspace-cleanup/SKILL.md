---
name: workspace-cleanup
description: 清理过期文件、计划、日志和未使用的技能，防止上下文污染。在用户要求清理工作区或 agchk 自检发现"脏数据"时触发。
trigger: "当用户要求清理工作区，或 agchk 自检发现过期计划、旧日志等脏数据时。"
version: 1.1.0
---

# 工作区清理协议

## 核心理念

**活跃目录中的文件就是上下文。** 过期文件（`.plans/` 中的废弃草稿、`RELEASE_*.md` 旧日志）是"脏数据"，会误导 Agent 的判断。

## 前置检查

```bash
# 确认当前位置
pwd

# 查看当前目录结构
find . -maxdepth 2 -type f -name "*.md" -o -name "*.yaml" -o -name "*.yml" | head -50

# 检查 git 状态
git status --short
```

## 清理步骤

### 1. 识别过期文件

扫描以下目录和文件模式：

| 模式 | 说明 | 清理标准 |
|------|------|----------|
| `.plans/` | 过期计划草稿 | 超过 7 天未更新且无引用的 |
| `RELEASE_*.md` | 旧发布日志 | 超过 30 天的 |
| `optional-skills/` | 未使用的技能 | 未被 `config.yaml` 引用的 |
| `*.bak`, `*.tmp` | 临时/备份文件 | 创建超过 24 小时的 |
| 空目录 | 无内容的目录 | 确认后删除 |

```bash
# 快速扫描
find . -name "*.bak" -o -name "*.tmp" -o -name "*.log" | head -20
find .plans/ -mtime +7 -type f 2>/dev/null
find . -name "RELEASE_*.md" -mtime +30 2>/dev/null
```

### 2. 验证影响

在删除前：
- 检查这些文件是否被当前 `config.yaml` 引用
- 检查是否被活跃代码引用
- 确认不是文档或 wiki 内容

```bash
# 检查文件引用
grep -r "文件名" config.yaml 2>/dev/null
grep -r "文件名" --include="*.py" . 2>/dev/null
```

### 3. 归档与删除

```bash
# 不确定时先归档
mkdir -p _archive/$(date +%Y%m%d)
mv <可疑文件> _archive/$(date +%Y%m%d)/

# 确认可以删除的直接删除
rm -rf <明确的过期文件>
```

### 4. Git 清理

```bash
# 清理未跟踪的文件（先 dry-run 预览）
git clean -fdn

# 确认无误后执行
git clean -fd
```

### 5. 验证清理效果

```bash
# 重新运行 agchk 检查评分
agchk 2>/dev/null || echo "agchk 不可用"

# 确认活跃文件未被误删
ls -la config.yaml AGENTS.md SOUL.md 2>/dev/null
```

## 错误处理与异常恢复

### 常见风险与规避
| 风险 | 后果 | 规避方法 |
|------|------|----------|
| 误删活跃配置文件 | Agent 无法正常工作 | 删除前检查 `config.yaml` 引用；重要文件先备份 |
| 误删 wiki/docs 内容 | 知识丢失 | **绝不**删除 `docs/` 或 `wiki/` 内容，除非用户明确要求 |
| 误删 `.github/` 工作流 | CI/CD 中断 | **绝不**删除 `.github/` 目录 |
| 归档目录爆炸 | `_archive/` 越来越大 | 定期清理超过 90 天的归档 |
| git clean 误删 | 未跟踪但有用的文件丢失 | 先 `git clean -fdn` 预览，确认后再执行 |

### 回滚流程
```bash
# 如果误删了文件
# 1. 从归档恢复
mv _archive/$(date +%Y%m%d)/<文件> <原路径>/

# 2. 从 git 恢复（如果是 tracked 文件）
git checkout -- <file>

# 3. 从 git stash 恢复（如果 stash 过）
git stash list
git stash pop
```

### 安全规则
- ⛔ **禁止**删除 `docs/` 或 `wiki/` 内容（除非用户明确要求）
- ⛔ **禁止**删除 `.github/` 工作流
- ⛔ **禁止**删除 `config.yaml`、`AGENTS.md`、`SOUL.md` 等核心配置
- ⛔ **禁止**删除当前正在使用的技能文件
- ✅ **可以**删除仅包含历史草稿或日志的纯历史文件
- ✅ **可以**清理未跟踪的临时文件
- ✅ **可以**归档不确定的文件（而非直接删除）

## 清理报告模板

清理完成后输出报告：
```
━━━ 工作区清理报告 ━━━
📅 时间: YYYY-MM-DD HH:MM
📁 扫描路径: /path/to/workspace

| 操作 | 文件数 | 说明 |
|------|--------|------|
| 已删除 | N | 明确过期的文件 |
| 已归档 | N | 不确定的文件（可恢复） |
| 已跳过 | N | 活跃或被引用的文件 |

⚠️ 注意事项: [如有需要关注的情况]
✅ 清理完成，agchk 评分变化: X → Y
```
