"""
Client factory. Selects auth in this order:
  1. AWS_BEARER_TOKEN_BEDROCK → AnthropicBedrock with bearer-token Authorization.
  2. ANTHROPIC_API_KEY        → direct anthropic.Anthropic() client.
  3. Fallback                 → AnthropicBedrock via AWS SSO profile (default "bootcamp").

Region and model IDs default to us-west-2 (Oregon) with `us.` cross-region
inference profiles. Override via AWS_REGION / AWS_PROFILE /
BEDROCK_SONNET_MODEL / BEDROCK_HAIKU_MODEL.
"""

from __future__ import annotations

import os

import anthropic

AWS_REGION = os.environ.get("AWS_REGION", "us-west-2")
AWS_PROFILE = os.environ.get("AWS_PROFILE", "bootcamp")
SONNET_MODEL = os.environ.get(
    "BEDROCK_SONNET_MODEL", "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
)
HAIKU_MODEL = os.environ.get(
    "BEDROCK_HAIKU_MODEL", "us.anthropic.claude-haiku-4-5-20251001-v1:0"
)


def _bearer_token() -> str | None:
    token = os.environ.get("AWS_BEARER_TOKEN_BEDROCK", "").strip()
    if not token or token.startswith("{"):
        return None
    return token


def _use_bedrock() -> bool:
    return not os.environ.get("ANTHROPIC_API_KEY") or _bearer_token() is not None


def make_client() -> anthropic.Anthropic | anthropic.AnthropicBedrock:
    token = _bearer_token()
    if token:
        return anthropic.AnthropicBedrock(aws_region=AWS_REGION, api_key=token)

    if os.environ.get("ANTHROPIC_API_KEY"):
        return anthropic.Anthropic()

    return anthropic.AnthropicBedrock(aws_region=AWS_REGION, aws_profile=AWS_PROFILE)


def coordinator_model() -> str:
    return SONNET_MODEL if _use_bedrock() else "claude-sonnet-4-6"


def specialist_model() -> str:
    return HAIKU_MODEL if _use_bedrock() else "claude-haiku-4-5-20251001"
