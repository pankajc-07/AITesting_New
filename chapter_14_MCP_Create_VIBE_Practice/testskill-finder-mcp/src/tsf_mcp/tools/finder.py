"""Finder tools: search, browse, and discover skills."""

from __future__ import annotations

from typing import Callable

from fastmcp import FastMCP

from tsf_mcp.catalog import Catalog


def register(mcp: FastMCP, get_catalog: Callable[[], Catalog]) -> None:

    @mcp.tool(name="search_skills", description="Search skills by keyword. Finds skills matching your query across name, title, triggers, description, and body.")
    def search_skills(query: str, limit: int = 10) -> dict:
        catalog = get_catalog()
        results = catalog.search(query, limit=limit)
        return {
            "query": query,
            "total": len(results),
            "results": [s.summary() for s in results],
        }

    @mcp.tool(name="find_skill_for_task", description="Find the best skill for a plain-English task description. Returns top matches with trigger phrases.")
    def find_skill_for_task(task: str, limit: int = 3) -> dict:
        catalog = get_catalog()
        results = catalog.search(task, limit=limit)
        return {
            "task": task,
            "total": len(results),
            "results": [s.summary() for s in results],
        }

    @mcp.tool(name="get_skill", description="Get full details of a skill by name.")
    def get_skill(name: str) -> dict:
        catalog = get_catalog()
        skill = catalog.skills.get(name)
        if not skill:
            # Try case-insensitive
            for sname, s in catalog.skills.items():
                if sname.lower() == name.lower():
                    return s.detail()
            return {"error": f"Skill '{name}' not found. Use search_skills to find available skills."}
        return skill.detail()

    @mcp.tool(name="get_skill_file", description="Get the raw SKILL.md content for a skill by name.")
    def get_skill_file(name: str) -> str:
        catalog = get_catalog()
        skill = catalog.skills.get(name)
        if not skill:
            for sname, s in catalog.skills.items():
                if sname.lower() == name.lower():
                    return s.raw
            return f"Skill '{name}' not found."
        return skill.raw

    @mcp.tool(name="list_categories", description="List all skill categories (STLC phases and framework packs) with counts.")
    def list_categories() -> dict:
        catalog = get_catalog()
        groups = catalog.categories()
        return {
            "categories": [
                {"name": cat, "count": len(skills), "kind": skills[0].kind if skills else "unknown"}
                for cat, skills in groups.items()
            ]
        }

    @mcp.tool(name="list_skills", description="List all skills, optionally filtered by category.")
    def list_skills(category: str | None = None) -> dict:
        catalog = get_catalog()
        skills = list(catalog.skills.values())
        if category:
            skills = [s for s in skills if s.category.lower() == category.lower()]
        return {
            "total": len(skills),
            "skills": [s.summary() for s in sorted(skills, key=lambda x: x.name)],
        }

    @mcp.tool(name="get_stlc_pipeline", description="Get the full STLC pipeline with skills mapped to each phase.")
    def get_stlc_pipeline() -> dict:
        catalog = get_catalog()
        groups = catalog.categories()
        pipeline = {}
        for cat, skills in groups.items():
            if skills and skills[0].kind == "stlc":
                pipeline[cat] = [s.summary() for s in skills]
        return {"pipeline": pipeline}

    @mcp.tool(name="get_related_skills", description="Find skills related to a given skill (same category or pack).")
    def get_related_skills(name: str) -> dict:
        catalog = get_catalog()
        skill = catalog.skills.get(name)
        if not skill:
            for sname, s in catalog.skills.items():
                if sname.lower() == name.lower():
                    skill = s
                    break
        if not skill:
            return {"error": f"Skill '{name}' not found."}
        related = [s.summary() for s in catalog.skills.values()
                   if s.name != skill.name and s.category == skill.category]
        return {
            "skill": skill.summary(),
            "related_count": len(related),
            "related": related,
        }

    @mcp.tool(name="compare_skills", description="Compare two skills side by side.")
    def compare_skills(name1: str, name2: str) -> dict:
        catalog = get_catalog()
        s1 = catalog.skills.get(name1)
        s2 = catalog.skills.get(name2)
        if not s1:
            for sn, s in catalog.skills.items():
                if sn.lower() == name1.lower():
                    s1 = s
                    break
        if not s2:
            for sn, s in catalog.skills.items():
                if sn.lower() == name2.lower():
                    s2 = s
                    break
        if not s1:
            return {"error": f"Skill '{name1}' not found."}
        if not s2:
            return {"error": f"Skill '{name2}' not found."}
        return {
            "skill_1": s1.summary(),
            "skill_2": s2.summary(),
            "same_category": s1.category == s2.category,
            "same_kind": s1.kind == s2.kind,
        }