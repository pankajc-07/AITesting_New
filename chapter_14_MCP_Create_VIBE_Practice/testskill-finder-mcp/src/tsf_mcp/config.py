"""Runtime settings for TSF MCP."""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PACKAGE_DIR.parent.parent  # testskill-finder-mcp/
SKILLS_DIR = PROJECT_DIR / "skills"


def skills_dir() -> Path:
    env = os.getenv("TSF_SKILLS_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return SKILLS_DIR


def allow_write() -> bool:
    return os.getenv("TSF_ALLOW_WRITE", "").strip().lower() in {"1", "true", "yes", "on"}


def transport() -> str:
    return os.getenv("TSF_TRANSPORT", "stdio").strip().lower()


def host() -> str:
    return os.getenv("TSF_HOST", "127.0.0.1")


def port() -> int:
    return int(os.getenv("TSF_PORT", "8110"))