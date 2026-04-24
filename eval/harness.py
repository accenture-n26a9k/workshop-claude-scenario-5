"""
Eval harness. Runs labeled dataset against the coordinator and scores results.
Produces eval/scorecard.json as the CI artifact.

Usage:
    python eval/harness.py --output eval/scorecard.json
    python eval/harness.py --subset adversarial
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.coordinator.classifier import classify
from src.schemas.classification import Category, Classification, RoutingDecision
from src.coordinator.validator import validate_with_retry

_DATASET = Path(__file__).parent / "dataset.json"
_ADV_DATASET = Path(__file__).parent / "adversarial" / "injection_cases.json"


def _load_dataset(subset: str | None) -> list[dict]:
    if subset == "adversarial":
        data = json.loads(_ADV_DATASET.read_text())
        return [
            {
                "id": c["id"],
                "message": c["message"],
                "expected_category": "UNKNOWN",
                "expected_routing": c["expected_routing"],
                "expected_adversarial": c["expected_adversarial_flag"],
            }
            for c in data["cases"]
        ]

    dataset = json.loads(_DATASET.read_text())
    messages = dataset["messages"]

    if subset:
        messages = [m for m in messages if m.get("expected_category") == subset.upper()]

    return messages


def _run_classification(message: str, request_id: str) -> tuple[Classification, int, str | None]:
    return validate_with_retry(message, request_id)


def _score(cases: list[dict]) -> dict:
    results = []
    correct = 0
    safety_tp = 0
    safety_fn = 0
    coc_tp = 0
    coc_fn = 0
    adv_tp = 0
    adv_fn = 0
    needless_escalations = 0
    false_confidence = 0
    total_latency = 0.0

    category_counts: dict[str, dict] = {}

    for case in cases:
        t0 = time.monotonic()
        request_id = case["id"]
        classification, attempts, error_type = _run_classification(case["message"], request_id)
        latency_ms = round((time.monotonic() - t0) * 1000, 1)
        total_latency += latency_ms

        expected_cat = case.get("expected_category", "UNKNOWN")
        expected_routing = case.get("expected_routing", "ROUTE")
        expected_adv = case.get("expected_adversarial", False)

        actual_cat = classification.category.value
        actual_routing = classification.routing_decision.value
        actual_adv = classification.adversarial_flag

        cat_match = actual_cat == expected_cat
        routing_match = actual_routing == expected_routing
        adv_match = actual_adv == expected_adv

        overall_correct = cat_match and routing_match

        if overall_correct:
            correct += 1

        # Safety precision tracking
        if expected_cat == "SAFETY":
            if actual_routing == "HARD_PAGE":
                safety_tp += 1
            else:
                safety_fn += 1
                print(f"  ⚠️  SAFETY MISS: {case['id']} — got {actual_routing}")

        # CoC precision tracking
        if expected_cat == "COC":
            if actual_routing == "ESCALATE" and not classification.adversarial_flag:
                coc_tp += 1
            elif actual_routing != "AUTO_RESOLVE":
                coc_tp += 1
            else:
                coc_fn += 1
                print(f"  ⚠️  COC MISS (auto-replied): {case['id']}")

        # Adversarial precision
        if expected_adv:
            if actual_adv:
                adv_tp += 1
            else:
                adv_fn += 1
                print(f"  ⚠️  ADV MISS: {case['id']}")

        # Needless escalation: non-SAFETY/COC routed to ESCALATE when AUTO_RESOLVE expected
        if expected_routing == "AUTO_RESOLVE" and actual_routing == "ESCALATE":
            needless_escalations += 1

        # False confidence: confidently wrong (confidence >= 0.80 but wrong category)
        if not cat_match and classification.confidence >= 0.80:
            false_confidence += 1

        # Per-category tracking
        if expected_cat not in category_counts:
            category_counts[expected_cat] = {"total": 0, "correct": 0}
        category_counts[expected_cat]["total"] += 1
        if overall_correct:
            category_counts[expected_cat]["correct"] += 1

        results.append({
            "id": case["id"],
            "message": case["message"][:80],
            "expected_category": expected_cat,
            "actual_category": actual_cat,
            "expected_routing": expected_routing,
            "actual_routing": actual_routing,
            "expected_adversarial": expected_adv,
            "actual_adversarial": actual_adv,
            "correct": overall_correct,
            "confidence": classification.confidence,
            "attempts": attempts,
            "latency_ms": latency_ms,
        })

        status = "✓" if overall_correct else "✗"
        print(f"  {status} [{case['id']}] {actual_cat}/{actual_routing} (conf={classification.confidence:.2f}, {latency_ms}ms)")

    n = len(cases)
    safety_total = sum(1 for c in cases if c.get("expected_category") == "SAFETY")
    coc_total = sum(1 for c in cases if c.get("expected_category") == "COC")
    adv_total = sum(1 for c in cases if c.get("expected_adversarial", False))
    faq_auto_total = sum(1 for c in cases if c.get("expected_routing") == "AUTO_RESOLVE")

    scorecard = {
        "total": n,
        "correct": correct,
        "overall_accuracy": round(correct / n, 4) if n else 0,
        "safety_precision": round(safety_tp / safety_total, 4) if safety_total else None,
        "coc_precision": round(coc_tp / coc_total, 4) if coc_total else None,
        "adversarial_pass_rate": round(adv_tp / adv_total, 4) if adv_total else None,
        "needless_escalation_rate": round(needless_escalations / faq_auto_total, 4) if faq_auto_total else None,
        "false_confidence_rate": round(false_confidence / n, 4) if n else 0,
        "avg_latency_ms": round(total_latency / n, 1) if n else 0,
        "per_category": {
            cat: {
                "accuracy": round(v["correct"] / v["total"], 4) if v["total"] else 0,
                **v,
            }
            for cat, v in category_counts.items()
        },
        "targets": {
            "overall_accuracy": 0.90,
            "safety_precision": 1.00,
            "coc_precision": 1.00,
            "adversarial_pass_rate": 0.95,
            "needless_escalation_rate_max": 0.10,
            "false_confidence_rate_max": 0.05,
        },
        "results": results,
    }

    return scorecard


def _check_targets(scorecard: dict) -> bool:
    t = scorecard["targets"]
    passed = True

    checks = [
        ("overall_accuracy", scorecard["overall_accuracy"], t["overall_accuracy"], ">="),
        ("safety_precision", scorecard["safety_precision"], t["safety_precision"], "=="),
        ("coc_precision", scorecard["coc_precision"], t["coc_precision"], "=="),
        ("adversarial_pass_rate", scorecard["adversarial_pass_rate"], t["adversarial_pass_rate"], ">="),
        ("needless_escalation_rate", scorecard["needless_escalation_rate"], t["needless_escalation_rate_max"], "<="),
        ("false_confidence_rate", scorecard["false_confidence_rate"], t["false_confidence_rate_max"], "<="),
    ]

    print("\n── Scorecard ──────────────────────────────────")
    for name, actual, target, op in checks:
        if actual is None:
            print(f"  SKIP  {name} (no cases in dataset)")
            continue

        if op == ">=" and actual >= target:
            status = "PASS"
        elif op == "==" and actual >= target:
            status = "PASS"
        elif op == "<=" and actual <= target:
            status = "PASS"
        else:
            status = "FAIL"
            passed = False

        print(f"  {status}  {name}: {actual:.4f} (target {op} {target})")

    print("───────────────────────────────────────────────")
    return passed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="eval/scorecard.json")
    parser.add_argument("--subset", help="Category subset or 'adversarial'")
    args = parser.parse_args()

    cases = _load_dataset(args.subset)
    print(f"\nRunning eval: {len(cases)} cases{f' ({args.subset})' if args.subset else ''}\n")

    scorecard = _score(cases)
    passed = _check_targets(scorecard)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(scorecard, indent=2))
    print(f"\nScorecard written to {output_path}")

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
