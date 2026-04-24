#!/usr/bin/env python3
"""Export pattern_catalog.pptx slides as individual PNGs and generate catalog_map.json.

Usage:
    python export_pattern_catalog.py [--catalog PATH] [--output-dir PATH]

Requires: pywin32 (PowerPoint COM), Windows with PowerPoint installed.
"""
import argparse
import json
import os
import sys

# Slide index (1-based) -> (pattern_id, name, category)
SLIDE_MAP = {
    1:  ("_catalog_cover", "Pattern Catalog", "special"),
    2:  ("A",        "Title + Body",                    "text"),
    3:  ("B",        "Two Column",                      "grid"),
    4:  ("section",  "Section Divider",                "special"),
    5:  ("D",        "Key Message",                     "text"),
    6:  ("E",        "Bullet with Accent Mark",         "text"),
    7:  ("F",        "Card Grid 2x2",                   "grid"),
    8:  ("G",        "Table",                           "data"),
    9:  ("H",        "Circular Flow",                   "flow"),
    10: ("I",        "Agenda",                          "special"),
    11: ("J",        "KPI / Metrics",                   "data"),
    12: ("J-hero",   "Hero Stat",                       "data"),
    13: ("K",        "Three Column",                    "grid"),
    14: ("K-badge",  "Numbered Badge",                  "grid"),
    15: ("L",        "Do / Don't",                      "special"),
    16: ("M",        "Chart (Column)",                  "data"),
    17: ("M-bar",    "Bar Chart",                       "data"),
    18: ("M-line",   "Line Chart",                      "data"),
    19: ("M-pie",    "Pie Chart",                       "data"),
    20: ("M-stacked","Stacked Column",                  "data"),
    21: ("M-area",   "Area Chart",                      "data"),
    22: ("M-doughnut","Doughnut",                       "data"),
    23: ("M-combination","Combination",                 "data"),
    24: ("N",        "Team Introduction",               "special"),
    25: ("N-org",    "Org Chart",                       "special"),
    26: ("P",        "Chevron Flow",                    "flow"),
    27: ("P-labeled","Labeled-Chevron",                 "flow"),
    28: ("P-multirow","Multi-row Flow",                 "flow"),
    29: ("P-iterative","Iterative Loop",                "flow"),
    30: ("Q",        "Icon Grid",                       "grid"),
    31: ("R",        "Split Visual",                    "special"),
    32: ("S",        "Framework Matrix",                "data"),
    33: ("T",        "Two-Section with Arrow",          "flow"),
    34: ("T-3section","3-Section Cascade",              "flow"),
    35: ("U",        "Three Column + Footer",           "grid"),
    36: ("V",        "Numbered Card Grid",              "grid"),
    37: ("W",        "Open-Canvas KPI",                 "data"),
    38: ("W-grid",   "2x2 Grid KPI",                   "data"),
    39: ("X",        "Step Chart",                      "flow"),
    40: ("Y",        "Arrow Roadmap",                   "flow"),
    41: ("Z",        "Maturity Model",                  "structure"),
    42: ("AA",       "2x2 Quadrant Matrix",             "structure"),
    43: ("AB",       "Issue Tree",                      "structure"),
    44: ("AB-vertical","Vertical Tree",                 "structure"),
    45: ("AC",       "Stacked Pyramid",                 "structure"),
    46: ("AD",       "Program Status Dashboard",        "structure"),
    47: ("AE",       "Venn Diagram",                    "structure"),
    48: ("AF",       "Pull Quote",                      "text"),
    49: ("AG",       "Architecture Diagram",            "structure"),
    50: ("AH",       "Decision Matrix",                 "data"),
    51: ("AI",       "Evaluation Scorecard",            "data"),
    52: ("AJ",       "Radar Chart",                     "data"),
    53: ("AK",       "Calendar",                        "special"),
    54: ("AL",       "Business Model Canvas",           "structure"),
    55: ("AM",       "Interview Card",                  "text"),
    56: ("AN",       "Layer Diagram",                   "structure"),
    57: ("_closing", "Thank You",                       "special"),
}


def export_slides(catalog_path: str, output_dir: str, width_px: int = 1280):
    """Export each slide as PNG using PowerPoint COM."""
    import win32com.client
    import pythoncom

    pythoncom.CoInitialize()
    ppt_app = None
    prs = None
    try:
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        # Visible=True for COM stability on some Windows versions
        ppt_app.Visible = True
        ppt_app.DisplayAlerts = 0

        abs_catalog = os.path.abspath(catalog_path)
        abs_output = os.path.abspath(output_dir)
        os.makedirs(abs_output, exist_ok=True)

        prs = ppt_app.Presentations.Open(abs_catalog, ReadOnly=True, WithWindow=False)
        try:
            slide_w = prs.PageSetup.SlideWidth  # points
            slide_h = prs.PageSetup.SlideHeight
            height_px = int(width_px * slide_h / slide_w)

            catalog_map = {}

            for slide_num, (pattern_id, name, category) in SLIDE_MAP.items():
                if slide_num > prs.Slides.Count:
                    print(f"  SKIP slide {slide_num}: beyond presentation range")
                    continue

                # Skip catalog cover and closing
                if pattern_id.startswith("_"):
                    continue

                filename = f"{pattern_id}.png"
                out_path = os.path.join(abs_output, filename)

                slide = prs.Slides(slide_num)
                slide.Export(out_path, "PNG", width_px, height_px)

                catalog_map[pattern_id] = {
                    "name": name,
                    "filename": filename,
                    "category": category,
                    "slide_index": slide_num,
                }
                print(f"  Exported: {pattern_id} -> {filename}")

            # Write catalog_map.json
            map_path = os.path.join(abs_output, "catalog_map.json")
            with open(map_path, "w", encoding="utf-8") as f:
                json.dump(catalog_map, f, ensure_ascii=False, indent=2)
            print(f"\nCatalog map saved: {map_path}")
            print(f"Total patterns exported: {len(catalog_map)}")

        finally:
            if prs:
                prs.Close()
    finally:
        if ppt_app:
            ppt_app.Quit()
        pythoncom.CoUninitialize()


def main():
    parser = argparse.ArgumentParser(description="Export pattern catalog slides as PNGs")
    skill_dir = os.path.join(os.path.expanduser("~"), ".claude", "skills", "acnpptx")
    parser.add_argument("--catalog", default=os.path.join(skill_dir, "assets", "pattern_catalog.pptx"))
    parser.add_argument("--output-dir", default=os.path.join(skill_dir, "assets", "pattern_previews"))
    parser.add_argument("--width", type=int, default=1280)
    args = parser.parse_args()

    if not os.path.exists(args.catalog):
        print(f"ERROR: Catalog not found: {args.catalog}", file=sys.stderr)
        sys.exit(1)

    print(f"Exporting: {args.catalog}")
    print(f"Output: {args.output_dir}")
    export_slides(args.catalog, args.output_dir, args.width)
    print("Done.")


if __name__ == "__main__":
    main()