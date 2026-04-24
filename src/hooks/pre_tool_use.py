"""
Deterministic safety brake. Not an LLM decision — string match only.
Executes before any write tool. Cannot be prompted away.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

SAFETY_KEYWORDS = [
    "fire", "alarm", "evacuation", "evac", "medical", "ambulance",
    "weapon", "bomb", "threat", "blood", "unconscious", "assault",
    "injury", "hurt", "emergency",
]

_AUDIT_PATH = Path("logs/safety_audit.jsonl")


def check_safety_keywords(raw_message: str) -> tuple[bool, list[str]]:
    lower = raw_message.lower()
    matched = [kw for kw in SAFETY_KEYWORDS if kw in lower]
    return bool(matched), matched


def _write_audit(entry: dict) -> None:
    _AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _AUDIT_PATH.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def pre_tool_use_hook(
    tool_name: str,
    tool_input: dict,
    raw_message: str,
    request_id: str,
    sender_id: str | None = None,
) -> dict:
    """
    Returns {"blocked": False} to allow execution, or
    {"blocked": True, "reason": ..., "matched_keywords": [...]} to hard-stop.

    On block: pages safety lead and writes to audit trail only.
    No public channel log. No auto-reply.
    """
    is_safety, matched = check_safety_keywords(raw_message)

    if is_safety:
        audit_entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "sender_id": sender_id,
            "raw_message": raw_message,
            "tool_attempted": tool_name,
            "tool_input": tool_input,
            "matched_keywords": matched,
            "action": "BLOCKED_HARD_PAGE",
        }
        _write_audit(audit_entry)

        _page_safety_lead(request_id, raw_message, sender_id, matched)

        return {
            "blocked": True,
            "reason": f"Safety keywords detected: {matched}",
            "matched_keywords": matched,
            "action": "HARD_PAGE",
        }

    return {"blocked": False}


def _page_safety_lead(
    request_id: str,
    raw_message: str,
    sender_id: str | None,
    matched_keywords: list[str],
) -> None:
    """Simulate paging the safety lead. In production: PagerDuty / SMS."""
    print(
        f"\n🚨 [SAFETY PAGE] request_id={request_id} sender={sender_id}\n"
        f"   Keywords: {matched_keywords}\n"
        f"   Message:  {raw_message}\n"
        f"   All further agent action on this request is BLOCKED.\n"
    )
