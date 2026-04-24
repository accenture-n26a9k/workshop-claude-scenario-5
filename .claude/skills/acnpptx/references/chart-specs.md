# Chart Specifications — python-pptx Native Charts

All charts use Accenture brand colors. No SVG / No Node.js required.
Import from `scripts/charts.py`.

## Quick Reference

```python
from charts import (
    add_column_chart,        # vertical bars — most common
    add_bar_chart,           # horizontal bars
    add_line_chart,          # trend lines
    add_pie_chart,           # composition
    add_stacked_column_chart,# part-to-whole
    add_area_chart,          # filled area
)
```

## Series Data Format

```python
series_data = [
    {"name": "2025 Actual", "values": [100, 120, 130, 150]},
    {"name": "2026 Forecast", "values": [110, 135, 145, 170]},
]
```

## Color Palette (auto-applied in order)

| Priority | Color | Hex | Typical use |
|----------|-------|-----|-------------|
| 1st series | CORE_PURPLE | #A100FF | Primary metric |
| 2nd series | DARKEST_PURPLE | #460073 | Comparison |
| 3rd series | DARK_PURPLE | #7500C0 | Third dimension |
| 4th series | LIGHT_PURPLE | #C2A3FF | Baseline / target |
| 5th series | BLUE | #224BFF | External reference |
| 6th series | AQUA | #05F2DB | Supplemental |
| 7th series | PINK | #FF50A0 | Alert / exception |

---

## Pattern M Layout Options

### Full-width chart (recommended)
```python
chart = add_column_chart(
    slide, title="",
    categories=cats, series_data=series,
    x=ML, y=2.30, w=CW, h=4.20,
    font_name=FONT,
)
```

### Left text + right chart
```python
# Left description
tb = slide.shapes.add_textbox(Inches(ML), Inches(2.35), Inches(3.50), Inches(4.00))
# Chart on right
chart = add_bar_chart(
    slide, title=None,
    categories=cats, series_data=series,
    x=4.20, y=2.30, w=8.60, h=4.20,
    font_name=FONT, show_legend=False,
)
```

### Chart + annotation below
```python
chart = add_line_chart(
    slide, title="Monthly Trend",
    categories=cats, series_data=series,
    x=ML, y=2.20, w=CW, h=3.60,
    font_name=FONT, show_markers=True,
)
# Source note below chart
tb = slide.shapes.add_textbox(Inches(ML), Inches(5.90), Inches(CW), Inches(0.40))
p = tb.text_frame.paragraphs[0]
p.text = "Source: Internal data as of end of Feb 2026"
p.font.size = Pt(11); p.font.color.rgb = MID_GRAY; p.font.name = FONT
```

---

## Chart Type Guide

### Column Chart
Best for: category comparisons, quarterly/yearly data

```python
add_column_chart(
    slide, title="Quarterly Revenue",
    categories=["Q1", "Q2", "Q3", "Q4"],
    series_data=[{"name": "Revenue", "values": [100, 120, 135, 150]}],
    x=ML, y=2.30, w=CW, h=4.20,
    show_data_labels=True,   # show values on bars
    font_name=FONT,
)
```

### Bar Chart
Best for: rankings, comparisons with long category names

```python
add_bar_chart(
    slide, title="Cost Reduction Rate by Department",
    categories=["Manufacturing", "Logistics", "Sales", "Administration"],
    series_data=[{"name": "Reduction Rate (%)", "values": [15, 12, 8, 5]}],
    x=ML, y=2.30, w=CW, h=4.20,
    show_data_labels=True,
    font_name=FONT,
)
```

### Line Chart
Best for: trends over time, continuous metrics

```python
add_line_chart(
    slide, title="Monthly Utilization Rate Trend",
    categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    series_data=[
        {"name": "Utilization Rate", "values": [88, 91, 87, 93, 95, 97]},
        {"name": "Target", "values": [90, 90, 90, 90, 90, 90]},
    ],
    x=ML, y=2.30, w=CW, h=4.20,
    show_markers=True,
    font_name=FONT,
)
```

