# Outline Schema -- JSON Outline Format

Create a JSON outline before slide generation and confirm with the user.
Use `scripts/outline.py` for generation, validation, and Markdown conversion.

## Usage

```python
from outline import generate_outline, format_outline_md, validate_outline, save_outline

# 1. Generate outline
outline = generate_outline(
    title="AIIS Project Overview",
    sections=["Background", "Solution", "Impact", "Summary"]
)

# 2. Display as Markdown for review
print(format_outline_md(outline))

# 3. Validate (including diversity checks)
valid, errors, warnings = validate_outline(outline)

# 4. Save to file
save_outline(outline, "outline.json")
```

---

## Top-Level Fields

```json
{
  "title":    "Presentation Title",
  "subtitle": "Subtitle (optional)",
  "date":     "2026-03",
  "author":   "Author Name (optional)",
  "slides":   [ ... ]
}
```

---

## Common Slide Fields

| Field | Required | Description |
|-----------|------|------|
| `pattern` | Yes | Pattern ID ("cover", "section", "A"-"R") |
| `title` | Yes | Slide title |
| `breadcrumb` | No | Breadcrumb "Section > Topic" |

---

## Pattern-Specific Fields

### cover (Title Slide)
```json
{
  "pattern": "cover",
  "title": "Presentation Title",
  "subtitle": "March 2026"
}
```

### section (Section Divider)
```json
{
  "pattern": "section",
  "title": "Section Name",
  "subtitle": "Optional sub-text"
}
```

### A (Title + Body)
```json
{
  "pattern": "A",
  "title": "Slide Title",
  "breadcrumb": "Section > Topic",
  "lead": "Lead text (optional)",
  "bullets": ["Point 1", "Point 2", "Point 3"]
}
```

### B (Two Column)
```json
{
  "pattern": "B",
  "title": "Slide Title",
  "left":  { "header": "Left Heading", "bullets": ["Item A", "Item B"] },
  "right": { "header": "Right Heading", "bullets": ["Item C", "Item D"] }
}
```

### D (Key Message)
```json
{
  "pattern": "D",
  "title": "Slide Title (small)",
  "message": "One bold statement to convey",
  "supporting": "Supporting explanation. Details and rationale."
}
```

### E (Accent Mark Bullets)
```json
{
  "pattern": "E",
  "title": "Slide Title",
  "items": [
    { "headline": "Heading 1", "detail": "Detailed explanation text" },
    { "headline": "Heading 2", "detail": "Detailed explanation text" }
  ]
}
```

### F (Card Grid 2x2)
```json
{
  "pattern": "F",
  "title": "Slide Title",
  "cards": [
    { "title": "Card 1", "body": "Description text" },
    { "title": "Card 2", "body": "Description text" },
    { "title": "Card 3", "body": "Description text" },
    { "title": "Card 4", "body": "Description text" }
  ]
}
```

### G (Table)
```json
{
  "pattern": "G",
  "title": "Slide Title",
  "headers": ["Column 1", "Column 2", "Column 3"],
  "rows": [
    ["Data 1", "Data 2", "Data 3"],
    ["Data 4", "Data 5", "Data 6"]
  ]
}
```

### H (Timeline / Process)
```json
{
  "pattern": "H",
  "title": "Slide Title",
  "steps": [
    { "label": "Phase 1", "detail": "Description" },
    { "label": "Phase 2", "detail": "Description" },
    { "label": "Phase 3", "detail": "Description" }
  ]
}
```

### I (Agenda)
```json
{
  "pattern": "I",
  "title": "Agenda",
  "items": ["1. Background", "2. Solution", "3. Summary"],
  "active": null
}
```
`active` is the current section number (0-based) or `null`.

### J (KPI / Metrics)
```json
{
  "pattern": "J",
  "title": "Results Summary",
  "kpis": [
    { "value": "82%", "label": "KPI Achievement", "detail": "+12% YoY" },
    { "value": "1.8x", "label": "Productivity Gain", "detail": "Post-AI adoption" },
    { "value": "60 days", "label": "Lead Time Reduction", "detail": "Shortened cycle" }
  ]
}
```

### K (Three Column)
```json
{
  "pattern": "K",
  "title": "Slide Title",
  "columns": [
    { "header": "Pillar 1", "bullets": ["Point A", "Point B"] },
    { "header": "Pillar 2", "bullets": ["Point C", "Point D"] },
    { "header": "Pillar 3", "bullets": ["Point E", "Point F"] }
  ]
}
```

