---
name: himalaya
description: "CLI to manage emails via IMAP/SMTP. Use `himalaya` to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language)."
homepage: https://github.com/pimalaya/himalaya
category: communication
categories:
  - communication
  - email
metadata:
  builtin_skill_version: "1.2"
  copaw:
    emoji: "📧"
    requires:
      bins:
        - himalaya
    install:
      - id: brew
        kind: brew
        formula: himalaya
        bins:
          - himalaya
        label: "Install Himalaya (brew)"
---
# Himalaya Email CLI

Himalaya is a CLI email client that lets you manage emails from the terminal using IMAP, SMTP, Notmuch, or Sendmail backends.

## References

- `references/configuration.md` (config file setup + IMAP/SMTP authentication)

## Prerequisites

1. **Himalaya CLI** — the `himalaya` binary must already be on `PATH`. Check with `himalaya --version`.
   - **Recommended: v1.2.0 or newer.** Older releases can fail against some IMAP servers; v1.2.0+ includes related fixes.
2. A configuration file at `~/.config/himalaya/config.toml`
3. IMAP/SMTP credentials configured (password stored securely)

## Pre-flight Checklist

Before any operation, run through this checklist:

```bash
# 1. Version check
himalaya --version   # Must be >= 1.2.0

# 2. Config exists
ls ~/.config/himalaya/config.toml

# 3. Auth command works
# (Replace with whatever your auth.cmd is configured to)
pass show email/imap 2>/dev/null && echo "✅ Auth OK" || echo "❌ Auth broken"

# 4. Account loaded
himalaya account list

# 5. IMAP connection alive
himalaya folder list
```

