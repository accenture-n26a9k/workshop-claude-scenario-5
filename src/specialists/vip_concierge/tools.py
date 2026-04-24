"""
VIP Concierge tools.
Handles sponsor escalations, VIP requests, accessibility needs.
Never auto-replies to a VIP without human confirmation first.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

_DATA = Path(__file__).parents[3] / "data"


def _load(filename: str) -> dict:
    return json.loads((_DATA / filename).read_text())


def read_vip_profile(sender_id: str) -> dict:
    """
    Return VIP guest preferences, dietary, and access needs.
    Does NOT expose financial tier or contract value.
    """
    guests = _load("vip_guests.json")
    record = guests["vip_guests"].get(sender_id)

    if not record:
        return {
            "isError": True,
            "reason": "VIP_RECORD_NOT_FOUND",
            "guidance": f"No VIP profile for sender_id={sender_id}. Treat as high-priority and escalate to concierge.",
        }

    return {
        "found": True,
        "name": record["name"],
        "dietary": record["dietary"],
        "access_needs": record.get("access_needs", []),
        "concierge_id": record.get("concierge_id"),
    }


def read_sponsor_record(sender_id: str) -> dict:
    """
    Return booth number, assigned concierge, and SLA tier for a sponsor.
    Does NOT modify the sponsor record or expose contract value.
    """
    vendors = _load("vendors.json")

    for sponsor_id, sponsor in vendors["sponsors"].items():
        if sponsor_id == sender_id or sponsor.get("contact", "").startswith(sender_id):
            concierge = vendors["concierges"].get(sponsor["concierge_id"], {})
            return {
                "found": True,
                "company": sponsor["company"],
                "booth": sponsor["booth"],
                "tier": sponsor["tier"],
                "sla_tier": sponsor["sla_tier"],
                "concierge_id": sponsor["concierge_id"],
                "concierge_name": concierge.get("name"),
                "concierge_channel": concierge.get("channel"),
            }

    return {
        "isError": True,
        "reason": "SPONSOR_NOT_FOUND",
        "guidance": "No sponsor record found. Escalate to VIP ops lead immediately.",
    }


def notify_concierge(concierge_id: str, request_id: str, message: str) -> dict:
    """
    Page the assigned human concierge with full context.
    Does NOT auto-respond to VIP — human must confirm before any reply goes out.
    """
    vendors = _load("vendors.json")
    concierge = vendors["concierges"].get(concierge_id)

    if not concierge:
        return {
            "isError": True,
            "reason": "CONCIERGE_NOT_FOUND",
            "guidance": f"concierge_id={concierge_id} not found. Page ops lead directly.",
        }

    print(f"  [CONCIERGE PAGE → {concierge['channel']}] {concierge['name']}: {message}")
    return {
        "notified": True,
        "concierge_name": concierge["name"],
        "channel": concierge["channel"],
    }


def create_vip_ticket(request_id: str, issue_type: str, description: str, concierge_id: str) -> dict:
    """
    Create a high-priority ticket in the concierge queue.
    Does NOT downgrade ticket priority.
    Always creates at HIGH priority.
    """
    ticket_id = f"VIP-{uuid.uuid4().hex[:6].upper()}"
    ticket = {
        "ticket_id": ticket_id,
        "request_id": request_id,
        "issue_type": issue_type,
        "description": description,
        "priority": "HIGH",
        "assigned_concierge": concierge_id,
        "status": "open",
    }
    print(f"  [VIP TICKET] {json.dumps(ticket)}")
    return {"created": True, "ticket_id": ticket_id, "priority": "HIGH"}


TOOL_DEFINITIONS = [
    {
        "name": "read_vip_profile",
        "description": (
            "Return VIP preferences, dietary restrictions, and access needs. "
            "Does NOT expose financial tier or contract value. "
            "Use sender_id from request context."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sender_id": {"type": "string"},
            },
            "required": ["sender_id"],
        },
    },
    {
        "name": "read_sponsor_record",
        "description": (
            "Return booth number, assigned concierge, and SLA tier for a sponsor. "
            "Does NOT modify sponsor data or expose contract value."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sender_id": {"type": "string"},
            },
            "required": ["sender_id"],
        },
    },
    {
        "name": "notify_concierge",
        "description": (
            "Page the assigned human concierge with context. "
            "Does NOT auto-reply to VIP — human must confirm before any response. "
            "Always call this for VIP requests. concierge_id from read_vip_profile or read_sponsor_record."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "concierge_id": {"type": "string"},
                "request_id": {"type": "string"},
                "message": {"type": "string", "description": "Full context for the concierge"},
            },
            "required": ["concierge_id", "request_id", "message"],
        },
    },
    {
        "name": "create_vip_ticket",
        "description": (
            "Create a HIGH-priority ticket in the concierge queue. "
            "Always creates at HIGH priority — cannot be downgraded. "
            "Call after notify_concierge."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "request_id": {"type": "string"},
                "issue_type": {"type": "string", "enum": ["DIETARY", "ACCESSIBILITY", "BOOTH_POWER", "AV", "GENERAL"]},
                "description": {"type": "string"},
                "concierge_id": {"type": "string"},
            },
            "required": ["request_id", "issue_type", "description", "concierge_id"],
        },
    },
]

TOOL_HANDLERS = {
    "read_vip_profile": lambda inp: read_vip_profile(inp["sender_id"]),
    "read_sponsor_record": lambda inp: read_sponsor_record(inp["sender_id"]),
    "notify_concierge": lambda inp: notify_concierge(
        inp["concierge_id"], inp["request_id"], inp["message"]
    ),
    "create_vip_ticket": lambda inp: create_vip_ticket(
        inp["request_id"], inp["issue_type"], inp["description"], inp["concierge_id"]
    ),
}
