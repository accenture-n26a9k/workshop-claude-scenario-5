"""
PPTX Skill — Outline Schema and Generator

Before generating slides, Claude creates a JSON outline to confirm the
structure with the user. This module provides:

  1. OUTLINE_SCHEMA     — the JSON structure spec
  2. generate_outline() — create a skeleton outline from a topic + notes
  3. validate_outline() — check the outline is well-formed
  4. format_outline_md()— render the outline as readable Markdown for review
  5. save/load helpers

Usage:
    from outline import generate_outline, format_outline_md, save_outline

    outline = generate_outline(
        title="AIIS Project Overview",
        language="en",
        notes="4 chapters: Background, Solution, Results, Summary"
    )
    print(format_outline_md(outline))
    save_outline(outline, "outline.json")
"""

import json
import os
from collections import Counter

# ─────────────────────────────────────────────────────────────────────────────
# SCHEMA CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

# Valid slide patterns
VALID_PATTERNS = {
    "cover": "Cover Slide",
    "C": "Section Divider (Pattern C)",
    "section": "Section Divider (Pattern C)",
    "A": "Title + Body (Standard)",
    "B": "Two-Column Comparison",
    "D": "Key Message (Impact Statement)",
    "E": "Bullet List with GT Icons",
    "F": "Card Grid 2x2",
    "G": "Table",
    "I": "Agenda (Table of Contents)",
    "J": "KPI / Metrics",
    "K": "Three Column",
    "L": "Do / Don't Comparison",
    "M": "Chart (Column/Line/Pie)",
    "N": "Team Introduction",
    "P": "Chevron Flow",
    "Q": "Icon Grid",
    "R": "Split Visual (Image + Text)",
    "S": "Framework Matrix (Evaluation Criteria)",
    "T": "Two-Section Arrow Flow (Problem → Proposal)",
    "U": "Three Column Icons + Footer Bar",
    "V": "Numbered Card Grid",
    "W": "Open-Canvas KPI (Large Stats)",
    "X": "Phased Step Chart",
    "H": "Circular Flow (PDCA Cycle)",
    "Y": "Gantt Chart / Roadmap",
    "Z": "Maturity Model (Current vs Target)",
    "AA": "2x2 Quadrant Matrix (Priority Assessment)",
    "AB": "Logic Tree / Issue Tree",
    "AC": "Stacked Pyramid",
    "AD": "RAG Status Dashboard",
    "AE": "Venn Diagram (3-Circle)",
    "AF": "Pull Quote",
    "AG": "Architecture / Connector Diagram",
    "AH": "Decision Matrix (Rating Evaluation)",
    "AI": "Evaluation Scorecard",
    "AJ": "Radar Chart",
    "AK": "Calendar (3-Month)",
    "AL": "Business Model Canvas",
    "AM": "Interview Card",
    "AN": "Layer Diagram (System Architecture)",
}

# Pattern categories for diversity validation
PATTERN_CATEGORIES = {
    "text":      {"A", "D", "E", "AF"},
    "grid":      {"B", "F", "K", "Q", "U", "V"},
    "data":      {"G", "J", "M", "W", "S", "AH", "AI", "AJ"},
    "flow":      {"P", "H", "T", "X"},
    "structure": {"AA", "AB", "AC", "AD", "AE", "AG", "AN", "Z"},
    "special":   {"L", "N", "R", "Y", "AK", "AL", "AM"},
}

# Valid chart types for pattern M
VALID_CHART_TYPES = ["column", "bar", "line", "pie", "stacked_column", "area",
                     "radar", "doughnut", "scatter", "bubble", "combination", "range_bar"]

# ─────────────────────────────────────────────────────────────────────────────
# OUTLINE SCHEMA EXAMPLE (for reference / documentation)
# ─────────────────────────────────────────────────────────────────────────────

