---
name: self-healing-browser-extractor
description: "Use when browser automation needs to self-heal from failures — stale selectors, dynamic content, anti-bot measures. The agent writes/patches browser helper functions dynamically during tasks. Trigger: browser automation failing/stale element/anti-bot/dynamic content. Do NOT trigger for static page extraction (use web scraping), API-based data fetching, or when browser tools are unavailable."
version: 1.3.0
---

# 自愈浏览器提取

## 一句话版本

不依赖固定框架的浏览器提取方案。Agent 在任务中动态编写/修补 `browser_helper.py`，遇到新问题时自己写新函数。

## 如何使用本技能

1. **先运行决策树**: `checklists/decision-tree.md`
2. **从 philosophy 开始**: 判断提取类型和反爬强度
3. **按需加载 references**: 匹配问题到具体模式文件
4. **交付前运行**: `checklists/ship-readiness.md`

## 核心反模式（看到这些立刻停下）

- **"写通用框架处理所有网站"** → 每个网站反爬不同，通用框架必然臃肿。按需写专用函数
- **"浏览器自动化失败就放弃"** → 这是自愈 skill 存在的意义。分析原因，写修复
- **"用 Selenium 重写整个流程"** → 太重。优先 Playwright（browser_helper.py 封装）
- **"不缓存 Cookie/Session"** → 重复登录触发反爬。提取后保存 Cookie
- **"在 2GB 服务器开多个浏览器实例"** → 内存不够。一次只用一个，用完关闭
- **"把 browser_helper.py 当黑盒"** → 这个文件是 agent 自己写的，要理解每一行

## 配套文件

- `references/01-philosophy.md` — 自愈哲学 + 循环策略
- `references/02-browser-helper-patterns.md` — 常用修复模式
- `references/03-pitfalls.md` — 常见坑（反爬/内存/超时/选择器）
- `checklists/decision-tree.md` — 工具选择决策树
- `checklists/ship-readiness.md` — 交付前检查清单
