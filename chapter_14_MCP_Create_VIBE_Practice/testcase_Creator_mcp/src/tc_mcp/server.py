"""TestCreator MCP server — FastMCP entry point."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from fastmcp import FastMCP

from tc_mcp import config
from tc_mcp.repository import Repository
from tc_mcp.tools import authoring, export, planning, quality, search


def build_instructions(r: Repository, writes_enabled: bool) -> str:
    live = len(r.live_rows())
    mode = "Writes are ON: create_test_case, update_test_case, update_test_case_status, delete_test_case are available." if writes_enabled else "This server is read-only. Set TC_MCP_ALLOW_WRITE=true to enable writes."
    return (
        f"TestCreator MCP serves the VWO test case catalog: {len(r.rows)} tests ({live} live) across "
        f"{len(r.modules)} modules.\n"
        "- Search: search_test_cases (by module, priority, type, browser, device, status, keyword).\n"
        "- Detail: get_test_case by Issue Key (e.g. VWO-1001).\n"
        "- Browse: list_modules, list_test_types, get_test_case_count.\n"
        "- Coverage: get_coverage_report, get_coverage_gaps, generate_test_plan_outline.\n"
        "- Quality: validate_test_case, find_duplicates, get_stale_test_cases.\n"
        "- Export: export_test_cases (json/csv/md), export_test_case (md).\n"
        "- Authoring: create_test_case, update_test_case, update_test_case_status, delete_test_case.\n"
        + mode
    )


def create_server(
    repository: Repository | None = None,
    *,
    allow_write: bool | None = None,
) -> FastMCP:
    repo_instance = repository or Repository()
    writes_enabled = config.allow_write() if allow_write is None else allow_write

    def repo() -> Repository:
        return repo_instance

    mcp = FastMCP(
        name="TestCreator MCP",
        instructions=build_instructions(repo_instance, writes_enabled),
        version="0.1.0",
    )
    search.register(mcp, repo)
    planning.register(mcp, repo)
    quality.register(mcp, repo)
    export.register(mcp, repo)
    authoring.register(mcp, repo, writes_enabled)
    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(prog="tc-mcp", description="TestCreator MCP server")
    parser.add_argument("--transport", choices=["stdio", "http"], default=config.transport(),
                        help="stdio (default) or http")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--allow-write", action="store_true", default=config.allow_write(),
                        help="Enable create/update/delete tools")
    args = parser.parse_args()

    if args.transport == "stdio":
        create_server(allow_write=args.allow_write).run(transport="stdio", show_banner=False)
        return

    mcp = create_server(allow_write=args.allow_write)
    mcp.run(transport="http", host=args.host, port=args.port, show_banner=True, stateless_http=True)


if __name__ == "__main__":
    main()