OUTLINE_SCHEMA = {
    "title": "Presentation Title",
    "subtitle": "Subtitle (optional)",
    "date": "2026-03",
    "author": "Presenter Name",
    "language": "ja",       # "ja" | "en"
    "slides": [
        # Cover slide
        {
            "pattern": "cover",
            "title": "Presentation Title",
            "subtitle": "Subtitle"
        },
        # Agenda
        {
            "pattern": "I",
            "title": "Agenda",
            "breadcrumb": "",
            "items": ["1. Background", "2. Solution", "3. Summary"]
        },
        # Section divider
        {
            "pattern": "section",
            "title": "Section Title",
            "subtitle": "Optional subtext"
        },
        # Standard content
        {
            "pattern": "A",
            "title": "Slide Title",
            "breadcrumb": "Section > Topic",
            "lead": "Lead text (optional)",
            "bullets": ["Point 1", "Point 2", "Point 3"]
        },
        # Two-column
        {
            "pattern": "B",
            "title": "Slide Title",
            "left": {"header": "Left Header", "bullets": ["Item 1", "Item 2"]},
            "right": {"header": "Right Header", "bullets": ["Item A", "Item B"]}
        },
        # Chart
        {
            "pattern": "M",
            "title": "Slide Title",
            "breadcrumb": "Section > Data",
            "chart_type": "column",
            "chart_title": "Chart Title",
            "categories": ["Q1", "Q2", "Q3", "Q4"],
            "series": [
                {"name": "2025", "values": [100, 120, 130, 150]},
                {"name": "2026", "values": [110, 135, 145, 170]}
            ]
        },
        # KPI
        {
            "pattern": "J",
            "title": "Slide Title",
            "kpis": [
                {"value": "82%", "label": "KPI Achievement", "detail": "+12% YoY"},
                {"value": "1.8x", "label": "Productivity Gain", "detail": "Post-AI adoption"},
            ]
        },
        # Key message
        {
            "pattern": "D",
            "title": "Slide Title",
            "message": "Key message to convey",
            "supporting": "Supporting detail text"
        }
    ]
}


# ─────────────────────────────────────────────────────────────────────────────
# GENERATE OUTLINE (skeleton from notes)
# ─────────────────────────────────────────────────────────────────────────────

def generate_outline(title, language="en", sections=None, notes="",
                     include_cover=True, include_agenda=True):
    """
    Generate a skeleton outline dict from high-level information.

    This creates a starting point for Claude to refine with actual content.
    Claude should fill in the 'bullets', 'message', 'series', etc. fields
    based on the user's actual content before generating slides.

    Args:
        title       : presentation title
        language    : "ja" | "en"
        sections    : list of section names (e.g. ["Background", "Issues", "Solution", "Summary"])
        notes       : free-form notes about the content (used as breadcrumb hints)
        include_cover : add a cover slide (default True)
        include_agenda: add an agenda slide (default True)

    Returns:
        dict conforming to OUTLINE_SCHEMA structure
    """
    if sections is None:
        sections = (
            ["Background", "Solution", "Results", "Summary"] if language == "ja"
            else ["Background", "Solution", "Results", "Summary"]
        )

    outline = {
        "title": title,
        "subtitle": "",
        "date": _today_ym(),
        "author": "",
        "language": language,
        "slides": []
    }

    # Cover
    if include_cover:
        outline["slides"].append({
            "pattern": "cover",
            "title": title,
            "subtitle": outline["date"]
        })

    # Agenda
    if include_agenda and sections:
        agenda_items = [f"{i+1}. {s}" for i, s in enumerate(sections)]
        outline["slides"].append({
            "pattern": "I",
            "title": "Agenda",
            "breadcrumb": "",
            "items": agenda_items
        })

    # Section + placeholder content slides
    for i, section in enumerate(sections):
        # Section divider
        outline["slides"].append({
            "pattern": "section",
            "title": section,
            "subtitle": ""
        })

        # Default content slide for this section
        outline["slides"].append({
            "pattern": "A",
            "title": f"{section}: Overview",
            "breadcrumb": f"{section} > Overview",
            "lead": "(Enter lead text here)",
            "bullets": [
                "(Point 1)",
                "(Point 2)",
                "(Point 3)"
            ]
        })

    return outline


def _today_ym():
    """Return current year-month string like '2026-03'."""
    import datetime
    d = datetime.date.today()
    return d.strftime("%Y-%m")


# ─────────────────────────────────────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

