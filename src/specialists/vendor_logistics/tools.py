"""
Vendor Logistics tools.
Handles catering delays, booth power, deliveries, external vendor issues.
Never contacts the external vendor directly — always internal coordinator.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

_DATA = Path(__file__).parents[3] / "data"


def _load(filename: str) -> dict:
    return json.loads((_DATA / filename).read_text())


def read_vendor_manifest(vendor_query: str) -> dict:
    """
    Return vendor schedule, contact, and dock assignment.
    Does NOT access vendor contract or payment data.
    Matches by vendor type or name.
    """
    vendors = _load("vendors.json")

    query_lower = vendor_query.lower()
    results = []

    for vendor_id, vendor in vendors["vendors"].items():
        if (
            query_lower in vendor["name"].lower()
            or query_lower in vendor["type"].lower()
        ):
            results.append({
                "vendor_id": vendor_id,
                "name": vendor["name"],
                "type": vendor["type"],
                "dock_assignment": vendor["dock_assignment"],
                "schedule": vendor["schedule"],
                "coordinator_id": vendor["coordinator_id"],
            })

    if results:
        return {"found": True, "vendors": results}

    return {
        "isError": True,
        "reason": "VENDOR_NOT_FOUND",
        "guidance": f"No vendor matched '{vendor_query}'. Try vendor type: catering, booth_setup, av_equipment, delivery.",
    }


def create_vendor_ticket(vendor_name: str, issue_type: str, location: str, description: str) -> dict:
    """
    Create a ticket with vendor name, issue type, and location.
    Does NOT auto-contact the vendor directly — always routes through internal coordinator.
    """
    ticket_id = f"VND-{uuid.uuid4().hex[:6].upper()}"
    ticket = {
        "ticket_id": ticket_id,
        "vendor_name": vendor_name,
        "issue_type": issue_type,
        "location": location,
        "description": description,
        "status": "open",
    }
    print(f"  [VENDOR TICKET] {json.dumps(ticket)}")
    return {"created": True, "ticket_id": ticket_id}


def notify_vendor_lead(coordinator_id: str, request_id: str, message: str) -> dict:
    """
    Page the internal vendor coordinator.
    Does NOT notify the external vendor directly.
    """
    vendors = _load("vendors.json")
    coordinator = vendors["coordinators"].get(coordinator_id)

    if not coordinator:
        return {
            "isError": True,
            "reason": "COORDINATOR_NOT_FOUND",
            "guidance": f"coordinator_id={coordinator_id} not found. Check vendor manifest for coordinator_id.",
        }

    print(f"  [VENDOR LEAD → {coordinator['channel']}] {coordinator['name']}: {message}")
    return {
        "notified": True,
        "coordinator_name": coordinator["name"],
        "channel": coordinator["channel"],
    }


TOOL_DEFINITIONS = [
    {
        "name": "read_vendor_manifest",
        "description": (
            "Return vendor schedule, contact, and dock assignment. "
            "Does NOT access contract or payment data. "
            "Search by type (catering, booth_setup, av_equipment, delivery) or name."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "vendor_query": {"type": "string", "description": "Vendor name or type"},
            },
            "required": ["vendor_query"],
        },
    },
    {
        "name": "create_vendor_ticket",
        "description": (
            "Create a ticket with vendor name, issue type, and location. "
            "Does NOT contact the vendor directly — routes through internal coordinator."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "vendor_name": {"type": "string"},
                "issue_type": {"type": "string", "enum": ["DELIVERY_DELAY", "POWER_OUTAGE", "ACCESS_ISSUE", "CATERING", "OTHER"]},
                "location": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["vendor_name", "issue_type", "location", "description"],
        },
    },
    {
        "name": "notify_vendor_lead",
        "description": (
            "Page the internal vendor coordinator. "
            "Does NOT notify the external vendor directly. "
            "coordinator_id comes from read_vendor_manifest result."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "coordinator_id": {"type": "string"},
                "request_id": {"type": "string"},
                "message": {"type": "string"},
            },
            "required": ["coordinator_id", "request_id", "message"],
        },
    },
]

TOOL_HANDLERS = {
    "read_vendor_manifest": lambda inp: read_vendor_manifest(inp["vendor_query"]),
    "create_vendor_ticket": lambda inp: create_vendor_ticket(
        inp["vendor_name"], inp["issue_type"], inp["location"], inp["description"]
    ),
    "notify_vendor_lead": lambda inp: notify_vendor_lead(
        inp["coordinator_id"], inp["request_id"], inp["message"]
    ),
}
