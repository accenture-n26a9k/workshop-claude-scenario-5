# Troubleshooting

## Error: Template file not found
**Cause:** `TEMPLATE_PATH` points to a file that does not exist.
**Fix:** Verify that `assets/slide-master.pptx` exists. Alternatively, update `TEMPLATE_PATH` in `helpers.py` to the correct path.

## Warning: Layout sparse
**Cause:** Content does not use enough vertical space (verify_pptx check #7).
**Fix:** Dynamically expand card/table height: `h = AH - other_elements - gaps`. Instead of increasing font size, add charts or flow diagrams to increase density.

## Warning: Text may be clipped
**Cause:** Textbox is too small for its content (verify_pptx check #5).
**Fix:** Increase the shape height. Guideline: `min_h = lines x (font_pt / 72 x 1.4)`

## Footer/slidenum missing on content slides
**Cause:** python-pptx does not automatically inherit footer placeholders from the layout.
**Fix:** Call `set_footer(slide)` on all content slides. This clones idx=20 and idx=21 from the layout and sets the `FOOTER_TEXT` text. If the company name is wrong, update `FOOTER_TEXT` in `helpers.py`.

## PowerPoint COM ERROR_FILE_CORRUPT (0x80070570)
**Cause:** A textbox has a negative height. When a table uses nearly all available space, the height calculation for a textbox below it becomes negative.
**Fix:** Add a `max(value, 0.20)` guard to height calculations. Use fixed row heights for tables to reserve space for tips textboxes.

## Placeholder hint text remains visible
**Cause:** Template hint text such as "Click to add title" or "Click to add text" was not overwritten.
**Fix:** Detected by verify_pptx.py check #0. Replace the text of the affected shape with actual content.

## Table/chart width is too narrow
**Cause:** Content width is less than 80% of CW (12.50").
**Fix:** Set table/chart width to `w=CW` (12.50") to use the full width.