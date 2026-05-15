---
name: douyin-content-extraction
description: "Use when the user provides a Douyin (抖音) link or asks to extract content from Douyin notes/videos. Supports short links, 图文笔记, and video descriptions. Trigger: 抖音/抖音链接/抖音图文/douyin.com. Do NOT trigger for WeChat articles (use wechat-article-extraction), Xiaohongshu (use web-scraping-methodology), or general web scraping."
version: 2.2.0
---

# 抖音图文/视频内容提取

## 一句话版本

从抖音链接到文字的结构化提取工作流。适配抖音反爬机制，在受限服务器环境下稳定获取内容。

## 如何使用本技能

1. **先运行决策树**: `checklists/decision-tree.md`
2. **从 philosophy 开始**: 判断链接类型和内容类型
3. **按需加载 references**: 匹配问题到反爬策略或坑文档
4. **交付前运行**: `checklists/ship-readiness.md`

## 核心反模式（看到这些立刻停下）

- **"直接 requests.get 抖音链接"** → 返回空页面，必须用 browser
- **"直接截图页面（会空白）"** → headless 下经常不渲染，用 browser_vision AI 读字
- **"自己写 Playwright 脚本"** → 2GB 环境容易超时，用 browser_navigate + browser_vision
- **"不关闭登录弹窗就截图"** → 必须先关 3 个 class 弹窗
- **"依赖 browser_get_images 拿正文"** → 抖音正文多图在 rich_media_content，拿不到
- **"把抖音链接发给微信提取"** → 职责错误，用本 skill
