"""Export tools for TC MCP — CSV, JSON, Markdown output."""

from __future__ import annotations

import csv
import io
import json
from typing import Callable

from fastmcp import FastMCP

from tc_mcp.models import TestFilter


def register(mcp: FastMCP, repo: Callable) -> None:

    @mcp.tool(name="export_test_cases", description="Export filtered test cases as CSV, JSON, or Markdown.")
    def export_test_cases(
        format: str = "json",
        module: str | None = None,
        test_type: list[str] | None = None,
        priority: list[str] | None = None,
        status: list[str] | None = None,
        limit: int = 50,
    ) -> str:
        r = repo()
        f = TestFilter(module=module, test_type=test_type, priority=priority, status=status)
        results = r.search(f)[:limit]

        if format == "json":
            return json.dumps([tc.full() for tc in results], indent=2)
        elif format == "csv":
            buf = io.StringIO()
            writer = csv.DictWriter(buf, fieldnames=["Issue Key", "Summary", "Priority", "Component", "Test Type", "Status", "Browser", "Device"])
            writer.writeheader()
            for tc in results:
                writer.writerow({"Issue Key": tc.key, "Summary": tc.summary, "Priority": tc.priority,
                                 "Component": tc.module, "Test Type": tc.test_type, "Status": tc.status,
                                 "Browser": tc.browser, "Device": tc.device})
            return buf.getvalue()
        elif format == "md":
            lines = ["| Issue Key | Summary | Priority | Module | Type | Status |",
                      "|-----------|---------|----------|--------|------|--------|"]
            for tc in results:
                lines.append(f"| {tc.key} | {tc.summary[:60]} | {tc.priority} | {tc.module} | {tc.test_type} | {tc.status} |")
            return "\n".join(lines)
        else:
            return f"Unsupported format: {format}. Use json, csv, or md."

    @mcp.tool(name="export_test_case", description="Export a single test case as formatted Markdown.")
    def export_test_case(issue_key: str) -> str:
        r = repo()
        tc = r.get(issue_key)
        if not tc:
            return f"Test case '{issue_key}' not found."
        return f"""# {tc.key}: {tc.summary}

**Priority:** {tc.priority} | **Type:** {tc.test_type} | **Status:** {tc.status}
**Module:** {tc.module} | **Browser:** {tc.browser} | **Device:** {tc.device}

## Description
{tc.description}

## Preconditions
{tc.preconditions}

## Steps
{chr(10).join(f'{i}. {s}' for i, s in enumerate(tc.steps, 1))}

## Expected Result
{tc.expected_result}

## Labels
{' '.join(tc.labels)}
"""