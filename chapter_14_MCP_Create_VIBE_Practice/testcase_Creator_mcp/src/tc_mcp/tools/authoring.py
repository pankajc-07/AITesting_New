"""Authoring tools for TC MCP — create, update, delete test cases."""

from __future__ import annotations

from typing import Callable

from fastmcp import FastMCP

from tc_mcp.models import TestCase, TestCaseChanges, TestCaseDraft


def register(mcp: FastMCP, repo: Callable, writes_enabled: bool) -> None:

    @mcp.tool(name="create_test_case", description="Create a new test case with auto-generated Issue Key. Returns the created test case.")
    def create_test_case(
        module: str,
        test_type: str,
        priority: str,
        summary: str,
        preconditions: str,
        steps: list[str],
        expected_result: str,
        browser: str,
        device: str,
        description: str | None = None,
        status: str = "Draft",
    ) -> dict:
        if not writes_enabled:
            return {"error": "Writes are disabled. Set TC_MCP_ALLOW_WRITE=true to enable."}
        r = repo()
        draft = TestCaseDraft(
            module=module, test_type=test_type, priority=priority,
            summary=summary, preconditions=preconditions, steps=steps,
            expected_result=expected_result, browser=browser, device=device,
            description=description, status=status,
        )
        key = r.next_key()
        desc = draft.description or f"As a QA engineer, {draft.summary.lower().rstrip('.')}."
        tc = TestCase(
            key=key, summary=draft.summary, description=desc,
            priority=draft.priority, module=draft.module,
            labels=[draft.module.lower().replace(" ", "-"), draft.test_type.lower()],
            test_type=draft.test_type, preconditions=draft.preconditions,
            steps=list(draft.steps), expected_result=draft.expected_result,
            browser=draft.browser, device=draft.device, status=draft.status,
        )
        r.add(tc)
        return {"message": f"Created {key}", "test_case": tc.full()}

    @mcp.tool(name="update_test_case", description="Update fields of an existing test case. Omit a field to keep its current value.")
    def update_test_case(issue_key: str, summary: str | None = None, priority: str | None = None,
                         status: str | None = None, test_type: str | None = None,
                         preconditions: str | None = None, steps: list[str] | None = None,
                         expected_result: str | None = None, browser: str | None = None,
                         device: str | None = None) -> dict:
        if not writes_enabled:
            return {"error": "Writes are disabled. Set TC_MCP_ALLOW_WRITE=true to enable."}
        r = repo()
        changes = {k: v for k, v in locals().items()
                   if k not in ("issue_key",) and v is not None}
        updated = r.update(issue_key, changes)
        if not updated:
            return {"error": f"Test case '{issue_key}' not found."}
        return {"message": f"Updated {issue_key}", "test_case": updated.full()}

    @mcp.tool(name="update_test_case_status", description="Quick status change for a test case.")
    def update_test_case_status(issue_key: str, new_status: str) -> dict:
        if not writes_enabled:
            return {"error": "Writes are disabled. Set TC_MCP_ALLOW_WRITE=true to enable."}
        r = repo()
        updated = r.update(issue_key, {"status": new_status})
        if not updated:
            return {"error": f"Test case '{issue_key}' not found."}
        return {"message": f"Updated {issue_key} status to {new_status}", "test_case": updated.compact()}

    @mcp.tool(name="delete_test_case", description="Soft-delete a test case (mark as Deprecated).")
    def delete_test_case(issue_key: str) -> dict:
        if not writes_enabled:
            return {"error": "Writes are disabled. Set TC_MCP_ALLOW_WRITE=true to enable."}
        r = repo()
        updated = r.update(issue_key, {"status": "Deprecated"})
        if not updated:
            return {"error": f"Test case '{issue_key}' not found."}
        return {"message": f"Deprecated {issue_key}"}