"""Search & discovery tools for TC MCP."""

from __future__ import annotations

from typing import Callable

from fastmcp import FastMCP

from tc_mcp.models import TestFilter


def register(mcp: FastMCP, repo: Callable) -> None:

    @mcp.tool(name="search_test_cases", description="Search test cases by module, priority, type, browser, device, status, or keyword.")
    def search_test_cases(
        module: str | None = None,
        priority: list[str] | None = None,
        test_type: list[str] | None = None,
        browser: str | None = None,
        device: str | None = None,
        status: list[str] | None = None,
        keyword: str | None = None,
        include_deprecated: bool = False,
        limit: int = 20,
    ) -> dict:
        r = repo()
        f = TestFilter(
            module=module, priority=priority, test_type=test_type,
            browser=browser, device=device, status=status,
            keyword=keyword, include_deprecated=include_deprecated,
        )
        results = r.search(f)[:limit]
        return {
            "total": len(results),
            "results": [tc.compact() for tc in results],
        }

    @mcp.tool(name="get_test_case", description="Get full details of a single test case by its Issue Key (e.g. VWO-1001).")
    def get_test_case(issue_key: str) -> dict:
        r = repo()
        tc = r.get(issue_key)
        if not tc:
            return {"error": f"Test case '{issue_key}' not found."}
        return tc.full()

    @mcp.tool(name="list_modules", description="List all VWO modules with test case counts.")
    def list_modules() -> dict:
        r = repo()
        counts = r.get_counts("component")
        return {"modules": [{"name": k, "count": v} for k, v in counts.items()]}

    @mcp.tool(name="list_test_types", description="List all test types with counts.")
    def list_test_types() -> dict:
        r = repo()
        counts = r.get_counts("test_type")
        return {"test_types": [{"name": k, "count": v} for k, v in counts.items()]}

    @mcp.tool(name="get_test_case_count", description="Get aggregate counts grouped by a dimension (component, test_type, priority, status, browser, device).")
    def get_test_case_count(group_by: str = "component") -> dict:
        r = repo()
        valid = ["component", "test_type", "priority", "status", "browser", "device"]
        if group_by not in valid:
            return {"error": f"Invalid group_by. Choose from: {valid}"}
        return {"group_by": group_by, "counts": r.get_counts(group_by)}

    @mcp.tool(name="find_related_test_cases", description="Find test cases in the same module and test type as a given test case.")
    def find_related_test_cases(issue_key: str, limit: int = 10) -> dict:
        r = repo()
        tc = r.get(issue_key)
        if not tc:
            return {"error": f"Test case '{issue_key}' not found."}
        related = [t for t in r.live_rows()
                   if t.module == tc.module and t.test_type == tc.test_type and t.key != tc.key][:limit]
        return {
            "source": tc.compact(),
            "related_count": len(related),
            "related": [t.compact() for t in related],
        }