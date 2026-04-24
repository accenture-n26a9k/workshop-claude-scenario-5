---
name: safety-brake-invariants
description: Invariants that must hold when touching safety/CoC paths — src/hooks/pre_tool_use.py, src/specialists/safety_coc/, SAFETY_KEYWORDS, escalation_rules.yaml. Use this skill whenever you read, edit, or review any of these files, or when discussing their behavior. The 100% safety precision guarantee depends on these rules holding; one erosion is one lawsuit.
---

# Safety Brake Invariants

The Stage Manager has a hard, non-negotiable precision requirement: **100% on safety, 100% on CoC, zero public auto-replies under either**. That guarantee is not produced by the LLM — it is produced by two independent layers that sit *around* the LLM. This skill enumerates the invariants those layers depend on. If any invariant is broken, the guarantee is gone, whether or not the tests still pass.

Authoritative reasoning lives in `adr/002-safety-brake-design.md`. Read it if you are unsure why a rule exists.

## The invariants

Before marking any change to a safety path "done", confirm every item below still holds. If even one is uncertain, stop and verify directly against the file.

### 1. The PreToolUse hook is a deterministic string match, not an LLM call

- `src/hooks/pre_tool_use.py` must perform a pure substring/token match against `SAFETY_KEYWORDS`.
- No `anthropic.*` import, no model call, no `await`, no async LLM client, no "classifier" function being invoked here.
- No regex with unbounded backtracking — catastrophic regex is its own risk.
- Rationale: an LLM can be prompted away. A string match cannot.

### 2. `safety_coc/tools.py` has exactly 2 tools

- Count the module-level tool definitions. Expected: 2.
- `page_safety_lead` and `create_coc_record` (names may differ slightly — check the file). Nothing else.
- Do not add `send_reply`, `create_ops_ticket`, `notify_concierge`, or anything that could write to a public channel. Not even "just for diagnostics". Not even behind a flag.
- Rationale: the safety/CoC specialist must be incapable of public action by construction, not by instruction.

### 3. Safety and CoC specialists never write to public channels

- Grep the safety/CoC paths (`src/specialists/safety_coc/`) for `send_reply`, channel-posting helpers, Slack webhooks, or anything resembling broadcast. Expected result: none.
- If a utility they import could post publicly, that is also a violation — the tool allowlist is the fence, not a suggestion.

### 4. Escalation rules live in `escalation_rules.yaml`, not in prompts

- Routing decisions for SAFETY / COC / PRESS / VIP-HIGH / low-confidence / high-dollar cases are enforced from YAML.
- If you are about to add an `if category == "SAFETY"` branch in a prompt or a Python file that duplicates a rule already in YAML, stop — that is the bug this design prevents.
- Legal audits the YAML. They do not and should not read the prompt to know when a human is paged.

### 5. The hook fires on every write tool, via `_base.py`

- Registration is in `src/specialists/_base.py` against `_WRITE_TOOLS`. It is shared, not per-specialist.
- If you add a new write-capable tool, its name must be in `_WRITE_TOOLS`. Adding a tool and forgetting to register it is how the brake gets silently bypassed.

### 6. `SAFETY_KEYWORDS` only grows, and every change ships with tests

- Never delete a keyword — the cost of a false positive (human pages on a benign "fire up the demo") is trivial next to the cost of a false negative.
- If you add a keyword, add a matching test in `tests/test_hooks.py`.
- If you remove one, justify it in the PR and in the ADR.

### 7. The safety audit trail is append-only and isolated

- `logs/safety_audit.jsonl` receives the hook's output. Nothing reads from it during the agent loop; nothing writes to it from a regular specialist path.
- No public log entry is emitted for a safety event. No auto-reply is composed. The only outward action is `_page_safety_lead()`.

## Verification checklist

Run these before declaring a change complete. Actually run them — do not infer.

```bash
# Hook is deterministic (expect: no LLM imports, no model calls)
grep -nE 'anthropic|client\.messages|AnthropicBedrock|await ' src/hooks/pre_tool_use.py

# safety_coc tool count (expect: 2)
grep -cE '^(def |@tool|TOOL)' src/specialists/safety_coc/tools.py

# No public-write tools in safety_coc
grep -nE 'send_reply|create_ops_ticket|notify_concierge|channel|webhook|slack' src/specialists/safety_coc/

# Safety hook tests pass (hard requirement: 100%)
pytest tests/test_hooks.py -v

# Adversarial tests still pass
pytest tests/test_adversarial.py -v

# Full eval — safety and CoC precision must remain 100%
python eval/harness.py --output eval/scorecard.json && \
  python -c "import json; s=json.load(open('eval/scorecard.json')); \
  assert s['by_category']['SAFETY']['precision']==1.0, 'SAFETY precision regressed'; \
  assert s['by_category']['COC']['precision']==1.0, 'COC precision regressed'; \
  print('OK — safety/CoC precision 100%')"
```

If any command surfaces a violation, **do not** patch the test to pass. Fix the code, or revert the change.

## Common traps

- "I'll just add a tiny LLM check to the hook for ambiguous cases." No. The whole point is determinism. Put ambiguity handling in a *separate* step that runs *after* the hook and has no authority to unblock what the hook blocked.
- "I'll let safety_coc send a reassurance reply so the reporter knows we saw it." No. Auto-replying to a CoC reporter is one of the exact failure modes this system exists to prevent. A human sends that message.
- "I'll move one rule out of YAML and into the classifier prompt because it's cleaner." No. That rule is auditable today. In a prompt, it isn't.
- "I'll add a third tool to safety_coc, just a read-only one." Measure carefully. If it is truly read-only and cannot trigger side effects, it may be acceptable — but update this skill, the ADR, and the tests. Do not silently bump the count.
- "Tests pass, I'm done." The tests are a floor, not a ceiling. They can pass while an invariant above is broken.

## When the invariants genuinely need to change

Sometimes they do. If a real requirement is pushing against one of these rules:

1. Write an ADR superseding or amending `adr/002-safety-brake-design.md`.
2. Get Legal sign-off in the PR (this is explicitly their turf).
3. Update this skill to reflect the new rule.
4. Update the eval harness thresholds only if Legal has agreed to the new precision floor — never silently.

The rules are load-bearing. Move them deliberately, not incidentally.
