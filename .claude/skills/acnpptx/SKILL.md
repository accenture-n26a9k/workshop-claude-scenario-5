---
name: acnpptx
description: "Generates, reads, edits, restyles, and rethemes Accenture-branded PowerPoint presentations (.pptx/.ppt) using python-pptx with official brand assets (logos, Greater Than symbol, Graphik font), slide masters, and structured layouts. Use when creating slide decks, pitch decks, PowerPoint, or presentations from scratch; reading or extracting content from .pptx/.ppt files; editing existing presentations; restyling/redesigning existing decks; or changing deck themes/templates. Trigger when user mentions PowerPoint, PPT, pptx, deck, slides, presentation, restyle, redesign. Do NOT trigger for Google Slides, Keynote, or web/CSS presentations."
---

# PPTX Skill — Multi-Theme Brand Edition

Five workflows: **Read**, **Edit** (template-based), **Create** (from scratch), **Restyle** (redesign existing deck), **Retheme** (change colors/template only).

References: [color-palette.md](references/color-palette.md) | [brand-guidelines.md](references/brand-guidelines.md) | [pattern-specs.md](references/pattern-specs.md) | [pattern-selection-guide.md](references/pattern-selection-guide.md) | [chart-specs.md](references/chart-specs.md) | [api-reference.md](references/api-reference.md) | [common-mistakes.md](references/common-mistakes.md)

## Setup

```bash
$HOME/.claude/skills/.venv/Scripts/pip install python-pptx Pillow lxml "markitdown[pptx]" pywin32
```

## Font / Assets

| Font | Template |
|------|----------|
| Graphik | `assets/slide-master.pptx` |

```python
import helpers as _h
from helpers import *
```

**Logo and GT symbol are automatically provided by the slide master. Calling `add_logo()` / `add_gt_symbol()` is prohibited.**

---

## Workflow: Reading Content

```bash
$HOME/.claude/skills/.venv/Scripts/python -m markitdown presentation.pptx
```

---

## Workflow: Editing Existing Slides

See [editing-workflow.md](references/editing-workflow.md).

```
scripts/unpack.py → scripts/add_slide.py → edit XML → scripts/clean.py → scripts/pack.py
```

---

## Workflow: Modifying Existing Presentations (Restyle / Retheme)

When the user requests changes to an existing PPTX, first **call the AskUserQuestion tool** (the actual tool, not plain text) to clarify the direction. Pass this text to AskUserQuestion:

```
Which approach would you like?

1. Restyle — Overhaul layout, structure, and visuals (slide count may change)
2. Retheme — Change only colors, fonts, and master; keep the same structure
```

> **You MUST invoke the AskUserQuestion tool. Printing these options as plain text in your response is prohibited.**

Then **call the AskUserQuestion tool** again to let the user choose a theme (with color swatches). See [theme-setup-guide.md](references/theme-setup-guide.md) for details.

- **Restyle** → See [restyle-workflow.md](references/restyle-workflow.md)
- **Retheme** → Execute Step 8 (below)

---

## Workflow: Creating from Scratch

> **HARD GATE — You must complete two user confirmations via AskUserQuestion tool before writing any script:**
> 1. **Step 0b: Outline confirmation** — **Call the AskUserQuestion tool** to present options and get approval
> 2. **Step 1: Theme selection** — **Call the AskUserQuestion tool** to let the user choose a theme (never skip even if only one theme exists)
>
> **Both gates require actual AskUserQuestion tool invocations. Printing options as plain text is NOT a valid substitute.**
> **Code generation is strictly prohibited until both confirmations are complete.** Any violation requires a redo.

**FILE LOCATION RULES:** Generated scripts and output .pptx files are saved in the user's CWD. `~/.claude/skills/acnpptx/` is READ-ONLY.

### Step 0 — Outline First

