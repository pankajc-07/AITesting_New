"""Trace generation. Creates trace.json mapping plan sections to Jira fields."""
import json
from datetime import datetime, timezone
from pathlib import Path


def new(key: str) -> dict:
    """Initialize a trace dict for a given Jira key."""
    return {
        "jira_key": key,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "steps": [],
    }


def step(trace: dict, step_name: str, **kwargs):
    """Record a trace step with metadata."""
    trace["steps"].append({
        "step": step_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **kwargs,
    })


def finish(trace: dict, out_dir: Path, outcome: str, output: dict = None) -> Path:
    """Finalize trace, write to out_dir/<KEY>-trace.json. Returns path."""
    trace["outcome"] = outcome
    trace["finished_at"] = datetime.now(timezone.utc).isoformat()
    if output:
        trace["output"] = output

    key = trace["jira_key"]
    out_dir.mkdir(exist_ok=True)
    path = out_dir / f"{key}-trace.json"
    with open(path, "w") as f:
        json.dump(trace, f, indent=2, default=str)
    return path