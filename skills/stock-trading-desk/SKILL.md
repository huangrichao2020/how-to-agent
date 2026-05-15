---
name: stock-trading-desk
description: Run A-share and stock-analysis tasks using Xiaochao/CoPaw constitution plus imported finance skills. Use for market judgment, watchlist review, sector analysis, company breakdown, and trading action plans.
version: 1.0.0
author: Local custom install
license: Private
---

# Stock Trading Desk

Use this skill when the user asks about A-shares, stocks, sectors, market structure, trading plans, board rotation, or company setup.

## Core constitution

In stock or market tasks, obey the imported CoPaw constitution:

- 人性
- 执念
- 住相
- 供需

This is not optional. Do not reduce the answer to price trivia or surface news.

## Question-Form Mode (强制)

在盘前分析、盘后复盘、盘中异动分析时，**必须先锁定以下三要素，再给结论**。不得跳过直接拍脑袋。

| 要素 | 选项 | 说明 |
|------|------|------|
| **市场状态** | 主线行情 / 独立龙头行情 / 震荡防御 | 当前资金共识在哪 |
| **执念阶段** | 孕育→确认→高潮→分歧→退潮→冰点 | 六阶段中处于哪个（人性镜头） |
| **金融三级表** | 外资 / 机构 / 游资 / 散户 | 谁在动、谁在跑 |

## Mandatory reasoning order

1. 【Question-Form】先锁定：市场状态 + 执念阶段 + 金融三级表
2. 执念是谁在扛
3. 当前处于哪个阶段
4. 是需求增强还是供给增强
5. 龙头是否仍在确认主线
6. 给出动作，而不是空洞评论

## Default answer format

When the user wants a judgment, prefer:

1. 现状
2. 执念/阶段判断
3. 供需与龙头
4. 风险点
5. 动作建议

## Use these imported skills when relevant

- `/root/.hermes/skills/copaw-imported/uwillberich/SKILL.md`
- `/root/.hermes/skills/copaw-imported/股票研究/SKILL.md`
- `/root/.hermes/skills/copaw-imported/市场情绪偏离分析/SKILL.md`
- `/root/.hermes/skills/copaw-imported/财报前瞻/SKILL.md`
- `/root/.hermes/skills/copaw-imported/竞争格局分析/SKILL.md`
- `/root/.hermes/skills/copaw-imported/产业链解读/SKILL.md`
- `/root/.hermes/skills/copaw-imported/捕捉公司事件机会/SKILL.md`

## Data Sources for A-share (Empirical Findings)

### API endpoints (cron/server environment)

- **腾讯行情 `qt.gtimg.cn` — 指数行情（✅ 最可靠）**
  - 格式：`https://qt.gtimg.cn/q=sh000001,sz399001,sz399006,sh000688,sh000300`
  - 返回 GBK 编码的 JS 变量，需 `iconv -f GBK -t UTF-8` 解码
  - 字段以 `~` 分隔：名称~当前价~昨收~今开~成交量~涨跌幅
  - 示例解析：`v_sh000001="1~上证指数~000001~4069.37~4093.25~4081.03~...~-23.88~-0.58~..."`
  - **这是 cron 环境中获取指数行情最稳定的方式**

- **东方财富 `push2.eastmoney.com` — 指数行情（❌ 实测不可靠）**
  - `ulist.np` 接口在 cron 服务器环境中经常返回空响应或连接失败
  - 已实测：带 Referer/User-Agent 仍失败（exit code 52 / empty body）
  - **不推荐作为主数据源**，仅在腾讯接口失效时尝试

- **东方财富 `clist` 接口 — 板块/概念数据（❌ 不可用）**
  - `fs=m:90+t:2` 等参数变体均返回空或无法解析

- **雪球 `stock.xueqiu.com` — 需要有效 token**
  - dummy token 会被拒绝，无法获取数据
  - 如果有用户会话中的有效 cookie，可复用

### Browser access (headless)
### Browser access (headless)
- **东方财富行情中心** (`quote.eastmoney.com`) — 板块数据表格在 headless 模式下不渲染，DOM 中无数据
  - 只能获取到沪深港通概况（港股通净买额等）
  - 个股列表、板块排名等 SPA 内容需要 JS 渲染，但数据表格为空
- **东方财富资讯栏目** (`finance.eastmoney.com/a/czqyw.html`, `cywjh.html` 等) — ❌ 实测只返回页脚（"违法和违规信息举报中心"等），正文内容不渲染。**不推荐作为新闻数据源。**
- **财联社电报** (`cls.cn/telegraph`) — ✅ 可用，实时滚动新闻。**推荐：`curl` + regex 直接提取，无需浏览器。** 比 browser_navigate 方案更快、更稳定、资源消耗更低。提取方法：curl 获取 HTML 后用 Python re.findall 匹配 telegraph-content-box 或 content 字段。
- **Avoid**: 在 cron 环境中依赖浏览器获取板块行情数据、个股实时报价

### 推荐策略
1. 指数行情 → 腾讯 `qt.gtimg.cn` API（最快最稳，GBK 编码需转换）
2. 北向资金/港股通 → 东方财富沪深港通页面 browser 可获取概况表
3. 盘中新闻/电报 → 财联社 `cls.cn/telegraph` + `curl` + regex 提取（无需浏览器）
4. 板块/概念行情 → 目前无可靠自动化手段，需在日报中注明数据不可用
5. 个股详情 → 需要有效雪球 token 或用户会话中的浏览器环境
6. **Avoid**: 在 cron 环境中依赖东方财富 push2 API、浏览器 SPA 渲染获取行情数据

- Do not bluff on prices, reports, or news timing.
- For current market/news/company facts, fetch current evidence first.
- If the user asks for action, give a concrete action plan, not only a narrative.