### Pie Chart
Best for: composition/breakdown (max 5-6 slices, sum = 100%)

**WARNING: Always use `w=CW`.** Narrow widths (6-7") leave large whitespace on the right. Legends are auto-placed within the chart area.

```python
add_pie_chart(
    slide, title="Resource Allocation",
    labels=["Development", "Testing", "Design", "Management"],
    values=[45, 25, 20, 10],
    x=ML, y=2.20, w=CW, h=4.40,   # w=CW required — do not narrow
    show_legend=True,
    show_data_labels=True,
    font_name=FONT,
)
```

### Stacked Column
Best for: part-to-whole over time/categories

```python
add_stacked_column_chart(
    slide, title="Cost Breakdown",
    categories=["2023", "2024", "2025", "2026"],
    series_data=[
        {"name": "Personnel", "values": [500, 520, 540, 560]},
        {"name": "Equipment", "values": [200, 210, 215, 220]},
        {"name": "Other", "values": [100, 95, 90, 85]},
    ],
    x=ML, y=2.30, w=CW, h=4.20,
    percentage=False,  # True for 100% stacked
    font_name=FONT,
)
```

### Radar Chart / Spider Chart
Best for: multi-axis evaluation, skill assessment, competitive comparison (3-8 axes)
Corresponds to Multilayer Chart.pptx slide 3 "Radar Chart 2"

```python
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE

chart_data = ChartData()
chart_data.categories = ["Quality", "Cost", "Speed", "Innovation", "Customer Satisfaction"]
chart_data.add_series("Our Company", (80, 70, 60, 90, 75))
chart_data.add_series("Competitor A", (60, 80, 75, 55, 65))

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.RADAR_FILLED,   # RADAR / RADAR_FILLED / RADAR_MARKERS
    Inches(ML), Inches(2.30), Inches(CW), Inches(4.20),
    chart_data,
)
chart = chart_frame.chart
chart.has_legend = True
chart.has_title = False  # Title is expressed via the slide message line

# Series color settings
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn as _qn
SERIES_COLORS = [CORE_PURPLE, DARK_PURPLE, DARKEST_PURPLE, LIGHT_PURPLE]
for i, series in enumerate(chart.series):
    color = SERIES_COLORS[i % len(SERIES_COLORS)]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = color
    series.format.line.color.rgb = color
    # Fill transparency (used with RADAR_FILLED)
    sp_pr = series.format._element
    solid_fill = sp_pr.find('.//' + _qn('a:solidFill'))
    if solid_fill is not None:
        alpha = solid_fill.find(_qn('a:alpha'))
        if alpha is None:
            from lxml import etree
            alpha = etree.SubElement(solid_fill, _qn('a:alpha'))
        alpha.set('val', '40000')  # 40% transparency (100000 = 100%)

# Font settings
chart.plots[0].series[0].data_labels.font.size = Pt(10)
if chart.has_legend:
    chart.legend.font.size = Pt(11)
    chart.legend.font.name = FONT
```

**Chart type variants:**
| Type | OOXML constant | Use |
|------|----------------|------|
| `RADAR` | `XL_CHART_TYPE.RADAR` | Line only (no fill) |
| `RADAR_FILLED` | `XL_CHART_TYPE.RADAR_FILLED` | Transparent fill (best for multi-series comparison) |
| `RADAR_MARKERS` | `XL_CHART_TYPE.RADAR_MARKERS` | Line with markers |

---

### Doughnut Chart
Best for: Single-series composition (pie variant). Effective when overlaying a large number in the center for visual impact
Corresponds to Multilayer Chart.pptx slide 2 "Doughnut Chart"

```python
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE

chart_data = ChartData()
chart_data.categories = ["Label A", "Label B", "Label C", "Other"]
chart_data.add_series("Composition", (45, 28, 17, 10))

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.DOUGHNUT,
    Inches(ML), Inches(2.20), Inches(6.50), Inches(4.40),
    chart_data,
)
chart = chart_frame.chart
chart.has_legend = True
chart.has_title = False

# Set individual slice colors (modify each point in the series)
SLICE_COLORS = [DARKEST_PURPLE, CORE_PURPLE, LIGHT_PURPLE, LIGHTEST_PURPLE]
series = chart.series[0]
for i, point in enumerate(series.points):
    point.format.fill.solid()
    point.format.fill.fore_color.rgb = SLICE_COLORS[i % len(SLICE_COLORS)]

# Adjust doughnut hole size (default 75%)
# Set directly via XML: chart.plots[0]._element.get_or_add("c:holeSize").set("val", "60")

# Overlay a large number in the center (optional)
# Calculate the center coordinates of the doughnut and overlay a textbox
center_x = ML + (6.50 / 2) - 0.80
center_y = 2.20 + (4.40 / 2) - 0.50
tb_center = slide.shapes.add_textbox(
    Inches(center_x), Inches(center_y), Inches(1.60), Inches(1.00))
tf = tb_center.text_frame
p = tf.paragraphs[0]; p.text = "45%"
p.font.size = Pt(36); p.font.bold = True
p.font.color.rgb = DARKEST_PURPLE; p.font.name = FONT; p.alignment = PP_ALIGN.CENTER
p2 = tf.add_paragraph(); p2.text = "Label A"
p2.font.size = Pt(12); p2.font.color.rgb = MID_GRAY; p2.font.name = FONT
p2.alignment = PP_ALIGN.CENTER
```

---

### Combination Chart — Column + Line
Best for: Displaying volume (bars) and ratio/trend (line) simultaneously. Uses secondary axis
Corresponds to Multilayer Chart.pptx slide 60 "Combination Column-line Chart 1"

```python
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from lxml import etree
from pptx.oxml.ns import qn as _qn, nsmap as _nsmap

# Combination charts cannot be created directly with python-pptx high-level API
# Generate as bar chart first, then change 2nd series type to line
chart_data = ChartData()
chart_data.categories = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
chart_data.add_series("Revenue (M)", (204, 274, 900, 204, 400, 550))   # bars
chart_data.add_series("Growth Rate (%)", (5,   3,   6,   9,   10,  3)) # line (secondary axis)

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(ML), Inches(2.30), Inches(CW), Inches(4.20),
    chart_data,
)
chart = chart_frame.chart

# Bar chart color (1st series)
chart.series[0].format.fill.solid()
chart.series[0].format.fill.fore_color.rgb = DARKEST_PURPLE
chart.series[0].format.line.fill.background()

# Convert 2nd series to line chart (XML manipulation)
# Change 2nd series in plotArea from barChart to lineChart
plot_area = chart._element.find('.//' + _qn('c:plotArea'))
bar_charts = plot_area.findall(_qn('c:barChart'))
if bar_charts:
    bar_chart_el = bar_charts[0]
    ser_els = bar_chart_el.findall(_qn('c:ser'))
    if len(ser_els) >= 2:
        # Extract 2nd series from barChart and create lineChart
        ser2 = ser_els[1]
        bar_chart_el.remove(ser2)

        line_chart_xml = f'''<c:lineChart xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart">
  <c:barDir val="col"/>
  <c:grouping val="standard"/>
  <c:varyColors val="0"/>
  {etree.tostring(ser2, encoding="unicode")}
  <c:axId val="200"/>
  <c:axId val="201"/>
</c:lineChart>'''
        line_chart_el = etree.fromstring(line_chart_xml)
        plot_area.append(line_chart_el)

# 2nd series color (line)
# If ser[1] remains in bar_chart, set directly
# Here we recommend the simpler approach of overlaying a separate add_line_chart

# -- Practical alternative: overlay two charts (recommended) --------------------
# Column chart (primary axis)
from charts import add_column_chart, add_line_chart

col_chart = add_column_chart(
    slide, title="",
    categories=["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"],
    series_data=[{"name": "Revenue (M)", "values": [204, 274, 900, 204, 400, 550]}],
    x=ML, y=2.30, w=CW, h=4.20, font_name=FONT, show_data_labels=False,
)
col_chart.series[0].format.fill.solid()
col_chart.series[0].format.fill.fore_color.rgb = DARKEST_PURPLE

# Overlay line chart at the same position (transparent background, axis acts as secondary)
# Note: this is purely a visual overlay; axis scales are not auto-synchronized
# In practice, align max_scale before placement
line_chart = add_line_chart(
    slide, title="",
    categories=["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"],
    series_data=[{"name": "Growth Rate (%)", "values": [5, 3, 6, 9, 10, 3]}],
    x=ML, y=2.30, w=CW, h=4.20, font_name=FONT, show_markers=True,
)
# Make the line chart plot area transparent (so the column chart beneath shows through)
line_chart_frame = slide.shapes[-1]  # last added shape
from pptx.util import Emu
line_chart_frame.chart.plot_area.format.fill.background()
```

**Tips:**
- python-pptx has no API for directly generating combination charts, so the overlay method is most reliable
- To match axis scales: set `chart.value_axis.maximum_scale = N`
- If data labels overlap, hide one side with `series.has_data_labels = False`

---

## Scatter Chart (XY_SCATTER)
**Use**: Correlation and distribution analysis of 2 variables (Y-axis: value/impact, X-axis: difficulty/cost). See Slide 4 type.

```python
from pptx.chart.data import XyChartData
from pptx.enum.chart import XL_CHART_TYPE

chart_data = XyChartData()
series1 = chart_data.add_series("Service A")
for x, y in [(1.5, 60), (3.0, 75), (4.5, 85), (6.0, 70), (8.0, 50)]:
    series1.add_data_point(x, y)
series2 = chart_data.add_series("Service B")
for x, y in [(2.0, 40), (4.0, 55), (7.0, 65)]:
    series2.add_data_point(x, y)

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.XY_SCATTER,
    Inches(ML), Inches(2.30), Inches(CW), Inches(4.20),
    chart_data)
chart = chart_frame.chart
chart.has_legend = True
chart.value_axis.axis_title.text_frame.text   = "Y-Axis Label"
chart.category_axis.axis_title.text_frame.text = "X-Axis Label"

# Marker colors
chart.series[0].marker.format.fill.solid()
chart.series[0].marker.format.fill.fore_color.rgb = DARKEST_PURPLE
chart.series[0].marker.size = 10
chart.series[1].marker.format.fill.solid()
chart.series[1].marker.format.fill.fore_color.rgb = CORE_PURPLE
chart.series[1].marker.size = 10
```

**Tips:**
- `XY_SCATTER`: Markers only (no lines). With lines: `XY_SCATTER_LINES`, smooth: `XY_SCATTER_SMOOTH`
- Marker shape: `from pptx.enum.chart import XL_MARKER_STYLE` then `series.marker.style = XL_MARKER_STYLE.CIRCLE`
- Omitting axis labels results in no title. Requires `axis_title.has_title = True`

---

## Bubble Chart (BUBBLE)
**Use**: 3-variable visualization (X-axis, Y-axis, bubble size). Ideal for 3D portfolio analysis. See Slide 5 type.

```python
from pptx.chart.data import BubbleChartData
from pptx.enum.chart import XL_CHART_TYPE

chart_data = BubbleChartData()
series1 = chart_data.add_series("Group 1")
for x, y, size in [(2, 4, 0.5), (5, 7, 1.0), (8, 3, 0.7)]:
    series1.add_data_point(x, y, size)
series2 = chart_data.add_series("Group 2")
for x, y, size in [(3, 2, 0.3), (6, 5, 0.8), (9, 6, 0.4)]:
    series2.add_data_point(x, y, size)

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.BUBBLE,
    Inches(ML), Inches(2.30), Inches(CW), Inches(4.20),
    chart_data)
chart = chart_frame.chart
chart.series[0].format.fill.solid()
chart.series[0].format.fill.fore_color.rgb = DARKEST_PURPLE
chart.series[1].format.fill.solid()
chart.series[1].format.fill.fore_color.rgb = CORE_PURPLE
```

**Tips:**
- `size` unit is python-pptx internal scale (0.1-2.0 range is visually readable)
- Semi-transparent bubbles: add alpha XML to `series.format.fill.fore_color._xClrChange` (see Radar Chart)
- 3D bubbles: `XL_CHART_TYPE.BUBBLE_THREE_D_EFFECT` (looks heavy, not recommended)

---

## Range / Floating Bar Chart
**Use**: Visualizing start-to-end ranges (Gantt-like), data ranges (min-max). See Slide 57 type.

python-pptx has no direct Range Bar API, so use the **stacked bar with transparent offset method**.

```python
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE

categories = ["Process A", "Process B", "Process C", "Process D"]
# starts: transparent (invisible) offset / widths: visible bar width (end - start)
starts = [2, 4, 1, 5]
widths = [3, 2, 4, 2]

chart_data = ChartData()
chart_data.categories = categories
chart_data.add_series("Offset (hidden)", starts)
chart_data.add_series("Range",          widths)

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.BAR_STACKED,
    Inches(ML), Inches(2.30), Inches(CW), Inches(4.20),
    chart_data)
chart = chart_frame.chart

# Make offset series transparent
chart.series[0].format.fill.background()
chart.series[0].format.line.fill.background()
chart.series[0].has_data_labels = False

# Visible series color and labels
chart.series[1].format.fill.solid()
chart.series[1].format.fill.fore_color.rgb = DARKEST_PURPLE
chart.series[1].has_data_labels = True
chart.series[1].data_labels.font.size = Pt(11)
chart.series[1].data_labels.font.name = FONT
chart.series[1].data_labels.font.color.rgb = WHITE
```

**Tips:**
- For vertical orientation (Column): change to `XL_CHART_TYPE.COLUMN_STACKED`
- Gap adjustment: `chart.plots[0].gap_width = 100` (smaller values make bars thicker)
- Fix X-axis range: `chart.category_axis.minimum_scale = 0` and `maximum_scale = N` to lock scale

---

## Post-Chart Styling (advanced)

After calling the helper, you can fine-tune the chart object:

```python
# Access chart object
chart = add_column_chart(...)  # returns pptx Chart object

# Override series color
from pptx.dml.color import RGBColor
series = chart.series[0]
series.format.fill.solid()
series.format.fill.fore_color.rgb = RGBColor(0x46, 0x00, 0x73)

# Add data labels to specific series
series.has_data_labels = True
series.data_labels.font.size = Pt(10)
series.data_labels.font.name = FONT

# Adjust axis range
chart.value_axis.maximum_scale = 200
chart.value_axis.minimum_scale = 0

# Legend position
from pptx.enum.chart import XL_LEGEND_POSITION
chart.legend.position = XL_LEGEND_POSITION.RIGHT
```

---

## Common Mistakes

| Issue | Fix |
|-------|-----|
| Chart has wrong colors | `_apply_series_colors(chart, [custom_list])` |
| Legend overlaps chart | `chart.legend.include_in_layout = False` |
| Axis labels too small | `chart.value_axis.tick_labels.font.size = Pt(10)` |
| Pie slices wrong color | Color each `series.points[i]` individually |
| Chart has white border | `chart_frame.line.fill.background()` |
| Values not showing | `series.has_data_labels = True` |