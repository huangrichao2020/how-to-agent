# Per-Scene Context Budget + Anchor Consistency Check

On 2026-06-01, Hermes and GenericAgent independently evolved four reusable architecture patterns. These are not theoretical designs — they are solutions forced by prompt bloat, state drift, and response latency in live agent runtimes.

## Why This Matters

The most insidious enemy of agent runtimes is not bugs — it's **gradual system prompt inflation**. Every new feature adds a block of rules, every rule adds trigger keywords, and within months the agent reads 15,000+ tokens of "manual" each turn, 80% of which is irrelevant to the current task.

In a single day's conversation, Daoyou (the human operator) flagged Hermes as "too slow", and GA discovered that its memory recall block was eating the majority of its token budget. Both agents independently arrived at the same conclusion: **inject context per-scene, not all-at-once.**

## Pattern 1: Per-Scene Context Injection

### Core Insight

```text
Don't: inject all tools / memory surfaces / cognitive frameworks into every turn
Do:   classify current scene → inject only relevant context → keep core as fallback
```

### Three Layers: Tools / Memory / Cognition

| Layer | Full injection (old) | Per-scene injection (new) | Token savings |
|---|---|---|---|
| **Tool Schema** | All tool descriptions injected | CORE 14 always present, scene groups triggered by keywords | 6-8K/turn |
| **Memory Recall** | MemoryHub 7 surfaces fully injected | coding=3 surfaces, chat=2, stock=3 | 3-5K/turn |
| **Cognitive Framework** | L0-L5 layers + experience bundles always injected | Full framework only when cognitive keywords triggered; lightweight mode otherwise | 2.5K/turn |

### Implementation Skeleton

```python
# Tool selection: CORE always present + scene-triggered groups
CORE_TOOLS = {"terminal", "read_file", "search_files", "patch", ...}  # 14 tools

GROUPS = {
    "browser": {"browser_navigate", "browser_snapshot", ...},
    "feishu": {"feishu_doc_create", "feishu_msg_send", ...},
    "stock": {"stock_quote", "ztb_track", ...},
}

TRIGGERS = {
    "browser": ["web", "browser", "page", "url", "网页", "浏览器"],
    "stock": ["股票", "涨停", "A股", "行情", "复盘"],
}

def select_tools(user_message: str) -> set[str]:
    selected = set(CORE_TOOLS)
    for group_name, keywords in TRIGGERS.items():
        if any(kw in user_message for kw in keywords):
            selected |= GROUPS[group_name]
    return selected
```

### Key Constraints

- **CORE always present**: even if scene classification fails, basic tools never disappear
- **min_tools fallback**: if too few tools matched, pad to a minimum (e.g., 18)
- **Description compression**: non-CORE tool descriptions compressed to 120-180 chars
- **Scene switch auto-releases**: when user switches from "check stocks" to "fix code", previous scene's tools auto-release

## Pattern 2: L1↔L2 Anchor Consistency Check

### Problem

The agent's system prompt injects runtime state every turn ("current project is info-hub", "cultivation: 筑基1层", "model: deepseek-v4-pro"). But these injected values can drift from actual behavior:

- Injection says "project is info-hub" but tool calls target hermes-agent source
- Injection says "model is deepseek" but requests actually go to mimo
- Injection says "cultivation 筑基1层" but state.json was updated to 筑基2层 by cron

Undetected drift causes the agent to make decisions on false premises — memory archived to wrong project, dream analysis using wrong data, self-description completely offline.

### Solution

```text
Injection log (every turn) → dream nightly analysis → consistency report → next prompt correction bias
```

**Step 1: Injection log** (gateway/session.py)

After `_build_runtime_state_section()`, append one JSON line:

```json
{
  "ts": "2026-06-01T18:52:00",
  "cwd": "/Users/tingchi/hermes/hermes-agent",
  "repo": "hermes-agent",
  "cultivation": "筑基1层",
  "model": "deepseek-v4-pro",
  "platforms": ["feishu", "weixin"]
}
```

Stored at `~/.hermes/logs/anchor_drift/YYYY-MM-DD.jsonl`

**Step 2: Dream nightly comparison** (cognitive_dream.py)

`check_anchor_consistency(target_day)` traverses injection log + runtime_ledger (actual tool calls), comparing per anchor:

