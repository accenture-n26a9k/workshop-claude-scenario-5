#!/usr/bin/env python3
"""evaluate_visual.py - Context generation for visual evaluation sub-agent

Receives outline.json and slides/ directory,
returns a structured checklist to stdout for the evaluation sub-agent.

Usage:
    python evaluate_visual.py outline.json slides/

Design rationale:
    Follows Anthropic "Harness Design for Long-Running Apps" Generator-Evaluator pattern.
    An independent sub-agent without generation context evaluates thumbnails "fresh",
    eliminating self-evaluation bias.
"""

import json
import os
import sys
import glob


# Pattern -> expected visual characteristics mapping
PATTERN_VISUAL_EXPECTATIONS = {
    "cover": "Cover slide: Title, subtitle, date, and author all visible with no placeholder hints remaining",
    "A": "Title + body: 5 or more bullet points arranged vertically. At least 70% of the content area should be used",
    "B": "2-column comparison: Two clearly separated left/right panels, each with text or content",
    "C": "Section divider: Large title text on a dark background",
    "D": "Key message: One impactful statement displayed prominently",
    "E": "GT bullet list: 3-4 items, each prefixed with a GT symbol (>)",
    "F": "2x2 card grid: Exactly 4 cards arranged in a grid layout",
    "G": "Table: Clear row-and-column tabular format with a header row",
    "H": "Circular flow: Elements arranged in a circle with arrows indicating cyclic flow",
    "I": "Agenda: Table-of-contents list with 4-7 items and numbered badges",
    "J": "KPI metrics: 2-4 large numeric cards",
    "K": "3-column: Three equally-sized panels arranged horizontally",
    "L": "Do/Don't: Recommended vs. not-recommended paired display",
    "M": "Chart: Graph displayed (bar/line/pie/area etc.) with axis labels and legend",
    "N": "Team profile: Member information cards",
    "P": "Chevron flow: 4-6 step process flow with chevron (arrow-shaped) shapes",
    "Q": "Icon grid: 3-6 item grid with icons",
    "R": "Split visual: Left/right split layout with image and text",
    "S": "Matrix: Two-axis classification table",
    "T": "Arrow pair: 2-4 sections connected by arrows",
    "U": "3-column icons: Three columns with icons",
    "V": "Numbered card grid: 5-8 numbered cards",
    "W": "Large statistics: 1-3 large numeric displays",
    "X": "Phase steps: Sequential step chart",
    "Y": "Gantt chart / roadmap: Timeline-format display",
    "Z": "Maturity model: Progressive level display",
    "AA": "4 quadrants: 2x2 matrix classification",
    "AB": "Logic tree: Hierarchical branching structure",
    "AC": "Pyramid: Triangular hierarchical structure",
    "AD": "RAG status: Red/Amber/Green evaluation table",
    "AE": "Venn diagram: Overlapping circles",
    "AF": "Quote: Large quotation text",
    "AG": "Architecture diagram: Layered technical diagram",
    "AH": "Decision matrix: Evaluation criteria x options table",
    "AI": "Scorecard: Evaluation items with scores",
    "AJ": "Radar chart: Polygon radar display",
    "AK": "Calendar: Date-based schedule",
    "AL": "Canvas: Free-form placement layout",
    "AM": "Interview card: Interview/hearing result cards",
    "AN": "Layers: Stacked layer diagram",
}


def build_evaluation_context(outline_path: str, slides_dir: str) -> dict:
    """Generate structured context for the evaluation sub-agent."""

    with open(outline_path, encoding="utf-8") as f:
        outline = json.load(f)

    # List of slide PNGs
    pngs = sorted(glob.glob(os.path.join(slides_dir, "slide_*.png")))

    # Build per-slide expectations from the outline
    slide_expectations = []

    # Cover slide (always slide 1)
    slide_expectations.append({
        "slide_number": 1,
        "pattern": "cover",
        "title": outline.get("title", ""),
        "expected_visual": PATTERN_VISUAL_EXPECTATIONS.get("cover", ""),
    })

    # Content slides
    for i, slide in enumerate(outline.get("slides", []), start=2):
        pattern = slide.get("pattern", "unknown")
        exp = {
            "slide_number": i,
            "pattern": pattern,
            "title": slide.get("title", ""),
            "expected_visual": PATTERN_VISUAL_EXPECTATIONS.get(pattern, f"Standard layout for pattern {pattern}"),
        }
        # Pattern-specific expectations
        if pattern == "F":
            exp["detail"] = "Must have exactly 4 cards"
        elif pattern == "K":
            exp["detail"] = "Must have exactly 3 columns"
        elif pattern == "P":
            steps = slide.get("steps", [])
            exp["detail"] = f"Chevron must have {len(steps)} steps"
        elif pattern == "M":
            exp["detail"] = f"Chart type: {slide.get('chart_type', 'unknown')}"
        elif pattern == "J":
            kpis = slide.get("kpis", [])
            exp["detail"] = f"Must have {len(kpis)} KPI cards"

        slide_expectations.append(exp)

    # Closing slide (+1)
    slide_expectations.append({
        "slide_number": len(slide_expectations) + 1,
        "pattern": "closing",
        "title": "Closing",
        "expected_visual": "Closing slide: Thank You or appropriate closing text",
    })

    return {
        "deck_title": outline.get("title", ""),
        "total_slides": len(pngs),
        "total_expected": len(slide_expectations),
        "slide_images": [os.path.abspath(p) for p in pngs],
        "slide_expectations": slide_expectations,
        "evaluation_criteria": [
            "Pattern match: Does the slide visually match the pattern specified in the outline",
            "Content density: No large blank space in the lower half of the slide (at least 70% filled)",
            "Text readability: No truncated text, overlaps, or extremely small fonts",
            "Message line alignment: The subtitle/insight below the title matches the slide content",
            "Visual balance: Content is not skewed left/right or top/bottom",
            "Hint text residue: No placeholder hint text visible",
            "Cover completeness: All placeholders are filled in",
        ],
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python evaluate_visual.py <outline.json> <slides_dir>")
        sys.exit(1)

    outline_path = sys.argv[1]
    slides_dir = sys.argv[2]

    if not os.path.isfile(outline_path):
        print(f"ERROR: outline.json not found: {outline_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(slides_dir):
        print(f"ERROR: slides directory not found: {slides_dir}", file=sys.stderr)
        sys.exit(1)

    context = build_evaluation_context(outline_path, slides_dir)
    print(json.dumps(context, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()