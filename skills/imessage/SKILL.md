---
name: imessage
description: Send and receive iMessages/SMS via the imsg CLI on macOS.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [iMessage, SMS, messaging, macOS, Apple]
prerequisites:
  commands: [imsg]
---

# iMessage

Use `imsg` to read and send iMessage/SMS via macOS Messages.app.

## Prerequisites

- **macOS** with Messages.app signed in
- Install: `brew install steipete/tap/imsg`
- Grant Full Disk Access for terminal (System Settings → Privacy → Full Disk Access)
- Grant Automation permission for Messages.app when prompted

## When to Use

- User asks to send an iMessage or text message
- Reading iMessage conversation history
- Checking recent Messages.app chats
- Sending to phone numbers or Apple IDs

## When NOT to Use

- Telegram/Discord/Slack/WhatsApp messages → use the appropriate gateway channel
- Group chat management (adding/removing members) → not supported
- Bulk/mass messaging → always confirm with user first

## Quick Reference

### List Chats

```bash
imsg chats --limit 10 --json
```

### View History

```bash
# By chat ID
imsg history --chat-id 1 --limit 20 --json

# With attachments info
imsg history --chat-id 1 --limit 20 --attachments --json
```

### Send Messages

```bash
# Text only
imsg send --to "+141****1212" --text "Hello!"

# With attachment
imsg send --to "+141****1212" --text "Check this out" --file /path/to/image.jpg

# Force iMessage or SMS
imsg send --to "+141****1212" --text "Hi" --service imessage
imsg send --to "+141****1212" --text "Hi" --service sms
```

### Watch for New Messages

```bash
imsg watch --chat-id 1 --attachments
```

## Service Options

- `--service imessage` — Force iMessage (requires recipient has iMessage)
- `--service sms` — Force SMS (green bubble)
- `--service auto` — Let Messages.app decide (default)

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `command not found: imsg` | imsg not installed | `brew install steipete/tap/imsg` |
| `Permission denied` | No Full Disk Access | System Settings → Privacy → Full Disk Access → Terminal |
| `Messages.app is not running` | Messages.app not launched | Open Messages.app manually or via `open -a Messages` |
| `Chat not found` | Invalid chat-id or recipient | Run `imsg chats` to verify; use phone/Apple ID directly |
| `Failed to send` | Network issue or blocked contact | Check connectivity; verify recipient accepts messages |
| `Attachment not found` | Invalid file path | Verify path with `ls -la`; ensure file type is supported |
| `Automation permission denied` | macOS security blocking | System Settings → Privacy → Automation → allow Terminal |
| `JSON parse error` | imsg output format changed | Try without `--json`; check imsg version with `imsg --version` |

### Robust Send Pattern

```bash
#!/bin/bash
# Safe message send with validation

RECIPIENT="$1"
MESSAGE="$2"

# Validate inputs
if [ -z "$RECIPIENT" ] || [ -z "$MESSAGE" ]; then
    echo "Usage: $0 <recipient> <message>"
    exit 1
fi

# Check imsg is available
if ! command -v imsg &>/dev/null; then
    echo "ERROR: imsg not installed. Run: brew install steipete/tap/imsg"
    exit 1
fi

# Check Messages.app is running
if ! pgrep -x "Messages" >/dev/null 2>&1; then
    echo "WARNING: Messages.app not running, attempting to launch..."
    open -a Messages
    sleep 3
fi

# Verify recipient exists in contacts
imsg chats --limit 100 --json | grep -q "$RECIPIENT" || \
    echo "WARNING: Recipient not found in recent chats. Sending anyway..."

# Send message
imsg send --to "$RECIPIENT" --text "$MESSAGE"
if [ $? -eq 0 ]; then
    echo "✅ Message sent to $RECIPIENT"
else
    echo "❌ Failed to send message. Check connectivity and permissions."
    exit 1
fi
```

### Verification Before Send

```bash
# 1. Verify imsg is functional
imsg chats --limit 1 --json

# 2. Find recipient
imsg chats --limit 50 --json | jq '.[] | select(.displayName | contains("Mom"))'

# 3. Send with confirmation prompt
imsg send --to "+155****3456" --text "I'll be late"
```

## Rules

1. **Always confirm recipient and message content** before sending
2. **Never send to unknown numbers** without explicit user approval
3. **Verify file paths** exist before attaching
4. **Don't spam** — rate-limit yourself (max 1 message/3 seconds)
5. **Handle failures gracefully** — if send fails, notify user instead of retrying blindly

## Example Workflow

User: "Text mom that I'll be late"

```bash
# 1. Find mom's chat
imsg chats --limit 20 --json | jq '.[] | select(.displayName | contains("Mom"))'

# 2. Confirm with user: "Found Mom at +155****3456. Send 'I'll be late' via iMessage?"

# 3. Send after confirmation
imsg send --to "+155****3456" --text "I'll be late"
```
