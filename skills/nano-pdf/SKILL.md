---
name: nano-pdf
description: Edit PDFs with natural-language instructions using the nano-pdf CLI. Triggers when user asks to 修改PDF, 编辑PDF, 修正PDF内容, 改标题, fix PDF text, update PDF content, or any PDF text editing request. Modify text, fix typos, update titles, and make content changes to specific pages without manual editing.
trigger: User requests to modify PDF content, fix typos in PDF, update dates/titles in a PDF document, or says 修改PDF、编辑PDF、修正PDF.
version: 1.2.0
author: community
license: MIT
metadata:
  hermes:
    tags: [PDF, Documents, Editing, NLP, Productivity]
    homepage: https://pypi.org/project/nano-pdf/
---

# nano-pdf

Edit PDFs using natural-language instructions. Point it at a page and describe what to change.

## Prerequisites

```bash
# Install with uv (recommended — already available in Hermes)
uv pip install nano-pdf

# Or with pip
pip install nano-pdf
```

Verify installation:
```bash
nano-pdf --version
```

## 用法 (Usage)

```bash
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

## 示例 (Examples)

```bash
# Change a title on page 1
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"

# Update a date on a specific page
nano-pdf edit report.pdf 3 "Update the date from January to February 2026"

# Fix content
nano-pdf edit contract.pdf 2 "Change the client name from 'Acme Corp' to 'Acme Industries'"
```

## 执行步骤 (Workflow)

### Step 1: 前置检查 (Pre-flight)
1. **验证文件存在**: `test -f <file.pdf> || echo "File not found"`
2. **检查文件类型**: `file <file.pdf>` 应返回 "PDF document"
3. **检查文件是否被锁定**: 确保无其他进程占用该文件
4. **验证 API 密钥**: `nano-pdf --help` 查看所需环境变量 — 如需设置 `NANO_PDF_API_KEY`

### Step 2: 安全备份 (Backup)
```bash
cp original.pdf original.pdf.bak
```

### Step 3: 执行编辑 (Execute)
```bash
nano-pdf edit original.pdf <page_number> "your instruction"
```
- 指令应尽可能具体，包含要查找的原文和替换后的内容
- 如果不确定页码，先用 `pdfinfo` 查看总页数

### Step 4: 验证结果 (Verify)
```bash
file original.pdf          # 确认仍是有效 PDF
ls -la original.pdf        # 检查文件大小是否变化
```

## 异常处理 (Error Handling)

| 错误 | 原因 | 恢复方案 |
|------|------|----------|
| `Command not found` | nano-pdf 未安装 | 运行 `uv pip install nano-pdf` 重新安装 |
| `Permission denied` | 文件或目录缺少写权限 | `chmod u+w <directory>` 或先复制到可写目录 |
| `Page number out of range` | 页码超出范围 | 用 `pdfinfo <file.pdf> \| grep Pages` 查看总页数 |
| `API key missing` | 环境变量未设置 | 设置 `export NANO_PDF_API_KEY=***` 或查阅文档配置 |
| `Edit failed / no changes` | 指令模糊或页面上找不到文本 | 用更精确的原文描述重试；尝试更宽泛的描述 |
| `Corrupted output PDF` | 编辑引擎遇到不支持的内容 | 从备份恢复；尝试更简单的指令；考虑用 qpdf 作为兜底 |
| `Wrong page modified` | 页码基数不一致 (0-based vs 1-based) | 重试时 page_number ± 1 |
| 编辑超时 (>60s) | LLM API 响应慢或网络问题 | 取消当前操作；检查网络连接；重试或换用离线工具兜底 |

### 兜底方案 (Fallback)
1. 如果 nano-pdf 反复失败，改用 `qpdf` 做结构性修改（合并、拆分、旋转）
2. 对于扫描版 PDF（图片型），先用 OCR 工具提取文本，再考虑编辑
3. 超大 PDF (>50MB)：先提取目标页面，编辑后再合并回去
4. 复杂布局修改：nano-pdf 无法处理，建议用专业 PDF 编辑器手动操作

## 避坑指南 (Pitfalls)

- ⚠️ **注意页码基数**: 不同版本的页码可能是 0-based 或 1-based — 如果编辑错了页面，重试 ±1
- ⚠️ **注意只支持文本编辑**: 复杂布局/图形修改可能失败
- ⚠️ **注意扫描版 PDF**: 图片型 PDF 无法用 nano-pdf 编辑 — 需要先用 OCR
- ⚠️ **注意 API 密钥**: 工具底层调用 LLM — 需要有效的 API key
- ⚠️ **禁止在生产环境直接编辑** — 始终先备份原始文件
- ⚠️ **注意验证输出** — 每次编辑后确认 PDF 仍有效且改动正确

## Limitations

- **Text-only edits**: Works best for text changes. Complex layout/graphic modifications may fail.
- **Scanned PDFs**: If the PDF is image-based (scanned), nano-pdf cannot edit text — use OCR tools first.
- **Large PDFs**: For files >50MB, consider extracting the target page first, editing it, then merging back.
