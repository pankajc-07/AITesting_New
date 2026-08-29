# SOP 02: Resolve Fields

**Goal:** Map human-readable Jira field names to customfield_XXXXX keys.

**Input:** The `names` dict from Jira v3: `{"customfield_10034": "Acceptance Criteria", ...}`

**Logic:**
1. Iterate all customfield_ entries
2. Match against patterns (case-insensitive):
   - Acceptance Criteria: "acceptance criteria", "ac", "accept criteria"
   - Environment: "environment"

**Output:** `{"acceptance_criteria": "customfield_10034" or None, "environment": "customfield_10035" or None}`

**Edge Cases:** No match = None (downstream falls back to regex from description)

**Implementation:** `tools/field_map.py`