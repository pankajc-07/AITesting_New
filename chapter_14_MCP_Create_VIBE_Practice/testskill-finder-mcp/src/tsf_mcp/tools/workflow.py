"""Workflow tools: skill chains, export, and prompts."""

from __future__ import annotations

from typing import Callable

from fastmcp import FastMCP

from tsf_mcp.catalog import Catalog


def register(mcp: FastMCP, get_catalog: Callable[[], Catalog]) -> None:

    @mcp.tool(name="suggest_skill_chain", description="Suggest a chain of skills for a multi-step testing workflow. E.g., 'I need to test a new login feature end-to-end'.")
    def suggest_skill_chain(task: str) -> dict:
        catalog = get_catalog()
        # Find relevant skills across STLC phases
        results = catalog.search(task, limit=15)
        # Group by category
        chain: dict[str, list[dict]] = {}
        for s in results:
            chain.setdefault(s.category, []).append(s.summary())
        return {
            "task": task,
            "suggested_chain": [
                {"phase": cat, "skills": skills}
                for cat, skills in chain.items()
            ],
            "total_skills": len(results),
        }

    @mcp.tool(name="export_skill", description="Export a skill as a ready-to-use prompt for Claude Code, Copilot, or Cursor.")
    def export_skill(name: str, target: str = "copilot") -> str:
        catalog = get_catalog()
        skill = catalog.skills.get(name)
        if not skill:
            for sname, s in catalog.skills.items():
                if sname.lower() == name.lower():
                    skill = s
                    break
        if not skill:
            return f"Skill '{name}' not found."

        if target == "claude":
            return f"""# {skill.title}
{skill.description}

## When to Use
{chr(10).join(f'- {u}' for u in skill.when_to_use) if skill.when_to_use else 'Use this skill when you need to ' + skill.description.lower()}

## Workflow
{chr(10).join(f'{i}. {step}' for i, step in enumerate(skill.workflow, 1)) if skill.workflow else 'Follow the steps in the skill file.'}

## Guardrails
{chr(10).join(f'- {g}' for g in skill.guardrails) if skill.guardrails else 'Follow standard testing best practices.'}
"""
        else:
            return f"""You are a {skill.title}. {skill.description}

When to use: {', '.join(skill.when_to_use[:3]) if skill.when_to_use else skill.description}

Workflow:
{chr(10).join(f'{i}. {step}' for i, step in enumerate(skill.workflow, 1)) if skill.workflow else '1. Follow the skill instructions.'}

Guardrails:
{chr(10).join(f'- {g}' for g in skill.guardrails) if skill.guardrails else '- Follow testing best practices.'}
"""

    @mcp.tool(name="get_skill_prompt", description="Get a ready-to-use prompt for a skill that can be sent to an LLM.")
    def get_skill_prompt(name: str) -> str:
        catalog = get_catalog()
        skill = catalog.skills.get(name)
        if not skill:
            for sname, s in catalog.skills.items():
                if sname.lower() == name.lower():
                    skill = s
                    break
        if not skill:
            return f"Skill '{name}' not found."
        return skill.raw