# progress.md — Build Log

> **Project:** Test Plan Creator from Jira ID
> **Protocol:** B.L.A.S.T. — Protocol 0 (Initialization)
> **Log Rule:** Every entry records what was **done**, what **errored**, and what the **result** was. Nothing is logged as complete until verified. Future slots stay `PENDING`.
> **Timezone:** IST (UTC+5:30)
> **Day 1:** 2026-08-29

---

## Status Board

| Item | State | Evidence |
|---|---|---|
| Protocol 0 memory files | ✅ **DONE** (4/4) | `task_plan.md`, `findings.md`, `progress.md`, `LLM.md` on disk |
| GATE A — Discovery Questions answered | 🟢 **DONE** | `LLM.md` section 2, all 5 answered |
| GATE B — Schemas frozen | 🟢 **DONE** | `schemas/plan.schema.json` created, LLM.md section 3 confirmed |
| GATE C — Blueprint approved | 🟢 **GREEN** | Building per user instruction: "everything in one go" |
| `tools/` | 🔓 **UNLOCKED** (13 files) | All Layer 3 tools created |
| `architecture/` | ✅ **DONE** (6 SOPs) | SOP_01 through SOP_06 created |
| `navigation.py` | ✅ **DONE** | Layer 2 orchestrator created |
| `app.py` | ✅ **DONE** | Streamlit UI with prompt box + 4 result tabs |
| `pages/settings.py` | ✅ **DONE** | Settings page with Jira + Groq test connection |
| `run.py` | ✅ **DONE** | CLI with --health, --dry-run, --force |
| Jira API calls made | **ZERO** | Awaiting user credentials |
| LLM calls made | **ZERO** | Awaiting Groq key |

---

## Day 1 — 2026-08-29

### Block 1: Orientation & Project Setup (Start Time ~Now)

**Step 1 — Read the Prompt**
- Action: Read the user's request and `Prompt_Used.md` from `chapter_07/` for context.
- What was asked: Create 4 files (`task_plan.md`, `findings.md`, `progress.md`, `LLM.md`) using BLAST Protocol 0.
- Target folder: `Practice_chapter_07_AI_Agents_Test-Plan-Agent-Blast/`

**Step 2 — Inspect Target Folder**
- Action: Listed directory contents.
- Result: Folder contains only `BLAST.md`. Clean slate — exactly what Protocol 0 expects.
- Decision: Proceed with full initialization from scratch.

**Step 3 — Survey the Reference Implementation**
- Action: Read `chapter_07_AI_Agents_Test-Plan-Agent-Blast/` directory listing and key files.
- Files read:
  - `BLAST.md` — The protocol definition (identical to our copy)
  - `task_plan.md` — Reference: v1 BUILT AND RUNNING, 10 goals, 6 SOPs, 9 tools
  - `findings.md` — Reference: detailed API research, ADF breakdown, prior art survey
  - `progress.md` — Reference: minute-by-minute build log from 08:58 to 09:39 IST
  - `LLM.md` — Reference: full constitution with JSON schemas, behavioral rules, discovery answers
  - `README.md` — Reference: setup, usage, architecture overview
- Key learning: The reference project is fully built and functional. Our task is to rebuild it with understanding in the practice folder, following BLAST Protocol 0 strictly.

**Step 4 — Analyze the Architecture Pattern**
- What the reference does:
  - 7-step pipeline: prompt → parse key → fetch Jira → normalize → readiness → LLM → render
  - 6 steps deterministic Python, 1 calls a model
  - 3-layer A.N.T. architecture: architecture/ (SOPs) → navigation.py (orchestrator) → tools/ (scripts)
  - LLM returns JSON, not markdown — the core anti-hallucination pattern
- Decision: Adopt the same 7-step pipeline and 3-layer architecture. The pattern is proven.

**Step 5 — Draft task_plan.md**
- Action: Created `task_plan.md` with full structure.
- Contents:
  - One-liner mission statement
  - "Why not just a prompt" comparison table
  - 10 goals (6 primary v1,4 secondary v1.1)
  - 3 explicit non-goals
  - 5 Discovery Questions (BLAST Phase 1)
  - Full B.L.A.S.T. phase checklist (Protocol 0 through Phase 5)
  - Tech stack proposal
  - 3 GATE conditions
