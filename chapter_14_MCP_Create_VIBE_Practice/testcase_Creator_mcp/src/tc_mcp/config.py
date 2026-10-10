"""Runtime settings for TC MCP."""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PACKAGE_DIR.parent.parent  # testcase_Creator_mcp/
CSV_NAME = "vwo_5000_test_cases.csv"
REPO_CSV = PROJECT_DIR.parent / "data" / CSV_NAME  # chapter_14_MCP_Create_VIBE_Practice/data/

MAX_COMPACT_ROWS = 100
MAX_FULL_ROWS = 25
DEFAULT_LIMIT = 20

PRIORITY_WEIGHT = {"Highest": 40, "High": 30, "Medium": 20, "Low": 10}
STATUS_WEIGHT = {"Ready": 10, "Automated": 8, "Draft": 2, "Deprecated": 0}
TYPE_WEIGHT = {
    "Security": 6, "Functional": 6, "Negative": 5, "API": 5,
    "Regression": 4, "Boundary": 4, "Performance": 3, "UI/UX": 2, "Accessibility": 2,
}


def data_path() -> Path:
    env = os.getenv("TC_MCP_DATA_PATH")
    if env:
        return Path(env).expanduser().resolve()
    return REPO_CSV


def allow_write() -> bool:
    return os.getenv("TC_MCP_ALLOW_WRITE", "").strip().lower() in {"1", "true", "yes", "on"}


def transport() -> str:
    return os.getenv("TC_MCP_TRANSPORT", "stdio").strip().lower()