### L (Do / Don't)
```json
{
  "pattern": "L",
  "title": "Recommendations and Cautions",
  "do":   { "header": "Do", "bullets": ["Things to do proactively"] },
  "dont": { "header": "Don't", "bullets": ["Things to avoid"] }
}
```

### M (Chart)
```json
{
  "pattern": "M",
  "title": "Slide Title",
  "breadcrumb": "Data > Results",
  "chart_type": "column",
  "chart_title": "Chart Title (optional)",
  "categories": ["Q1", "Q2", "Q3", "Q4"],
  "series": [
    { "name": "2025", "values": [100, 120, 130, 150] },
    { "name": "2026", "values": [110, 135, 145, 170] }
  ],
  "description": "Supplementary text to display on the left (optional)"
}
```

`chart_type`: `"column"` | `"bar"` | `"line"` | `"pie"` | `"stacked_column"` | `"area"`

### N (Team Introduction)
```json
{
  "pattern": "N",
  "title": "Team Introduction",
  "members": [
    { "name": "John Smith", "title": "Project Manager", "detail": "10+ years experience", "photo": null },
    { "name": "Jane Doe", "title": "Technical Lead", "detail": "AI/ML specialist", "photo": null }
  ]
}
```

### P (Chevron Flow)
```json
{
  "pattern": "P",
  "title": "Implementation Process",
  "steps": [
    { "label": "Plan", "detail": "Requirements definition and scope setting" },
    { "label": "Design", "detail": "Architecture design" },
    { "label": "Build", "detail": "Implementation and unit testing" },
    { "label": "Test", "detail": "Integration testing and UAT" },
    { "label": "Release", "detail": "Production deployment" }
  ]
}
```

### Q (Icon Grid)
```json
{
  "pattern": "Q",
  "title": "Coverage Areas",
  "items": [
    { "keyword": "cloud", "label": "Cloud" },
    { "keyword": "ai", "label": "AI/ML" },
    { "keyword": "data", "label": "Data Analytics" },
    { "keyword": "security", "label": "Security" },
    { "keyword": "team", "label": "Org Transformation" },
    { "keyword": "chart", "label": "Performance Mgmt" }
  ],
  "cols": 3
}
```

### R (Split Visual)
```json
{
  "pattern": "R",
  "title": "Slide Title",
  "visual": null,
  "lead": "Lead text",
  "bullets": ["Point 1", "Point 2"]
}
```

### S (Framework Matrix)
```json
{
  "pattern": "S",
  "title": "Slide Title",
  "headers": ["", "Column Header A", "Column Header B"],
  "row_labels": ["Row Label 1", "Row Label 2"],
  "rows": [
    ["Issue 1 description", "Key success factor 1"],
    ["Issue 2 description", "Key success factor 2"]
  ]
}
```

### T (Two-Section + Arrow)
```json
{
  "pattern": "T",
  "title": "Slide Title",
  "sections": [
    { "label": "Background", "body": "* Background item 1\n* Background item 2" },
    { "label": "Proposal", "body": "* Proposal item 1\n* Proposal item 2" }
  ]
}
```
`sections` contains 2-4 items. 3+ items use the 3-Section Cascade variant.

### U (Three Column with Icons + Footer)
```json
{
  "pattern": "U",
  "title": "Slide Title",
  "columns": [
    { "icon": "cloud", "header": "Pillar 1", "bullets": ["Point A", "Point B"] },
    { "icon": "ai", "header": "Pillar 2", "bullets": ["Point C", "Point D"] },
    { "icon": "data", "header": "Pillar 3", "bullets": ["Point E", "Point F"] }
  ],
  "footer": "Summary text"
}
```

### V (Numbered Card Grid)
```json
{
  "pattern": "V",
  "title": "Slide Title",
  "cards": [
    { "title": "Card 1", "body": "* Description" },
    { "title": "Card 2", "body": "* Description" }
  ],
  "n_cols": 3,
  "highlight_indices": [0, 3]
}
```

### W (Large Number Statistics)
```json
{
  "pattern": "W",
  "title": "Slide Title",
  "stats": [
    { "value": "> 50%", "label": "Label", "detail": "Description", "source": "Source" }
  ]
}
```

### X (Phased Step Chart)
```json
{
  "pattern": "X",
  "title": "Slide Title",
  "phases": [
    { "label": "Phase 1", "steps": [
      { "title": "Step 1", "subtitle": "Sub", "bullets": ["Content 1"] }
    ]}
  ]
}
```

