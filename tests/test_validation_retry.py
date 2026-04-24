"""
Validation-retry loop tests.
Tests schema validation and fallback escalation behaviour.
No API calls — mocks the classifier.
"""

import uuid
from unittest.mock import patch

import pytest

from src.coordinator.validator import validate_with_retry
from src.schemas.classification import Category, Classification, RoutingDecision, SLATier


class TestValidateWithRetry:
    def test_valid_classification_first_attempt(self):
        valid_output = {
            "category": "FAQ",
            "confidence": 0.92,
            "sla_tier": "LOW",
            "routing_decision": "AUTO_RESOLVE",
            "reasoning": "Standard FAQ about badge location",
            "adversarial_flag": False,
        }
        with patch("src.coordinator.validator.classify", return_value=valid_output):
            classification, attempts, error_type = validate_with_retry(
                "where is badge pickup?", "req-001"
            )

        assert classification.category == Category.FAQ
        assert classification.routing_decision == RoutingDecision.AUTO_RESOLVE
        assert attempts == 1
        assert error_type is None

    def test_retry_on_missing_impact_tier_for_vip(self):
        """VIP category requires impact_tier — should trigger retry."""
        invalid_output = {
            "category": "VIP",
            "confidence": 0.88,
            "sla_tier": "HIGH",
            "routing_decision": "ESCALATE",
            "reasoning": "VIP dietary issue",
            "adversarial_flag": False,
            # missing impact_tier
        }
        valid_output = {
            "category": "VIP",
            "confidence": 0.88,
            "impact_tier": "HIGH",
            "sla_tier": "HIGH",
            "routing_decision": "ESCALATE",
            "reasoning": "VIP dietary issue",
            "adversarial_flag": False,
        }
        call_count = 0

        def mock_classify(message, validation_error=None):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return invalid_output
            return valid_output

        with patch("src.coordinator.validator.classify", side_effect=mock_classify):
            classification, attempts, error_type = validate_with_retry(
                "my dietary need is wrong, I'm a VIP", "req-002"
            )

        assert classification.category == Category.VIP
        assert classification.impact_tier is not None
        assert attempts == 2
        assert error_type is None

    def test_fallback_after_max_retries(self):
        """After 3 failed attempts, returns safe ESCALATE fallback."""
        bad_output = {
            "category": "VIP",
            "confidence": 0.88,
            "sla_tier": "HIGH",
            "routing_decision": "ESCALATE",
            "reasoning": "test",
            "adversarial_flag": False,
            # always missing impact_tier — will always fail
        }
        with patch("src.coordinator.validator.classify", return_value=bad_output):
            classification, attempts, error_type = validate_with_retry(
                "VIP request", "req-003"
            )

        assert attempts == 3
        assert error_type == "validation_failure"
        assert classification.routing_decision == RoutingDecision.ESCALATE
        assert classification.category == Category.UNKNOWN
        assert classification.confidence == 0.0

    def test_request_id_is_set(self):
        valid_output = {
            "category": "FAQ",
            "confidence": 0.85,
            "sla_tier": "LOW",
            "routing_decision": "AUTO_RESOLVE",
            "reasoning": "FAQ",
            "adversarial_flag": False,
        }
        req_id = str(uuid.uuid4())
        with patch("src.coordinator.validator.classify", return_value=valid_output):
            classification, _, _ = validate_with_retry("wifi password?", req_id)

        assert classification.request_id == req_id

    def test_confidence_bounds_validation(self):
        """Confidence outside 0–1 range should fail validation and retry."""
        invalid_output = {
            "category": "FAQ",
            "confidence": 1.5,  # invalid
            "sla_tier": "LOW",
            "routing_decision": "AUTO_RESOLVE",
            "reasoning": "FAQ",
            "adversarial_flag": False,
        }
        valid_output = {**invalid_output, "confidence": 0.85}

        call_count = 0

        def mock_classify(message, validation_error=None):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return invalid_output
            return valid_output

        with patch("src.coordinator.validator.classify", side_effect=mock_classify):
            classification, attempts, error_type = validate_with_retry("where is coffee?", "req-004")

        assert classification.confidence <= 1.0
        assert attempts == 2
