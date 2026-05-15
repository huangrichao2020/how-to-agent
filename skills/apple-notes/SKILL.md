---
name: apple-notes
description: Manage Apple Notes via the memo CLI on macOS (create, view, search, edit).
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Notes, Apple, macOS, note-taking]
    related_skills: [obsidian]
prerequisites:
  commands: [memo]
---

# Apple Notes

Use `memo` to manage Apple Notes directly from the terminal. Notes sync across all Apple devices via iCloud.

## Prerequisites

- **macOS** with Notes.app
- Install: `brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`
- Grant Automation access to Notes.app when prompted (System Settings → Privacy → Automation)

## When to Use

- User asks to create, view, or search Apple Notes
- Saving information to Notes.app for cross-device access
- Organizing notes into folders
- Exporting notes to Markdown/HTML

## When NOT to Use

- Obsidian vault management → use the `obsidian` skill
- Bear Notes → separate app (not supported here)
- Quick agent-only notes → use the `memory` tool instead

## Quick Reference

### View Notes

```bash
memo notes                        # List all notes
memo notes -f "Folder Name"       # Filter by folder
memo notes -s "query"             # Search notes (fuzzy)
```

### Create Notes

```bash
memo notes -a                     # Interactive editor
memo notes -a "Note Title"        # Quick add with title
```

### Edit Notes

```bash
memo notes -e                     # Interactive selection to edit
```

### Delete Notes

```bash
memo notes -d                     # Interactive selection to delete
```

### Move Notes

```bash
memo notes -m                     # Move note to folder (interactive)
```

### Export Notes

```bash
memo notes -ex                    # Export to HTML/Markdown
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `command not found: memo` | memo not installed | `brew tap antoniorodr/memo && brew install antoniorodr/memo/memo` |
| `Automation permission denied` | macOS blocks Notes access | System Settings → Privacy → Automation → grant terminal |
| `Notes.app is not running` | Notes.app not launched | Open Notes.app: `open -a Notes` |
| `Folder not found` | Folder name doesn't exist | Run `memo notes` to list folders; use exact name |
| `Cannot edit note with images` | Note contains attachments | Use Notes.app GUI for rich-content notes |
| `Interactive prompt hangs` | Non-interactive terminal | Use `pty=true` for terminal; pipe input via stdin |
| `iCloud sync delay` | Changes not visible on other devices | Wait 1-2 min; verify iCloud Notes is enabled |
| `Export fails (HTML/Markdown)` | Note has unsupported content | Skip rich-media notes; use `memo notes -ex --plain` |

### Robust Note Creation

```bash
#!/bin/bash
# Safe note creation with validation

create_note() {
    local title="$1"
    local folder="${2:-}"
    
    # Validate memo
    if ! command -v memo &>/dev/null; then
        echo "ERROR: memo not installed."
        echo "Run: brew tap antoniorodr/memo && brew install antoniorodr/memo/memo"
        return 1
    fi
    
    # Verify Notes.app is running
    if ! pgrep -x "Notes" >/dev/null 2>&1; then
        echo "Launching Notes.app..."
        open -a Notes
        sleep 3
    fi
    
    # Create note
    if [ -n "$folder" ]; then
        memo notes -a "$title" -f "$folder"
    else
        memo notes -a "$title"
    fi
    
    if [ $? -eq 0 ]; then
        echo "✅ Note created: '$title'"
    else
        echo "❌ Failed to create note. Check folder name and permissions."
        return 1
    fi
}

# Usage: create_note "Meeting Notes" "Work"
```

### Safe Search with Fallback

```bash
# Search with graceful fallback if no results
search_notes() {
    local query="$1"
    local result
    result=$(memo notes -s "$query" 2>&1)
    
    if [ $? -ne 0 ]; then
        echo "Search failed. Try a broader query."
        return 1
    fi
    
    if [ -z "$result" ]; then
        echo "No notes found for '$query'"
        echo "Available folders:"
        memo notes | head -20
        return 1
    fi
    
    echo "$result"
}
```

## Limitations

- Cannot edit notes containing images or attachments
- Interactive prompts require terminal access (use pty=true if needed)
- macOS only — requires Apple Notes.app

## Rules

1. Prefer Apple Notes when user wants cross-device sync (iPhone/iPad/Mac)
2. Use the `memory` tool for agent-internal notes that don't need to sync
3. Use the `obsidian` skill for Markdown-native knowledge management
4. Verify folder names exist before creating notes in specific folders
