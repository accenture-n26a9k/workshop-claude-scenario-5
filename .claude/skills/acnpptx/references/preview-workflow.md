# Step 0b -- Outline Preview UI Detailed Procedure

> This file contains detailed implementation steps extracted from SKILL.md Step 0b.
> Gate declarations, choices, and rules remain in SKILL.md.

## Launching the UI Preview (when user selects "1. Review in UI")

```bash
VENV="$HOME/.claude/skills/.venv/Scripts/python.exe"
SKILL="$HOME/.claude/skills/acnpptx/scripts"
PORT=3118
# ready_file path matches Python's tempdir (Windows compatible)
READY_FILE=$("$VENV" -c "import tempfile; print(tempfile.gettempdir())")/reviewer_${PORT}.ready
rm -f "$READY_FILE"

# Start server (background)
"$VENV" "$SKILL/reviewer_server.py" --mode preview --port $PORT &

# Wait for ready (max 10 seconds)
for i in $(seq 1 20); do [ -f "$READY_FILE" ] && break; sleep 0.5; done
TOKEN=$("$VENV" -c "import json; print(json.load(open(r'$READY_FILE'))['token'])")
```

## Sending outline.json to the Server

```bash
"$VENV" -c "
import json, urllib.request
outline = json.load(open('outline.json', encoding='utf-8'))
payload = json.dumps({'mode': 'preview', 'outline': outline}).encode()
req = urllib.request.Request('http://127.0.0.1:${PORT}/api/init',
    data=payload,
    headers={'Content-Type': 'application/json'},
    method='POST')
urllib.request.urlopen(req)
print('Sent to reviewer')
"
```

## Polling for User Confirmation

The user reviews, modifies, and reorders patterns in the browser, then presses "Confirm":

```bash
# Lightweight polling (/api/status returns only the confirmed flag)
while true; do
  STATUS=$(curl -s http://127.0.0.1:$PORT/api/status)
  CONFIRMED=$(echo "$STATUS" | "$VENV" -c "import sys,json; print(json.load(sys.stdin).get('confirmed',False))")
  [ "$CONFIRMED" = "True" ] && break
  sleep 2
done
# Fetch full data after confirmation
curl -s http://127.0.0.1:$PORT/api/state > confirmed_state.json

# Shutdown
curl -s -X POST http://127.0.0.1:$PORT/api/shutdown
```

## Post-Confirmation Processing

Reflect pattern changes from confirmed_state.json to update outline.json, then proceed.

**If the user selects "Review as text":** Display `format_outline_md(outline)` as before and wait for user approval.

See [outline-schema.md](outline-schema.md) for schema details.
