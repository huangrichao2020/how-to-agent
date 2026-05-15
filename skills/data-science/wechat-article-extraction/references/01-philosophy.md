# 微信文章提取哲学

## 核心原则
- 微信公众号有强反爬（环境异常验证），浏览器访问会触发验证码
- Raw HTTP 请求可绕过验证码获取正文，优先使用 requests
- 2GB 服务器环境，不要用 Playwright/Selenium 访问微信文章
- HTML 实体编码（&gt; &amp; \x3c）需要多层解码

## 核心方法
1. requests 带桌面端 UA 直接 GET
2. 从原始 HTML 中提取 js_content / rich_media_content
3. HTML 实体解码 + 标签清理
4. 提取元信息（OG 标签 + JS 变量）
