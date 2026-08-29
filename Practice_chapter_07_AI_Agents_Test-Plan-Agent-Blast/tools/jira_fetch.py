"""SOP 01 - key in, raw Jira JSON out. I/O only, no interpretation."""
import re
import time
from pathlib import Path

import requests

from tools.config_store import load_config
from tools.errors import (InvalidKeyError, JiraAuthError, JiraConnectionError,
                          JiraError, JiraNotFoundError, JiraPermissionError,
                          JiraRateLimitError)
from tools.jira_auth import get_auth

KEY_RE = re.compile(r"^[A-Z][A-Z0-9]+-[0-9]+$")
TMP = Path(__file__).resolve().parent.parent / ".tmp"
TIMEOUT = 25

FIELDS = ("summary,description,issuetype,status,priority,labels,components,"
          "fixVersions,versions,parent,subtasks,issuelinks,attachment,assignee,"
          "reporter,creator,duedate,created,updated,environment")


def extract_key(text: str) -> str:
    """Pull an issue key out of a URL or a sentence. Deterministic, no LLM (AI-2)."""
    if not text:
        raise InvalidKeyError("No Jira key given.",
                             "Include a key such as SCRUM-42.")
    text = text.strip()
    # URL pattern: /browse/KEY-123
    m = re.search(r"/browse/([A-Z][A-Z0-9]+-\d+)", text, re.I)
    if m:
        return m.group(1).upper()
    # "PROJ-123" or "PROJ - 123"
    m = re.search(r"\b([A-Z][A-Z0-9]{1,9})\s*-\s*(\d+)\b", text.upper())
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    # "PROJ 123" (space instead of hyphen)
    m = re.search(r"\b([A-Z][A-Z0-9]{1,9})\s+(\d{1,6})\b", text.upper())
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    raise InvalidKeyError(
        f"No Jira issue key found in: {text[:80]!r}",
        "Include a key like PROJ-123, or paste the browse URL.",
    )


def _request(url, auth, params=None, attempt=1):
    try:
        resp = requests.get(url, auth=auth, params=params,
                            headers={"Accept": "application/json"}, timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise JiraConnectionError(
            f"Cannot reach Jira at {url.split('/rest')[0]}.",
            "Check the Jira URL in Settings and your network.")
    except requests.exceptions.Timeout:
        raise JiraConnectionError(f"Jira timed out after {TIMEOUT}s.", "Retry.")

    if resp.status_code == 429 and attempt <= 3:
        time.sleep(float(resp.headers.get("Retry-After", 2 ** attempt)))
        return _request(url, auth, params, attempt + 1)
    if resp.status_code >= 500 and attempt <= 3:
        time.sleep(2 ** (attempt - 1))
        return _request(url, auth, params, attempt + 1)
    return resp, attempt - 1


def _raise_for(resp, key):
    if "application/json" not in resp.headers.get("Content-Type", ""):
        raise JiraError("Jira returned HTML instead of JSON.",
                        "The Jira URL points at the web app, not the API.")
    if resp.status_code == 401:
        raise JiraAuthError("Jira authentication failed (401).",
                            "Regenerate the API token and update Settings.")
    if resp.status_code == 403:
        raise JiraPermissionError(
            "Jira refused the request (403).",
            "Your account cannot read this project.")
    if resp.status_code == 404:
        raise JiraNotFoundError(
            f"Ticket {key} was not found.",
            "Check the issue key and that you have access to the project.")
    if not resp.ok:
        raise JiraError(
            f"Jira returned {resp.status_code}: {resp.text[:200]}",
            "Unexpected error. Check the response for details.")


def fetch(key: str) -> dict:
    """Fetch a Jira issue and return the raw response + metadata.

    Returns:
        {"issue": {...}, "_meta": {"site": "...", "requests": 1, "api_version": "v3"}}
    """
    key = key.strip().upper()
    if not KEY_RE.match(key):
        raise InvalidKeyError(
            f"Invalid issue key: {key}",
            "Use the format PROJ-123 (uppercase project, hyphen, number).")

    cfg = load_config()
    site = cfg["jira_url"].rstrip("/")
    if not site:
        raise ConfigError("Jira URL is not set.", "Add it in Settings.")

    auth = get_auth()
    requests_made = 0

    # Fetch the ticket (v3 for ADF description)
    resp, retries = _request(
        f"{site}/rest/api/3/issue/{key}",
        auth,
        params={"fields": FIELDS, "expand": "renderedFields,names,schema"},
    )
    requests_made += 1 + retries
    _raise_for(resp, key)
    issue = resp.json()

    # Fetch comments
    comments = []
    try:
        c_resp, c_retries = _request(
            f"{site}/rest/api/3/issue/{key}/comment", auth)
        requests_made += 1 + c_retries
        if c_resp.ok:
            comments = c_resp.json().get("comments", [])

            # Handle pagination for comments
            while c_resp.ok and c_resp.json().get("total", 0) > len(comments):
                next_token = c_resp.json().get("nextPageToken")
                if not next_token:
                    break
                c_resp, c_retries = _request(
                    f"{site}/rest/api/3/issue/{key}/comment",
                    auth,
                    params={"nextPageToken": next_token},
                )
                requests_made += 1 + c_retries
                if c_resp.ok:
                    comments.extend(c_resp.json().get("comments", []))
    except Exception:
        pass  # Comments are optional

    issue["_comments"] = comments

    return {
        "issue": issue,
        "_meta": {
            "site": site,
            "requests": requests_made,
            "api_version": "v3",
        },
    }