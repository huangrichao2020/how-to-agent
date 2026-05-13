---
name: self-healing-browser
description: 自愈式浏览器提取工作流。Agent 在任务中动态编写或修补浏览器辅助函数，而不是依赖僵硬框架。涵盖 DOM 蒸馏、反爬处理、视觉 AI 集成、微信和抖音内容提取。
---

# 自愈式浏览器提取器

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md)

当 agent 需要从有反爬、动态渲染或复杂交互的网站提取内容时，使用这个 skill。

## 核心哲学

**Agent writes missing functions.**

不要为每一种网站场景预先设计僵硬框架。维护一个可写的 `browser_helpers.py` 模块，让 agent 在任务中动态编写和 patch 辅助函数。遇到新的反爬机制，就写一个新函数处理它。

## 架构

```text
┌─────────────────────────────────────────────┐
│           Agent Decision Layer               │
│  分析页面，决定提取策略                         │
└──────────────────┬──────────────────────────┘
┌──────────────────▼──────────────────────────┐
│        browser_helpers.py (writable)         │
│  - extract_wechat_article()                  │
│  - close_login_popup()                       │
│  - bypass_cloudflare()                       │
│  ... agent 按需新增函数                        │
└──────────────────┬──────────────────────────┘
┌──────────────────▼──────────────────────────┐
│        Playwright / Selenium (engine)        │
│  Chromium browser, headless or headed        │
└─────────────────────────────────────────────┘
```

## 工作流

### 1. 导航和快照

```python
browser_navigate(url)
# 返回包含交互元素和 ref IDs 的初始 snapshot
```

### 2. 处理反爬机制

Agent 应识别并处理常见模式：

- **登录弹窗**：把遮罩或弹窗元素设为 `display='none'`
- **验证码**：用视觉 AI 读取挑战
- **Cookie walls**：接受或关闭 cookie banner
- **Cloudflare challenges**：等待 JS challenge 完成

### 3. 提取内容

动态内容流程：

1. **先 snapshot**：获取 accessibility tree 和元素引用。
2. **识别内容区域**：找到主内容容器。
3. **提取**：使用合适的 helper function。
4. **验证**：检查提取结果是否合理。

### 4. 编写缺失函数

遇到新模式时：

```python
def extract_new_site_pattern(page):
    # 根据当前页面分析实现
    pass
```

## 平台模式

### 微信文章

```python
def extract_wechat_article(url):
    # 通过 rich_media_content 区域绕过验证
    # 从渲染后的 HTML 正则提取
    # 返回 title, author, content, publish_date
```

### 抖音笔记

1. 短链 -> requests 解析重定向。
2. 用 browser_navigate 打开页面。
3. 关闭三类登录弹窗：
   - `.disturb-login-panel`
   - `.douyin_login_new_class`
   - `.comment-input-un-login-container`
4. 用 browser_vision 截图并让 AI 读文本。
5. **不要**直接截图、直接写 Playwright 脚本、或依赖 browser_get_images 抽正文图片。

### SPA 数据提取

- 用 `browser_console` 运行 JavaScript 表达式检查 DOM 状态。
- 等待异步内容渲染后再 snapshot。
- 滚动触发懒加载内容。

## 视觉 AI 集成

当文本 snapshot 不够时：

```python
browser_vision(question="What does this CAPTCHA say?")
# 返回 AI 分析和 screenshot_path
```

适用场景：

- 验证码
- 视觉验证挑战
- 复杂布局理解
- 图片型内容提取

## 反模式

- **不要直接写 Playwright 脚本**：容易 timeout。
- **不要直接截图**：可能空白或漏内容。
- **不要依赖 browser_get_images 提取正文**：它返回页面图片，不等于渲染后的正文。
- **不要使用僵硬框架**：新反爬模式会让框架失效。
- **不要重复同一种失败策略**：失败一次后，写新的 helper function。

## Helper 模板

```python
def extract_<site>_<content_type>(page):
    """
    Extract <content_type> from <site>.

    Anti-bot handling:
    - <specific mechanism>

    Returns:
    - <structured data>
    """
    # Implementation
    pass
```

## 验证清单

提取后检查：

- [ ] 内容长度合理，不为空、不截断
- [ ] 标题符合预期页面
- [ ] 关键数据点存在
- [ ] 提取文本里没有错误消息
- [ ] helper function 已保存到 `browser_helpers.py` 以便复用
