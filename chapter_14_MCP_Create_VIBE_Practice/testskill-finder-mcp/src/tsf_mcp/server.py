"""TestSkill Finder MCP server — FastMCP entry point."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from fastmcp import FastMCP

from tsf_mcp import config
from tsf_mcp.catalog import Catalog
from tsf_mcp.tools import finder, workflow


def build_instructions(catalog: Catalog, writes_enabled: bool) -> str:
    groups = catalog.categories()
    stlc_phases = [cat for cat in groups if groups[cat][0].kind == "stlc"] if groups else []
    packs = [cat for cat in groups if groups[cat][0].kind == "pack"] if groups else []
    return (
        f"TestSkill Finder serves {len(catalog.skills)} QA agent skills: "
        f"{len(stlc_phases)} STLC phases, {len(packs)} framework packs.\n"
        "- Find a skill: search_skills (keywords) or find_skill_for_task (plain English).\n"
        "- Browse: list_categories, list_skills, get_stlc_pipeline.\n"
        "- Detail: get_skill, get_skill_file, get_related_skills, compare_skills.\n"
        "- Use: get_skill_prompt, export_skill (for Claude Code, Copilot, Cursor).\n"
        "- Chain: suggest_skill_chain for multi-step workflows.\n"
        + ("Writes are ON." if writes_enabled else "This server is read-only.")
    )


def create_server(catalog: Catalog | None = None, *, allow_write: bool | None = None) -> FastMCP:
    catalog = catalog or Catalog()
    for problem in catalog.load_problems[:20]:
        print(f"[tsf-mcp] {problem}", file=sys.stderr)
    writes_enabled = config.allow_write() if allow_write is None else allow_write

    def get_catalog() -> Catalog:
        return catalog

    mcp = FastMCP(
        name="TestSkill Finder MCP",
        instructions=build_instructions(catalog, writes_enabled),
        version="0.1.0",
    )
    finder.register(mcp, get_catalog)
    workflow.register(mcp, get_catalog)
    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(prog="tsf-mcp", description="TestSkill Finder MCP server")
    parser.add_argument("--transport", choices=["stdio", "http"], default=config.transport(),
                        help="stdio (default) or http")
    parser.add_argument("--host", default=config.host())
    parser.add_argument("--port", type=int, default=config.port())
    parser.add_argument("--allow-write", action="store_true", default=config.allow_write())
    args = parser.parse_args()

    if args.transport == "stdio":
        create_server(allow_write=args.allow_write).run(transport="stdio", show_banner=False)
        return

    mcp = create_server(allow_write=args.allow_write)
    mcp.run(transport="http", host=args.host, port=args.port, show_banner=True, stateless_http=True)


if __name__ == "__main__":
    main()