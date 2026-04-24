"""
Validation-retry loop. Feeds schema errors back to the classifier for self-correction.
Escalates with validation_failure flag after MAX_RETRIES.
"""

from __future__ import annotations

from pydantic import ValidationError

from ..schemas.classification import Category, Classification, ImpactTier, RoutingDecision, SLATier
from .classifier import classify

MAX_RETRIES = 3


def validate_with_retry(
    raw_message: str,
    request_id: str,
) -> tuple[Classification, int, str | None]:
    """
    Returns (classification, attempt_count, error_type).
    error_type is None on success, or "validation_failure" after exhausting retries.
    Every request logs attempt_count and error_type for the audit trail.
    """
    last_error: str | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        raw = classify(raw_message, validation_error=last_error)
        raw["request_id"] = request_id

        try:
            classification = Classification(**raw)
            return classification, attempt, None
        except ValidationError as exc:
            last_error = _format_validation_error(exc)

    # Exhausted retries — return a safe escalation fallback
    fallback = Classification(
        request_id=request_id,
        category=Category.UNKNOWN,
        confidence=0.0,
        sla_tier=SLATier.HIGH,
        routing_decision=RoutingDecision.ESCALATE,
        reasoning=f"Classification validation failed after {MAX_RETRIES} attempts: {last_error}",
        adversarial_flag=False,
    )
    return fallback, MAX_RETRIES, "validation_failure"


def _format_validation_error(exc: ValidationError) -> str:
    errors = exc.errors()
    lines = []
    for err in errors:
        loc = " -> ".join(str(x) for x in err["loc"])
        lines.append(f"  Field '{loc}': {err['msg']}")
    return "\n".join(lines)