```python
import sys, os
_SKILL = os.path.join(os.path.expanduser("~"), ".claude", "skills", "acnpptx", "scripts")
sys.path.insert(0, _SKILL)
from outline import generate_outline, format_outline_md, save_outline, validate_outline
outline = generate_outline(title="Title", language="en", sections=["Background","Solution","Impact","Summary"])
print(format_outline_md(outline))

valid, errors, warnings = validate_outline(outline)
if warnings:
    print("Improvements recommended:")
    for w in warnings:
        print(f"  {w}")
if not valid:
    print("Errors:")
    for e in errors:
        print(f"  {e}")

save_outline(outline, "outline.json")
```

**Pattern selection**: When assigning patterns to each slide in the outline, refer to [pattern-selection-guide.md](references/pattern-selection-guide.md). Defaulting to Pattern A is prohibited — always assign a pattern appropriate to the content purpose.

### Step 0b — Outline Confirmation + Visual Pattern Preview

**ABSOLUTE GATE — AskUserQuestion tool call required (no exceptions):**

**Immediately after** displaying the outline in Step 0, you **must call the AskUserQuestion tool** to confirm with the user.

> **CRITICAL ENFORCEMENT RULES:**
> - You MUST invoke the **AskUserQuestion tool** (the actual tool, not a text message). Printing the options as plain text in your response is **NOT a substitute** and is strictly **prohibited**.
> - If you find yourself typing the options below as regular text output instead of passing them to the AskUserQuestion tool, **STOP and use the tool instead**.
> - **Do NOT proceed to Step 1 until you have received the user's response via AskUserQuestion.**

Pass this text to the AskUserQuestion tool:
```
Would you like to proceed with this outline? Would you also like to review the slide patterns visually?

Options:
1. Review in UI (browse pattern images in the browser to select and reorder)
2. Proceed as text (this outline is OK)
3. I want to modify the outline
```

- 1 → Read [preview-workflow.md](references/preview-workflow.md) and follow the UI launch, polling, and confirmation procedure
- 2 → Proceed to Step 1 (theme selection)
- 3 → Gather modification requests and redo Step 0

See [outline-schema.md](references/outline-schema.md) for schema details.

**Slide ordering rules:**
1. Cover (always first)
2. Agenda (Pattern I) — **If present, must be placed immediately after the cover. No other slides between them**
3. Thereafter — section dividers and content slides

**Slide count rules:**
- When the user specifies "make N slides", N = **Cover + Agenda (if present) + Content slides**
- **Included in the count**: Cover, Agenda (if present), Content slides
- **Not included in the count**: Section dividers (Pattern C), Closing (Thank You)
- Section dividers receive page numbers but are not counted as substantive slides

**Section divider usage rules:**
- **No section dividers for decks of 10 slides or fewer** (use breadcrumbs to indicate sections)
- When using section dividers for 11+ slides, **all sections must have dividers**. Adding dividers for some sections but not others is prohibited
- If there is only one section (no point in dividing), dividers are not needed

**Pattern diversity rules (mandatory):**
- **Never use the same pattern consecutively.** Choose a different pattern from the previous slide
- **In principle, use each pattern only once per deck.** Reuse is permitted only when content demands it (e.g., two comparison tables in different sections)
- Perform a duplicate check on used patterns when creating the outline; replace duplicates with different patterns
- **Pattern selection priority**: Unused pattern (highest priority) > Second use with content justification (acceptable) > Third use or more (prohibited)
- For a diverse visual experience, balance text-based (A, E), shape-based (P, H, T), data-based (G, J, M, W), and grid-based (B, F, K, Q) patterns
- **Pattern A usage restriction**: Treat Pattern A as a "last resort when no other pattern fits." If the outline has 2+ Pattern A slides, refer to [pattern-selection-guide.md](references/pattern-selection-guide.md) and replace with appropriate patterns
- **Automated check via validate_outline()**: Run `validate_outline()` before saving the outline and review diversity WARNING/ERROR messages. Consecutive use, 3+ uses, and category imbalance are detected

