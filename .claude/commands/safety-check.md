---
description: Go/no-go report on safety-path changes — runs hook tests, adversarial subset, and inspects the diff for any drift in the load-bearing invariants. Use before merging anything that touches src/hooks/, src/specialists/safety_coc/, SAFETY_KEYWORDS, or escalation_rules.yaml.
---

Produce a go/no-go safety report for the current branch. This is the last-line check before a change that touches safety paths is merged. The `safety-brake-invariants` skill has the full rule set — this command mechanically verifies the subset that can be verified.

Steps:

1. **Scope the diff.** `git diff main...HEAD --name-only` (or the appropriate base branch). Flag any touched files that match:
   - `src/hooks/pre_tool_use.py`
   - `src/specialists/safety_coc/**`
   - `src/specialists/_base.py` (hook registration lives here)
   - `escalation_rules.yaml`
   - `tests/test_hooks.py`, `tests/test_adversarial.py`
   - Anything referencing `SAFETY_KEYWORDS`

   If none matched, report "no safety-path changes detected" and exit with a green status — no need to run the rest.

2. **Static invariant checks.** Run each and record pass/fail:

   ```bash
   # Hook stays deterministic (expect: no hits)
   grep -nE 'anthropic|client\.messages|AnthropicBedrock|model\.|await ' src/hooks/pre_tool_use.py

   # safety_coc tool count (expect: 2)
   grep -cE '^(def |@tool|TOOL)' src/specialists/safety_coc/tools.py

   # No public-write references in safety_coc
   grep -nE 'send_reply|create_ops_ticket|notify_concierge|channel|webhook|slack' src/specialists/safety_coc/

   # SAFETY_KEYWORDS is still a list of strings (no regex, no function)
   grep -nE 'SAFETY_KEYWORDS\s*=' src/hooks/pre_tool_use.py
   ```

   For each check, report the expected outcome and the actual outcome side by side.

3. **Run the hook tests.** These are the 100%-pass gate.

   ```bash
   pytest tests/test_hooks.py -v
   ```

   Any failure is a stop. Report which cases failed and the diff line they most likely implicate (from step 1).

4. **Run the adversarial subset.** The ≥95% pass bar has to hold.

   ```bash
   pytest tests/test_adversarial.py -v
   ```

   If pass rate drops below 95%, do not recommend merge. Do not suggest lowering the threshold.

5. **Run the eval harness on safety + CoC only.** Precision must be 100% on both.

   ```bash
   python eval/harness.py --output eval/scorecard.json
   ```

   Then read `eval/scorecard.json` and check:
   - `by_category.SAFETY.precision == 1.0`
   - `by_category.COC.precision == 1.0`

   Either dropping below 1.0 is a stop.

6. **Escalation-rules sanity check.** If `escalation_rules.yaml` was modified:
   - Parse it and confirm the `SAFETY` and `PRESS` rules still have `threshold: null` (always fire).
   - Confirm no rule was deleted — only amended or added.
   - If Legal needs to sign off (any change to the YAML does), surface that in the report.

7. **Produce the final report.** Keep it compact. Format:

   ```
   SAFETY CHECK — <branch>

   Touched safety-path files: <N>
     - <file1>
     - <file2>

   Static invariants:     ✅ all pass  |  ❌ <list violations>
   Hook tests:            ✅ N/N pass  |  ❌ M/N pass
   Adversarial subset:    ✅ X% pass   |  ❌ X% pass (<below 95% threshold>)
   Safety precision:      ✅ 1.00      |  ❌ 0.XX
   CoC precision:         ✅ 1.00      |  ❌ 0.XX
   Escalation YAML:       ✅ unchanged | ⚠ modified — Legal review required

   VERDICT: GO  |  NO-GO

   If NO-GO, blocking reasons:
     1. <specific invariant or test>
     2. <specific invariant or test>
   ```

Do not auto-fix violations. Do not rewrite tests to pass. A NO-GO is a report, not a repair job — the human needs to see it and decide.
