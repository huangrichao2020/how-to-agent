---
name: agentic-architecture-patterns
version: 2026-04-30
description: Patterns from open-design and agentic-stack for building portable, memory-driven agent systems. Use when designing agent architecture, improving context injection, or implementing self-evolving memory loops.
triggers: ["agent architecture", "context budget", "memory loop", "design system", ".agent folder", "dream cycle"]
---

# Agentic Architecture Patterns

## Core Concepts

### 1. The `.agent/` Portable Brain
A standardized directory structure that works across any harness (Hermes, Claude Code, Cursor):
```
.agent/
├── AGENTS.md              # Entry guide
├── memory/
│   ├── personal/          # Stable user preferences
│   ├── working/           # Current task state + review queue
│   ├── semantic/          # Distilled lessons (LESSONS.md + lessons.jsonl)
│   └── episodic/          # Raw experience log (AGENT_LEARNINGS.jsonl)
├── skills/                # SKILL.md bundles with _manifest.jsonl
├── tools/                 # CLI utilities (recall.py, learn.py, graduate.py)
├── harness/               # Context assembly + hooks
└── protocols/             # Permissions + delegation rules
```

### 2. Experience Lifecycle (Dream Cycle)
```
Episodic Log → auto_dream.py (clustering) → Candidates → 
Host Agent Review (accept/reject) → Graduated Lessons → Recall
```
- **auto_dream.py**: Mechanical clustering of episodic entries into candidate patterns. No subjective judgment.
- **Review Queue**: Host agent reviews candidates in batch using `list_candidates.py`, `graduate.py`, `reject.py`.
- **Recall**: `recall.py "<intent>"` surfaces relevant graduated lessons before complex tasks.

### 3. Context Budgeting
Instead of injecting all memory, assemble context within a token budget:
- **Always-on**: PREFERENCES, permissions, WORKSPACE (cheap, safety-critical).
- **Query-matched**: Score episodes/lessons by lexical overlap + salience. Take top-k.
- **Skill triggers**: Load full SKILL.md only when triggers match the current task.

### 4. DESIGN.md as Contract
Portable visual system contract (9 sections: color, typography, spacing, layout, components, motion, voice, brand, anti-patterns).
- **Read-only by default**: Implementation consumes the contract; doesn't edit it.
- **71 built-in systems**: Linear, Stripe, Vercel, Airbnb, xiaohongshu, etc.
- **Validation**: `npx @google/design.md lint DESIGN.md` if available.

### 5. Prompt Stack Layering
Compose system prompt from layers:
```
DISCOVERY directives (question-form locking)
  + Identity charter (anti-slop rules)
  + Active DESIGN.md (if present)
  + Active SKILL.md (matched by triggers)
  + Project metadata
  + Top-k relevant lessons (by recall)
  + Always-on protocols (permissions)
```

## Implementation for Hermes

### Migration Steps
1. Create `~/.hermes/.agent/` structure mirroring agentic-stack.
2. Migrate existing gbrain pages to semantic/episodic layers.
3. Implement `auto_dream.py` adapted for gbrain Postgres data source.
4. Add `recall.py` to session start logic (query-aware lesson surfacing).

### Key Files to Port
- `harness/context_budget.py`: Query-aware context assembly.
- `tools/recall.py`: Lexical overlap scoring for lessons.
- `tools/learn.py`: One-shot lesson teaching.
- `memory/auto_dream.py`: Clustering + staging logic.

## Pitfalls
- **Don't hand-edit LESSONS.md**: It's rendered from lessons.jsonl. Use graduate/reject tools.
- **Dream cycle is mechanical**: No reasoning. Host agent does the judgment.
- **Context budget is hard**: If you exceed it, drop low-salience episodes first.
- **DESIGN.md is read-only**: Unless user explicitly asks for design system changes.

## References
- [open-design](https://github.com/nexu-io/open-design): Design engine patterns.
- [agentic-stack](https://github.com/codejunkie99/agentic-stack): Portable brain structure.