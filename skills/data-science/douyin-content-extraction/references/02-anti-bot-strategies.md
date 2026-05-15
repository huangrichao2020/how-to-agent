# 抖音反爬策略详解

## 登录弹窗关闭
必须关闭三个 class：
- `.disturb-login-panel`
- `.douyin_login_new_class`
- `.comment-input-unlogin-container`

方法：在页面 JS 中执行 setAttribute('style', 'display:none')

## 图文笔记 vs 视频
- 图文笔记：多张图片，需要 browser_vision 逐张读取
- 视频：提取 description 字段即可

## 短链接解析
- v.douyin.com/xxx → requests.get(allow_redirects=True)
- 最终 URL 格式：douyin.com/note/xxx 或 douyin.com/video/xxx

## 内容区域
- 正文在 rich_media_content 区域
- browser_get_images 拿不到，必须用 vision AI