**Content quality rules (consultant-grade requirements):**
- **Specificity**: Every slide must include proper nouns, figures, years, and monetary values. Abstract placeholders like "Point 1" or "Initiative A" are strictly prohibited
- **Information density**: Each slide's content area must contain at least 4 information elements (figures, facts, analysis, concrete examples). Slides with only 3 bullets of generic text are unacceptable
- **So What**: Each slide's message line must clearly state the "So What" — implications, conclusions, or assertions, not just a list of facts
- **Storyline**: Maintain logical connections between slides. The conclusion of one slide should serve as the premise for the next
- **Research**: Conduct sufficient research on the topic before creating content. Include specific data points, not just general knowledge

**Whitespace / layout density rules (mandatory):**
- **Content fill rate**: Fill **70% or more** of the content area (CY to BY) with content. Slides with an empty bottom half are unacceptable
- **Textbox height**: Always set textbox height to **fill the remaining available space** (e.g., `h = BY - detail_y - 0.10`). Do not shrink it to match the text volume
- **Vertical center alignment (anchor: middle)**: When text is sparse and clusters at the top of the box, set the bodyPr `anchor` to `'ctr'` to vertically center the text. **This is a mandatory setting across all patterns.** Apply it to card text, panel text, flow description text, and everything else
```python
# Correct: vertically center text
tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
tf = tb.text_frame; tf.word_wrap = True
tf._txBody.find(_qn('a:bodyPr')).set('anchor', 'ctr')  # vertical center
# add text...

# Wrong: anchor not set, text clusters at top
```
- **Line spacing (space_after) is mandatory**: For bullet lists and multi-line text, always set **`p.space_after = Pt(8)`** (guideline: 6-12pt). Default line spacing makes text appear cramped and leaves large gaps at the bottom. Increasing line spacing distributes content naturally in the vertical direction
```python
# Correct: set line spacing to distribute content vertically
for j, line in enumerate(lines):
    p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
    p.text = line; p.font.size = Pt(14)
    p.font.color.rgb = TEXT_BODY; p.font.name = FONT
    p.space_after = Pt(8)  # mandatory: increase line spacing

# Wrong: no space_after, text clusters at top
```
- **Bottom text for Chevron / Flow patterns**: Set the detail textbox height to `BY - detail_y - 0.10` and apply `space_after = Pt(8)`. Even with ~4 lines of text, line spacing spreads it vertically and reduces bottom whitespace
- **Pattern A (Title+Body) prohibition**: Do not cram text into a single textbox positioned at the top, leaving the bottom half blank. If there are 6 or fewer bullets, switch to Pattern E (Accent Bullet) or Pattern K (3-Column), or add visual elements like shapes or cards to utilize the space
- **Cards / Panels**: If internal text occupies less than 50% of an OFF_WHITE panel's height, add more content. Some whitespace is acceptable due to the panel background, but apply `space_after` to text to distribute it
- **Whitespace minimization**: For every slide, ask "Is this whitespace intentional?" If not, enlarge the content or adjust the layout
- **Cover slide**: Always loop through all placeholders and fill or clear them. Leaving hint text like "Presenter 14pt" or "Click to add text" is strictly prohibited. For unused placeholders, set `p.text = " "` (single space) — an empty string `""` may cause the layout's hint text to display

### Step 1 — Theme Selection (must be done before writing scripts)

