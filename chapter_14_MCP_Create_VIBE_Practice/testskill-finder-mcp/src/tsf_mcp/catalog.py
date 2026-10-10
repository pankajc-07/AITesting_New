"""Load every SKILL.md under the skills folder into structured, searchable records."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from tsf_mcp import config
from tsf_mcp.text import tokenize

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.DOTALL)
TRIGGER_RE = re.compile(r'"([^"]{3,120})"')


@dataclass
class Skill:
    name: str
    title: str
    description: str
    license: str
    metadata: dict[str, Any]
    kind: str
    phase: str | None
    phase_number: int | None
    pack: str | None
    category: str
    rel_dir: str
    body: str
    raw: str
    triggers: list[str]
    when_to_use: list[str]
    workflow: list[str]
    guardrails: list[str]
    tokens: dict[str, set[str]] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "title": self.title,
            "category": self.category,
            "kind": self.kind,
            "phase": self.phase,
            "pack": self.pack,
            "description": self.description[:200],
            "triggers": self.triggers[:5],
            "path": f"{self.rel_dir}/SKILL.md",
        }

    def detail(self) -> dict[str, Any]:
        return {
            **self.summary(),
            "description": self.description,
            "license": self.license,
            "metadata": self.metadata,
            "when_to_use": self.when_to_use,
            "workflow": self.workflow,
            "guardrails": self.guardrails,
        }


class Catalog:
    def __init__(self, root: Path | None = None):
        self.root = root or config.skills_dir()
        self.skills: dict[str, Skill] = {}
        self.load_problems: list[str] = []
        self._load()

    def _load(self) -> None:
        if not self.root.exists():
            self.load_problems.append(f"Skills directory not found: {self.root}")
            return
        for md_file in sorted(self.root.rglob("SKILL.md")):
            try:
                skill = self._parse_skill(md_file)
                if skill:
                    self.skills[skill.name] = skill
            except Exception as e:
                self.load_problems.append(f"Failed to parse {md_file}: {e}")

    def _parse_skill(self, path: Path) -> Skill | None:
        raw = path.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(raw)
        if not m:
            self.load_problems.append(f"No frontmatter in {path}")
            return None

        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as e:
            self.load_problems.append(f"YAML error in {path}: {e}")
            return None

        body = m.group(2).strip()
        rel_dir = str(path.parent.relative_to(self.root)).replace("\\", "/")
        parts = rel_dir.split("/")

        # Determine kind, phase, pack
        kind = "stlc"
        phase = None
        phase_number = None
        pack = None
        category = "Other"

        if parts[0].startswith("0") and "-" in parts[0]:
            kind = "stlc"
            phase = parts[0]
            try:
                phase_number = int(parts[0].split("-")[0])
            except ValueError:
                pass
            category = parts[0].replace("-", " ").title()
        elif parts[0] == "framework-packs" and len(parts) > 1:
            kind = "pack"
            pack = parts[1]
            category = pack.replace("-", " ").title()

        name = fm.get("name", path.parent.name)
        title = fm.get("title", name.replace("-", " ").title())
        description = fm.get("description", "")
        license_val = fm.get("license", "MIT")
        metadata = {k: v for k, v in fm.items() if k not in ("name", "title", "description", "license")}

        triggers = TRIGGER_RE.findall(body)
        when_to_use = self._extract_section(body, "When to Use")
        workflow = self._extract_section(body, "Workflow")
        guardrails = self._extract_section(body, "Guardrails")

        # Build token index
        tokens: dict[str, set[str]] = {
            "name": set(tokenize(name)),
            "title": set(tokenize(title)),
            "triggers": set().union(*(set(tokenize(t)) for t in triggers)),
            "category": set(tokenize(category)),
            "description": set(tokenize(description)),
            "body": set(tokenize(body)),
        }

        return Skill(
            name=name, title=title, description=description,
            license=license_val, metadata=metadata,
            kind=kind, phase=phase, phase_number=phase_number,
            pack=pack, category=category, rel_dir=rel_dir,
            body=body, raw=raw, triggers=triggers,
            when_to_use=when_to_use, workflow=workflow,
            guardrails=guardrails, tokens=tokens,
        )

    @staticmethod
    def _extract_section(body: str, heading: str) -> list[str]:
        pattern = rf"(?:^|\n)#{{2,4}}\s*{re.escape(heading)}\s*\n(.*?)(?:\n#{{2,4}}\s|\Z)"
        m = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
        if not m:
            return []
        lines = [l.strip().lstrip("-* ").strip() for l in m.group(1).strip().split("\n") if l.strip()]
        return [l for l in lines if l]

    def categories(self) -> dict[str, list[Skill]]:
        groups: dict[str, list[Skill]] = {}
        for skill in self.skills.values():
            groups.setdefault(skill.category, []).append(skill)
        return dict(sorted(groups.items()))

    def search(self, query: str, limit: int = 10) -> list[Skill]:
        from tsf_mcp.text import expand, tokenize

        terms = tokenize(query)
        if not terms:
            return []
        weights = expand(terms)
        scored: list[tuple[float, Skill]] = []
        for skill in self.skills.values():
            score = 0.0
            for term, weight in weights.items():
                if term in skill.tokens["name"]:
                    score += weight * 6
                if term in skill.tokens["title"]:
                    score += weight * 4
                if term in skill.tokens["triggers"]:
                    score += weight * 3
                if term in skill.tokens["category"]:
                    score += weight * 3
                if term in skill.tokens["description"]:
                    score += weight * 2
                if term in skill.tokens["body"]:
                    score += weight * 0.5
            if score > 0:
                scored.append((score, skill))
        scored.sort(key=lambda x: -x[0])
        return [s for _, s in scored[:limit]]