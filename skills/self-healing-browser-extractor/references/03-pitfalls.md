# 浏览器提取常见坑

## 反爬坑
- 抖音/微信/小红书都有独立反爬机制，不能复用同一套逻辑
- 登录弹窗必须在截图前关闭，否则截图空白
- Cookie 过期后自动触发验证，需要重新获取

## 内存坑
- 2GB 服务器开多个浏览器实例 → OOM
- headless 模式下 Chrome 默认占 300-500MB，必须用 --no-sandbox + --disable-gpu

## 超时坑
- 自己写 Playwright 脚本在 2GB 环境下容易超时
- 优先用 browser_navigate + browser_vision，不要裸写 Playwright

## 选择器失效坑
- 网站更新后 CSS 选择器失效，需要重新分析 DOM
- 不要硬编码选择器，用更通用的策略（如文本匹配、ARIA 标签）
