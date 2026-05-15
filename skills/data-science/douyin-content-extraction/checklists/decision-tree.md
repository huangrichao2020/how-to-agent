# 抖音内容提取决策树

## 1. 判断链接类型
- [ ] 是抖音链接吗？→ 否：退出，本 skill 不适用
- [ ] 短链接（v.douyin.com）？→ 是：先解析重定向

## 2. 判断内容类型
- [ ] 图文笔记？→ browser_navigate + 关弹窗 + browser_vision
- [ ] 视频？→ 提取 description 字段

## 3. 判断反爬
- [ ] 有登录弹窗？→ 关闭 3 个 class
- [ ] 页面渲染正常？→ 否：等待加载或重试

## 4. 判断提取
- [ ] browser_vision 可用？→ 是：截图 + AI 读字
- [ ] Vision API 失效？→ 检查 config.yaml 配置
- [ ] 全部失败？→ 提示用户手动复制