def validate_outline(outline):
    """
    Validate an outline dict for required fields and valid patterns.

    Returns:
        (is_valid: bool, errors: list[str], warnings: list[str])
    """
    errors = []
    warnings = []

    if not isinstance(outline, dict):
        return False, ["Outline must be a dict"], []

    if "title" not in outline:
        errors.append("Missing 'title' at top level")
    if "slides" not in outline:
        errors.append("Missing 'slides' list")
        return False, errors, warnings
    if not isinstance(outline["slides"], list):
        errors.append("'slides' must be a list")
        return False, errors, warnings

    for i, slide in enumerate(outline["slides"]):
        prefix = f"slides[{i}]"
        if "pattern" not in slide:
            errors.append(f"{prefix}: missing 'pattern'")
            continue
        pattern = slide["pattern"]
        if pattern not in VALID_PATTERNS:
            errors.append(f"{prefix}: unknown pattern '{pattern}'. "
                          f"Valid: {list(VALID_PATTERNS.keys())}")

        # Pattern-specific checks
        if pattern == "M":
            if "chart_type" not in slide:
                errors.append(f"{prefix}: pattern M requires 'chart_type'")
            elif slide["chart_type"] not in VALID_CHART_TYPES:
                errors.append(f"{prefix}: invalid chart_type '{slide['chart_type']}'")
            if "categories" not in slide or "series" not in slide:
                errors.append(f"{prefix}: pattern M requires 'categories' and 'series'")

        if pattern == "B":
            for side in ("left", "right"):
                if side not in slide:
                    errors.append(f"{prefix}: pattern B requires '{side}'")

        if pattern == "J":
            if "kpis" not in slide or not slide["kpis"]:
                errors.append(f"{prefix}: pattern J requires non-empty 'kpis' list")

        if pattern == "E":
            if "items" not in slide:
                errors.append(f"{prefix}: pattern E requires 'items' list")

        if pattern == "F":
            if "cards" not in slide:
                errors.append(f"{prefix}: pattern F requires 'cards' list")
            elif len(slide["cards"]) != 4:
                errors.append(f"{prefix}: pattern F requires exactly 4 'cards' (currently {len(slide['cards'])})")

        if pattern == "K":
            if "columns" not in slide:
                errors.append(f"{prefix}: pattern K requires 'columns' list")
            elif len(slide["columns"]) != 3:
                errors.append(f"{prefix}: pattern K requires exactly 3 'columns' (currently {len(slide['columns'])})")

        if pattern == "P":
            if "steps" not in slide:
                errors.append(f"{prefix}: pattern P requires 'steps' list")
            elif len(slide["steps"]) < 3:
                errors.append(f"{prefix}: pattern P requires at least 3 'steps' (currently {len(slide['steps'])})")

        if pattern == "D":
            if "message" not in slide:
                errors.append(f"{prefix}: pattern D requires 'message'")

        if pattern == "G":
            if "headers" not in slide:
                errors.append(f"{prefix}: pattern G requires 'headers'")
            if "rows" not in slide:
                errors.append(f"{prefix}: pattern G requires 'rows'")

        if pattern == "T":
            if "sections" not in slide:
                errors.append(f"{prefix}: pattern T requires 'sections' list")
            elif not (2 <= len(slide["sections"]) <= 4):
                errors.append(f"{prefix}: pattern T requires 2-4 'sections' (currently {len(slide['sections'])})")

    # ─── Diversity checks (content slides only) ───
    _excluded = {"cover", "section", "I"}
    content_patterns = [
        s["pattern"] for s in outline.get("slides", [])
        if "pattern" in s and s["pattern"] not in _excluded
    ]

    # Consecutive same pattern → warning
    for idx in range(1, len(content_patterns)):
        if content_patterns[idx] == content_patterns[idx - 1]:
            warnings.append(
                f"Pattern '{content_patterns[idx]}' is used consecutively "
                f"(content slides {idx} and {idx + 1})"
            )

    # Pattern frequency checks
    pattern_counts = Counter(content_patterns)
    for pat, count in pattern_counts.items():
        if count >= 3:
            errors.append(f"Pattern '{pat}' is used {count} times (maximum 2 allowed)")
        elif count == 2:
            warnings.append(f"Pattern '{pat}' is used 2 times — consider adding variation")

    # Category diversity for larger decks (10+ content slides)
    if len(content_patterns) >= 10:
        used_categories = set()
        for pat in content_patterns:
            for cat_name, cat_patterns in PATTERN_CATEGORIES.items():
                if pat in cat_patterns:
                    used_categories.add(cat_name)
                    break
        if len(used_categories) < 3:
            warnings.append(
                f"Only {len(used_categories)} visual categories are used "
                f"(3 or more recommended for decks with 10+ slides)"
            )

    return len(errors) == 0, errors, warnings


