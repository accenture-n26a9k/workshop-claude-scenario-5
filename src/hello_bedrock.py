import os
import time

from anthropic import AnthropicBedrock
from anthropic.types import ToolUseBlock, TextBlock

MODEL = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
SYSTEM_PROMPT = "You are a helpful assistant."

AWS_PROFILE = os.getenv("AWS_PROFILE", "bootcamp")
AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
client = AnthropicBedrock(
    aws_region=AWS_REGION,
    aws_profile=AWS_PROFILE,
)

def print_common_error_hints(error: Exception):
    err = str(error)
    print("\nCommon fixes:")
    if "NoCredentials" in err or "could not resolve credentials" in err:
        print("- Re-run browser login first, then run: aws login --profile bootcamp")
        print("- Run this script in the same terminal session used for login")
    elif "profile" in err.lower() and "bootcamp" in err.lower():
        print("- Run: aws login --profile bootcamp")
        print("- Or set AWS_PROFILE=bootcamp before running the script")
    elif "AccessDenied" in err or "access denied" in err.lower():
        print("- Confirm your EID has AWS bootcamp access/assignment")
    else:
        print("- Verify .venv is active")
        print("- Reinstall dependencies: python -m pip install -U \"anthropic[bedrock]\" \"botocore[crt]\"")


def call_messages_with_retry(**kwargs):
    last_error = None
    for attempt in range(1, 3):
        try:
            return client.messages.create(**kwargs)
        except Exception as e:
            last_error = e
            if attempt == 1:
                time.sleep(2)
    raise last_error


try:
    message = call_messages_with_retry(
        model=MODEL,
        max_tokens=256,
        messages=[{"role": "user", "content": "Hello, world"}],
    )
    print(message.content)
    print("Test 1 Cleared Successfully if above response is not an error message.")
except Exception as e:
    print(f"Test 1 failed: {e}")
    print_common_error_hints(e)
    raise

def get_product(product: str):
    catalog = {
        "jeans": 49.99,
        "shirt": 29.99,
        "dress": 59.99,
        "jacket": 89.99,
        "sneakers": 74.99,
        "hat": 19.99,
        "socks": 9.99,
        "hoodie": 44.99,
        "shorts": 34.99,
        "t-shirt": 24.99,
        "sweater": 54.99,
        "belt": 24.99,
    }
    return catalog[product]


def calculate(op: str, input1: float, input2: float):
    if op == "+":
        return input1 + input2
    elif op == "-":
        return input1 - input2
    elif op == "*":
        return input1 * input2
    elif op == "/":
        return input1 / input2
    elif op == "**":
        return input1 ** input2
    else:
        raise ValueError(f"unsupported op: {op!r}")

TOOL_REGISTRY = {
    "get_product": get_product,
    "calculate": calculate,
}

# ── Tool specs (sent to Claude) ──────────────────────────────────────────────

GET_PRODUCT_SPEC = {
    "name": "get_product",
    "description": "get_product",
    "input_schema": {
        "type": "object",
        "properties": {
            "product": {
                "type": "string",
                "description": "product",
            },
        },
        "required": ["product"],
    },
}

CALCULATE_SPEC = {
    "name": "calculate",
    "description": "calculator",
    "input_schema": {
        "type": "object",
        "properties": {
            "op": {
                "type": "string",
                "description": "operator",
            },
            "input1": {
                "type": "number",
                "description": "input1",
            },
            "input2": {
                "type": "number",
                "description": "input2",
            },
        },
        "required": ["op", "input1", "input2"],
    },
}

ALL_TOOL_SPECS = [GET_PRODUCT_SPEC, CALCULATE_SPEC]

# ── Agent ─────────────────────────────────────────────────────────────────────

def call_claude(messages, tools, model=None):
    return call_messages_with_retry(
        model=model or MODEL,
        system=SYSTEM_PROMPT,
        max_tokens = 1024,
        tools=tools,
        messages=messages,
    )


def execute_tool(name, inputs):
    try:
        return str(TOOL_REGISTRY[name](**inputs))
    except Exception as e:
        return f"Error: {e}"


def run_agent(prompt, eval_mode=False, model=None):
    messages = [{"role": "user", "content": prompt}]
    total_input_tokens = 0
    total_output_tokens = 0

    response = call_claude(messages, tools=ALL_TOOL_SPECS, model=model)
    total_input_tokens += response.usage.input_tokens
    total_output_tokens += response.usage.output_tokens
    messages.append({"role": "assistant", "content": response.content})

    tool_calls = [block for block in response.content if isinstance(block, ToolUseBlock)]

    if tool_calls:
        tool_results = [
            {
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": execute_tool(tool_call.name, tool_call.input),
            }
            for tool_call in tool_calls
        ]
        messages.append({"role": "user", "content": tool_results})

        response = call_claude(messages, tools=ALL_TOOL_SPECS, model=model)
        total_input_tokens += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens

    return "\n".join(block.text for block in response.content if isinstance(block, TextBlock))

query = "How much should jeans cost? Use the get product tool."

try:
    print(f"\nBoutique: {run_agent(query)}")
    print("Test 2 Successful if you see Jeans cost $49.99 -- If error printed before this.. please fix the error as suggested above.")
except Exception as e:
    print(f"Test 2 failed: {e}")
    print_common_error_hints(e)
    raise

print("common errors to check: Login requires 2 steps to refresh a token:  1) access https://myapps.microsoft.com/signin/113614_310378384655_ACP_AWS_APP/7a0cfafa-ac66-4c4e-b11f-e9385ddc5573?tenantId=e0793d39-0939-496d-b129-198edd916feb with bootcamp directly on the broswer to initiate the session 2) run aws login in the same terminal session you are running the code for the security key to transfer")