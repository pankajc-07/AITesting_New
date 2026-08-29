"""SOP 03 - raw Jira JSON -> normalized ticket.json."""
import re
from datetime import datetime, timezone

from tools import adf_flatten, field_map


def normalize(raw: dict, site: str, include_comments: bool = True) -> dict:
    """Convert raw Jira v3 response into a clean ticket.json object."""
    issue = raw["issue"]
    fields = issue.get("fields", {})
    names = issue.get("names", {})

    key = issue["key"]
    issue_type = fields.get("issuetype", {}).get("name", "Unknown")

    fm = field_map.resolve(names)

    # Description: ADF -> flatten
    desc_raw = fields.get("description")
    unknown_adf = []
    if isinstance(desc_raw, dict):
        flat = adf_flatten.flatten(desc_raw)
        desc_md = flat["markdown"]
        unknown_adf = flat["unknown_types"]
    elif isinstance(desc_raw, str):
        desc_md = desc_raw
    else:
        desc_md = ""

    # Rendered HTML cross-check
    rendered = fields.get("renderedFields")
    if not isinstance(rendered, dict):
        rendered = {}
    desc_html = rendered.get("description")

    # Acceptance criteria
    acceptance_criteria = _extract_ac(desc_md, fields, fm)

    # Comments
    comments = []
    if include_comments:
        for c in issue.get("_comments", []):
            body_raw = c.get("body")
            if isinstance(body_raw, dict):
                body_md = adf_flatten.flatten(body_raw)["markdown"]
            else:
                body_md = str(body_raw or "")
            comments.append({
                "author": c.get("author", {}).get("displayName", "Unknown"),
                "body_md": body_md,
                "created": c.get("created", ""),
            })

    # Sprint
    sprint = None
    sprint_raw = fields.get("sprint")
    if sprint_raw:
        if isinstance(sprint_raw, dict):
            sprint = sprint_raw
        elif isinstance(sprint_raw, list) and sprint_raw:
            sprint = sprint_raw[-1]

    # Parent / Epic
    parent = None
    parent_raw = fields.get("parent")
    if parent_raw:
        parent = {
            "key": parent_raw.get("key", ""),
            "summary": parent_raw.get("fields", {}).get("summary", ""),
        }

    # Linked issues
    linked = []
    for link in fields.get("issuelinks", []) or []:
        link_type = link.get("type", {}).get("name", "relates to")
        for direction in ("inwardIssue", "outwardIssue"):
            li = link.get(direction)
            if li:
                linked.append({
                    "key": li.get("key", ""),
                    "summary": li.get("fields", {}).get("summary", ""),
                    "link_type": link_type,
                })

    # Subtasks
    subtasks = []
    for st in fields.get("subtasks", []) or []:
        subtasks.append({
            "key": st.get("key", ""),
            "summary": st.get("fields", {}).get("summary", ""),
            "status": st.get("fields", {}).get("status", {}).get("name", ""),
        })

    # Attachments
    attachments = []
    for att in fields.get("attachment", []) or []:
        attachments.append({
            "filename": att.get("filename", ""),
            "mimeType": att.get("mimeType", ""),
            "size": att.get("size", 0),
        })

    # Environment
    env_val = fields.get("environment")
    if not env_val and fm["environment"]:
        env_val = fields.get(fm["environment"])
    env = str(env_val) if env_val else None

    # Gaps
    gaps = []
    if not acceptance_criteria:
        gaps.append("No acceptance criteria found on the ticket.")
    if not desc_md.strip():
        gaps.append("Ticket description is empty.")
    if not env:
        gaps.append("Environment not specified on the ticket.")

    components = [c.get("name", "") for c in (fields.get("components", []) or []) if c.get("name")]
    fix_versions = [v.get("name", "") for v in (fields.get("fixVersions", []) or []) if v.get("name")]

    return {
        "key": key,
        "url": f"{site}/browse/{key}",
        "summary": fields.get("summary", ""),
        "issue_type": issue_type,
        "status": fields.get("status", {}).get("name", None),
        "priority": (fields.get("priority") or {}).get("name", None),
        "labels": fields.get("labels", []) or [],
        "components": components,
        "fix_versions": fix_versions,
        "environment": env,
        "description_md": desc_md,
        "description_html": desc_html,
        "acceptance_criteria": acceptance_criteria,
        "comments": comments,
        "sprint": sprint,
        "parent": parent,
        "linked_issues": linked,
        "subtasks": subtasks,
        "attachments_meta": attachments,
        "source": "jira-cloud-v3",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "gaps": gaps,
    }


def _extract_ac(desc_md: str, fields: dict, fm: dict) -> list:
    """Extract acceptance criteria from description and/or custom fields."""
    ac_list = []

    # 1. Regex AC from description
    if desc_md:
        patterns = [
            r'(?:###?\s*Acceptance\s*Criteria\s*:?\s*\n)([\s\S]*?)(?:\n###?\s|\n\*\*[^*]+\*\*|\Z)',
            r'(?:Acceptance\s*Criteria\s*:?\s*\n)([\s\S]*?)(?:\n\*\s*\n\*\*|\Z)',
        ]
        for pat in patterns:
            match = re.search(pat, desc_md, re.IGNORECASE)
            if match:
                ac_text = match.group(1).strip()
                ac_lines = re.findall(r'[-*]\s*(.+)', ac_text)
                for line in ac_lines:
                    ac_list.append({
                        "text": line.strip(),
                        "origin": "description",
                        "field_name": None,
                    })
                break

    # 2. Custom field for AC
    if fm["acceptance_criteria"] and fm["acceptance_criteria"] in fields:
        ac_raw = fields[fm["acceptance_criteria"]]
        if isinstance(ac_raw, list):
            for ac in ac_raw:
                if isinstance(ac, str):
                    ac_list.append({
                        "text": ac,
                        "origin": "customfield",
                        "field_name": fm["acceptance_criteria"],
                    })
                elif isinstance(ac, dict) and ac.get("value"):
                    ac_list.append({
                        "text": str(ac["value"]),
                        "origin": "customfield",
                        "field_name": fm["acceptance_criteria"],
                    })
        elif isinstance(ac_raw, str):
            for line in ac_raw.split("\n"):
                line = line.strip()
                if line:
                    ac_list.append({
                        "text": line,
                        "origin": "customfield",
                        "field_name": fm["acceptance_criteria"],
                    })

    # 3. Last resort: bullet scan
    if not ac_list and desc_md:
        ac_section = re.search(
            r'Acceptance\s+Criteria[:\s]*\n((?:\s*[-*]\s*.+\n?)*)',
            desc_md, re.IGNORECASE)
        if ac_section:
            ac_lines = re.findall(r'[-*]\s*(.+)', ac_section.group(0))
            for line in ac_lines:
                ac_list.append({
                    "text": line.strip(),
                    "origin": "description",
                    "field_name": None,
                })

    return ac_list