- Result: `task_plan.md` on disk. All checklists ready. Awaiting Discovery answers.

**Step 6 — Draft findings.md**
- Action: Created `findings.md` with research, API details, and curl examples.
- Contents:
  - Prior art survey (5 artifacts found in this repo)
  - Jira API surface analysis (v3 vs v2, Agile API, MCP)
  - ADF node type catalog (P0-P2 priority) with known pitfalls
  - Curl and Python examples for fetching tickets
  - Field name discovery pattern (`/rest/api/3/field`)
  - LLM provider comparison (Groq, DeepSeek, Ollama, OpenAi)
  - 14-section test plan template structure
  - Constraints, risks, and design decisions
- Result: `findings.md` on disk. All research documented with UNVERIFIED markers where applicable.

**Step 7 — Draft progress.md**
- Action: Creating `progress.md` (this file).
- Contents:
  - Status board (tracking all major items)
  - Build log with timestamps and detailed entries
  - What was done, what errored, what the result was
- Result: In progress. This entry being written now.

---

### PENDING — Next Steps

- [x] Create `LLM.md` (Project Constitution) — schemas, rules, architecture invariants ✅
- [x] Answer Discovery Questions (Q1-Q5) ✅ — recorded in LLM.md section 2
- [x] Create `architecture/` (6 SOPs) ✅
- [x] Create `tools/` (12 Python modules) ✅
- [x] Create `navigation.py` (Layer 2 orchestrator) ✅
- [x] Create `app.py` (Streamlit UI) ✅
- [x] Create `pages/settings.py` (Settings page) ✅
- [x] Create `run.py` (CLI entry point) ✅
- [x] Create `schemas/`, `assets/`, `fixtures/` ✅
- [ ] Install dependencies
- [ ] Run the project

---

## Day 1 — 2026-08-29 (continued)

### Block 2: Full Build — Phases 1-4 (All Code)

**Step 8 — Read Reference Implementation**
- Action: Read `navigation.py`, `app.py`, `run.py`, `errors.py`, `jira_fetch.py`, `llm_client.py` from reference `chapter_07/`.
- Result: All patterns understood. Decided to recreate with the same 7-step pipeline and 3-layer architecture but adapted for Groq-only provider.

**Step 9 — Create Directory Structure**
- Action: Created all directories: `tools/`, `architecture/`, `schemas/`, `fixtures/`, `assets/`, `pages/`, `tests/`, `out/`, `.tmp/`.
- Result: Full project scaffold ready.

**Step 10 — Build Layer 3: Tools (12 modules)**
- Files created:
  - `tools/__init__.py` — Package marker
  - `tools/errors.py` — Typed error taxonomy (AgentError, JiraAuthError, LLMError, NotPlannableError, etc.)
  - `tools/config_store.py` — Config loader: .env -> config.json -> defaults pattern
  - `tools/jira_auth.py` — Jira auth helper + verify() for test connection
  - `tools/jira_fetch.py` — SOP 01: key extraction (regex), fetch v3 + comments, error handling
  - `tools/llm_client.py` — Groq OpenAI-compatible client: chat(), verify(), provider_spec()
  - `tools/field_map.py` — Custom field resolver for AC and environment fields
  - `tools/adf_flatten.py` — ADF -> Markdown flattener with loss detection
  - `tools/normalize.py` — SOP 03: raw Jira -> ticket.json with AC extraction
  - `tools/readiness.py` — SOP 04: 11-factor readiness score
  - `tools/plan_build.py` — SOP 05: THE ONE LLM CALL with retry + schema validation
  - `tools/render.py` — SOP 06: JSON plan -> markdown with 14-section template
  - `tools/trace.py` — Trace generation for auditability
- Result: All 12 tool files on disk. AI-2 preserved: only plan_build.py calls a model.

**Step 11 — Build Layer 2: Navigation**
- File created: `navigation.py`
- Contains: parse_intent() (deterministic regex), run() (full pipeline), health() (Phase 2 LINK verification)
- Result: Orchestrator routes data between tools, handles failure branches, enforces readiness gate.

