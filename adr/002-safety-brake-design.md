# ADR-002: Two-Layer Safety Brake Design

**Status:** Accepted  
**Date:** 2024

---

## Context

A live-event ops agent has the ability to send messages, create tickets, page humans, and store records. In the presence of a safety emergency or a Code of Conduct report, an automatic action — any automatic action — is the wrong action. The human must own the response. The agent must stop.

Two failure modes exist:
1. The LLM misclassifies a safety message and routes it to the wrong specialist
2. An adversary crafts a message that tricks the LLM into taking an automated action during a safety event

Both must be blocked. An LLM-only solution cannot guarantee either.

---

## Decision

We implement two independent layers. Both must pass for a write tool to execute.

### Layer 1: PreToolUse Hook (Hard Stop, Deterministic)

Before any write tool executes, a Python function checks the raw message for a hardcoded keyword list:

```python
SAFETY_KEYWORDS = [
    "fire", "alarm", "evacuation", "evac", "medical", "ambulance",
    "weapon", "bomb", "threat", "blood", "unconscious", "assault",
    "injury", "hurt", "emergency",
]
```

**This is a string match. It is not an LLM decision. It cannot be prompted away.**

On match:
- Safety lead is paged via `_page_safety_lead()`
- Write tool execution is blocked
- Event is written to `logs/safety_audit.jsonl` only
- No public channel entry is created
- No auto-reply is sent
- All further agent action on this request is blocked

The hook is registered in `src/specialists/_base.py` and fires before every tool in `_WRITE_TOOLS`:
```python
_WRITE_TOOLS = {
    "send_reply", "create_ops_ticket", "send_room_alert",
    "notify_concierge", "create_vip_ticket",
    "page_safety_lead", "create_coc_record",
    "create_vendor_ticket", "notify_vendor_lead",
}
```

Note: `page_safety_lead` is itself a write tool. The hook fires on it too — this means a safety keyword in a CoC report does not result in a duplicate LLM-triggered page; the hook pages first and stops.

### Layer 2: Escalation Rules (Structured, Enumerated, Config-Driven)

Classification-level rules enforce routing decisions based on category, confidence, and dollar impact. These live in `escalation_rules.yaml` — not in a prompt — so they are auditable by Legal without reading code.

```yaml
escalation_rules:
  - condition: "category == SAFETY"
    action: HARD_PAGE
    threshold: null   # always

  - condition: "category == COC"
    action: HUMAN_ONLY
    threshold: 0.4    # low bar intentional

  - condition: "category == PRESS"
    action: HUMAN_ONLY
    threshold: null   # always
```

The rules are enforced in `src/coordinator/agent.py::_apply_escalation_rules()` after classification, before routing.

### Why Two Layers?

Layer 1 is a hard stop that fires regardless of classification. It catches:
- Misclassified safety messages (e.g., a fire alarm classified as ROOM_OPS)
- Adversarial messages that smuggle safety keywords alongside a benign request
- Any case where the coordinator loop does not execute (early failure)

Layer 2 is a slow stop that fires at routing time. It catches:
- Correctly classified but incorrectly routed messages
- Edge cases where confidence thresholds matter (VIP HIGH + low confidence → ESCALATE)
- Dollar impact escalations

Neither layer alone is sufficient. Layer 1 cannot express confidence-based or dollar-impact rules. Layer 2 depends on correct classification, which can be wrong.

---

## Alternatives Considered

**Single LLM-based safety check**  
Rejected. An LLM can be prompted into bypassing its own safety instructions. A string match cannot. For hard safety stops, determinism is required.

**Prompt-based escalation rules**  
Rejected. Prompt rules cannot be audited or versioned independently of the model. They can drift, be overridden by injection, or produce inconsistent thresholds. Config-in-YAML is auditable, diffable, and reviewable by Legal without reading model prompts.

**Per-specialist safety check (instead of shared hook)**  
Rejected. A shared hook in `_base.py` is harder to accidentally omit. If the hook were per-specialist, a new specialist added without the hook would have no safety brake. Shared is safer.

---

## Consequences

- Safety events are handled deterministically regardless of LLM output
- The hook is tested with 100% pass requirement in `tests/test_hooks.py`
- Escalation rules can be modified by product/Legal without code changes
- Safety audit trail is append-only and separate from all other logs
- The agent never auto-replies to a safety or CoC event under any circumstances
