---
name: agent-architecture-evolution
description: Methodology for evolving Hermes Agent architecture using "Router + Blackboard + Graph" patterns from mainstream AI Agent research. Focuses on plugin-based extension without modifying core code.
version: "1.0.0"
metadata:
  hermes:
    tags: ["architecture", "plugin", "router", "blackboard", "dag"]
---

# Agent Architecture Evolution Methodology

## Core Philosophy
Evolve the agent architecture by adopting proven patterns (Router, Blackboard, Graph) while maintaining a **2GB memory constraint** and **zero heavy dependencies** (no LangChain). Use a **plugin system** to decouple new features from the core loop.

## Key Patterns Adopted

### 1. Router + Expert Agents (Intent Routing)
**Problem**: High skill discovery cost; loading all skills wastes tokens.
**Solution**: 
- Create `intent_router.py` that classifies user queries into 9 categories (stock, dev, content, etc.).
- Inject filtered skill lists into `prompt_builder.py` via environment variables (`HERMES_ROUTER_SKILLS`).
- **Result**: 40-60% token reduction in system prompts.

### 2. Blackboard (Shared Context)
**Problem**: Information silos between cron jobs (pre-market, intra-day, post-market).
**Solution**:
- Implement `blackboard.py` with 5 channels (stock, dev, content, system, general).
- Support async read/write, conflict detection, and versioning.
- **Integration**: Cron jobs read/write shared state (e.g., pre-market analysis results are available to intra-day monitoring).

### 3. Graph/Workflow (DAG Orchestration)
**Problem**: Linear scripts lack error handling and dependency management.
**Solution**:
- Build `workflow_dag.py` engine supporting node dependencies, timeouts, and retries.
- **Example**: `check_signals_dag.py` replaces linear monitoring with a 6-node DAG (Market Check -> Fetch Pool -> Fetch Quotes -> Check Signals -> Push Alert -> Update Blackboard).
- **Benefit**: Failed nodes automatically skip downstream dependents.

## Implementation Steps

### Step 1: Create Arch Plugins System
Create `~/.hermes/arch_plugins/__init__.py` to manage plugin lifecycle.
- Plugins inherit `ArchPlugin` base class.
- Configured via `~/.hermes/arch_config.json`.
- Loaded at startup/cron init.

### Step 2: Develop Specific Plugins
1. **IntentRouterPlugin**: Calls `intent_router.py` to set env vars.
2. **BlackboardPlugin**: Initializes `Blackboard()` and registers the agent.
3. **WorkflowDAGPlugin**: Loads DAG definitions for execution.

### Step 3: Integrate with Core
- **Prompt Builder**: Patch `build_skills_system_prompt` in `agent/prompt_builder.py` to read `HERMES_ROUTER_SKILLS` and filter the skill index.
- **Cron Jobs**: Update job prompts to read/write Blackboard state.
- **Scripts**: Refactor critical scripts (e.g., stock monitoring) into DAGs.

## File Structure
```
~/.hermes/
├── arch_plugins/
│   └── __init__.py       # Plugin manager
├── scripts/
│   ├── intent_router.py  # Intent classification
│   ├── blackboard.py     # Shared context
│   ├── workflow_dag.py   # DAG engine
│   └── bull_bear_debate.py # Example DAG
├── router-categories.json # Intent mapping config
├── arch_config.json       # Plugin activation config
└── dual_model_strategy.json # Quick/Deep model routing
```

## Pitfalls & Lessons Learned
1. **Avoid Core Modification**: Do not patch `run_agent.py` directly. Use env vars and prompt additions to influence behavior.
2. **2GB Constraint**: All plugins must be pure Python/JSON. No heavy ML libraries.
3. **Conflict Detection**: Blackboard must track `updated_by` to detect race conditions between concurrent cron jobs.
4. **DAG Failure Handling**: If a node fails, mark all downstream nodes as `skipped` to prevent cascading errors.

## Verification
- Run `python3 ~/.hermes/scripts/intent_router.py` to test classification.
- Run `python3 ~/.hermes/scripts/blackboard.py` to test read/write/conflict.
- Run `python3 ~/.hermes/scripts/bull_bear_debate.py` to test DAG execution.
- Check `~/hermes-agent/scripts/stock_monitor/check_signals_dag.py` for production DAG example.