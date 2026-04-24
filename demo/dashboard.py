"""
Ops-lead dashboard: polls logs/demo_state.json and renders live queue state.
Run in a second terminal while demo/injector.py is running.

Usage:
    python demo/dashboard.py
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

_STATE_FILE = Path("logs/demo_state.json")
_REFRESH_INTERVAL = 0.5


def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _render(state: dict) -> None:
    stats = state.get("stats", {})
    queue = state.get("ops_queue", [])
    queue_size = state.get("ops_queue_size", 0)

    _clear()
    print("╔══════════════════════════════════════════════════╗")
    print("║     THE STAGE MANAGER — Ops Lead Dashboard       ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  Queue needing attention : {queue_size:<4}                   ║")
    print(f"║  Auto-resolved           : {stats.get('auto_resolved', 0):<4}                   ║")
    print(f"║  Routed to specialist    : {stats.get('routed', 0):<4}                   ║")
    print(f"║  Escalated to human      : {stats.get('escalated', 0):<4}                   ║")
    print(f"║  Adversarial flagged     : {stats.get('flagged', 0):<4}                   ║")
    print(f"║  Safety pages            : {stats.get('safety_pages', 0):<4}  🚨             ║")
    print(f"║  CoC discreet path       : {stats.get('coc_discreet', 0):<4}                   ║")
    print(f"║  Press held for human    : {stats.get('press_held', 0):<4}                   ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║  Items in your queue:                            ║")

    if not queue:
        print("║    (nothing yet)                                 ║")
    else:
        for item in queue[-5:]:
            cat = item.get("category", "?")[:10]
            sla = item.get("sla_tier", "?")[:8]
            req = item.get("request_id", "")[:8]
            line = f"    [{req}] {cat} / SLA:{sla}"
            print(f"║  {line:<48}║")

    print("╚══════════════════════════════════════════════════╝")
    print(f"\n  Refreshing every {_REFRESH_INTERVAL}s — Ctrl+C to exit")


def main() -> None:
    print("Waiting for demo to start (watching logs/demo_state.json)...")
    while True:
        try:
            if _STATE_FILE.exists():
                state = json.loads(_STATE_FILE.read_text())
                _render(state)
            time.sleep(_REFRESH_INTERVAL)
        except KeyboardInterrupt:
            print("\nDashboard stopped.")
            break
        except Exception as exc:
            print(f"Error reading state: {exc}")
            time.sleep(1)


if __name__ == "__main__":
    main()
