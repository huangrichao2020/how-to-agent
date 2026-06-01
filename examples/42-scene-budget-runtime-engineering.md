# 42 - Scene-Budget Runtime Engineering: Verified Patterns from Dual-Agent Sprint

**Source**: GA + 小云 (Hermes) joint sprint, 2026-05-28 to 2026-06-01  
**Commits**: 13 commits, 93 files, +7986/-2694 lines  
**Status**: Verified in production runtime (GA main branch)

---

## The Problem This Sprint Solved

Two production agents (GA on mimo-v2.5, 小云 on DeepSeek) were burning 25k+ tokens per turn on prompt overhead, with 50+ tool schemas injected unconditionally. The user could feel the latency and cost. Both agents also suffered from cold-start context loss, invisible file changes, and duplicated work between the two bots.

## Pattern 1: Scene-Based Tool Schema Budgeting

**What**: Instead of injecting all 50+ tool JSON schemas every turn, split tools into CORE (always present) + GROUPS (scene-triggered) + TRIGGERS (keyword matching).

**Why it works**: Most turns only need 15-25 tools. The remaining 25-35 tool schemas (~6-8k tokens) are pure waste. Scene-based loading cuts tool schema cost by 40-60%.

**Verified architecture** (tool_schema_budget.py, 242 lines):

```
CORE_TOOLS (13, always injected):
  code_run, file_read, file_patch, file_write, update_working_checkpoint,
  ask_user, request_self_restart, runtime_reload, smart_restart,
  agent_hub, memory_section, wiki_query, self_audit

GROUPS (8-9 scene groups):
  browser, delegation, connectors, knowledge, content,
  stock, mcp, research, scheduling

TRIGGERS (keyword → groups mapping):
  "搜索|查一下|研究" → knowledge
  "飞书|文档|lark" → connectors
  "浏览器|网页|JS" → browser
  ...
```

**Key design decisions**:
- `min_tools=18` fallback: when scene detection fails, expand to browser+connectors+knowledge rather than leaving the model with too few tools
- `getBudgetTools()` single entry point: all callers use one function, no need to know which budget strategy is active
- Trigger matching uses last N messages (not just the latest), preventing context window loss when user switches topics mid-conversation

**Anti-pattern caught during testing**: Trigger matching on a single message causes "topic switch amnesia" — user says "search X" in turn 1, then "also check my Feishu doc" in turn 2, and turn 2 only loads connectors. Solution: scan the last 3-5 messages for trigger hits.

## Pattern 2: Hot Context as Startup Memory

**What**: A single `hot_context.md` file that gets auto-injected into every prompt turn via `attention_governance.py`. Contains only durable, high-impact facts: runtime environment, architecture state, key file locations, user preferences.

**Why it works**: Eliminates cold-start context loss without requiring the LLM to search memory every turn. The file is small (~1.3k tokens) but covers everything the agent needs to orient itself immediately.

**Key constraint**: No secrets, no raw private logs, no credentials. Only facts that would be true across multiple sessions.

**Injection path**: `hot_context.md` → `attention_governance.py reads` → merges into `key_info` → injected into system prompt.

## Pattern 3: File Artifact Classification

**What**: When the agent writes files, `artifact_notices.py` classifies the file path and generates a user-visible notice (e.g., "💾 Skill X created", "💾 Memory MEMORY.md updated").

**Why it works**: Users lose trust when agents make changes silently. A deterministic classifier (regex-based, no LLM needed) produces lightweight feedback that says "I changed something, here's what."

**Implementation** (89 lines, zero dependencies):
```python
def classify_file_artifact(path, *, existed_before=None):
    # Pattern match: skills/** → "💾 Skill name created/updated"
    # Pattern match: memory/MEMORY.md → "💾 Memory file updated"
    # Pattern match: wiki/** → "💾 Wiki entry created"
    # Empty string for non-notable files
```

**Wired into**: `ga_file_tools`, `ga_cognitive_tools`, `agent_loop`, `fsapp` (Feishu frontend).

## Pattern 4: Scene→Model Bridge

**What**: Different task scenes route to different LLM models. Code/architecture tasks go to a stronger model (mimo-v2.5-pro), casual conversation stays on the lighter model.

**Implementation**: `SCENE_MODEL_MAP` in `mykey.py` + two entry points in `llmcore.py`.

**Key insight**: Scene detection comes from the prompt text (via `pattern_learner.py`), not from metadata or configuration. The agent infers the scene from what the user is actually saying.

## Pattern 5: Dual-Bot Collaborative Architecture

**What**: When two agents (GA and 小云) work in the same chat, they need:
1. **Clear responsibility boundaries** — GA owns code/runtime, 小云 owns frontend/memory
2. **L1↔L2 anchor consistency** — both bots maintain aligned hot context and working state
3. **Shared handover diary** — when one bot makes changes, the other can read the change log
4. **Mutual ops runbook** (570 lines) — who does what, when to defer, how to review each other's work

**Why it matters**: Without explicit boundaries, two bots end up either duplicating work or leaving gaps. The runbook is not ceremony — it's the minimum coordination protocol that prevents stepping on each other.

## Pattern 6: Retry-on-Empty-Tool

**What**: When the model produces a thinking-only response with zero tool calls, retry with an adjusted prompt rather than returning empty output.

**Why**: Models sometimes produce "I'll help you with that..." thinking blocks without actually calling any tool. Failing silently frustrates users. A single retry with "please call the tool" in the prompt fixes this in most cases.

**Verified**: Added in commit `1f43302`, 2 files changed, +44 lines.

---

## What We'd Do Differently

1. **Token budget instrumentation should have come first**: We optimized before measuring. The per-turn token breakdown (system/tools/memory/history/user/assistant) should have been the first thing deployed, not an afterthought.

2. **Trigger coverage gaps**: Initial trigger mapping missed "search/research" keywords entirely, causing the research tool group to never load. Always validate triggers against real user messages, not developer assumptions.

3. **Dynamic upgrade mechanism**: When scene detection fails, the system should temporarily escalate to full tool loading, succeed, then降级 back to scene mode. We designed this but haven't deployed it yet — it's the natural next step.

## How to Apply This

If you're building an agent with 20+ tools:
1. **Audit your tool injection cost**: Count the JSON schema tokens. If it's >5k, you need scene-based budgeting.
2. **Start with CORE + 3 groups**: Don't try to map all scenes at once. Pick the 3 most common task types and build triggers for those.
3. **Add hot_context.md first**: Before any other optimization, ensure your agent can orient itself in <2k tokens on every turn.
4. **Classify file artifacts**: Even a simple regex classifier builds user trust. It's 89 lines of code with zero dependencies.
5. **If two bots share a workspace**: Write the mutual ops runbook before the bots start stepping on each other. 570 lines sounds like a lot; it's cheaper than debugging coordination failures.

---

*Written by GA, 2026-06-01. Verified in production runtime.*
