"""
Demo injector: fires the 15-message sequence with simulated timing.
Watch the ops-lead dashboard in a second terminal while this runs.

Usage:
    python demo/injector.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.coordinator.agent import process

_MESSAGES = json.loads((Path(__file__).parent / "messages.json").read_text())["sequence"]

_QUEUE: list[dict] = []
_STATS = {
    "auto_resolved": 0,
    "routed": 0,
    "escalated": 0,
    "flagged": 0,
    "safety_pages": 0,
    "coc_discreet": 0,
    "press_held": 0,
    "ops_queue": [],
}


def _update_stats(outcome: dict) -> None:
    routing = outcome.get("routing_decision", "ROUTE")
    category = outcome.get("category", "UNKNOWN")

    if routing == "HARD_PAGE":
        _STATS["safety_pages"] += 1
    elif routing == "AUTO_RESOLVE":
        _STATS["auto_resolved"] += 1
    elif routing == "ESCALATE":
        if outcome.get("adversarial_flag"):
            _STATS["flagged"] += 1
        elif category == "COC":
            _STATS["coc_discreet"] += 1
        elif category == "PRESS":
            _STATS["press_held"] += 1
        else:
            _STATS["escalated"] += 1
            _QUEUE.append(outcome)
    elif routing == "ROUTE":
        _STATS["routed"] += 1

    (Path("logs") / "demo_state.json").parent.mkdir(parents=True, exist_ok=True)
    (Path("logs") / "demo_state.json").write_text(json.dumps({
        "stats": {k: v for k, v in _STATS.items() if k != "ops_queue"},
        "ops_queue_size": len(_QUEUE),
        "ops_queue": _QUEUE[-5:],
    }, indent=2))


def main() -> None:
    print("\n" + "═" * 60)
    print("  THE STAGE MANAGER — Live Demo")
    print("  15 messages, simulated conference ops scenario")
    print("═" * 60 + "\n")

    for item in _MESSAGES:
        t = item["t"]
        msg = item["message"]
        expected = item["expected"]

        print(f"T+{t:02d}s  \"{msg}\"")
        print(f"       expected: {expected}")

        outcome = process(msg)

        routing = outcome.get("routing_decision", "?")
        category = outcome.get("category", "?")
        confidence = outcome.get("confidence", 0)
        adv = " 🚩 ADVERSARIAL" if outcome.get("adversarial_flag") else ""
        print(f"       → {category}/{routing} (conf={confidence:.2f}, {outcome.get('latency_ms', 0)}ms){adv}\n")

        _update_stats(outcome)

        # Simulate ~1s between messages (faster for demo)
        if t < len(_MESSAGES) - 1:
            time.sleep(0.5)

    print("\n" + "═" * 60)
    print(f"  Ops Lead Queue : {len(_QUEUE)} items")
    print(f"  Auto-resolved  : {_STATS['auto_resolved']}")
    print(f"  Routed         : {_STATS['routed']}")
    print(f"  Escalated      : {_STATS['escalated']}")
    print(f"  Flagged (adv)  : {_STATS['flagged']}")
    print(f"  Safety pages   : {_STATS['safety_pages']}")
    print(f"  CoC discreet   : {_STATS['coc_discreet']}")
    print(f"  Press held     : {_STATS['press_held']}")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()
