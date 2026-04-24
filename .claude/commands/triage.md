---
description: Run a message through the coordinator and show the full triage trace — classification, enrichment, validation retries, safety-hook outcome, and the specialist that would be spawned.
---

Run the message `$ARGUMENTS` through the coordinator pipeline end-to-end and report every stage. This is for fast iteration on edge cases — it does not actually spawn the specialist Task or send any outbound action.

Steps:

1. **Reproduce deterministically.** If `$ARGUMENTS` is empty, ask the user for a message. Otherwise treat everything after the command name as the raw message text (quotes included verbatim — do not strip).

2. **Check the hook first.** Call the same substring logic `src/hooks/pre_tool_use.py` uses against the raw message. Report:
   - Which keyword(s) matched, if any.
   - If any matched: stop here, report `HARD_PAGE` would fire and the write path would be blocked. Do not run the classifier for this path — that's the whole point of the brake being upstream of the LLM. Still print the rest of the report with "not evaluated" markers so the reader sees the full stage list.

3. **Run the classifier.** Invoke `src/coordinator/classifier.py` on the message and report:
   - Category + confidence.
   - The raw validator output (before retries).
   - If validation failed: the specific Pydantic error, the retry count, and whether it eventually passed or hit the 3-retry escalation path.

4. **Run the enricher.** Report the enrichment fields attached: `sender_role`, `sla_tier`, any routing metadata. Mark any field the enricher could not resolve — those are often the real bug.

5. **Apply escalation rules.** Read `escalation_rules.yaml` and show which rule matched, if any, and the action it produced (`HARD_PAGE`, `HUMAN_ONLY`, `ESCALATE`, or fall-through to routing).

6. **Name the specialist.** Based on category + rule outcome, state which specialist would be spawned and in which mode (auto-resolve, routed with SLA, escalated with context). Do not actually spawn it.

7. **Format the report as a compact trace.** One line per stage, so a regression diff is readable:

   ```
   HOOK          : no keyword match
   CLASSIFIER    : VIP (confidence=0.72)
   VALIDATOR     : ok (0 retries)
   ENRICHER      : sender_role=sponsor_liaison, sla_tier=HIGH
   ESCALATION    : rule "VIP high tier + uncertain" matched → ESCALATE
   SPECIALIST    : vip_concierge (escalation mode, human confirmation required)
   ```

8. **If the outcome is surprising, flag it.** Compare against the closest entry in `eval/dataset.json` if there is one. If the classification disagrees with the expected label on a nearby case, say so explicitly — that is the signal worth acting on.

Do not modify any files. Do not call real external tools. This command is read-only and exists to shorten the loop between "I wonder what would happen if…" and an answer you can trust.
