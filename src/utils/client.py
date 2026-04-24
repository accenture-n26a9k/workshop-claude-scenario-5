"""
Client factory. Uses AnthropicBedrock when USE_BEDROCK=1 is set,
relying on boto3's default credential chain (AWS SSO, env vars, instance profile).
Falls back to standard Anthropic client for ANTHROPIC_API_KEY.

To authenticate via AWS SSO browser login:
    aws sso login --profile <your-profile>
    export AWS_PROFILE=<your-profile>
    export USE_BEDROCK=1
"""

from __future__ import annotations

import os

import anthropic

# eu-north-1 cross-region inference profile IDs
SONNET_MODEL = "eu.anthropic.claude-3-5-sonnet-20241022-v2:0"
HAIKU_MODEL = "eu.anthropic.claude-3-haiku-20240307-v1:0"
AWS_REGION = "eu-north-1"


def _use_bedrock() -> bool:
    return os.environ.get("USE_BEDROCK", "").strip() == "1"


def _make_bedrock_client() -> anthropic.AnthropicBedrock:
    # No explicit credentials — boto3 resolves them from the credential chain:
    # AWS_PROFILE / AWS SSO cached token, env vars, instance profile, etc.
    return anthropic.AnthropicBedrock(aws_region=AWS_REGION)


def make_client() -> anthropic.Anthropic | anthropic.AnthropicBedrock:
    if _use_bedrock():
        return _make_bedrock_client()
    return anthropic.Anthropic()


def coordinator_model() -> str:
    if _use_bedrock():
        return SONNET_MODEL
    return "claude-sonnet-4-6"


def specialist_model() -> str:
    if _use_bedrock():
        return HAIKU_MODEL
    return "claude-haiku-4-5-20251001"