- **Level 1 factual calibration**: cwd/repo mismatch >60% → flag red
- **Level 2 multi-field drift**: multiple anchors drift simultaneously → escalate severity
- Output `consistency_YYYY-MM-DD.json`

**Step 3: Consumer injection** (GA side: anchor_consistency_consumer.py)

`format_for_prompt()` converts drift results into lightweight hints injected into the next system prompt. Not the full report — just the current known drift summary.

### Why This Is Universal

Any agent with runtime state awareness faces this drift problem. The injection-log → nightly-compare → lightweight-correct pipeline works across architectures:

- CLI agent: injection log to file, nightly script scans
- Web agent: injection log to SQLite, cron job analyzes
- Multi-agent: each agent independently logs, shares consistency reports

## Pattern 3: Runtime State Auto-Injection

### Problem

The agent needs to answer "what realm am I?", "which project?", "what time is it?" every turn. Without injection, it repeatedly reads files / calls tools, wasting tokens and time.

### Solution

Gateway layer builds system prompt with four live-injected anchors:

```python
def _build_runtime_state_section(session_ctx: dict) -> str:
    now = datetime.now()
    return f"""
    - Time: {now.strftime('%Y-%m-%d %a %H:%M')}
    - Platform: {session_ctx.get('platform')}, Chat: {session_ctx.get('chat_name')}
    - Cultivation: {get_cultivation_from_state()}
    - Model: {get_active_model_from_config()}
    - Repo: {get_git_repo_name()}, CWD: {os.getcwd()}
    """
```

**Core principle: rebuild every turn, never cache.** Lifetime is one turn — no file persistence, no cross-turn reuse, no dependency on memory tools. Even if memory injection fails, critical data is still in the system prompt.

## Pattern 4: Model Routing by Task Complexity

### Problem

All messages go through the same model — casual chat and architecture rewrites both use deepseek-v4-pro, high token cost, slow response.

### Solution

```python
def classify_task_complexity(message: str) -> str:
    """Heuristic classification — no LLM call needed"""
    if any(kw in message for kw in ["```", "Traceback", "Error", "import", "def ", "class ", "git "]):
        return "complex"
    if any(kw in message for kw in ["架构", "重构", "设计", "architecture"]):
        return "complex"
    if any(kw in message for kw in ["涨停", "盘前", "复盘", "选股"]):
        return "complex"
    return "lightweight"
```

- complex → deepseek-v4-pro / claude-sonnet
- lightweight → mimo-v2.5 / deepseek-v4-flash (cheap, fast)

**Key constraint: this is heuristic filtering, not text classification.** Better to use cheap model for an extra turn than to call an LLM just for classification. The cost of misclassification is occasionally using a cheap model for a complex question — but CORE tools remain present, so no functionality is lost.

## Implementation Evidence

| Pattern | Hermes commit | GA equivalent |
|---|---|---|
| Per-scene tool budget | `bb55583` feat: tool schema budget | `GA_TOOL_SCHEMA_MODE` / `GA_TOOL_SCHEMA_EXTRA` |
| Per-scene memory budget | `d9e3ef2` fix(memory_hub): per-scene surface budget | `cognitive_retrieval.py` per-face token budget |
| Cognitive capture tiered injection | `a4497e3` perf(cognitive_capture): tiered injection | — |
| Anchor consistency check | `fd88b8d` feat: anchor consistency check | `anchor_consistency_consumer.py` |
| Runtime state auto-injection | `27b77ac` / `fa1982b` / `92f6145` | hot/cold memory split + frame_id |
| Complexity-based model routing | `6415edf` feat: task-complexity model routing | — |

## How to Use

1. **Start with tool budget**: group tools (CORE + scene groups), add trigger word mapping. Largest token savings, simplest implementation.
2. **Then memory budget**: MemoryHub / recall system only injects relevant surfaces per scene.
3. **Add injection logging**: append one JSON line after prompt construction. Accumulate data before analysis.
4. **Add consistency check after data accumulates**: run one week of injection logs before writing comparison logic. Comparison without data is noise.
5. **Finally, model routing**: heuristic classification + cheap/expensive model dispatch. This is a nice-to-have; don't let it block the first four steps.

## Core Principle

```text
Agent optimization is not about adding features — it's about removing what shouldn't be in the current scene.
Every "just in case" injection is debt that future response latency will collect.
Make the agent fast first, then make it precise.
```
