---
name: github-x-clawhub-learning-loop
description: Continuously learn from GitHub, X/Twitter, and ClawHub/community-skill ecosystems, then synthesize what matters into a teach-back memo for the user.
version: 1.1.0
author: Local custom install
license: Private
---

# GitHub X ClawHub Learning Loop

Use this skill when the user wants Xiaoyun/Hermes to learn the latest knowledge from GitHub, X/Twitter, or ClawHub-like skill ecosystems and then explain it back clearly.

## Mission

Do not stop at “I found links”.

The output should become:

1. what changed
2. why it matters
3. what to copy
4. what to ignore
5. what the user should do next

If the user asks Xiaoyun to "study it and then teach me", "digest it for me", "organize it", or similar, this skill must produce a teaching artifact, not only a chat summary.

## Data source reliability (server environment)

From the Hermes cron/server environment, **web search engines (DuckDuckGo, Bing, Google) are blocked** (`Network is unreachable`). X/Twitter direct scraping is also unreliable.

**Reliable sources (API-based, confirmed working):**
- GitHub REST API (`api.github.com`) — trending search, repo details, READMEs, commits, releases
  - ⚠️ **GitHub Search API 的 OR 运算符不能与 qualifiers 混用**。例如 `q=stars:>500+topic:ai+OR+topic:llm` 会返回 "Validation Failed"。正确做法：用 `q=stars:>500+ai+OR+llm`（OR 只作用于纯文本关键词，不能作用于 `topic:`、`stars:` 等限定符）
- 东方财富 API (`push2.eastmoney.com`) — **INTERMITTENT**. `ulist.np` endpoint works some days but returns exit code 52 (empty reply) on others. TLS handshake succeeds but server sends no data. Sector/board concept data endpoints (`clist` with `fs=m:90+t:2`) consistently return empty/blocked.
- 雪球 API (`stock.xueqiu.com`) — requires valid `xq_a_token` cookie; dummy tokens are rejected

**Unreliable / blocked:**
- DuckDuckGo HTML scraping → `Network is unreachable`
- Bing web scraping → returns empty or blocked
- Direct X/Twitter page scraping → blocked or requires auth
- 东方财富 板块/概念数据 API → `clist` 接口返回空或无法解析
- 东方财富 行情中心 SPA (browser_navigate) → 板块数据表格在 headless 模式下不渲染
- ClawHub/ClawdHub API → "No matching routes found" or rate-limited; no working public endpoint
- `delegate_task` with `toolsets=['web']` → subagents report "no live web search tool attached"

**Strategy:** When X/Twitter or web search is unreachable, pivot to:
1. GitHub API for tech/agent/tooling signals (reliable and rich)
2. Eastmoney API for A-share market data (try first, but have fallback ready)
3. `session_search` to check if recent user-driven sessions have web search results
4. Framework-based analysis with explicit "no real-time data" disclaimers when all automated sources fail

## Source-specific playbooks

### GitHub

Look for:

- trending repositories
- release notes
- fast-growing agent / AI / tooling repos
- PRs/issues/discussions that reveal design direction

Prioritize:

- official release pages
- repo README / docs
- commit or changelog evidence when behavior changed recently

### X / Twitter

Use X/Twitter as a signal layer, not as the only truth source.

Look for:

- creators/operators sharing field-tested workflows
- launch announcements
- hot takes that can be verified elsewhere

Always separate:

- signal
- evidence
- speculation

### ClawHub / community skills ecosystem

Look for:

- new popular skills
- installable workflows users actually reuse
- patterns worth importing into Hermes

When the source is marketplace/community content:

- distinguish official/bundled skills vs community skills
- note maturity and maintenance risk

## Mandatory output contracts

Choose one of these formats based on the ask. If unspecified, prefer `Teach-back Brief`.

### Teach-back Brief

Use for fast user education after one learning pass.

Structure:

1. 本轮学到了什么
2. 最值得你知道的 3-5 条
3. 哪些值得抄，哪些不要抄
4. 我建议你下一步怎么用

### Daily Learning Note

Use when the task feels like a daily scan.

Structure:

1. 今日新增信号
2. 真正重要的变化
3. 对你有用的动作
4. 值得继续跟踪的对象

### Weekly Learning Report

Use when synthesizing multiple repositories, creators, or skill ecosystems.

Structure:

1. 本周最重要的 5-10 条变化
2. 变化背后的趋势判断
3. 可直接复用的方法/技能/项目
4. 下周值得继续跟踪的名单

### Tutorial / Playbook

Use when the user explicitly wants to be taught.

Structure:

1. 这是什么
2. 为什么现在值得学
3. 核心概念
4. 一步一步怎么做
5. 常见坑
6. 我建议你先练哪一部分

## Teach-back format

When done, answer the user in this structure:

1. 今日/本轮我学到了什么
2. 最值得你知道的 3-5 条
3. 我建议你马上吸收/忽略什么
4. 如果要落地，我会怎么装成技能/流程

## Persistence

If the findings are durable, write or update a concise note/manual rather than leaving the knowledge only in chat.

When possible, create or update a local artifact before replying:

- memo
- manual
- playbook
- handoff note

The user prefers tangible artifacts over vague summaries.
