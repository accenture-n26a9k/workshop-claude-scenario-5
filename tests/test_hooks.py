"""
Safety brake unit tests. Must be 100% pass — zero misses tolerated.
These tests are deterministic (no API calls).
"""

import pytest
from src.hooks.pre_tool_use import check_safety_keywords, pre_tool_use_hook


class TestCheckSafetyKeywords:
    def test_fire_keyword(self):
        matched, keywords = check_safety_keywords("there's a fire alarm going off in Hall B")
        assert matched is True
        assert "fire" in keywords
        assert "alarm" in keywords

    def test_medical_keyword(self):
        matched, keywords = check_safety_keywords("someone needs medical attention")
        assert matched is True
        assert "medical" in keywords

    def test_evacuation_keyword(self):
        matched, keywords = check_safety_keywords("evacuation alarm triggered on floor 3")
        assert matched is True
        assert "evacuation" in keywords

    def test_evac_abbreviation(self):
        matched, keywords = check_safety_keywords("evac needed in Hall A immediately")
        assert matched is True
        assert "evac" in keywords

    def test_weapon_keyword(self):
        matched, keywords = check_safety_keywords("I saw a weapon near the loading dock")
        assert matched is True
        assert "weapon" in keywords

    def test_unconscious_keyword(self):
        matched, keywords = check_safety_keywords("person is unconscious near the registration desk")
        assert matched is True
        assert "unconscious" in keywords

    def test_blood_keyword(self):
        matched, keywords = check_safety_keywords("there is blood on the floor in Room 21")
        assert matched is True
        assert "blood" in keywords

    def test_injury_keyword(self):
        matched, keywords = check_safety_keywords("there's been an injury in the expo hall")
        assert matched is True
        assert "injury" in keywords

    def test_emergency_keyword(self):
        matched, keywords = check_safety_keywords("emergency at the main stage")
        assert matched is True
        assert "emergency" in keywords

    def test_ambulance_keyword(self):
        matched, keywords = check_safety_keywords("we need an ambulance immediately")
        assert matched is True
        assert "ambulance" in keywords

    def test_no_match_faq(self):
        matched, keywords = check_safety_keywords("where is the coffee station?")
        assert matched is False
        assert keywords == []

    def test_no_match_av_issue(self):
        matched, keywords = check_safety_keywords("the projector in Hall B is dead")
        assert matched is False

    def test_no_match_vendor(self):
        matched, keywords = check_safety_keywords("the catering truck can't find the loading dock")
        assert matched is False

    def test_case_insensitive(self):
        matched, keywords = check_safety_keywords("FIRE ALARM IN HALL B")
        assert matched is True
        assert "fire" in keywords

    def test_embedded_keyword(self):
        matched, keywords = check_safety_keywords("there's a firealarm going off")
        assert matched is True  # "fire" is contained in "firealarm"

    def test_urgent_coffee_is_not_safety(self):
        """False urgency: URGENT coffee ran out is not a safety event."""
        matched, keywords = check_safety_keywords("URGENT URGENT: the coffee ran out in Hall A")
        assert matched is False

    def test_hurt_keyword(self):
        matched, keywords = check_safety_keywords("someone got hurt near the stage")
        assert matched is True
        assert "hurt" in keywords

    def test_assault_keyword(self):
        matched, keywords = check_safety_keywords("there was an assault in the parking lot")
        assert matched is True
        assert "assault" in keywords


class TestPreToolUseHook:
    def test_blocks_on_safety_keyword(self):
        result = pre_tool_use_hook(
            tool_name="send_reply",
            tool_input={"sender_channel": "ops", "message": "okay"},
            raw_message="there's a fire alarm going off in Hall B",
            request_id="test-001",
        )
        assert result["blocked"] is True
        assert result["action"] == "HARD_PAGE"
        assert "fire" in result["matched_keywords"]

    def test_allows_safe_message(self):
        result = pre_tool_use_hook(
            tool_name="send_reply",
            tool_input={"sender_channel": "ops", "message": "badge pickup is in Hall A"},
            raw_message="where is badge pickup?",
            request_id="test-002",
        )
        assert result["blocked"] is False

    def test_blocks_regardless_of_tool(self):
        """Hook fires on any write tool, not just send_reply."""
        for tool in ["create_ops_ticket", "notify_concierge", "create_coc_record"]:
            result = pre_tool_use_hook(
                tool_name=tool,
                tool_input={},
                raw_message="medical emergency at registration desk",
                request_id="test-003",
            )
            assert result["blocked"] is True, f"Expected block for tool={tool}"

    def test_block_includes_matched_keywords(self):
        result = pre_tool_use_hook(
            tool_name="create_ops_ticket",
            tool_input={},
            raw_message="evacuation alarm and medical emergency",
            request_id="test-004",
        )
        assert result["blocked"] is True
        assert "evacuation" in result["matched_keywords"]
        assert "medical" in result["matched_keywords"]
