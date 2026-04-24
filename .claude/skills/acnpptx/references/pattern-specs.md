# Pattern Specifications — Accenture Brand Patterns

39 patterns (A–AN) + cover/section. Choose the best fit for your content.
All patterns use native shapes only (SVG is not used).

## Layout Constants (inches)
```
ML=0.42  MR=0.42  CW=12.50  CY=1.50  BY=6.85  AH=5.35
Slide: 13.333" × 7.500"
Breadcrumb: idx=11, y=0.08, h=0.27
Title:       idx=0,  y=0.42, h=0.48  (bottom=0.90)
Message line:        y=0.95, h=0.45  (bottom=1.40)
Content area:        y=1.50 → BY=6.85
```

**Typography rules (apply to ALL patterns):**
- Titles: 28pt bold, BLACK (#000000), sentence case
- Message line: **18pt** bold, DARK_PURPLE (#7500C0) — mandatory on all content slides except cover/section/agenda
- Lead/intro: 18pt regular, TEXT_BODY (#333333)
- Body/bullets: 14pt regular, TEXT_BODY (#333333)
- Label on colored bg: 14pt regular/bold, WHITE (#FFFFFF)
- Box sub-info: 14pt regular, TEXT_BODY (#333333)
- Caption/note: **12pt** regular, MID_GRAY (#818180)  ← 13pt is FORBIDDEN
- Breadcrumb: **12pt** MID_GRAY
- Footer: 8pt TEXT_SUB (#666666)

**Font size rule: only 8 / 12 / 14 / 18 / 28 / 36–44pt allowed. 11pt and 13pt are forbidden.**

**Container minimum rule: text inside any box, card, panel, or table cell must be ≥14pt. 12pt is reserved for captions/notes *outside* containers only.**

**Message line placement (all patterns):**
```
Breadcrumb  (y=0.08, idx=11, 12pt MID_GRAY)
Title       (y=0.42, idx=0,  28pt bold BLACK)
────────────────────────────────── ← add_message_line() at y=MSG_Y=0.95
Message line (y=0.95, 18pt bold DARK_PURPLE)
──────────────────────────────────
Content area starts at CY=1.50
```


---

## Cover slide template

**Required**: Use `add_cover_slide()`. `add_slide()` is forbidden. Do not add background rectangles (the master auto-provides background, logo, and GT).

**Background and text color rules:**
- `cover_text_color: "BLACK"` -> all placeholders BLACK / MID_GRAY
- Purple background -> WHITE text, white background -> BLACK / TEXT_BODY text (WHITE becomes invisible)

```python
# ── Pattern 1: theme with idx=0/1 (purple background default) ──────────────────────
slide = add_cover_slide()
for ph in slide.placeholders:
    idx = ph.placeholder_format.idx
    ph.text_frame.clear()
    p = ph.text_frame.paragraphs[0]
    if idx == 0:        # Main title
        p.text = "Presentation Title"
        p.font.size = Pt(40); p.font.bold = True
        p.font.color.rgb = WHITE; p.font.name = FONT   # Change to BLACK for white background
    elif idx == 1:      # Subtitle
        p.text = "FY2025 Trends / Growth Strategy in the AI Era"
        p.font.size = Pt(22)
        p.font.color.rgb = WHITE; p.font.name = FONT   # Change to TEXT_BODY for white background
    else:               # Date / author
        p.text = "March 2026"
        p.font.size = Pt(16)
        p.font.color.rgb = LIGHT_PURPLE; p.font.name = FONT  # Change to MID_GRAY for white background

# ── Pattern 2: theme with different idx (refer to theme JSON layout_notes.cover.placeholders) ──
# Example: sample_sha -> idx=10 (organization), idx=11 (title), idx=12 (date)
slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_COVER])
ph_map = {
    10: ("Organization / Department",    18, False, BLACK),
    11: ("Presentation Title",           36, True,  BLACK),
    12: ("March 2026",                   14, False, MID_GRAY),
}
for ph in slide.placeholders:
    idx = ph.placeholder_format.idx
    if idx in ph_map:
        text, size, bold, color = ph_map[idx]
        ph.text_frame.clear()
        p = ph.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = text
        run.font.size = Pt(size); run.font.bold = bold
        run.font.color.rgb = color; run.font.name = FONT
```
---

## Pattern A — Title + Body (Standard)
**Use**: Text-heavy explanations, reports, meeting content

```
Title (28pt bold, BLACK)
─────────────────────────
Lead sentence (18pt)

• Bullet 1 (14pt)
• Bullet 2
• Bullet 3
```

| Shape | x | y | w | h | Fill | Font |
|-------|---|---|---|---|------|------|
| Title | ML | CY | CW | 0.60 | NONE | 28pt bold BLACK |
| Lead | ML | 2.40 | CW | 0.55 | NONE | 18pt TEXT_BODY |
| Body | ML | 3.10 | CW | 3.20 | NONE | 14pt TEXT_BODY |

GT symbol and logo are provided by the slide master — do NOT add them manually.

```python
slide = add_slide()
add_breadcrumb(slide, "Section > Topic")
add_title(slide, "Slide Title")
add_message_line(slide, "Key assertion in declarative form. Under 60 characters.")

body = slide.shapes.add_textbox(Inches(ML), Inches(CY), Inches(CW), Inches(AH))
tf = body.text_frame; tf.word_wrap = True
for i, line in enumerate(["Point 1", "Point 2", "Point 3"]):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.text = f"• {line}"; p.font.size = Pt(14)
    p.font.color.rgb = TEXT_BODY; p.font.name = FONT

set_footer(slide)
```

---

## Pattern B — Two Column
**Use**: Comparisons, before/after, two parallel concepts

Each panel has a 0.08" CORE_PURPLE accent bar at top.

| Shape | x | y | w | h | Fill |
|-------|---|---|---|---|------|
| Title | ML | CY | CW | 0.55 | NONE |
| Left panel | ML | 2.35 | 6.00 | 4.00 | OFF_WHITE |
| Left accent bar | ML | 2.35 | 6.00 | 0.08 | CORE_PURPLE |
| Left header | ML+0.15 | 2.50 | 5.70 | 0.35 | NONE, 16pt bold |
| Left body | ML+0.15 | 2.95 | 5.70 | 3.20 | NONE, 14pt |
| Right panel | 6.92 | 2.35 | 6.00 | 4.00 | OFF_WHITE |
| Right accent bar | 6.92 | 2.35 | 6.00 | 0.08 | CORE_PURPLE |
| Right header | 7.07 | 2.50 | 5.70 | 0.35 | NONE, 16pt bold |
| Right body | 7.07 | 2.95 | 5.70 | 3.20 | NONE, 14pt |

---

## Pattern C — Section Divider (Dark)
**Use**: Chapter breaks, agenda transitions

Full-slide DARKEST_PURPLE (#460073) background.
Title: 36pt bold WHITE, placed via `add_title(slide, "...", size_pt=36)`.
Subtitle: **28pt** LIGHT_PURPLE (#C2A3FF), added as textbox below title.

Logo and GT symbol are embedded in the slide master layout — do NOT add them manually.

**Breadcrumb must not be empty.** Passing `""` renders as "Enter text" placeholder in thumbnails. Always pass the section name/number.

```python
slide = add_slide()

# Full-slide dark background
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE as MSO
bg = slide.shapes.add_shape(MSO.RECTANGLE,
    Inches(0), Inches(0), prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = DARKEST_PURPLE
bg.line.fill.background()

# Breadcrumb — always provide section name (never empty string)
add_breadcrumb(slide, "Section 02")   # ← use actual section number/name

# Title
add_title(slide, "Section Title", size_pt=36)

# Optional subtitle textbox
tb = slide.shapes.add_textbox(Inches(ML), Inches(3.90), Inches(CW), Inches(0.60))
p = tb.text_frame.paragraphs[0]
p.text = "Section subtitle or overview description"
p.font.size = Pt(28); p.font.color.rgb = LIGHT_PURPLE; p.font.name = FONT

set_footer(slide)
```

---

## Pattern D — Key Message (Impact)
**Use**: Single bold statement, key insight, executive summary opener

| Shape | x | y | w | h | Fill | Font |
|-------|---|---|---|---|------|------|
| Title (small) | ML | CY | CW | 0.50 | NONE | 20pt bold BLACK |
| Accent bar | ML | 2.40 | 1.20 | 0.06 | CORE_PURPLE | — |
| Key message | ML | 2.55 | CW | 1.80 | NONE | 32pt bold BLACK |
| Supporting | ML | 5.20 | CW | 1.30 | NONE | 14pt TEXT_BODY |

---

## Pattern E — Bullet with Accent Mark
**Use**: Key findings, recommendations, executive readout

3–4 items max. Each row: small CORE_PURPLE accent rectangle (0.06"×0.28") + headline (18pt bold) + detail (14pt).

```python
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE as MSO

row_h = 1.35  # per item
for i, (headline, detail) in enumerate(items):
    row_y = CY + 0.60 + i * row_h
    # Accent mark (thin vertical rectangle instead of GT image)
    acc = slide.shapes.add_shape(MSO.RECTANGLE,
        Inches(ML), Inches(row_y + 0.05), Inches(0.06), Inches(0.28))
    acc.fill.solid(); acc.fill.fore_color.rgb = CORE_PURPLE
    acc.line.fill.background()
    # Headline text at x=ML+0.18, font 18pt bold
    tb_h = slide.shapes.add_textbox(Inches(ML + 0.18), Inches(row_y),
        Inches(CW - 0.18), Inches(0.42))
    p_h = tb_h.text_frame.paragraphs[0]
    p_h.text = headline; p_h.font.size = Pt(18)
    p_h.font.bold = True; p_h.font.color.rgb = TEXT_BODY; p_h.font.name = FONT
    # Detail text
    tb_d = slide.shapes.add_textbox(Inches(ML + 0.18), Inches(row_y + 0.45),
        Inches(CW - 0.18), Inches(0.85))
    p_d = tb_d.text_frame.paragraphs[0]
    p_d.text = detail; p_d.font.size = Pt(14)
    p_d.font.color.rgb = TEXT_BODY; p_d.font.name = FONT
```

---

## Pattern F — Card Grid (2×2)
**Use**: 4-item comparison, quadrant frameworks

Card: w=5.90", h=2.30", gap=0.35". Top accent bar: CORE_PURPLE, 0.06" tall.

| Shape | x | y | w | h | Fill |
|-------|---|---|---|---|------|
| Card TL | ML | 2.35 | 5.90 | 2.30 | OFF_WHITE |
| Card TL bar | ML | 2.35 | 5.90 | 0.06 | CORE_PURPLE |
| Card TR | 6.92 | 2.35 | 5.90 | 2.30 | OFF_WHITE |
| Card TR bar | 6.92 | 2.35 | 5.90 | 0.06 | CORE_PURPLE |
| Card BL | ML | 4.80 | 5.90 | 2.30 | OFF_WHITE |
| Card BL bar | ML | 4.80 | 5.90 | 0.06 | CORE_PURPLE |
| Card BR | 6.92 | 4.80 | 5.90 | 2.30 | OFF_WHITE |
| Card BR bar | 6.92 | 4.80 | 5.90 | 0.06 | CORE_PURPLE |

Card title: 14pt bold BLACK inside card (y offset +0.20 from bar)
Card body: 14pt TEXT_BODY (y offset +0.55 from bar)

---

## Pattern G — Table
**Use**: Data tables, structured information

Header row: DARKEST_PURPLE fill + WHITE 14pt bold text
Data rows: WHITE (solid color), 14pt TEXT_BODY — **alternating colors forbidden**

```python
table = slide.shapes.add_table(
    rows, cols, Inches(ML), Inches(2.30), Inches(CW), Inches(4.00)
).table

# Header
for c, h in enumerate(headers):
    cell = table.cell(0, c)
    cell.text = h
    cell.fill.solid(); cell.fill.fore_color.rgb = DARKEST_PURPLE
    for para in cell.text_frame.paragraphs:
        para.font.bold = True; para.font.size = Pt(14)
        para.font.color.rgb = WHITE; para.font.name = FONT

# Data rows (all rows WHITE — alternating colors forbidden)
for r, row in enumerate(data, 1):
    for c, val in enumerate(row):
        cell = table.cell(r, c); cell.text = str(val)
        cell.fill.solid(); cell.fill.fore_color.rgb = WHITE
        for para in cell.text_frame.paragraphs:
            para.font.size = Pt(14)
            para.font.color.rgb = TEXT_BODY; para.font.name = FONT
```

---

## Pattern I -- Agenda
**Use**: Table of contents, section overview (typically 4-7 items)

Numbered boxes on left + section text on right. Active section highlighted.

```
[01]  Background / Issues
[02]  Solution Overview
[03]  Results and Outcomes
[04]  Summary / Q&A
```

Agenda does not need a message line. Start items from CY and dynamically calculate spacing based on item count.

**WARNING: Badge color is solid DARKEST_PURPLE. Varying colors by index parity or sequence is strictly forbidden.**
Only the active item changes to CORE_PURPLE (if active_idx=None, all are DARKEST_PURPLE).

| Shape | x | y | w | h | Fill | Font |
|-------|---|---|---|---|------|------|
| Title | ML | CY | CW | 0.55 | NONE | 28pt bold BLACK |
| Number box [n] | ML | ITEM_Y + n*gap | 0.55 | 0.65 | DARKEST_PURPLE (all badges uniform) | 20pt bold WHITE |
| Item text | ML+0.70 | ITEM_Y + n*gap + 0.08 | 11.30 | 0.50 | NONE | 18pt TEXT_BODY |
| Active bar | ML | ITEM_Y + active*gap | 0.06 | 0.65 | CORE_PURPLE (active only) | — |

`ITEM_Y = CY + 0.10` (starts directly below title)
`gap = min(0.90, (BY - ITEM_Y - 0.65) / max(len(items) - 1, 1))` (supports 4-7 items)

```python
items = ["Background & Issues", "Solution", "Results & Outcomes", "Summary"]
active_idx = None  # or 0,1,2... to highlight current section

ITEM_Y = CY + 0.10   # Start directly below title (2.35" is too far down)
gap = min(0.90, (BY - ITEM_Y - 0.65) / max(len(items) - 1, 1))

for i, item in enumerate(items):
    iy = ITEM_Y + i * gap
    # Number badge
    num_box = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(ML), Inches(iy), Inches(0.55), Inches(0.65))
    num_box.fill.solid()
    num_box.fill.fore_color.rgb = (CORE_PURPLE if i == active_idx
                                   else DARKEST_PURPLE)
    num_box.line.fill.background()
    tf = num_box.text_frame
    tf.word_wrap = False   # <- Required: prevents "01" from splitting into "0\n1"
    from pptx.oxml.ns import qn as _qn
    _bp = tf._txBody.find(_qn('a:bodyPr'))
    for _attr in ('lIns', 'rIns', 'tIns', 'bIns'):
        _bp.set(_attr, '0')   # Zero internal margins to fully prevent wrapping
    _bp.set('anchor', 'ctr')  # Vertical center
    tf.paragraphs[0].text = f"{i+1:02d}"
    tf.paragraphs[0].font.size = Pt(18)   # 20->18pt: safe size that fits within 0.55" width
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = WHITE
    tf.paragraphs[0].font.name = FONT
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Item text
    tb = slide.shapes.add_textbox(
        Inches(ML + 0.70), Inches(iy + 0.08),
        Inches(11.30), Inches(0.50))
    p = tb.text_frame.paragraphs[0]
    p.text = item
    p.font.size = Pt(18)
    p.font.color.rgb = (BLACK if i == active_idx else TEXT_BODY)
    p.font.bold = (i == active_idx)
    p.font.name = FONT
```

---

## Pattern J — KPI / Metrics
**Use**: Key numbers, performance results (2–4 KPIs side by side)

Large value (48–60pt) + label (14pt) + detail (12pt), evenly spaced.

```
┌────────┐  ┌────────┐  ┌────────┐
│  82%   │  │  1.8x  │  │ 60 days │
│KPI Rate │  │Productiv│  │Reduction│
│YoY +12% │  │Post-AI  │  │Lead Time│
└────────┘  └────────┘  └────────┘
```

| Shape | x | y | w | h | Fill | Font |
|-------|---|---|---|---|------|------|
| Title | ML | CY | CW | 0.55 | NONE | 28pt bold BLACK |
| Accent bar (full) | ML | 2.35 | CW | 0.06 | CORE_PURPLE | — |
| KPI card [n] | ML + n*(CW/N) | 2.60 | CW/N - 0.20 | 3.50 | OFF_WHITE | — |
| KPI card bar | same x | 2.60 | same w | 0.06 | DARKEST_PURPLE | — |
| Value text | inside card | +0.50 | — | 0.80 | NONE | 52pt bold DARKEST_PURPLE |
| Label text | inside card | +1.50 | — | 0.40 | NONE | 14pt bold BLACK |
| Detail text | inside card | +2.00 | — | 0.35 | NONE | 12pt MID_GRAY |

```python
kpis = [
    {"value": "82%", "label": "KPI Achievement", "detail": "YoY +12%"},
    {"value": "1.8x", "label": "Productivity Gain", "detail": "Post-AI adoption"},
    {"value": "60 days", "label": "Lead Reduction", "detail": "Shortened timeline"},
]
n = len(kpis)
card_w = (CW - 0.20 * (n - 1)) / n

for i, kpi in enumerate(kpis):
    cx = ML + i * (card_w + 0.20)
    cy = 2.60
    # Card background
    card = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(cx), Inches(cy), Inches(card_w), Inches(3.50))
    card.fill.solid(); card.fill.fore_color.rgb = OFF_WHITE
    card.line.fill.background()
    # Top accent bar
    bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(cx), Inches(cy), Inches(card_w), Inches(0.06))
    bar.fill.solid(); bar.fill.fore_color.rgb = DARKEST_PURPLE
    bar.line.fill.background()
    # Value
    def _add_tb(text, x, y, w, h, size, bold, color):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        p = tb.text_frame.paragraphs[0]
        p.text = text; p.font.size = Pt(size); p.font.bold = bold
        p.font.color.rgb = color; p.font.name = FONT
        p.alignment = PP_ALIGN.CENTER
        return tb
    _add_tb(kpi["value"], cx, cy + 0.40, card_w, 0.80, 52, True, DARKEST_PURPLE)
    _add_tb(kpi["label"], cx, cy + 1.40, card_w, 0.40, 14, True, BLACK)
    _add_tb(kpi.get("detail", ""), cx, cy + 1.90, card_w, 0.35, 12, False, MID_GRAY)
```

**Variant: Hero Stat + Supporting Stats (1 hero + 3 supporting)**

Layout with one primary metric displayed large, and the rest arranged below (Slide 52 type).

```python
# Hero stat (full-width card, prominent)
hero = {"value": "94%", "label": "Customer Satisfaction", "detail": "Record-high level achieved"}
hero_h = 2.60
hero_card = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
    Inches(ML), Inches(CY), Inches(CW), Inches(hero_h))
hero_card.fill.solid(); hero_card.fill.fore_color.rgb = OFF_WHITE
hero_card.line.fill.background()
bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
    Inches(ML), Inches(CY), Inches(CW), Inches(0.06))
bar.fill.solid(); bar.fill.fore_color.rgb = DARKEST_PURPLE; bar.line.fill.background()
_add_tb(hero["value"],  ML, CY + 0.30, CW, 1.00, 64, True,  DARKEST_PURPLE)
_add_tb(hero["label"],  ML, CY + 1.40, CW, 0.40, 18, True,  BLACK)
_add_tb(hero["detail"], ML, CY + 1.90, CW, 0.40, 14, False, MID_GRAY)

# Supporting stats (3 equal cards below hero)
sub_kpis = [
    {"value": "1.8x", "label": "Productivity Gain",  "detail": "Post-AI adoption"},
    {"value": "60 days", "label": "Lead Reduction",  "detail": "Shortened timeline"},
    {"value": "¥2.4B","label": "Cost Savings","detail": "Cumulative"},
]
sub_y   = CY + hero_h + 0.20
sub_h   = BY - sub_y - 0.10
sub_n   = len(sub_kpis)
sub_w   = (CW - 0.20 * (sub_n - 1)) / sub_n
for i, kpi in enumerate(sub_kpis):
    cx = ML + i * (sub_w + 0.20)
    sc = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(cx), Inches(sub_y), Inches(sub_w), Inches(sub_h))
    sc.fill.solid(); sc.fill.fore_color.rgb = OFF_WHITE; sc.line.fill.background()
    sb = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(cx), Inches(sub_y), Inches(sub_w), Inches(0.06))
    sb.fill.solid(); sb.fill.fore_color.rgb = CORE_PURPLE; sb.line.fill.background()
    _add_tb(kpi["value"],  cx, sub_y + 0.25, sub_w, 0.65, 36, True,  DARKEST_PURPLE)
    _add_tb(kpi["label"],  cx, sub_y + 0.95, sub_w, 0.35, 14, True,  BLACK)
    _add_tb(kpi["detail"], cx, sub_y + 1.35, sub_w, 0.30, 12, False, MID_GRAY)
```

---

## Pattern K — Three Column
**Use**: Three pillars, three principles, three workstreams

Same structure as B but with 3 equal panels (w≈3.90").

**WARNING: All panel background colors must be uniform OFF_WHITE. Alternating or mixing purple variants (CORE_PURPLE / DARKEST_PURPLE etc.) is strictly forbidden. Only the top accent bar uses CORE_PURPLE.**

| Shape | x | y | w | h | Fill |
|-------|---|---|---|---|------|
| Title | ML | CY | CW | 0.55 | NONE |
| Panel 1 | ML | 2.35 | 3.90 | 4.00 | OFF_WHITE (all panels uniform) |
| Panel 1 bar | ML | 2.35 | 3.90 | 0.08 | CORE_PURPLE |
| Panel 2 | 4.62 | 2.35 | 3.90 | 4.00 | OFF_WHITE (all panels uniform) |
| Panel 2 bar | 4.62 | 2.35 | 3.90 | 0.08 | CORE_PURPLE |
| Panel 3 | 8.82 | 2.35 | 3.90 | 4.00 | OFF_WHITE (all panels uniform) |
| Panel 3 bar | 8.82 | 2.35 | 3.90 | 0.08 | CORE_PURPLE |

Panel header: 14pt bold BLACK, y offset +0.20 from bar
Panel body: 14pt TEXT_BODY, y offset +0.65 from bar
Gap between panels: 0.30"

**Variant: Numbered Badge Header (3-4 columns, Slide 50-51 type)**

Layout with number badges (DARKEST_PURPLE circle + white numbers) at the top of each panel.
Change `N_COLS = 3` or `4` to support either 3-column or 4-column layouts.

```python
N_COLS   = 3           # 3 or 4
PANEL_W  = (CW - 0.20 * (N_COLS - 1)) / N_COLS
PANEL_H  = BY - CY - 0.30
BADGE_D  = 0.48        # badge circle diameter

panels = [
    {"num": 1, "title": "Pillar 1",  "body": "- Initiative A\n- Initiative B\n- Initiative C"},
    {"num": 2, "title": "Pillar 2",  "body": "- Initiative D\n- Initiative E\n- Initiative F"},
    {"num": 3, "title": "Pillar 3",  "body": "- Initiative G\n- Initiative H\n- Initiative I"},
]

for i, panel in enumerate(panels):
    px = ML + i * (PANEL_W + 0.20)
    py = CY + 0.55   # leave room for badge above panel

    # Panel background
    bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(px), Inches(py), Inches(PANEL_W), Inches(PANEL_H))
    bg.fill.solid(); bg.fill.fore_color.rgb = OFF_WHITE; bg.line.fill.background()

    # Top accent bar
    bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(px), Inches(py), Inches(PANEL_W), Inches(0.06))
    bar.fill.solid(); bar.fill.fore_color.rgb = CORE_PURPLE; bar.line.fill.background()

    # Number badge (circle, overlapping top of panel)
    bx = px + (PANEL_W - BADGE_D) / 2
    badge = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL,
        Inches(bx), Inches(py - BADGE_D / 2), Inches(BADGE_D), Inches(BADGE_D))
    badge.fill.solid(); badge.fill.fore_color.rgb = DARKEST_PURPLE; badge.line.fill.background()
    tf = badge.text_frame
    p = tf.paragraphs[0]; p.text = str(panel["num"])
    p.font.size = Pt(18); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT; p.alignment = PP_ALIGN.CENTER
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

    # Panel title
    tb_t = slide.shapes.add_textbox(Inches(px + 0.15), Inches(py + 0.20),
        Inches(PANEL_W - 0.30), Inches(0.50))
    p = tb_t.text_frame.paragraphs[0]; p.text = panel["title"]
    p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = BLACK; p.font.name = FONT; p.alignment = PP_ALIGN.CENTER

    # Panel body
    tb_b = slide.shapes.add_textbox(Inches(px + 0.15), Inches(py + 0.80),
        Inches(PANEL_W - 0.30), Inches(PANEL_H - 1.00))
    tf = tb_b.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = panel["body"]
    p.font.size = Pt(14); p.font.color.rgb = TEXT_BODY; p.font.name = FONT
```

---

## Pattern L — Do / Don't
**Use**: Best practices, recommendations vs. anti-patterns

Left panel = Do (green check indicator), Right = Don't (red X indicator).
Indicator: small colored accent bar at top (CORE_PURPLE for Do, DARK_PURPLE for Don't).

| Shape | x | y | w | h | Fill |
|-------|---|---|---|---|------|
| Title | ML | CY | CW | 0.55 | NONE |
| Do panel | ML | 2.35 | 6.00 | 4.20 | OFF_WHITE |
| Do bar | ML | 2.35 | 6.00 | 0.08 | CORE_PURPLE |
| Do label | ML+0.15 | 2.50 | 2.50 | 0.35 | NONE | 16pt bold CORE_PURPLE |
| Do body | ML+0.15 | 2.95 | 5.70 | 3.40 | NONE | 14pt TEXT_BODY |
| Don't panel | 6.92 | 2.35 | 6.00 | 4.20 | OFF_WHITE |
| Don't bar | 6.92 | 2.35 | 6.00 | 0.08 | DARK_PURPLE |
| Don't label | 7.07 | 2.50 | 2.50 | 0.35 | NONE | 16pt bold DARK_PURPLE |
| Don't body | 7.07 | 2.95 | 5.70 | 3.40 | NONE | 14pt TEXT_BODY |

"✓ Do" label uses CORE_PURPLE; "✗ Don't" label uses DARK_PURPLE.

> WARNING: **Always set `tf.word_wrap = False` on label textboxes.** Default is True, so without it labels like "Do (Recommended)" will wrap. Use label width of 2.50" (1.50" causes wrapping with mixed text).
>
> ```python
> tb = slide.shapes.add_textbox(Inches(ML+0.15), Inches(2.50), Inches(2.50), Inches(0.35))
> tf = tb.text_frame
> tf.word_wrap = False   # <- Required
> p = tf.paragraphs[0]
> p.text = "✓ Do (Recommended)"
> p.font.size = Pt(16); p.font.bold = True
> p.font.color.rgb = CORE_PURPLE; p.font.name = FONT
> ```

---

## Pattern M — Chart
**Use**: Data visualization (bar, column, line, pie charts)

Use `scripts/charts.py` helpers. Chart occupies CX=9" H=4.20" area.
Optional description text on left (w=3.50") or below the chart.

```python
from charts import add_column_chart, add_bar_chart, add_line_chart, add_pie_chart

# Full-width chart (title + chart + footer)
chart = add_column_chart(
    slide,
    title="Chart Title",   # displayed inside chart area
    categories=["Q1", "Q2", "Q3", "Q4"],
    series_data=[
        {"name": "2025", "values": [100, 120, 130, 150]},
        {"name": "2026", "values": [110, 135, 145, 170]},
    ],
    x=ML, y=2.30, w=CW, h=4.20,
    font_name=FONT,
)

# Left description + right chart layout
# Description: x=ML, y=2.30, w=3.50, h=4.00
# Chart:       x=4.20, y=2.30, w=8.60, h=4.00
```

**Chart type selection guide:**
- Column (vertical bars): comparisons across categories, time series
- Bar (horizontal): rankings, comparisons with long labels
- Line: trends over time, continuous data
- Pie: composition/breakdown (max 5–6 slices)
- Stacked column: part-to-whole across categories

---

## Pattern N — Team Introduction
**Use**: Team member showcase (2–6 people)

Photo placeholder + name + title + optional description.

```
[Photo]    [Photo]    [Photo]
 Name       Name       Name
 Title      Title      Title
 Detail     Detail     Detail
```

| Shape | x (for 3-up) | y | w | h | Fill |
|-------|-------------|---|---|---|------|
| Photo box [n] | ML + n*4.25 | 2.35 | 3.50 | 2.50 | OFF_WHITE |
| Photo bar [n] | same x | 2.35 | 3.50 | 0.06 | CORE_PURPLE |
| Name [n] | same x | 4.95 | 3.50 | 0.35 | NONE | 14pt bold BLACK |
| Title [n] | same x | 5.35 | 3.50 | 0.30 | NONE | 12pt MID_GRAY |
| Detail [n] | same x | 5.70 | 3.50 | 0.55 | NONE | 12pt TEXT_BODY |

Photo box shows "[ Photo ]" placeholder text (14pt MID_GRAY, centered).
If an image path is provided, use `add_image_fit()` instead.

---

### Variant: Org Chart
**Use**: Visualizing reporting structures and project organization hierarchies (2-3 layers, expressing inter-departmental relationships with rectangles + connectors). Slides 41-43 type. Unlike "Team Introduction Cards" (Base), shows vertical hierarchy.

```
          ┌──────────────────┐
          │  Project Sponsor │
          └────────┬─────────┘
         ┌─────────┼─────────┐
         ▼         ▼         ▼
   ┌──────────┐ ┌──────────┐ ┌──────────┐
   │  Lead A  │ │  Lead B  │ │  Lead C  │
   └──────────┘ └──────────┘ └──────────┘
```

| Element | Shape | Fill | Text |
|---------|-------|------|------|
| L0 box  | RECTANGLE | DARKEST_PURPLE | WHITE 12pt bold |
| L1 box  | RECTANGLE | DARK_PURPLE    | WHITE 12pt |
| L2+ box | RECTANGLE | OFF_WHITE      | TEXT_BODY 12pt |
| Connector | add_connector_arrow | LIGHT_GRAY 1pt | arrow_end=False |

```python
from native_shapes import add_connector_arrow
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.oxml.ns import qn as _qn

BOX_W = 2.20
BOX_H = 0.65
H_GAP = 0.25   # Horizontal gap between siblings
V_GAP = 0.85   # Vertical gap between levels

# Tree: {"name", "title", "children": [...]}
org = {
    "name": "Taro Yamada", "title": "Project Sponsor",
    "children": [
        {"name": "Hanako Sato", "title": "PMO Lead",
         "children": [
             {"name": "Ichiro Tanaka", "title": "Analyst"},
             {"name": "Misaki Suzuki", "title": "Analyst"},
         ]},
        {"name": "Ken Takahashi",  "title": "Tech Lead",
         "children": [
             {"name": "Ryo Watanabe",  "title": "Engineer"},
         ]},
        {"name": "Makoto Ito",  "title": "Change Lead", "children": []},
    ]
}

FILLS   = [DARKEST_PURPLE, DARK_PURPLE, OFF_WHITE]
TCOLORS = [WHITE,          WHITE,       TEXT_BODY]

def _leaves(node):
    if not node.get("children"):
        return 1
    return sum(_leaves(c) for c in node["children"])

def _draw_org(slide, node, level, x_left, y_top):
    lc   = _leaves(node)
    span = lc * BOX_W + max(lc - 1, 0) * H_GAP
    x_c  = x_left + span / 2
    y    = y_top + level * (BOX_H + V_GAP)

    fill = FILLS[min(level, len(FILLS) - 1)]
    tcol = TCOLORS[min(level, len(TCOLORS) - 1)]

    box = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(x_c - BOX_W / 2), Inches(y), Inches(BOX_W), Inches(BOX_H))
    box.fill.solid(); box.fill.fore_color.rgb = fill; box.line.fill.background()
    tf = box.text_frame; tf.word_wrap = False
    p1 = tf.paragraphs[0]; p1.text = node["name"]
    p1.font.size = Pt(12); p1.font.bold = True
    p1.font.color.rgb = tcol; p1.font.name = FONT; p1.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph(); p2.text = node.get("title", "")
    p2.font.size = Pt(12); p2.font.color.rgb = tcol; p2.font.name = FONT
    p2.alignment = PP_ALIGN.CENTER
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

    if node.get("children"):
        child_y = y_top + (level + 1) * (BOX_H + V_GAP)
        cx = x_left
        for child in node["children"]:
            cl      = _leaves(child)
            child_w = cl * BOX_W + max(cl - 1, 0) * H_GAP
            child_c = cx + child_w / 2
            add_connector_arrow(slide,
                x_c,       y + BOX_H,
                child_c,   child_y,
                LIGHT_GRAY, width_pt=1, arrow_end=False)
            _draw_org(slide, child, level + 1, cx, y_top)
            cx += child_w + H_GAP

total_w = _leaves(org) * BOX_W + max(_leaves(org) - 1, 0) * H_GAP
_draw_org(slide, org, 0, ML + (CW - total_w) / 2, CY + 0.10)
```

**Tips:**
- If total width exceeds CW: reduce to `H_GAP=0.15`, `BOX_W=1.80`
- If title text is long: change to `BOX_H=0.80`, `tf.word_wrap=True`
- For 2 levels only (flat organization): list members in `org["children"]` with `"children": []`
- To add department icons: overlay with `add_icon()` on top-left of BOX (see `icon_utils.py`)
- For team introduction (photo cards), use Pattern N Base

---


## Pattern P — Process Flow
**Use**: Multi-step process with visual flow direction (4–6 steps)

Uses `add_chevron_flow()` from `native_shapes.py`.

**Standard style (required): `shape_style='chevron'` + `use_pentagon_first=True`**

```
[▷ Step1][▷ Step2][▷ Step3][▷ Step4][▷ Step5]
 homePlate  chevron  chevron  chevron  chevron
```
- **Left end only homePlate** (OOXML: `homePlate`, left side straight, right pointed) -- do not use `pentagon`
- **All remaining are chevron** (OOXML: `chevron`, left indented, right pointed)
- **All items must fit on a single row. Two-tier or multi-row splitting is strictly forbidden**
- `use_pentagon_first=False` forbidden

Auxiliary style: `shape_style='box_triangle'` -- rectangle + right-pointing triangle separator
Triangle has **height:width = 1:3** (unrotated cy:cx = 1:3). After 90 degrees CW rotation: screen height = box full height h, width = h/3 slim right-pointing triangle.
**WARNING: box_triangle rules:**
- Separator triangle is **always right-pointing**. Left-pointing is strictly forbidden. Internally uses `rotation_deg=-90` (OOXML 90 degrees CW). (`rotation_deg=+90` produces LEFT-pointing, so never use it)
- `gap` must be **0.10" or more** to ensure clear whitespace between Box and the triangle

```
[Step 1]  ▷  [Step 2]  ▷  [Step 3]  ▷  [Step 4]
  Detail         Detail         Detail         Detail
```

**WARNING: y-coordinate rules (vertical centering required):**
- **With detail text**: vertically center the entire chevron + detail text group
  ```python
  FLOW_H   = 0.80   # Chevron height
  GAP      = 0.25   # Gap between chevron and detail text
  DETAIL_H = 3.00   # Detail text area height (adjust by content volume)
  # Vertically center the entire group (relative to AH=5.35, CY=1.50)
  FLOW_Y   = CY + (AH - FLOW_H - GAP - DETAIL_H) / 2   # ≈ 1.65"
  DETAIL_Y = FLOW_Y + FLOW_H + GAP
  ```
- **Without detail text (flow only)**: `FLOW_Y = CY + (AH - FLOW_H) / 2` (vertically centered)
- Always verify with thumbnail that shapes and detail text do not overlap

```python
from native_shapes import add_chevron_flow

steps = ["Plan", "Design", "Develop", "Test", "Release"]
details = [
    "• Requirements definition & scope confirmation\n• Stakeholder alignment: all departments",
    "• Architecture design\n• Technology selection: cloud-native adoption",
    "• Implementation & unit testing\n• Code review: PR approval required",
    "• Integration testing & UAT\n• Quality gate check: zero defects",
    "• Production deployment\n• Migration & handover: SLA agreement",
]


FLOW_H   = 0.80   # Chevron height
GAP      = 0.25   # Gap between chevron and detail text
DETAIL_H = 3.00   # Detail text area height (adjust by content volume)
# Vertically center the entire group
FLOW_Y   = CY + (AH - FLOW_H - GAP - DETAIL_H) / 2
DETAIL_Y = FLOW_Y + FLOW_H + GAP

# Standard chevron style — use_pentagon_first=True required (left end=pentagon, rest=chevron)
add_chevron_flow(
    slide, steps,
    x=ML, y=FLOW_Y, total_w=CW, h=FLOW_H,
    gap=0.05,
    fill_color=DARKEST_PURPLE,
    text_color=WHITE,
    font_name=FONT,
    font_size_pt=14,
    shape_style='chevron',              # <- Standard style (required)
    use_pentagon_first=True,            # <- Required: left end=pentagon, rest=chevron
)

# box_triangle style (auxiliary): gap>=0.10 required, triangle is right-pointing only
# add_chevron_flow(..., shape_style='box_triangle', gap=0.10, use_pentagon_first=True)

# Detail text boxes — starting from vertically centered DETAIL_Y
n = len(steps)
flow_box_w = CW / n
for i, detail in enumerate(details):
    tb = slide.shapes.add_textbox(
        Inches(ML + i * flow_box_w), Inches(DETAIL_Y),
        Inches(flow_box_w - 0.10), Inches(DETAIL_H))
    tf = tb.text_frame; tf.word_wrap = True
    for j, line in enumerate(detail.split("
")):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = line; p.font.size = Pt(14)
        p.font.color.rgb = TEXT_BODY; p.font.name = FONT
```

**Tip**: To bold a keyword inside the subtitle (e.g., "Fortification"), use text runs:
```python
from pptx.oxml.ns import qn as _qn
tf = tb_sub.text_frame; tf.clear()
p = tf.paragraphs[0]
r1 = p.add_run(); r1.text = "Platform "
r1.font.size = Pt(18); r1.font.color.rgb = TEXT_BODY; r1.font.name = FONT
r2 = p.add_run(); r2.text = "Fortification"
r2.font.size = Pt(18); r2.font.bold = True; r2.font.color.rgb = DARK_PURPLE; r2.font.name = FONT
```

---

### Variant: Multi-row Process Flow (7+ steps, multiple rows)
**Use**: When 7+ steps do not fit in a single row. Split into multiple rows connected by down arrows between rows. (`add_chevron_flow` only supports one row/direction, so split into 2 rows)

```
[▷ S1][▷ S2][▷ S3][▷ S4][▷ S5]  <- Row 1 (DARKEST_PURPLE)
                                  ▼
[▷ S6][▷ S7][▷ S8][▷ S9][▷ S10] <- Row 2 (DARK_PURPLE)
```

```python
from native_shapes import add_chevron_flow, add_arrow_down
import math

steps = [
    "Current Analysis", "Issue Definition", "Hypothesis", "Data Collection", "Data Analysis",
    "Initiative Eval", "Initiative Design", "Prototype", "Impl Plan", "Execution",
]

ROW_H    = 0.70   # Chevron height
GAP_H    = 0.55   # Row gap (including arrow space)
ROW_SIZE = math.ceil(len(steps) / 2)   # Even split
ROW_W    = CW - 0.55   # Reserve arrow space at right end

row1 = steps[:ROW_SIZE]
row2 = steps[ROW_SIZE:]

# Row 1 (left to right)
add_chevron_flow(
    slide, row1,
    x=ML, y=CY, total_w=ROW_W, h=ROW_H,
    gap=0.05, fill_color=DARKEST_PURPLE, text_color=WHITE,
    font_name=FONT, font_size_pt=12,
    shape_style='chevron', use_pentagon_first=True,
)

# Down arrow between rows (at right end of row 1)
add_arrow_down(slide, ML + ROW_W + 0.05, CY + ROW_H * 0.2, 0.40, GAP_H * 0.8, DARKEST_PURPLE)

# Row 2 (left to right, different color to indicate phase change)
ROW2_Y = CY + ROW_H + GAP_H
add_chevron_flow(
    slide, row2,
    x=ML, y=ROW2_Y, total_w=ROW_W, h=ROW_H,
    gap=0.05, fill_color=DARK_PURPLE, text_color=WHITE,
    font_name=FONT, font_size_pt=12,
    shape_style='chevron', use_pentagon_first=True,
)

# Detail text (calculate DETAIL_Y per row)
DETAIL1_Y = CY + ROW_H + 0.10
DETAIL2_Y = ROW2_Y + ROW_H + 0.10
col_w = ROW_W / ROW_SIZE
details1 = ["• Detail\n• Detail"] * len(row1)
details2 = ["• Detail\n• Detail"] * len(row2)

for i, detail in enumerate(details1):
    tb = slide.shapes.add_textbox(
        Inches(ML + i * col_w), Inches(DETAIL1_Y),
        Inches(col_w - 0.08), Inches(GAP_H - 0.20))
    tf = tb.text_frame; tf.word_wrap = True
    for j, line in enumerate(detail.split("\n")):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = line; p.font.size = Pt(12); p.font.color.rgb = TEXT_BODY; p.font.name = FONT
```

**Tips:**
- `ROW_SIZE = ceil(len(steps) / 2)` for even split. With odd numbers, row 1 gets one extra
- Different `fill_color` for row 1 vs row 2 makes phase distinction visual (DARKEST_PURPLE / DARK_PURPLE)
- Detail text `h` should be around `GAP_H - 0.20`. Ensure `DETAIL_Y + h < ROW2_Y` always holds

---

### Variant: Iterative Loop (iterative flow with feedback)
**Use**: Sprint cycles like design->implement->test->feedback, iterative improvement processes (Slides 18-20 type). Combines forward flow with return feedback arrows.

```
[▷ Discover][▷ Design][▷ Build][▷ Validate]
<------------ Feedback -------------------
```

```python
from native_shapes import add_chevron_flow, add_connector_arrow

STEPS   = ["Discover", "Design", "Build", "Validate"]
FLOW_H  = 0.80

add_chevron_flow(
    slide, STEPS,
    x=ML, y=CY, total_w=CW, h=FLOW_H,
    gap=0.05, fill_color=DARKEST_PURPLE, text_color=WHITE,
    font_name=FONT, font_size_pt=14,
    shape_style='chevron', use_pentagon_first=True,
)

# Detail text for each step (directly below chevron)
DETAIL_Y = CY + FLOW_H + 0.12
n = len(STEPS)
col_w = CW / n
details = [
    "• User interviews\n• Problem definition",
    "• Wireframes\n• Prototyping",
    "• Sprint development\n• Unit testing",
    "• UAT & user validation\n• Improvement collection",
]
for i, detail in enumerate(details):
    tb = slide.shapes.add_textbox(
        Inches(ML + i * col_w), Inches(DETAIL_Y),
        Inches(col_w - 0.10), Inches(0.70))
    tf = tb.text_frame; tf.word_wrap = True
    for j, line in enumerate(detail.split("\n")):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = line; p.font.size = Pt(12); p.font.color.rgb = TEXT_BODY; p.font.name = FONT

# Feedback arrow (right end -> left end, right-to-left = arrow_end=True for left-pointing arrow)
LOOP_Y = DETAIL_Y + 0.80   # Below detail text
add_connector_arrow(slide,
    ML + CW, LOOP_Y,   # start: right edge
    ML,      LOOP_Y,   # end:   left edge
    CORE_PURPLE, width_pt=2.5, arrow_end=True)

# Feedback label
fb = slide.shapes.add_textbox(
    Inches(ML + CW / 2 - 1.20), Inches(LOOP_Y + 0.06),
    Inches(2.40), Inches(0.30))
p = fb.text_frame.paragraphs[0]; p.text = "Feedback / Iteration"
p.font.size = Pt(12); p.font.color.rgb = MID_GRAY; p.font.name = FONT
p.alignment = PP_ALIGN.CENTER
```

**Tips:**
- For multi-layer iteration (Iterative Flow 3/4: Slides 19-20): stack each layer as an independent chevron row with different `y`, and add right-to-left feedback arrows for each row
- Place `LOOP_Y` below detail text and adjust so it does not exceed `BY - 0.30`
- `connector_type="elbow"` creates an L-shaped connector that routes from below (see `connector_type` parameter of `add_connector_arrow`)

---

## Pattern Q — Icon Grid
**Use**: Service catalog, feature overview, category listing (4–9 icons)

Icon (0.50") + label below. 3-column default, can use 2 or 4 columns.
Uses `icon_utils.add_icon_grid()`.

```
[☁️]  [🤝]  [📊]
Cloud  Deal  Chart

[💡]  [🛡️]  [🌍]
Idea  Safety Global
```

```python
from icon_utils import add_icon_grid

items = [
    ("cloud", "Cloud"),
    ("handshake", "Partners"),
    ("chart", "Analytics"),
    ("bulb", "Innovation"),
    ("security", "Security"),   # "shield" may not exist -> try "security" / "lock"
    ("globe", "Global"),
]

add_icon_grid(
    slide, prs,
    items=items,
    x=ML, y=2.40,
    total_w=CW, total_h=3.80,
    cols=3,
    icon_size=0.55,
    font_name=FONT,
    font_size_pt=12,
)
```

Without icon_index.json (first run), add_icon falls back to a labeled placeholder box.

> WARNING: **Always verify keywords with `find_icons(keyword)` beforehand.** Specifying a non-existent keyword results in no icon (label only). Verify before script generation:
> ```python
> from icon_utils import find_icons
> for kw in ["cloud", "handshake", "chart", "bulb", "security", "lock", "globe"]:
>     print(kw, find_icons(kw)[:1])
> ```
> Alternative keyword examples: Security -> `"security"` / `"lock"` / `"shield"`, AI -> `"robot"` / `"brain"` / `"ai"`, People/Team -> `"person"` / `"team"` / `"people"`

---

## Pattern R — Split Visual
**Use**: Image or diagram (left 40%) + text explanation (right 60%)

Useful when you have a screenshot, diagram, or photo to anchor the narrative.

| Shape | x | y | w | h | Fill |
|-------|---|---|---|---|------|
| Title | ML | CY | CW | 0.55 | NONE | 28pt bold BLACK |
| Visual box | ML | 2.35 | 5.10 | 4.20 | OFF_WHITE |
| Visual bar | ML | 2.35 | 5.10 | 0.06 | CORE_PURPLE |
| Text area | 5.80 | 2.35 | 6.90 | 4.20 | NONE |
| Lead | 5.80 | 2.40 | 6.90 | 0.55 | NONE | 18pt TEXT_BODY |
| Body | 5.80 | 3.05 | 6.90 | 3.40 | NONE | 14pt TEXT_BODY |

Visual box shows "[ Figure / Image ]" placeholder or use `add_image_fit()`.

---

---

## Pattern S — Framework Matrix
**Use**: Comparison frameworks, diagnostic rubrics, evaluation tables with labeled rows

Left column = purple row labels, right 1–2 columns = content. Use a python-pptx table for automatic row height handling.

```
┌──────────┬──────────────────────┬──────────────────────┐
│          │ Column Header A        │ Column Header B        │
├──────────┼──────────────────────┼──────────────────────┤
│ Label 1   │ • Issue description     │ Countermeasure/Key     │
├──────────┼──────────────────────┼──────────────────────┤
│ Label 2   │ • Content              │ Content                │
└──────────┴──────────────────────┴──────────────────────┘
```

| Shape | x | y | w | h | Fill | Font |
|-------|---|---|---|---|------|------|
| Table | ML | CY | CW | BY-CY-0.20 | — | — |
| Header row cells | — | — | — | — | DARKEST_PURPLE | 14pt bold WHITE center |
| Label col cells | — | — | 1.80 | — | DARKEST_PURPLE | 14pt bold WHITE center |
| Content cells | — | — | auto | — | WHITE | 14pt TEXT_BODY |

```python
labels   = ["Strategy & Policy", "Operations", "Data", "Applications"]
col_a    = ["• No company-wide policy, each dept runs isolated PoCs...", "• Dept-first approach leads to local optimization...", "• Bottom-up model exploration...", "• App selected without considering requirements..."]
col_b    = ["Identify KGI/KPIs and prioritize", "Define ideal cross-departmental, globally optimized operations", "Organize data model based on ideal operations", "Select applications after organizing data model"]

n_rows = len(labels)
table = slide.shapes.add_table(
    n_rows + 1, 3,
    Inches(ML), Inches(CY), Inches(CW), Inches(BY - CY - 0.20)
).table

table.columns[0].width = Inches(1.80)   # label
table.columns[1].width = Inches(5.20)   # col A
table.columns[2].width = Inches(5.50)   # col B

# Header row
for c, hdr in enumerate(["", "Common Challenges", "Keys to Success"]):
    cell = table.cell(0, c)
    cell.fill.solid(); cell.fill.fore_color.rgb = DARKEST_PURPLE
    p = cell.text_frame.paragraphs[0]
    p.text = hdr; p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT
    p.alignment = PP_ALIGN.CENTER

# Data rows
from pptx.oxml.ns import qn as _qn
for r, (lbl, ca, cb) in enumerate(zip(labels, col_a, col_b), 1):
    # Label cell
    lc = table.cell(r, 0)
    lc.fill.solid(); lc.fill.fore_color.rgb = DARKEST_PURPLE
    lp = lc.text_frame.paragraphs[0]
    lp.text = lbl; lp.font.size = Pt(14); lp.font.bold = True
    lp.font.color.rgb = WHITE; lp.font.name = FONT
    lp.alignment = PP_ALIGN.CENTER
    lc.text_frame._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')
    # Content cells
    for col, text in [(1, ca), (2, cb)]:
        cc = table.cell(r, col)
        cc.fill.solid(); cc.fill.fore_color.rgb = WHITE
        cp = cc.text_frame.paragraphs[0]
        cp.text = text; cp.font.size = Pt(14)
        cp.font.color.rgb = TEXT_BODY; cp.font.name = FONT
```

**Tips:**
- Multi-line bullets in a cell: `cell.text_frame.add_paragraph()` for each line
- Emphasize specific text in a cell using runs with `run.font.bold = True` or `run.font.color.rgb = DARK_PURPLE`
- For a narrow single-column variant (no col B), set `table.columns[1].width = Inches(10.70)` and omit column 2

---

## Pattern T — Two-Section with Arrow (Problem & Proposal)
**Use**: Problem → solution, background → proposal, as-is → to-be (2 stacked sections)

Two panels stacked vertically, each with a narrow purple label on the left and white body on the right. A filled arrow connects them.

```
┌─────────────────────────────────────────────┐
│ Label A │ Background & issue description (bullets)  │
│        │ • Point 1                               │
│        │ • Point 2                               │
└─────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│ Label B │ Proposal content (bullets)               │
│        │ • Point 1                               │
│        │ * Supplementary notes                    │
└─────────────────────────────────────────────┘
```

| Shape | x | y | w | h | Fill |
|-------|---|---|---|---|------|
| Section A bg | ML | CY | CW | section_h | OFF_WHITE, border LIGHT_GRAY |
| Section A label | ML | CY | LABEL_W | section_h | DARKEST_PURPLE |
| Section A content | ML+LABEL_W+0.10 | CY+0.15 | CW-LABEL_W-0.15 | section_h-0.30 | NONE |
| Arrow (down) | center, ~6.17 | CY+section_h+0.08 | 1.0 | 0.40 | DARKEST_PURPLE |
| Section B bg | ML | CY+section_h+0.55 | CW | section_h | OFF_WHITE, border LIGHT_GRAY |
| Section B label | ML | CY+section_h+0.55 | LABEL_W | section_h | DARKEST_PURPLE |
| Section B content | ML+LABEL_W+0.10 | … | CW-LABEL_W-0.15 | section_h-0.30 | NONE |

```python
from native_shapes import add_arrow_down
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.oxml.ns import qn as _qn

LABEL_W  = 1.60
ARROW_H  = 0.45
GAP      = 0.10
section_h = (BY - CY - ARROW_H - GAP * 3) / 2   # ~2.10" each

sections = [
    {"label": "Proposal\nBackground", "body": "• Background item 1\n• Background item 2\n• Background item 3"},
    {"label": "Proposal\nContent",  "body": "• Proposal item 1\n• Proposal item 2\n* Supplementary notes"},
]

for i, sec in enumerate(sections):
    sy = CY + i * (section_h + ARROW_H + GAP)

    # Panel background with border
    bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(ML), Inches(sy), Inches(CW), Inches(section_h))
    bg.fill.solid(); bg.fill.fore_color.rgb = OFF_WHITE
    bg.line.color.rgb = LIGHT_GRAY; bg.line.width = Pt(0.75)

    # Left label box
    lbl = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(ML), Inches(sy), Inches(LABEL_W), Inches(section_h))
    lbl.fill.solid(); lbl.fill.fore_color.rgb = DARKEST_PURPLE
    lbl.line.fill.background()
    tf = lbl.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = sec["label"]
    p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT
    p.alignment = PP_ALIGN.CENTER
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

    # Content area
    cx = ML + LABEL_W + 0.10
    cw = CW - LABEL_W - 0.15
    tb = slide.shapes.add_textbox(Inches(cx), Inches(sy + 0.15), Inches(cw), Inches(section_h - 0.30))
    tf2 = tb.text_frame; tf2.word_wrap = True
    for j, line in enumerate(sec["body"].split("\n")):
        p2 = tf2.paragraphs[0] if j == 0 else tf2.add_paragraph()
        p2.text = line; p2.font.size = Pt(14)
        p2.font.color.rgb = TEXT_BODY; p2.font.name = FONT

    # Arrow between sections
    if i < len(sections) - 1:
        ax = (13.333 / 2) - 0.50   # centered
        add_arrow_down(slide, ax, sy + section_h + GAP, 1.0, ARROW_H, DARKEST_PURPLE)
```

**Tips:**
- For 3+ sections, reduce `section_h` and `ARROW_H` proportionally
- Highlight key words inside body text using `run.font.bold = True` on a text run
- To widen the label column for longer labels, increase `LABEL_W` and adjust `cx`/`cw`

---

### Variant: 3-Section Cascade (3+ sections)
**Use**: Background->issues->proposal, problem->cause->solution, and other 3+ tier logical structures (Slides 26-32 type). Simply change the number of elements in `sections` list to support 2-4 sections.

```
┌───────────────────────────────────────┐
│ Background │ External environment changes (market shrink...) │
└───────────────────────────────────────┘
                    ▼
┌───────────────────────────────────────┐
│ Issues     │ Delay in digitizing customer touchpoints...    │
└───────────────────────────────────────┘
                    ▼
┌───────────────────────────────────────┐
│ Proposal   │ CRM unified platform implementation             │
└───────────────────────────────────────┘
```

```python
from native_shapes import add_arrow_down
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.oxml.ns import qn as _qn

sections = [
    {"label": "Background",   "body": "• External environment changes (market shrinkage, intensified competition)\n• Limits of traditional model due to accelerating digitalization"},
    {"label": "Issues",   "body": "• Delayed digitization of customer touchpoints, declining CX\n• Information silos within organization causing disconnection"},
    {"label": "Proposal",   "body": "• Implement CRM unified platform\n• Establish cross-functional organization and KPI governance\n• PoC in 3 months -> rollout in 12 months"},
]

LABEL_W  = 1.60
ARROW_H  = 0.38
GAP      = 0.08
n        = len(sections)   # Supports 2-4

# Calculate section height evenly from available area
section_h = (BY - CY - ARROW_H * (n - 1) - GAP * n * 2) / n

for i, sec in enumerate(sections):
    sy = CY + i * (section_h + ARROW_H + GAP * 2)

    # Panel background
    bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(ML), Inches(sy), Inches(CW), Inches(section_h))
    bg.fill.solid(); bg.fill.fore_color.rgb = OFF_WHITE
    bg.line.color.rgb = LIGHT_GRAY; bg.line.width = Pt(0.75)

    # Left label
    lbl = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(ML), Inches(sy), Inches(LABEL_W), Inches(section_h))
    lbl.fill.solid(); lbl.fill.fore_color.rgb = DARKEST_PURPLE; lbl.line.fill.background()
    tf = lbl.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = sec["label"]
    p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT; p.alignment = PP_ALIGN.CENTER
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

    # Content
    cx = ML + LABEL_W + 0.10
    cw = CW - LABEL_W - 0.15
    tb = slide.shapes.add_textbox(Inches(cx), Inches(sy + 0.15), Inches(cw), Inches(section_h - 0.30))
    tf2 = tb.text_frame; tf2.word_wrap = True
    for j, line in enumerate(sec["body"].split("\n")):
        p2 = tf2.paragraphs[0] if j == 0 else tf2.add_paragraph()
        p2.text = line; p2.font.size = Pt(14)
        p2.font.color.rgb = TEXT_BODY; p2.font.name = FONT

    # Arrow (except last section)
    if i < n - 1:
        ax = (13.333 / 2) - 0.50
        add_arrow_down(slide, ax, sy + section_h + GAP, 1.0, ARROW_H, DARKEST_PURPLE)
```

**Tips:**
- `n=2`: `section_h ~ 2.10"` with plenty of room (same as Base). `n=4`: `section_h ~ 1.10"` is narrow, limit bullets to 2-3 lines
- To move label column to right side: change to `bg.x=ML`, `lbl.x=ML+CW-LABEL_W`, `cx=ML`, `cw=CW-LABEL_W-0.15`
- To use different label colors per section: pick `lbl.fill.fore_color.rgb` from `[DARKEST_PURPLE, DARK_PURPLE, CORE_PURPLE]` list

---

## Pattern U — Three Column with Icons and Summary Bar
**Use**: Service pillars, value propositions with icons, benefit overview with footer tagline

Three equal columns (no background fill), each with an icon, a CORE_PURPLE accent line, bold header, and bullet list. A LIGHTEST_PURPLE summary bar spans the bottom.

```
[ icon ]          [ icon ]          [ icon ]
─────────         ─────────         ─────────
Header 1          Header 2          Header 3
• Bullet point        • Bullet point        • Bullet point
• Detail            • Detail            • Detail
┌─────────────── Summary text ──────────────────┐
└───────────────────────────────────────────┘
```

| Shape | x | y | w | h | Fill | Font |
|-------|---|---|---|---|------|------|
| Icon [n] | col center | CY | icon_size | icon_size | image | — |
| Accent line [n] | col x | CY+icon+0.12 | col_w | 0.05 | CORE_PURPLE | — |
| Header [n] | col x | CY+icon+0.25 | col_w | 0.45 | NONE | 14pt bold DARKEST_PURPLE |
| Body [n] | col x+0.10 | CY+icon+0.78 | col_w-0.10 | body_h | NONE | 14pt TEXT_BODY |
| Footer bar | ML | BY-footer_h-0.10 | CW | footer_h | LIGHTEST_PURPLE | — |
| Footer text | ML+0.20 | footer bar y | CW-0.40 | footer_h | NONE | 14pt bold DARKEST_PURPLE center |

```python
from icon_utils import add_icon
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

ICON_SIZE = 0.55
FOOTER_H  = 0.55
N_COLS    = 3
GAP       = 0.30
col_w     = (CW - GAP * (N_COLS - 1)) / N_COLS   # ≈3.97"
footer_y  = BY - FOOTER_H - 0.10
body_h    = footer_y - (CY + ICON_SIZE + 0.78) - 0.10

columns = [
    {"icon": "chart",    "header": "Productivity improvement using design data",      "body": ["Auto-generate code from DB design data", "Auto-analyze source code for consistency checks"]},
    {"icon": "chat",     "header": "Enhanced collaboration within dev teams", "body": ["Automate reminders via chat integration", "Streamline procedures through workflows"]},
    {"icon": "dashboard","header": "Improved project management",           "body": ["Auto-generate accurate status reports", "Predictive analysis based on data"]},
]

for i, col in enumerate(columns):
    cx = ML + i * (col_w + GAP)

    # Icon (centered in column)
    add_icon(slide, prs, col["icon"], cx + (col_w - ICON_SIZE) / 2, CY, ICON_SIZE)

    # Accent line below icon
    line_y = CY + ICON_SIZE + 0.12
    bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(cx), Inches(line_y), Inches(col_w), Inches(0.05))
    bar.fill.solid(); bar.fill.fore_color.rgb = CORE_PURPLE
    bar.line.fill.background()

    # Header
    hdr = slide.shapes.add_textbox(Inches(cx), Inches(line_y + 0.12), Inches(col_w), Inches(0.45))
    hp = hdr.text_frame; hp.word_wrap = True
    p = hp.paragraphs[0]; p.text = col["header"]
    p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = DARKEST_PURPLE; p.font.name = FONT

    # Body bullets
    body = slide.shapes.add_textbox(Inches(cx + 0.10), Inches(line_y + 0.65), Inches(col_w - 0.10), Inches(body_h))
    bt = body.text_frame; bt.word_wrap = True
    for j, bullet in enumerate(col["body"]):
        p2 = bt.paragraphs[0] if j == 0 else bt.add_paragraph()
        p2.text = f"• {bullet}"; p2.font.size = Pt(14)
        p2.font.color.rgb = TEXT_BODY; p2.font.name = FONT

# Footer summary bar
fbar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
    Inches(ML), Inches(footer_y), Inches(CW), Inches(FOOTER_H))
fbar.fill.solid(); fbar.fill.fore_color.rgb = LIGHTEST_PURPLE
fbar.line.fill.background()

ft = slide.shapes.add_textbox(Inches(ML + 0.20), Inches(footer_y + 0.08), Inches(CW - 0.40), Inches(FOOTER_H - 0.10))
fp = ft.text_frame.paragraphs[0]
fp.text = "Enter summary message here"
fp.font.size = Pt(14); fp.font.bold = True
fp.font.color.rgb = DARKEST_PURPLE; fp.font.name = FONT
fp.alignment = PP_ALIGN.CENTER
```

**Tips:**
- If no icons are available, replace the icon area with a large number badge (DARKEST_PURPLE box, 28pt WHITE bold, centered)
- For 4 columns, set `N_COLS = 4` and reduce `GAP = 0.20`
- The footer bar is optional — omit it if the slide has no single-sentence conclusion

---

## Pattern V — Numbered Card Grid
**Use**: 5–12 equal-weight concepts each with a short explanation (e.g., 8 reasons, 6 principles)

This extends Pattern F (2×2) to larger N×M grids. Each card has a numbered circle badge,
a tinted header area with a bold title, and body text below.

```
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ (1) Title 1          │  │ (2) Title 2          │  │ (3) Title 3          │  │ (4) Title 4          │
├──────────────────────┤  ├──────────────────────┤  ├──────────────────────┤  ├──────────────────────┤
│ • Description text        │  │ • Description text        │  │ • Description text        │  │ • Description text        │
│                      │  │                      │  │                      │  │                      │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ (5) Title 5          │  │ (6) Title 6          │  │ (7) Title 7          │  │ (8) Title 8          │
├──────────────────────┤  ├──────────────────────┤  ├──────────────────────┤  ├──────────────────────┤
│ • Description text        │  │ • Description text        │  │ • Description text        │  │ • Description text        │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

Reference dimensions (2 rows × 4 cols, total grid = CW × AH):
Card grid starts at **y = 1.61" (4.1cm)** from the top of the slide — leaves room for title + 2-line message.

| Shape | x | y | w | h | Fill |
|-------|---|---|---|---|------|
| Card background | col×(card_w+gap) | row×(card_h+gap) | 2.975" | 2.475" | OFF_WHITE, **no border** |
| Header band | same x | same y | card_w | 0.65" | LIGHTEST_PURPLE |
| Badge (circle) | card_x+0.10 | card_y+(band-0.32)/2 | 0.32" | 0.32" | DARK_PURPLE |
| Badge number | inside badge | — | — | — | 12pt bold WHITE center |
| Title | card_x+0.50 | card_y+0.06 | card_w-0.58 | band | 14pt bold DARK_PURPLE |
| Body | card_x+0.10 | card_y+0.73 | card_w-0.20 | card_h-0.77 | 14pt TEXT_BODY |

> WARNING: **Card borders are forbidden.** Do not pass `highlight_indices`. All cards must use `bg.line.fill.background()` (no border) only.

Card dimensions for n_cols=4, n_rows=2 (y_start=1.61"):
- gap_h = 0.20", gap_v = 0.20"
- card_w = (12.50 - 0.20×3) / 4 = 2.975"
- card_h = (BY - 1.61 - 0.20×1) / 2 ≈ 2.475"

```python
import sys, os
_SKILL = os.path.join(os.path.expanduser("~"), ".claude", "skills", "acnpptx", "scripts")
sys.path.insert(0, _SKILL)
from helpers import *
from pattern_v import add_numbered_card_grid

cards = [
    {"title": "Securing DX-focused\nLeadership",
     "body": "• Secure leadership that champions your DX initiatives while strongly engaging technical staff"},
    {"title": "Talent Acquisition through\nDX-specific Compensation & HR Policies",
     "body": "• Establish competitive compensation and flexible work arrangements tailored to DX talent needs"},
    {"title": "Effective Personnel Exchange\n& Development Programs",
     "body": "• Strengthen your talent through personnel exchanges and development programs involving external partners"},
    {"title": "Promoting Collaboration\nwith Ecosystem Partners",
     "body": "• Form a broad ecosystem with domestic and international companies, universities, NPOs, and individuals to collaboratively drive your DX"},
    # ... 4 more cards ...
]

# 2×4 grid (default) — no colored borders
add_numbered_card_grid(
    slide, cards,
    n_cols=4,
    # highlight_indices is forbidden (no borders)
)
```

**Tips:**
- **`highlight_indices` is forbidden** (do not use colored borders). Omitting it results in all cards having no border
- Y start position defaults to 1.61" (4.1cm). Grid appears below 2-line message
- For 2×3 (6 cards): `n_cols=3` — card dimensions auto-calculated
- For 2×2 (4 cards with badges): `n_cols=2` — similar to F but with numbered badges
- Body text should have 1–3 bullets per card; more than 4 bullets causes overflow at 14pt
- The badge circle uses MSO_AUTO_SHAPE_TYPE.OVAL — this is correctly rounded, not a rectangle
- Import: `from pattern_v import add_numbered_card_grid`

---

## Pattern W — Open-Canvas KPI (Large Statistics)
**Use**: 2–4 large statistics that must make an immediate visual impact — without card backgrounds.
Contrast with Pattern J (which uses OFF_WHITE card panels): Pattern W uses the white slide canvas
with thin gray dividers, letting the typography itself carry the weight.

```
         │                    │
  > 50%  │    6.4 hours       │   52%
         │                    │
 Description  │   Description      │   Description
         │                    │
Source: ...  │   Source: ...       │   Source: ...
```

| Shape | x | y | w | h | Fill | Font |
|-------|---|---|---|---|------|------|
| Divider line [n] | ML + (n+1)×col_w | CY | 0.02" | BY-CY-0.20 | LIGHT_GRAY | — |
| Stat value | col center | CY+0.30 | col_w-0.20 | 1.20 | NONE | 64pt bold DARKEST_PURPLE center |
| Stat label | col center | CY+1.60 | col_w-0.20 | 0.50 | NONE | 18pt bold TEXT_BODY center |
| Stat detail | col center | CY+2.20 | col_w-0.20 | 1.40 | NONE | 14pt TEXT_BODY center |
| Source text | col center | BY-0.55 | col_w-0.20 | 0.45 | NONE | 12pt MID_GRAY center |

```python
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

stats = [
    {
        "value":  "> 50%",
        "label":  "Internet Penetration Rate",
        "detail": "More than half of the world's population, 4.5 billion people, have access to the internet",
        "source": "Source: Internet World Stats: Usage and Population Statistics.",
    },
    {
        "value":  "6.4 hours",
        "label":  "Daily Online Hours",
        "detail": "People are constantly connected to all types of devices, spending an average of 6.4 hours per day online worldwide",
        "source": "Source: Salim, S. (2019, February 4). More Than Six Hours of Our Day Is Spent Online.",
    },
    {
        "value":  "52%",
        "label":  "Technology Dependence",
        "detail": "52% of consumers responded that technology plays an important role in their daily lives",
        "source": "Source: Technology Vision 2020 research. Survey of 2,000 consumers in China, India, UK, and US",
    },
]

n = len(stats)
col_w = CW / n

# Vertical divider lines (n-1 lines between columns)
for i in range(1, n):
    lx = ML + i * col_w
    div = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(lx), Inches(CY), Inches(0.02), Inches(BY - CY - 0.20))
    div.fill.solid(); div.fill.fore_color.rgb = LIGHT_GRAY
    div.line.fill.background()

# Stat columns
def _stat_tb(slide, text, x, y, w, h, size, bold, color, font):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text; p.font.size = Pt(size); p.font.bold = bold
    p.font.color.rgb = color; p.font.name = font
    p.alignment = PP_ALIGN.CENTER
    return tb

for i, stat in enumerate(stats):
    cx  = ML + i * col_w
    cxp = cx + 0.15         # padded x
    cw  = col_w - 0.30      # padded width

    _stat_tb(slide, stat["value"],  cxp, CY + 0.30, cw, 1.20, 64, True,  DARKEST_PURPLE, FONT)
    _stat_tb(slide, stat["label"],  cxp, CY + 1.60, cw, 0.50, 18, True,  TEXT_BODY,      FONT)
    _stat_tb(slide, stat["detail"], cxp, CY + 2.20, cw, 1.40, 14, False, TEXT_BODY,      FONT)
    _stat_tb(slide, stat.get("source", ""), cxp, BY - 0.55, cw, 0.45, 12, False, MID_GRAY, FONT)
```

**When to use W vs J:**
- **W** — when the numbers ARE the message; minimal chrome, maximum typographic impact
- **J** — when each KPI needs structured context (card panel, label, detail line in a contained box)

**Tips:**
- 64pt is the default value size; for very long strings (e.g., "6.4 hours") reduce to 48pt
- Divider lines are optional — omit them for a fully open canvas
- Source citations are optional per stat; omit `"source"` key or pass empty string

**Variant: 2x2 Grid (4 statistics, Slide 53 type)**

Arrange 4 statistics in a 2x2 grid. Add horizontal dividers in addition to vertical dividers.

```python
stats_2x2 = [
    {"value": "> 50%",   "label": "Penetration",   "detail": "More than half the world population"},
    {"value": "6.4h",    "label": "Online Hours",   "detail": "Daily average (all devices)"},
    {"value": "52%",     "label": "Dependence",     "detail": "Technology dependence"},
    {"value": "¥12.4T",  "label": "Market Size",    "detail": "2030 digital market forecast"},
]
# 2×2: 2 columns, 2 rows
COLS, ROWS = 2, 2
col_w = CW / COLS
row_h = (BY - CY - 0.10) / ROWS

# Dividers
for c in range(1, COLS):
    div = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(ML + c * col_w), Inches(CY), Inches(0.02), Inches(BY - CY - 0.10))
    div.fill.solid(); div.fill.fore_color.rgb = LIGHT_GRAY; div.line.fill.background()
for r in range(1, ROWS):
    hdiv = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(ML), Inches(CY + r * row_h), Inches(CW), Inches(0.02))
    hdiv.fill.solid(); hdiv.fill.fore_color.rgb = LIGHT_GRAY; hdiv.line.fill.background()

for idx, stat in enumerate(stats_2x2):
    col = idx % COLS
    row = idx // COLS
    cx  = ML + col * col_w + 0.15
    cw  = col_w - 0.30
    cy  = CY + row * row_h
    _stat_tb(slide, stat["value"],  cx, cy + 0.20, cw, 0.90, 48, True,  DARKEST_PURPLE, FONT)
    _stat_tb(slide, stat["label"],  cx, cy + 1.15, cw, 0.40, 18, True,  TEXT_BODY,      FONT)
    _stat_tb(slide, stat["detail"], cx, cy + 1.60, cw, 0.80, 14, False, TEXT_BODY,      FONT)
```

---

## Pattern X — Step Chart (Phased Step Chart)
**Use**: Multi-phase process with grouped steps — each phase spans multiple columns, each step has detailed content (3–7 total steps across 2–4 phases)

Uses `add_step_chart()` from `pattern_x.py`.

Unlike Pattern P (chevron flow), Pattern X shows **phase grouping headers** spanning multiple steps and provides a **detail area** with bullets below each step. Best for roadmaps, transformation plans, and phased implementation processes.

```
[  Analysis  ][      Build        ][     Operations    ]  <-- phase header (DARKEST_PURPLE)
[ 1.Market Analysis ][ 2.System Build ][ 3.Security ][ 4.Operations ][ 5.Ecosystem ]  <-- step header (LIGHTEST_PURPLE)
┌────────────┐┌────────────────┐┌────────────────┐┌────────────┐┌──────────────┐
│- Market Needs ││- Capital Invest   ││- Risk Mgmt        ││- Test Ops     ││- Collaboration│  <-- detail (OFF_WHITE)
│  Research     ││  Equipment Select ││  Risk Assessment  ││  Test Exec    ││  Ecosystem    │
│  Regulations  ││  Talent Dev       ││  Training         ││  Improve Cycle││  Joint R&D    │
│- Tech Select  ││- Process Design   ││                ││- Improve Cycle││              │
│  Tech Choice  ││  Digitalization   ││                ││  Framework    ││            │
└────────────┘└────────────────┘└────────────────┘└────────────┘└──────────────┘
```

**3 vertical zones:**

| Zone | y | h | Fill | Font |
|------|---|---|------|------|
| Phase header | CY | 0.45" | DARKEST_PURPLE | 14pt bold WHITE center |
| Step header | CY+0.45 | 0.50" | LIGHTEST_PURPLE | 14pt bold DARK_PURPLE center |
| Detail area | CY+0.95 | remaining | OFF_WHITE + LIGHT_GRAY border | 14pt TEXT_BODY |

| Shape | Fill | Notes |
|-------|------|-------|
| Phase bar | DARKEST_PURPLE | Spans multiple step columns |
| Step header box | LIGHTEST_PURPLE | 1 per step, numbered "1. Title" |
| Detail panel | OFF_WHITE, 0.5pt LIGHT_GRAY border | Bullet content |
| Subtitle (optional) | — | ●bold BLACK inside detail |
| Bullets | — | 14pt TEXT_BODY |

```python
from pattern_x import add_step_chart

phases = [
    {
        "label": "Analysis",
        "steps": [
            {"title": "Market Analysis", "subtitle": "Market Needs",
             "bullets": [
                 "Thoroughly research market needs and extract elements required for smart factory transformation",
                 "Investigate related regulations and laws, and clarify compliance requirements",
             ]},
        ],
    },
    {
        "label": "Build",
        "steps": [
            {"title": "System Build", "subtitle": "Capital Investment",
             "bullets": [
                 "Select required equipment and establish investment plan",
                 "Develop talent training programs for new equipment deployment",
             ]},
            {"title": "Security", "subtitle": "Risk Management",
             "bullets": [
                 "Assess cybersecurity risks and implement countermeasures",
                 "Conduct security training to raise employee awareness",
             ]},
        ],
    },
    {
        "label": "Operations",
        "steps": [
            {"title": "Ops Improvement", "subtitle": "Test Operations",
             "bullets": [
                 "Conduct operational testing of the new system and identify issues",
                 "Improve the system based on feedback",
             ]},
            {"title": "Ecosystem", "subtitle": "Collaboration Structure",
             "bullets": [
                 "Build ecosystem with related companies and establish mutually beneficial relationships",
                 "Promote innovation through joint research and co-development",
             ]},
        ],
    },
]

add_step_chart(slide, phases)
```

**Tips:**
- Phase header color can be customized per phase: `{"label": "Analysis", "color": CORE_PURPLE, "steps": [...]}`
- `subtitle` is optional — omit for simpler layouts with only bullets
- Recommended: 3–7 total steps across 2–4 phases
- Each step should have 2–5 bullets for balanced density
- Pattern P (chevron) is better for simple linear flows; Pattern X is better when you need phase grouping and detailed content per step
- Import: `from pattern_x import add_step_chart`

---

## Pattern H — Circular Flow / Cycle Diagram
**Use**: PDCA cycles, iterative processes, continuous improvement loops (3-5 steps)

Place boxes in a circle and connect with clockwise arrows. Circular version of Pattern P (linear flow).

```
              [Plan]
             /      \
        [Act]         [Do]
             \      /
             [Check]
```

**Coordinate calculation approach (4 items = PDCA example):**

| Position | Clock direction | box top-left x | box top-left y |
|------|---------|-----------|-----------|
| Top (12 o'clock) | Step 1 | CX_CENTER - BOX_W/2 | CY_CENTER - RADIUS - BOX_H/2 |
| Right (3 o'clock) | Step 2 | CX_CENTER + RADIUS - BOX_W/2 | CY_CENTER - BOX_H/2 |
| Bottom (6 o'clock) | Step 3 | CX_CENTER - BOX_W/2 | CY_CENTER + RADIUS - BOX_H/2 |
| Left (9 o'clock) | Step 4 | CX_CENTER - RADIUS - BOX_W/2 | CY_CENTER - BOX_H/2 |

Constants: `CX_CENTER=6.667"`, `CY_CENTER=4.175"` (content area center), `RADIUS=1.80"`, `BOX_W=2.20"`, `BOX_H=0.75"`

```python
import math
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.oxml.ns import qn as _qn
from native_shapes import add_connector_arrow

items = [
    {"label": "Plan",  "detail": "• Goal/KPI setting\n• Initiative planning & scope definition"},
    {"label": "Do",  "detail": "• Initiative deployment & resource allocation\n• Progress monitoring"},
    {"label": "Check",  "detail": "• KPI measurement & impact analysis\n• Gap identification"},
    {"label": "Act",  "detail": "• Issue organization & action planning\n• Reflect in next cycle"},
]
n = len(items)

CX_CENTER = 13.333 / 2              # 6.667"
CY_CENTER = CY + (BY - CY) * 0.44  # 3.854" — upper-shifted (reserve detail space above/below)
RADIUS    = 1.50
BOX_W     = 2.00
BOX_H     = 0.60
DETAIL_W  = 2.00

# (1) Start at 12 o'clock, set angles clockwise (math angles are counter-clockwise)
angles = [90 - i * (360 / n) for i in range(n)]

box_positions = []
for a in angles:
    rad = math.radians(a)
    bx = CX_CENTER + RADIUS * math.cos(rad) - BOX_W / 2
    by = CY_CENTER - RADIUS * math.sin(rad) - BOX_H / 2
    box_positions.append((bx, by))

box_centers = [(bx + BOX_W / 2, by + BOX_H / 2) for bx, by in box_positions]

# (2) Draw boxes
for i, (item, (bx, by)) in enumerate(zip(items, box_positions)):
    box = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(bx), Inches(by), Inches(BOX_W), Inches(BOX_H))
    box.fill.solid(); box.fill.fore_color.rgb = DARKEST_PURPLE
    box.line.fill.background()
    tf = box.text_frame
    p = tf.paragraphs[0]; p.text = item["label"]
    p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT; p.alignment = PP_ALIGN.CENTER
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

# (3) Connecting arrows (clockwise)
half_diag = math.sqrt((BOX_W / 2) ** 2 + (BOX_H / 2) ** 2)
for i in range(n):
    cx1, cy1 = box_centers[i]
    cx2, cy2 = box_centers[(i + 1) % n]
    dx = cx2 - cx1; dy = cy2 - cy1
    d  = math.sqrt(dx ** 2 + dy ** 2)
    sx = cx1 + (dx / d) * half_diag
    sy = cy1 + (dy / d) * half_diag
    ex = cx2 - (dx / d) * half_diag
    ey = cy2 - (dy / d) * half_diag
    add_connector_arrow(slide, sx, sy, ex, ey, CORE_PURPLE, width_pt=2)

# (4) Detail text (placed outside boxes by direction)
# Place text at a position away from each box based on its angle.
# By placing outside with a fixed offset from the box edge rather than polar radius,
# overlap with boxes is reliably prevented.
DETAIL_H = 0.50   # Textbox height
PAD = 0.10         # Padding between box and text
for i, (item, (bx, by)) in enumerate(zip(items, box_positions)):
    a = angles[i]
    # Direction check: top(45<a<=135), right(-45<a<=45), bottom(-135<a<=-45), left(rest)
    if 45 < a <= 135:       # Top -> text is above box
        tx = bx + (BOX_W - DETAIL_W) / 2
        ty = by - DETAIL_H - PAD
    elif -45 < a <= 45:     # Right -> text is to right of box
        tx = bx + BOX_W + PAD
        ty = by + (BOX_H - DETAIL_H) / 2
    elif -135 < a <= -45:   # Bottom -> text is below box
        tx = bx + (BOX_W - DETAIL_W) / 2
        ty = by + BOX_H + PAD
    else:                    # Left -> text is to left of box
        tx = bx - DETAIL_W - PAD
        ty = by + (BOX_H - DETAIL_H) / 2
    # Clamp within slide bounds
    tx = max(ML, min(tx, ML + CW - DETAIL_W))
    ty = max(CY, min(ty, BY - DETAIL_H - 0.10))
    tb = slide.shapes.add_textbox(Inches(tx), Inches(ty), Inches(DETAIL_W), Inches(DETAIL_H))
    tf2 = tb.text_frame; tf2.word_wrap = True
    for j, line in enumerate(item["detail"].split("\n")):
        p2 = tf2.paragraphs[0] if j == 0 else tf2.add_paragraph()
        p2.text = line; p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_BODY; p2.font.name = FONT
```

**Tips:**
- 3 steps: `RADIUS=1.40`, `BOX_W=2.20`
- 5 steps: reduce to `RADIUS=1.80`, `BOX_W=1.60`, `BOX_H=0.55`
- **CY_CENTER should be upper-shifted** (`CY + AH * 0.42` recommended). `(CY + BY) / 2` causes bottom box detail text to exceed slide bottom, get clamped, and overlap with boxes
- If no detail text needed, skip step (4) and make boxes larger to contain details inside
- To place a center circle (CORE_PURPLE) to indicate the theme:
  ```python
  c = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL,
      Inches(CX_CENTER - 0.85), Inches(CY_CENTER - 0.85), Inches(1.70), Inches(1.70))
  c.fill.solid(); c.fill.fore_color.rgb = CORE_PURPLE; c.line.fill.background()
  ```

---

### Variant: Large Cycle (6-9 steps)
**Use**: Circular processes with many steps (6-9 steps). Detail text is omitted, using labels only. Smaller boxes to prevent overlap.

| N | RADIUS | BOX_W | BOX_H | font_size_pt |
|---|--------|-------|-------|-------------|
| 6 | 2.10   | 1.80  | 0.60  | 12 |
| 7 | 2.20   | 1.60  | 0.55  | 12 |
| 8 | 2.20   | 1.50  | 0.50  | 12 |
| 9 | 2.30   | 1.40  | 0.48  | 12 |

```python
import math
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.oxml.ns import qn as _qn
from native_shapes import add_connector_arrow

items = [
    {"label": "Discovery"},
    {"label": "Ideation"},
    {"label": "Prototype"},
    {"label": "Test"},
    {"label": "Implement"},
    {"label": "Evaluate"},
]
n = len(items)   # Can change to 6-9

CX_CENTER = 13.333 / 2
CY_CENTER = (CY + BY) / 2
RADIUS  = 2.10   # Refer to table above based on n
BOX_W   = 1.80
BOX_H   = 0.60
FONT_PT = 12     # 12pt for all sizes (brand rule compliant)

angles = [90 - i * (360 / n) for i in range(n)]
box_positions = []
for a in angles:
    rad = math.radians(a)
    bx = CX_CENTER + RADIUS * math.cos(rad) - BOX_W / 2
    by = CY_CENTER - RADIUS * math.sin(rad) - BOX_H / 2
    box_positions.append((bx, by))
box_centers = [(bx + BOX_W / 2, by + BOX_H / 2) for bx, by in box_positions]

for item, (bx, by) in zip(items, box_positions):
    box = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(bx), Inches(by), Inches(BOX_W), Inches(BOX_H))
    box.fill.solid(); box.fill.fore_color.rgb = DARKEST_PURPLE; box.line.fill.background()
    tf = box.text_frame
    p = tf.paragraphs[0]; p.text = item["label"]
    p.font.size = Pt(FONT_PT); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT; p.alignment = PP_ALIGN.CENTER
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

half_diag = math.sqrt((BOX_W / 2) ** 2 + (BOX_H / 2) ** 2)
for i in range(n):
    cx1, cy1 = box_centers[i]
    cx2, cy2 = box_centers[(i + 1) % n]
    dx = cx2 - cx1; dy = cy2 - cy1
    d  = math.sqrt(dx ** 2 + dy ** 2)
    add_connector_arrow(slide,
        cx1 + (dx / d) * half_diag, cy1 + (dy / d) * half_diag,
        cx2 - (dx / d) * half_diag, cy2 - (dy / d) * half_diag,
        CORE_PURPLE, width_pt=2)

# Optional: add theme label (center circle)
# center = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL,
#     Inches(CX_CENTER - 1.00), Inches(CY_CENTER - 0.45),
#     Inches(2.00), Inches(0.90))
# center.fill.solid(); center.fill.fore_color.rgb = CORE_PURPLE; center.line.fill.background()
# tf = center.text_frame
# p = tf.paragraphs[0]; p.text = "Theme Name"
# p.font.size = Pt(14); p.font.bold = True
# p.font.color.rgb = WHITE; p.font.name = FONT; p.alignment = PP_ALIGN.CENTER
# tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')
```

**WARNING: RADIUS calculation when using center circle (required):**
Adding a center circle risks overlapping with left/right (3/9 o'clock) boxes. Calculate minimum RADIUS with the formula below, **and always set a value equal to or greater than this:**
```
Minimum RADIUS = BOX_W / 2 + center_circle_W / 2 + 0.15
```
Example: BOX_W=2.00, center_W=1.70 -> Minimum RADIUS = 1.00 + 0.85 + 0.15 = **2.00"**
RADIUS=1.50 causes left/right boxes and center circle to overlap by 0.35" each, making shapes appear stuck together.

**Tips:**
- If detail text is needed: expand to `BOX_H=0.80` to fit 2-line text (label + detail) inside the box. Do not use external `DETAIL_RADIUS`
- Using a center circle (CORE_PURPLE) to indicate cycle theme improves visibility (see commented-out section)
- If box spacing is too tight: increase `RADIUS` or reduce `BOX_W` (try both and choose the smaller)
- **Without center circle**: RADIUS=1.50-1.80 is fine. **With center circle**: verify minimum RADIUS with the formula above

---

## Pattern Y — Arrow Roadmap
**Use**: Project schedules and phase-based roadmaps (3-6 rows, up to 12 columns). Place HOME_PLATE arrow tasks on a timeline grid. Completed tasks use dark color (DARK_PURPLE), planned/pending use light color (LIGHTEST_PURPLE).

```
         |Apr   |May   |Jun   |Jul   |Aug   |Sep   |Oct   |Nov   |Dec   |
─────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
         |[> Market Research ->]                                                |
Phase 1  |      [> KPI Setup ->]                                            |
─────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
         |            [> Basic Design ->]                                    |
Phase 2  |                  [> Detail Design ->]                                |
─────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
         |                        [> Development ->]                         |
Phase 3  |                                    [> Testing ->]               |
─────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
Phase 4  |                                          [> UAT ->]         |
```
- Vertical lines on both sides of all months -> months are always enclosed by borders
- Multiple tasks in the same row are split into upper/lower tiers via sub_row -> arrows do not overlap

```python
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE as MSO
from pptx.oxml.ns import qn as _qn

# ── Layout constants ──────────────────────────────────────────────────────
LABEL_W = 1.50          # Row label width (inches)
CHART_X = ML + LABEL_W  # Timeline start x
CHART_W = CW - LABEL_W  # Timeline width
HDR_H   = 0.42          # Header row (month names) height

# ── Timeline & row definitions ──────────────────────────────────────────────────────
periods = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rows    = ["Phase 1: Planning", "Phase 2: Design", "Phase 3: Implementation", "Phase 4: Deployment"]
N_COLS  = len(periods)
N_ROWS  = len(rows)

DATA_H  = AH - HDR_H
ROW_H   = DATA_H / N_ROWS   # Row height
COL_W   = CHART_W / N_COLS

def _cx(c):  return CHART_X + c * COL_W           # Left edge x of column c (inches)

# ── Task definitions: (row, sub_row, max_sub, start_col, span_cols, label, completed)
# - row: Phase row (0-indexed)
# - sub_row: Tier within row (0-indexed). Split into upper/lower tiers when multiple tasks in same row
# - max_sub: Maximum tiers in this row (1=single, 2=upper/lower, 3=three tiers)
# - completed: True=completed (DARK_PURPLE) / False=planned (LIGHTEST_PURPLE)
tasks = [
    (0, 0, 2, 0, 2, "Market Research & Req.",  True),
    (0, 1, 2, 1, 2, "KPI Setup",             True),
    (1, 0, 2, 2, 3, "Basic Design",          True),
    (1, 1, 2, 3, 2, "Detail Design & Review", False),
    (2, 0, 2, 3, 3, "Dev & Unit Test",       False),
    (2, 1, 2, 5, 2, "Integration Test",      False),
    (3, 0, 1, 6, 3, "UAT & Go-live",         False),
]

# Calculate task arrow y/height based on sub_row
PAD = 0.06  # Top/bottom padding
def _ty(r, sub, max_sub):
    """Top y of tier 'sub' within row r"""
    row_top = CY + HDR_H + r * ROW_H
    sub_h = (ROW_H - PAD * 2) / max_sub  # Height per tier
    return row_top + PAD + sub * sub_h

def _task_h(max_sub):
    """Task arrow height based on number of tiers"""
    sub_h = (ROW_H - PAD * 2) / max_sub
    return sub_h - 0.04  # Small gap between tiers

# ── (Optional) Today line: red vertical line at left edge of today_col ──────────────────
today_col  = 2    # 0-indexed. Set to None to hide

# ── (Optional) Milestones: (col, label) ──────────────────────────
milestones = [(4, "Mid Review"), (8, "Final Review")]  # col: 0-indexed

# ──────────────────────────────────────────────────────────────────────
# ── Drawing code ─────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────

# Header background bar (DARKEST_PURPLE, full width)
_hbg = slide.shapes.add_shape(MSO.RECTANGLE,
    Inches(ML), Inches(CY), Inches(CW), Inches(HDR_H))
_hbg.fill.solid(); _hbg.fill.fore_color.rgb = DARKEST_PURPLE
_hbg.line.fill.background()

# Month name text (each column)
for ci, period in enumerate(periods):
    tb = slide.shapes.add_textbox(
        Inches(_cx(ci)), Inches(CY), Inches(COL_W), Inches(HDR_H))
    tf = tb.text_frame; p = tf.paragraphs[0]
    p.text = period; p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(12); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

# Row background (WHITE uniform) + row label (left column)
for ri, row_label in enumerate(rows):
    ry = CY + HDR_H + ri * ROW_H
    bg = slide.shapes.add_shape(MSO.RECTANGLE,
        Inches(ML), Inches(ry), Inches(CW), Inches(ROW_H))
    bg.fill.solid(); bg.fill.fore_color.rgb = WHITE
    bg.line.color.rgb = LIGHT_GRAY

    lb = slide.shapes.add_textbox(
        Inches(ML + 0.08), Inches(ry), Inches(LABEL_W - 0.12), Inches(ROW_H))
    tf = lb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = row_label; p.font.size = Pt(12); p.font.bold = True
    p.font.color.rgb = TEXT_BODY; p.font.name = FONT
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

# Vertical divider lines (left/right boundaries of all months — months are always enclosed)
for ci in range(N_COLS + 1):  # 0 to N_COLS: all boundary lines from left to right
    vl = slide.shapes.add_shape(MSO.RECTANGLE,
        Inches(_cx(ci) - 0.005), Inches(CY + HDR_H),
        Inches(0.01), Inches(DATA_H))
    vl.fill.solid(); vl.fill.fore_color.rgb = LIGHT_GRAY
    vl.line.fill.background()

# Task arrows (HOME_PLATE = right-pointing pentagon, split by sub_row)
for (ri, sub, max_sub, sc, span, label, completed) in tasks:
    tx  = _cx(sc)
    ty  = _ty(ri, sub, max_sub)
    tw  = span * COL_W - 0.06   # 0.06" margin at right edge
    th  = _task_h(max_sub)
    col = DARK_PURPLE     if completed else LIGHTEST_PURPLE
    fg  = WHITE           if completed else TEXT_BODY

    sh = slide.shapes.add_shape(MSO.PENTAGON,
        Inches(tx), Inches(ty), Inches(tw), Inches(th))
    sh.fill.solid(); sh.fill.fore_color.rgb = col
    sh.line.fill.background()

    tf = sh.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    p.text = label
    # Reduce font size for 2+ tiers
    _fsz = Pt(12) if max_sub <= 1 else Pt(11)
    p.font.size = _fsz; p.font.bold = False
    p.font.color.rgb = fg; p.font.name = FONT
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

# Today line (optional)
if today_col is not None:
    _tlx = _cx(today_col)
    _tl = slide.shapes.add_shape(MSO.RECTANGLE,
        Inches(_tlx - 0.01), Inches(CY),
        Inches(0.02), Inches(AH))
    _tl.fill.solid(); _tl.fill.fore_color.rgb = RGBColor(0xFF, 0x00, 0x00)
    _tl.line.fill.background()
    _ttb = slide.shapes.add_textbox(
        Inches(_tlx - 0.25), Inches(CY - 0.20),
        Inches(0.50), Inches(0.20))
    _tp = _ttb.text_frame.paragraphs[0]
    _tp.text = "Today"; _tp.alignment = PP_ALIGN.CENTER
    _tp.font.size = Pt(10); _tp.font.bold = True
    _tp.font.color.rgb = RGBColor(0xFF, 0x00, 0x00); _tp.font.name = FONT

# Milestones (optional: marker + label)
for (mc, mlabel) in milestones:
    _mtb = slide.shapes.add_textbox(
        Inches(_cx(mc) - 0.30), Inches(CY + HDR_H - 0.28),
        Inches(1.20), Inches(0.28))
    _mp = _mtb.text_frame.paragraphs[0]
    _mp.text = f"▼{mlabel}"; _mp.alignment = PP_ALIGN.LEFT
    _mp.font.size = Pt(10); _mp.font.bold = False
    _mp.font.color.rgb = CORE_PURPLE; _mp.font.name = FONT
```

**Tips:**
- **How to determine sub_row**: When multiple tasks exist in the same row, set `max_sub` to the task count for that row, and assign `sub_row=0, 1, ...` to each task. For a single task, use `sub_row=0, max_sub=1`
- **For 3 tiers**: set `max_sub=3` for 3-tier split. Font auto-reduces to `Pt(11)`
- For many rows (5+): `ROW_H` becomes narrow, adjust `PAD = 0.04`
- For weekly granularity: change `periods` to a week number list (e.g., `["1w","2w","3w","4w","5w","6w","7w","8w"]`)
- Legend (top-right): add small HOME_PLATE + text for completed/planned at top-right corner (`x~ML+CW-2.00, y~CY+0.05`)
- Group rows (category dividers): set `is_category=True` row backgrounds to `OFF_WHITE` + `DARKEST_PURPLE` left accent bar (width 0.06") for visual distinction
- **Borders**: vertical dividers placed at `range(N_COLS + 1)` for all month left/right edges. Months are always enclosed by borders

---

## Pattern Z — Maturity Model
**Use**: Current vs. target maturity assessment, capability assessment (5-8 dimensions)

Horizontal axis for maturity levels (Basic -> Leading), vertical for evaluation targets. Current state (filled dot) and target (outlined dot) connected by bar.

```
           Basic  Advanced  Leading  Emerging
Strategy      ●──────────────○
Operations    ●────○
Data                 ●──────────────○
Applications         ●────○
Technology    ●──────────────────────○
```

```python
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.oxml.ns import qn as _qn

LEVELS = ["Basic", "Developing", "Advanced", "Leading"]
N_LEVELS = len(LEVELS)

# current/target: 0-based index into LEVELS
capabilities = [
    {"name": "Strategy & Policy",    "current": 0, "target": 2},
    {"name": "Business Processes",   "current": 0, "target": 1},
    {"name": "Data Management",      "current": 1, "target": 3},
    {"name": "Applications",         "current": 1, "target": 2},
    {"name": "Technology",           "current": 0, "target": 3},
    {"name": "People & Organization","current": 0, "target": 2},
]
N_CAPS = len(capabilities)

LABEL_W  = 2.10
SCALE_W  = CW - LABEL_W
COL_W    = SCALE_W / N_LEVELS
HEADER_H = 0.45
ROW_H    = (BY - CY - HEADER_H - 0.60) / N_CAPS
GRID_Y   = CY + HEADER_H + 0.10
DOT_R    = 0.14

# Scale header
for i, level in enumerate(LEVELS):
    lx = ML + LABEL_W + i * COL_W
    hbg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(lx), Inches(CY), Inches(COL_W - 0.03), Inches(HEADER_H))
    hbg.fill.solid(); hbg.fill.fore_color.rgb = DARKEST_PURPLE; hbg.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(lx), Inches(CY), Inches(COL_W), Inches(HEADER_H))
    tf = tb.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]; p.text = level; p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(12); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

def level_cx(idx):
    return ML + LABEL_W + (idx + 0.5) * COL_W

# Capability rows
for r, cap in enumerate(capabilities):
    ry  = GRID_Y + r * ROW_H
    rcy = ry + ROW_H / 2

    # Label
    lbl = slide.shapes.add_textbox(
        Inches(ML), Inches(ry + 0.05), Inches(LABEL_W - 0.15), Inches(ROW_H - 0.10))
    tf = lbl.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]; p.text = cap["name"]
    p.font.size = Pt(14); p.font.color.rgb = TEXT_BODY; p.font.name = FONT
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

    # Row background (solid color — alternating colors forbidden)
    rbg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(ML + LABEL_W), Inches(ry),
        Inches(SCALE_W), Inches(ROW_H - 0.04))
    rbg.fill.solid(); rbg.fill.fore_color.rgb = OFF_WHITE
    rbg.line.color.rgb = LIGHT_GRAY; rbg.line.width = Pt(0.5)

    cur_x = level_cx(cap["current"])
    tgt_x = level_cx(cap["target"])

    # Connection bar (current -> target)
    if cap["current"] != cap["target"]:
        bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
            Inches(min(cur_x, tgt_x) + DOT_R),
            Inches(rcy - 0.04),
            Inches(abs(tgt_x - cur_x) - DOT_R * 2), Inches(0.08))
        bar.fill.solid(); bar.fill.fore_color.rgb = CORE_PURPLE; bar.line.fill.background()

    # Filled dot: current state
    dc = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL,
        Inches(cur_x - DOT_R), Inches(rcy - DOT_R),
        Inches(DOT_R * 2), Inches(DOT_R * 2))
    dc.fill.solid(); dc.fill.fore_color.rgb = DARKEST_PURPLE; dc.line.fill.background()

    # Outlined dot: target
    dt = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL,
        Inches(tgt_x - DOT_R), Inches(rcy - DOT_R),
        Inches(DOT_R * 2), Inches(DOT_R * 2))
    dt.fill.background(); dt.line.color.rgb = CORE_PURPLE; dt.line.width = Pt(2.0)

# Legend
legend_y = GRID_Y + N_CAPS * ROW_H + 0.12
for dot_fill, dot_line, label, ox in [
    (DARKEST_PURPLE, None,        "Current", ML),
    (None,           CORE_PURPLE, "Target", ML + 1.70),
]:
    d = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL,
        Inches(ox), Inches(legend_y), Inches(0.20), Inches(0.20))
    if dot_fill: d.fill.solid(); d.fill.fore_color.rgb = dot_fill
    else:        d.fill.background()
    if dot_line: d.line.color.rgb = dot_line; d.line.width = Pt(2.0)
    else:        d.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(ox + 0.28), Inches(legend_y - 0.03), Inches(1.20), Inches(0.28))
    p = tb.text_frame.paragraphs[0]; p.text = label
    p.font.size = Pt(12); p.font.color.rgb = TEXT_BODY; p.font.name = FONT
```

**Tips:**
- To change scale labels: `LEVELS = ["Level 1", ..., "Level 5"]`
- If current == target: omit the connection bar and fill `dot_tgt` with DARKEST_PURPLE
- To separate rows into groups: insert separator rows (DARKEST_PURPLE label rows)

---

## Pattern AA — 2x2 Quadrant Matrix (Priority / Portfolio Matrix)
**Use**: Priority evaluation, Quick Win identification, portfolio analysis (Y-axis: value/impact, X-axis: difficulty/cost)

Color-code 4 quadrants and place items as numbered circles in each quadrant.

```
     High Impact
  ┌──────────┬──────────┐
  │ Quick Win│ Strategic│
  │ (2)(5)   │   (1)(8) │
  ├──────────┼──────────┤
  │  Avoid   │ Big Bet  │
  │  (4)     │  (3)(6)  │
  └──────────┴──────────┘
     Low Impact    High Difficulty
```

```python
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.oxml.ns import qn as _qn

QUAD_W    = CW / 2
AXIS_H    = 0.45
GRID_Y    = CY + AXIS_H
QUAD_H    = (BY - GRID_Y - 0.45) / 2
DOT_SIZE  = 0.32

quadrants = [
    {"label": "Quick Win",  "desc": "Prioritize",  "x": ML,          "y": GRID_Y,          "fill": LIGHTEST_PURPLE,              "text": DARKEST_PURPLE},
    {"label": "Strategic",  "desc": "Strategic Investment", "x": ML + QUAD_W, "y": GRID_Y,          "fill": RGBColor(0xE0, 0xCC, 0xFF),   "text": DARKEST_PURPLE},
    {"label": "Avoid",      "desc": "Low Priority",  "x": ML,          "y": GRID_Y + QUAD_H, "fill": RGBColor(0xF5, 0xF5, 0xF5),   "text": MID_GRAY},
    {"label": "Big Bet",    "desc": "Long-term Investment",  "x": ML + QUAD_W, "y": GRID_Y + QUAD_H, "fill": OFF_WHITE,                    "text": TEXT_BODY},
]

# Draw quadrants
for q in quadrants:
    bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(q["x"]), Inches(q["y"]),
        Inches(QUAD_W - 0.05), Inches(QUAD_H - 0.05))
    bg.fill.solid(); bg.fill.fore_color.rgb = q["fill"]
    bg.line.color.rgb = LIGHT_GRAY; bg.line.width = Pt(0.75)

    ql = slide.shapes.add_textbox(
        Inches(q["x"] + 0.12), Inches(q["y"] + 0.10),
        Inches(QUAD_W - 0.24), Inches(0.55))
    tf = ql.text_frame; tf.word_wrap = False
    p1 = tf.paragraphs[0]; p1.text = q["label"]
    p1.font.size = Pt(14); p1.font.bold = True
    p1.font.color.rgb = q["text"]; p1.font.name = FONT
    p2 = tf.add_paragraph(); p2.text = q["desc"]
    p2.font.size = Pt(12); p2.font.color.rgb = MID_GRAY; p2.font.name = FONT

# Axis labels
for text, x, y, align in [
    ("High Impact", ML,          GRID_Y - 0.40, PP_ALIGN.LEFT),
    ("Low Impact", ML,          GRID_Y + QUAD_H * 2 + 0.05, PP_ALIGN.LEFT),
    ("Low Difficulty",   ML,          GRID_Y - 0.40, PP_ALIGN.LEFT),
    ("High Difficulty",   ML + QUAD_W, GRID_Y - 0.40, PP_ALIGN.RIGHT),
]:
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(QUAD_W), Inches(0.35))
    p = tb.text_frame.paragraphs[0]; p.text = text; p.alignment = align
    p.font.size = Pt(12); p.font.color.rgb = MID_GRAY; p.font.name = FONT

# Items (numbered circles)
# x_ratio / y_ratio: specify position within quadrant from 0.0 to 1.0
items = [
    {"num": 1, "name": "CRM Integration",        "q": 1, "x_ratio": 0.65, "y_ratio": 0.35},
    {"num": 2, "name": "Report Automation",  "q": 0, "x_ratio": 0.35, "y_ratio": 0.30},
    {"num": 3, "name": "Core System Renewal","q": 3, "x_ratio": 0.55, "y_ratio": 0.50},
    {"num": 4, "name": "Legacy Form Migration",      "q": 2, "x_ratio": 0.45, "y_ratio": 0.55},
    {"num": 5, "name": "Mobile Support",    "q": 0, "x_ratio": 0.60, "y_ratio": 0.60},
    {"num": 6, "name": "AI Predictive Analytics",     "q": 3, "x_ratio": 0.30, "y_ratio": 0.35},
]

qx_list = [ML, ML + QUAD_W, ML, ML + QUAD_W]
qy_list = [GRID_Y, GRID_Y, GRID_Y + QUAD_H, GRID_Y + QUAD_H]

for item in items:
    qx = qx_list[item["q"]]
    qy = qy_list[item["q"]]
    ix = qx + item["x_ratio"] * (QUAD_W - 0.05) - DOT_SIZE / 2
    iy = qy + item["y_ratio"] * (QUAD_H - 0.05) - DOT_SIZE / 2

    dot = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL,
        Inches(ix), Inches(iy), Inches(DOT_SIZE), Inches(DOT_SIZE))
    dot.fill.solid(); dot.fill.fore_color.rgb = DARKEST_PURPLE; dot.line.fill.background()
    tf = dot.text_frame
    p = tf.paragraphs[0]; p.text = str(item["num"])
    p.font.size = Pt(12); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT; p.alignment = PP_ALIGN.CENTER
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

# Legend (number -> name)
legend_y = GRID_Y + QUAD_H * 2 - len(items) * 0.28 - 0.10
for j, item in enumerate(items):
    tb = slide.shapes.add_textbox(
        Inches(ML + CW * 0.52), Inches(legend_y + j * 0.28),
        Inches(CW * 0.46), Inches(0.26))
    p = tb.text_frame.paragraphs[0]
    p.text = f"{item['num']}. {item['name']}"
    p.font.size = Pt(12); p.font.color.rgb = TEXT_BODY; p.font.name = FONT
```

**Tips:**
- To change axis labels: simply modify `"High Impact"` / `"Low Difficulty"` etc.
- To change quadrant names: update `quadrants[i]["label"]` / `["desc"]`
- Keep `x_ratio` / `y_ratio` within 0.05-0.95 (placing at edges reduces visibility)
- For many items, split legend into 2 columns (`ML + CW * 0.0` and `ML + CW * 0.52`)

**Variant: Shaded Area Only (zone visualization only, Slides 47-48 type)**

Variant that creates an "empty evaluation framework" with only 4-zone coloring and axis labels, without placing items.
In addition to setting `items = []`, change axis labels to X/Y criteria format.

```python
# Use the AA quadrants drawing block as-is
# Set items = [] to skip item drawing loop
# Change to 4 axis labels (top/bottom/left/right)

AXIS_H  = 0.45
GRID_Y  = CY + AXIS_H
QUAD_W  = CW / 2
QUAD_H  = (BY - GRID_Y - 0.45) / 2

# Quadrant labels and colors (customizable by use case)
quadrants = [
    {"label": "Area 1", "x": ML,          "y": GRID_Y,          "fill": LIGHTEST_PURPLE},
    {"label": "Area 2", "x": ML + QUAD_W, "y": GRID_Y,          "fill": RGBColor(0xE0, 0xCC, 0xFF)},
    {"label": "Area 3", "x": ML,          "y": GRID_Y + QUAD_H, "fill": OFF_WHITE},
    {"label": "Area 4", "x": ML + QUAD_W, "y": GRID_Y + QUAD_H, "fill": RGBColor(0xF5, 0xF5, 0xF5)},
]
for q in quadrants:
    bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(q["x"]), Inches(q["y"]),
        Inches(QUAD_W - 0.05), Inches(QUAD_H - 0.05))
    bg.fill.solid(); bg.fill.fore_color.rgb = q["fill"]
    bg.line.color.rgb = LIGHT_GRAY; bg.line.width = Pt(0.75)
    tb = slide.shapes.add_textbox(Inches(q["x"] + 0.15), Inches(q["y"] + 0.15),
        Inches(QUAD_W - 0.30), Inches(0.40))
    p = tb.text_frame.paragraphs[0]; p.text = q["label"]
    p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = TEXT_BODY; p.font.name = FONT

# 4-directional axis labels (X/Y criteria format)
for text, x, y, align in [
    ("▲ Y-Criteria High", ML,          GRID_Y - 0.40, PP_ALIGN.LEFT),
    ("Y-Criteria Low ▼",  ML,          GRID_Y + QUAD_H * 2 + 0.05, PP_ALIGN.LEFT),
    ("◀ X-Criteria Low",  ML,          GRID_Y - 0.40, PP_ALIGN.LEFT),
    ("X-Criteria High ▶", ML + QUAD_W, GRID_Y - 0.40, PP_ALIGN.RIGHT),
]:
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(QUAD_W), Inches(0.35))
    p = tb.text_frame.paragraphs[0]; p.text = text; p.alignment = align
    p.font.size = Pt(12); p.font.color.rgb = MID_GRAY; p.font.name = FONT
```

---

## Pattern AB — Issue Tree / Logic Tree
**Use**: MECE decomposition, issue structuring, root cause analysis (logic tree, issue tree)

Horizontal tree expanding from root node (left) to leaves (right). Nodes auto-positioned via recursive function.

```
 ┌──────────────┐
 │  Root Issue    │──▶ Factor A ──▶ A-1: …
 │              │         └──▶ A-2: …
 │              │──▶ Factor B ──▶ B-1: …
 │              │         └──▶ B-2: …
 │              │              B-3: …
 │              │──▶ Factor C ──▶ C-1: …
 └──────────────┘         └──▶ C-2: …
```

| Element | Shape | Fill | Text |
|---------|-------|------|------|
| Root node | RECTANGLE | DARKEST_PURPLE | WHITE 14pt bold |
| Level 1 nodes | RECTANGLE | DARK_PURPLE | WHITE 12pt |
| Level 2 nodes | RECTANGLE | CORE_PURPLE | WHITE 12pt |
| Level 3+ nodes | RECTANGLE | OFF_WHITE | TEXT_BODY 12pt |
| Connectors | Straight line | LIGHT_GRAY 1pt | — |

```python
from native_shapes import add_connector_arrow
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.oxml.ns import qn as _qn

NODE_W = 1.90   # width of each node box (in)
NODE_H = 0.50   # height of each node box (in)
H_GAP  = 0.50   # horizontal space between levels
V_GAP  = 0.22   # vertical space between siblings
LEVEL_FILLS = [DARKEST_PURPLE, DARK_PURPLE, CORE_PURPLE, OFF_WHITE]
LEVEL_TEXTS = [WHITE,          WHITE,       WHITE,       TEXT_BODY]

# Tree structure: nested dicts with "label" and optional "children"
tree = {
    "label": "Root Issue",
    "children": [
        {"label": "Factor A",
         "children": [{"label": "A-1: Sub-factor"}, {"label": "A-2: Sub-factor"}]},
        {"label": "Factor B",
         "children": [{"label": "B-1: Sub-factor"}, {"label": "B-2: Sub-factor"},
                      {"label": "B-3: Sub-factor"}]},
        {"label": "Factor C",
         "children": [{"label": "C-1: Sub-factor"}, {"label": "C-2: Sub-factor"}]},
    ]
}

def _leaf_count(n):
    if not n.get("children"):
        return 1
    return sum(_leaf_count(c) for c in n["children"])

def _draw_tree(slide, node, level, x, y_top):
    lc      = _leaf_count(node)
    total_h = lc * NODE_H + (lc - 1) * V_GAP
    y_c     = y_top + total_h / 2   # vertical center of this subtree

    fill = LEVEL_FILLS[min(level, len(LEVEL_FILLS) - 1)]
    tcol = LEVEL_TEXTS[min(level, len(LEVEL_TEXTS) - 1)]

    rect = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(x), Inches(y_c - NODE_H / 2), Inches(NODE_W), Inches(NODE_H))
    rect.fill.solid(); rect.fill.fore_color.rgb = fill; rect.line.fill.background()
    tf = rect.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = node["label"]
    p.font.size  = Pt(12 if level > 0 else 13)
    p.font.bold  = (level == 0)
    p.font.color.rgb = tcol; p.font.name = FONT
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

    if node.get("children"):
        child_x = x + NODE_W + H_GAP
        cy = y_top
        for child in node["children"]:
            clc     = _leaf_count(child)
            child_h = clc * NODE_H + (clc - 1) * V_GAP
            child_c = cy + child_h / 2
            # Straight connector: parent right-center → child left-center
            add_connector_arrow(slide,
                x + NODE_W, y_c,
                child_x,    child_c,
                LIGHT_GRAY, width_pt=1, arrow_end=False)
            _draw_tree(slide, child, level + 1, child_x, cy)
            cy += child_h + V_GAP

_draw_tree(slide, tree, 0, ML, CY + 0.20)
```

**Tips:**
- Total tree height = `_leaf_count(tree) * NODE_H + (_leaf_count(tree) - 1) * V_GAP`. Adjust `CY + 0.20` for centering
- For deep hierarchies (4+ levels): reduce `NODE_W` to 1.50 or less, lower font to 12pt (brand rule minimum)
- To convert to vertical tree (top->bottom): swap x/y and use `H_GAP` as `V_GAP`

---

### Variant: Vertical Tree (top->down)
**Use**: Strategy->initiatives, KGI->KPI->actions, or other "top-down concept to execution" structures (Slide 24 type). Shows top-down decision flow more intuitively than horizontal tree.

```
              ┌──────────┐
              │ Strategic Goal │
              └──┬────┬──┘
                 ▼    ▼
         ┌───────┐  ┌───────┐
         │Theme A│  │Theme B│
         └──┬────┘  └───────┘
            ▼
     ┌───────┐ ┌───────┐
     │Init A-1│ │Init A-2│
     └───────┘ └───────┘
```

Convert the horizontal tree (Pattern AB Base) `_draw_tree` function to vertical by "swapping X/Y + width span calculation".

```python
from native_shapes import add_connector_arrow
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.oxml.ns import qn as _qn

NODE_W  = 2.00
NODE_H  = 0.50
H_GAP   = 0.25   # Horizontal gap between siblings
V_GAP   = 0.65   # Vertical gap between levels

LEVEL_FILLS = [DARKEST_PURPLE, DARK_PURPLE, CORE_PURPLE, OFF_WHITE]
LEVEL_TEXTS = [WHITE,          WHITE,       WHITE,       TEXT_BODY]

tree = {
    "label": "Strategic Goal",
    "children": [
        {"label": "Theme A",
         "children": [{"label": "Initiative A-1"}, {"label": "Initiative A-2"}]},
        {"label": "Theme B",
         "children": [{"label": "Initiative B-1"}]},
        {"label": "Theme C",
         "children": [{"label": "Initiative C-1"}, {"label": "Initiative C-2"}]},
    ]
}

def _leaf_count_v(n):
    if not n.get("children"):
        return 1
    return sum(_leaf_count_v(c) for c in n["children"])

def _draw_vtree(slide, node, level, x_left, y_top):
    # Vertical tree: x_left is the horizontal span left edge of this subtree
    lc    = _leaf_count_v(node)
    span  = lc * NODE_W + max(lc - 1, 0) * H_GAP
    x_c   = x_left + span / 2   # Horizontal center of this node
    y     = y_top + level * (NODE_H + V_GAP)

    fill = LEVEL_FILLS[min(level, len(LEVEL_FILLS) - 1)]
    tcol = LEVEL_TEXTS[min(level, len(LEVEL_TEXTS) - 1)]

    rect = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(x_c - NODE_W / 2), Inches(y), Inches(NODE_W), Inches(NODE_H))
    rect.fill.solid(); rect.fill.fore_color.rgb = fill; rect.line.fill.background()
    tf = rect.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = node["label"]
    p.font.size  = Pt(12 if level > 0 else 14)
    p.font.bold  = (level == 0)
    p.font.color.rgb = tcol; p.font.name = FONT; p.alignment = PP_ALIGN.CENTER
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

    if node.get("children"):
        child_y = y_top + (level + 1) * (NODE_H + V_GAP)
        cx = x_left
        for child in node["children"]:
            cl      = _leaf_count_v(child)
            child_w = cl * NODE_W + max(cl - 1, 0) * H_GAP
            child_c = cx + child_w / 2
            add_connector_arrow(slide,
                x_c,      y + NODE_H,
                child_c,  child_y,
                LIGHT_GRAY, width_pt=1, arrow_end=False)
            _draw_vtree(slide, child, level + 1, cx, y_top)
            cx += child_w + H_GAP

total_leaves = _leaf_count_v(tree)
total_tree_w = total_leaves * NODE_W + max(total_leaves - 1, 0) * H_GAP
start_x      = ML + (CW - total_tree_w) / 2   # Horizontal centering
_draw_vtree(slide, tree, 0, start_x, CY + 0.10)
```

**Tips:**
- For many leaf nodes (8+): reduce to `NODE_W=1.50`, `H_GAP=0.15`. Keep total width `total_tree_w` within CW
- For 4+ levels: reduce `V_GAP=0.50` and lower font to 12pt (brand rule minimum)
- Choosing between horizontal tree (Base): "cause->effect" or "problem->solution" is natural horizontally. "strategy->initiatives" or "KGI->KPI->actions" is natural vertically
- Asymmetric trees (Slide 23 type): simply provide tree data with varying child node counts to the horizontal tree (Base) and it auto-adapts (no changes to recursive logic needed)

---

## Pattern AC — Stacked Pyramid
**Use**: Hierarchy visualization (foundation->value, lower->upper), prerequisite build-up, Maslow-type models. 3-5 layers optimal.

```
          ┌────┐
         /  L4  \
        /─────────\
       /    L3      \
      /───────────────\
     /       L2         \
    /─────────────────────\
   /          L1             \
  └───────────────────────────┘
```

| Element | Shape | Fill | Text |
|---------|-------|------|------|
| Pyramid layer | Custom trapezoid (custGeom) | Level color | WHITE 14pt bold / 12pt |
| Sub-label | textbox (centered in trapezoid) | — | Same as fill text color 12pt |

```python
from lxml import etree
from pptx.oxml.ns import qn as _qn
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

LAYERS = [  # Bottom → Top order
    {"label": "Infrastructure",  "sub": "Foundation, Processes, Data",    "fill": DARKEST_PURPLE, "text": WHITE},
    {"label": "Capability",      "sub": "Skills, Tools, Governance", "fill": DARK_PURPLE,   "text": WHITE},
    {"label": "Enablement",      "sub": "Standardization, Risk Management",        "fill": CORE_PURPLE,   "text": WHITE},
    {"label": "Value",           "sub": "Business Value, Customer Experience",     "fill": LIGHT_PURPLE,  "text": DARKEST_PURPLE},
]

PYR_W   = CW          # total base width (in)
PYR_H   = AH - 0.30  # total pyramid height (in)
PYR_Y   = CY + 0.15  # top of pyramid in slide

def _add_trapezoid(slide, x, y, bottom_w, top_w, h, fill_color):
    """Draw a centered isoceles trapezoid using custom geometry."""
    EMU = 914400
    bw  = int(bottom_w * EMU)
    tw  = int(top_w    * EMU)
    off = int((bottom_w - top_w) / 2 * EMU)
    h_e = int(h * EMU)
    sh  = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(x), Inches(y), Inches(bottom_w), Inches(h))
    spPr = sh._element.find(_qn('p:spPr'))
    prstGeom = spPr.find(_qn('a:prstGeom'))
    if prstGeom is not None:
        spPr.remove(prstGeom)
    custGeom_xml = (
        '<a:custGeom xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/>'
        f'<a:rect l="0" t="0" r="{bw}" b="{h_e}"/>'
        '<a:pathLst>'
        f'<a:path w="{bw}" h="{h_e}">'
        f'<a:moveTo><a:pt x="{off}" y="0"/></a:moveTo>'
        f'<a:lnTo><a:pt x="{bw - off}" y="0"/></a:lnTo>'
        f'<a:lnTo><a:pt x="{bw}" y="{h_e}"/></a:lnTo>'
        f'<a:lnTo><a:pt x="0" y="{h_e}"/></a:lnTo>'
        '<a:close/></a:path></a:pathLst>'
        '</a:custGeom>'
    )
    # Insert right after xfrm (index 0 would place it before xfrm, breaking the shape)
    xfrm = spPr.find(_qn('a:xfrm'))
    ins_idx = list(spPr).index(xfrm) + 1 if xfrm is not None else 0
    spPr.insert(ins_idx, etree.fromstring(custGeom_xml))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill_color; sh.line.fill.background()
    return sh

n       = len(LAYERS)
layer_h = PYR_H / n
for i, layer in enumerate(LAYERS):          # i=0 = bottom
    row   = n - 1 - i                       # row 0 = top in drawing
    b_w   = PYR_W * (row + 1) / n          # Trapezoid bottom width (wider for lower layers)
    t_w   = PYR_W * row / n  # Top width (width=0 at row=0 -> pointed apex)
    x     = ML + (PYR_W - b_w) / 2
    y     = PYR_Y + row * layer_h
    _add_trapezoid(slide, x, y, b_w, t_w, layer_h - 0.04, layer["fill"])

    # Text inside trapezoid (horizontally centered)
    mid_w = (b_w + t_w) / 2
    mid_x = x + (b_w - mid_w) / 2
    tb = slide.shapes.add_textbox(
        Inches(mid_x + 0.10), Inches(y + 0.06),
        Inches(mid_w - 0.20), Inches(layer_h - 0.16))
    tf = tb.text_frame; tf.word_wrap = True
    p1 = tf.paragraphs[0]; p1.text = layer["label"]
    p1.font.size = Pt(14); p1.font.bold = True
    p1.font.color.rgb = layer["text"]; p1.font.name = FONT
    p1.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph(); p2.text = layer["sub"]
    p2.font.size = Pt(12); p2.font.color.rgb = layer["text"]; p2.font.name = FONT
    p2.alignment = PP_ALIGN.CENTER
```

**Tips:**
- 3 layers: `layer_h ~ 1.78"` with ample room. 5 layers is `layer_h ~ 1.07"` somewhat tight -> use 12pt font (brand rule minimum)
- To place labels on right side: position textbox at `x = ML + PYR_W + 0.15` and connect with `add_connector_arrow`
- To invert colors (lighter at bottom): reverse the `LAYERS` list order or swap `fill` colors

---

## Pattern AD — Program Status Dashboard (RAG Dashboard)
**Use**: Project status reporting, issue/risk management, RAG (Red/Amber/Green) status visualization

Two-section layout: status table (time, quality, budget etc.) + issues/actions table.

```
 ┌──────────────────────────────────────────────┐
 │ Overall Status   ● GREEN   Comment              │
 │ Time             ● AMBER   Comment              │
 │ Budget           ● RED     Comment              │
 ├──────────────────────────────────────────────┤
 │ Issues / Risks        Responsible   Due Date │
 │ Issue details          Responsible   MM/DD    │
 ├──────────────────────────────────────────────┤
 │ Next Steps            Responsible   Due Date │
 │ Action details         Responsible   MM/DD    │
 └──────────────────────────────────────────────┘
```

| Element | Shape | Fill | Notes |
|---------|-------|------|-------|
| Section header row | RECTANGLE | DARKEST_PURPLE | WHITE 14pt bold |
| Status rows | RECTANGLE | WHITE | RAG indicator (OVAL) + text |
| RAG indicator | OVAL | GREEN / AMBER / RED | 0.22" × 0.22" |
| Issues/Actions table | add_table | DARKEST_PURPLE header | 3 columns |

```python
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

# ── RAG color constants ─────────────────────────────────────────────────
RAG_GREEN = RGBColor(0x00, 0x70, 0x00)
RAG_AMBER = RGBColor(0xFF, 0xA5, 0x00)
RAG_RED   = RGBColor(0xCC, 0x00, 0x00)

# ── Status items ────────────────────────────────────────────────────────
STATUS_ITEMS = [
    {"label": "Time",    "rag": RAG_GREEN, "comment": "Proceeding on schedule. Milestones achieved."},
    {"label": "Budget",  "rag": RAG_AMBER, "comment": "Budget overrun risk. Re-estimation planned at month-end."},
    {"label": "Quality", "rag": RAG_GREEN, "comment": "All quality metrics within baseline. Test completion rate 92%."},
    {"label": "Scope",   "rag": RAG_RED,   "comment": "3 scope addition requests. In change management process."},
]

DOT_SIZE  = 0.22
ROW_H     = 0.55
LABEL_W   = 1.30
DOT_COL_W = 0.40
COMMENT_W = CW - LABEL_W - DOT_COL_W

def _sec_header(slide, y, text):
    hdr = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(ML), Inches(y), Inches(CW), Inches(0.38))
    hdr.fill.solid(); hdr.fill.fore_color.rgb = DARKEST_PURPLE; hdr.line.fill.background()
    tf = hdr.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]; p.text = text
    p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT
    tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')

# ── RAG status section ──────────────────────────────────────────────────
_sec_header(slide, CY, "Overall Status")
ry = CY + 0.40
for item in STATUS_ITEMS:
    rb = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(ML), Inches(ry), Inches(CW), Inches(ROW_H - 0.04))
    rb.fill.solid(); rb.fill.fore_color.rgb = WHITE
    rb.line.color.rgb = LIGHT_GRAY; rb.line.width = Pt(0.5)

    lb = slide.shapes.add_textbox(Inches(ML + 0.10), Inches(ry + 0.06),
        Inches(LABEL_W - 0.10), Inches(ROW_H - 0.10))
    p = lb.text_frame.paragraphs[0]; p.text = item["label"]
    p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = TEXT_BODY; p.font.name = FONT

    dot = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL,
        Inches(ML + LABEL_W + (DOT_COL_W - DOT_SIZE) / 2),
        Inches(ry + (ROW_H - DOT_SIZE) / 2 - 0.04),
        Inches(DOT_SIZE), Inches(DOT_SIZE))
    dot.fill.solid(); dot.fill.fore_color.rgb = item["rag"]; dot.line.fill.background()

    cb = slide.shapes.add_textbox(
        Inches(ML + LABEL_W + DOT_COL_W + 0.10), Inches(ry + 0.07),
        Inches(COMMENT_W - 0.20), Inches(ROW_H - 0.10))
    tf = cb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = item["comment"]
    p.font.size = Pt(12); p.font.color.rgb = TEXT_BODY; p.font.name = FONT
    ry += ROW_H

# ── Issues / Risks table ────────────────────────────────────────────────
_sec_header(slide, ry + 0.10, "Issues / Risks")
ISSUES = [
    {"issue": "External vendor delivery delay (API integration components)",        "owner": "Taro Yamada", "due": "03/20"},
    {"issue": "Insufficient memory in production environment (16GB -> 32GB needed)", "owner": "Hanako Suzuki", "due": "03/25"},
]
issues_y = ry + 0.50
tbl_h    = len(ISSUES) * ROW_H + 0.05
tbl = slide.shapes.add_table(
    len(ISSUES) + 1, 3,
    Inches(ML), Inches(issues_y), Inches(CW), Inches(tbl_h)).table
tbl.columns[0].width = Inches(CW * 0.60)
tbl.columns[1].width = Inches(CW * 0.25)
tbl.columns[2].width = Inches(CW * 0.15)

for j, hdr_text in enumerate(["Issue / Risk", "Responsible", "Due Date"]):
    c = tbl.cell(0, j)
    c.text = hdr_text
    c.fill.solid(); c.fill.fore_color.rgb = DARKEST_PURPLE
    p = c.text_frame.paragraphs[0]
    p.font.size = Pt(12); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT

for i, issue in enumerate(ISSUES):
    for j, val in enumerate([issue["issue"], issue["owner"], issue["due"]]):
        c = tbl.cell(i + 1, j)
        c.text = val
        c.fill.solid(); c.fill.fore_color.rgb = WHITE
        p = c.text_frame.paragraphs[0]
        p.font.size = Pt(12); p.font.color.rgb = TEXT_BODY; p.font.name = FONT
```

**Tips:**
- All status rows must be uniform WHITE (alternating colors forbidden)
- Keep RAG colors as Python constants. Use GREEN/AMBER/RED/GRAY (not started) depending on slide purpose
- Section header spacing: previous section last row y + 0.10" -> header -> + 0.40" -> content
- To add a Next Steps section: repeat the same pattern below the Issues table
- Do not add horizontal lines above table headers (per forbidden rules)

---

## Pattern AE — Venn Diagram
**Use**: Visualize overlap/intersection of 3 concepts (economy/society/environment intersection, skill x business x technology, etc.)

Overlay 3 semi-transparent circles in triangular arrangement. Place label at center intersection.

```
         ╭─────╮
        /  L1   \
       /    ╭────┼──╮
      │  ╭──┼────╯  │
       \  │  ╰──╮  /
        ╰─┼──╮  ╰─╯
          │ L3│
     L2   ╰───╯
```

| Element | Shape | Fill | Notes |
|---------|-------|------|-------|
| Circle 1 (top) | OVAL | DARKEST_PURPLE 55% alpha | 3.20" diameter |
| Circle 2 (bottom-left) | OVAL | DARK_PURPLE 55% alpha | 3.20" diameter |
| Circle 3 (bottom-right) | OVAL | CORE_PURPLE 55% alpha | 3.20" diameter |
| Outer labels | textbox | — | 14pt bold DARKEST_PURPLE |
| Center overlap label | textbox | — | 14pt bold WHITE |

```python
from lxml import etree
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.oxml.ns import qn as _qn

CIRCLE_D = 3.20   # circle diameter (in)
CX_C = ML + CW / 2   # diagram center X
CY_C = CY + AH / 2   # diagram center Y
R    = CIRCLE_D * 0.40  # triangle arrangement radius

# Three circle centers (top, bottom-left, bottom-right)
positions = [
    (CX_C,             CY_C - R * 0.65),  # top
    (CX_C - R * 0.85,  CY_C + R * 0.50),  # bottom-left
    (CX_C + R * 0.85,  CY_C + R * 0.50),  # bottom-right
]
circle_colors = [DARKEST_PURPLE, DARK_PURPLE, CORE_PURPLE]
labels        = ["Economic Growth", "Social Responsibility", "Environmental Protection"]

def _oval_with_alpha(slide, cx, cy, d, rgb_color, alpha_pct=55):
    # Draw an oval with alpha transparency via XML.
    shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL,
        Inches(cx - d / 2), Inches(cy - d / 2), Inches(d), Inches(d))
    shape.line.fill.background()
    spPr = shape._element.find(_qn('p:spPr'))
    solidFill = spPr.find(_qn('a:solidFill'))
    if solidFill is not None:
        spPr.remove(solidFill)
    r, g, b = rgb_color.r, rgb_color.g, rgb_color.b
    fill_xml = (
        '<a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:srgbClr val="{r:02X}{g:02X}{b:02X}">'
        f'<a:alpha val="{int(alpha_pct * 1000)}"/>'
        '</a:srgbClr></a:solidFill>'
    )
    # Insert right after xfrm/prstGeom (index 0 would place it before xfrm, breaking the shape)
    xfrm = spPr.find(_qn('a:xfrm'))
    prstGeom = spPr.find(_qn('a:prstGeom'))
    ref = prstGeom if prstGeom is not None else xfrm
    ins_idx = list(spPr).index(ref) + 1 if ref is not None else 0
    spPr.insert(ins_idx, etree.fromstring(fill_xml))
    return shape

# Draw circles (back to front for Z-order)
for (cx, cy), color in zip(reversed(positions), reversed(circle_colors)):
    _oval_with_alpha(slide, cx, cy, CIRCLE_D, color, alpha_pct=55)

# Outer labels (at non-overlapping portion of each circle)
label_offsets = [
    (0.00, -0.65),   # top circle: above center
    (-0.75, 0.55),   # bottom-left: lower-left
    (0.75,  0.55),   # bottom-right: lower-right
]
for (cx, cy), (dx, dy), label in zip(positions, label_offsets, labels):
    tb = slide.shapes.add_textbox(
        Inches(cx + dx - 1.10), Inches(cy + dy - 0.22),
        Inches(2.20), Inches(0.50))
    tf = tb.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]; p.text = label
    p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = DARKEST_PURPLE; p.font.name = FONT
    p.alignment = PP_ALIGN.CENTER

# Center overlap label
tb_c = slide.shapes.add_textbox(
    Inches(CX_C - 1.00), Inches(CY_C - 0.25),
    Inches(2.00), Inches(0.55))
tf = tb_c.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Shared Commitment"
p.font.size = Pt(14); p.font.bold = True
p.font.color.rgb = WHITE; p.font.name = FONT
p.alignment = PP_ALIGN.CENTER
```

**Tips:**
- `alpha_pct=55` produces natural semi-transparent overlap. 70+ becomes too opaque, making intersections hard to see
- For 2-circle Venn diagram: reduce `positions` to 2 and change arrangement to left/right
- To add supplementary text to each circle: add textboxes at `label_offsets` positions
- Alpha value uses OOXML `val` attribute as `alpha_pct * 1000` (55% = 55000)

---

## Pattern AF — Pull Quote
**Use**: Quoting important statements/survey results, executive impact emphasis, key vision declaration (Slide 54 type)

Maximize visual impact with large decorative quotation marks and center-aligned text. Difference from Pattern D (Key Message): D is for asserting a message, AF is for explicitly quoting a statement.

```
          ❝
    Important message or quote goes here
    displayed large and center-aligned in 2-3 lines.
                                    ❞
        -- Speaker name, title / source
```

| Element | Shape | Fill | Font |
|---------|-------|------|------|
| Opening quote ❝ | textbox | — | 96pt LIGHTEST_PURPLE |
| Closing quote ❞ | textbox | — | 96pt LIGHTEST_PURPLE |
| Quote text | textbox | — | 28pt bold DARKEST_PURPLE center |
| Accent line | RECTANGLE | CORE_PURPLE | w=1.50" h=0.05" centered |
| Attribution | textbox | — | 14pt MID_GRAY center |

```python
QUOTE_TEXT  = "By combining the power of technology and human ingenuity, we can build a better future together. We believe in that possibility."
ATTRIBUTION = "-- Jane Smith, CEO of ExampleCorp (Source: FY2025 Annual Report)"

# Opening quote mark (top-left, decorative)
qm_open = slide.shapes.add_textbox(
    Inches(ML), Inches(CY + 0.05), Inches(1.00), Inches(1.20))
p = qm_open.text_frame.paragraphs[0]; p.text = "\u201C"
p.font.size = Pt(96); p.font.color.rgb = LIGHTEST_PURPLE; p.font.name = FONT

# Quote text (centered, large)
QUOTE_Y = CY + 0.65
QUOTE_H = 3.20
qt = slide.shapes.add_textbox(
    Inches(ML + 0.70), Inches(QUOTE_Y),
    Inches(CW - 1.40), Inches(QUOTE_H))
tf = qt.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = QUOTE_TEXT
p.font.size = Pt(28); p.font.bold = True
p.font.color.rgb = DARKEST_PURPLE; p.font.name = FONT
p.alignment = PP_ALIGN.CENTER

# Closing quote mark (bottom-right)
qm_close = slide.shapes.add_textbox(
    Inches(ML + CW - 1.00), Inches(QUOTE_Y + QUOTE_H - 0.90),
    Inches(1.00), Inches(1.20))
p = qm_close.text_frame.paragraphs[0]; p.text = "\u201D"
p.font.size = Pt(96); p.font.color.rgb = LIGHTEST_PURPLE; p.font.name = FONT

# Accent divider line
div_y = QUOTE_Y + QUOTE_H + 0.15
div = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
    Inches(ML + CW / 2 - 0.75), Inches(div_y), Inches(1.50), Inches(0.05))
div.fill.solid(); div.fill.fore_color.rgb = CORE_PURPLE; div.line.fill.background()

# Attribution
at = slide.shapes.add_textbox(
    Inches(ML), Inches(div_y + 0.20), Inches(CW), Inches(0.45))
p = at.text_frame.paragraphs[0]; p.text = ATTRIBUTION
p.font.size = Pt(14); p.font.color.rgb = MID_GRAY; p.font.name = FONT
p.alignment = PP_ALIGN.CENTER
```

**Tips:**
- For short quotes (1 line): reduce `QUOTE_H = 1.80` and adjust `QUOTE_Y`
- For no-quote-marks simple version (between Pattern D): omit `qm_open` / `qm_close`
- Alternative quote marks: `\u300C` / `\u300D` can be used instead of `\u201C` / `\u201D`
- The accent underline serves as a visual separator between quote and attribution

---

## Pattern AG — Architecture / Connector Diagram
**Use**: System architecture diagrams, flow diagrams, and other diagrammatic slides connecting boxes with lines (arrows). All shapes and connectors are editable as PowerPoint native objects (no PNGs).

```
┌──────────┐               ┌──────────┐
│  Box A   │ ────────────► │  Box B   │
└──────────┘               └──────────┘
      │ (elbow)
      ▼
┌──────────┐               ┌──────────┐
│  Box C   │ ◄────────────►│  Box D   │
└──────────┘               └──────────┘
```

| Element | Shape | Fill | Font |
|---------|-------|------|------|
| Normal box | RECTANGLE | OFF_WHITE | 14pt TEXT_BODY |
| Emphasis box | RECTANGLE | LIGHTEST_PURPLE | 14pt bold DARKEST_PURPLE |
| Header box | RECTANGLE | DARKEST_PURPLE | 14pt bold WHITE |
| Connector (arrow) | add_connector_arrow | — | Line: CORE_PURPLE, 1.5pt |
| Box label | textbox | — | 12pt MID_GRAY (sub-label) |

```python
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE as MSO
from native_shapes import add_connector_arrow

# ── Box creation helper ───────────────────────────────────────────
def make_box(slide, x, y, w, h, label,
             fill=OFF_WHITE, border=LIGHT_GRAY,
             font_size=14, bold=False, text_color=None):
    """Create a box with native rectangle + textbox"""
    if text_color is None:
        text_color = TEXT_BODY
    shape = slide.shapes.add_shape(
        MSO.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid(); shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = border
    tb = slide.shapes.add_textbox(
        Inches(x + 0.08), Inches(y + 0.08),
        Inches(w - 0.16), Inches(h - 0.16))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run(); run.text = label
    run.font.size = Pt(font_size); run.font.bold = bold
    run.font.color.rgb = text_color; run.font.name = FONT
    return shape

# ── Layout constants ────────────────────────────────────────────────
BOX_W, BOX_H = 2.40, 0.72   # Standard box size
COL_GAP = 1.60               # Column gap (connector + margin)
ROW_GAP = 0.80               # Row gap
COL1_X = ML                  # Left column X
COL2_X = ML + BOX_W + COL_GAP  # Right column X
ROW1_Y = CY + 0.20
ROW2_Y = ROW1_Y + BOX_H + ROW_GAP

# ── Box placement ──────────────────────────────────────────────────
make_box(slide, COL1_X, ROW1_Y, BOX_W, BOX_H, "Frontend")
make_box(slide, COL2_X, ROW1_Y, BOX_W, BOX_H, "Backend API",
         fill=LIGHTEST_PURPLE, text_color=DARKEST_PURPLE)
make_box(slide, COL1_X, ROW2_Y, BOX_W, BOX_H, "User DB")
make_box(slide, COL2_X, ROW2_Y, BOX_W, BOX_H, "Analytics Platform",
         fill=DARKEST_PURPLE, text_color=WHITE, bold=True)

# ── Connectors ─────────────────────────────────────────────────────
# A -> B (horizontal, straight)
add_connector_arrow(
    slide,
    x1=COL1_X + BOX_W, y1=ROW1_Y + BOX_H / 2,
    x2=COL2_X,          y2=ROW1_Y + BOX_H / 2,
    color=CORE_PURPLE, width_pt=1.5)

# A -> C (vertical elbow)
add_connector_arrow(
    slide,
    x1=COL1_X + BOX_W / 2, y1=ROW1_Y + BOX_H,
    x2=COL1_X + BOX_W / 2, y2=ROW2_Y,
    color=DARK_PURPLE, width_pt=1.5, connector_type="elbow")

# C <-> D (bidirectional)
add_connector_arrow(
    slide,
    x1=COL1_X + BOX_W, y1=ROW2_Y + BOX_H / 2,
    x2=COL2_X,          y2=ROW2_Y + BOX_H / 2,
    color=CORE_PURPLE, width_pt=1.5, arrow_end=True, arrow_start=True)
```

**Sizing mode:** Adjust `BOX_W` / `COL_GAP` / `ROW_GAP` based on box count and column count. All boxes must fit within `ML` to `ML+CW` (right edge = `ML + CW = 12.92"`).

**Tips:**
- `connector_type='elbow'` -> L-shaped routing (PPT auto-routes)
- `connector_type='curved'` -> organic curved line
- `connector_type='straight'` -> straight line (default)
- Labeled connectors: add textbox near arrow midpoint (12pt MID_GRAY)
- Emphasis box: `fill=LIGHTEST_PURPLE` + `text_color=DARKEST_PURPLE` (normal) or `fill=DARKEST_PURPLE` + `text_color=WHITE` (maximum emphasis)
- For many boxes (6+): reduce to `BOX_W=2.00, BOX_H=0.60` and use `font_size=12`
- For vertical flow (top->down only): `add_arrow_down()` combinations also work
- Rectangle lines: `shape.line.color.rgb = LIGHT_GRAY` (normal) or `shape.line.fill.background()` (no border)

---

## Pattern AH — Decision Matrix

Evaluate multiple options across multiple criteria, visualized with symbols. Similar structure to Pattern S (Framework Matrix), but differs in that cells primarily contain symbol text.

```
┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Options ╲ Criteria│    Cost     │  Feasibility │   Speed      │    Risk     │  ← DARKEST_PURPLE
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Option A (highlight)│      ○     │      △      │      ◎      │      △      │  <- CORE_PURPLE BG
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Option B            │      ◎     │      ○      │      △      │      ○      │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Option C            │      △     │      ◎      │      ○      │      ▲      │
└─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

| Shape | x | y | w | h | Fill | Text |
|-------|---|---|---|---|------|------|
| Table header row | ML | CY | CW | 0.55 | DARKEST_PURPLE | WHITE 14pt bold center |
| Row label (recommended) | ML | — | 1.80 | 0.80 | CORE_PURPLE | WHITE 14pt bold |
| Row label (normal) | ML | — | 1.80 | 0.80 | OFF_WHITE | TEXT_BODY 14pt |
| Symbol cell | — | — | vary | 0.80 | WHITE | Symbol 18pt center BLACK |

**Symbols and meanings:**
| Symbol | Meaning | Font color |
|------|------|-----------|
| ◎ | Excellent / Optimal | BLACK |
| ○ | Good | BLACK |
| △ | Needs review | BLACK |
| × | Unsuitable | BLACK |
| ▲ | Warning | BLACK |

```python
# ── Pattern AH — Decision Matrix ──────────────────────────────────────────
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

criteria  = ["Cost Efficiency", "Feasibility", "Speed", "Risk"]
options   = ["Option A", "Option B", "Option C"]
ratings   = [
    ["○", "△", "◎", "△"],   # Option A (recommended -> highlight row)
    ["◎", "○", "△", "○"],
    ["△", "◎", "○", "▲"],
]
highlight_row = 0  # Recommended candidate row index (0-based)

LABEL_W = 1.80
CELL_W  = (CW - LABEL_W) / len(criteria)
ROW_H   = 0.80
HDR_H   = 0.55

tbl_y = CY

# ── Header row (criteria) ──────────────────────────────────────────────────
hdr = slide.shapes.add_table(1, len(criteria) + 1,
    Inches(ML), Inches(tbl_y),
    Inches(CW), Inches(HDR_H)).table
hdr.columns[0].width = Inches(LABEL_W)
for ci in range(len(criteria)):
    hdr.columns[ci + 1].width = Inches(CELL_W)

# Corner label
c = hdr.cell(0, 0)
c.fill.solid(); c.fill.fore_color.rgb = DARKEST_PURPLE
c.text = "Options ╲ Criteria"
p = c.text_frame.paragraphs[0]
p.font.size = Pt(12); p.font.bold = True
p.font.color.rgb = WHITE; p.font.name = FONT
p.alignment = PP_ALIGN.CENTER

for ci, crit in enumerate(criteria):
    c = hdr.cell(0, ci + 1)
    c.fill.solid(); c.fill.fore_color.rgb = DARKEST_PURPLE
    c.text = crit
    p = c.text_frame.paragraphs[0]
    p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = WHITE; p.font.name = FONT
    p.alignment = PP_ALIGN.CENTER

# ── Data rows ──────────────────────────────────────────────────────────────
for ri, (opt, row_ratings) in enumerate(zip(options, ratings)):
    is_highlight = (ri == highlight_row)
    row_y = tbl_y + HDR_H + ri * ROW_H

    data_tbl = slide.shapes.add_table(1, len(criteria) + 1,
        Inches(ML), Inches(row_y),
        Inches(CW), Inches(ROW_H)).table
    data_tbl.columns[0].width = Inches(LABEL_W)
    for ci in range(len(criteria)):
        data_tbl.columns[ci + 1].width = Inches(CELL_W)

    # Row label
    c = data_tbl.cell(0, 0)
    lbl_fill = CORE_PURPLE if is_highlight else OFF_WHITE
    lbl_text_color = WHITE if is_highlight else TEXT_BODY
    c.fill.solid(); c.fill.fore_color.rgb = lbl_fill
    c.text = opt
    p = c.text_frame.paragraphs[0]
    p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = lbl_text_color; p.font.name = FONT

    # Symbol cells
    for ci, sym in enumerate(row_ratings):
        c = data_tbl.cell(0, ci + 1)
        c.fill.solid(); c.fill.fore_color.rgb = WHITE
        c.text = sym
        p = c.text_frame.paragraphs[0]
        p.font.size = Pt(18); p.font.bold = False
        p.font.color.rgb = BLACK; p.font.name = FONT
        p.alignment = PP_ALIGN.CENTER
```

**Sizing mode:** Adjust `LABEL_W` and `CELL_W` based on criteria count. Fit within total width CW.

**Tips:**
- Recommended row (`highlight_row`) uses CORE_PURPLE for the row label for visual emphasis
- For many columns (5+): `LABEL_W=1.40`, reduce header text to 12pt
- To use numeric scores (1-5) instead of symbols: keep `p.font.size = Pt(18)` center-aligned with numbers

---

## Pattern AI — Evaluation Scorecard

Evaluate multiple options across multiple axes, with the recommended candidate shown as a highlighted row. Final column adds recommendation reason text (-> format).

```
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────────────────┐
│  Item     │ Criteria1 │ Criteria2 │ Criteria3 │ Criteria4 │     Summary         │  ← DARKEST_PURPLE
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────────────────┤
│  Option A  │    ◎    │    ◎    │    ◎    │    —    │-> Best choice        │  ← LIGHTEST_PURPLE BG
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────────────────┤
│  Option B  │    △    │    △    │    △    │    △    │-> Limited            │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────────────────┤
│  Option C  │    △    │    △    │    ×    │    ×    │-> Needs re-evaluation│
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────────────────┘
```

| Shape | Fill | Text |
|-------|------|------|
| Header row | DARKEST_PURPLE | WHITE 14pt bold center |
| Highlight row (recommended) | LIGHTEST_PURPLE | CORE_PURPLE 14pt bold (label column)|
| Normal row | WHITE | TEXT_BODY 14pt |
| Summary cell | same as row | 14pt regular "-> ..."|

```python
# ── Pattern AI — Evaluation Scorecard ────────────────────────────────────
criteria = ["Dev Speed", "Ecosystem", "Learning Cost", "Summary"]
options  = [
    ("Python",  ["◎", "◎", "◎", "-> Mature ecosystem"],  True),   # True = highlight
    ("R",       ["△", "△", "△", "-> Limited talent market"],       False),
    ("Julia",   ["△", "△", "×", "-> Learning cost needs review"],       False),
]

LABEL_W  = 1.80
EVAL_W   = (CW - LABEL_W - 2.80) / (len(criteria) - 1)  # Last column is wider
LAST_W   = 2.80
ROW_H    = 0.90
HDR_H    = 0.55

# Implemented as header row (table 1) + data rows (table N rows) pattern
# Evaluation symbols are center-aligned 18pt / Summary is left-aligned 14pt
```

**Tips:**
- Highlight row label uses CORE_PURPLE bold to indicate recommendation
- Summary column uses -> + short text (under 16 characters)
- Symbol size is 18pt (ensures in-cell visibility)

---

## Pattern AJ — Radar Chart

Overview multi-axis evaluation in spider web form. **Lines only (no fill)** for comparing multiple series.

```
        Technology
          ↑
  Creativity ━━ ━━ Communication
          ↓
   Analysis ←   → Leadership
```

```python
# ── Pattern AJ — Radar Chart (lines only, no fill) ──────────────────────────
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Pt
from pptx.oxml.ns import qn as _qn
from lxml import etree

chart_data = ChartData()
chart_data.categories = ["Technology", "Communication", "Leadership", "Analysis", "Creativity"]
chart_data.add_series("Current", (4, 3, 4, 3, 3))
chart_data.add_series("Target", (5, 4, 5, 4, 4))

# Square layout centered on slide
CHART_W = CW * 0.65   # 8.125"
CHART_H = AH * 0.90   # 4.815"
CHART_X = ML + (CW - CHART_W) / 2
CHART_Y = CY + (AH - CHART_H) / 2

chart_obj = slide.shapes.add_chart(
    XL_CHART_TYPE.RADAR,       # Lines only (no fill)
    Inches(CHART_X), Inches(CHART_Y),
    Inches(CHART_W), Inches(CHART_H),
    chart_data,
)
chart = chart_obj.chart

# ── Axis label font size setting (XML manipulation) ──────────────────────────────
for series in chart.series:
    sp = series._element
    # Set series line width to 2pt
    spPr = sp.find(_qn("c:spPr"))
    if spPr is None:
        spPr = etree.SubElement(sp, _qn("c:spPr"))
    ln = spPr.find(_qn("a:ln"))
    if ln is None:
        ln = etree.SubElement(spPr, _qn("a:ln"))
    ln.set("w", str(int(Pt(2).pt * 12700)))   # EMU

# Place legend at bottom of chart
chart.has_legend = True
from pptx.enum.chart import XL_LEGEND_POSITION
chart.legend.position = XL_LEGEND_POSITION.BOTTOM
chart.legend.include_in_layout = False

# Legend text 12pt
leg_txPr = chart.legend._element.find(_qn("c:txPr"))
# (Optional) Legend font size can be skipped if default (~12pt) is acceptable
```

**Sizing mode:** Center the chart. Maintain `CHART_W : CHART_H ~ 1.7 : 1` ratio, as distortion makes the spider web elliptical.

**Tips:**
- `XL_CHART_TYPE.RADAR` = lines only (no fill). Do not use `RADAR_FILLED`
- Changing series colors requires XML manipulation (`a:ln > a:solidFill > a:srgbClr`)
- Axis maximum can be fixed with `chart.value_axis.maximum_scale = 5` (may not be available in python-pptx radar)
- Practical category count (axes) is 4-8. 3 makes a triangle

---

## Pattern AK — Calendar

Display 3 months of calendars side by side. Include events/holidays as small rectangle badges.

```
┌────────────┬────────────┬────────────┐
│  2026-03   │  2026-04   │  2026-05   │  <- DARKEST_PURPLE header
├─┬─┬─┬─┬─  ├─┬─┬─┬─┬─  ├─┬─┬─┬─┬─  │
│M │T │W │Th│F  │M │T │W │Th│F  │M │T │W │Th│F  │  <- CORE_PURPLE, WHITE 14pt
│  │  │ 1│ 2│ 3 │  │  │  │  │  │  │  │  │  │ 1 │
│ …                                        │
└────────────┴────────────┴────────────┘
```

| Shape | Fill | Text |
|-------|------|------|
| Month header | DARKEST_PURPLE | WHITE 18pt bold center |
| Day-of-week row | CORE_PURPLE | WHITE 12pt bold center |
| Date cell | WHITE / OFF_WHITE (alternating) | 14pt center |
| Event badge | CORE_PURPLE | WHITE 8pt |
| Holiday text | NONE | CORE_PURPLE 8pt |

```python
# ── Pattern AK — Calendar (3 months)──────────────────────────────────────────
import calendar
from datetime import date

YEAR, START_MONTH = 2026, 3   # Start year/month
NUM_MONTHS = 3

# Event definitions: {date(Y, M, D): "Event name"}
EVENTS = {
    date(2026, 3, 20): "Spring Equinox",
    date(2026, 4, 16): "Mid Review",
    date(2026, 4, 29): "Showa Day",
}

WEEKS_DISP = ["Mon", "Tue", "Wed", "Thu", "Fri"]   # Mon-Fri only (weekends omitted)
CAL_X      = ML
CAL_Y      = CY
CAL_W      = CW / NUM_MONTHS - 0.20          # Width per month (inter-month gap 0.20")
HDR_H      = 0.45
DOW_H      = 0.30
CELL_H     = 0.65                            # Date cell height
CELL_W     = CAL_W / len(WEEKS_DISP)

for mi in range(NUM_MONTHS):
    month = START_MONTH + mi
    year  = YEAR + (month - 1) // 12
    month = (month - 1) % 12 + 1
    ox    = CAL_X + mi * (CAL_W + 0.20)

    # Month header
    from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE as MSO
    bg = slide.shapes.add_shape(MSO.RECTANGLE,
        Inches(ox), Inches(CAL_Y), Inches(CAL_W), Inches(HDR_H))
    bg.fill.solid(); bg.fill.fore_color.rgb = DARKEST_PURPLE
    bg.line.fill.background()
    tf = bg.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]; run = p.add_run()
    run.text = f"{year:04d}-{month:02d}"; run.font.size = Pt(18)
    run.font.bold = True; run.font.color.rgb = WHITE; run.font.name = FONT
    from pptx.enum.text import PP_ALIGN; p.alignment = PP_ALIGN.CENTER

    # Day-of-week header
    for di, dow in enumerate(WEEKS_DISP):
        cx = ox + di * CELL_W
        dh = slide.shapes.add_shape(MSO.RECTANGLE,
            Inches(cx), Inches(CAL_Y + HDR_H), Inches(CELL_W), Inches(DOW_H))
        dh.fill.solid(); dh.fill.fore_color.rgb = CORE_PURPLE
        dh.line.fill.background()
        tf = dh.text_frame; tf.word_wrap = False
        p = tf.paragraphs[0]; run = p.add_run()
        run.text = dow; run.font.size = Pt(12)
        run.font.bold = True; run.font.color.rgb = WHITE; run.font.name = FONT
        p.alignment = PP_ALIGN.CENTER

    # Date cells (Mon-Fri only)
    cal = calendar.monthcalendar(year, month)
    for wk_idx, week in enumerate(cal):
        for di, day_num in enumerate(week[:5]):   # 0=Mon, 4=Fri
            if day_num == 0:
                continue
            cx = ox + di * CELL_W
            cy = CAL_Y + HDR_H + DOW_H + wk_idx * CELL_H
            d  = date(year, month, day_num)

            cell_fill = OFF_WHITE if wk_idx % 2 == 0 else WHITE
            ds = slide.shapes.add_shape(MSO.RECTANGLE,
                Inches(cx), Inches(cy), Inches(CELL_W), Inches(CELL_H))
            ds.fill.solid(); ds.fill.fore_color.rgb = cell_fill
            ds.line.color.rgb = LIGHT_GRAY

            # Date number
            tb = slide.shapes.add_textbox(
                Inches(cx + 0.04), Inches(cy + 0.04),
                Inches(CELL_W - 0.08), Inches(0.28))
            tf = tb.text_frame; tf.word_wrap = False
            p = tf.paragraphs[0]; run = p.add_run()
            run.text = str(day_num); run.font.size = Pt(14)
            run.font.color.rgb = TEXT_BODY; run.font.name = FONT
            p.alignment = PP_ALIGN.CENTER

            # Event badge
            if d in EVENTS:
                ev_name = EVENTS[d]
                eb = slide.shapes.add_shape(MSO.RECTANGLE,
                    Inches(cx + 0.04), Inches(cy + 0.32),
                    Inches(CELL_W - 0.08), Inches(0.22))
                eb.fill.solid(); eb.fill.fore_color.rgb = CORE_PURPLE
                eb.line.fill.background()
                tf2 = eb.text_frame; tf2.word_wrap = False
                p2 = tf2.paragraphs[0]; run2 = p2.add_run()
                run2.text = ev_name; run2.font.size = Pt(8)
                run2.font.color.rgb = WHITE; run2.font.name = FONT
                p2.alignment = PP_ALIGN.CENTER
```

**Sizing mode:** Adjust `CAL_W` and `CELL_W` based on month count and day-of-week count (Mon-Fri vs Mon-Sat).

**Tips:**
- To include weekends: `WEEKS_DISP = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]` + `week[:7]`
- For lighter display with holiday text only (no badge): remove badge rectangle and set font color to CORE_PURPLE
- Month height varies by week count (4-5 weeks). Calculate with `len(cal) * CELL_H` and verify it does not exceed BY

---

## Pattern AL — Business Model Canvas

Overview business model in 9 blocks. Implement Osterwalder BMC using pptx native rectangles.

```
┌──────────┬─────────┬────────────────┬──────────────────┬──────────────┐
│  Key     │ Key     │                │ Customer Relat.  │ Customer     │
│ Partners │ Activ.  │ Value          │                  │ Segments     │
│          ├─────────┤ Propositions   ├──────────────────┤              │
│          │ Key     │                │ Channels         │              │
│          │ Resou.  │                │                  │              │
├──────────┴─────────┴────────────────┴──────────────────┴──────────────┤
│ Cost Structure                      │ Revenue Streams                  │
└─────────────────────────────────────┴──────────────────────────────────┘
```

**9 block definitions:**

| Block | Column | Row | Width (CW ratio) | Height |
|---------|---|---|---------|------|
| Key Partners | 1 | 1-2 | 0.20 | Full upper height |
| Key Activities | 2 | 1 | 0.18 | Upper/2 |
| Key Resources | 2 | 2 | 0.18 | Upper/2 |
| Value Propositions | 3 | 1-2 | 0.22 | Full upper height |
| Customer Relationships | 4 | 1 | 0.22 | Upper/2 |
| Channels | 4 | 2 | 0.22 | Upper/2 |
| Customer Segments | 5 | 1-2 | 0.18 | Full upper height |
| Cost Structure | 1-3 | Lower row | 0.50 | 1.20 |
| Revenue Streams | 4-5 | Lower row | 0.50 | 1.20 |

```python
# ── Pattern AL — Business Model Canvas ───────────────────────────────────
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE as MSO
from pptx.enum.text import PP_ALIGN

UPPER_H = 3.60    # Upper section (7 blocks) height
LOWER_H = 1.20    # Lower section (Cost/Revenue) height
TOP_Y   = CY

# Column width definitions (ratio to CW)
# Key Partners | Key Activities+Resources | Value Props | Cust.Rel+Channels | Cust.Segments
COL_RATIOS = [0.20, 0.18, 0.22, 0.22, 0.18]
col_widths  = [CW * r for r in COL_RATIOS]
col_xs      = [ML + sum(col_widths[:i]) for i in range(len(col_widths))]

BORDER = LIGHT_GRAY

def _bmc_box(slide, x, y, w, h, title, content="", title_bold=True):
    """BMC 1 block: header title (top DARKEST_PURPLE) + body text"""
    # Outer frame
    box = slide.shapes.add_shape(MSO.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h))
    box.fill.solid(); box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = BORDER

    # Header label (purple bar)
    hdr_h = 0.36
    hdr = slide.shapes.add_shape(MSO.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(hdr_h))
    hdr.fill.solid(); hdr.fill.fore_color.rgb = DARKEST_PURPLE
    hdr.line.fill.background()
    tf = hdr.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; run = p.add_run()
    run.text = title; run.font.size = Pt(12)
    run.font.bold = title_bold; run.font.color.rgb = WHITE; run.font.name = FONT
    p.alignment = PP_ALIGN.CENTER

    # Body text
    if content:
        tb = slide.shapes.add_textbox(
            Inches(x + 0.10), Inches(y + hdr_h + 0.08),
            Inches(w - 0.20), Inches(h - hdr_h - 0.16))
        tf2 = tb.text_frame; tf2.word_wrap = True
        for line in content.split("\n"):
            p2 = tf2.add_paragraph() if tf2.paragraphs[0].text else tf2.paragraphs[0]
            if p2.text:
                p2 = tf2.add_paragraph()
            run2 = p2.add_run()
            run2.text = line; run2.font.size = Pt(14)
            run2.font.color.rgb = TEXT_BODY; run2.font.name = FONT

# ── Upper 7 blocks ───────────────────────────────────────────────────────
_bmc_box(slide, col_xs[0], TOP_Y,    col_widths[0], UPPER_H,
         "Key Partners",       "Cloud vendors\nSI partners")
_bmc_box(slide, col_xs[1], TOP_Y,    col_widths[1], UPPER_H / 2,
         "Key Activities",     "Product development\nCustomer success")
_bmc_box(slide, col_xs[1], TOP_Y + UPPER_H / 2, col_widths[1], UPPER_H / 2,
         "Key Resources",      "Development team\nData infrastructure")
_bmc_box(slide, col_xs[2], TOP_Y,    col_widths[2], UPPER_H,
         "Value Propositions", "Operational efficiency\nCost reduction")
_bmc_box(slide, col_xs[3], TOP_Y,    col_widths[3], UPPER_H / 2,
         "Customer Relationships", "Dedicated support\nCommunity")
_bmc_box(slide, col_xs[3], TOP_Y + UPPER_H / 2, col_widths[3], UPPER_H / 2,
         "Channels",           "Direct sales\nVia partners")
_bmc_box(slide, col_xs[4], TOP_Y,    col_widths[4], UPPER_H,
         "Customer Segments",  "Mid-market enterprises\nLarge enterprises")

# ── Lower 2 blocks ───────────────────────────────────────────────────────
lower_y = TOP_Y + UPPER_H
_bmc_box(slide, ML,            lower_y, CW * 0.50, LOWER_H,
         "Cost Structure",     "Personnel costs\nInfrastructure costs")
_bmc_box(slide, ML + CW * 0.50, lower_y, CW * 0.50, LOWER_H,
         "Revenue Streams",    "Subscription\nImplementation support")
```

**Tips:**
- Upper section height (`UPPER_H`) adjustable from 3.20-4.00" based on content volume
- Keeping header labels small (12pt) ensures body text space within cells
- If body text is heavy, lowering from 14pt to 12pt is acceptable (12pt treated as caption)

---

## Pattern AM — Interview Card

Present persona information (left sidebar) and Q&A list (right main area) in a structured format.

```
┌────────────────┬──────────────────────────────────────────────────────┐
│                │ Q. What is your biggest challenge right now?                             │← CORE_PURPLE 14pt bold
│   [Initial]      │ ─────────────────────────────────────────           │<- LIGHT_GRAY divider
│                │ A. Too much duplicate data entry, month-end reporting takes 3 days │← TEXT_BODY 14pt
│   Name (bold)    │                                                      │
│   Title          ├──────────────────────────────────────────────────────┤
│   Department     │ Q. What is your ideal workflow?                             │
│   X years exp    ├──────────────────────────────────────────────────────┤
│                │ Q. What are your concerns about adoption?                               │
└────────────────┴──────────────────────────────────────────────────────┘
```

| Shape | x | y | w | h | Fill | Text |
|-------|---|---|---|---|------|------|
| Left sidebar | ML | CY | 2.20 | AH | LIGHTEST_PURPLE | — |
| Left accent bar | ML | CY | 0.06 | AH | CORE_PURPLE | — |
| Avatar circle | ML+0.35 | CY+0.20 | 0.80 | 0.80 | NONE (border: CORE_PURPLE 2pt) | Initial 18pt bold CORE_PURPLE center |
| Name | ML+0.11 | CY+1.10 | 2.00 | 0.35 | NONE | 14pt bold TEXT_BODY center |
| Sub-info lines | ML+0.11 | CY+1.50 | 2.00 | vary | NONE | 12pt MID_GRAY center |
| Q label | ML+2.40 | vary | CW-2.20 | 0.40 | NONE | CORE_PURPLE 14pt bold |
| Divider | ML+2.40 | vary | CW-2.20 | 0 | — | LIGHT_GRAY 0.5pt |
| A text | ML+2.40 | vary | CW-2.20 | vary | NONE | TEXT_BODY 14pt |

```python
# ── Pattern AM — Interview Card ───────────────────────────────────────────
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE as MSO
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn as _qn
from lxml import etree

SIDEBAR_W = 2.20
CONTENT_X = ML + SIDEBAR_W + 0.20   # Right area start X
CONTENT_W = CW - SIDEBAR_W - 0.20

persona = {
    "name":    "Taro Tanaka",
    "role":    "Sales Director",
    "dept":    "Sales Division",
    "exp":     "15 years exp",
    "initial": "T",
}
qa_list = [
    ("What is your biggest challenge right now?",
     "Too much duplicate data entry, month-end reporting takes 3 days"),
    ("What is your ideal workflow?",
     "Halve data entry through automation, real-time dashboard access"),
    ("What are your concerns about adoption?",
     "User resistance and securing training time"),
]

# ── Left sidebar background ──────────────────────────────────────────────────────
sb_bg = slide.shapes.add_shape(MSO.RECTANGLE,
    Inches(ML), Inches(CY), Inches(SIDEBAR_W), Inches(AH))
sb_bg.fill.solid(); sb_bg.fill.fore_color.rgb = LIGHTEST_PURPLE
sb_bg.line.fill.background()

# Accent bar (thin CORE_PURPLE at left edge)
accent = slide.shapes.add_shape(MSO.RECTANGLE,
    Inches(ML), Inches(CY), Inches(0.06), Inches(AH))
accent.fill.solid(); accent.fill.fore_color.rgb = CORE_PURPLE
accent.line.fill.background()

# Avatar (oval to mimic circle)
av_x, av_y, av_s = ML + 0.70, CY + 0.25, 0.80
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
oval = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL,
    Inches(av_x), Inches(av_y), Inches(av_s), Inches(av_s))
oval.fill.solid(); oval.fill.fore_color.rgb = LIGHTEST_PURPLE
oval.line.color.rgb = CORE_PURPLE
# Set line width to 2pt
oval.line.width = Pt(2).pt * 12700   # EMU
tb_av = slide.shapes.add_textbox(
    Inches(av_x), Inches(av_y), Inches(av_s), Inches(av_s))
tf_av = tb_av.text_frame
p_av = tf_av.paragraphs[0]; run_av = p_av.add_run()
run_av.text = persona["initial"]
run_av.font.size = Pt(18); run_av.font.bold = True
run_av.font.color.rgb = CORE_PURPLE; run_av.font.name = FONT
p_av.alignment = PP_ALIGN.CENTER
tf_av.word_wrap = False

# Name
nm_tb = slide.shapes.add_textbox(
    Inches(ML + 0.11), Inches(CY + 1.20), Inches(SIDEBAR_W - 0.22), Inches(0.40))
tf_nm = nm_tb.text_frame
p_nm = tf_nm.paragraphs[0]; run_nm = p_nm.add_run()
run_nm.text = persona["name"]
run_nm.font.size = Pt(14); run_nm.font.bold = True
run_nm.font.color.rgb = TEXT_BODY; run_nm.font.name = FONT
p_nm.alignment = PP_ALIGN.CENTER

# Sub-info (title, department, experience)
for si, info_key in enumerate(["role", "dept", "exp"]):
    si_tb = slide.shapes.add_textbox(
        Inches(ML + 0.11), Inches(CY + 1.65 + si * 0.32),
        Inches(SIDEBAR_W - 0.22), Inches(0.30))
    tf_si = si_tb.text_frame
    p_si = tf_si.paragraphs[0]; run_si = p_si.add_run()
    run_si.text = persona[info_key]
    run_si.font.size = Pt(12); run_si.font.color.rgb = MID_GRAY
    run_si.font.name = FONT
    p_si.alignment = PP_ALIGN.CENTER

# ── Right area Q&A list ──────────────────────────────────────────────────
qa_cur_y = CY + 0.10
QA_H     = AH / len(qa_list)

for qi, (question, answer) in enumerate(qa_list):
    # Q label
    q_tb = slide.shapes.add_textbox(
        Inches(CONTENT_X), Inches(qa_cur_y),
        Inches(CONTENT_W), Inches(0.40))
    tf_q = q_tb.text_frame; tf_q.word_wrap = False
    p_q  = tf_q.paragraphs[0]; run_q = p_q.add_run()
    run_q.text = f"Q. {question}"
    run_q.font.size = Pt(14); run_q.font.bold = True
    run_q.font.color.rgb = CORE_PURPLE; run_q.font.name = FONT
    qa_cur_y += 0.40

    # Divider line
    from native_shapes import add_divider_line
    add_divider_line(slide, CONTENT_X, qa_cur_y, CONTENT_W, LIGHT_GRAY)
    qa_cur_y += 0.10

    # A text
    a_tb = slide.shapes.add_textbox(
        Inches(CONTENT_X), Inches(qa_cur_y),
        Inches(CONTENT_W), Inches(QA_H - 0.65))
    tf_a = a_tb.text_frame; tf_a.word_wrap = True
    p_a  = tf_a.paragraphs[0]; run_a = p_a.add_run()
    run_a.text = f"A. {answer}"
    run_a.font.size = Pt(14); run_a.font.color.rgb = TEXT_BODY; run_a.font.name = FONT
    qa_cur_y += QA_H - 0.55

    # Separator rectangle (divider between Q&As: light gray background band)
    if qi < len(qa_list) - 1:
        sep = slide.shapes.add_shape(MSO.RECTANGLE,
            Inches(CONTENT_X), Inches(qa_cur_y),
            Inches(CONTENT_W), Inches(0.06))
        sep.fill.solid(); sep.fill.fore_color.rgb = LIGHT_GRAY
        sep.line.fill.background()
        qa_cur_y += 0.10
```

**Sizing mode:** Auto-split with `QA_H = AH / len(qa_list)` based on Q&A count. 3-4 items is optimal.

**Tips:**
- Avatar oval is an exception to the brand rule "rounded rectangles (roundRect) forbidden". Circles (OVAL) are allowed
- Sidebar width `SIDEBAR_W` adjustable in the 2.00-2.40" range
- For long questions, set `tf_q.word_wrap = True` and increase textbox height

---

## Pattern AN — Layer Diagram (Stacked Layers)

Display each system layer in a stacked format. Left column for layer name (emphasized), right column for description text (concise) side by side.

```
┌────────────────────┬──────────────────────────────────────────────┐
│  Presentation Layer    │  UI/UX                                      │  <- CORE_PURPLE BG
├────────────────────┼──────────────────────────────────────────────┤
│  Business Logic Layer  │  API/Rules                                  │  <- DARK_PURPLE BG
├────────────────────┼──────────────────────────────────────────────┤
│  Data Access Layer     │  ORM/DB                                      │  <- Different accent color
├────────────────────┼──────────────────────────────────────────────┤
│  Infrastructure Layer  │  Cloud                                    │  <- DARKEST_PURPLE BG
└────────────────────┴──────────────────────────────────────────────┘
```

**WARNING: Brand rule note**: Image examples may use rounded rectangles, but per brand rules (Rectangles only -- no rounded corners), implement with **RECTANGLE only**.

| Shape | x | y | w | h | Fill | Text |
|-------|---|---|---|---|------|------|
| Layer label box | ML | CY + row * LAYER_H | LABEL_W=3.20 | LAYER_H | accent_color(i) | WHITE 14pt bold center |
| Description box | ML+3.30 | CY + row * LAYER_H | CW-3.30 | LAYER_H | OFF_WHITE | TEXT_BODY 14pt left |
| Connector line (optional) | ML+3.20 | center_y | 0.10 | 0.02 | LIGHT_GRAY | — |

```python
# ── Pattern AN — Layer Diagram (Stacked Layers) ─────────────────────
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE as MSO
from pptx.enum.text import PP_ALIGN

layers = [
    ("Presentation Layer", "UI/UX -- User Interface"),
    ("Business Logic Layer",   "API/Rules -- Business Logic Processing"),
    ("Data Access Layer",     "ORM/DB -- Data Persistence"),
    ("Infrastructure Layer",   "Cloud -- AWS/Azure/GCP"),
]

LABEL_W = 3.20
DESC_W  = CW - LABEL_W - 0.10
LAYER_H = AH / len(layers)

# Layer colors (top-down: light to dark)
LAYER_COLORS = [CORE_PURPLE, DARK_PURPLE, DARKEST_PURPLE, DARKEST_PURPLE]
# Note: for more than 4 layers, use accent_color(i)

for i, (name, desc) in enumerate(layers):
    ly = CY + i * LAYER_H
    fill_color = LAYER_COLORS[i] if i < len(LAYER_COLORS) else accent_color(i)

    # Label box (left, colored)
    lbl = slide.shapes.add_shape(MSO.RECTANGLE,
        Inches(ML), Inches(ly), Inches(LABEL_W), Inches(LAYER_H))
    lbl.fill.solid(); lbl.fill.fore_color.rgb = fill_color
    lbl.line.fill.background()
    tf_l = lbl.text_frame; tf_l.word_wrap = True
    p_l = tf_l.paragraphs[0]; run_l = p_l.add_run()
    run_l.text = name
    run_l.font.size = Pt(14); run_l.font.bold = True
    run_l.font.color.rgb = WHITE; run_l.font.name = FONT
    p_l.alignment = PP_ALIGN.CENTER

    # Description box (right, OFF_WHITE)
    desc_x = ML + LABEL_W + 0.10
    desc_box = slide.shapes.add_shape(MSO.RECTANGLE,
        Inches(desc_x), Inches(ly), Inches(DESC_W), Inches(LAYER_H))
    desc_box.fill.solid(); desc_box.fill.fore_color.rgb = OFF_WHITE
    desc_box.line.color.rgb = LIGHT_GRAY
    tb_d = slide.shapes.add_textbox(
        Inches(desc_x + 0.15), Inches(ly + 0.12),
        Inches(DESC_W - 0.30), Inches(LAYER_H - 0.24))
    tf_d = tb_d.text_frame; tf_d.word_wrap = True
    p_d = tf_d.paragraphs[0]; run_d = p_d.add_run()
    run_d.text = desc
    run_d.font.size = Pt(14); run_d.font.color.rgb = TEXT_BODY; run_d.font.name = FONT
```

**Sizing mode:** Auto-divide with `LAYER_H = AH / len(layers)` based on layer count. 4-6 layers is optimal for visibility.

**Tips:**
- Auto-cycling layer colors with `accent_color(i)` automatically adapts to theme changes
- To add connector dotted lines between label box (`LABEL_W` right edge): use `add_connector_arrow(..., color=LIGHT_GRAY)`
- For multi-line description text: increase `LAYER_H` or shorten text to fit in 1 line
- To explicitly show layer boundaries: set border with `desc_box.line.color.rgb = LIGHT_GRAY`

---

## Choosing a Pattern

| Situation | Pattern |
|-----------|---------|
| Explaining a concept with text | A |
| Comparing two things | B or L |
| Chapter/section break | C |
| Single bold statement | D |
| 3–4 recommendations | E |
| 4 equal-weight concepts | F |
| Data in rows/columns | G |
| Sequential steps (arrows / chevron) | P |
| Iterative / cyclical process (PDCA, continuous improvement) | H |
| Table of contents | I |
| Key numbers/KPIs (with card panels) | J |
| Three pillars/workstreams | K |
| Best practices vs. pitfalls | L |
| Charts and graphs | M |
| Team/people intro | N |
| Process with visual flow | P |
| Service/feature catalog | Q |
| Image + text explanation | R |
| Framework / evaluation matrix with row labels | S |
| Problem → solution / background → proposal | T |
| Service pillars with icons and footer message | U |
| 5–12 numbered concepts (e.g., 8 reasons, 6 principles) | V |
| 2–4 large stats for maximum visual impact (no card panels) | W |
| Phased process with grouped steps and detailed content | X |
| Project schedule / roadmap (Gantt chart) | Y |
| Capability / maturity assessment (current vs. target) | Z |
| Priority / portfolio quadrant (value vs. effort) | AA |
| MECE decomposition / logic tree / issue tree | AB |
| Layered hierarchy / prerequisite build-up (pyramid) | AC |
| Project status report with RAG indicators | AD |
| 3-circle Venn diagram (concept overlap / intersection) | AE |
| Key quote / pull quote with attribution | AF |
| Architecture diagram / system map with connectors | AG |
| Decision matrix with symbols (options x criteria) | AH |
| Evaluation scorecard with highlighted winner row | AI |
| Radar / spider chart (multi-axis, line only) | AJ |
| Calendar (3-month grid with event badges) | AK |
| Business Model Canvas (9-block BMC) | AL |
| Interview card (persona sidebar + Q&A list) | AM |
| Layer / stack diagram (system architecture layers) | AN |
