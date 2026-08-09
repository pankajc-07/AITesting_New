"""
config_store.py — Persisted settings layer for Jira Test Case Generator.

Reads credentials from .env on first run, then persists user-editable
settings to a local settings.json file (gitignored).  The .env file
remains the source of truth for secrets; settings.json stores the
user's runtime preferences (provider choice, etc.).
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # chapter_03_Local_TC_Genarator/
ENV_PATH = BASE_DIR / ".env"
SETTINGS_PATH = BASE_DIR / "settings.json"

# Load .env once at import time
load_dotenv(ENV_PATH)

# ---------------------------------------------------------------------------
# Defaults (used when neither .env nor settings.json has a value)
# ---------------------------------------------------------------------------
DEFAULTS = {
    "JIRA_BASE_URL": "",
    "JIRA_EMAIL": "",
    "JIRA_API_TOKEN": "",
    "LLM_PROVIDER": "ollama",
    "GROQ_API_KEY": "",
    "OLLAMA_BASE_URL": "http://localhost:11434",
    "OLLAMA_MODEL": "gemma3:1b",
}

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_settings() -> dict:
    """
    Return the merged settings dict.

    Priority:  settings.json  >  .env  >  DEFAULTS
    """
    settings = dict(DEFAULTS)

    # Layer 1: .env overrides defaults
    for key in DEFAULTS:
        env_val = os.getenv(key)
        if env_val is not None:
            settings[key] = env_val

    # Layer 2: settings.json overrides .env (user explicitly saved these)
    if SETTINGS_PATH.exists():
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as fh:
                file_settings = json.load(fh)
            settings.update(file_settings)
        except (json.JSONDecodeError, OSError):
            pass  # corrupted file → fall through to env/defaults

    return settings


def save_settings(settings_dict: dict) -> None:
    """Persist a settings dict to settings.json."""
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as fh:
        json.dump(settings_dict, fh, indent=2)


def get_setting(key: str, default=None):
    """Convenience: return a single setting value."""
    return load_settings().get(key, default)


def set_setting(key: str, value: str) -> None:
    """Update a single key in settings.json (read-modify-write)."""
    current = load_settings()
    current[key] = value
    save_settings(current)


# ---------------------------------------------------------------------------
# Standalone smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    s = load_settings()
    print("Loaded settings:")
    for k, v in s.items():
        # Mask secrets
        if "TOKEN" in k or "KEY" in k or "PASSWORD" in k:
            v = (v[:4] + "****") if len(v) > 4 else "****"
        print(f"  {k} = {v}")