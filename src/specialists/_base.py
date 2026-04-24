"""
Shared agent loop for all specialists.
Each specialist is a self-contained Claude call with its own tools and system prompt.
The PreToolUse hook runs before every write tool execution.
"""

from __future__ import annotations

import json

from ..hooks.pre_tool_use import pre_tool_use_hook
from ..schemas.classification import SpecialistTask
from ..utils.client import make_client, specialist_model

_client = make_client()

_WRITE_TOOLS = {
    "send_reply", "create_ops_ticket", "send_room_alert",
    "notify_concierge", "create_vip_ticket",
    "page_safety_lead", "create_coc_record",
    "create_vendor_ticket", "notify_vendor_lead",
}

MAX_ITERATIONS = 10


def run_specialist(
    task: SpecialistTask,
    system_prompt: str,
    tool_definitions: list[dict],
    tool_handlers: dict,
    specialist_name: str,
) -> dict:
    """
    Agentic loop for a specialist. Runs until end_turn or MAX_ITERATIONS.
    PreToolUse hook blocks write tools when safety keywords are present.
    """
    system_blocks = [
        {"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}
    ]
    messages = [{"role": "user", "content": _build_task_prompt(task)}]

    for _ in range(MAX_ITERATIONS):
        response = _client.messages.create(
            model=specialist_model(),
            max_tokens=1024,
            system=system_blocks,
            messages=messages,
            tools=tool_definitions,
        )

        if response.stop_reason == "end_turn":
            final_text = _extract_text(response)
            return {
                "specialist": specialist_name,
                "action_taken": "completed",
                "notes": final_text,
            }

        if response.stop_reason == "tool_use":
            tool_results = []
            blocked = False

            for block in response.content:
                if block.type != "tool_use":
                    continue

                # PreToolUse hook — hard stop for write tools
                if block.name in _WRITE_TOOLS:
                    hook_result = pre_tool_use_hook(
                        tool_name=block.name,
                        tool_input=block.input,
                        raw_message=task.raw_message,
                        request_id=task.request_id,
                        sender_id=task.sender_id,
                    )
                    if hook_result["blocked"]:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "is_error": True,
                            "content": json.dumps({
                                "isError": True,
                                "reason": "SAFETY_HOOK_BLOCKED",
                                "detail": hook_result["reason"],
                            }),
                        })
                        blocked = True
                        continue

                result = tool_handlers[block.name](block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            if blocked:
                return {
                    "specialist": specialist_name,
                    "action_taken": "BLOCKED_BY_SAFETY_HOOK",
                    "notes": "PreToolUse hook stopped execution. Safety lead has been paged.",
                }

        else:
            break

    return {
        "specialist": specialist_name,
        "action_taken": "max_iterations_reached",
        "notes": "Specialist loop hit MAX_ITERATIONS — escalating.",
    }


def _build_task_prompt(task: SpecialistTask) -> str:
    return (
        f"REQUEST ID: {task.request_id}\n"
        f"CATEGORY: {task.category} (confidence {task.confidence:.2f})\n"
        f"SLA TIER: {task.sla_tier}\n"
        f"SENDER: {task.sender_id or 'unknown'} via {task.sender_channel}\n"
        f"SENDER HISTORY: {task.sender_history_count} prior messages\n"
        f"ROUTING DECISION: {task.routing_decision}\n"
        f"COORDINATOR REASONING: {task.reasoning}\n"
        f"ADVERSARIAL FLAG: {task.adversarial_flag}\n\n"
        f"MESSAGE:\n{task.raw_message}"
    )


def _extract_text(response) -> str:
    texts = [b.text for b in response.content if hasattr(b, "text")]
    return " ".join(texts).strip()
