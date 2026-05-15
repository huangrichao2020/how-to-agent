---
name: feishu-rich-text-formatting
description: 飞书富文本消息格式化规范 — 避免 Markdown 乱码，使用飞书支持的 post/md 语法。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [feishu, formatting, markdown, messaging]
    related_skills: []
---

# 飞书富文本消息格式化

## 核心问题

飞书的 `post` 消息类型（`{"tag": "md"}`）对 Markdown 支持有限：
- ✅ 支持：`**粗体**`、`*斜体*`、`[链接](url)`、代码块（```）、列表（`- ` / `1. `）
- ❌ **不支持**：Markdown 表格、HTML 标签、标题语法（`#`）、引用（`>`）

**症状**：发送包含表格的 Markdown 到飞书，会显示原始 `| 日期 | 白天 |...` 语法，而非渲染后的表格。标题 `#` 也会原样显示。

## 解决方案

### 方案 A：用列表替代表格（推荐）

**不要用：**
```markdown
| 日期 | 天气 | 气温 |
|------|------|------|
| 今天 | 中雨 | 10°C |
```

**改用：**
```markdown
**今天 (4/29)**
- 天气：中雨转小雨
- 气温：10~11°C
- 风力：东北风 1-3级

**明天 (4/30)**
- 天气：晴
- 气温：12~20°C
- 风力：东风 1-3级
```

### 方案 B：避免使用标题语法

**不要用：**
```markdown
## 杭州天气
```

**改用：**
```markdown
**杭州天气**

简要说明文字。
```

### 方案 C：纯文本模式

如果内容复杂且不需要富文本，可以通过避免所有 Markdown 语法来间接实现纯文本效果。

## 飞书支持的 Markdown 语法清单

| 语法 | 示例 | 支持 |
|------|------|------|
| 粗体 | `**text**` | ✅ |
| 斜体 | `*text*` | ✅ |
| 删除线 | `~~text~~` | ✅ |
| 下划线 | `<u>text</u>` | ✅ |
| 行内代码 | `` `code` `` | ✅ |
| 代码块 | ` ```lang\n...\n``` ` | ✅ |
| 链接 | `[text](url)` | ✅ |
| 无序列表 | `- item` | ✅ |
| 有序列表 | `1. item` | ✅ |
| 引用 | `> text` | ⚠️ 部分支持 |
| **表格** | `\| col \| col \|` | **❌ 不支持** |
| HTML | `<div>...</div>` | **❌ 不支持** |
| 图片 | `![alt](url)` | ❌ 需用专用 API |

## 最佳实践

1. **避免表格**：用列表或分段描述替代
2. **避免 HTML**：只用 Markdown 原生语法
3. **代码块明确语言**：`` ```python `` 比 `` ``` `` 更好
4. **链接必带文字**：`[点击这里](url)` 而非裸 URL
5. **测试发送**：不确定时先发一条测试消息验证格式

## 相关配置

在 `~/.hermes/config.yaml` 中控制飞书的消息显示：

```yaml
display:
  platforms:
    feishu:
      tool_progress: verbose   # off / new / all / verbose
      tool_preview_length: 0   # 0 = 不截断，完整显示
```

- `verbose`：每次工具调用都显示完整参数
- `all`：每次工具调用都显示，但预览长度受 `tool_preview_length` 限制
- `new`：只在切换工具时显示
- `off`：不显示工具调用过程

## 常见陷阱

1. **表格乱码**：飞书不渲染 Markdown 表格 → 改用列表
2. **HTML 标签被忽略**：`<br>`、`<div>` 等无效 → 用换行符 `\n`
3. **Emoji 显示异常**：部分 Emoji 在某些客户端不显示 → 测试后再用
4. **长消息被截断**：飞书单条消息有长度限制 → 分段发送