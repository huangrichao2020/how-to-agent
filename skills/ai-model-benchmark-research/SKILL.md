---
name: ai-model-benchmark-research
category: research
description: Workflow for researching AI model performance benchmarks when operating from a restricted network (China/Alibaba Cloud). Covers fallback sources, SPA content extraction, and benchmark table parsing.
---

## 触发条件
用户询问某个 AI 模型的性能、基准测试分数、与其他模型的对比。

## 网络环境约束
国内阿里云环境，以下站点通常不可达或触发验证：
- Google / Hugging Face / GitHub → 连接超时
- Baidu / Sogou → 验证码/反爬
- Zhihu → 页面渲染异常（SPA 框架，snapshot 经常为空或极短）

## 可靠信息源（按优先级）
1. **ModelScope** (`modelscope.cn/models/...`) — 国产模型官方托管页，通常可达
2. **cn.bing.com** — 搜索可用，但知乎链接往往渲染不全
3. **官方技术博客/论文** — 如果能访问则优先

## 核心技巧：提取 SPA 页面内容
当 `browser_snapshot(full=true)` 截断或返回极少内容时（常见于 React/Vue SPA），用 `browser_console` 的 JS 表达式直接抓取：

```js
// 提取所有段落、列表项、表格单元格中的有效文本
Array.from(document.querySelectorAll('p, li, td, th, span, div'))
  .map(el => el.innerText)
  .filter(t => t.length > 10 && t.length < 500)
  .join(' | ')
  .substring(0, 10000)
```

如果页面有 `<article>` 或 `.prose` 容器，优先从容器内提取：
```js
const article = document.querySelector('article, .prose, .markdown-body');
if(article) article.innerText.substring(3000, 12000);
```

## 执行流程
1. 先试 ModelScope 搜索模型名
2. 进入模型卡片页，用 `browser_snapshot` 看是否有完整 model card
3. 如果内容被截断，切到 `browser_console` 用 JS 提取
4. 提取的文本中定位 benchmark 表格（通常包含 "Model | Size | Score" 格式的文本）
5. 整理为 Markdown 表格回复用户

## 常见陷阱
- `browser_vision` 截图**无法捕获页面下方的长表格**，只适合确认页面头部信息
- `browser_snapshot(full=true)` 超过 8000 字符会被截断，且对 SPA 经常只返回框架结构
- 模型卡片中的 benchmark 数据通常在页面中下部，需要先滚动或直接 JS 提取全文