### Y (Gantt Chart)
```json
{
  "pattern": "Y",
  "title": "Slide Title",
  "months": ["Jan", "Feb", "Mar"],
  "rows": [
    { "label": "Phase 1", "is_phase": true, "bar": null },
    { "label": "  Task 1", "is_phase": false, "bar": [1, 2] }
  ]
}
```

### Z (Maturity Assessment)
```json
{
  "pattern": "Z",
  "title": "Slide Title",
  "levels": ["Basic", "Developing", "Advanced", "Leading"],
  "capabilities": [
    { "name": "Strategy", "current": 0, "target": 2 }
  ]
}
```

### AA (2x2 Matrix)
```json
{
  "pattern": "AA",
  "title": "Slide Title",
  "quadrants": ["Quick Win", "Strategic", "Avoid", "Big Bet"],
  "x_axis": "Difficulty", "y_axis": "Impact",
  "items": [
    { "num": 1, "name": "Initiative Name", "q": 0, "x_ratio": 0.35, "y_ratio": 0.30 }
  ]
}
```

### AB (Logic Tree)
```json
{
  "pattern": "AB",
  "title": "Slide Title",
  "variant": "horizontal",
  "tree": {
    "label": "Root Issue",
    "children": [
      { "label": "Factor A", "children": [{ "label": "Sub-factor" }] }
    ]
  }
}
```
`variant`: `"horizontal"` (left-to-right) or `"vertical"` (top-to-bottom)

### AC (Stacked Pyramid)
```json
{
  "pattern": "AC",
  "title": "Slide Title",
  "layers": [
    { "label": "Infrastructure", "sub": "Foundation", "fill": "darkest" },
    { "label": "Value", "sub": "Value delivery", "fill": "lightest" }
  ]
}
```
`layers` are in bottom-to-top order.

### AD (RAG Dashboard)
```json
{
  "pattern": "AD",
  "title": "Slide Title",
  "status_items": [
    { "label": "Time", "rag": "green", "comment": "Comment" }
  ],
  "issues": [
    { "issue": "Issue description", "owner": "Owner", "due": "MM/DD" }
  ]
}
```

### AE (Venn Diagram)
```json
{
  "pattern": "AE",
  "title": "Slide Title",
  "circles": ["Concept 1", "Concept 2", "Concept 3"],
  "center_label": "Intersection Label"
}
```

### AF (Pull Quote)
```json
{
  "pattern": "AF",
  "title": "Slide Title",
  "quote": "Quote text",
  "attribution": "-- Speaker Name, Title"
}
```

### AG (Architecture / Connector Diagram)
```json
{
  "pattern": "AG",
  "title": "System Architecture",
  "nodes": [
    { "id": "web", "label": "Web App", "x": 1, "y": 1, "w": 2, "h": 1 },
    { "id": "api", "label": "API Gateway", "x": 4, "y": 1, "w": 2, "h": 1 },
    { "id": "db",  "label": "Database", "x": 7, "y": 1, "w": 2, "h": 1 }
  ],
  "connectors": [
    { "from": "web", "to": "api", "label": "REST" },
    { "from": "api", "to": "db", "label": "SQL" }
  ]
}
```

### AH (Decision Matrix)
```json
{
  "pattern": "AH",
  "title": "Tool Comparison",
  "headers": ["", "Cost", "Features", "Scalability", "Support"],
  "rows": [
    { "label": "Option A", "scores": ["Excellent", "Good", "Fair", "Good"], "recommended": true },
    { "label": "Option B", "scores": ["Good", "Excellent", "Good", "Fair"], "recommended": false },
    { "label": "Option C", "scores": ["Fair", "Good", "Excellent", "Good"], "recommended": false }
  ]
}
```
Rows with `recommended: true` are highlighted with CORE_PURPLE.

### AI (Evaluation Scorecard)
```json
{
  "pattern": "AI",
  "title": "Vendor Evaluation Results",
  "headers": ["Vendor", "Technical", "Price", "Track Record", "Summary"],
  "rows": [
    { "values": ["Company A", "4.5", "3.0", "4.0", "Outstanding technical capabilities. Cost needs negotiation"], "recommended": true },
    { "values": ["Company B", "3.5", "4.5", "3.5", "Best for cost-conscious selection"], "recommended": false }
  ]
}
```
Rows with `recommended: true` are highlighted. The last column contains summary text (with arrow prefix).

