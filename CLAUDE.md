# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**The Stage Manager** — a multi-agent intake system built on the Claude Agent SDK that triages, routes, and resolves operational requests at live events in real time. Coordinator + specialist architecture; five specialist subagents; deterministic safety brake; eval harness with adversarial cases.

## Commands

```bash
# Install dependencies
pip install anthropic pydantic

# Required env var
export ANTHROPIC_API_KEY=your_key_here

# Run live demo (20 messages in 15 simulated seconds)
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
2. **`enricher.py`** — attaches sender history, SLA tier, contextual metadata
3. **`validator.py`** — validates the structured output against the Pydantic schema in `src/schemas/classification.py`; on failure, feeds the specific error back to the coordinator and retries up to 3 times; escalates with `validation_failure=true` after 3 failures

The coordinator then spawns one of five specialist subagents via `Task{}`. **Task subagents receive no inherited coordinator context** — every specialist operates only on what is explicitly passed in the Task prompt (see `adr/001-agent-architecture.md`). This is intentional.

### Specialists (`src/specialists/`)

| Specialist | Handles | Key constraint |
|---|---|---|
| `attendee_services` | FAQ, badge, schedule, wifi | Read-only tools + `send_reply` to origin channel only |
| `room_ops` | AV failures, facilities, captain routing | Must call `lookup_room_captain` before `create_ops_ticket` |
| `vip_concierge` | Sponsors, VIPs, accessibility | Never auto-replies without human confirmation |
| `safety_coc` | Safety incidents, CoC reports | 2 tools only; no public channel writes; always human |
| `vendor_logistics` | Catering, booth power, deliveries | Never contacts external vendor directly |

Each specialist has ~4–5 tools. Tool descriptions in `tools.py` files explicitly state what each tool does *not* do — this is load-bearing for routing correctness.

### Safety brake (`src/hooks/pre_tool_use.py`)

Two independent layers:

1. **PreToolUse hook** — deterministic string match against `SAFETY_KEYWORDS` before any write tool executes. Not an LLM decision. Cannot be prompted away. On match: pages safety lead, blocks all further agent action on the request, writes only to the safety audit trail.

2. **Escalation rules** (`escalation_rules.yaml`) — structured conditions on category + confidence + dollar impact. Lives in config, not in a prompt, so Legal can audit it without reading code. `SAFETY` and `COC` categories always go to human; `PRESS` always human; confidence < 0.60 (non-FAQ) escalates.

### Routing decisions

The four possible outcomes for every message: **Auto-resolve** (agent replies directly), **Route** (to specialist queue with SLA clock), **Escalate** (human notified with context), **Hard page** (safety lead paged, agent stops, no auto-reply).

### Eval harness (`eval/`)

100 labeled messages stratified across categories. Key metrics: safety precision = 100% (zero misses), CoC precision = 100% (zero auto-replies), adversarial pass ≥ 95%, overall accuracy ≥ 90%. Runs in CI; produces `eval/scorecard.json` as a Legal-facing artifact.

## Hard constraints

These are architectural decisions, not preferences — do not relax them:

- Safety/CoC specialists never write to public channels under any circumstances
- `safety_coc/tools.py` has exactly 2 tools
- The PreToolUse hook is a string match, not an LLM call
- Escalation rules live in config (`escalation_rules.yaml`), not in system prompts
- Each specialist's Task prompt must be fully self-contained — no shared state with coordinator
- Press/media inquiries always route to human, no exceptions
