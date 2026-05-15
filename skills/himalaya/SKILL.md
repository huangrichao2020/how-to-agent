---
name: himalaya
description: CLI to manage emails via IMAP/SMTP. Use himalaya to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language).
version: 1.1.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Email, IMAP, SMTP, CLI, Communication]
    homepage: https://github.com/pimalaya/himalaya
prerequisites:
  commands: [himalaya]
---

# Himalaya Email CLI

Himalaya is a CLI email client that lets you manage emails from the terminal using IMAP, SMTP, Notmuch, or Sendmail backends.

## References

- `references/configuration.md` (config file setup + IMAP/SMTP authentication)
- `references/message-composition.md` (MML syntax for composing emails)

## Prerequisites

1. Himalaya CLI installed (`himalaya --version` to verify)
2. A configuration file at `~/.config/himalaya/config.toml`
3. IMAP/SMTP credentials configured (password stored securely)

### Installation

```bash
# Pre-built binary (Linux/macOS — recommended)
curl -sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh

# macOS via Homebrew
brew install himalaya

# Or via cargo (any platform with Rust)
cargo install himalaya --locked
```

## Configuration Setup

Run the interactive wizard to set up an account:

```bash
himalaya account configure
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

## Hermes Integration Notes

- **Reading, listing, searching, moving, deleting** all work directly through the terminal tool
- **Composing/replying/forwarding** — piped input (`cat << EOF | himalaya template send`) is recommended for reliability. Interactive `$EDITOR` mode works with `pty=true` + background + process tool, but requires knowing the editor and its commands
- Use `--output json` for structured output that's easier to parse programmatically
- The `himalaya account configure` wizard requires interactive input — use PTY mode: `terminal(command="himalaya account configure", pty=true)`

## Common Operations

### List Folders

```bash
himalaya folder list
```

### List Emails

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

### Search Emails

```bash
himalaya envelope list from john@example.com subject meeting
```

### Read an Email

Read email by ID (shows plain text):

```bash
himalaya message read 42
```

Export raw MIME:

```bash
himalaya message export 42 --full
```

### Reply to an Email

To reply non-interactively from Hermes, read the original message, compose a reply, and pipe it:

```bash
# Get the reply template, edit it, and send
himalaya template reply 42 | sed 's/^$/\nYour reply text here\n/' | himalaya template send
```

Or build the reply manually:

```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: sender@example.com
Subject: Re: Original Subject
In-Reply-To: <original-message-id>

Your reply here.
EOF
```

Reply-all (interactive — needs $EDITOR, use template approach above instead):

```bash
himalaya message reply 42 --all
```

### Forward an Email

```bash
# Get forward template and pipe with modifications
himalaya template forward 42 | sed 's/^To:.*/To: newrecipient@example.com/' | himalaya template send
```

### Write a New Email

**Non-interactive (use this from Hermes)** — pipe the message via stdin:

```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: recipient@example.com
Subject: Test Message

Hello from Himalaya!
EOF
```

Or with headers flag:

```bash
himalaya message write -H "To:recipient@example.com" -H "Subject:Test" "Message body here"
```

Note: `himalaya message write` without piped input opens `$EDITOR`. This works with `pty=true` + background mode, but piping is simpler and more reliable.

### Move/Copy Emails

Move to folder:

```bash
himalaya message move 42 "Archive"
```

Copy to folder:

```bash
himalaya message copy 42 "Important"
```

### Delete an Email

```bash
himalaya message delete 42
```

### Manage Flags

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

## 异常处理与故障排查

### 认证失败

| 错误现象 | 原因 | 解决方案 |
|----------|------|----------|
| `authentication failed` | 密码错误或 auth.cmd 返回为空 | 检查 `auth.cmd` 命令能否正确输出密码；手动运行 `pass show email/imap` 验证 |
| `connection refused` | IMAP/SMTP 服务不可达 | 检查网络连通性 `nc -zv imap.example.com 993`；确认 host/port 配置正确 |
| `TLS handshake failed` | 证书问题或加密类型不匹配 | 临时设置 `backend.encryption.type = "none"` 排查；或检查证书链 |

### 发送失败

| 错误现象 | 原因 | 解决方案 |
|----------|------|----------|
| `server refused to accept` | SMTP 服务器拒绝收件人地址 | 检查收件人邮箱格式；部分服务商禁止发送给外部地址 |
| `message too large` | 附件超出 SMTP 限制 | 一般限制 25MB，改用云存储链接替代附件 |
| `template send: no recipients` | MML 模板缺少 To/CC/BCC 头 | 确保模板至少包含一个 `To:` 头 |

### 超时处理

- IMAP 默认超时约 30 秒，大文件夹操作可能超时。可添加环境变量延长：`HIMALAYA_IMAP_TIMEOUT=60`
- 发送大量邮件时建议分批发送，每批间隔 5-10 秒避免触发速率限制
- 如果 `envelope list` 返回空但文件夹有邮件，可能是索引未更新，尝试 `himalaya folder refresh`

### 常见坑点

- **Message ID 是相对当前文件夹的**：切换文件夹后 ID 可能指向不同邮件，每次操作前重新确认
- **非 ASCII 字符编码**：中文邮件主题/正文可能出现乱码，确保 `--output json` 解析时正确处理 UTF-8
- **`auth.cmd` 必须只输出密码**：如果命令输出了额外文本（如 prompt），会导致认证失败，用 `pass show -q` 避免换行符
- **删除操作不可逆**：`message delete` 直接删除邮件，建议先用 `message move` 移到 Trash 目录

### 诊断命令

```bash
# 快速验证连接
himalaya account list

# 详细调试日志
RUST_LOG=debug himalaya envelope list

# 完整追踪（含堆栈）
RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list

# 验证配置语法
cat ~/.config/himalaya/config.toml | python3 -c "import sys, tomllib; tomllib.load(sys.stdin); print('OK')" 2>/dev/null || echo "配置有误"
```

### 降级方案

- 如果 himalaya CLI 不可用，可回退到 Python `imaplib` + `smtplib` 直接操作
- 如果 IMAP 连接失败，尝试切换加密模式：`tls` → `start-tls` → `none`（仅排查用）
- 对于不支持 OAuth2 的账户，可考虑使用应用专用密码替代主密码

## Debugging

Enable debug logging:

```bash
RUST_LOG=debug himalaya envelope list
```

Full trace with backtrace:

```bash
RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list
```

## Tips

- Use `himalaya --help` or `himalaya <command> --help` for detailed usage.
- Message IDs are relative to the current folder; re-list after folder changes.
- For composing rich emails with attachments, use MML syntax (see `references/message-composition.md`).
- Store passwords securely using `pass`, system keyring, or a command that outputs the password.
