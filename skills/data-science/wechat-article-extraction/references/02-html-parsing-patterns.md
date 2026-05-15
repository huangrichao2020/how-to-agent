# 微信文章 HTML 解析模式

## 元信息提取
- 标题：<meta property="og:title" content="...">
- 描述：<meta property="og:description" content="...">
- 封面图：<meta property="og:image" content="...">
- 发布时间：var ct = "timestamp" (Unix timestamp)
- 公众号 ID：var user_name = "..."

## 正文提取
正文在 class="rich_media_content" 的 div 中：
```python
content = re.findall(r'class="rich_media_content[^"]*"[^>]*>(.*?)</div>\s*(?=<script|<div class="qr_code)', html, re.DOTALL)
```

## 代码块提取
微信文章代码通常被多层 span 包裹 + HTML 实体编码：
```python
def decode_html(s):
    s = s.replace('\x3c', '<').replace('\x3e', '>')
    s = s.replace('\x26', '&').replace('\x22', '"')
    s = s.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
    return s
```

## 完整提取模板
见 SKILL.md 中的 extract_wechat_article 函数
