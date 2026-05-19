# Tencent Docs

Research sources:

- Tencent Docs official OpenClaw scenario page: official token/skill entry.
- `liyang58/tencent-docs`: Tencent Docs MCP skill package with SmartCanvas,
  SmartSheet, Markdown creation, append, and management references.
- `easy-wx/qq-doc`: Python SDK for Tencent Docs API file import/export and
  permissions.

## When To Use

Use Tencent Docs when the target collaboration surface is docs.qq.com, when the
user asks for Tencent Docs specifically, or when the output should be an online
SmartCanvas/Word/Sheet/Mind/Flow document.

## Default Target

Prefer SmartCanvas for new narrative documents:

```bash
mcporter call "tencent-docs" "create_smartcanvas_by_markdown" --args '{"title":"标题","markdown":"# 标题\n\n正文"}'
```

Use Word only if the user needs traditional Word-like output. Use Excel/SmartSheet
for structured data.

## Current Gap

Tencent's official skill explains capability, not enough aesthetic layout.
Therefore treat layout as an empirical protocol:

1. Start from clean Markdown with stable headings.
2. Create a SmartCanvas preview.
3. Inspect the resulting document.
4. Record which Markdown patterns render well.
5. Promote proven patterns into this reference.

## SmartCanvas Layout Heuristics

- Use H1 only for title, H2 for major sections, H3 for local structure.
- Keep paragraphs short and avoid over-nested lists.
- Use tables for comparisons and schedules, not for decorative layout.
- Use block quotes for important emphasis.
- Put a short summary near the top when the doc is long.
- For reports, use: conclusion -> evidence -> details -> action items.

## Editing Existing Docs

Use SmartCanvas append/update tools when available. Prefer Markdown append for
new sections. Before editing important existing docs, read/search the document
or export if the tool supports it.

## External Links

- https://docs.qq.com/scenario/open-claw.html
- https://github.com/liyang58/tencent-docs
- https://github.com/easy-wx/qq-doc

