# API Reference -- pptx Skill

## helpers.py

All exports can be imported with `from helpers import *`.

### Slide Setup

```python
clear_placeholders(slide)
# Removes unused idx=10 body placeholder from Layout 2 slides.
# Call immediately after add_slide(). Retains idx=0 (title) and idx=11 (breadcrumb).
```

### Required Header Functions (call in this order)

```python
add_breadcrumb(slide, "Section > Topic")
# Writes to idx=11 placeholder (y=0.08"). 12pt MID_GRAY.
# WARNING: Empty string is forbidden -- leaving it blank shows hint text.

add_title(slide, "Title", size_pt=28)
# Writes to idx=0 placeholder (y=0.42"). 28pt bold BLACK.
# WARNING: Do not place titles directly with textbox -- it causes duplicate display.

add_message_line(slide, "Slide assertion in declarative style.")
# Used when layout_notes does not define a message line placeholder idx.
# Adds a textbox at y=MSG_Y=0.95", 18pt bold DARK_PURPLE.
# If layout_notes defines an idx, write directly to that placeholder instead.

set_footer(slide)
# Required on all content slides.
```

### Layout Constants

```python
# Default values -- if layout_notes.content.content_area_y exists, use that instead
CY    = 1.50   # content area Y start
BY    = 6.85   # content area bottom
AH    = 5.35   # available height (BY - CY)
ML    = 0.42   # margin left
CW    = 12.50  # content width
MSG_Y = 0.95   # message line Y (placeholder coordinate takes priority if defined in layout_notes)
MSG_H = 0.45   # message line height
```

### Theme

```python
_h.load_theme("Accenture") # Pass the theme name (confirmed via AskUserQuestion)
# After `from helpers import *`, TEMPLATE_PATH, FONT, and all color constants are available
```

### Modern Visual Helpers

```python
accent_color(index)       # RGBColor: dark -> primary -> light cycle
accent_color_hex(index)   # "#RRGGBB" string version (for SVG / string formatting)

make_dark_divider(slide, "Section Title", "Optional subtitle")
# Section divider with DARKEST_PURPLE bg + white text. Max 2 per deck.

add_title_accent_line(slide)
# Adds a thin CORE_PURPLE line just above the content area (y = CY - 0.03).

make_closing_slide(prs, "Thank You")
# Closing slide using the cover layout. The master auto-provides bg/logo/GT.
# For white-background themes, pass text_color=BLACK.

strip_sections(prs)
# Removes PowerPoint section headers. Always call just before prs.save().
```

---

## native_shapes.py

```python
from native_shapes import *

add_arrow_right(slide, x, y, w, h, color)
add_arrow_left(slide, x, y, w, h, color)
add_arrow_down(slide, x, y, w, h, color)
add_arrow_up(slide, x, y, w, h, color)

add_connector_arrow(slide, x1, y1, x2, y2, color, width_pt=2,
                    arrow_end=True, connector_type="straight")

add_divider_line(slide, x, y, w, color)
add_accent_corner(slide, x, y, w, h, color)
add_highlight_bar(slide, x, y, w, h, bg_color, border_color)

add_chevron_flow(slide, items, x, y, total_w, h, gap,
                 fill_color, text_color, font_name, font_size_pt=14,
                 use_pentagon_first=True,
                 shape_style='chevron')
# shape_style='chevron'     -> homePlate(first) + chevron(rest). Required style.
# shape_style='box_triangle' -> rectangle + right-pointing triangle separator
# WARNING: use_pentagon_first=False is forbidden. Always use True.
# WARNING: Multi-line splitting is forbidden. Alternating directions (left-right) are not supported.
```

---

## charts.py

See [chart-specs.md](chart-specs.md) for details.

```python
from charts import add_column_chart, add_bar_chart, add_line_chart, add_pie_chart

add_column_chart(slide, title, categories, series_data, x, y, w, h, font_name,
                 show_data_labels=True, ...)
add_bar_chart(...)
add_line_chart(...)
add_pie_chart(slide, title, labels, values, x, y, w, h, font_name, ...)
add_stacked_column_chart(...)
add_area_chart(...)
# Theme palette is automatically applied by helpers.py.
```

---

## icon_utils.py

```python
from icon_utils import add_icon, add_icon_grid, find_icons

# Initial setup (once per machine)
build_icon_index()

find_icons("cloud")   # -> [(keyword, info), ...] search results
add_icon(slide, prs, keyword, x, y, size)   # Place a single icon
add_icon_grid(slide, prs, items, x, y, total_w, total_h, cols, font_name=FONT)
# items = [("cloud","Cloud"), ("ai","AI"), ...]
```

---

## outline.py

See [outline-schema.md](outline-schema.md) for schema details.

```python
from outline import generate_outline, format_outline_md, validate_outline, save_outline, load_outline

outline = generate_outline(title="Title", sections=["Background","Proposal"])
print(format_outline_md(outline))   # Markdown for user review
validate_outline(outline)           # -> (is_valid, errors)
save_outline(outline, "outline.json")
```

---

## pattern_v.py / pattern_x.py

```python
from pattern_v import add_numbered_card_grid
add_numbered_card_grid(slide, cards, x=ML, y=CY, w=CW, ...)
# cards = [{"title": "...", "body": "..."}, ...]

from pattern_x import add_step_chart
add_step_chart(slide, phases, ...)
```