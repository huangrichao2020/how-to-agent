---
name: obsidian
description: Read, search, create, and manage notes in the Obsidian vault with proper error handling and best practices.
version: 1.1.0
---

# Obsidian Vault

**Location:** Set via `OBSIDIAN_VAULT_PATH` environment variable (e.g., in `~/.hermes/.env`).

If unset, defaults to `~/Documents/Obsidian Vault`.

> ⚠️ Vault paths may contain spaces — always quote them in shell commands.

## Pre-flight checks

Before operating on the vault:
```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# Verify vault exists and is accessible
if [ -d "$VAULT" ]; then
  echo "Vault found: $VAULT"
else
  echo "⚠️ Vault not found at $VAULT"
  echo "Set OBSIDIAN_VAULT_PATH or create the directory"
fi
```

## Read a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
cat "$VAULT/Note Name.md"
```

## List notes

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# All notes recursively
find "$VAULT" -name "*.md" -type f

# Notes in a specific folder
ls "$VAULT/Subfolder/"

# Recently modified notes (last 7 days)
find "$VAULT" -name "*.md" -mtime -7 -type f
```

## Search

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# By filename (case-insensitive)
find "$VAULT" -name "*.md" -iname "*keyword*"

# By content (case-insensitive, show file + line)
grep -rni "keyword" "$VAULT" --include="*.md"

# By content with context (3 lines before/after)
grep -rni -C 3 "keyword" "$VAULT" --include="*.md"
```

## Create a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# Ensure parent directory exists
mkdir -p "$VAULT/Subfolder"

# Create with write_file (preferred) or heredoc
cat > "$VAULT/Subfolder/New Note.md" << 'ENDNOTE'
# Title

Content here.
ENDNOTE
```

## Append to a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
echo "
New content here." >> "$VAULT/Existing Note.md"
```

## Update a note (safe replace)

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# Backup first
cp "$VAULT/Note.md" "$VAULT/Note.md.bak"

# Then use sed/patch or rewrite the file
```

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes:
- Use wikilinks to connect related content
- If the target note doesn't exist, Obsidian will show it as a "missing link" — this is normal
- For cross-folder links, use `[[Folder/Note Name]]` format

## Error handling & recovery

| Symptom | Cause | Fix |
|---|---|---|
| Vault not found | `OBSIDIAN_VAULT_PATH` unset + default path doesn't exist | Set env var in `~/.hermes/.env` or create default directory |
| Permission denied | Vault directory owned by another user | `chown -R $USER "$VAULT"` or adjust permissions |
| Note not found after creation | Path typo or unquoted spaces in path | Always quote `$VAULT` and use exact filenames |
| Duplicate note created | Note with same name already exists | Use `test -f "$VAULT/Note.md"` before creating; offer to append or rename |
| Search returns nothing | Wrong vault path or no `.md` files | Verify path; check for alternative extensions (`.mdx`, `.txt`) |
| Corrupted note content | Concurrent edits or interrupted writes | Restore from `.bak` if available; check for lock files |
| Symlinked attachments broken | Attachments stored outside vault | Update paths or copy attachments into vault directory |

### Safe modification workflow
1. **Always backup** before modifying: `cp note.md note.md.bak`
2. **Verify** the note exists before editing: `test -f "$VAULT/Note.md"`
3. **Create directories** as needed: `mkdir -p "$VAULT/Subfolder"`
4. **Confirm changes** after editing: read back the file to verify

## Best practices

- **Naming**: Use Title Case for note names to match Obsidian conventions
- **Tags**: Add `#tags` at the top or bottom of notes for discoverability
- **Frontmatter**: Use YAML frontmatter (`---`) for metadata like `created`, `tags`, `status`
- **Atomicity**: Keep notes focused on single topics; link related notes with wikilinks
- **Attachments**: Store images and files in a `_attachments/` folder within the vault
