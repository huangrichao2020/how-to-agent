---
name: daily-learning-report-cron
description: Workflow for generating and delivering the daily 09:00 AM CST learning report (GitHub + X/Twitter + ClawHub + A-share market) via cron job. Documents environment constraints and workarounds.
version: 1.2.0
author: Hermes
license: Private
---

# Daily Learning Report Cron Workflow

Use this skill when running or troubleshooting the daily 09:00 AM CST learning report cron job.

## Environment constraints (as of April 25, 2026)

### ✅ CONFIRMED WORKING
- **GitHub REST API** (`api.github.com`) — fully reliable for trending, releases, repo details, commits
- **Tencent index quotes** (`qt.gtimg.cn`) — **BEST source for A-share index data**. Returns GBK-encoded text, pipe through `iconv -f GBK -t UTF-8`. Fields are `~` delimited.
- **财联社电报** (`cls.cn/telegraph`) — Next.js SPA. Extract data from `__NEXT_DATA__` script tag JSON (see section 3 below for exact extraction method). Do NOT use regex on HTML div content.
- **Python execute_code** — `terminal`, `read_file`, `write_file`, `search_files`, `patch` available

### ❌ CONFIRMED BROKEN
- **Eastmoney `ulist.np` API** — consistently returns exit code 52 (empty reply). TLS handshake succeeds but no data. Do not use.
- **Eastmoney `clist` API** (板块/概念数据) — returns empty/blocked responses.
- **ClawHub/ClawdHub API** — "No matching routes found" or rate-limited. No usable Endpoint.
- **`delegate_task` with `toolsets=['web']`** — subagents report "no live web search tool attached".
- **DuckDuckGo/Bing/Google web scraping** — `Network is unreachable` in cron environment.
- **Direct X/Twitter scraping** — blocked or requires auth.
- **雪球 API** — requires valid `xq_a_token` cookie; dummy tokens rejected.
- **财联社 API** (`nodeapi/updateTelegraph`) — returns empty/invalid JSON. Use HTML page instead.

## Recommended research approach

### 1. GitHub trending ✅ WORKING (primary signal source)
- **Trending repos:** `terminal()` + `curl` to `api.github.com/search/repositories?q=created:>YYYY-MM-DD&sort=stars&order=desc&per_page=15`
- **Specific searches to run in parallel:**
  - Recent hot: `q=created:>YYYY-MM-DD&stars:>50&sort=stars&order=desc` (last 5 days)
  - AI/Agent: `q=ai+agent+OR+llm+stars:>200&sort=stars&order=desc` (without `topic:` qualifier to avoid OR+qualifier conflict)
  - Python trending: `q=created:>YYYY-MM-DD&language:python&stars:>100&sort=stars&order=desc`
- **Release notes:** `api.github.com/repos/{owner}/{repo}/releases?per_page=2`
- **Repo details:** `api.github.com/repos/{owner}/{repo}`
- **README:** `api.github.com/repos/{owner}/{repo}/readme` with `Accept: application/vnd.github.v3.raw`
- GitHub API is the most reliable and richest automated data source in this environment.

### 2. A-share market data ✅ WORKING (Tencent API)
- **Index quotes endpoint:** `https://qt.gtimg.cn/q=sh000001,sz399001,sz399006,sh000688,sh000300,sh000016,sh000905`
- **Decode:** `iconv -f GBK -t UTF-8`
- **Fields (tilde-separated):** name~current~prev_close~open~volume~change~change_pct~high~low
- **This is the MOST RELIABLE way to get A-share index data from the cron environment.**
- Eastmoney `ulist.np` API is NOT recommended — consistently fails (exit 52 / empty).

### 3. A-share news / 财联社 ✅ WORKING (CLS telegraph)

财联社是 Next.js SPA，数据埋在 `__NEXT_DATA__` 脚本标签的 JSON 中。

**推荐提取方法（解析 __NEXT_DATA__ JSON）：**
```bash
curl -s "https://www.cls.cn/telegraph" -H "User-Agent: Mozilla/5.0" | python3 -c "
import sys, json, re
html = sys.stdin.read()
match = re.search(r'<script[^>]*id=\"__NEXT_DATA__\"[^>]*>(.*?)</script>', html, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    items = data['props']['initialState']['telegraph']['telegraphList']
    for item in items[:20]:
        content = re.sub(r'<[^>]+>', '', item.get('content',''))
        print(f\"{item['id']}: {content[:200]}\")
"
```

**不要用** `telegraph-content-box` 的 HTML 正则匹配（Next.js 渲染的内容结构不稳定）。
**不要用** CLS API 端点 `nodeapi/updateTelegraph`（返回空或无效 JSON）。

**推荐过滤关键词：** A股, 板块, 业绩, 公告, 监管, 半导体, AI, 科技, DeepSeek, 工信部, 证监会

**推荐新闻筛选优先级：**
1. DeepSeek/AI/科技 相关（跟用户工作和自媒体方向最相关）
2. A 股/板块/公司公告（跟炒股兴趣最相关）
3. 宏观政策/地缘政治（影响市场判断）

### 4. X/Twitter signals ⚠️ NOT DIRECTLY ACCESSIBLE
- Use `session_search` to check if recent user-driven sessions captured web search results.
- Otherwise, provide analysis based on GitHub signals + known trajectories.

