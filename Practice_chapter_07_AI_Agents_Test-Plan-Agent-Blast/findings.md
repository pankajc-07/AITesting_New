# findings.md — Research, Discoveries, Constraints

> **Project:** Test Plan Creator from Jira ID
> **Protocol:** B.L.A.S.T. — Protocol 0 (Initialization)
> **Date:** 2026-08-29
> **Rule:** Everything here is either verified against a real artifact in this repo, or marked `⚠️ UNVERIFIED` and turned into a Discovery Question. No confident guessing.

---

## 1. Prior Art Found in This Repository

The workspace already contains a working implementation in `chapter_07_AI_Agents_Test-Plan-Agent-Blast/`. This is both a blessing (proven patterns) and a constraint (must not blindly copy — this is a practice rebuild).

| Artifact | Path | What It Gives Us |
|---|---|---|
| Working Jira client | `chapter_03_Local_TC_Generator/src/jira_client.py` | Proven fetch + ADF-flatten + AC-extract path, with typed exceptions for 401/404/timeout |
| Credential loader | `chapter_03_Local_TC_Generator/src/config_store.py` | `.env` → `config.json` fallback with `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` |
| Full BLAST pipeline | `chapter_07_A_Agents_Test-Plan-Agent-Blast/` | Complete reference: `app.py`, `navigation.py`, 6 SOPs, 9 tools, schemas, tests |
| 14-section test plan template | `chapter_07_.../assets/test-plan-template.md` | The exact output format to target |
| Streamlit UI pattern | `chapter_03_.../src/app.py` and `chapter_07.../app.py` | Multi-page Streamlit with Settings page and prompt box |

**Key Insight 1.1:** The existing `jira_client.py` calls `/rest/api/2/issue/{key}` (v2 API) and defensively handles both string descriptions (v2) and ADF objects (v3) via `isinstance(description_raw, dict)`. On Jira Cloud, v3 returns ADF, v2 returns wiki-markup strings. Both are useful.

**Key Insight 1.2:** The existing solution has the LLM return **JSON, not markdown**. The rendering step is deterministic Python. This is the core anti-hallucination pattern: the model never touches the template.

**Key Insight 1.3:** The reference `chapter_07/` codebase maps directly to the BLAST 3-layer architecture:
- `architecture/` = 6 Markdown SOPs (Layer 1)
- `navigation.py` = orchestrator (Layer 2)
- `tools/` = 9 deterministic Python scripts (Layer 3)

---

## 2. Jira API Surface — Which Endpoints and Why

### 2.1 Core Ticket Fetch

| Option | Endpoint | Auth | When to Use |
|---|---|---|---|
| **Jira Cloud REST v3** | `GET /rest/api/3/issue/{issueIdOrKey}` | Basic Auth (email + API token, base64) | **Primary.** Description arrives as ADF (structured JSON). Current API. |
| **Jira Cloud REST v2** | `GET /rest/api/2/issue/{issueIdOrKey}` | Same | **Fallback.** Description as wiki-markup string. No ADF parsing needed. |
| **Jira Agile API** | `GET /rest/agile/1.0/issue/{issueIdOrKey}` | Same | **Supplement.** Better sprint/board/epic data for Scrum boards. |
| **Atlassian MCP** | Tool calls (no HTTP) | OAuth via VS Code connector | **Optional.** Zero setup if connector is active, but not portable. |

### 2.2 v3 vs v2 — The Difference That Matters

```
v3: description is an ADF document (JSON object with content arrays, marks, attrs)
v2: description is a plain wiki-markup string like "h2. Summary\n||Key||Value||"
```

**Recommendation:** Fetch v3 for structured data, fall back to v2 if ADF parsing fails. Both are cheap (one GET each, same auth).

### 2.3 Authentication

Jira Cloud uses **Basic Auth** with:
- Username: your Atlassian account email
- Password: an **API Token** (NOT your login password)

API Token creation: `https://id.atlassian.com/manage-profile/security/api-tokens` → "Create API token"

### 2.4 Expand Parameters

The `?expand=` query parameter controls how much data comes back:

| Expand Value | What You Get |
|---|---|
| `renderedFields` | HTMl-rendered description (cross-check for flattener loss) |
| `names` | Human-readable field names (maps `customfield_10034` → "Acceptance Criteria") |
| `transitions` | Available workflow transitions |
| `editmeta` | Field metadata (required, allowed values) |
| `schema` | Field type information |
| `operations` | Allowed operations on the issue |

**Recommended expand for v1:** `?expand=renderedFields,names,schema`

---

## 3. Curl / Request Examples

### 3.1 Fetch a Single Ticket (v3)

