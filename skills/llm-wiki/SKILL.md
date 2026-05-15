---
name: llm-wiki
description: "Karpathy's LLM Wiki Agent — build, maintain, and query a persistent interlinked markdown knowledge base with automated health, lint, and graph tools."
version: 3.1.0
author: SamurAIGPT (adapted for Hermes)
license: MIT
metadata:
  hermes:
    tags: [wiki, knowledge-base, research, notes, markdown, rag-alternative]
    category: research
    related_skills: [obsidian, arxiv, agentic-research-ideas]
---

# LLM Wiki Agent

A personal knowledge base that builds and maintains itself. Drop in sources — the agent reads them, extracts knowledge, and maintains a persistent interlinked wiki. Works with any agent that reads this skill. Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and evolved by the open-source community.

**Division of labor:** The human curates sources and directs analysis. The agent reads, summarizes, cross-references, files, and maintains consistency.

## When This Skill Activates

Use this skill when the user:
- Asks to create, build, or start a wiki or knowledge base
- Asks to ingest, add, or process a source into their wiki
- Asks a question and an existing wiki is present at the configured path
- Asks to lint, audit, health-check, or build a knowledge graph for their wiki
- References their wiki, knowledge base, or "notes" in a research context

## Wiki Location

**Location:** Set via `WIKI_PATH` environment variable (e.g., in `~/.hermes/.env`).
If unset, defaults to `~/wiki`.

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
```

The wiki is just a directory of markdown files — open it in Obsidian, VS Code, or any editor.

## Architecture: Directory Layout

```
wiki/
├── index.md          # Catalog of all pages — update on every ingest
├── log.md            # Append-only chronological record
├── overview.md       # Living synthesis across all sources
├── sources/          # One summary page per source document
├── entities/         # People, companies, projects, products
├── concepts/         # Ideas, frameworks, methods, theories
└── syntheses/        # Saved query answers
graph/                # Auto-generated graph data (optional)
tools/                # Standalone Python scripts (included in skill assets)
  health.py           # Structural checks (deterministic, zero LLM calls)
  lint.py             # Content quality checks (uses LLM for semantic analysis)
  build_graph.py      # Knowledge graph generation
```

## Page Format

Every wiki page uses this frontmatter:

```yaml
---
title: "Page Title"
type: source | entity | concept | synthesis
tags: []
sources: []       # list of source slugs that inform this page
last_updated: YYYY-MM-DD
---
```

Use `[[PageName]]` or `[[filename|Display Name]]` wikilinks to link to other wiki pages.

## Core Workflows

### 1. Ingest Workflow
Triggered by: *"ingest <file/url>"*

**Steps:**
1. Read the source document fully. (Use `web_extract` for URLs).
2. Read `wiki/index.md` and `wiki/overview.md` for current wiki context.
3. Write `wiki/sources/<slug>.md` — include summary, key claims, quotes, and connections.
4. Update `wiki/index.md` — add entry under Sources section.
5. Update `wiki/overview.md` — revise synthesis if warranted.
6. Update/create entity pages for key people, companies, projects mentioned.
7. Update/create concept pages for key ideas and frameworks discussed.
8. Flag any contradictions with existing wiki content.
9. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <Title>`
10. **Post-ingest validation** — check for broken `[[wikilinks]]`, verify all new pages are in `index.md`, print a change summary.

### 2. Query Workflow
Triggered by: *"query: <question>"*

**Steps:**
1. Read `wiki/index.md` to identify relevant pages.
2. Read those pages using `read_file`.
3. Synthesize an answer with inline citations as `[[PageName]]` wikilinks.
4. Ask the user if they want the answer filed as `wiki/syntheses/<slug>.md`.

### 3. Health Workflow (Fast, Every Session)
Triggered by: *"health"*

Run: `python <skill_dir>/tools/health.py <wiki_path>`
Fast structural integrity checks — **zero LLM calls**, safe to run every session:
- **Empty / stub files** — pages with no content beyond frontmatter.
- **Index sync** — `wiki/index.md` entries vs actual files on disk.
- **Log coverage** — source pages missing a corresponding `ingest` entry in `wiki/log.md`.

### 4. Lint Workflow (Expensive, Periodic)
Triggered by: *"lint"*

Check for:
- **Orphan pages** — wiki pages with no inbound `[[links]]` from other pages.
- **Broken links** — `[[WikiLinks]]` pointing to pages that don't exist.
- **Contradictions** — claims that conflict across pages.
- **Stale summaries** — pages not updated after newer sources.
- **Missing entity pages** — entities mentioned in 3+ pages but lacking their own page.
- **Sparse pages** — pages with fewer than 2 outbound `[[wikilinks]]`.
Output a lint report and ask if the user wants it saved to `wiki/lint-report.md`.

