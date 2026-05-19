# Feishu/Lark Docs

Research sources:

- `riba2534/feishu-cli`: broad Feishu CLI with Claude skills, Markdown import/export, writing, permissions, tables, diagrams, and document guide.
- `leemysw/feishu-docx`: lighter Feishu/Lark document export/write tool with Claude skill and WeChat article import/export.

## When To Use

Use Feishu docs for durable knowledge, work manuals, reports, handoffs, meeting
notes, architecture records, and collaborative documents.

## Tool Choice

- Use `feishu-cli` when you need full control: import, content update,
  permissions, sheets, wiki, diagrams, callouts, and large tables.
- Use `feishu-docx` when you need a simpler read/write/export path, especially
  exporting docs to Markdown or importing a WeChat article URL.

## Preferred Flow With feishu-cli

Create from Markdown:

```bash
python3 -c "d=open('/tmp/doc.md','rb').read(); assert b'\xef\xbf\xbd' not in d; d.decode('utf-8')"
feishu-cli doc import /tmp/doc.md --title "文档标题" --upload-images --verbose
```

Update existing docs:

```bash
feishu-cli doc content-update <document_id> --mode append --markdown-file /tmp/append.md
feishu-cli doc content-update <document_id> --mode replace_range --selection-by-title "## 旧章节" --markdown-file /tmp/new.md
```

Do not append when the user asked to replace a section.

## Markdown Compatibility

- Tables over 9 rows can stay one table via row insertion; very large tables
  should become Sheets.
- Mermaid/PlantUML can become editable Feishu boards, but keep diagrams simple.
- Callouts should use `NOTE`, `WARNING`, `TIP`, `CAUTION`, `IMPORTANT`, or
  `SUCCESS`.
- Images should be uploaded with explicit image handling.

## Verification

- Confirm document id or URL.
- Check owner/permission if the user needs access.
- For existing documents, export with block ids before precise updates.
- For high-stakes docs, export/read back to Markdown once.

## External Links

- https://github.com/riba2534/feishu-cli
- https://github.com/leemysw/feishu-docx