### 5. ClawHub/community skills ⚠️ NOT DIRECTLY ACCESSIBLE
- Scan local `~/.hermes/skills/` for recently modified SKILL.md files.
- Cross-reference with GitHub signals for overlapping trends.

### 6. Skill ecosystem scan
- Use `skills_list` tool to list available skills and detect new ones.
- Check `~/.hermes/imports/` for any new CoPaw-imported skills.

### 7. Parallel data collection strategy

For efficiency, launch independent data fetches in parallel:
```
terminal: Tencent index quotes
terminal: GitHub trending (recent hot repos)
terminal: GitHub AI/Agent repos
terminal: GitHub Python repos (last 5 days)
terminal: CLS telegraph news
```

Then process all results sequentially. This reduces total wall-clock time.

## 异常处理

### 数据源异常处理
- **GitHub API 超时/限流**：减少 `per_page`，增加重试间隔（30s→60s→120s 退避）；检查 rate limit via `curl -sI api.github.com | grep x-ratelimit`
- **Tencent 返回空**：重试 1 次；如仍失败，使用上一交易日缓存（如有）；否则在报告中注明"A 股数据暂时不可用"
- **财联社 HTML 结构变更**：`__NEXT_DATA__` 解析失败时，fallback 到纯 HTML 正则匹配 `class="telegraph-content-box"`；如仍失败，标记数据源不可用
- **所有数据源不可用**：生成降级报告 — 注明数据来源异常，提供基于历史趋势的框架性分析，不编造数据

### 网络异常处理
- **Network is unreachable**：检查 DNS 配置 (`cat /etc/resolv.conf`)；尝试 `ping 8.8.8.8`；如确认为环境问题，走降级路径
- **TLS 证书错误**：使用 `curl -k` 跳过验证（仅限已确认安全的内部端点）
- **响应超时**：所有 curl 请求增加 `--connect-timeout 10 --max-time 30` 参数

### 报告生成异常
- **数据量过多**：截断到 TOP 5/10，注明"仅展示部分结果"
- **数据量过少**：明确说明，不因数据少而凑数
- **编码问题**：所有外部数据源输出统一转 UTF-8；处理乱码时尝试 `iconv -f GB2312 -t UTF-8`
- **JSON 解析失败**：捕获异常，记录原始响应前 500 字符用于调试

### 静默规则
- 如果所有数据源均不可用且无有意义的分析可生成 → 输出 `[SILENT]` 跳过本次发送
- 如果仅有少量旧数据（无新变化）→ 输出 `[SILENT]`
- 非交易日 A 股无数据但 GitHub 有新信号 → 正常生成，A 股部分标注"今日休市"

## Report structure (fixed)

1. 今日最值得知道的 5 条变化
2. 为什么重要
3. 哪些值得抄，哪些不要抄
4. 今日值得跟踪的股票/板块/市场结构线索
5. 今日值得部署试用的 GitHub 项目
6. 给用户的一个最推荐动作

## Delivery

- Output directly as the cron job response — system auto-delivers to Feishu.
- Do NOT use `send_message` in cron jobs.
- If genuinely nothing new, output exactly `[SILENT]` to suppress delivery.

## Quality rules

- Signal vs speculation must be labeled
- Must produce actionable output, not link dumps
- If real-time data unavailable, state it clearly and provide framework-based analysis instead
- Every repo mention should ideally link to: full_name, stars count, one-line description
- For X/Twitter signals, always note "not directly verified" if only from secondary sources

## Known persistent tracking targets

These repos/projects change frequently and should be checked each run:
- `garrytan/gbrain` — YC总裁的 Hermes/OpenClaw 增强
- `MemPalace/mempalace` — AI记忆系统（竞争GBrain生态位）
- `wbh604/UZI-Skill` — A股深度分析（支持 Hermes）
- `JuliusBrussee/caveman` — token压缩Claude Code skill
- `op7418/guizang-ppt-skill` — 杂志风HTML PPT技能
- `browser-use/browser-harness` — self-healing browser agent

## Patterns worth adopting (from daily learning)

### Multi-agent role specialization
- **Signal**: gstack (87K⭐), agency-agents (89K⭐) split tools into CEO/designer/QA roles
- **Action**: Create standardized subagent role templates in delegate_task (e.g., `code-reviewer`, `researcher`) with default toolsets

### Active-run steering for cron jobs
- **Signal**: OpenClaw v2026.4.29 supports dynamic intervention mid-execution
- **Action**: Use `cronjob(action='send_job_message')` to inject mid-run instructions into long-running jobs

### Skill catalog discovery
- **Signal**: Superpowers (175K⭐) proves skills are the new npm
- **Action**: Build a skills catalog page (wiki/gbrain) listing all skills with triggers/dependencies

### BYOB (Bring Your Own Browser)
- **Signal**: wxtsky/byob (107⭐) reuses existing Chrome sessions with login state
- **Action**: Leverage existing `browser_cdp` skill for connect_cdp mode instead of always launching new instances

### Spec-driven development integration
- **Signal**: github/spec-kit v0.8.3 (92K⭐) adds community extensions
- **Action**: Standardize project kickoff with `specify init` → spec.md → design.md → tasks.md workflow
