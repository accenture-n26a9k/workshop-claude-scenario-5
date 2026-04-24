"""
Coordinator agent: the entry point for every inbound message.
Enriches → validates/classifies → applies escalation rules → routes to specialist.
Logs every decision with request_id, attempt_count, error_type, routing_target, latency_ms.
"""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path

from ..hooks.pre_tool_use import check_safety_keywords, _page_safety_lead
from ..schemas.classification import Category, Classification, RoutingDecision, SpecialistTask
from .enricher import enrich
from .validator import validate_with_retry

_LOG_PATH = Path("logs/coordinator.jsonl")


def _log(entry: dict) -> None:
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _LOG_PATH.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def _apply_escalation_rules(classification: Classification) -> Classification:
    """
    Post-classification escalation rule engine.
    Rules are documented in escalation_rules.yaml; this is the enforcement.
    """
    c = classification

    # Safety is always a hard page — belt and suspenders with the hook
    if c.category == Category.SAFETY:
        return c.model_copy(update={"routing_decision": RoutingDecision.HARD_PAGE})

    # CoC and Press always go to human
    if c.category in (Category.COC, Category.PRESS):
        return c.model_copy(update={"routing_decision": RoutingDecision.ESCALATE})

    # Adversarial content always surfaces to a human
    if c.adversarial_flag:
        return c.model_copy(update={"routing_decision": RoutingDecision.ESCALATE})

    # Low confidence (non-FAQ) → escalate
    if c.confidence < 0.60 and c.category != Category.FAQ:
        return c.model_copy(update={"routing_decision": RoutingDecision.ESCALATE})

    # VIP HIGH impact with uncertain confidence → escalate
    from ..schemas.classification import ImpactTier
    if c.category == Category.VIP and c.impact_tier == ImpactTier.HIGH and c.confidence < 0.85:
        return c.model_copy(update={"routing_decision": RoutingDecision.ESCALATE})

    # High dollar impact → escalate
    if c.estimated_dollar_impact and c.estimated_dollar_impact > 5000:
        return c.model_copy(update={"routing_decision": RoutingDecision.ESCALATE})

    return c


def _build_specialist_task(enrichment: dict, classification: Classification) -> SpecialistTask:
    return SpecialistTask(
        request_id=enrichment["request_id"],
        raw_message=enrichment["raw_message"],
        category=classification.category,
        confidence=classification.confidence,
        impact_tier=classification.impact_tier,
        sla_tier=classification.sla_tier,
        routing_decision=classification.routing_decision,
        sender_id=enrichment["sender_id"],
        sender_channel=enrichment["sender_channel"],
        sender_history_count=enrichment["sender_history_count"],
        reasoning=classification.reasoning,
        adversarial_flag=classification.adversarial_flag,
    )


def _route(task: SpecialistTask) -> dict:
    """Dispatch to the correct specialist. Each specialist is self-contained."""
    from ..specialists.attendee_services.agent import run as run_attendee
    from ..specialists.room_ops.agent import run as run_room_ops
    from ..specialists.vip_concierge.agent import run as run_vip
    from ..specialists.safety_coc.agent import run as run_safety
    from ..specialists.vendor_logistics.agent import run as run_vendor

    routing_map = {
        Category.FAQ: run_attendee,
        Category.ROOM_OPS: run_room_ops,
        Category.VIP: run_vip,
        Category.SAFETY: run_safety,
        Category.COC: run_safety,
        Category.VENDOR: run_vendor,
        Category.PRESS: None,  # always escalated before reaching here
        Category.UNKNOWN: None,
    }

    runner = routing_map.get(task.category)
    if runner is None:
        return {"action": "ESCALATE", "reason": f"No specialist for category {task.category}"}

    return runner(task)


def process(raw_message: str, request_id: str | None = None) -> dict:
    """
    Main entry point. Processes one inbound message end-to-end.
    Returns the outcome dict including routing target and specialist result.
    """
    t_start = time.monotonic()
    request_id = request_id or str(uuid.uuid4())

    # Layer 1: hard stop before any processing if safety keywords present
    is_safety, matched = check_safety_keywords(raw_message)
    if is_safety:
        _page_safety_lead(request_id, raw_message, None, matched)
        outcome = {
            "request_id": request_id,
            "routing_decision": "HARD_PAGE",
            "category": "SAFETY",
            "matched_keywords": matched,
            "latency_ms": round((time.monotonic() - t_start) * 1000, 1),
        }
        _log(outcome)
        return outcome

    # Enrich
    enrichment = enrich(raw_message, request_id)

    # Classify with validation-retry loop
    classification, attempt_count, error_type = validate_with_retry(raw_message, request_id)

    # Apply escalation rules
    classification = _apply_escalation_rules(classification)

    # Build task packet for specialist
    task = _build_specialist_task(enrichment, classification)

    # Route
    specialist_result = _route(task)

    latency_ms = round((time.monotonic() - t_start) * 1000, 1)

    outcome = {
        "request_id": request_id,
        "category": classification.category,
        "confidence": classification.confidence,
        "routing_decision": classification.routing_decision,
        "routing_target": classification.category,
        "attempt_count": attempt_count,
        "error_type": error_type,
        "adversarial_flag": classification.adversarial_flag,
        "adversarial_type": classification.adversarial_type,
        "sla_tier": classification.sla_tier,
        "reasoning": classification.reasoning,
        "specialist_result": specialist_result,
        "latency_ms": latency_ms,
    }
    _log(outcome)
    return outcome