If any step fails, see [Troubleshooting Quick Reference](#troubleshooting-quick-reference) below.

## Configuration Setup

Run the interactive wizard to set up an account (replace `default` with any name you want, e.g. `gmail`, `work`):

```bash
himalaya account configure default
```

Or create `~/.config/himalaya/config.toml` manually:

```toml
[accounts.personal]
email = "you@example.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@example.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show email/imap"  # or use keyring

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@example.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show email/smtp"
```

If you are using 163 mail account, add `backend.extensions.id.send-after-auth = true` in the config file to ensure proper functionality.

## Common Operations

### 步骤 1: 列出文件夹

```bash
himalaya folder list
```

### 步骤 2: 列出邮件

List emails in INBOX (default):

```bash
himalaya envelope list
```

List emails in a specific folder:

```bash
himalaya envelope list --folder "Sent"
```

List with pagination:

```bash
himalaya envelope list --page 1 --page-size 20
```

If meet with error, try:

```bash
himalaya envelope list -f INBOX -s 1
```

### 步骤 3: 搜索邮件

```bash
himalaya envelope list from john@example.com subject meeting
```

### 步骤 4: 读取邮件

Read email by ID (shows plain text):

```bash
himalaya message read 42
```

Export raw MIME:

```bash
himalaya message export 42 --full
```

### 步骤 5: 发送邮件

**Recommended approach:** Use `template write | template send` pipeline for simple emails.

**Send a simple email:**

```bash
export EDITOR=cat
himalaya template write \
  -H "To: recipient@example.com" \
  -H "Subject: Email Subject" \
  "Email body content" | himalaya template send
```

**Send with multiple headers:**

```bash
export EDITOR=cat
himalaya template write \
  -H "To: recipient@example.com" \
  -H "Cc: cc@example.com" \
  -H "Subject: Email Subject" \
  "Email body content" | himalaya template send
```

**Send with attachments (using Python):**

For emails with attachments, use Python's `smtplib` and `email.mime` modules:

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

msg = MIMEMultipart()
msg['From'] = 'sender@163.com'
msg['To'] = 'recipient@example.com'
msg['Subject'] = 'Email with attachment'

msg.attach(MIMEText('Email body', 'plain'))

# Add attachment
with open('/path/to/file.pdf', 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename=\"file.pdf\"')
    msg.attach(part)

server = smtplib.SMTP_SSL('smtp.163.com', 465)
server.login('sender@163.com', 'password')
server.send_message(msg)
server.quit()
```

**⚠️ MML attachment limitations:** The `template send` command with MML format may fail with "cannot parse MML message: empty body" when using multipart/attachments. This is a known issue in himalaya v1.1.0. Use Python approach for attachments.

**⚠️ Avoid `message write` for automation:** The `himalaya message write` command requires interactive TUI selection (Edit/Discard/Quit) and will hang in non-interactive environments.

**⚠️ `message send` limitations:** Direct `himalaya message send <raw_email>` may fail with "cannot send message without a recipient" due to header parsing issues. Use `template send` instead.

**Configuration requirement:** Ensure `message.send.save-to-folder` is set in config.toml to avoid "Folder not exist" errors:

```toml
[accounts.163]
# ... other config ...
message.send.save-to-folder = "Sent"
```

For 163 mail accounts, create the Sent folder first if it doesn't exist:

```bash
himalaya folder create Sent
```

### 步骤 6: 管理邮件（移动/复制/删除/标记）

Move to folder:

```bash
himalaya message move 42 "Archive"
```

Copy to folder:

```bash
himalaya message copy 42 "Important"
```

Delete an email:

```bash
himalaya message delete 42
```

Add flag:

```bash
himalaya flag add 42 --flag seen
```

Remove flag:

```bash
himalaya flag remove 42 --flag seen
```

## Multiple Accounts

List accounts:

```bash
himalaya account list
```

Use a specific account:

```bash
himalaya --account work envelope list
```

## Attachments

Save attachments from a message:

```bash
himalaya attachment download 42
```

Save to specific directory:

```bash
himalaya attachment download 42 --dir ~/Downloads
```

## Output Formats

Most commands support `--output` for structured output:

```bash
himalaya envelope list --output json
himalaya envelope list --output plain
```

## Debugging

Enable debug logging:

```bash
RUST_LOG=debug himalaya envelope list
```

Full trace with backtrace:

```bash
RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list
```

## Troubleshooting Quick Reference

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| `connection refused` / `timeout` | Wrong IMAP/SMTP host or port | Verify host/port: IMAP TLS=993, SMTP TLS=465, SMTP STARTTLS=587 |
| `LOGIN failed` | Wrong password or needs app-specific password | Gmail/163/QQ require app-specific passwords, not account passwords |
| `TLS handshake failed` | Non-standard TLS (common with Chinese providers) | Last resort: add `backend.extensions.insecure = true` (warn user about security) |
| `config file not found` | No config at `~/.config/himalaya/config.toml` | Run `himalaya account configure default` or create manually |
| `Folder not exist` | `message.send.save-to-folder` not set or folder missing | Set in config; run `himalaya folder create Sent` for 163 mail |
| `message not found` | Message ID expired (folder-scoped + session-scoped) | Re-run `envelope list` to refresh IDs |
| `cannot send message without a recipient` | Header parsing issue in `message send` | Use `template write \| template send` pipeline instead |
| `cannot parse MML message: empty body` | MML multipart bug in v1.1.0 | Use Python smtplib for attachments |
| SMTP 550 | Recipient address rejected by receiving server | Not a himalaya issue; verify recipient address |
| SMTP 421/451 | Temporary server overload | Retry after 30s, max 3 retries |
| `envelope list` very slow | Large mailbox (>10K emails) | Always use `--page` and `--page-size` |
| `folder list` empty/hangs | Server LIST command not fully supported | Try `himalaya folder list --output json` |
| Commands work intermittently | IMAP server rate-limiting | Add 2-3s delay between consecutive himalaya commands |
| TOML syntax error / cryptic failure | Invalid config.toml | Validate: `python3 -c "import tomllib; tomllib.load(open('~/.config/himalaya/config.toml', 'rb'))"` |

## 注意 / Pitfalls

- **注意**: Message IDs are folder-scoped and session-scoped. Always re-run `envelope list` before operating on a message ID.
- **注意**: 163 mail accounts need `backend.extensions.id.send-after-auth = true` in config.
- **注意**: Avoid `message write` in automation — it requires interactive TUI and will hang.
- **注意**: Use English folder names (e.g., "Sent" not "已发送") for better IMAP compatibility.
- **注意**: For large mailboxes (>10K emails), always use `--page` and `--page-size` to avoid timeout.
- **坑**: MML attachment sending fails in v1.1.0 — use Python smtplib as fallback.
- **坑**: `message send` may fail with "cannot send message without a recipient" — use `template send` as fallback.

## Tips

- Use `himalaya --help` or `himalaya <command> --help` for detailed usage.
- Message IDs are relative to the current folder; re-list after folder changes.
- For composing rich emails with attachments, use MML syntax (see `references/message-composition.md`).
- Store passwords securely using `pass`, system keyring, or a command that outputs the password.
- **For automation:** Always use `template write | template send` pipeline with `export EDITOR=cat`.
- **163 Mail users:** Set `backend.extensions.id.send-after-auth = true` and `message.send.save-to-folder = "Sent"` in config.
- **Folder names:** Use English folder names (e.g., "Sent" instead of "已发送") for better compatibility.

## Exception handling & troubleshooting

**Connection & authentication failures:**
- If `himalaya envelope list` fails with "connection refused" or "timeout" → verify IMAP/SMTP host and port. Common ports: IMAP TLS=993, SMTP TLS=465, SMTP STARTTLS=587.
- If authentication fails with "LOGIN failed" → check if the mail provider requires an app-specific password (Gmail, 163 mail, QQ mail all require this). Regular account passwords will not work.
- If TLS handshake fails → some providers (especially Chinese ones) use non-standard TLS. Try adding `backend.extensions.insecure = true` as a last resort, but warn the user about security implications.

**IMAP server compatibility:**
- If commands work intermittently → the IMAP server may be rate-limiting. Add a 2-3 second delay between consecutive himalaya commands in automation scripts.
- If `folder list` returns empty or hangs → the server may not support the LIST command properly. Try `himalaya folder list --output json` as an alternative format.
- If mailbox is very large (>10K emails) → `envelope list` without pagination will be extremely slow. Always use `--page` and `--page-size` for large mailboxes.

**Message ID staleness:**
- Message IDs are folder-scoped and session-scoped. If you switch folders or the IMAP session refreshes, old IDs become invalid. Always re-run `envelope list` before operating on a message ID.
- If `message read 42` returns "message not found" → the message may have been moved/deleted by another client, or the folder was re-synced. Re-list the folder to get current IDs.

**Send failures beyond known issues:**
- If `template send` fails with SMTP error 550 → the recipient address was rejected by the receiving server. This is not a himalaya issue; verify the recipient address.
- If `template send` fails with SMTP error 421/451 → temporary server overload. Retry after 30 seconds. Max 3 retries.
- If `template send` succeeds but the email doesn't appear in Sent folder → check `message.send.save-to-folder` config. Some providers use different folder names ("Sent Items" vs "Sent" vs "已发送").

**Config file issues:**
- If himalaya reports "config file not found" → run `himalaya account configure default` to generate one, or create `~/.config/himalaya/config.toml` manually.
- If config file has TOML syntax errors → himalaya will fail silently or with cryptic errors. Validate TOML syntax before using: `python3 -c "import tomllib; tomllib.load(open('~/.config/himalaya/config.toml', 'rb'))"`.
- If switching providers (e.g. from 163 to Gmail) → back up the old config first: `cp ~/.config/himalaya/config.toml ~/.config/himalaya/config.toml.bak`.

**Debugging checklist (when things go wrong):**
1. `himalaya --version` — verify version (recommended: v1.2.0+)
2. `himalaya account list` — verify accounts are loaded
3. `himalaya folder list` — verify IMAP connection works
4. `RUST_LOG=debug himalaya envelope list` — enable debug output
5. `RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list` — full trace for deep debugging
6. Check `~/.config/himalaya/config.toml` for typos or missing fields
7. Verify the auth command works independently: `pass show email/imap` (or whatever auth.cmd is set to)
