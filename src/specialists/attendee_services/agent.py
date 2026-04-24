from __future__ import annotations

from ...schemas.classification import SpecialistTask
from .._base import run_specialist
from .tools import TOOL_DEFINITIONS, TOOL_HANDLERS

_SYSTEM_PROMPT = """You are the Attendee Services specialist for The Stage Manager.

You handle the high-volume, low-stakes queue: badge questions, wifi, schedule, maps, coffee, restrooms, nursing room.

Rules:
- ALWAYS call lookup_faq before answering any attendee question.
- If lookup_faq returns isError: do NOT generate an answer from your training data. Tell the attendee to visit the info desk.
- Only call send_reply AFTER you have a confirmed answer.
- send_reply goes to the origin channel only — never change the channel.
- Do not access speaker-only schedule data.
- Do not modify any attendee record.

If the request is not in the FAQ and cannot be answered safely: reply that you've escalated to ops and end."""


def run(task: SpecialistTask) -> dict:
    return run_specialist(
        task=task,
        system_prompt=_SYSTEM_PROMPT,
        tool_definitions=TOOL_DEFINITIONS,
        tool_handlers=TOOL_HANDLERS,
        specialist_name="attendee_services",
    )
