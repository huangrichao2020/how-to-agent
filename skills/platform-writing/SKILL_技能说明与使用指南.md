---
name: platform-writing
description: Use when writing, polishing, formatting, or publishing long-form content for WeChat Official Account, Feishu/Lark Docs, or Tencent Docs. Separates writing quality from platform layout and chooses the right tool path.
---

# Platform Writing

Use this skill when the user wants a public article, Feishu document, Tencent
Doc, writing draft, platform-specific polish, or a reusable writing workflow.

## Core Idea

Write once, land differently.

```text
content intent -> writing structure -> platform layout -> tool execution -> preview/verify
```

Do not let a platform API decide the article. First produce a strong content
shape, then map it to the target platform.

## Writing Core

Before choosing tools, answer four questions:

1. **Reader**: who is this for, and what do they already believe?
2. **Promise**: what will they get by reading?
3. **Memory**: what one sentence should remain after reading?
4. **Action**: what should they do next?

Then draft with this spine:

```text
hook -> context -> main claim -> evidence/story -> method/framework -> payoff -> next action
```

Use the user's real voice when available. If the text feels generic, increase
concreteness: names, scenes, numbers, before/after contrast, and lived detail.

## Platform Choice

| Target | Primary job | Default tool path |
|---|---|---|
| WeChat Official Account | reader attention, phone readability, sharing, follow/convert | `md2wechat` flow |
| Feishu/Lark Docs | durable knowledge, collaboration, traceability, structured handoff | `feishu-cli` or `feishu-docx` flow |
| Tencent Docs | online document creation, SmartCanvas polish, lightweight collaboration | Tencent Docs MCP/OpenClaw flow |

Read only the relevant reference:

- WeChat: `references/wechat-official-account.md`
- Feishu/Lark Docs: `references/feishu-docs.md`
- Tencent Docs: `references/tencent-docs.md`

## Layout Rule

The same Markdown should not be blindly reused across platforms:

- WeChat needs stronger first-screen promise, shorter paragraphs, more visual
  rhythm, and explicit conversion modules.
- Feishu needs stable headings, tables, callouts, diagrams, permissions, and
  export/update friendliness.
- Tencent Docs should prefer SmartCanvas for new docs and learn layout by
  previewing real output, because the official skill is capability-rich but
  light on aesthetic rules.

## Verification

Always do at least one of:

- local preview or inspect command;
- export/read-back after writing;
- block ID check before updating an existing document;
- user-visible link plus permission check.

Do not publish, create a draft, or write to a shared document unless the user
asked for that side effect.

