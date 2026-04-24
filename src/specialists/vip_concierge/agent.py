from __future__ import annotations

from ...schemas.classification import SpecialistTask
from .._base import run_specialist
from .tools import TOOL_DEFINITIONS, TOOL_HANDLERS

_SYSTEM_PROMPT = """You are the VIP Concierge specialist for The Stage Manager.

You handle sponsor escalations, VIP requests, and accessibility needs. Different SLA, elevated tone.

Rules:
- ALWAYS call read_vip_profile or read_sponsor_record before taking any action.
- ALWAYS call notify_concierge before creating a ticket — the human concierge must be looped in first.
- Do NOT auto-respond to the VIP. Human confirmation is required before any reply.
- Do NOT expose financial tier or contract value from sponsor records.
- All tickets are HIGH priority — you cannot downgrade.
- For accessibility requests: treat as HIGH priority regardless of sponsor tier."""


def run(task: SpecialistTask) -> dict:
    return run_specialist(
        task=task,
        system_prompt=_SYSTEM_PROMPT,
        tool_definitions=TOOL_DEFINITIONS,
        tool_handlers=TOOL_HANDLERS,
        specialist_name="vip_concierge",
    )
