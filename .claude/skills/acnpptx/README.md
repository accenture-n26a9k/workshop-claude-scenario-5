# Claude Code ACN PPTX Skill

A Claude Code skill for generating consulting-quality PowerPoint slides with multi-theme support.

> **This README must be placed OUTSIDE the `acnpptx/` skill folder.**
> Skill folders may only contain `SKILL.md`, `references/`, `scripts/`, `assets/`, `agents/`, and `evals/`.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [5 Core Functions](#5-core-functions)
- [AskUserQuestion Integration](#askuserquestion-integration)
- [Design Token Import](#design-token-import-theme-registration)
- [Theme System](#theme-system)
- [Layout Patterns](#layout-patterns-38-types)
- [Directory Structure](#directory-structure)
- [Agent System](#agent-system)
- [HTML Reviewer App](#html-reviewer-app)
- [3-Stage Verification](#3-stage-verification)
- [Troubleshooting](#troubleshooting)
- [Post-Installation Notes](#post-installation-notes)

---

## Overview

Install this skill into Claude Code to enable the following capabilities:

- **Multi-theme support** -- Switch color palettes, fonts, and slide masters via JSON definitions
- **Template-based PPTX generation** -- Auto-place content while preserving slide master designs
- **5 core functions** -- Read / Edit / Create / Restyle / Retheme
- **38 layout patterns** -- Cover every common consulting slide type
- **matplotlib charts** -- column, bar, line, pie, stacked column, area + Advanced (radar, doughnut, scatter, bubble, combination, range bar)
- **AskUserQuestion interactive workflow** -- Confirm theme selection and Restyle/Retheme decisions with the user before execution
- **Design token extraction** -- Auto-extract color tokens, fonts, and layout info from existing .pptx templates into theme JSON
- **Automated quality verification + visual self-review** -- 3-stage verification: structural check + brand check + thumbnail visual inspection
- **Image embedding** -- Auto-place PNG/JPEG/WebP with aspect ratio preservation
- **Agent system (parallel generation, evaluation, fixing)** -- Split large decks into batches for parallel generation, independent agent visual evaluation, scope-limited surgical fixes
- **HTML Reviewer App** -- Browser-based slide review UI (pattern preview / markup-annotated feedback)

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.9+
- Node.js 18+ (icon embedding only)
- Microsoft PowerPoint (thumbnail output and editing workflow, Windows only)

## Installation

### 1. Dependencies

```bash
pip install python-pptx Pillow lxml "markitdown[pptx]" matplotlib pywin32
```

### 2. Place the Skill

```bash
# macOS / Linux
cp -r acnpptx ~/.claude/skills/acnpptx

# Windows (PowerShell)
Copy-Item -Recurse acnpptx "$env:USERPROFILE\.claude\skills\acnpptx"
```

### 3. Verify Installation

```bash
python -m markitdown ~/.claude/skills/acnpptx/assets/slide-master.pptx
python ~/.claude/skills/acnpptx/scripts/verify_pptx.py --help
```

---

## 5 Core Functions

### 1. Read -- Read Content from Existing PPTX

```
"Summarize the contents of this proposal.pptx"
```

Extracts text using `markitdown` and analyzes/summarizes the content.

### 2. Edit -- Partial Editing of Existing Slides

```
"Fix slide 3 in this presentation.pptx"
```

Non-destructive editing of existing slides via the `unpack.py` -> direct XML editing -> `pack.py` pipeline.

### 3. Create -- Create Slides from Scratch

```
"Create a 5-slide presentation about AI agents"
"Create a 10-slide deck with the ACN theme"
```

Outline generation -> AskUserQuestion for theme selection -> pattern assignment -> code generation -> verification loop.

### 4. Restyle -- Redesign Layout, Structure, and Visuals

```
"Restyle this slide" / "Redesign the deck"
```

| Item | Details |
|------|---------|
| Scope of changes | Layout, structure, visual patterns, content arrangement |
| Slide count | May change (dense slides are split, thin slides are merged) |
| Process | Extract via markitdown -> restructure -> pattern assignment -> regenerate from scratch |
| Use case | Deck is outdated, inconsistent, or migrating from another template |

### 5. Retheme -- Change Only Colors, Fonts, and Masters

```
"Change this slide to the Accenture theme"
```

| Item | Details |
|------|---------|
| Scope of changes | Colors, fonts, and slide master only |
| Slide count | Unchanged |
| Process | Automated conversion via the `retheme.py` script |
| Use case | Keep the structure as-is but change brand colors |

**Restyle vs Retheme determination**: When a user requests changes to an existing PPTX, the skill uses **AskUserQuestion** to confirm which option is desired before proceeding.

---

## AskUserQuestion Integration

This skill uses Claude Code's **AskUserQuestion** tool in the following situations:

| Situation | Question Content |
|-----------|-----------------|
| Theme selection | Present available themes with color swatches and let the user choose |
| Restyle / Retheme determination | When modifying an existing PPTX, confirm whether to redesign the layout (Restyle) or only change colors (Retheme) |
| Outline approval | Present the generated slide outline to the user and get confirmation before implementation |
| New theme registration | Specify the theme name and confirm the extracted colors |

---

## Design Token Import (Theme Registration)

Automatically extract design tokens (colors, fonts, layout structure) from an existing .pptx template and register them as a theme JSON.

### Steps

1. Place the slide master (.pptx) in `assets/masters/`
2. Auto-extract color tokens, fonts, and layout info using `master_to_theme.py`:
   ```bash
   PYTHONUTF8=1 python ~/.claude/skills/acnpptx/scripts/master_to_theme.py <path/to/file.pptx> "ThemeName"
   ```
3. `assets/themes/ThemeName.json` is generated -- color palette, font, and layout indices are automatically configured
4. Manually adjust the JSON as needed (e.g., fine-tuning accent colors)

### Extracted Information

| Item | Details |
|------|---------|
| `tokens` | Color tokens: primary, secondary, accent, background, text, etc. |
| `font` | Theme font name |
| `template` | Path to the slide master file |
| `layout_indices` | Layout indices for cover / content / section |
| `layout_notes` | Placeholder structure for each layout (idx, coordinates, purpose) |

---

## Theme System

Themes are defined in JSON format under `assets/themes/`. Each theme switches color palettes, fonts, and slide masters.

### Included Themes

| Theme | File | Description |
|-------|------|-------------|
| Accenture Standard | `accenture.json` | Purple-based, Greater Than symbol |
| ACN Slide Master | `acn-slide-master.json` | ACN standard slide master |
| ACN Technology Graphik | `acn-technology-graphik.json` | Graphik font support |

---

## Layout Patterns (38 types)

| Pattern | Name |
|---------|------|
| **A** | Title + Body |
| **B** | Two Column |
| **C** | Section Divider |
| **D** | Key Message |
| **E** | Bullet with GT Icon |
| **F** | Card Grid 2x2 |
| **G** | Table |
| **I** | Agenda |
| **J** | KPI / Metrics |
| **K** | 3-Column |
| **L** | Do / Don't |
| **M** | Chart (column, bar, line, pie, stacked, area, radar, doughnut, scatter, bubble, combo, range bar) |
| **N** | Team Intro / Org Chart |
| **P** | Chevron Flow |
| **Q** | Icon Grid |
| **R** | Split Visual (Image + Text) |
| **S** | Framework Matrix |
| **T** | Two-Section with Arrow |
| **U** | Three Column with Icons + Footer |
| **V** | Numbered Card Grid |
| **W** | Open-Canvas KPI |
| **X** | Step Chart |
| **H** | Circular Flow |
| **Y** | Arrow Roadmap |
| **Z** | Maturity Model |
| **AA** | 2x2 Quadrant Matrix |
| **AB** | Issue Tree / Logic Tree |
| **AC** | Stacked Pyramid |
| **AD** | Program Status Dashboard |
| **AE** | Venn Diagram |
| **AF** | Pull Quote |
| **AG** | Architecture / Connector Diagram |
| **AH** | Decision Matrix |
| **AI** | Evaluation Scorecard |
| **AJ** | Radar Chart |
| **AK** | Calendar |
| **AL** | Business Model Canvas |
| **AM** | Interview Card |
| **AN** | Layer Diagram |

---

## Directory Structure

```
acnpptx/
├── SKILL.md                          # Main skill definition
├── evals/
│   └── evals.json                   # Evaluation test cases
├── agents/                           # Sub-agent definitions
│   ├── batch_generator.md           # Batch parallel generation agent
│   ├── visual_evaluator.md          # Visual quality evaluation agent
│   └── slide_fixer.md               # Slide fixing agent
├── scripts/
│   ├── helpers.py                   # Constants, colors, layout helpers
│   ├── verify_pptx.py               # Structural quality verification
│   ├── brand_check.py               # Brand guideline verification
│   ├── charts.py                    # matplotlib chart generation
│   ├── icon_utils.py                # Icon search and placement
│   ├── master_to_theme.py           # .pptx -> theme JSON auto-extraction
│   ├── native_shapes.py             # Preset shapes (chevrons, arrows, etc.)
│   ├── outline.py                   # Outline generation and validation
│   ├── retheme.py                   # Theme migration script
│   ├── pattern_v.py                 # Pattern V implementation
│   ├── pattern_x.py                 # Pattern X implementation
│   ├── thumbnail.py                 # PowerPoint COM thumbnail output
│   ├── reviewer.html                # Browser review UI (SPA)
│   ├── reviewer_server.py           # Review UI local HTTP server
│   ├── evaluate_visual.py           # Visual evaluation context generation
│   ├── export_pattern_catalog.py    # Pattern catalog PNG export
│   ├── unpack.py                    # PPTX -> XML extraction
│   ├── add_slide.py                 # Slide duplication and addition
│   ├── clean.py                     # Orphaned media deletion
│   └── pack.py                      # XML -> PPTX repack
├── references/
│   ├── api-reference.md             # Script API reference
│   ├── brand-guidelines.md          # Brand guidelines
│   ├── chart-specs.md               # Chart specifications
│   ├── color-palette.md             # Color palette definitions
│   ├── common-mistakes.md           # Common mistakes and solutions
│   ├── editing-workflow.md          # Template editing process
│   ├── outline-schema.md            # Outline schema
│   ├── pattern-selection-guide.md   # Pattern selection guide
│   ├── pattern-specs.md             # Layout pattern specifications
│   ├── preview-workflow.md          # Preview UI workflow
│   ├── review-workflow.md           # Review UI workflow
│   ├── restyle-workflow.md          # Restyle workflow
│   ├── retheme-guide.md             # Retheme internal specifications
│   ├── theme-setup-guide.md         # Theme setup guide
│   ├── troubleshooting.md           # Troubleshooting
│   └── verify-guide.md             # Verification guide
└── assets/
    ├── slide-master.pptx            # Default slide master
    ├── icon_index.json              # Icon index
    ├── pattern_catalog.pptx         # Pattern catalog (all pattern samples)
    ├── pattern_previews/            # Pattern preview images
    ├── icons/
    │   └── Icon-library.pptx
    ├── masters/                      # Theme-specific slide masters
    │   ├── accenture.pptx
    │   ├── acn-slide-master.pptx
    │   └── acn-technology-graphik.pptx
    └── themes/                       # Theme JSON definitions
        ├── accenture.json
        ├── acn-slide-master.json
        └── acn-technology-graphik.json
```

---

## Agent System

Three sub-agents are defined in `agents/` for large-scale deck generation and quality management. They are launched in parallel via Claude Code's Agent tool, achieving quality improvement through context isolation.

| Agent | File | Role |
|-------|------|------|
| Batch Generator | `agents/batch_generator.md` | Splits large decks into batches of 4-5 slides and outputs slide generation code in parallel |
| Visual Evaluator | `agents/visual_evaluator.md` | An independent agent with no generation context evaluates thumbnails "fresh" against 7 criteria (eliminates self-evaluation bias) |
| Slide Fixer | `agents/slide_fixer.md` | Surgically fixes only the flagged slides; never touches non-target slides |

### Design Philosophy

- **Generator-Evaluator pattern**: Separates generation and evaluation into different agents to eliminate self-evaluation bias (see [Anthropic: Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps))
- **Context isolation**: Each agent operates with fresh context, reducing token consumption on the main thread
- **Parallel execution**: Batch Generator launches multiple batches simultaneously, reducing generation time for large decks

---

## HTML Reviewer App

A browser-based slide review UI (`scripts/reviewer.html` + `scripts/reviewer_server.py`) is included. It starts a local HTTP server and offers two modes.

### Preview Mode (before generation)

Visually browse and reorder pattern selections in the browser before generation.

```
Select "Review in UI" -> Browse pattern images and reorder in the browser -> Confirm
```

### Review Mode (after generation)

Annotate generated slide thumbnails with markup (rectangles, arrows, circles, text annotations) and submit fix feedback.

```
Select "Review and markup in UI" -> Annotate slides in the browser -> Submit Feedback
```

### Technical Components

| Component | Description |
|-----------|-------------|
| `reviewer_server.py` | Local HTTP server (127.0.0.1 only, token-based authentication) |
| `reviewer.html` | SPA frontend (dark theme, keyboard shortcut support) |
| API | `/api/init`, `/api/status`, `/api/state`, `/api/confirm`, `/api/shutdown` |

---

## 3-Stage Verification

| Stage | Tool | Description |
|-------|------|-------------|
| 1. Structural verification | `verify_pptx.py` | Font size, overflow, shape overlap, layout density |
| 2. Brand verification | `brand_check.py` | Color, font, and prohibited element checks based on theme definitions |
| 3. Visual inspection | `thumbnail.py` + Read | Export all slides as PNG and visually check for hint text residue, excessive whitespace, text clipping, etc. |

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Font 'Graphik' not found` | Font not installed | Change the `font` value in the theme JSON |
| `Template file not found` | Incorrect template path | Check the `template` path in the theme JSON |
| `thumbnail.py` fails | `pywin32` not installed | `pip install pywin32` (requires Windows + PowerPoint) |
| `ERROR_FILE_CORRUPT` | Negative height / Shape ID collision | Use `verify_pptx.py` to identify the problem location |

---

## Post-Installation Notes

Tips to ensure Claude Code works smoothly after installing the skill.

### Python Environment

- Works as-is if the required packages are installed on the `python` available on PATH.
- If using venv or conda, activate the environment before launching Claude Code.
- On Windows, the `PYTHONUTF8=1` environment variable is required when outputting non-ASCII text:
  ```bash
  PYTHONUTF8=1 python my_script.py
  ```

### Platform Support

| Feature | Windows | macOS / Linux |
|---------|---------|---------------|
| Create / Read / Edit / Restyle / Retheme | OK | OK |
| `thumbnail.py` (visual review) | OK (requires PowerPoint + `pywin32`) | Not available |
| `brand_check.py` / `verify_pptx.py` | OK | OK |

- `pywin32` is only needed for `thumbnail.py` (thumbnail generation). All other features are cross-platform.
- If `pywin32` is not installed, it is safe to skip the thumbnail step.

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `load_theme()` has no effect | Calling `set_lang()` afterward resets `TEMPLATE_PATH` | Call `set_lang()` BEFORE `load_theme()` |
| "File corrupt" error in PowerPoint | Negative text box height | Use `height = max(Inches(0.2), calculated_value)` |
| "File corrupt" error in PowerPoint | Shape ID collision | Use `slide.shapes._spTree.max_shape_id + 1` |
| `UnicodeEncodeError` on Windows | `PYTHONUTF8=1` not set | Set `PYTHONUTF8=1` before running scripts |

---

## License

MIT

## Author

Kyohei Doai