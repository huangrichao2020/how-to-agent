---
name: wechat-article-extraction-v2
description: 微信公众号文章提取工作流 v2.0。针对微信反爬升级（环境异常验证、HTML 动态渲染）及内容图片化趋势，采用“HTML 源码解析 + Vision AI 图片识别”的混合提取方案。适用于 mp.weixin.qq.com 链接的内容获取与归档。
category: data-science
---

# 微信公众号文章提取工作流 v2.0

## 核心逻辑
微信反爬已从“前端弹窗拦截”升级为“服务端 IP 标记 + HTML 内容隐藏”。此外，大量复盘/数据类文章采用**全图片排版**以规避文本抓取。
因此，单一的文字提取已失效，必须采用 **Vision AI (视觉识别)** 兜底。

## 触发条件
- 用户提供 `mp.weixin.qq.com` 链接并要求学习/提取内容。
- 自动化脚本返回内容为空或仅包含 UI 引导文字（如“点击上方蓝字关注”）。

## 工作流步骤

### Step 1: 尝试基础请求 (Fast Path)
使用 `requests` 配合桌面端 UA 获取 HTML。检查 `id="js_content"` 区域是否有实质性中文文本。
```python
import requests, re, html
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
r = requests.get(url, headers=headers, timeout=15)
match = re.search(r'id="js_content"[^>]*>(.*?)</div>', r.text, re.DOTALL)
text = re.sub(r'<[^>]+>', '', match.group(1)) if match else ""
if len(text) < 100: 
    # 判定为失败，进入 Step 2
```

### Step 2: 提取图片链接 (Image Extraction)
如果文本提取失败，从 HTML 中提取所有 `data-src` 属性。这些通常是高清原图链接。
```python
images = re.findall(r'data-src="([^"]+)"', r.text)
# 清理 URL：将 &amp; 替换为 &
clean_urls = [u.replace('&amp;', '&') for u in images]
```

### Step 3: Vision AI 批量识别 (Vision OCR)
对提取出的图片 URL 逐一调用 `vision_analyze`。
- **Prompt 策略**：明确告知 AI 这是 A 股数据/复盘图表，要求提取所有板块、个股、涨跌幅等结构化数据。
- **注意**：如果图片数量过多（>10），优先识别前 3-5 张核心图表，或根据图片文件名/上下文判断重点。

### Step 4: 内容重组与归档
将 Vision AI 返回的文本进行清洗、去重和格式化，按照 Wiki 约定（Markdown + Frontmatter）归档到 `/root/wiki/queries/` 目录。

## 常见陷阱与应对
1. **登录弹窗遮挡**：浏览器自动化（Playwright/Selenium）在阿里云环境下极易触发“环境异常”验证码且无法自动绕过。**解决方案**：放弃浏览器渲染，直接分析静态 HTML 中的图片资源。
2. **图片防盗链**：微信图片通常有 Referer 限制。`vision_analyze` 工具通常能处理此类请求，若失败可尝试在 Header 中添加 `Referer: https://mp.weixin.qq.com/`。
3. **长图截断**：部分超长图片可能被 Vision API 截断。若发现内容不完整，需提示用户手动提供截图或分段识别。

## 适用场景
- 财经复盘类公众号（正文多为连板天梯、板块涨幅图）。
- 深度研报类公众号（正文多为复杂图表）。
- 任何 HTML 文本提取失败的微信文章。