"""
Attendee Services tools.
All tools are read-only except send_reply, which sends to the origin channel only.
"""

from __future__ import annotations

import json
from pathlib import Path

_DATA = Path(__file__).parents[3] / "data"


def _load(filename: str) -> dict:
    return json.loads((_DATA / filename).read_text())


def lookup_faq(query: str) -> dict:
    """
    Search the curated FAQ knowledge base.
    Does NOT generate answers — only returns from the KB.
    Returns the best matching entry or isError if no match found.
    """
    kb = _load("faq_kb.json")
    query_lower = query.lower()

    best_match = None
    best_score = 0

    for entry in kb["entries"]:
        score = sum(1 for tag in entry["tags"] if tag in query_lower)
        if entry["question"].lower() in query_lower:
            score += 3
        if score > best_score:
            best_score = score
            best_match = entry

    if best_match and best_score > 0:
        return {
            "found": True,
            "id": best_match["id"],
            "answer": best_match["answer"],
            "source": f"faq_kb/{best_match['id']}",
        }

    return {
        "isError": True,
        "reason": "NO_MATCH",
        "guidance": "No FAQ entry matched this query. Do not generate an answer — escalate to human ops.",
    }


def read_attendee_record(sender_id: str) -> dict:
    """
    Read registration, dietary, and session data for an attendee.
    Does NOT write or modify any record.
    Returns isError if sender_id is unknown.
    """
    attendees = _load("attendees.json")

    record = attendees["attendees"].get(sender_id)
    if not record:
        return {
            "isError": True,
            "reason": "ATTENDEE_NOT_FOUND",
            "guidance": f"No attendee record for sender_id={sender_id}. Ask them to visit the registration desk.",
        }

    return {
        "found": True,
        "badge_id": record["badge_id"],
        "name": record["name"],
        "tier": record["tier"],
        "dietary": record["dietary"],
        "session_count": len(record["sessions"]),
    }


def read_schedule(session_query: str) -> dict:
    """
    Return current session schedule with room assignments.
    Does NOT access speaker-only schedule data.
    """
    schedule = {
        "keynote-day1": {"title": "Opening Keynote", "room": "Hall A", "time": "09:00"},
        "keynote-day2": {"title": "Closing Keynote", "room": "Hall A", "time": "09:30"},
        "workshop-r21-1030": {"title": "Hands-on Workshop: AI Tooling", "room": "Room 21", "time": "10:30"},
        "talk-hallb-1400": {"title": "Panel: Future of Data", "room": "Hall B", "time": "14:00"},
        "talk-room7-1130": {"title": "Deep Dive: Distributed Systems", "room": "Room 7", "time": "11:30"},
    }

    query_lower = session_query.lower()
    results = []
    for session_id, details in schedule.items():
        if (
            query_lower in details["title"].lower()
            or query_lower in details["room"].lower()
            or query_lower in session_id
        ):
            results.append({"session_id": session_id, **details})

    if results:
        return {"found": True, "sessions": results}

    return {
        "isError": True,
        "reason": "NO_SESSIONS_FOUND",
        "guidance": f"No sessions matched '{session_query}'. Try the full schedule at sched.conference.example.com",
    }


def send_reply(sender_channel: str, message: str) -> dict:
    """
    Post an auto-reply to the attendee's originating channel.
    Does NOT send to any channel other than origin.
    sender_channel must match the channel from the original request.
    """
    print(f"  [REPLY → {sender_channel}]: {message}")
    return {"sent": True, "channel": sender_channel}


TOOL_DEFINITIONS = [
    {
        "name": "lookup_faq",
        "description": (
            "Search the curated FAQ knowledge base for known questions. "
            "Use for: badge pickup, wifi, coffee, restrooms, schedule, maps, nursing room. "
            "Does NOT generate answers — returns from the KB only. "
            "If no match: return isError and do not attempt to answer from training data."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The attendee's question or keywords"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "read_attendee_record",
        "description": (
            "Read registration, dietary, and session data for a known attendee. "
            "Does NOT write or modify any record. "
            "Use sender_id from the request context."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sender_id": {"type": "string", "description": "Attendee ID from request context"},
            },
            "required": ["sender_id"],
        },
    },
    {
        "name": "read_schedule",
        "description": (
            "Return current session schedule with room and time. "
            "Does NOT return speaker-only data. "
            "Use for questions about session times, rooms, or the keynote."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "session_query": {"type": "string", "description": "Session title, room, or keyword"},
            },
            "required": ["session_query"],
        },
    },
    {
        "name": "send_reply",
        "description": (
            "Post an auto-reply to the attendee. "
            "ONLY sends to the channel from the original request. "
            "Do not call this until you have a confirmed answer from lookup_faq or read_schedule."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sender_channel": {"type": "string", "description": "Origin channel (from request context)"},
                "message": {"type": "string", "description": "Reply message text"},
            },
            "required": ["sender_channel", "message"],
        },
    },
]

TOOL_HANDLERS = {
    "lookup_faq": lambda inp: lookup_faq(inp["query"]),
    "read_attendee_record": lambda inp: read_attendee_record(inp["sender_id"]),
    "read_schedule": lambda inp: read_schedule(inp["session_query"]),
    "send_reply": lambda inp: send_reply(inp["sender_channel"], inp["message"]),
}
