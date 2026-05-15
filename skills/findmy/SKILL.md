---
name: findmy
description: Track Apple devices and AirTags via FindMy.app on macOS using AppleScript and screen capture.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [FindMy, AirTag, location, tracking, macOS, Apple]
---

# Find My (Apple)

Track Apple devices and AirTags via the FindMy.app on macOS. Since Apple doesn't
provide a CLI for FindMy, this skill uses AppleScript to open the app and
screen capture to read device locations.

## Prerequisites

- **macOS** with Find My app and iCloud signed in
- Devices/AirTags already registered in Find My
- Screen Recording permission for terminal (System Settings → Privacy → Screen Recording)
- **Optional but recommended**: Install `peekaboo` for better UI automation:
  `brew install steipete/tap/peekaboo`

## When to Use

- User asks "where is my [device/cat/keys/bag]?"
- Tracking AirTag locations
- Checking device locations (iPhone, iPad, Mac, AirPods)
- Monitoring pet or item movement over time (AirTag patrol routes)

## Method 1: AppleScript + Screenshot (Basic)

### Open FindMy and Navigate

```bash
# Open Find My app
osascript -e 'tell application "FindMy" to activate'

# Wait for it to load
sleep 3

# Take a screenshot of the Find My window
screencapture -w -o /tmp/findmy.png
```

Then use `vision_analyze` to read the screenshot:
```
vision_analyze(image_url="/tmp/findmy.png", question="What devices/items are shown and what are their locations?")
```

### Switch Between Tabs

```bash
# Switch to Devices tab
osascript -e '
tell application "System Events"
    tell process "FindMy"
        click button "Devices" of toolbar 1 of window 1
    end tell
end tell'

# Switch to Items tab (AirTags)
osascript -e '
tell application "System Events"
    tell process "FindMy"
        click button "Items" of toolbar 1 of window 1
    end tell
end tell'
```

## Method 2: Peekaboo UI Automation (Recommended)

If `peekaboo` is installed, use it for more reliable UI interaction:

```bash
# Open Find My
osascript -e 'tell application "FindMy" to activate'
sleep 3

# Capture and annotate the UI
peekaboo see --app "FindMy" --annotate --path /tmp/findmy-ui.png

# Click on a specific device/item by element ID
peekaboo click --on B3 --app "FindMy"

# Capture the detail view
peekaboo image --app "FindMy" --path /tmp/findmy-detail.png
```

Then analyze with vision:
```
vision_analyze(image_url="/tmp/findmy-detail.png", question="What is the location shown for this device/item? Include address and coordinates if visible.")
```

## Workflow: Track AirTag Location Over Time

For monitoring an AirTag (e.g., tracking a cat's patrol route):

```bash
# 1. Open FindMy to Items tab
osascript -e 'tell application "FindMy" to activate'
sleep 3

# 2. Click on the AirTag item (stay on page — AirTag only updates when page is open)

# 3. Periodically capture location
while true; do
    screencapture -w -o /tmp/findmy-$(date +%H%M%S).png
    sleep 300  # Every 5 minutes
done
```

Analyze each screenshot with vision to extract coordinates, then compile a route.

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Application "FindMy" is not running` | FindMy.app not installed (iOS-only device) | Requires macOS with iCloud signed in |
| `System Events got an error: -1719` | UI element not found / macOS version mismatch | Check System Settings → Accessibility; try peekaboo instead |
| `screencapture: cannot write to file` | No Screen Recording permission | System Settings → Privacy → Screen Recording → grant terminal |
| `peekaboo: command not found` | peekaboo not installed | `brew install steipete/tap/peekaboo` |
| `vision_analyze returns empty` | Screenshot blank or FindMy not loaded | Increase sleep delay; verify app is foreground |
| `AirTag location stale/unchanged` | Page not in foreground | Keep FindMy app visible; don't minimize |
| `AppleScript timeout (AppleEvent timed out)` | App unresponsive or dialog blocking | Kill FindMy: `killall FindMy`; retry |

### Robust Tracking Script

```bash
#!/bin/bash
# Safe FindMy location check with error handling

check_findmy() {
    # Verify FindMy is running
    if ! pgrep -x "FindMy" >/dev/null 2>&1; then
        echo "Launching FindMy..."
        osascript -e 'tell application "FindMy" to activate'
        sleep 5
    fi
    
    # Verify Screen Recording permission
    screencapture -x /tmp/test_permission.png 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "ERROR: No Screen Recording permission."
        echo "Fix: System Settings → Privacy → Screen Recording → Terminal"
        return 1
    fi
    rm -f /tmp/test_permission.png
    
    # Capture with retry
    local retries=3
    for i in $(seq 1 $retries); do
        screencapture -w -o /tmp/findmy-check.png 2>/dev/null
        if [ -s /tmp/findmy-check.png ]; then
            echo "✅ Screenshot captured successfully"
            return 0
        fi
        echo "Retry $i/$retries..."
        sleep 2
    done
    
    echo "❌ Failed to capture screenshot after $retries attempts"
    return 1
}

check_findmy
```

## Limitations

- FindMy has **no CLI or API** — must use UI automation
- AirTags only update location while the FindMy page is actively displayed
- Location accuracy depends on nearby Apple devices in the FindMy network
- Screen Recording permission required for screenshots
- AppleScript UI automation may break across macOS versions

## Rules

1. Keep FindMy app in the foreground when tracking AirTags (updates stop when minimized)
2. Use `vision_analyze` to read screenshot content — don't try to parse pixels
3. For ongoing tracking, use a cronjob to periodically capture and log locations
4. Respect privacy — only track devices/items the user owns
