---
name: hermes-skill-sync-mechanism
description: "Use when setting up or maintaining the real-time synchronization of local Hermes skills to the `how-to-agent` GitHub repository. Trigger: skill sync setup, inotify watcher configuration, how-to-agent integration. Do NOT trigger for general git operations or manual skill editing."
version: 1.0.0
---

# Hermes Skill Sync Mechanism (inotify-based)

## One-paragraph version

Real-time synchronization of `~/.hermes/skills/` changes to the `huangrichao2020/how-to-agent` GitHub repo using `inotifywait` and a systemd service. Replaces coarse cron polling with instant detection, debouncing, and MD5-diffed commits.

## How to use this skill

1. **Verify prerequisites**: `inotify-tools` installed, `how-to-agent` repo cloned at `~/how-to-agent`.
2. **Check service status**: `systemctl status hermes-skill-sync`.
3. **Manual sync**: Run `/root/hermes-agent/scripts/sync_skills_to_how_to_agent.py --push`.
4. **Debugging**: Check logs at `~/.hermes/logs/skill-sync-watcher.log`.

## Core anti-patterns (stop immediately if you see these)

- **"Using cron for skill sync"** → Too coarse (6h interval). Use the inotify watcher for near-real-time updates.
- **"Manually copying files to how-to-agent"** → Bypasses MD5 diffing and commit history. Always use the sync script.
- **"Ignoring the 2s debounce"** → Rapid file saves (e.g., editor autosave) trigger multiple events. The watcher handles this; don't disable it.
- **"Running the watcher as root without systemd"** → Leads to orphaned processes. Use the `hermes-skill-sync.service` for lifecycle management.
- **"Syncing non-skill files"** → The watcher filters for `SKILL.md`, `references/`, and `checklists/`. Don't add unrelated paths.

## Implementation details

### 1. The Watcher Script (`skill-sync-watcher.sh`)
- Uses `inotifywait -m -r` to monitor `~/.hermes/skills/`.
- Filters events: `create`, `modify`, `move`, `delete`.
- Debounce: `sleep 2` after detection to batch rapid writes.
- Triggers: `python3 sync_skills_to_how_to_agent.py --push`.

### 2. The Sync Script (`sync_skills_to_how_to_agent.py`)
- Scans source skills and compares MD5 hashes with destination.
- Copies only changed/new files (including nested `references/` and `checklists/`).
- Auto-commits and pushes to `how-to-agent` main branch.
- Handles subdirectory structures (e.g., `category/skill-name/`).

### 3. Systemd Service (`hermes-skill-sync.service`)
- Ensures the watcher restarts on failure (`Restart=always`).
- Runs as root to access all skill directories.
- Logs to journal and `~/.hermes/logs/skill-sync-watcher.log`.

## Troubleshooting

- **Service failed (203/EXEC)**: Check script permissions (`chmod +x`) and shebang (`#!/bin/bash`).
- **Sync not triggering**: Verify `inotifywait` is running (`ps aux | grep inotify`). Check logs for permission errors.
- **Git push failed**: Ensure SSH keys are configured for `git@github.com:huangrichao2020/how-to-agent.git`.

## Files involved

- `/root/hermes-agent/scripts/skill-sync-watcher.sh`
- `/root/hermes-agent/scripts/sync_skills_to_how_to_agent.py`
- `/etc/systemd/system/hermes-skill-sync.service`
- `~/.hermes/logs/skill-sync-watcher.log`