# ─────────────────────────────────────────────────────────────────────────────
# MARKDOWN RENDERING (for user review)
# ─────────────────────────────────────────────────────────────────────────────

def format_outline_md(outline):
    """
    Render an outline dict as a human-readable Markdown string.

    Used by Claude to present the outline for user review before generating slides.

    Returns:
        str: Markdown representation
    """
    lines = []

    lines.append(f"# {outline.get('title', '(Untitled)')}")
    if outline.get("subtitle"):
        lines.append(f"*{outline['subtitle']}*")
    meta = []
    if outline.get("date"):    meta.append(f"Date: {outline['date']}")
    if outline.get("author"):  meta.append(f"Author: {outline['author']}")
    if outline.get("language"): meta.append(f"Language: {outline['language']}")
    if meta:
        lines.append("  ".join(meta))
    lines.append("")

    for i, slide in enumerate(outline.get("slides", [])):
        pattern = slide.get("pattern", "?")
        title = slide.get("title", "(No title)")
        pattern_label = VALID_PATTERNS.get(pattern, pattern)

        lines.append(f"## Slide {i+1}  `[{pattern}]` {pattern_label}")
        lines.append(f"**Title**: {title}")

        if slide.get("subtitle"):
            lines.append(f"**Subtitle**: {slide['subtitle']}")
        if slide.get("breadcrumb"):
            lines.append(f"**Breadcrumb**: {slide['breadcrumb']}")
        if slide.get("lead"):
            lines.append(f"**Lead**: {slide['lead']}")
        if slide.get("message"):
            lines.append(f"**Message**: {slide['message']}")
        if slide.get("supporting"):
            lines.append(f"**Supporting**: {slide['supporting']}")

        # Bullets
        if slide.get("bullets"):
            lines.append("**Body**:")
            for b in slide["bullets"]:
                lines.append(f"  - {b}")

        # Two-column
        for side in ("left", "right"):
            if slide.get(side):
                s = slide[side]
                lines.append(f"**{side.upper()}** [{s.get('header', '')}]:")
                for b in s.get("bullets", []):
                    lines.append(f"  - {b}")

        # Agenda items
        if slide.get("items"):
            lines.append("**Items**:")
            for item in slide["items"]:
                lines.append(f"  - {item}")

        # KPIs
        if slide.get("kpis"):
            lines.append("**KPI**:")
            for kpi in slide["kpis"]:
                lines.append(f"  - **{kpi.get('value', '?')}** {kpi.get('label', '')}"
                              + (f"  _{kpi.get('detail', '')}_" if kpi.get("detail") else ""))

        # Chart
        if pattern == "M":
            lines.append(f"**Chart Type**: {slide.get('chart_type', 'column')}")
            if slide.get("chart_title"):
                lines.append(f"**Chart Title**: {slide['chart_title']}")
            if slide.get("categories"):
                lines.append(f"**Categories**: {', '.join(str(c) for c in slide['categories'])}")
            if slide.get("series"):
                for s in slide["series"]:
                    vals = ", ".join(str(v) for v in s.get("values", []))
                    lines.append(f"  - {s.get('name', '?')}: [{vals}]")

        # Steps for P (chevron flow)
        if slide.get("steps"):
            lines.append("**Steps**:")
            for step in slide["steps"]:
                label = step if isinstance(step, str) else step.get("label", "?")
                lines.append(f"  - {label}")

        lines.append("")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# FILE I/O
# ─────────────────────────────────────────────────────────────────────────────

def save_outline(outline, path):
    """Save outline dict to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(outline, f, ensure_ascii=False, indent=2)


def load_outline(path):
    """Load outline dict from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ─────────────────────────────────────────────────────────────────────────────
# CLI DEMO
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    outline = generate_outline(
        title="Project Overview",
        language="en",
        sections=["Background", "Issues", "Solution", "Results", "Summary"]
    )
    print(format_outline_md(outline))
    valid, errors, warnings = validate_outline(outline)
    print(f"\nValidation: {'OK' if valid else 'ERRORS FOUND'}")
    for e in errors:
        print(f"  ERROR: {e}")
    for w in warnings:
        print(f"  WARNING: {w}")
