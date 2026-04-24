# verify-guide.md -- Verification and Quality Check Details

## Execution Commands (Step 9)

```bash
VENV="$HOME/.claude/skills/.venv/Scripts/python.exe"
$VENV ~/.claude/skills/acnpptx/scripts/brand_check.py output.pptx
$VENV ~/.claude/skills/acnpptx/scripts/verify_pptx.py output.pptx
$VENV ~/.claude/skills/acnpptx/scripts/thumbnail.py output.pptx slides/

# Final check for remaining placeholder hint text
$VENV -m markitdown output.pptx
# If "Click to add title", "Place subtitle here", etc. appear, fix the script
```

Fix all ERRORs. Review WARNINGs and decide on each case.

---

## brand_check.py -- Check Items

| Check Item | Description |
|------------|-------------|
| Cover logo | Verify it is provided by the master |
| Rounded shapes | Check that no roundRect shapes are used |
| Color palette | Verify only approved colors are used |
| Font size | Check for text smaller than 12pt |
| Overflow | Check for text overflowing its bounding box |
| Headlines | Verify sentence case |
| **Contrast** | WCAG contrast ratio check |

**Contrast check details:**
- Calculates WCAG contrast ratio between all text on all slides and their background color (resolved in order: slide -> layout -> master)
- **ratio < 2.0** -> ERROR (nearly invisible, e.g., white text on white background)
- **ratio < 3.0** -> WARNING (cover/closing slides only; hard to read)
- If background color cannot be resolved, white (#FFFFFF) is assumed

---

## verify_pptx.py -- Check Items

| Check Item | Description |
|------------|-------------|
| Hint text remaining | Regex detection of "Click to add title", "Place subtitle here", etc. -> ERROR |
| Font size | pt size of each text element |
| Overflow | Text overflowing its box |
| Overlap | Shape overlap detection |
| Footer | Check if `set_footer()` was called |
| **Vertical clipping** | Line count estimation with CJK/ASCII mix support. +8% -> WARN, +20% -> FAIL |
| **Horizontal overflow** | Two patterns detected (see below) |
| Layout density | WARNING if table/chart is less than 80% of CW |

**Horizontal overflow (Check 6) details:**
- `word_wrap=False` boxes: FAIL if estimated text width exceeds box width by 10%
- Card boundary overflow: FAIL if a textbox right edge exceeds the surrounding container shape right edge -- catches text bleeding into adjacent cards

---

## Step 10 -- Visual Review Checklist (thumbnail verification)

Read each `slides/slide_NN.png` with the Read tool and verify the following:

- [ ] **Cover: Sufficient contrast between background and text colors** (white bg -> BLACK text, purple bg -> WHITE text)
- [ ] Cover: logo, GT symbol provided by the master
- [ ] Content slides: white bg, BLACK title, small GT bottom-right
- [ ] **No placeholder hint text remaining** ("Click to add title", "Place subtitle here", etc.)
- [ ] **Message line: present on all content slides (except cover/section/agenda)**
- [ ] **Message line: directly below title, DARK_PURPLE color, 18pt, not overlapping content**
- [ ] Purple accent bars visible on panels/cards
- [ ] No rounded rectangles anywhere
- [ ] Text not clipped, generous whitespace
- [ ] Sentence case headlines
- [ ] Body text >= 14pt, captions >= 12pt
- [ ] Charts: theme palette applied, axis labels readable
- [ ] Icons: visible and properly labeled

Fix any issues found and re-run verify.