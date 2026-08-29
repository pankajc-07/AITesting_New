"""Jira authentication helper."""
from tools.config_store import load_config
from tools.errors import ConfigError


def get_auth():
    """Return (email, api_token) tuple from config."""
    cfg = load_config()
    email = cfg.get("jira_email")
    token = cfg.get("jira_api_token")
    if not email or not token:
        raise ConfigError(
            "Jira credentials are not configured.",
            "Open the Settings page and add your Jira email and API token.",
        )
    return email, token


def verify() -> dict:
    """Phase 2 LINK handshake. Returns account info on success, raises on failure."""
    import requests
    from tools.errors import JiraAuthError, JiraConnectionError

    cfg = load_config()
    url = cfg.get("jira_url", "").rstrip("/")
    if not url:
        raise ConfigError("Jira URL is not set.", "Add it in Settings.")
    email, token = get_auth()

    try:
        resp = requests.get(
            f"{url}/rest/api/3/myself",
            auth=(email, token),
            headers={"Accept": "application/json"},
            timeout=15,
        )
    except requests.exceptions.ConnectionError:
        raise JiraConnectionError(
            f"Cannot reach Jira at {url}.",
            "Check the URL in Settings and your network connection.",
        )
    except requests.exceptions.Timeout:
        raise JiraConnectionError("Jira timed out.", "Check your network and retry.")

    if resp.status_code == 401:
        raise JiraAuthError(
            "Jira authentication failed (401).",
            "Regenerate your API token at id.atlassian.com and update Settings.",
        )
    if resp.status_code == 403:
        raise JiraAuthError(
            "Jira refused access (403).",
            "Your account may not have permission to this instance.",
        )
    if not resp.ok:
        raise JiraAuthError(
            f"Jira returned {resp.status_code}: {resp.text[:200]}",
            "Check the Jira URL in Settings.",
        )

    return resp.json()