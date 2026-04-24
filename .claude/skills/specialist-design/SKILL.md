---
name: specialist-design
description: Design rules for adding or modifying a specialist subagent under src/specialists/. Covers the self-contained Task prompt rule (no inherited coordinator context), "what this tool does NOT do" tool descriptions, tool-count discipline, and the routing/escalation boundary. Use this skill whenever you create a new specialist or edit an existing specialist's agent.py, tools.py, or prompt.
---

# Specialist Design

Specialists are the second stage of the coordinator → specialist pipeline. The coordinator classifies, enriches, and validates; then it spawns one specialist in an isolated Task. The specialist does the real work: read the right data, decide, act (or escalate).

Specialists look simple. They are simple by design. Most of the subtlety is in the rules that keep them simple. Deviating from these rules has caused the exact failures this architecture exists to prevent — read `adr/001-agent-architecture.md` before you argue with a rule here.

## The four rules

### 1. The Task prompt is fully self-contained

A specialist Task inherits **no** state from the coordinator. No chain-of-thought, no scratchpad, no "by the way the classifier thought…". Everything the specialist needs to act must be passed explicitly in the Task prompt.

Why: the specialist's behavior has to be reproducible from its inputs alone. If it silently depends on coordinator reasoning, the specialist is no longer independently testable, auditable, or swappable. A misclassified message should *fail cleanly* in the specialist, not inherit a confident-but-wrong framing.

How to apply:
- The Task prompt includes the raw message, the enrichment metadata, and the classification — nothing more.
- The specialist does not ask the coordinator for clarification. It decides or escalates.
- When you write a new specialist, list every field you think it needs. If a field isn't in the enrichment schema, add it to the schema — do not reach back into coordinator state.

### 2. Tool descriptions state what the tool does NOT do

Every tool in `tools.py` has a description that includes a negative clause. This is load-bearing for routing correctness — when the model is deciding whether to call a tool, the negative clause is what prevents "close enough" misuse.

Example shape:
```
create_ops_ticket:
  Creates an operational ticket for a room/AV/facilities issue.
  Use when a crew member reports a problem with a specific room or piece of equipment.
  DOES NOT: page the safety lead, contact external vendors, notify sponsors,
  modify door access, or send messages to attendees.
```

When you add or edit a tool:
- Write the positive clause first: what it does, for what kind of request.
- Then write the negative clause: the *adjacent* things it is not for. Specifically call out the adjacent specialist's territory (e.g., a `room_ops` tool should explicitly say it does not do VIP concierge work).
- If the negative clause feels redundant, it probably isn't — adversarial messages exploit exactly the "obviously I know this tool isn't for that" cases.

### 3. Each specialist has 4–5 tools (safety_coc has 2)

Specialists are not Swiss Army knives. A large tool inventory dilutes the model's selection signal and creates new adjacent-misuse failure modes.

| Specialist | Expected tool count |
|---|---|
| `crew_services` | 4–5 |
| `room_ops` | 4–5 |
| `vip_concierge` | 4–5 |
| `safety_coc` | **exactly 2** — see `safety-brake-invariants` skill |
| `vendor_logistics` | 4–5 |

Before you add a sixth tool, ask: can this be folded into an existing tool with a broader signature? Can it be pushed up to the coordinator? Can it live in a utility and be called *from within* an existing tool? Adding is easy, removing is hard — favor consolidation.

### 4. Routing and escalation are not the specialist's job

The specialist decides: "do the thing, or hand off to a human." It does not decide "this should have gone to a different specialist" — by the time the Task has started, that call has been made upstream.

- If the specialist receives a message it cannot handle, it escalates with a reason. It does not call a different specialist's tools.
- Escalation rules live in `escalation_rules.yaml`, enforced in the coordinator. The specialist reads its own hard constraints from the skill/ADR, not from runtime state.
- Tickets created by a specialist include the classification and confidence that drove the spawn, so the ops lead can see if the upstream decision was wrong.

## Specialist-specific constraints (must be preserved)

These are stated in `CLAUDE.md` and are not negotiable during routine edits:

- **`crew_services`** — read-only tools plus `send_reply` to the origin channel *only*. No cross-channel writes.
- **`room_ops`** — must call `lookup_room_captain` before `create_ops_ticket`. The ticket without the captain is the bug.
- **`vip_concierge`** — never auto-replies without human confirmation. If you add an auto-reply path, you've broken the rule.
- **`safety_coc`** — 2 tools, zero public-channel writes, always human-in-the-loop. See `safety-brake-invariants` skill.
- **`vendor_logistics`** — never contacts an external vendor directly. Internal vendor lead only.

If a change touches any of these, verify the constraint still holds *by reading the code*, not by trusting the test suite.

## Scaffolding a new specialist

Follow this order, and update the eval dataset before you consider it ready.

1. **Write the ADR amendment.** A new specialist changes the category space — `adr/001-agent-architecture.md` needs an entry.
2. **Define the category** in `src/schemas/classification.py` and update the classifier's category list + few-shots.
3. **Create the directory**: `src/specialists/<name>/` with `__init__.py`, `agent.py`, `tools.py`.
4. **Design tools first, prompt second.** Tools constrain the prompt; the prompt cannot broaden the tools.
5. **Write tool descriptions with the positive-then-negative pattern** (rule 2 above).
6. **Write the system prompt.** Keep it short. Reference the tools by name. State the escalation criterion explicitly. Do not duplicate YAML escalation rules.
7. **Register the specialist** in the coordinator's routing table.
8. **Add eval cases**: at minimum 10 positive messages, 2 adversarial injection attempts, 2 boundary cases that could plausibly be another specialist's territory.
9. **Run the full harness**, not just the new specialist's tests. A new specialist can degrade routing for existing categories if the coordinator's classifier drifts.

## Before you mark the change done

```bash
# Specialist tool count (adjust path; expect 4–5 for most, 2 for safety_coc)
grep -cE '^(def |@tool|TOOL)' src/specialists/<name>/tools.py

# No cross-specialist tool imports
grep -nE 'from src\.specialists\.(crew_services|room_ops|vip_concierge|safety_coc|vendor_logistics)' \
  src/specialists/<name>/

# Every tool description has a negative clause
grep -nE 'DOES NOT|does not|NOT for' src/specialists/<name>/tools.py

# Full eval — not just the one you think you changed
python eval/harness.py --output eval/scorecard.json
```

If the scorecard regresses on *any* category (not just the one you touched), the coordinator's classifier has shifted and you need to look at the few-shots, not the specialist.
