# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**The Stage Manager** — a multi-agent intake triage system for the internal ops channel at live conferences. It handles messages from **ops crew and staff** (room captains, AV techs, vendor contacts, sponsor liaisons) — not attendees. Attendee-facing communication is deliberately out of scope; the ops channel's value depends on staying clean.

The system classifies, routes, and resolves every inbound ops message so the ops lead sees only what genuinely needs her judgment — roughly 20% of total volume. The other 80% is auto-resolved, routed to the right specialist, or escalated with context already attached.

## Commands

```bash
# Install dependencies
pip install anthropic pydantic

# Required env var (standard Anthropic API)
export ANTHROPIC_API_KEY=your_key_here

# Or AWS Bedrock (eu-north-1 bearer token)
export AWS_BEARER_TOKEN_BEDROCK=bedrock-api-key-...

# Run live demo
python demo/injector.py

# Watch ops-lead dashboard (separate terminal)
python demo/dashboard.py

# Full eval harness — produces eval/scorecard.json
python eval/harness.py --output eval/scorecard.json

# Adversarial subset only
python eval/harness.py --subset adversarial

# All tests
pytest tests/

# Safety brake tests (must be 100% pass)
pytest tests/test_hooks.py -v

# Adversarial injection tests
pytest tests/test_adversarial.py -v
```

## Architecture

### Coordinator → Specialist flow

Every inbound message goes through `src/coordinator/` in three steps:

1. **`classifier.py`** — assigns category + confidence score
2. **`enricher.py`** — attaches sender role/history, SLA tier, contextual metadata
3. **`validator.py`** — validates output against the Pydantic schema in `src/schemas/classification.py`; feeds the specific error back to Claude and retries up to 3 times on failure; escalates with `validation_failure=true` after 3 failures

The coordinator then spawns one of five specialist subagents. **Task subagents receive no inherited coordinator context** — every specialist operates only on what is explicitly passed in the Task prompt (see `adr/001-agent-architecture.md`). This is intentional.

### Specialists (`src/specialists/`)

| Specialist | Handles | Key constraint |
|---|---|---|
| `crew_services` (code: `attendee_services`) | Crew FAQ, schedule, logistics, internal questions | Read-only tools + `send_reply` to origin channel only |
| `room_ops` | AV failures, facilities, captain routing | Must call `lookup_room_captain` before `create_ops_ticket` |
| `vip_concierge` | Sponsors, VIPs, accessibility | Never auto-replies without human confirmation |
| `safety_coc` | Safety incidents, CoC reports | 2 tools only; no public channel writes; always human |
| `vendor_logistics` | Catering, booth power, deliveries | Never contacts external vendor directly |

> **Note:** The README names the first specialist `crew_services`; the current code directory is `attendee_services`. These are the same specialist — rename pending.

Each specialist has ~4–5 tools. Tool descriptions in `tools.py` explicitly state what each tool does *not* do — this is load-bearing for routing correctness.

### Client factory (`src/utils/client.py`)

When `AWS_BEARER_TOKEN_BEDROCK` is set the app uses `AnthropicBedrock` (eu-north-1, cross-region inference profiles). When `ANTHROPIC_API_KEY` is set it uses the standard `Anthropic` client. Model IDs are selected automatically by `coordinator_model()` and `specialist_model()`.

### Safety brake (`src/hooks/pre_tool_use.py`)

Two independent layers:

1. **PreToolUse hook** — deterministic string match against `SAFETY_KEYWORDS` before any write tool executes. Not an LLM decision. Cannot be prompted away. On match: pages safety lead, blocks all further agent action, writes only to the safety audit trail — no public log, no auto-reply.

2. **Escalation rules** (`escalation_rules.yaml`) — structured conditions on category + confidence + dollar impact. Lives in config, not in a prompt, so Legal can audit without reading code. `SAFETY` and `COC` always go to human; `PRESS` always human; confidence < 0.60 (non-FAQ) escalates.

### Routing decisions

The four possible outcomes for every message: **Auto-resolve** (agent replies directly), **Route** (specialist queue, SLA clock started), **Escalate** (human notified with full context), **Hard page** (safety lead paged, agent stops, no auto-reply).

### Eval harness (`eval/`)

100 labeled messages stratified across categories. Key metrics: safety precision = 100% (zero misses), CoC precision = 100% (zero auto-replies), adversarial pass ≥ 95%, overall accuracy ≥ 90%. Runs in CI; `eval/scorecard.json` is the Legal-facing artifact.

## Hard constraints

These are architectural decisions, not preferences — do not relax them:

- The ops channel is for crew. The agent never replies to attendees and attendee-facing features are not in scope.
- Safety/CoC specialists never write to public channels under any circumstances
- `safety_coc/tools.py` has exactly 2 tools
- The PreToolUse hook is a string match, not an LLM call
- Escalation rules live in `escalation_rules.yaml`, not in system prompts
- Each specialist's Task prompt must be fully self-contained — no shared state with coordinator
- Press/media inquiries always route to human, no exceptions
- The agent never opens doors, modifies crew permissions, or makes financial commitments > $500
