# SOP 01: Fetch Ticket from Jira

**Goal:** Given a Jira issue key, retrieve the full ticket as raw JSON from Jira Cloud REST API v3.

**Inputs:**
- `key`: Jira issue key (e.g., `PROJ-123`)
- Jira credentials from config (URL, email, API token)

**Tool Logic:**
1. Parse user prompt to extract key using regex (deterministic — not an LLM call)
2. Validate key format: `^[A-Z][A-Z0-9]+-[0-9]+$`
3. Call `GET /rest/api/3/issue/{key}?fields=...&expand=renderedFields,names,schema`
4. Fetch comments via `GET /rest/api/3/issue/{key}/comment` (paginated)
5. Return raw issue + metadata

**Output:** `{"issue": {...}, "_meta": {"site": "...", "requests": N, "api_version": "v3"}}`

**Edge Cases:**
- 401 → JiraAuthError, 404 → JiraNotFoundError, 429 → retry 3x, 5xx → retry 3x

**Implementation:** `tools/jira_fetch.py`