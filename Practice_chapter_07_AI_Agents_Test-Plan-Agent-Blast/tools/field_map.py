"""Field name resolver. Maps customfield_XXXXX to human-readable names."""

FIELD_CACHE = {}

# Known field name patterns to search for
AC_PATTERNS = [
    "acceptance criteria",
    "acceptance criterias",
    "acceptance_criteria",
    "ac",
    "accept criteria",
]


def resolve(names: dict) -> dict:
    """Given Jira's 'names' dict, find key custom fields.

    Args:
        names: The 'names' object from a Jira v3 response.
               Maps customfield_XXXXX -> "Human Readable Name"

    Returns:
        {"acceptance_criteria": "customfield_10034" or None,
         "environment": "customfield_10035" or None}
    """
    result = {"acceptance_criteria": None, "environment": None}

    for field_id, field_name in names.items():
        name_lower = field_name.lower().strip()

        if result["acceptance_criteria"] is None:
            for pat in AC_PATTERNS:
                if pat in name_lower:
                    result["acceptance_criteria"] = field_id
                    break

        if result["environment"] is None and "environment" in name_lower:
            result["environment"] = field_id

        # Cache for later use
        FIELD_CACHE[field_id] = field_name

    return result


def get_name(field_id: str) -> str:
    """Get the human-readable name for a field ID."""
    return FIELD_CACHE.get(field_id, field_id)