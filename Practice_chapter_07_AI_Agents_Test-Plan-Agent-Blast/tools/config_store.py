"""Config store. .env -> config.json fallback, matching course conventions."""
import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / ".tmp" / "config.json"
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

DEFAULTS = {
    "jira_url": "",
    "jira_email": "",
    "jira_api_token": "",
    "llm_provider": "groq",
    "groq_api_key": "",
    "groq_model": "openai/gpt-oss-120b",
    "include_comments": True,
    "default_jira_key": "PROJ-1",
    "field_map_cache": {},
}


def load_config() -> dict:
    """Load from env, then fall back to config.json, then defaults."""
    cfg = dict(DEFAULTS)

    # 1. config.json overrides defaults
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                cfg.update(json.load(f))
        except (json.JSONDecodeError, OSError):
            pass

    # 2. .env overrides everything (highest priority)
    if ENV_PATH.exists():
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k in DEFAULTS:
                        cfg[k] = v

    return cfg


def save_config(overrides: dict) -> None:
    """Merge overrides into config.json. Never writes secrets to disk."""
    cfg = load_config()
    cfg.update(overrides)
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def missing_credentials() -> list:
    """Which required credentials are missing? Returns a list of human-readable names."""
    cfg = load_config()
    missing = []

    if not cfg.get("jira_url"):
        missing.append("Jira URL")
    if not cfg.get("jira_email"):
        missing.append("Jira email")
    if not cfg.get("jira_api_token"):
        missing.append("Jira API token")

    provider = cfg.get("llm_provider", "groq")
    if provider == "groq" and not cfg.get("groq_api_key"):
        missing.append("Groq API key")

    return missing