```bash
curl -X GET \
  "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123?expand=renderedFields,names,schema" \
  -H "Authorization: Basic $(echo -n 'your-email@example.com:your-api-token' | base64)" \
  -H "Accept: application/json"
```

### 3.2 Fetch a Single Ticket (v2 — Simpler Description)

```bash
curl -X GET \
  "https://your-domain.atlassian.net/rest/api/2/issue/PROJ-123" \
  -H "Authorization: Basic $(echo -n 'your-email@example.com:your-api-token' | base64)" \
  -H "Accept: application/json"
```

### 3.3 Python (requests) — The Pattern We'll Use

```python
import requests
import base64

JIRA_URL = "https://your-domain.atlassian.net"
JIRA_EMAL = "your-email@example.com"
JIRA_API_TOKEN = "your-api-token"
ISSUE_KEY = "PROJ-123"

auth_str = base64.b64encode(f"{JIRA_EMAL}:{JIRA_API_TOKEN}".encode()).decode()

response = requests.get(
    f"{JIRA_URL}/rest/api/3/issue/{ISSUE_KEY}",
    headers={
        "Authorization": f"Basic {auth_str}",
        "Accept": "application/json"
    },
    params={"expand": "renderedFields,names,schema"}
)

if response.status_code == 200:
    ticket = response.json()
elif response.status_code == 401:
    raise Exception("Authentication failed — check emal and API token")
elif response.status_code == 404:
    raise Exception(f"Ticket {ISSUE_KEY} not found")
else:
    raise Exception(f"Jira returned {response.status_code}: {response.text}")
```

### 3.4 Python (requests) — v2 Fallback

```python
# Same auth, different endpoint. Description is a plain string.
response = requests.get(
    f"{JIRA_URL}/rest/api/2/issue/{ISSUE_KEY}",
    headers={"Authorization": f"Basic {auth_str}"}
)
```

---

## 4. ADF (Atlassian Document Format) — What We're Dealing With

The v3 API returns description as an ADF document. It looks like:

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "As a user, I want to..."}
      ]
    },
    {
      "type": "codeBlock",
      "attrs": {"language": "json"},
      "content": [{"type": "text", "text": "{\"key\": \"value\"}"}]
    },
    {
      "type": "table",
      "content": [
        {"type": "tableRow", "content": [
          {"type": "tableHeader", "content": [...]},
          {"type": "tableCell", "content": [...]}
        ]}
      ]
    }
  ]
}
```

### ADF Node Types We Must Handle

| ADF Type | Markdown Equivalent | Priority |
|---|---|---|
| `doc` | (root container) | P0 |
| `paragraph` | Plain text block | P0 |
| `text` | Inline text (can have `marks` for strong, em, link, code) | P0 |
| `heading` | `#`, `##`, `###`... (`attrs.level` 1-6) | P0 |
| `bulletList` / `orderedList` | `- ` / `1. ` | P0 |
| `listItem` | List item content | P0 |
| `codeBlock` | ` ```language\ncode\n``` ` | P0 |
| `blockquote` | `> ` | P1 |
| `table`, `tableRow`, `tableHeader`, `tableCell` | GFm table (`\| col \|`) | P1 |
| `panel` (info/note/warning/error/success) | `> **ℹ️ Note:** ...` | P2 |
| `rule` | `---` | P2 |
| `mention` | `@username` | P2 |
| `hardBreak` | Newline | P1 |
| `mediaGroup`, `media` | `[attached: filename]` | P2 |
| `inlineCard` | `[link](url)` | P2 |
| `emoji` | Unicode emoji or `:shortcode:` | P2 |

**Strategy:** P0 + P1 covered in v1 flattener. P2 are nice-to-haves.

### Known Pitfalls

1. **Text marks can nest:** `{"type": "text", "text": "foo", "marks": [{"type": "strong"}, {"type": "em"}]}` → `***foo***`
2. **Unknown node types:** Must not crash. Log and render as `[Unsupported: <type>]`.
3. **Empty content arrays:** A `paragraph` with `"content": []` is a blank line.
4. **Acceptance Criteria location:** NOT a standard field. Usually in description (regex `h3. Acceptance Criteria` or `*Acceptance Criteria*`) or in a custom field. Must discover field name at runtime via `/rest/api/3/field` → match `"Acceptance Criteria"` name → get `customfield_XXXXX`.

---

## 5. Field Name Discovery — The Hidden Problem

Jira stores custom fields with keys like `customfield_10034`. The human-readable name "Acceptance Criteria" is in the field metadata, not the ticket.

### How to Discover Field Names

