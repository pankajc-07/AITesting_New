"""Planning & coverage tools for TC MCP."""

from __future__ import annotations

from typing import Callable

from fastmcp import FastMCP


def register(mcp: FastMCP, repo: Callable) -> None:

    @mcp.tool(name="get_coverage_report", description="Get per-module coverage: counts by test type, priority, and status.")
    def get_coverage_report(module: str | None = None) -> dict:
        r = repo()
        rows = r.live_rows()
        if module:
            rows = [tc for tc in rows if tc.module.lower() == module.lower()]

        by_type: dict[str, int] = {}
        by_priority: dict[str, int] = {}
        by_status: dict[str, int] = {}
        for tc in rows:
            by_type[tc.test_type] = by_type.get(tc.test_type, 0) + 1
            by_priority[tc.priority] = by_priority.get(tc.priority, 0) + 1
            by_status[tc.status] = by_status.get(tc.status, 0) + 1

        return {
            "module": module or "All",
            "total": len(rows),
            "by_test_type": dict(sorted(by_type.items(), key=lambda x: x[1], reverse=True)),
            "by_priority": dict(sorted(by_priority.items(), key=lambda x: x[1], reverse=True)),
            "by_status": dict(sorted(by_status.items(), key=lambda x: x[1], reverse=True)),
        }

    @mcp.tool(name="get_coverage_gaps", description="Find modules with zero test cases for a given test type or priority.")
    def get_coverage_gaps(test_type: str | None = None, priority: str | None = None) -> dict:
        r = repo()
        gaps: list[str] = []
        for mod in r.modules:
            mod_tests = [tc for tc in r.live_rows() if tc.module == mod]
            if test_type and not any(tc.test_type == test_type for tc in mod_tests):
                gaps.append(f"{mod} (no {test_type} tests)")
            if priority and not any(tc.priority == priority for tc in mod_tests):
                gaps.append(f"{mod} (no {priority} priority tests)")
        return {"gaps": gaps, "total_gaps": len(gaps)}

    @mcp.tool(name="generate_test_plan_outline", description="Generate a structured test plan outline for a module.")
    def generate_test_plan_outline(module: str) -> dict:
        r = repo()
        mod_tests = [tc for tc in r.live_rows() if tc.module.lower() == module.lower()]
        if not mod_tests:
            return {"error": f"No test cases found for module '{module}'."}

        by_type: dict[str, list[dict]] = {}
        for tc in mod_tests:
            by_type.setdefault(tc.test_type, []).append(tc.compact())

        return {
            "module": module,
            "total_test_cases": len(mod_tests),
            "test_types_covered": list(by_type.keys()),
            "highest_priority_count": sum(1 for tc in mod_tests if tc.priority == "Highest"),
            "ready_count": sum(1 for tc in mod_tests if tc.status == "Ready"),
            "automated_count": sum(1 for tc in mod_tests if tc.status == "Automated"),
            "sample_test_cases": [tc.compact() for tc in mod_tests[:5]],
        }