> **ABSOLUTE GATE — AskUserQuestion tool call required (no exceptions)**:
> - Calling `theme_selector.py` / `select_theme()` inside a script is prohibited
> - **Even if there is only one theme, you MUST call the AskUserQuestion tool** (e.g., "I will use ACN Slide Master. Is that OK?")
> - **You must not determine the theme name for `load_theme()` without the user's explicit approval**
> - See [theme-setup-guide.md](references/theme-setup-guide.md) for detailed flow, AskUserQuestion format examples, and master_to_theme.py internals
>
> **CRITICAL ENFORCEMENT RULES:**
> - You MUST invoke the **AskUserQuestion tool** (the actual tool, not a text message). Printing theme options as plain text in your response is **NOT a substitute** and is strictly **prohibited**.
> - If you find yourself typing theme choices as regular text output instead of passing them to the AskUserQuestion tool, **STOP and use the tool instead**.
> - **Do NOT write any script boilerplate or code until you have received the user's theme selection via AskUserQuestion.**

Confirmation procedure (write the boilerplate only after all steps are complete):
1. List `~/.claude/skills/acnpptx/assets/themes/*.json` (excluding `_` prefixed files)
2. Read each theme's `name`, `tokens.primary`, `tokens.background`, and `layout_notes`
3. Verify that `layout_notes.content` includes breadcrumb, title, and message line placeholders
4. **Call the AskUserQuestion tool** to let the user choose both color and master as a set (confirmation is mandatory even with one theme; resolve both in a single question)
5. Once the user selects and approves a theme, write the boilerplate

> See [theme-setup-guide.md](references/theme-setup-guide.md) for theme JSON constant setup, `layout_notes` details, and `master_to_theme.py`.

#### Script boilerplate

```python
import sys, os
_SKILL = os.path.join(os.path.expanduser("~"), ".claude", "skills", "acnpptx", "scripts")
sys.path.insert(0, _SKILL)

import helpers as _h
_h.load_theme("THEME_NAME_HERE")    # theme name confirmed via AskUserQuestion
from helpers import *               # all constants and functions become available

from native_shapes import *
from charts import (add_column_chart, add_bar_chart, add_line_chart, add_pie_chart,
                    add_stacked_column_chart, add_area_chart,
                    chart_marimekko, chart_gantt, chart_stacked_bar_100)
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.oxml.ns import qn as _qn

prs = Presentation(TEMPLATE_PATH)
while len(prs.slides) > 0:
    sldId = prs.slides._sldIdLst[0]
    prs.part.drop_rel(sldId.get(_qn("r:id")))
    del prs.slides._sldIdLst[0]
```

### Step 1b — Batch Generation for Large Decks (only for 12+ content slides)

