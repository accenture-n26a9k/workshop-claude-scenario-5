# Restyle Workflow

Transform an existing presentation into the pptx design system while preserving its content.
This is different from **Retheme** (which only changes colors and slide master while keeping layout structure intact).

## When to Use

The user has an existing `.pptx` and wants it **restyled** -- better visuals, consistent layout patterns, proper typography, restructured slides. The original deck may be plain, inconsistent, or from a different template.

**Restyle vs Retheme:**

| | Restyle | Retheme |
|---|---------|---------|
| **What changes** | Layout, structure, visual patterns, content arrangement | Colors, fonts, slide master only |
| **Content** | Preserved but may be split/merged/reorganized | Preserved as-is |
| **Slide count** | May change (split dense, merge sparse) | Same |
| **Process** | Extract -> restructure -> regenerate from scratch | Run `retheme.py` script |
| **When to use** | Deck looks outdated/inconsistent, needs redesign | Deck structure is fine, just needs brand colors |

## Steps

### 1. Extract Content

```bash
VENV="$HOME/.claude/skills/.venv/Scripts/python.exe"
$VENV -m markitdown existing.pptx
```

Read the markdown output to understand slide boundaries, headings, bullet points, data tables, and any embedded chart descriptions.

### 2. Analyze and Plan

For each original slide, note:
- **Content type**: title/cover, agenda, data table, bullet list, process flow, chart, quote, key message
- **Content volume**: how much text, how many items
- **Data**: any numbers, statistics, or data series that could become charts

### 3. Restructure (if beneficial)

Restructuring is allowed and encouraged:
- **Split** dense slides with 8+ bullet points into 2-3 focused slides
- **Merge** sparse slides that have only a heading and 1-2 bullets
- **Promote** data buried in bullets to chart slides (Pattern M)
- **Add** an agenda slide (Pattern I) if the original lacks one and has 3+ sections
- **Convert** text-heavy process descriptions into chevron flows (Pattern P) or step patterns

The goal is readability and visual impact, not 1:1 slide count preservation.

### 4. Map to Patterns

Select the best pattern (A-W from pattern-specs.md) for each slide:

| Original Content | Recommended Pattern |
|-------------------|-------------------|
| Bullet list (3-4 items) | B (Two Column) or F (Card Grid 2x2) |
| Bullet list (5+ items) | Split into multiple slides |
| Data table | G (Table) |
| Two comparisons | B (Two Column) or L (Do/Don't) |
| Process/steps | P (Chevron Flow) |
| Key takeaway | D (Key Message) |
| Quote/testimonial | A (Title + Body) with emphasis |
| Statistics/KPIs | J (KPI/Metrics) or W (Open-Canvas KPI) |
| Before/after | T (Two-Section with Arrow) |
| Services/features | Q (Icon Grid) or U (Three Column Icons) |
| Framework/matrix | S (Framework Matrix) |

### 5. Generate New Deck

Create a generation script following the standard Create workflow (Steps 0-10 from SKILL.md). Use:
- The extracted content as input text
- The mapped patterns for layout
- Native shapes and charts for data visualization
- Icons where concepts have clear visual matches

### 6. Preserve Data Integrity

Critical: all numbers, data, quotes, and attributions from the original must carry over exactly. Do not paraphrase statistics or round numbers.

If the original deck contains images:
- Extract them from the unpacked PPTX (use `unpack.py`)
- Re-embed using `add_image_fit()` or Pattern R

### 7. Mandatory Closing Sequence

```python
make_closing_slide(prs)   # or make_closing_slide(prs, "Thank You")
strip_sections(prs)
prs.save(output_path)
```

### 8. Verify

Run the standard verification pipeline (Steps 9-10 from SKILL.md):
1. `brand_check.py` -> brand compliance
2. `verify_pptx.py` -> structural QA
3. `thumbnail.py` -> visual export
4. `markitdown output.pptx` -> placeholder residual check
5. Read each thumbnail -> visual self-review checklist

Compare the restyled deck against the original to ensure no content was lost.