---
name: wechat-account-tracking
description: 追踪指定微信公众号的最新文章。当自动抓取被反爬拦截时，采用“用户转发 + 自动提取分析”的半自动化工作流。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  yao_category: "AI营销"
  hermes:
    tags: [wechat, tracking, monitoring, anti-scraping]
    related_skills: [wechat-article-extraction, a-stock-market-analysis-framework]
---

# WeChat Account Tracking (Anti-Scraping Workaround)

## 核心问题与实测结论

微信公众号（mp.weixin.qq.com）和搜狗微信搜索（weixin.sogou.com）有极强的反爬机制：

1. **Sogou 搜索**：索引延迟严重（实测延迟 27 天），且跳转链接触发 `antispider` 验证码。
2. **直接访问**：`mp.weixin.qq.com/s/xxx` 在 Headless 浏览器或无 Cookie 环境下会弹出“环境异常，请验证”。
3. **RSS 服务**：大多数公共 RSS 桥接服务（如 rsshub, wechat2rss）在国内阿里云环境下不可达或已失效。

## 推荐方案：半自动化工作流

由于全自动抓取在 2GB 内存服务器上极不稳定且维护成本高，采用 **“用户转发 + 自动提取”** 模式。

### Step 1: 用户触发
用户在微信中看到目标公众号（如“盘前”）的文章，**直接转发给 Hermes**。

### Step 2: 自动提取
Hermes 收到链接后，调用 `wechat-article-extraction` 技能：
- 使用 `requests` 带移动端 UA 和 Referer 直接 GET。
- 正则提取 `rich_media_content` 区域。
- 解码 HTML 实体（`&gt;`, `\x3c` 等）。

### Step 3: 框架分析
提取正文后，根据账号属性套用分析框架：
- **财经号**：使用 `stock-trading-desk` 或 `a-stock-market-analysis-framework`。
- **技术号**：使用 `github-x-clawhub-learning-loop`。

## 为什么不做全自动 Cron？

| 维度 | 全自动 Cron | 半自动化转发 |
|------|-------------|--------------|
| **稳定性** | ❌ 极低（频繁触发验证码） | ✅ 极高（利用用户会话 Cookie） |
| **实时性** | ❌ Sogou 延迟 27 天 | ✅ 秒级（用户看到即转发） |
| **资源占用** | ❌ 需常驻 Node/Browser 进程 | ✅ 零常驻，按需触发 |
| **维护成本** | ❌ 需不断更换 IP/Cookie | ✅ 零维护 |

## 实施建议

1. **不要尝试**：在服务器上跑 Headless Chrome 模拟登录微信（极易封号且内存爆炸）。
2. **不要依赖**：Sogou 搜索作为实时数据源（仅适合做历史回溯）。
3. **引导用户**：在日报中提示“如需实时解读某篇微信文章，请直接转发链接给我”。
3. **RSS 服务**：大多数公共 RSS 桥接服务（WeRSS, RSSHub）对热门账号已失效或域名不通。
4. **索引延迟**：搜狗搜索索引通常滞后 20-30 天，无法获取“今日”最新文章。

## 解决方案：半自动化转发工作流

既然全自动抓取不可行，采用 **“用户转发链接 → Agent 自动提取分析”** 的模式。

### Step 1: 设置定时提醒（可选）

使用 `cronjob` 每天早上在固定时间提醒用户转发文章：

```python
# 示例：每天早上 8:00 提醒
from hermes_tools import cronjob
cronjob(action='create', 
        name='盘前文章提醒', 
        schedule='0 8 * * *', 
        prompt='提醒用户：请转发公众号“盘前”的最新文章链接给我，我将为你进行深度分析。',
        deliver='local') # 或者推送到飞书/微信
```

### Step 2: 用户转发链接

用户在微信中看到文章后，直接复制链接发送给你。

### Step 3: 自动提取与分析

收到链接后，按以下流程处理：

1. **提取正文**：调用 `wechat-article-extraction` 技能（或内置工具链）。
   - 关键点：使用移动端 UA + Referer，正则提取 `rich_media_content`。
2. **深度分析**：调用 `a-stock-market-analysis-framework` 技能。
   - 框架：市场状态 → 供需拆解 → 龙头锚定 → 动作指引。
3. **输出报告**：将分析结果整理成简洁的执行建议。

### Step 4: 归档（可选）

将提取的文章和分析报告归档到 `~/wiki/queries/daily-panqian-YYYY-MM-DD.md`，方便后续回溯。

## 为什么不用全自动？

- **成本过高**：需要维护高匿代理池 + 打码服务，且在阿里云国内环境下极不稳定。
- **收益过低**：每天只有一篇文章，手动转发只需 5 秒，自动化投入产出比极低。
- **稳定性**：转发链接是 100% 成功的，而自动抓取随时可能因改版而失效。

## 备选方案：Sogou 监控（仅用于发现新账号）

如果需要寻找某个公众号的最新文章链接（且不知道具体 URL），可以使用 Sogou 搜索作为“目录”，但最终仍需通过浏览器或用户转发获取真实内容。

```python
import requests, re

def search_wechat_account(account_name):
    """搜索公众号文章，返回标题和搜狗跳转链接（注意：链接通常无法直接访问）"""
    url = f"https://weixin.sogou.com/weixin?type=2&query={account_name}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    resp = requests.get(url, headers=headers, timeout=10)
    # 解析逻辑...
    return articles
```

**结论**：对于日常高频使用的账号，**“转发即触发”** 是最稳健、最省心的方案。