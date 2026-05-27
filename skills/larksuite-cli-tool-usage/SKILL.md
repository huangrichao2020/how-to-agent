---
name: larksuite-cli-tool-usage
description: "Use when Hermes needs to accomplish work with lark-cli: search or update docs, send/read IM messages, manage calendar, tasks, sheets, wiki, drive, mail, approvals, whiteboards, or call raw Feishu OpenAPI. Focuses on schema-first tool use, identity selection, pagination, dry-run safety, and permission handling."
yao_category: "AI工作"
---

# LarkSuite CLI Tool Usage

This skill teaches how to use `lark-cli` as a Feishu/Lark tool. It is not an installation guide.

## Core Loop

1. Map the user goal to a domain: `im`, `docs`, `calendar`, `sheets`, `drive`, `wiki`, `task`, `mail`, `base`, `approval`, `contact`, `vc`, `minutes`, `whiteboard`, or raw `api`.
2. Select identity:
   - `--as user` for personal docs, calendar, drive, mail, tasks, and resources owned by the user.
   - `--as bot` for app-owned resources, bot messages, and application-level operations.
3. Inspect help before guessing:

```bash
lark-cli <domain> --help
lark-cli <domain> <command> --help
```

4. Inspect schema before low-level API calls:

```bash
lark-cli schema <service.resource.method> --format pretty
```

5. Use `--dry-run` for write/update/delete/send operations when supported.
6. Report concise evidence: command shape, identity, resource id/url, and result.

## Command Shapes

High-level helpers:

```bash
lark-cli calendar +agenda --as user
lark-cli docs +search --query "keyword" --as user --page-size 20
lark-cli docs +fetch --api-version v2 --doc "<doc_url_or_token>" --as user
lark-cli task +get-my-tasks --as user --page-all
```

Structured wrapper:

```bash
lark-cli calendar events instance_view \
  --params '{"calendar_id":"primary","start_time":"1700000000","end_time":"1700086400"}' \
  --as user
```

Raw OpenAPI fallback:

```bash
lark-cli api GET /open-apis/calendar/v4/calendars --as user
lark-cli api POST /open-apis/im/v1/messages \
  --params '{"receive_id_type":"chat_id"}' \
  --data '{"receive_id":"<chat_id>","msg_type":"text","content":"{\"text\":\"hello\"}"}' \
  --as bot
```

Use raw `api` only when no domain command or helper exists.

## Feishu Document Reading Rule

When the user gives a Feishu/Lark `/docx/` or `/wiki/` URL and asks Hermes to read, learn, summarize, or extract the document, use `lark-cli docs +fetch --api-version v2` first. Do not start with browser tabs, page scrolling, DOM scraping, screenshots, or web automation unless `docs +fetch` fails.

Recommended first pass:

```bash
lark-cli docs +fetch --api-version v2 --doc "<doc_url_or_token>" --scope outline --max-depth 3 --as user
lark-cli docs +fetch --api-version v2 --doc "<doc_url_or_token>" --doc-format markdown --as user
```

## Output Control

```bash
lark-cli <domain> <command> --format json
lark-cli <domain> <command> --jq '.data'
lark-cli <domain> <command> --page-all --page-limit 10 --page-size 50
```

Use `-o <path>` for binary downloads.

## Permission Handling

For user authorization, run the narrowest login and send the generated URL to the user:

```bash
lark-cli auth login --domain calendar
lark-cli auth login --scope "<missing_scope>"
```

For bot permission failures, do not run user auth. Give the user the developer-console URL and missing scopes from the error output.

## Safety

- Never expose `appSecret`, access tokens, or refresh tokens.
- Confirm target resource before write/delete/send operations.
- Do not invent document tokens, chat IDs, or scopes. Discover them with `lark-cli`.
- Summarize large JSON instead of pasting it into chat.

## Common Workflows

Read a document:

```bash
lark-cli docs +search --query "<keywords>" --as user --page-size 20
lark-cli docs +fetch --api-version v2 --doc "<doc_url_or_token>" --as user
```

Append to a document:

```bash
lark-cli docs +create --api-version v2 --title "<title>" --markdown "<initial_markdown>" --as user
lark-cli docs +update --api-version v2 --doc "<doc_token>" --mode append --markdown "<markdown>" --as user --dry-run
lark-cli docs +update --api-version v2 --doc "<doc_token>" --mode append --markdown "<markdown>" --as user
```

Calendar:

```bash
lark-cli calendar +agenda --as user
lark-cli calendar +create --help
```

Messages:

```bash
lark-cli im --help
lark-cli im messages --help
lark-cli api POST /open-apis/im/v1/messages \
  --params '{"receive_id_type":"chat_id"}' \
  --data '{"receive_id":"<chat_id>","msg_type":"text","content":"{\"text\":\"hello\"}"}' \
  --dry-run --as bot
```

Sheets:

```bash
lark-cli sheets --help
lark-cli schema sheets.spreadsheets.get --format pretty
```
