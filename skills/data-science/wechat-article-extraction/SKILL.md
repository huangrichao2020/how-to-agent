---
name: wechat-article-extraction
description: Extract content from WeChat public articles (mp.weixin.qq.com) when browser access is blocked by captcha. Uses raw HTTP + HTML parsing. Trigger: 微信公众号/微信文章/mp.weixin.qq.com. Do NOT trigger for Douyin (use douyin-content-extraction), Xiaohongshu, or general web scraping.
version: 2.0.0
---

# 微信公众号文章提取

## 一句话版本

微信公众号文章有反爬验证码，浏览器访问会被拦截。用 raw HTTP + HTML 解析绕过验证码获取正文。核心：requests 带 UA 请求 + rich_media_content 提取 + HTML 实体解码。

## 如何使用本技能

1. **先运行决策树**: `checklists/decision-tree.md`
2. **从 philosophy 开始**: 确认反爬机制和提取策略
3. **按需加载 references**: 匹配问题到解析模式或坑文档
4. **交付前运行**: `checklists/ship-readiness.md`

## 核心反模式（看到这些立刻停下）

- **"用 Playwright/browser 访问微信文章"** → 会触发"环境异常"验证码，白白浪费内存
- **"直接 requests.get 不带 UA/Referer"** → 可能被拦截
- **"不解码 HTML 实体"** → 代码中的 &gt; &amp; \x3c 会乱码
- **"忽略 JS 动态渲染"** → requests 只能拿到骨架，需备用方案
- **"在 2GB 环境开浏览器"** → 极易崩溃，优先 requests 方案

## 配套文件

- `references/01-philosophy.md` — 提取哲学 + 核心方法
- `references/02-html-parsing-patterns.md` — HTML 解析模式详解
- `references/03-pitfalls.md` — 常见坑（反爬/编码/内容缺失/性能）
- `checklists/decision-tree.md` — 策略选择决策树
- `checklists/ship-readiness.md` — 交付前检查清单
