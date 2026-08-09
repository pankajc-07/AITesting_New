"""
jira_client.py — Jira REST API wrapper.

Fetches issue details (summary, description, acceptance criteria)
using Basic Auth with the credentials stored via config_store.
"""

import re
import requests
from requests.auth import HTTPBasicAuth
from config_store import get_setting


def _build_url(path: str) -> str:
    """Build a full Jira REST API URL from a relative path."""
    base = get_setting("JIRA_BASE_URL", "").rstrip("/")
    return f"{base}{path}"


def _extract_acceptance_criteria(description: str | None) -> str:
    """
    Try to pull out an 'Acceptance Criteria' / 'AC' section from the
    description field.  Returns the extracted text or a fallback message.
    """
    if not description:
        return "Not specified"

    # Common patterns in Jira descriptions
    patterns = [
        r"(?:Acceptance\s*Criteria|AC)\s*[:;]\s*\n?(.*?)(?=\n\s*\n\s*(?:#|Given|When|Then|Scenario|Out\s*of\s*Scope)|$)",
        r"h\d\.\s*Acceptance\s*Criteria\s*\n+(.*?)(?=\n\s*\n\s*h\d\.|$)",
    ]

    for pat in patterns:
        m = re.search(pat, description, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()

    # Fallback: return the whole description
    return description


def fetch_issue(issue_key: str) -> dict:
    """
    Fetch a Jira issue and return a structured dict.

    Returns on success:
        {"ok": True, "key": "...", "summary": "...",
         "description": "...", "acceptance_criteria": "..."}

    Returns on failure:
        {"ok": False, "error": "human-readable message"}
    """
    email = get_setting("JIRA_EMAIL")
    token = get_setting("JIRA_API_TOKEN")
    base_url = get_setting("JIRA_BASE_URL")

    # --- Validation ---
    if not base_url:
        return {"ok": False, "error": "Jira Base URL is not configured. Go to Settings."}
    if not email or not token:
        return {"ok": False, "error": "Jira credentials are not configured. Go to Settings."}

    # --- API call ---
    try:
        resp = requests.get(
            _build_url(f"/rest/api/2/issue/{issue_key}"),
            auth=HTTPBasicAuth(email, token),
            headers={"Accept": "application/json"},
            timeout=15,
        )
    except requests.exceptions.ConnectionError:
        return {"ok": False, "error": f"Cannot connect to Jira at {base_url}. Check the URL."}
    except requests.exceptions.Timeout:
        return {"ok": False, "error": "Jira request timed out. Try again."}
    except requests.exceptions.RequestException as exc:
        return {"ok": False, "error": f"Jira request failed: {exc}"}

    # --- Handle HTTP errors ---
    if resp.status_code == 401:
        return {"ok": False, "error": "Jira authentication failed. Check email / API token in Settings."}
    if resp.status_code == 404:
        return {"ok": False, "error": f"Issue '{issue_key}' not found. Check the key and try again."}
    if not resp.ok:
        return {"ok": False, "error": f"Jira returned HTTP {resp.status_code}: {resp.text[:200]}"}

    # --- Parse response ---
    data = resp.json()
    fields = data.get("fields", {})

    summary = fields.get("summary", "No summary")
    description = fields.get("description", "")
    # description can be a string or an Atlassian Document Format dict
    if isinstance(description, dict):
        # Flatten ADF to plain text (simple approach)
        description = _flatten_adf(description)

    acceptance_criteria = _extract_acceptance_criteria(description)

    return {
        "ok": True,
        "key": data.get("key", issue_key),
        "summary": summary,
        "description": description or "No description",
        "acceptance_criteria": acceptance_criteria,
    }


def _flatten_adf(doc: dict) -> str:
    """Crude ADF → plain-text converter. Good enough for our use case."""
    parts = []

    def walk(node):
        if isinstance(node, str):
            parts.append(node)
        elif isinstance(node, dict):
            if node.get("type") == "text":
                parts.append(node.get("text", ""))
            for child in node.get("content", []):
                walk(child)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(doc)
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Standalone smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    key = sys.argv[1] if len(sys.argv) > 1 else "SAMPLE-1"
    result = fetch_issue(key)
    for k, v in result.items():
        print(f"{k}: {v[:120] if isinstance(v, str) and len(v) > 120 else v}")