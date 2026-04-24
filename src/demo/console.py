"""
Interactive console for the coordinator agent.
Type a message, see the routing decision, category, confidence, and
specialist output. Empty line or Ctrl-C/Ctrl-D to exit.

Usage:
    python src/demo/console.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parents[2]))

from src.coordinator.agent import process


_COLORS = {
    "HARD_PAGE": "\033[91m",    # red
    "ESCALATE": "\033[93m",     # yellow
    "ROUTE": "\033[94m",        # blue
    "AUTO_RESOLVE": "\033[92m", # green
}
_RESET = "\033[0m"
_DIM = "\033[2m"
_BOLD = "\033[1m"


def _fmt(key: str) -> str:
    color = _COLORS.get(str(key), "")
    return f"{color}{_BOLD}{key}{_RESET}"


def _render(outcome: dict) -> None:
    decision = str(outcome.get("routing_decision", "?"))
    category = str(outcome.get("category", "?"))
    confidence = outcome.get("confidence")
    latency = outcome.get("latency_ms")
    reasoning = outcome.get("reasoning")
    adversarial = outcome.get("adversarial_flag")
    specialist = outcome.get("specialist_result")

    header = f"  {_fmt(decision)}  →  {category}"
    if confidence is not None:
        header += f"  (conf {confidence:.2f})"
    if latency is not None:
        header += f"  {_DIM}[{latency} ms]{_RESET}"
    print(header)

    if adversarial:
        adv_type = outcome.get("adversarial_type") or "unspecified"
        print(f"  {_COLORS['ESCALATE']}⚠  adversarial flag: {adv_type}{_RESET}")

    if reasoning:
        print(f"  {_DIM}reasoning:{_RESET} {reasoning}")

    if specialist:
        snippet = json.dumps(specialist, default=str)
        if len(snippet) > 240:
            snippet = snippet[:240] + "…"
        print(f"  {_DIM}specialist:{_RESET} {snippet}")


def main() -> int:
    print("─" * 60)
    print("  Coordinator console — type a message, Enter to send.")
    print("  Empty line or Ctrl-C exits.")
    print("─" * 60)

    while True:
        try:
            msg = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not msg:
            return 0

        try:
            outcome = process(msg)
        except Exception as err:
            print(f"  {_COLORS['HARD_PAGE']}error:{_RESET} {err}")
            continue

        _render(outcome)


if __name__ == "__main__":
    sys.exit(main())