> **Design rationale**: When generating decks of 15+ slides in a single context, the quality of later slides tends to degrade compared to earlier ones (context degradation). Batch splitting allows each sub-agent to focus on a small number of slides, maintaining uniform quality. ([Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Context degradation mitigation)

**Trigger condition**: Only when the content slides in outline.json (excluding cover, section divider "C", and closing) number **12 or more**. For 11 or fewer, skip this step and generate with a single script as usual.

**Batch splitting rules:**
1. **Batch 1**: Cover + Agenda (if Pattern I exists) + first 4-5 content slides
2. **Batch 2-N**: Next 4-5 content slides each (include section divider "C" in the corresponding batch)
3. **Final batch**: Remaining content slides + Closing

**Implementation:**
```
Launch each batch in parallel using the Agent tool:
  description: "Batch N slide generation"
  prompt:
    1. Read agents/batch_generator.md in full
    2. Prepend the following input parameters to the prompt:
       ## Inputs
       - batch_number: {N}
       - boilerplate: {Script boilerplate from Step 1}
       - batch_slides: {Excerpt of relevant slide definitions from outline.json}
       - total_batches: {Total number of batches}
       - is_first_batch: {true/false}
       - is_last_batch: {true/false}
    3. Append the full text of batch_generator.md as-is
```

**Merging:**
Combine all batch functions into a single script and execute:
```python
# batch_combined.py
{common boilerplate}

{batch_1 function definitions}
{batch_2 function definitions}
...
{batch_N function definitions}

generate_batch_1(prs)
generate_batch_2(prs)
...
generate_batch_N(prs)

make_closing_slide(prs)
strip_sections(prs)
prs.save(output_path)
```

**Note**: To maintain slide index consistency across batches, each batch should directly append to `prs.slides`. Avoid hardcoding index numbers.

### Step 2 — Adding Slides

```python
LAYOUT_COVER   = 0   # follows theme JSON layout_indices.cover
LAYOUT_CONTENT = 2   # follows theme JSON layout_indices.content
LAYOUT_SECTION = 6   # if present in the template

def add_slide(layout_idx=LAYOUT_CONTENT):
    slide = prs.slides.add_slide(prs.slide_layouts[layout_idx])
    clear_placeholders(slide)   # remove unused idx=10 body placeholder
    return slide

def add_cover_slide():
    return prs.slides.add_slide(prs.slide_layouts[LAYOUT_COVER])
    # do NOT call clear_placeholders()
```

**Layout 2 placeholder structure:**

| Placeholder | idx | y (in) | Usage |
|-------------|-----|--------|-------|
| Breadcrumb  | 11  | 0.08   | `add_breadcrumb(slide, "Section > Topic")` — empty string prohibited |
| Title       | 0   | 0.42   | `add_title(slide, "Title")` — direct textbox placement prohibited |
| *(unused)*  | 10  | 0.87   | Auto-removed by `clear_placeholders()` |
| Message line| *   | 0.95*  | **Required on all content slides** (except cover and agenda) |
| Content     | --  | CY=1.50"| Positioned per pattern |

### Step 3 — Slide Content

**Required zones (content slides):**

| Zone | Notes |
|------|-------|
| Breadcrumb | `add_breadcrumb(slide, "Section > Topic")` — 12pt MID_GRAY |
| Title | `add_title(slide, "Title")` — 28pt bold BLACK |
| Message line | **Required on all content slides** (except cover and agenda). If `_MSG_IDX` is defined, write to that placeholder (explicitly set 18pt bold DARK_PURPLE). If undefined, use `add_message_line(slide, "...")`. 60 characters max, declarative tone |
| Body | Min **14pt**. Position from CONTENT_Y |
| Footer | `set_footer(slide)` — required on all content slides |

Detailed API → [api-reference.md](references/api-reference.md)

**Content density rules:**
- Each card/panel should have a title + 3-5 bullet lines. Use specific sentences with figures and proper nouns
- If whitespace exceeds 50% of the container area, add more bullets

**Short label rules:** `tf.word_wrap = False`, width = character count x 0.20" or more

**Agenda badge rules (prevent "01" vertical split):** The badge textframe must always have `tf.word_wrap = False` set, and bodyPr lIns/rIns/tIns/bIns must all be reset to `"0"`. Omitting this causes "0\n1" vertical wrapping.

**Chevron flow (Pattern P) y-coordinate / vertical balance:**
- **With detail text**: Vertically center the entire group of chevron + detail text
  ```python
  FLOW_H   = 0.80   # chevron height
  GAP      = 0.25   # gap between chevron and detail
  DETAIL_H = 3.00   # detail text area height (adjust based on content volume)
  FLOW_Y   = CY + (AH - FLOW_H - GAP - DETAIL_H) / 2   # approx 1.65"
  DETAIL_Y = FLOW_Y + FLOW_H + GAP
  ```
- **Without detail text (flow only)**: `FLOW_Y = CY + (AH - FLOW_H) / 2` (vertically centered)
- Always verify via thumbnail that shapes and detail text do not overlap

### Step 4 — Pattern Selection

> See [pattern-selection-guide.md](references/pattern-selection-guide.md) for the full pattern list and selection guidance.
> See [pattern-specs.md](references/pattern-specs.md) for ASCII layouts, shape tables, and code examples.

**Brand rules (common to all patterns):**
- Rectangles only — rounded rectangles (roundRect) prohibited
- Gradients prohibited — solid fill only
- **Alternating colors strictly prohibited** — Never assign different colors to same-type elements (table rows, cards, badges, etc.) based on index parity or order. Color changes are allowed only based on state (active / header)
- No horizontal line between lead and body / no horizontal line above table headers
- Tables and charts use `w=CW` for full width
- **Table col_widths sum must equal CW (mandatory):** When specifying `col_widths`, the total of all column widths must equal `CW` (12.50"). If the total is less than CW, the table shifts left with whitespace on the right
- **Table number column width rule (mandatory):** Columns displaying item numbers, sequential numbers, or Q-numbers must have enough width for the longest text to **fit on a single line**. Guidelines: single-digit integer -> 0.45", double-digit integer -> 0.55", "X.X" format -> 0.65", "QXX" format -> 0.65". Width shortage causing "10" to wrap as "1\n0" or "2.1" as "2.\n1" is a **critical display defect** and is strictly prohibited
- **No y-coordinate overlap between panel header/body:** For Patterns B / K etc., when placing a header and body inside a panel, maintain at least 0.10" gap between the header bottom (y+h) and body top. If the header text wraps to 2 lines, set h to 0.50" or more
- Calling `add_logo()` / `add_gt_symbol()` is prohibited (master provides them automatically)

### Image Handling

1. User specifies an explicit path -> use that path
2. An image was provided in the conversation -> use that path
3. Image files exist in CWD's `assets/` -> read the contents and select an image matching the topic
4. No image available -> substitute with native shapes

`add_image_fit(slide, img_path, x, y, max_w, max_h)` (helpers.py)

| Scenario | Pattern |
|----------|---------|
| 1 image + text | Pattern R (Split Visual) |
| 1 image is the main focus | full-width `add_picture` |
| Multiple images | 2x2 `add_picture` |

### Step 5 — Cover Slide

**Mandatory rules:**
- Use `add_cover_slide()` (using `add_slide()` is prohibited). Do not add background rectangles
- Purple background -> WHITE text. White background -> BLACK / TEXT_BODY text (WHITE is invisible)
- If `cover_text_color: "BLACK"`, fill all placeholders with BLACK / MID_GRAY
- **All placeholders must be filled** (leaving them empty = hint text is displayed)
- Check placeholder idx for each theme via `layout_notes.cover.placeholders`
- **If the title spans 2 lines, manually break at a meaningful point** (auto-wrapping may break mid-phrase). Use `tf.add_paragraph()` to add a second paragraph and match font settings:
  ```python
  ph.text_frame.clear()
  p1 = ph.text_frame.paragraphs[0]
  p1.text = "March 2026 Generative AI"   # break at a meaningful boundary
  p1.font.size = Pt(40); p1.font.bold = True; p1.font.color.rgb = WHITE; p1.font.name = FONT
  p2 = ph.text_frame.add_paragraph()
  p2.text = "Trend Report"               # second line
  p2.font.size = Pt(40); p2.font.bold = True; p2.font.color.rgb = WHITE; p2.font.name = FONT
  ```

-> See [pattern-specs.md](references/pattern-specs.md) `## Cover slide template` for code examples (purple/white background variants, ph_map patterns)

**Section divider (Pattern C):**
```python
slide = add_slide()
bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE,
    Inches(0), Inches(0), prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = DARKEST_PURPLE; bg.line.fill.background()
add_breadcrumb(slide, "Section 02")   # empty string prohibited
add_title(slide, "Section Title", size_pt=36)
set_footer(slide)
```

### Step 6 — Charts (Pattern M)

> See [chart-specs.md](references/chart-specs.md) for full code examples and parameter details for all chart types.

**Basic**: `add_column_chart`, `add_bar_chart`, `add_line_chart`, `add_pie_chart`, `add_stacked_column_chart`, `add_area_chart` — `charts.py` helpers
**Matplotlib**: `chart_marimekko`, `chart_gantt`, `chart_stacked_bar_100` — returns PNG bytes -> `BytesIO` -> `add_picture`
**Advanced**: Radar, Doughnut, Scatter, Bubble, Combination, Range Bar — use `XL_CHART_TYPE` directly

### Step 7 — Icons (Pattern Q)

```python
# Initial setup: $VENV ~/.claude/skills/acnpptx/scripts/icon_utils.py
from icon_utils import add_icon_grid, find_icons
find_icons("cloud")
add_icon_grid(slide, prs, [("cloud","Cloud"),("ai","AI")],
    x=ML, y=2.40, total_w=CW, total_h=3.80, cols=3, font_name=FONT)
```

### Step 8 — Migrating Themes on Existing PPTX (Optional)

```bash
VENV="$HOME/.claude/skills/.venv/Scripts/python.exe"
PYTHONUTF8=1 $VENV ~/.claude/skills/acnpptx/scripts/retheme.py deck.pptx <target>
PYTHONUTF8=1 $VENV ~/.claude/skills/acnpptx/scripts/retheme.py deck.pptx <target> --from fiori
PYTHONUTF8=1 $VENV ~/.claude/skills/acnpptx/scripts/retheme.py deck.pptx <target> --out deck_out.pptx
```

See [retheme-guide.md](references/retheme-guide.md) for processing details (color map construction, schemeClr resolution, placeholder migration, empty placeholder removal).

### Step 8b — Mandatory Closing Sequence

```python
make_closing_slide(prs)          # Default "Thank You", left-aligned. Change only if user specifies different text
# White background theme: make_closing_slide(prs, text_color=BLACK)
# To specify custom text: make_closing_slide(prs, "Thank you for your time")
strip_sections(prs)              # Remove PowerPoint section headers
prs.save(output_path)
```

### Step 9a — Automated Verification

```bash
VENV="$HOME/.claude/skills/.venv/Scripts/python.exe"
$VENV ~/.claude/skills/acnpptx/scripts/brand_check.py output.pptx
$VENV ~/.claude/skills/acnpptx/scripts/verify_pptx.py output.pptx
$VENV ~/.claude/skills/acnpptx/scripts/thumbnail.py output.pptx slides/
$VENV -m markitdown output.pptx   # Check for residual hint text like "Click to add title"
```

Fix all ERRORs. Review all WARNINGs. See [verify-guide.md](references/verify-guide.md) for detailed check items and visual inspection checklist.

### Step 9b — Independent Visual Evaluation (Generator-Evaluator Pattern)

> **Design rationale**: When the same agent that generated the output evaluates its own work, "self-evaluation bias" occurs ([Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)). By having an independent sub-agent with no generation context evaluate the thumbnails "fresh," this bias is eliminated.

After passing the automated checks in Step 9a, launch an evaluation-only sub-agent using the **Agent tool**:

```
Agent tool call:
  description: "Visual quality evaluation"
  prompt:
    1. Read agents/visual_evaluator.md in full
    2. Prepend the following input parameters to the prompt:
       ## Inputs
       - outline_path: {CWD}/outline.json
       - slides_dir: {CWD}/slides/
    3. Append the full text of visual_evaluator.md as-is
```

**Handling evaluation results:**
- **All slides pass**: Proceed to Step 10
- **Warnings only**: Review the content, make corrections if needed, then proceed to Step 10
- **Failures present**: Fix the flagged issues -> prs.save() -> re-generate thumbnails with thumbnail.py -> re-run brand_check + verify_pptx -> redo Step 9b sub-agent evaluation (loop until all failures are resolved)

**MANDATORY visual inspection checklist (in addition to Step 9b, verify thumbnails yourself):**
1. **Residual hint text**: Check for "Presenter 14pt", "Click to add text", "Place subtitle here", etc. (also verify with markitdown)
2. **Excessive whitespace**: Check if the bottom half of the content area is blank. For slides with noticeable whitespace, change the layout or add content
3. **Text overlap**: Check for shape-text overlap (especially Chevron details, Circular Flow arrows)
4. **Text clipping**: Check for text overflowing its box (especially KPI large numbers, table cells)
5. **Arrows / Connectors**: Verify correct source and destination (Circular Flow arrows should form a cycle)
6. **Cover**: Verify all placeholders are properly filled. Check for residual hint text in unused placeholders
7. **Pattern quality**: Verify each pattern "looks right" for its type. No empty cards, distorted panels, etc.

**Always fix issues before delivery. "Automated checks passed" alone is insufficient. Independent evaluation + visual inspection is the final gate.**

### Step 10 — Visual Review & Markup

**ABSOLUTE GATE — AskUserQuestion tool call required (no exceptions):**

**Immediately after** Step 9 is complete, you **must call the AskUserQuestion tool** for final confirmation. Declaring "done" based solely on automated check results is **prohibited**.

> **CRITICAL ENFORCEMENT RULES:**
> - You MUST invoke the **AskUserQuestion tool** (the actual tool, not a text message). Printing the review options as plain text in your response is **NOT a substitute** and is strictly **prohibited**.
> - If you find yourself typing the options below as regular text output instead of passing them to the AskUserQuestion tool, **STOP and use the tool instead**.

Pass this text to the AskUserQuestion tool:
```
Would you like to do a final review of the slides in the UI?

Options:
1. Review and markup in UI (add markup and revision notes to each slide in the browser)
2. Finish with Claude's automated checks only
3. Provide revision instructions as text
```

- 1 -> Read [review-workflow.md](references/review-workflow.md) and follow the UI launch, polling, feedback capture, and image save procedure
- 2 -> Done
- 3 -> Receive text input, make corrections, then loop back to Steps 9-10

**Revision loop (must be followed)** — Repeat until the user gives the OK. **AskUserQuestion tool call is required at the end of each loop** (plain text is NOT a substitute):

```
Loop start:
  1. Launch a revision-dedicated sub-agent using the Agent tool (context isolation)
  2. Save with prs.save()
  3. Re-generate slide images with thumbnail.py
  4. Run brand_check.py + verify_pptx.py for automated verification
  5. AskUserQuestion (mandatory):
     1. Review and markup in UI -> follow review-workflow.md procedure -> return to 1
     2. OK, finish -> exit loop
     3. Provide additional revision instructions as text -> return to 1
```

This loop ends **only when the user selects "2. OK, finish"**.

#### Revision Sub-Agent (Context Isolation)

When revisions are needed, launch a revision sub-agent using the **Agent tool**:

```
Agent tool call:
  description: "Slide revision"
  prompt:
    1. Read agents/slide_fixer.md in full
    2. Prepend the following input parameters to the prompt:
       ## Inputs
       - feedback: {specific revision details}
       - script_path: {path to the generated script}
       - output_pptx: {output file path}
       - slides_dir: {CWD}/slides/
       - annotations_dir: {CWD}/review_annotations/ (if available)
    3. Append the full text of slide_fixer.md as-is
```

**Exception**: Single-line typo fixes or simple string changes may be done directly. Use the sub-agent for "multi-location revisions," "revisions involving layout adjustments," and "revisions spanning 3+ slides."

---

## Quick References

> Read the following before generating any code:

| Reference | Content |
|-----------|---------|
| [api-reference.md](references/api-reference.md) | All function parameters and code examples |
| [color-palette.md](references/color-palette.md) | Color constant Python quick reference |
| [brand-guidelines.md](references/brand-guidelines.md) | Font size table (**13pt is prohibited.** Allowed: 12/14/18/28/36-44) |
| [common-mistakes.md](references/common-mistakes.md) | Common mistakes and prevention measures (required reading) |

**Layout constants:** `CY=1.50` / `BY=6.85` / `AH=5.35` / `ML=0.42` / `CW=12.50` / `MSG_Y=0.95`