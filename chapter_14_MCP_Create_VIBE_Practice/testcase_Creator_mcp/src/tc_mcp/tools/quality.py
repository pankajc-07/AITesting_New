"""Quality & validation tools for TC MCP."""

from __future__ import annotations

from difflib import SequenceMatcher
from typing import Callable

from fastmcp import FastMCP


def register(mcp: FastMCP, repo: Callable) -> None:

    @mcp.tool(name="validate_test_case", description="Check a test case for completeness and quality issues.")
    def validate_test_case(issue_key: str) -> dict:
        r = repo()
        tc = r.get(issue_key)
        if not tc:
            return {"error": f"Test case '{issue_key}' not found."}

        issues: list[str] = []
        if not tc.summary or len(tc.summary) < 10:
            issues.append("Summary is too short (min 10 chars)")
        if not tc.preconditions or len(tc.preconditions) < 10:
            issues.append("Preconditions are too short or missing")
        if not tc.steps or len(tc.steps) < 2:
            issues.append("At least 2 steps are recommended")
        if not tc.expected_result or len(tc.expected_result) < 10:
            issues.append("Expected result is too short or missing")
        if tc.status == "Draft":
            issues.append("Test case is still in Draft status")
        if tc.status == "Deprecated":
            issues.append("Test case is Deprecated")

        return {
            "issue_key": issue_key,
            "valid": len(issues) == 0,
            "issues": issues,
            "score": max(0, 100 - len(issues) * 15),
        }

    @mcp.tool(name="find_duplicates", description="Find potentially duplicate test cases by similar summary text.")
    def find_duplicates(module: str | None = None, threshold: float = 0.8) -> dict:
        r = repo()
        rows = r.live_rows()
        if module:
            rows = [tc for tc in rows if tc.module.lower() == module.lower()]

        duplicates: list[dict] = []
        seen: set[str] = set()
        for i, tc1 in enumerate(rows):
            for tc2 in rows[i + 1:]:
                pair_key = f"{min(tc1.key, tc2.key)}-{max(tc1.key, tc2.key)}"
                if pair_key in seen:
                    continue
                ratio = SequenceMatcher(None, tc1.summary.lower(), tc2.summary.lower()).ratio()
                if ratio >= threshold:
                    seen.add(pair_key)
                    duplicates.append({
                        "test_1": tc1.compact(),
                        "test_2": tc2.compact(),
                        "similarity": round(ratio, 2),
                    })

        return {"duplicates_found": len(duplicates), "duplicates": duplicates[:20]}

    @mcp.tool(name="get_stale_test_cases", description="Find Draft or Deprecated test cases.")
    def get_stale_test_cases() -> dict:
        r = repo()
        drafts = [tc.compact() for tc in r.rows if tc.status == "Draft"]
        deprecated = [tc.compact() for tc in r.rows if tc.status == "Deprecated"]
        return {
            "draft_count": len(drafts),
            "deprecated_count": len(deprecated),
            "drafts": drafts[:20],
            "deprecated": deprecated[:20],
        }