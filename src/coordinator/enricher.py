"""
Enriches raw inbound messages with sender context before classification.
Reads from mock data files; in production these would be live system lookups.
"""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

_DATA = Path(__file__).parents[2] / "data"


def _load(filename: str) -> dict:
    return json.loads((_DATA / filename).read_text())


def _infer_sender(raw_message: str, attendees: dict) -> tuple[str | None, str, int]:
    """
    Returns (sender_id, sender_channel, history_count).
    In production this would come from a session/identity header.
    Uses heuristic matching for the mock implementation.
    """
    lower = raw_message.lower()

    for att_id, att in attendees["attendees"].items():
        if att["name"].lower() in lower:
            return att_id, att["channel"], att["message_history_count"]

    # Default: unknown sender on the ops channel
    return None, "ops", 0


def enrich(raw_message: str, request_id: str | None = None) -> dict:
    """
    Returns an enrichment dict:
      { request_id, raw_message, sender_id, sender_channel, sender_history_count }
    """
    if not request_id:
        request_id = str(uuid.uuid4())

    attendees = _load("attendees.json")
    sender_id, sender_channel, history_count = _infer_sender(raw_message, attendees)

    return {
        "request_id": request_id,
        "raw_message": raw_message,
        "sender_id": sender_id,
        "sender_channel": sender_channel,
        "sender_history_count": history_count,
    }
