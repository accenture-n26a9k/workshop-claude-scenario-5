from __future__ import annotations

import uuid
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class Category(str, Enum):
    FAQ = "FAQ"
    ROOM_OPS = "ROOM_OPS"
    VIP = "VIP"
    SAFETY = "SAFETY"
    COC = "COC"
    VENDOR = "VENDOR"
    PRESS = "PRESS"
    UNKNOWN = "UNKNOWN"


class SLATier(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    ALWAYS_HUMAN = "ALWAYS_HUMAN"


class RoutingDecision(str, Enum):
    AUTO_RESOLVE = "AUTO_RESOLVE"
    ROUTE = "ROUTE"
    ESCALATE = "ESCALATE"
    HARD_PAGE = "HARD_PAGE"


class ImpactTier(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Classification(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: Category
    confidence: float = Field(ge=0.0, le=1.0)
    impact_tier: Optional[ImpactTier] = None
    sla_tier: SLATier
    routing_decision: RoutingDecision
    reasoning: str
    estimated_dollar_impact: Optional[float] = None
    adversarial_flag: bool = False
    adversarial_type: Optional[str] = None

    @model_validator(mode="after")
    def impact_tier_required_for_vip(self) -> Classification:
        if self.category == Category.VIP and self.impact_tier is None:
            raise ValueError("impact_tier is required when category is VIP")
        return self


class EnrichedRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    raw_message: str
    sender_id: Optional[str] = None
    sender_channel: str = "ops"
    sender_history_count: int = 0
    classification: Optional[Classification] = None
    attempt_count: int = 0
    error_type: Optional[str] = None
    latency_ms: Optional[float] = None


class SpecialistTask(BaseModel):
    """Self-contained task packet passed to each specialist. No coordinator context inherited."""
    request_id: str
    raw_message: str
    category: Category
    confidence: float
    impact_tier: Optional[ImpactTier] = None
    sla_tier: SLATier
    routing_decision: RoutingDecision
    sender_id: Optional[str] = None
    sender_channel: str = "ops"
    sender_history_count: int = 0
    reasoning: str
    adversarial_flag: bool = False


class SpecialistOutcome(BaseModel):
    request_id: str
    specialist: str
    action_taken: str
    reply_sent: bool = False
    reply_text: Optional[str] = None
    ticket_id: Optional[str] = None
    human_notified: bool = False
    notes: Optional[str] = None
