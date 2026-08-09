## Plan: Jira Test Case Generator — Streamlit App

**TL;DR** — Build a two-screen Streamlit app that takes a Jira ticket ID from chat, fetches the ticket via Jira REST API, merges it into a test case prompt template, generates test cases via Ollama (local, default) or Groq (cloud fallback), and renders the result in a ChatGPT-style chat pane. All credentials live in `.env` (gitignored), persisted settings in a local JSON file.

---

## Phase 1: Project Scaffolding & Config Layer

**Steps**

1. **Create `.env` file** at `chapter_03_Local_TC_Genarator/.env` with placeholder keys:
   - `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `GROQ_API_KEY`, `LLM_PROVIDER` (default `ollama`), `OLLAMA_BASE_URL`, `OLLAMA_MODEL`
   - *User will fill in real credentials after creation.*

2. **Create `requirements.txt`** — dependencies: `streamlit`, `requests`, `python-dotenv`, `groq`
   - *parallel with step 1*

3. **Create `config_store.py`** — reads/writes a local `settings.json` (gitignored). Functions:
   - `load_settings()` → dict (falls back to `.env` values if `settings.json` missing)
   - `save_settings(settings_dict)` → writes to `settings.json`
   - `get_setting(key)` / `set_setting(key, value)`
   - On first run, seeds from `.env` if available
   - *depends on step 1*

4. **Update `.gitignore`** at workspace root — add `settings.json` and any other generated config files
   - *parallel with step 3*

**Relevant files**
- `chapter_03_Local_TC_Genarator/.env` — new, credential store
- `chapter_03_Local_TC_Genarator/requirements.txt` — new
- `chapter_03_Local_TC_Genarator/config_store.py` — new
- `.gitignore` (workspace root) — append entries

**Verification**
1. `config_store.py` runs standalone: `python config_store.py` prints loaded settings
2. `settings.json` is created on first save, excluded from git

---

## Phase 2: Backend Clients (Jira + LLM)

**Steps**

5. **Create `jira_client.py`** — Jira REST API wrapper:
   - `fetch_issue(issue_key: str)` → dict with `summary`, `description`, `acceptance_criteria`
   - Uses Basic Auth (email + API token) from `config_store.get_setting()`
   - Parses acceptance criteria from description (looks for "Acceptance Criteria" / "AC" section) or a custom field
   - Handles errors: invalid key, auth failure, network issues → returns structured error dict
   - *depends on step 3 (config_store)*

6. **Create `llm_client.py`** — LLM orchestrator with fallback:
   - `generate_test_cases(prompt: str, provider: str = None)` → str
   - **Ollama path**: POST to `{OLLAMA_BASE_URL}/api/generate` with model from config, stream=False
   - **Groq path**: Uses `groq` Python SDK, model `llama-3.1-8b-instant` (fast + cheap)
   - **Fallback logic**: Try Ollama → if connection refused/timeout → auto-switch to Groq → if Groq also fails → return error message
   - Provider override: if user selected "Groq" in settings, skip Ollama entirely
   - *depends on step 3 (config_store)*

**Relevant files**
- `chapter_03_Local_TC_Genarator/jira_client.py` — new
- `chapter_03_Local_TC_Genarator/llm_client.py` — new

**Verification**
1. `jira_client.py` can be tested with a mock or real Jira instance
2. `llm_client.py` standalone test: call `generate_test_cases("Hello")` and verify Ollama responds; stop Ollama and verify Groq fallback kicks in

---

## Phase 3: Streamlit UI — Settings Screen

**Steps**

7. **Create `pages/settings.py`** — Streamlit multipage settings screen:
   - Form fields: Jira Base URL, Jira Email, Jira API Token (password type), LLM Provider (selectbox: Ollama / Groq), Groq API Key (password type, shown only when Groq selected)
   - "Save Settings" button → calls `config_store.save_settings()`
   - "Test Connection" button for Jira: calls `jira_client.fetch_issue()` with a test key
   - "Test Connection" button for LLM: calls `llm_client.generate_test_cases()` with a simple prompt
   - Load current values from `config_store.load_settings()` on page load
   - *depends on steps 3, 5, 6*

**Relevant files**
- `chapter_03_Local_TC_Genarator/pages/__init__.py` — empty init file
- `chapter_03_Local_TC_Genarator/pages/settings.py` — new

**Verification**
1. Run `streamlit run app.py`, navigate to Settings page, fill form, save → `settings.json` updated
2. Test Connection buttons show success/error feedback

---

## Phase 4: Streamlit UI — Chat Screen (Main App)

**Steps**

8. **Create `app.py`** — Main Streamlit chat interface:
   - **Page config**: title "Jira Test Case Generator", layout "wide"
   - **Sidebar**: Quick status indicators (LLM provider active, Jira connected), link to Settings page
   - **Chat history**: Uses `st.session_state.messages` to store conversation
   - **Message rendering**: User messages on right, assistant (test cases) on left with markdown table rendering
   - **Input**: `st.chat_input()` at bottom
   - **On send**:
     1. Append user message to session state
     2. Parse Jira issue key from message using regex (`[A-Z]+-\d+`)
     3. If no key found → respond with "Please include a Jira issue key (e.g., QA-102)"
     4. Call `jira_client.fetch_issue(key)` → if error, show error in chat
     5. Load template from `templates/testcase_creator.md`
     6. Merge: replace `[FEATURE]` with issue summary, `[PASTE REQUIREMENTS HERE]` with description + acceptance criteria
     7. Call `llm_client.generate_test_cases(merged_prompt)`
     8. Render response as markdown in chat
   - **Loading states**: Show spinner during Jira fetch and LLM generation
   - *depends on steps 5, 6*

**Relevant files**
- `chapter_03_Local_TC_Genarator/app.py` — new

**Verification**
1. Run `streamlit run app.py`, type "create test cases for QA-102" → full flow executes
2. Test with Ollama running → test cases generated locally
3. Test with Ollama stopped → auto-fallback to Groq (if key configured)
4. Test with invalid Jira key → graceful error in chat

---

## Phase 5: Integration & Polish

**Steps**

9. **Create `README.md`** in `chapter_03_Local_TC_Genarator/` — setup instructions:
   - Prerequisites: Python 3.10+, Ollama running with `gemma3:1b`
   - Setup: `pip install -r requirements.txt`, copy `.env.example` to `.env`, fill credentials
   - Run: `streamlit run app.py`
   - *parallel with step 10*

10. **End-to-end smoke test** — run the full flow with real/placeholder credentials, verify:
    - Settings persist across restarts
    - Chat history maintained in session
    - Jira fetch → template merge → LLM generation → render works end-to-end
    - Fallback from Ollama to Groq works
    - Error states handled gracefully (no crash, user-friendly messages)

**Relevant files**
- `chapter_03_Local_TC_Genarator/README.md` — new

---

## Complete File Structure (Target)

```
chapter_03_Local_TC_Genarator/
├── .env                          # Credentials (gitignored, user-provided)
├── .gitignore                    # (append settings.json)
├── README.md                     # Setup & usage guide
├── requirements.txt              # streamlit, requests, python-dotenv, groq
├── app.py                        # Main chat screen (Streamlit entry point)
├── config_store.py               # Settings persistence (JSON file)
├── jira_client.py                # Jira REST API wrapper
├── llm_client.py                 # Ollama + Groq with fallback
├── settings.json                 # Runtime settings (gitignored, auto-generated)
├── pages/
│   ├── __init__.py
│   └── settings.py               # Settings configuration screen
├── Templates/
│   └── testcase_creator.md       # Existing prompt template (reuse as-is)
├── src/
│   ├── Finetune_Prompt.md        # Existing spec (unchanged)
│   ├── plan.md                   # This plan
│   └── application_sceenshot.png # Existing reference (unchanged)
└── Testcases_generated_from_local_olama.md  # Existing sample output (unchanged)
```

---

## Data Flow Diagram

```
User types "create test cases for QA-102"
    │
    ▼
