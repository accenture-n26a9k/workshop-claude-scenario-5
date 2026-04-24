"""
Client factory. Uses AnthropicBedrock when AWS_BEARER_TOKEN_BEDROCK is set,
falls back to standard Anthropic client for ANTHROPIC_API_KEY.

AnthropicBedrock(api_key=bearer_token) uses the token directly as
Authorization: Bearer — no SigV4 signing needed.
"""

from __future__ import annotations

import os

import anthropic

# eu-north-1 cross-region inference profile IDs
SONNET_MODEL = "eu.anthropic.claude-3-5-sonnet-20241022-v2:0"
HAIKU_MODEL = "eu.anthropic.claude-3-haiku-20240307-v1:0"
AWS_REGION = "eu-north-1"


def _make_bedrock_client() -> anthropic.AnthropicBedrock:
    bearer_token = os.environ["AWS_BEARER_TOKEN_BEDROCK"]
    return anthropic.AnthropicBedrock(
        aws_region=AWS_REGION,
        api_key=bearer_token,
    )


def make_client() -> anthropic.Anthropic | anthropic.AnthropicBedrock:
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
        return _make_bedrock_client()
    return anthropic.Anthropic()


def coordinator_model() -> str:
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
        return SONNET_MODEL
    return "claude-sonnet-4-6"


def specialist_model() -> str:
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
        return HAIKU_MODEL
    return "claude-haiku-4-5-20251001"
