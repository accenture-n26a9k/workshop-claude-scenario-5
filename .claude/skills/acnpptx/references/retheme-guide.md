# retheme.py -- Theme Migration Internal Specification

## Layout Type Detection Rules

The source `slide_layout.name` is checked for keywords to estimate the type (if no keyword matches, everything defaults to "content"). The destination is determined by placeholder **type** (`placeholder_format.type`) structure, making it independent of template name or language.

| Type | Source Detection Keywords (examples) | Destination Structure Condition | Example Layouts Selected (ACN) |
|--------|--------------------------|---------------|---------------------------|
| cover | cover / title slide | CENTER_TITLE (type=3) + SUBTITLE (type=4) present | `Title: White3+Image` (idx=0) |
| section | section / divider / chapter | CENTER_TITLE present, SUBTITLE absent | `Title Master: White` (idx=6) |
| content | (none of the above match) | Staged fallback (see below) | `3_Blank - Light` (idx=2) |
| blank | blank | Falls back to content | Same as above |

### Content Layout Staged Fallback (revised 2026-03-17)

When placeholder structures differ significantly between templates (e.g., ACN -> BCG), exact matching previously failed to find an appropriate layout, falling back to layouts with many decorative elements and causing layout corruption.

Current priority order:

| Priority | Condition | Example |
|--------|------|-----|
| 1 (highest) | TITLE + BODY + footer idx=20/21 | ACN `3_Blank - Light` |
| 2 | TITLE only (no CENTER_TITLE/SUBTITLE/BODY, prefer fewest placeholders) | BCG `Title Only` |
| 3 | TITLE + BODY (no footer) | BCG `4_Title and Text` |
| 4 (last resort) | idx=1 layout (hardcoded fallback) | -- |

**Design principle**: Retheme preserves layouts as close to original as possible. Only colors, fonts, and masters change -- content placement is not disrupted. Prioritizing the cleanest canvas ("Title Only" equivalent) preserves the original slide's shape placement.

## Content Slide Placeholder Migration Policy

| Placeholder | Policy | Reason |
|------------|------|------|
| idx=0 (title) | Copy directly to destination idx=0 | Common across templates, same position |
| idx=11 (message line / breadcrumb) | Transplant as **free-floating textbox** at original coordinates | Fiori places msg line at idx=11 but ACN's idx=11 is breadcrumb (y=0.08") at a different position |
| idx=10 (body) | Transplant as free-floating textbox | Fiori body position may differ from ACN |
| Other unmatched idx | Transplant as free-floating textbox | Preserves template-specific placement |

## Processing Steps

| Step | Description |
|----------|------|
| Color map construction | Build mapping from old theme token hex -> new theme token hex (matched by token name) |
| Slide type auto-detection | Determine target layout by placeholder type. Maps correctly even across templates with different layout names |
| Slide master replacement | Use new template PPTX as base, transplanting shapes and images from old slides |
| Placeholder position preservation | Placeholders with no matching idx in the target have `p:ph` removed and are transplanted as free-floating textboxes at original coordinates |
| Empty placeholder removal | Delete placeholders with no content to prevent "Click to add text" hint text display |
| schemeClr resolution | Convert old theme schemeClr (theme slot references + lumMod/tint HLS modifiers) to actual hex before applying color replacement |
| Bulk color replacement | Replace all `srgbClr` elements across all slides according to the color_map (shape fills, text colors, line colors) |
| Image relation preservation | Carry over icon PNG `r:embed` rId to new slides |

## master_to_theme.py -- Color Extraction Internal Specification (Debug Reference)

`master_to_theme.py` extracts color tokens from a template PPTX. If colors seem wrong, refer to the following.

| Specification | Details |
|------|------|
| **Scan method** | Does not use `fill.fore_color.rgb` (python-pptx API) -- it silently raises `AttributeError` on `schemeClr`, failing to pick up any colors in Fiori/SAP templates |
| **schemeClr resolution** | `_build_theme_map` builds slot -> hex from master theme XML, applies `lumMod`/`lumOff`/`shade`/`tint` modifiers in **HLS color space** to calculate actual display colors |
| **Namespace-independent scan** | Uses `element.iter(f"{NS_A}solidFill")` for all solidFill. `element.findall(".//a:sp")` misses `p:sp` (PresentationML) namespace |
| **text_body / text_muted selection criteria** | Only selects gray tones with saturation < 0.20. Accent/warning colors in text do not contaminate body/muted tokens |

Re-run command: `PYTHONUTF8=1 $VENV ~/.claude/skills/acnpptx/scripts/master_to_theme.py <file.pptx> "ThemeName"`

## Template Preparation (Notes for New Theme Registration)

When registering external presentations (e.g., other company templates) as themes, the original file may contain content slides. retheme.py clears existing slides from the new template before transplanting content, but **the master PPTX should be a clean version without content slides**.

```python
# Clean master creation procedure
from pptx import Presentation
from pptx.oxml.ns import qn
prs = Presentation("original_template.pptx")
while len(prs.slides) > 0:
    sldId = prs.slides._sldIdLst[0]
    prs.part.drop_rel(sldId.get(qn("r:id")))
    del prs.slides._sldIdLst[0]
prs.save("template-clean.pptx")
```

The theme JSON `template` field should point to the clean version.

## ZIP Duplicate Media Entry Repair

If `Duplicate name: 'ppt/media/imageXX.png'` warning appears after running retheme.py, PowerPoint COM may fail to open the file. Use the following script to repair:

```python
import zipfile, io
src = "rethemed.pptx"
seen = set(); buf = io.BytesIO()
with zipfile.ZipFile(src, 'r') as zin, zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename not in seen:
            seen.add(item.filename)
            zout.writestr(item, zin.read(item.filename))
with open(src, 'wb') as f:
    f.write(buf.getvalue())
```

**Always verify the file opens with thumbnail.py after retheme.** If a COM error occurs, apply the repair above.

## Limitations

- Colors inside charts are not replaced (content is preserved)
- When new master background color differs significantly from old (white vs. purple), text colors may become invisible -> verify with thumbnail and fix manually
- If source theme has section divider slides with layout names lacking keywords, they are treated as "content". Fix manually or verify source layout names in advance
