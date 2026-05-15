# 抖音提取常见坑

## 反爬坑
- 直接 requests.get 返回空页面或验证页
- headless 模式下页面经常不渲染
- 不关弹窗就截图 → 空白

## 工具坑
- 自己写 Playwright 脚本 → 2GB 环境超时
- 依赖 browser_get_images → 拿不到正文
- 直接截图页面 → 经常空白

## Vision 坑
- Vision API 失效 → 检查 config.yaml 的 auxiliary.vision
- 截图分辨率不够 → 文字识别不清

## 链接坑
- 短链接不解析重定向 → 无法访问
- 微信链接混入 → 应该用 wechat-article-extraction
