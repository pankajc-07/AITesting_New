"""SOP 04 - Readiness check. Is this ticket testable enough to plan?"""


def check(ticket: dict) -> dict:
    """Score a ticket on 11 readiness factors. Below 5/11 = refuse to plan.

    Returns:
        {"score": int, "max": 11, "threshold": 5, "plannable": bool,
         "blockers": [...], "gaps": [...]}
    """
    score = 0
    blockers = []
    factors = []

    # F1: Has a summary
    if ticket.get("summary", "").strip():
        score += 1
    else:
        blockers.append("Ticket has no summary — cannot identify what to test.")

    # F2: Has a description
    if ticket.get("description_md", "").strip():
        score += 1
    else:
        blockers.append("Ticket has no description — no requirements to test against.")

    # F3: Has acceptance criteria
    if ticket.get("acceptance_criteria"):
        score += 1
    else:
        blockers.append("No acceptance criteria — cannot define pass/fail.")

    # F4: Has an issue type
    if ticket.get("issue_type"):
        score += 1

    # F5: Has a status (in progress or defined)
    if ticket.get("status"):
        score += 1

    # F6: Has components/labels for categorisation
    if ticket.get("components") or ticket.get("labels"):
        score += 1

    # F7: Has fix versions (knows what release)
    if ticket.get("fix_versions"):
        score += 1

    # F8: Has environment info
    if ticket.get("environment"):
        score += 1
    else:
        blockers.append("Environment not specified — cannot define test environment.")

    # F9: Has parent/epic for context
    if ticket.get("parent"):
        score += 1

    # F10: Has linked issues (related work)
    if ticket.get("linked_issues"):
        score += 1

    # F11: Has comments (team discussion indicates maturity)
    if ticket.get("comments"):
        score += 1

    # Description has reasonable length (>100 chars)
    if len(ticket.get("description_md", "")) > 100:
        # Bonus: rich description, add extra confidence
        pass

    threshold = 5
    plannable = score >= threshold

    return {
        "score": score,
        "max": 11,
        "threshold": threshold,
        "plannable": plannable,
        "blockers": blockers,
        "gaps": ticket.get("gaps", []),
    }