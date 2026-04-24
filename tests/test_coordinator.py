"""
Coordinator agent tests.
Tests routing logic, escalation rules, and safety brake integration.
Mocks the classifier so tests are deterministic.
"""

from unittest.mock import patch

import pytest

from src.schemas.classification import (
    Category, Classification, ImpactTier, RoutingDecision, SLATier
)


def _make_classification(**kwargs) -> dict:
    defaults = {
        "category": "FAQ",
        "confidence": 0.90,
        "sla_tier": "LOW",
        "routing_decision": "AUTO_RESOLVE",
        "reasoning": "test",
        "adversarial_flag": False,
    }
    defaults.update(kwargs)
    return defaults


class TestEscalationRules:
    """Tests _apply_escalation_rules in coordinator/agent.py"""

    def _apply(self, **kwargs) -> Classification:
        from src.coordinator.agent import _apply_escalation_rules
        raw = _make_classification(**kwargs)
        c = Classification(request_id="test", **raw)
        return _apply_escalation_rules(c)

    def test_safety_always_hard_page(self):
        result = self._apply(category="SAFETY", routing_decision="ROUTE", confidence=0.99)
        assert result.routing_decision == RoutingDecision.HARD_PAGE

    def test_coc_always_escalate(self):
        result = self._apply(category="COC", routing_decision="ROUTE", confidence=0.99)
        assert result.routing_decision == RoutingDecision.ESCALATE

    def test_press_always_escalate(self):
        result = self._apply(category="PRESS", routing_decision="ROUTE", confidence=0.99)
        assert result.routing_decision == RoutingDecision.ESCALATE

    def test_adversarial_escalates(self):
        result = self._apply(
            category="FAQ",
            routing_decision="AUTO_RESOLVE",
            adversarial_flag=True,
            confidence=0.90,
        )
        assert result.routing_decision == RoutingDecision.ESCALATE

    def test_low_confidence_non_faq_escalates(self):
        result = self._apply(
            category="ROOM_OPS",
            routing_decision="ROUTE",
            confidence=0.50,
        )
        assert result.routing_decision == RoutingDecision.ESCALATE

    def test_low_confidence_faq_does_not_escalate(self):
        """Low-confidence FAQ should not be escalated by the rule."""
        result = self._apply(
            category="FAQ",
            routing_decision="AUTO_RESOLVE",
            confidence=0.50,
        )
        assert result.routing_decision == RoutingDecision.AUTO_RESOLVE

    def test_vip_high_impact_uncertain_escalates(self):
        result = self._apply(
            category="VIP",
            routing_decision="ROUTE",
            confidence=0.70,
            impact_tier="HIGH",
        )
        assert result.routing_decision == RoutingDecision.ESCALATE

    def test_vip_high_impact_confident_routes(self):
        result = self._apply(
            category="VIP",
            routing_decision="ROUTE",
            confidence=0.90,
            impact_tier="HIGH",
        )
        # confidence >= 0.85 with HIGH impact → stays as ROUTE
        assert result.routing_decision == RoutingDecision.ROUTE

    def test_high_dollar_impact_escalates(self):
        result = self._apply(
            category="VENDOR",
            routing_decision="ROUTE",
            confidence=0.88,
            estimated_dollar_impact=6000.0,
        )
        assert result.routing_decision == RoutingDecision.ESCALATE

    def test_faq_high_confidence_auto_resolves(self):
        result = self._apply(
            category="FAQ",
            routing_decision="AUTO_RESOLVE",
            confidence=0.92,
        )
        assert result.routing_decision == RoutingDecision.AUTO_RESOLVE


class TestSafetyCutoff:
    """Safety keywords should be caught before the classifier is ever called."""

    def test_safety_keyword_bypasses_classifier(self):
        from src.coordinator.agent import process

        with patch("src.coordinator.agent.validate_with_retry") as mock_validate:
            outcome = process("there's a fire alarm going off in Hall B", "test-safety-001")

        mock_validate.assert_not_called()
        assert outcome["routing_decision"] == "HARD_PAGE"
        assert "fire" in outcome["matched_keywords"]

    def test_safe_message_calls_classifier(self):
        from src.coordinator.agent import process

        valid_raw = _make_classification()
        valid_classification = Classification(request_id="x", **valid_raw)

        with patch("src.coordinator.agent.validate_with_retry", return_value=(valid_classification, 1, None)):
            with patch("src.coordinator.agent._route", return_value={"action": "ok"}):
                outcome = process("where is badge pickup?", "test-safe-001")

        assert outcome["routing_decision"] != "HARD_PAGE"