app.py ──parse Jira key──► "QA-102"
    │
    ▼
jira_client.py ──GET /rest/api/2/issue/QA-102──► {summary, description, AC}
    │
    ▼
app.py ──load template──► Templates/testcase_creator.md
    │
    ▼
app.py ──merge──► filled prompt with ticket data
    │
    ▼
llm_client.py
    ├── Ollama available? ──Yes──► POST localhost:11434/api/generate ──► response
    └── Ollama down?    ──Yes──► Groq API (llama-3.1-8b-instant) ──► response
    │
    ▼
app.py ──render markdown──► Chat pane (test case table)
```

---

## Decisions

- **Config storage**: JSON file (`settings.json`) over SQLite — simpler, no ORM needed, human-readable for debugging
- **Template reuse**: The existing `Templates/testcase_creator.md` is used as-is; `[FEATURE]` and `[PASTE REQUIREMENTS HERE]` are replaced at runtime
- **Jira auth**: Basic Auth with email + API token (standard for Jira Cloud; works for Server with personal access tokens too)
- **Groq model**: `llama-3.1-8b-instant` — fast, cheap, good quality for test case generation
- **Ollama model**: `gemma3:1b` as specified in the prompt; configurable via settings
- **No database**: Chat history is in-memory only (`st.session_state`), lost on refresh — acceptable for an internal tool
- **Scope boundary**: Single Jira ticket → test cases only. No batch processing, no Jira write-back, no test management tool integration

---

## Verification (End-to-End)

1. `pip install -r requirements.txt` succeeds with no conflicts
2. `streamlit run app.py` launches without import errors
3. Settings page loads, saves, and persists across browser refresh
4. Chat: "create test cases for VALID-123" → fetches from Jira → generates test cases → displays in chat
5. Chat: "hello" (no Jira key) → prompts user to include a key
6. Chat: "create test cases for INVALID-999" → shows Jira error gracefully
7. Stop Ollama → send request → auto-fallback to Groq → response rendered
8. Switch provider to Groq in Settings → Ollama skipped entirely
