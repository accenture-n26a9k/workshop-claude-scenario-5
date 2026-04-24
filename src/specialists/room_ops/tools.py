"""
Room Ops tools.
Handles AV failures, facilities issues, room captain coordination.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

_DATA = Path(__file__).parents[3] / "data"


def _load(filename: str) -> dict:
    return json.loads((_DATA / filename).read_text())


def lookup_room_captain(room_name: str) -> dict:
    """
    Return the on-call captain for a given room right now.
    Does NOT return off-duty or unavailable captains.
    """
    venue = _load("venue_map.json")

    room = venue["rooms"].get(room_name)
    if not room:
        # Try partial match
        for r_name, r_data in venue["rooms"].items():
            if room_name.lower() in r_name.lower():
                room = r_data
                room_name = r_name
                break

    if not room:
        return {
            "isError": True,
            "reason": "ROOM_NOT_FOUND",
            "guidance": f"Room '{room_name}' not in venue map. Check spelling or use full room name (e.g. 'Hall A', 'Room 12').",
        }

    captain = venue["captains"].get(room["captain_id"])
    if not captain or not captain["available"]:
        return {
            "isError": True,
            "reason": "NO_CAPTAIN_AVAILABLE",
            "guidance": "No captain currently available for this room. Escalate to ops lead immediately.",
        }

    return {
        "found": True,
        "room": room_name,
        "captain_id": room["captain_id"],
        "captain_name": captain["name"],
        "captain_phone": captain["phone"],
        "captain_channel": captain["channel"],
    }


def read_av_status(room_name: str) -> dict:
    """
    Return current AV health for a room.
    Does NOT control or reset AV equipment.
    """
    venue = _load("venue_map.json")

    room = venue["rooms"].get(room_name)
    if not room:
        for r_name, r_data in venue["rooms"].items():
            if room_name.lower() in r_name.lower():
                room = r_data
                room_name = r_name
                break

    if not room:
        return {
            "isError": True,
            "reason": "ROOM_NOT_FOUND",
            "guidance": f"Room '{room_name}' not in venue map.",
        }

    return {
        "room": room_name,
        "av_system": room["av_system"],
        "av_status": room["av_status"],
    }


def create_ops_ticket(room_name: str, issue_type: str, description: str, priority: str, captain_id: str) -> dict:
    """
    Create a ticket in the ops system.
    Does NOT auto-assign without a captain_id — always call lookup_room_captain first.
    priority must be: P1 | P2 | P3
    """
    if not captain_id:
        return {
            "isError": True,
            "reason": "CAPTAIN_ID_REQUIRED",
            "guidance": "Call lookup_room_captain before create_ops_ticket. captain_id must be set.",
        }

    ticket_id = f"OPS-{uuid.uuid4().hex[:6].upper()}"
    ticket = {
        "ticket_id": ticket_id,
        "room": room_name,
        "issue_type": issue_type,
        "description": description,
        "priority": priority,
        "assigned_captain": captain_id,
        "status": "open",
    }
    print(f"  [TICKET CREATED] {json.dumps(ticket)}")
    return {"created": True, "ticket_id": ticket_id, "priority": priority}


def send_room_alert(captain_channel: str, room_name: str, message: str) -> dict:
    """
    Push an alert to a specific room captain's channel.
    Does NOT broadcast to all captains simultaneously.
    """
    print(f"  [ROOM ALERT → {captain_channel}] {room_name}: {message}")
    return {"sent": True, "channel": captain_channel}


TOOL_DEFINITIONS = [
    {
        "name": "lookup_room_captain",
        "description": (
            "Return the on-call captain for a given room. "
            "MUST be called before create_ops_ticket. "
            "Does NOT return off-duty captains. "
            "room_name examples: 'Hall A', 'Hall B', 'Room 7', 'Room 12', 'Expo Hall'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "room_name": {"type": "string", "description": "Full room name from venue map"},
            },
            "required": ["room_name"],
        },
    },
    {
        "name": "read_av_status",
        "description": (
            "Return current AV health for a room. "
            "Does NOT control or reset equipment. "
            "Use to confirm whether AV is already flagged as down before creating a ticket."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "room_name": {"type": "string"},
            },
            "required": ["room_name"],
        },
    },
    {
        "name": "create_ops_ticket",
        "description": (
            "Create a ticket with priority and captain assignment. "
            "captain_id is required — call lookup_room_captain first. "
            "priority: P1 (talk in progress / imminent), P2 (next session at risk), P3 (low urgency)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "room_name": {"type": "string"},
                "issue_type": {"type": "string", "enum": ["AV_FAILURE", "FACILITIES", "POWER", "OTHER"]},
                "description": {"type": "string"},
                "priority": {"type": "string", "enum": ["P1", "P2", "P3"]},
                "captain_id": {"type": "string", "description": "From lookup_room_captain result"},
            },
            "required": ["room_name", "issue_type", "description", "priority", "captain_id"],
        },
    },
    {
        "name": "send_room_alert",
        "description": (
            "Push an alert directly to a room captain's channel. "
            "Does NOT broadcast to all captains. "
            "Use captain_channel from lookup_room_captain result."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "captain_channel": {"type": "string"},
                "room_name": {"type": "string"},
                "message": {"type": "string"},
            },
            "required": ["captain_channel", "room_name", "message"],
        },
    },
]

TOOL_HANDLERS = {
    "lookup_room_captain": lambda inp: lookup_room_captain(inp["room_name"]),
    "read_av_status": lambda inp: read_av_status(inp["room_name"]),
    "create_ops_ticket": lambda inp: create_ops_ticket(
        inp["room_name"], inp["issue_type"], inp["description"], inp["priority"], inp["captain_id"]
    ),
    "send_room_alert": lambda inp: send_room_alert(
        inp["captain_channel"], inp["room_name"], inp["message"]
    ),
}
