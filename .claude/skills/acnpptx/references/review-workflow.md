# Step 10 -- Visual Review UI Detailed Procedure

> This file contains detailed implementation steps extracted from SKILL.md Step 10.
> Gate declarations, loop controls, and sub-agent references remain in SKILL.md.

## Launching the UI Review (when user selects "1. Review in UI")

```bash
VENV="$HOME/.claude/skills/.venv/Scripts/python.exe"
SKILL="$HOME/.claude/skills/acnpptx/scripts"
PORT=3118
READY_FILE=$("$VENV" -c "import tempfile; print(tempfile.gettempdir())")/reviewer_${PORT}.ready
rm -f "$READY_FILE"

# Start server (review mode)
"$VENV" "$SKILL/reviewer_server.py" --mode review --port $PORT &
for i in $(seq 1 20); do [ -f "$READY_FILE" ] && break; sleep 0.5; done
TOKEN=$("$VENV" -c "import json; print(json.load(open(r'$READY_FILE'))['token'])")
```

## Sending Slide Images to the Server

```python
# Base64-encode slide images and send to server (run via python -c from bash)
import json, base64, urllib.request, glob, os

slides_data = []
for png in sorted(glob.glob("slides/slide_*.png")):
    idx = int(os.path.basename(png).replace("slide_","").replace(".png","")) - 1
    with open(png, "rb") as f:
        b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode()
    slides_data.append({"index": idx, "title": f"Slide {idx+1}", "image_b64": b64, "pattern": ""})

# PORT and TOKEN are injected via bash variable expansion
payload = json.dumps({"mode": "review", "slides": slides_data}).encode()
req = urllib.request.Request(f"http://127.0.0.1:{PORT}/api/init",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST")
urllib.request.urlopen(req)
```

## Polling for Feedback

The user draws markup (rectangles, arrows, circles, text) in the browser and enters text feedback, then presses "Submit Feedback":

```bash
# Lightweight polling (uses /api/status which excludes image data)
while true; do
  STATUS=$(curl -s http://127.0.0.1:$PORT/api/status)
  CONFIRMED=$(echo "$STATUS" | "$VENV" -c "import sys,json; print(json.load(sys.stdin).get('confirmed',False))")
  [ "$CONFIRMED" = "True" ] && break
  sleep 2
done
# Fetch full data after confirmation
curl -s http://127.0.0.1:$PORT/api/state > review_feedback.json
curl -s -X POST http://127.0.0.1:$PORT/api/shutdown
```

review_feedback.json contains per-slide text_feedback (text correction instructions) and annotated_image_b64 (marked-up images).

## Post-Feedback Processing Steps

```python
# Extract annotated images from review_feedback.json and save as PNG files
import json, base64, os

with open("review_feedback.json", encoding="utf-8") as f:
    data = json.load(f)

os.makedirs("review_annotations", exist_ok=True)
for item in data.get("feedback", []):
    idx = item["slide_index"]
    # Display text feedback
    if item.get("text_feedback"):
        print(f"Slide {idx+1}: {item['text_feedback']}")
    # Save annotated image as PNG file
    if item.get("annotated_image_b64"):
        b64 = item["annotated_image_b64"].replace("data:image/png;base64,", "")
        png_path = f"review_annotations/slide_{idx+1:02d}_annotated.png"
        with open(png_path, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"  -> Annotated image: {png_path}")
```

## Applying Feedback

1. Save annotated images to `review_annotations/` using the script above
2. **Read each `slide_XX_annotated.png` with the Read tool** -- Claude visually interprets the image, understanding user intent from red rectangles, arrows, and text annotations
3. Cross-reference both text_feedback and annotated images, then execute corrections
4. After corrections, regenerate thumbnails with thumbnail.py and run the visual review checklist
5. Use **AskUserQuestion** again for final user confirmation. Repeat this loop until the user approves