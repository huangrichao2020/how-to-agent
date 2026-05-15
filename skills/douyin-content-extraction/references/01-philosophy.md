# 抖音内容提取哲学

## 核心原则
- 抖音反爬严格，必须用浏览器，不能裸 requests
- headless 模式下页面经常不渲染，用 browser_vision AI 读字
- 登录弹窗必须在截图前关闭，否则截图空白
- Vision API 失效时检查 config.yaml 的 auxiliary.vision 配置

## 短链接处理流程
1. requests 解析重定向获取最终 URL
2. browser_navigate 访问
3. 关闭登录弹窗（3 个 class）
4. browser_vision 截图 + AI 读字

## 约束
- 2GB 服务器环境，不要自己写 Playwright 脚本
- 不要直接截图页面（会空白）
- 不要依赖 browser_get_images（拿不到正文多图）
