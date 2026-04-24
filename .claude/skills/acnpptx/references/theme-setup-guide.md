# theme-setup-guide.md -- Theme Selection and Configuration Detailed Guide

## Required Gate -- Complete Before Writing a Single Line of Script

- If multiple themes are available, use **AskUserQuestion** to let the user choose before writing boilerplate
- **Calling `theme_selector.py` / `select_theme()` in a script is strictly forbidden** (Tkinter dialogs cannot return results to Claude Code)
- **`load_theme` order must be respected** (`set_lang` was removed -- just call `load_theme` directly)
- **Color theme and slide master must be selected in a single question**

---

## Confirmation Procedure (5 Steps)

1. Read `*.json` files (excluding those starting with `_`) in `~/.claude/skills/acnpptx/assets/themes/` to list available themes
2. Read each theme JSON's `name`, `tokens.primary`, `tokens.background`, `template`, and `layout_notes`
3. Verify the theme's `layout_notes.content` has placeholders for breadcrumb, title, and message line. Exclude or explain to user any masters lacking these
4. **Call the AskUserQuestion tool** to let the user choose (see format below). **Even if only one theme exists, AskUserQuestion is mandatory** (e.g., "I will use ACN Slide Master. Is that OK?"). Auto-applying without confirmation is **prohibited**.

---

## AskUserQuestion Format Example

Read actual values from each theme JSON (do not copy this example verbatim):

```
Please select the theme (color + slide master) to use.
Note: Selecting a theme determines both colors and slide master simultaneously.

Accenture
   Accent: #A100FF    Background: #FFFFFF
   Master: accenture.pptx (white background -- text is BLACK)

Sample Corp
   Accent: #FF50AA    Background: #FFFFFF
   Master: sample_sha.pptx

Fiori
   Accent: #21B7C4    Background: #FFFFFF
   Master: fiori.pptx (SAP Fiori template)
```

After receiving the answer, hardcode that `name` field in `load_theme()` and then write the boilerplate.

---

## New .pptx Template Registration Procedure

1. Use **AskUserQuestion** to ask "What name should this theme have? (e.g., 'ClientXYZ')"
2. Run `master_to_theme.py` to extract color tokens:
   ```bash
   PYTHONUTF8=1 $VENV ~/.claude/skills/acnpptx/scripts/master_to_theme.py <path/to/file.pptx> "ThemeName"
   ```
3. The extraction result (color token list) is output to stdout -- confirm with user if colors seem off
4. After saving, include in AskUserQuestion choices again

**How `master_to_theme.py` works:**

| Item | Details |
|------|------|
| Scan method | Does not use `fill.fore_color.rgb` (python-pptx API) -- silently raises AttributeError on `schemeClr`, failing to pick up colors in Fiori/SAP templates |
| schemeClr resolution | `_build_theme_map` builds slot -> hex from master theme XML, applies `lumMod`/`lumOff`/`shade`/`tint` modifiers in HLS color space |
| Namespace independent | Uses `element.iter(f"{NS_A}solidFill")` for all solidFill |
| text_body/text_muted | Selects only gray tones with saturation < 0.20 -- accent colors do not contaminate |

---

## Using `layout_notes` from Theme JSON for Layout Configuration

When the theme JSON contains the following fields, always reference them at the top of the script to set constants:

| JSON Field | Example Setting |
|----------------|--------|
| `layout_indices.cover` | `LAYOUT_COVER = theme_data["layout_indices"]["cover"]` |
| `layout_indices.content` | `LAYOUT_CONTENT = theme_data["layout_indices"]["content"]` |
| `layout_notes.content.content_area_y` | `CONTENT_Y = layout_notes["content"]["content_area_y"]` (use `CY=1.50"` if undefined) |
| `layout_notes.cover.placeholders` | Check cover placeholder idx assignments before filling |
| `cover_text_color` | If `"BLACK"`, fill all placeholders with BLACK/MID_GRAY (WHITE is invisible on white-background themes) |
| `layout_notes.content.message_line_idx` | If null, use `add_message_line()`. If a number, write directly to that idx |

```python
import json as _json
_theme_path = os.path.join(_SKILL, "..", "assets", "themes", "ThemeName.json")
with open(_theme_path) as _f:
    _td = _json.load(_f)
LAYOUT_COVER   = _td["layout_indices"]["cover"]
LAYOUT_CONTENT = _td["layout_indices"]["content"]
CONTENT_Y      = _td.get("layout_notes", {}).get("content", {}).get("content_area_y", CY)
_MSG_IDX       = _td.get("layout_notes", {}).get("content", {}).get("message_line_idx")
```
