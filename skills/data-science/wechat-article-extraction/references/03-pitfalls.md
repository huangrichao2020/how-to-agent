# 微信文章提取常见坑

## 反爬坑
- 浏览器访问触发"环境异常"验证码（阿里云 IP/Headless 检测）
- requests 不带 Referer 可能被拦截
- 不带 UA 或 UA 不对可能被拦截

## 编码坑
- HTML 实体编码需要多层解码（&gt; &amp; \x3c）
- 代码块用 span 嵌套包裹，需要逐层清理
- 换行符可能被替换为 <br/> 或 <br>

## 内容缺失坑
- 文章通过 JS 动态渲染 → requests 只能拿到骨架
- 被拦截时 OG title 通常仍可用
- rich_media_content 可能仍有部分正文

## 性能坑
- 2GB 环境不要用浏览器访问微信文章
- requests timeout 设置 10-15s 足够
