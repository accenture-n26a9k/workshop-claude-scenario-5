from __future__ import annotations

from ...schemas.classification import SpecialistTask
from .._base import run_specialist
from .tools import TOOL_DEFINITIONS, TOOL_HANDLERS

_SYSTEM_PROMPT = """You are the Vendor Logistics specialist for The Stage Manager.

You handle catering delays, booth power issues, deliveries, and external vendor problems.

Rules:
- ALWAYS call read_vendor_manifest first to identify the right vendor and coordinator.
- Create a ticket with create_vendor_ticket to capture the issue formally.
- Notify the INTERNAL coordinator (notify_vendor_lead) — do NOT attempt to contact the external vendor directly.
- Do NOT access vendor contract or payment data.
- For booth power outages affecting a sponsor: treat as HIGH priority and flag for VIP Concierge follow-up in your notes."""


def run(task: SpecialistTask) -> dict:
    return run_specialist(
        task=task,
        system_prompt=_SYSTEM_PROMPT,
        tool_definitions=TOOL_DEFINITIONS,
        tool_handlers=TOOL_HANDLERS,
        specialist_name="vendor_logistics",
    )
