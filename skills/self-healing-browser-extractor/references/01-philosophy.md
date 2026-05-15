# 自愈浏览器提取哲学

## 核心原则
- 不依赖固定框架，agent 在任务中动态编写/修补 helper 函数
- 每个网站反爬机制不同，按需写专用函数，不做通用框架
- 2GB 服务器内存约束，一次只用一个浏览器实例，用完关闭
- Cookie/Session 必须缓存，重复登录触发反爬

## 自愈循环
1. 尝试标准 browser 工具链 → navigate → snapshot → click/type
2. 失败 → 分析原因（DOM 变化/反爬/动态渲染）
3. 编写针对性修复函数 → 存入 browser_helper.py
4. 下次遇到同类问题 → 直接调用已有函数

## 工具选择
- 优先 Playwright（通过 browser_helper.py 封装）
- Selenium 太重，仅在 Playwright 不可用时考虑
- 2GB 环境不要开多个浏览器实例
