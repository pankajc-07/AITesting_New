"""SOP 05 - The ONE probabilistic step. Calls the LLM to build plan data.

Returns JSON, not markdown. BR-6: the model never touches the template.
AI-2: this is the only function in the project that calls a language model.
"""
import json
from pathlib import Path

from tools import llm_client
from tools.errors import LLMError, SchemaError

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "plan.schema.json"


def _load_schema() -> dict:
    if SCHEMA_PATH.exists():
        with open(SCHEMA_PATH) as f:
            return json.load(f)
    return {}


def _build_system_prompt() -> str:
    return """You are a senior QA architect. Your ONLY job is to produce a JSON test plan
object from a Jira ticket. You do NOT write markdown. You do NOT invent facts.

CRITICAL RULES:
1. NEVER invent an acceptance criterion. Only reference the exact ACs provided.
2. NEVER invent URLs, endpoint names, tool names, environment names, or dates.
   If the ticket doesn't provide them, say "Not specified in ticket".
3. Every section that has data MUST include a "justified_by" array naming
   the exact ticket fields that produced it.
4. If the ticket is missing information, list it under "assumptions" with
   reason set to "not_in_ticket" - never silently fill gaps.
5. The scope sections (in_scope, out_of_scope) must contain items that each
   have a "justified_by" naming the ticket field that justifies inclusion/exclusion.
6. Risks must be realistic for this specific ticket, not generic boilerplate.

Return ONLY valid JSON. No explanations, no markdown wrapping."""


def build(ticket: dict) -> tuple:
    """Build a test plan from a normalized ticket using the LLM.

    Returns:
        (plan_data: dict, usage: dict) with token counts and model info.
    """
    plan_schema = _load_schema()

    ticket_json = json.dumps({
        "key": ticket["key"],
        "summary": ticket["summary"],
        "issue_type": ticket["issue_type"],
        "status": ticket.get("status"),
        "priority": ticket.get("priority"),
        "labels": ticket.get("labels", []),
        "components": ticket.get("components", []),
        "fix_versions": ticket.get("fix_versions", []),
        "environment": ticket.get("environment"),
        "description": ticket["description_md"],
        "acceptance_criteria": [
            ac["text"] for ac in ticket.get("acceptance_criteria", [])
        ],
        "comments": [
            {"author": c["author"], "body": c["body_md"]}
            for c in ticket.get("comments", [])
        ],
        "linked_issues": ticket.get("linked_issues", []),
        "gaps": ticket.get("gaps", []),
    }, indent=2)

    messages = [
        {"role": "system", "content": _build_system_prompt()},
        {"role": "user", "content": f"""Generate a complete test plan JSON for this Jira ticket.

The JSON must conform to this schema:
{json.dumps(plan_schema, indent=2)}

Here is the ticket data:
{ticket_json}

Return ONLY the JSON test plan. No markdown, no code blocks, no explanations."""},
    ]

    max_attempts = 2
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            response = llm_client.chat(
                messages=messages,
                temperature=0.3,
                max_tokens=4096,
                response_format={"type": "json_object"},
            )
        except LLMError as e:
            last_error = e
            continue

        content = response["choices"][0]["message"]["content"]
        usage = {
            "model": response.get("model", "unknown"),
            "input_tokens": response.get("usage", {}).get("prompt_tokens", 0),
            "output_tokens": response.get("usage", {}).get("completion_tokens", 0),
            "schema_valid_on_attempt": attempt,
        }

        try:
            plan_data = json.loads(content)
        except json.JSONDecodeError as e:
            last_error = SchemaError(
                f"LLM returned invalid JSON on attempt {attempt}: {e}",
                "The model did not return parseable JSON. Retrying.")
            continue

        required = ["plan_meta", "objective", "scope", "test_strategy",
                    "risks_and_mitigations", "assumptions"]
        missing = [k for k in required if k not in plan_data]
        if missing:
            last_error = SchemaError(
                f"LLM plan missing required fields: {missing}",
                "The model omitted required sections. Retrying.")
            continue

        usage["schema_valid_on_attempt"] = attempt
        return plan_data, usage

    raise LLMError(
        f"Failed to generate a valid plan after {max_attempts} attempts.",
        f"Last error: {last_error}")