```bash
curl -X GET \
  "https://your-domain.atlassian.net/rest/api/3/field" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)"
```

Response:
```json
[
  {"id": "customfield_10034", "name": "Acceptance Criteria", "custom": true, "schema": {"type": "string"}},
  {"id": "customfield_10035", "name": "Story Points", "custom": true, "schema": {"type": "number"}},
  ...
]
```

**Strategy:** Fetch `/rest/api/3/field` once at startup (or once per session), build a `{name → key}` map. Use it to locate AC, environment, and any other custom fields.

⚠️ **UNVERIFIED:** The existing `jira_client.py` in `chapter_03/` attempts to find AC by scanning field *keys* for the substring `"acceptance"`. On Jira Cloud this will never match because keys are `customfield_10034`. This is a latent bug. Our approach (field metadata endpoint) fixes it.

---

## 6. LLM Provider Options

| Provider | Model | Endpoint | Notes |
|---|---|---|---|
| **Groq** | `openai/gpt-oss-120b` or similar | `https://api.groq.com/openai/v1` | Fast, free tier, OpenAi-compatible |
| **DeepSeek** | `deepseek-chat` | `https://api.deepseek.com/v1` | Cheap, good reasoning, OpenAi-compatible |
| **Ollama** | `llama3.1:8b` or similar | `http://localhost:11434/v1` | Local, free, no network needed after pull |
| **OpenAI** | `gpt-4o-mini` | `https://api.openai.com/v1` | Paid, best quality |

**Recommendation:** Use the OpenAi-compatible interface (`base_url` + `api_key` + `model`) so any provider works by changing config.

---

## 7. Output Test Plan Template Structure

Based on the reference in `chapter_07/`, a standard test plan should have these sections:

1. **Objective** — What are we testing and why
2. **Scope** — Inclusions, exclusions, assumptions
3. **Test Environment** — Hardware, software, browsers, devices
4. **Test Strategy** — Types of testing (functional, integration, performance, security...)
5. **Test Data** — What data is needed
6. **Defect Reporting** — How and where to log bugs
7. **Entry Criteria** — Conditions to start testing
8. **Exit Criteria** — Conditions to end testing
9. **Test Deliverables** — What documents/artifacts we produce
10. **Test Schedule** — Timeline and milestones
11. **Risks & Mitigations** — What could go wrong
12. **Tools** — What tools we'll use
13. **Approvals** — Who signs off
14. **Trace Matrix** — Requirements → test cases

**Anti-Hallucination Rule:** Every section that has no corresponding Jira data gets marked `_(No data in ticket — requires product owner input)_`. Never invent.

---

## 8. Constraints & Risks

### Constraints

| # | Constraint | Impact |
|---|---|---|
| C1 | This is a **practice rebuild** of `chapter_07/`. Must demonstrate understanding, not just copy. | Architecture decisions must be justified; code may differ from reference where we find better approaches. |
| C2 | The folder is **empty** except `BLAST.md`. We start from zero. | Must scaffold everything: directories, config, schemas, tools. |
| C3 | Must follow BLAST protocol strictly. | No code until GATE A/B/C are green. |
| C4 | No Jira credentials in workspace yet. | Phase 2 will need a `.env` file. |

### Risks

| # | Risk | Mitigation |
|---|---|---|
| R1 | Jira API rate limits (200 req/min on free tier) | Single-ticket fetch + field metadata fetch = 2 calls per run. Well within limits. |
| R2 | ADF format varies between Jira instances | Defensive parsing: handle unknown types gracefully, never crash. |
| R3 | LLM may hallucinate even with schema constraints | JSON schema + low temperature + system prompt rules + post-render audit. |
| R4 | Ticket too thin to create a meaningful plan | Readiness gate (SOP_04 pattern): score the ticket, refuse below threshold with a gap report. |

---

## 9. Design Decisions (Recorded for Rationale)

| # | Decision | Rationale |
|---|---|---|
| D1 | LLM returns JSON, not markdown | The model is probabilistic; formatting is deterministic. Let Python own the template. |
| D2 | One LLM call, not multiple | Every call is a chance for drift. Box it into one structured response. |
| D3 | Streamlit UI + CLI both supported | UI for demo/ux, CLI for automation/pipes. Same `navigation.py` core. |
| D4 | `.env` + Settings page for credentials | No credentials in code. Settings page has "Test connection" buttons. |
| D5 | `ticket.json` is the internal contract | Upstream (REST, MCP, fixture, pasted text) is replaceable. Downstream doesn't care how the ticket arrived. |

---

> **Next:** Answer Discovery Questions → freeze schemas in `LLM.md` → unlock `tools/`.