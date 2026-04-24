# ADR-001: Coordinator + Specialist Architecture with Explicit Context Passing

**Status:** Accepted  
**Date:** 2024

---

## Context

The Stage Manager must handle a continuous inbound stream across multiple categories — FAQ, AV failures, VIP requests, safety incidents, CoC reports, vendor issues, and press — simultaneously, at a live conference. A single flat agent would face competing prompt priorities, tool-count reliability degradation, and dangerous cross-contamination between sensitive categories (CoC, Safety) and routine ones (FAQ).

---

## Decision

We use a **coordinator + specialist** architecture:

1. The **coordinator** ingests every message, classifies it, enriches it with sender context, validates the output, and routes it to one of five specialist subagents via an explicit Task prompt.
2. Each **specialist** operates in isolation with its own system prompt, its own bounded tool set, and no access to any context outside what is explicitly passed in its Task prompt.

### Context Passing — The Critical Design Rule

**Task subagents do not inherit the coordinator's context.**

This is not a limitation — it is a deliberate constraint. Each specialist receives a self-contained `SpecialistTask` struct:

```
{ request_id, raw_message, category, confidence, impact_tier, sla_tier,
  routing_decision, sender_id, sender_channel, sender_history_count,
  reasoning, adversarial_flag }
```

Nothing from the coordinator's conversation history, tool results, or reasoning chain is implicitly available. Every specialist starts clean.

**Why this matters:**
- A specialist can never be prompted into accessing CoC records or Safety audit logs by referencing context from a prior request
- Tool-count discipline (4–5 tools per specialist) is enforceable because each specialist has a bounded scope
- A specialist compromise cannot cascade — it has no visibility into other specialists' work
- Prompts are auditable in isolation; Legal and Security can review each specialist independently

### Agent Loop

```
Inbound Message
      │
      ▼
[PreToolUse Hook — hard stop if safety keywords]
      │ (passes)
      ▼
[Coordinator]
  1. enrich(raw_message)          → sender_id, channel, history
  2. classify(raw_message)        → category, confidence, routing_decision
  3. validate_with_retry(...)     → Classification (up to 3 attempts)
  4. _apply_escalation_rules(...) → may upgrade routing_decision
  5. _route(task)                 → dispatches to specialist
      │
      ▼
[Specialist Agent Loop]
  - Receives SpecialistTask only
  - Calls tools (PreToolUse hook fires on every write tool)
  - Returns SpecialistOutcome
      │
      ▼
[Log outcome]   request_id | attempt_count | error_type | routing_target | latency_ms
```

### stop_reason Handling

The specialist loop checks `response.stop_reason`:
- `end_turn` → extract final text, return outcome
- `tool_use` → execute tools (with hook), append results, continue loop
- Anything else → exit loop, escalate

`MAX_ITERATIONS = 10` per specialist prevents runaway loops.

---

## Alternatives Considered

**Single flat agent with all tools**  
Rejected. Tool-selection reliability drops significantly past 5–6 tools. A single agent with 20+ tools for all categories would have unpredictable routing and no isolation between Safety/CoC and routine operations.

**Shared context between coordinator and specialists**  
Rejected. Shared context creates implicit coupling that is hard to audit, allows cross-contamination between sensitive and routine categories, and makes it impossible to reason about what each specialist can and cannot access.

**Tool-level permission system instead of specialist isolation**  
Rejected. Permission systems can be bypassed by prompt manipulation. Physical isolation (separate specialist prompt + context boundary) is a stronger guarantee.

---

## Consequences

- Every specialist can be reviewed, tested, and audited independently
- Adding a new specialist category requires no changes to existing specialists
- Tool counts stay bounded per specialist (documented in CLAUDE.md)
- Log records are fully replayable from `request_id` alone
