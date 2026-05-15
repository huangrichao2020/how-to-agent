---
name: apple-reminders
description: Manage Apple Reminders via remindctl CLI (list, add, complete, delete).
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Reminders, tasks, todo, macOS, Apple]
prerequisites:
  commands: [remindctl]
---

# Apple Reminders

Use `remindctl` to manage Apple Reminders directly from the terminal. Tasks sync across all Apple devices via iCloud.

## Prerequisites

- **macOS** with Reminders.app
- Install: `brew install steipete/tap/remindctl`
- Grant Reminders permission when prompted
- Check: `remindctl status` / Request: `remindctl authorize`

## When to Use

- User mentions "reminder" or "Reminders app"
- Creating personal to-dos with due dates that sync to iOS
- Managing Apple Reminders lists
- User wants tasks to appear on their iPhone/iPad

## When NOT to Use

- Scheduling agent alerts → use the cronjob tool instead
- Calendar events → use Apple Calendar or Google Calendar
- Project task management → use GitHub Issues, Notion, etc.
- If user says "remind me" but means an agent alert → clarify first

## Quick Reference

### View Reminders

```bash
remindctl                    # Today's reminders
remindctl today              # Today
remindctl tomorrow           # Tomorrow
remindctl week               # This week
remindctl overdue            # Past due
remindctl all                # Everything
remindctl 2026-01-04         # Specific date
```

### Manage Lists

```bash
remindctl list               # List all lists
remindctl list Work          # Show specific list
remindctl list Projects --create    # Create list
remindctl list Work --delete        # Delete list
```

### Create Reminders

```bash
remindctl add "Buy milk"
remindctl add --title "Call mom" --list Personal --due tomorrow
remindctl add --title "Meeting prep" --due "2026-02-15 09:00"
```

### Complete / Delete

```bash
remindctl complete 1 2 3          # Complete by ID
remindctl delete 4A83 --force     # Delete by ID
```

### Output Formats

```bash
remindctl today --json       # JSON for scripting
remindctl today --plain      # TSV format
remindctl today --quiet      # Counts only
```

## Date Formats

Accepted by `--due` and date filters:
- `today`, `tomorrow`, `yesterday`
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:mm`
- ISO 8601 (`2026-01-04T12:34:56Z`)

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `command not found: remindctl` | remindctl not installed | `brew install steipete/tap/remindctl` |
| `Permission denied` / `Authorization failed` | No Reminders access | Run `remindctl authorize`; grant in System Settings → Privacy → Reminders |
| `List 'X' not found` | Typo in list name or list doesn't exist | Run `remindctl list` to see available lists |
| `Invalid date format` | Unrecognized date string | Use `YYYY-MM-DD` or natural language like `tomorrow` |
| `ID not found` | Reminder already completed/deleted or wrong ID | Use `remindctl all --json` to verify IDs |
| `iCloud sync delay` | Reminders not appearing on other devices | Wait 1-2 min; check iCloud status in System Settings |
| `remindctl status: error` | Reminders.app not running or DB locked | Open Reminders.app; restart if stuck |

### Robust Reminder Creation

```bash
#!/bin/bash
# Safe reminder creation with validation

create_reminder() {
    local title="$1"
    local list="${2:-}"
    local due="${3:-}"
    
    # Validate remindctl
    if ! command -v remindctl &>/dev/null; then
        echo "ERROR: remindctl not installed."
        return 1
    fi
    
    # Check authorization
    if ! remindctl status &>/dev/null; then
        echo "WARNING: Authorization issue. Running authorize..."
        remindctl authorize
    fi
    
    # Build command
    local cmd="remindctl add --title \"$title\""
    [ -n "$list" ] && cmd="$cmd --list \"$list\""
    [ -n "$due" ] && cmd="$cmd --due \"$due\""
    
    # Execute
    eval $cmd
    if [ $? -eq 0 ]; then
        echo "✅ Reminder created: '$title'"
    else
        echo "❌ Failed to create reminder. Check list name and date format."
        return 1
    fi
}

# Usage: create_reminder "Buy milk" "Personal" "tomorrow 10:00"
```

### Safe ID-based Operations

```bash
# Always verify ID exists before completing/deleting
remindctl all --json | jq '.[] | select(.id == "4A83")'

# Complete with confirmation
ID="4A83"
remindctl all --json | jq -e ".[] | select(.id == \"$ID\")" >/dev/null && \
    remindctl complete "$ID" || echo "ID $ID not found"
```

## Rules

1. When user says "remind me", clarify: Apple Reminders (syncs to phone) vs agent cronjob alert
2. Always confirm reminder content and due date before creating
3. Use `--json` for programmatic parsing
4. Verify list names exist before creating reminders in specific lists