### AJ (Radar Chart)
```json
{
  "pattern": "AJ",
  "title": "Skill Assessment",
  "categories": ["Strategy", "Technical", "Management", "Communication", "Leadership"],
  "series": [
    { "name": "Current", "values": [3, 4, 2, 5, 3] },
    { "name": "Target", "values": [5, 5, 4, 5, 5] }
  ]
}
```
Line-only, no fill. `values` are on a 0-5 scale.

### AK (Calendar -- 3 months)
```json
{
  "pattern": "AK",
  "title": "Q1 Event Calendar",
  "start_month": "2026-01",
  "months": 3,
  "events": [
    { "date": "2026-01-15", "label": "Kickoff", "color": "primary" },
    { "date": "2026-02-28", "label": "Mid-Review", "color": "accent" },
    { "date": "2026-03-31", "label": "Final Report", "color": "primary" }
  ],
  "holidays": ["2026-01-01", "2026-01-13", "2026-02-11", "2026-03-20"]
}
```

### AL (Business Model Canvas)
```json
{
  "pattern": "AL",
  "title": "Business Model Analysis",
  "blocks": {
    "key_partners":    ["Partner 1", "Partner 2"],
    "key_activities":  ["Activity 1", "Activity 2"],
    "key_resources":   ["Resource 1"],
    "value_propositions": ["Value Prop 1", "Value Prop 2"],
    "customer_relationships": ["Relationship 1"],
    "channels":        ["Channel 1", "Channel 2"],
    "customer_segments": ["Segment 1"],
    "cost_structure":  ["Cost 1", "Cost 2"],
    "revenue_streams": ["Revenue 1"]
  }
}
```
Standard BMC 9-block layout.

### AM (Interview Card / Persona)
```json
{
  "pattern": "AM",
  "title": "User Interview",
  "persona": {
    "name": "John Smith",
    "role": "Division Director",
    "department": "Digital Transformation",
    "photo": null
  },
  "qa": [
    { "q": "What is your current challenge?", "a": "Data utilization is siloed to individuals and cannot be leveraged for organizational decision-making" },
    { "q": "What is the ideal state?", "a": "A dashboard where all departments can check KPIs in real-time" }
  ]
}
```
Left sidebar (LIGHTEST_PURPLE) with persona info, right side with Q&A list.

### AN (Layer Diagram -- System Architecture)
```json
{
  "pattern": "AN",
  "title": "Architecture Layers",
  "layers": [
    { "label": "Presentation Layer", "detail": "React / Next.js frontend", "color": "lightest" },
    { "label": "Application Layer", "detail": "Node.js API server, auth", "color": "light" },
    { "label": "Domain Layer", "detail": "Business logic, rule engine", "color": "medium" },
    { "label": "Infrastructure Layer", "detail": "AWS, PostgreSQL, Redis", "color": "darkest" }
  ]
}
```
`layers` are in top-to-bottom order. `color`: `lightest` / `light` / `medium` / `darkest` for gradation.

---

## Validation Rules

- `pattern` must be a defined pattern ID (cover, section, A-AN. O is skipped)
- Pattern M: `chart_type`, `categories`, `series` required
- Pattern B/L: `left`/`right` or `do`/`dont` required
- Pattern D: `message` required
- Pattern E: `items` required (1 or more)
- Pattern F: `cards` must be 4
- Pattern G: `headers` and `rows` required
- Pattern J: `kpis` must be 1 or more
- Pattern K: `columns` must be 3
- Pattern P: `steps` must be 3 or more
- Pattern T: `sections` must be 2-4
- Pattern AB: `tree` must have nested structure, `variant` must be `horizontal`/`vertical`
- Pattern AC: `layers` in bottom-to-top order (3-5 items)
- Pattern AD: `rag` must be `green`/`amber`/`red`
- Pattern AH/AI: `headers` and `rows` required
- Pattern AJ: `categories` and `series` required
- Pattern AL: `blocks` required
- Pattern AN: `layers` in top-to-bottom order
- All slides: `title` required
- **Diversity check**: Same pattern 3+ times -> ERROR, consecutive same pattern -> WARNING, 2 uses -> WARNING

---

## Workflow

```
1. outline.generate_outline() to create skeleton
2. format_outline_md() to convert to Markdown -> show to user
3. User reviews and modifies content
4. validate_outline() to check
5. Create and execute PPTX generation script
```