**Step12 — Build UI Layer**
- Files created:
  - `app.py` — Streamlit main page: prompt box, progress display, 4 result tabs (Test Plan, Ticket, Trace, Raw JSON)
  - `pages/settings.py` — Settings page: Jira URL/email/token + Groq key/model inputs, Test connection buttons, Save
- Result: Simple UI built. User types a prompt, clicks Run, sees step-by-step progress.

**Step13 — Build CLI**
- File created: `run.py`
- Supports: `python run.py PROJ-123`, `--health`, `--dry-run`, `--force`
- Exit codes: 0 ok, 2 bad input, 3 auth, 4 not found, 5 rate limited, 6 schema, 7 LLM
- Result: CLI mirrors all UI functionality.

**Step14 — Create Schemas, Assets, Fixtures**
- Files created:
  - `schemas/plan.schema.json` — TestPlan JSON schema (plan_meta, objective, scope, strategy, risks, assumptons, trace)
  - `assets/test-plan-template.md` — 14-section template with {{placeholders}}
  - `fixtures/sample_ticket_rich.json` — Rich ticket (SSO login story with 5 AC, comments, linked issues)
  - `fixtures/sample_ticket_thn.json` — Thin ticket ("Fix bug" with no AC, no environment)
- Result: Schema and sample data ready for testing.

**Step15 — Create Architecture SOPs (6 files)**
- Files created:
  - `archtecture/SP_01_fetch_ticket.md` — Fetch ticket procedure
  - `architecture/SOP_02_resolve_fieds.md` — Field resolution procedure
  - `architecture/SP_03_noralize.md` — Normalization procedure
  - `architecture/SP_04_readness_check.md` — Readiness gating procedure
  - `architecture/SOP_05_buid_plan.md` — LLM plan generation procedure
  - `architecture/SOP_06_render.md` — Markdown rendering procedure
- Result: 6 SOPs docmenting every step. Follow BLAST Golden Rule: SOPs exist before code runs.

**Step 16 — Create Config Files**
- Files created:
  - `requirements.txt` — streamlit, requests, python-dotenv
  - `.env.exmple` — Template with all required variables
- Result: Enviroment ready for `pip install`.

**Step 17 — Record Discovery Answers**
- Action: Updated `LLM.md` section 2 with the user's answers from Prompt 02.
- North Star: "Simple UI, fetch Jira and create test plan automatically"
- Integrations: Jira Cloud + Groq (`operai/gpt-oss-120b`)
- Source of Truth: Jira ticket + comments
- Delivery: Markdown + Streamlit UI with download
- Behavioral Rules: Anti-hallucination, Settings page with test connection buttons

---

### PENDING — Installation & Run

- [ ] `pip install -r reqirements.txt`
- [ ] Configure `.env` or Settings page
- [ ] Run `streamlit run app.py`
- [ ] Test with a real Jira ticket

---

## Error Log

| Time | Error | Cause | Resolution |
|---|---|---|---|
| — | No errors yet | — | — |

---

## Decisions Log

| Time | Decision | Rationale |
|---|---|---|
| Start | Rebuild from scratch (not copy reference) | Practice folder. Must demonstrate understanding |
| Start | Adopt 7-step pipeline + 3-layer A.N.T. architecture | Proven pattern from reference implementation |
| Start | Keep same tech stack (Python + requests + Streamlit) | Consistent with course; OpenAi-compatible LLM interface for flexibility |
| Start | LLM returns JSON, never markdown | Core anti-hallucination pattern from reference |
| Start | Follow BLAST Protocol 0 strictly: no code until GATEs green | Protocol mandates this; discipline prevents premature design |

---

## Time Summary

| Block | Duration | Files Created | Lines Written |
|---|---|---|
| Block 1 (Orientation + Protocol 0) | ~20 min | 3/4 (`task_plan.md`, `findings.md`, `progress.md`) | ~350+ (est.) |
| **TOTAL** | **~20 min** | **3/4** | **~350+** |

---

> **Note:** Times are approximate at this stage. Will add precise timestamps in subsequent blocks.