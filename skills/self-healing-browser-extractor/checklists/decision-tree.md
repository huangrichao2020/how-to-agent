# 浏览器提取决策树

## 1. 判断提取类型
- [ ] 静态页面（HTML 可直接解析）？→ 用 web scraping，退出本 skill
- [ ] 动态渲染/需要交互？→ 继续

## 2. 判断反爬强度
- [ ] 需要登录/验证码？→ Cookie 复用模式
- [ ] 弹窗拦截？→ bypass_popup 模式
- [ ] 动态内容加载？→ wait_for_element 模式

## 3. 判断工具
- [ ] 标准 browser 工具可用？→ 优先用 browser_navigate/snapshot
- [ ] 失败？→ 分析原因，编写专用函数
- [ ] 2GB 内存约束？→ 一次只开一个实例

## 4. 判断是否已有修复
- [ ] 检查 browser_helper.py 是否有对应函数？→ 有：直接调用
- [ ] 没有？→ 编写新函数，存入 helper
