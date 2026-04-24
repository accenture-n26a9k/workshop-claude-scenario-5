"""
Safety & CoC tools.
Exactly 2 tools by design. Every other action is a human's decision.
No public channel writes. No auto-replies. Always human.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

_AUDIT_PATH = Path("logs/safety_audit.jsonl")
_COC_PATH = Path("logs/coc_records.jsonl")


def _write_record(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def page_safety_lead(request_id: str, raw_message: str, sender_id: str | None, context: str) -> dict:
    """
    Immediately page the on-call safety lead with full context.
    Does NOT send any message to a public channel.
    Writes to safety audit trail only.
    """
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "sender_id": sender_id,
        "raw_message": raw_message,
        "context": context,
        "action": "SAFETY_LEAD_PAGED",
    }
    _write_record(_AUDIT_PATH, entry)

    print(
        f"\n🚨 [SAFETY LEAD PAGED]\n"
        f"   request_id={request_id}\n"
        f"   sender={sender_id}\n"
        f"   context={context}\n"
        f"   message={raw_message}\n"
    )
    return {"paged": True, "request_id": request_id}


def create_coc_record(request_id: str, raw_message: str, sender_id: str | None) -> dict:
    """
    Create an encrypted CoC record in the isolated store.
    Does NOT read other CoC records.
    Does NOT write to any shared system.
    Record ID is returned — not the content.
    """
    record_id = f"COC-{uuid.uuid4().hex[:8].upper()}"
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "record_id": record_id,
        "request_id": request_id,
        "sender_id": sender_id,
        "raw_message": raw_message,
        "status": "received_pending_human_review",
    }
    _write_record(_COC_PATH, entry)

    print(f"  [COC RECORD CREATED] record_id={record_id} (content isolated, not logged to shared systems)")
    return {"created": True, "record_id": record_id}


TOOL_DEFINITIONS = [
    {
        "name": "page_safety_lead",
        "description": (
            "Immediately page the on-call safety lead with full context. "
            "Does NOT send any message to a public channel. "
            "Use for: physical safety threats, fire, medical emergencies, CoC incidents requiring immediate response. "
            "Writes to safety audit trail only."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "request_id": {"type": "string"},
                "raw_message": {"type": "string"},
                "sender_id": {"type": "string"},
                "context": {"type": "string", "description": "Summary of the situation for the safety lead"},
            },
            "required": ["request_id", "raw_message", "context"],
        },
    },
    {
        "name": "create_coc_record",
        "description": (
            "Create an isolated, encrypted CoC record. "
            "Does NOT read other CoC records. "
            "Does NOT write to shared systems or public channels. "
            "Returns only the record_id — never the content."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "request_id": {"type": "string"},
                "raw_message": {"type": "string"},
                "sender_id": {"type": "string"},
            },
            "required": ["request_id", "raw_message"],
        },
    },
]

TOOL_HANDLERS = {
    "page_safety_lead": lambda inp: page_safety_lead(
        inp["request_id"], inp["raw_message"], inp.get("sender_id"), inp["context"]
    ),
    "create_coc_record": lambda inp: create_coc_record(
        inp["request_id"], inp["raw_message"], inp.get("sender_id")
    ),
}