### 5. Graph Workflow
Triggered by: *"build graph"*

Run: `python <skill_dir>/tools/build_graph.py <wiki_path>`
- Pass 1: Parses all `[[wikilinks]]` → deterministic `EXTRACTED` edges.
- Pass 2: Infers implicit relationships → `INFERRED` edges with confidence scores.
- Runs Louvain community detection.
- Outputs `graph/graph.json` + `graph/graph.html`.

## Resuming an Existing Wiki (CRITICAL)

When the user has an existing wiki, **always orient yourself before doing anything**:
1. **Read `SCHEMA.md` or `overview.md`** — understand the domain and conventions.
2. **Read `wiki/index.md`** — learn what pages exist and their summaries.
3. **Scan recent `wiki/log.md`** — read the last 20-30 entries to understand recent activity.

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
read_file "$WIKI/overview.md"
read_file "$WIKI/index.md"
read_file "$WIKI/log.md" offset=<last 30 lines>
```

Only after orientation should you ingest, query, or lint.

## Exception Handling & Pitfalls

### Source Fetch Failures
- **URL unreachable:** If `web_extract` fails, retry once with a 5-second delay. If still failing, report the URL as unreachable and skip ingestion — do not fabricate content.
- **File not found:** If the specified source file path doesn't exist, report clearly and suggest checking `WIKI_PATH` or listing available files.
- **Binary / non-text files:** Detect non-text encoding before reading. Skip PDFs, images, etc. with a clear message suggesting extraction first.

### Wiki Directory Issues
- **Wiki not initialized:** If `wiki/` doesn't exist or is empty, create the skeleton structure (`index.md`, `log.md`, `overview.md`, directories) before any operation.
- **Disk space full:** Before writing, check available disk space (`df -h`). If <100MB free, abort writes and warn the user.
- **Corrupted frontmatter:** If YAML parsing fails, attempt to repair by re-serializing with known-safe defaults. If unrepairable, skip the page and log it.
- **Concurrent modification:** If `index.md` or `log.md` is locked by another process, wait up to 10 seconds then retry. After 3 failures, report lock contention.

### Ingest Recovery
- **Partial ingest failure:** If the ingest crashes mid-way (e.g., after writing source but before updating index), run a self-recovery check: scan `sources/` for entries not in `index.md` and backfill them.
- **Duplicate slug collision:** If a source with the same slug already exists, append a timestamp suffix (e.g., `my-article-20260515.md`) instead of overwriting.
- **LLM context overflow:** If the source document exceeds context window, chunk it into sections, ingest each chunk separately, and merge summaries.

### Query Failures
- **No relevant pages found:** If `index.md` has no matches for the query, search all pages with keyword matching as fallback. If still nothing found, say "wiki has no relevant information" — do not fabricate.
- **Contradictory information:** If two wiki pages contain conflicting claims, surface both with citations and flag the contradiction for human review.

### Tool Failures
- **health.py/lint.py crash:** If the tool script exits with non-zero, capture stderr, report the error, and continue with manual checks where possible.
- **build_graph.py memory error:** For large wikis (>500 pages), build_graph may OOM. Limit to top 200 pages by inbound link count, or use streaming mode if available.
- **networkx missing:** If `networkx` not installed, skip graph-aware lint checks and report gracefully.

### Working with the Wiki

#### Bulk Ingest
When ingesting multiple sources at once, batch the updates:
1. Read all sources first.
2. Identify all entities and concepts across all sources.
3. Check existing pages for all of them (one search pass, not N).
4. Create/update pages in one pass.
5. Update `index.md` once at the end.
6. Write a single log entry covering the batch.

#### Archiving
When content is fully superseded:
1. Move the page to `_archive/` with its original path.
2. Remove from `index.md`.
3. Update any pages that linked to it — replace wikilink with plain text + "(archived)".
4. Log the archive action.

### General Safety Rules
- **Never modify files in `raw/`** — sources are immutable.
- **Always update `index.md` and `log.md`** — skipping this makes the wiki degrade.
- **Don't create pages for passing mentions** — follow the Page Thresholds. A name appearing once doesn't warrant an entity page.
- **Keep pages scannable** — a wiki page should be readable in 30 seconds. Split pages over 200 lines.
- **Backup before bulk operations** — before any operation that modifies >5 files, snapshot the wiki directory.
