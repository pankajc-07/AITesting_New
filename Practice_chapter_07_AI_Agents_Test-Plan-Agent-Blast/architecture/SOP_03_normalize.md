# SOP 03: Normalize

**Goal:** Convert raw Jira v3 response → clean `ticket.json` conforming to ticket schema.

**Input:** Output of SOP 01 (raw dict) + Jira site URL.

**Logic:**
1. Flatten ADF description → markdown via `adf_flatten.flatten()`
2. Extract acceptance criteria (3-stage: regex from description → custom field → bullet scan fallback)
3. Process comments, sprint, parent, linked issues, subtasks, attachments
4. Identify gaps (missing AC, empty description, no environment)
5. Return normalized dict

**Output:** Normalized ticket dict (matches ticket.schema.json shape)

**Edge Cases:**
- Unknown ADF nodes: render as `[ADF:<type>]` — never silently drop data (BR-10)
- Empty description: flag as gap, not error
- AC in custom field with nested JSON: handle both string and dict values

**Implementation:** `tools/normalize.py`