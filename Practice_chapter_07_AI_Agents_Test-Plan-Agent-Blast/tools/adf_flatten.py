"""ADF (Atlassian Document Format) to Markdown flattener."""


def flatten(adf_doc: dict) -> dict:
    """Convert an ADF document to clean markdown.

    Returns {"markdown": str, "unknown_types": list}
    """
    if not adf_doc or not isinstance(adf_doc, dict):
        return {"markdown": "", "unknown_types": []}

    unknown = []

    def _marks_to_wrap(text: str, marks: list) -> str:
        """Apply text marks (bold, italic, code, link, etc.)"""
        if not marks:
            return text
        for mark in marks:
            mtype = mark.get("type", "")
            if mtype == "strong":
                text = f"**{text}**"
            elif mtype == "em":
                text = f"*{text}*"
            elif mtype == "code":
                text = f"`{text}`"
            elif mtype == "link":
                href = mark.get("attrs", {}).get("href", "")
                if href:
                    text = f"[{text}]({href})"
            elif mtype == "strike":
                text = f"~~{text}~~"
        return text

    def _content_to_md(content: list, prefix: str = "") -> str:
        nonlocal unknown
        result = []

        for node in content:
            ntype = node.get("type", "")

            if ntype == "paragraph":
                para = _content_to_md(node.get("content", []))
                result.append(f"{prefix}{para}")

            elif ntype == "text":
                text = node.get("text", "")
                marks = node.get("marks", [])
                result.append(_marks_to_wrap(text, marks))

            elif ntype == "heading":
                level = node.get("attrs", {}).get("level", 1)
                text = _content_to_md(node.get("content", []))
                result.append(f"{prefix}{'#' * level} {text}")

            elif ntype == "bulletList":
                items = node.get("content", [])
                for item in items:
                    item_text = _content_to_md(item.get("content", []), "")
                    result.append(f"{prefix}- {item_text}")

            elif ntype == "orderedList":
                items = node.get("content", [])
                for i, item in enumerate(items, 1):
                    item_text = _content_to_md(item.get("content", []), "")
                    result.append(f"{prefix}{i}. {item_text}")

            elif ntype == "listItem":
                # Handled by bulletList/orderedList
                inner = _content_to_md(node.get("content", []))
                result.append(inner)

            elif ntype == "codeBlock":
                lang = node.get("attrs", {}).get("language", "")
                code = _content_to_md(node.get("content", []))
                result.append(f"{prefix}```{lang}\n{code}\n{prefix}```")

            elif ntype == "blockquote":
                quoted = _content_to_md(node.get("content", []), "> ")
                result.append(quoted)

            elif ntype == "rule":
                result.append(f"{prefix}---")

            elif ntype == "hardBreak":
                result.append("\n")

            elif ntype == "table":
                rows = node.get("content", [])
                table_md = []
                for row in rows:
                    cells = row.get("content", [])
                    cell_texts = []
                    for cell in cells:
                        ct = _content_to_md(cell.get("content", [])).strip()
                        cell_texts.append(ct)
                    table_md.append(f"| {' | '.join(cell_texts)} |")
                if table_md:
                    # Add header separator after first row
                    header_sep = "|" + "|".join(
                        " --- " for _ in range(len(table_md[0].split("|")) - 2)) + "|"
                    table_md.insert(1, header_sep)
                result.append("\n".join(table_md))

            elif ntype == "panel":
                panel_type = node.get("attrs", {}).get("panelType", "info")
                panel_text = _content_to_md(node.get("content", []))
                result.append(f"> **{panel_type.upper()}:** {panel_text}")

            elif ntype == "mention":
                attrs = node.get("attrs", {})
                name = attrs.get("text", attrs.get("id", "@unknown"))
                result.append(f"@{name}")

            elif ntype == "emoji":
                short_name = node.get("attrs", {}).get("shortName", "")
                result.append(f":{short_name}:")

            elif ntype == "media":
                filename = node.get("attrs", {}).get("filename", "attachment")
                result.append(f"[📎 {filename}]")

            elif ntype in ("mediaGroup", "mediaSingle", "inlineCard", "expand",
                         "nestedExpand", "decisionList", "decisionItem",
                         "taskList", "taskItem", "date", "status", "placeholder"):
                # Silently skip these for now
                pass

            else:
                unknown.append(ntype)
                result.append(f"[ADF:{ntype}]")

        return "\n".join(result) if prefix else "".join(result)

    md = _content_to_md(adf_doc.get("content", []))
    return {"markdown": md.strip(), "unknown_types": list(set(unknown))}


def loss_delta_pct(markdown: str, html: str) -> float:
    """Estimate information loss between markdown and rendered HTML.

    Returns percentage delta. >10% suggests the flattener lost content.
    """
    if not html or not markdown:
        return 0.0
    # Crude heuristic: compare stripped text length
    import re
    html_text = re.sub(r'<[^>]+>', '', html).strip()
    md_text = markdown.strip()
    if not html_text:
        return 0.0
    return round(abs(len(html_text) - len(md_text)) / len(html_text) * 100, 1)