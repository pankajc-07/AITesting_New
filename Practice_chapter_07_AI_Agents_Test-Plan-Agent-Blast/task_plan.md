# task_plan.md — Test Plan Creator from Jira ID

> **Protocol:** B.L.A.S.T. — Protocol 0 (Initialization)
> **Project:** Practice_chapter_07_AI_Agents_Test-Plan-Agent-Blast
> **Created:** 2026-08-29
> **Status:** 🔴 PLANNING — No code written. Protocol 0 in progress.
> **Lock:** `tools/` EMPTY and LOCKED until GATE A, B, C are green.

---

## 1. The One-Line Mission (North Star)

**Given a Jira ticket ID, automatically fetch the ticket and produce a formal, review-ready Test Plan in markdown.**

The user types something like _"Fetch SCRUM-42 and create a test plan"_ into a prompt box, and the system:

1. Parses the Jira key from the prompt
2. Fetches the full ticket from Jira Cloud REST API
3. Normalizes the data into a clean structured object
4. Reasons about what testing is needed (and what gaps exist)
5. Renders a professional test plan markdown file
6. Delivers it back to the user with a trace of where every claim came from

---

## 2. Why This Is Not Just "Ask ChatGPT to Write a Test Plan"

| Naive approach problem | What this project does instead |
|---|---|
| Model hallucinates ACs, endpoints, environments | Schema-validated ticket object; missing fields are marked `_(Not in ticket)_`, never invented |
| Output shape changes every run | Frozen template; LLM fills slots, doesn't choose structure |
| Re-run gives different results | Layers 1 & 3 are deterministic Python; only Layer 2 is probabilistic |
| Jira changes break silently | Every fetch validated against schema; shape change = loud failure at boundary |
| No audit trail | `trace.json` maps every generated sentence back to its Jira source field |

---

## 3. Goals

### 3.1 Primary Goals (v1 — Definition of Done)

- [ ] **G1 — Fetch:** Pull full Jira ticket (summary, description, AC, type, status, priority, labels, components, fix versions, sprint, comments, attachments metadata) from Jira Cloud REST API
- [ ] **G2 — Normalize:** Flatten ADF (Atlassian Document Format) into clean markdown → emit one `ticket.json` conforming to a defined schema
- [ ] **G3 — Reason:** Map ticket facts onto a formal test plan template. Keep only scope areas the ticket actually justifies
- [ ] **G4 — Render:** Write `<JIRA-KEY>-test-plan.md` with zero leftover `{{placeholders}}` and zero authoring comments
- [ ] **G5 — Trace:** Emit `trace.json` mapping each section back to the Jira field(s) that produced it
- [ ] **G6 — Fail Loudly:** Auth failure, missing ticket, permission denied, rate limit, and schema mismatch each produce a distinct, actionable error — never a half-written plan

### 3.2 Secondary Goals (v1.1 — after v1 signed off)

- [ ] **G7:** `.docx` export for client-facing delivery
- [ ] **G8:** Batch mode — one epic → all child stories, one plan each
- [ ] **G9:** Write-back — post finished plan as a Jira comment or Confluence page
- [ ] **G10:** Diff mode — ticket changed after plan; show what to absorb

### 3.3 Explicit Non-Goals (v1)

- ❌ Real-time collaboration or multi-user
- ❌ Jira Server/Data Center support (Cloud only for v1)
- ❌ Custom test plan templates (one standard template for v1)
- ❌ Integration with test management tools (TestRail, Zephyr, etc.)

---

## 4. Discovery Questions (BLAST Phase 1 — Awaiting Answers)

These are the 5 mandatory BLAST discovery questions. Coding is **locked** until these are answered.

| # | Question | Status |
|---|---|---|
| Q1 — **North Star** | What is the singular desired outcome? ("Create a test plan from Jira" — confirm this is the full scope, or add specifics) | 🔴 UNANSWERED |
| Q2 — **Integrations** | Which Jira instance? Cloud or Server? Is the API token ready? Any other integrations (LLM provider, Confluence)? | 🔴 UNANSWERED |
| Q3 — **Source of Truth** | Which Jira fields are mandatory to read? Should comments be included? Should linked issues be expanded? | 🔴 UNANSWERED |
| Q4 — **Delivery Payload** | Output format: markdown file only? Also `.docx`? Delivered where — local file, Streamlit UI, Jira comment? | 🔴 UNANSWERED |
| Q5 — **Behavioral Rules** | Anti-hallucination rules confirmed? What tone? What to do when the ticket is too thin to plan? | 🔴 UNANSWERED |

---

## 5. Phase Checklist (B.L.A.S.T.)

### 🔵 Protocol 0 — Initialize
- [x] Create `task_plan.md` (this file)
- [x] Create `findings.md`
- [x] Create `progress.md`
- [x] Create `LLM.md` (Project Constitution)
- [ ] Answer Discovery Questions (Q1–Q5)
- [ ] Freeze data schemas in `LLM.md`
- [ ] Blueprint approved → **UNLOCK `tools/`**

### 🟢 Phase 1 — B: Blueprint
- [ ] Answer all 5 Discovery Questions
- [ ] Define JSON Data Schema (Input/Output) in `LLM.md`
- [ ] Research prior art in this workspace (`chapter_03/`, `chapter_07/`)
- [ ] Design the pipeline: prompt → parse → fetch → normalize → reason → render → deliver
- [ ] Choose tech stack

### ⚡ Phase 2 — L: Link
- [ ] Set up `.env` with Jira credentials
- [ ] Verify Jira API connection (test fetch a known ticket)
- [ ] Verify LLM provider connection (test a minimal completion)
- [ ] Build minimal `tools/` scripts for connectivity verification

### ⚙️ Phase 3 — A: Architect (3-Layer Build)
- [ ] **Layer 1 — Architecture:** Write SOPs in `architecture/`
  - [ ] SOP_01: Fetch ticket from Jira
  - [ ] SOP_02: Resolve and normalize fields
  - [ ] SOP_03: Normalize to `ticket.json`
  - [ ] SOP_04: Readiness check (is this ticket testable?)
  - [ ] SOP_05: Build test plan (the LLM step)
  - [ ] SOP_06: Render to markdown
- [ ] **Layer 2 — Navigation:** Build `navigation.py` (orchestrator)
- [ ] **Layer 3 — Tools:** Build deterministic Python scripts in `tools/`

### ✨ Phase 4 — S: Stylize
- [ ] Format test plan markdown for professional delivery
- [ ] Build Streamlit UI with prompt box and download button
- [ ] Add Settings page for credentials
- [ ] User feedback loop

### 🚀 Phase 5 — T: Trigger
- [ ] End-to-end test with real Jira ticket
- [ ] Run pipeline with thin ticket → verify refusal
- [ ] Run pipeline with rich ticket → verify complete plan
- [ ] Validate `trace.json` against output

---

## 6. Tech Stack (Proposed, Subject to Discovery)

| Layer | Technology | Rationale |
|---|---|---|
| Runtime | Python 3.10+ | Consistent with rest of course repo |
| HTTP | `requests` | Simple, no async needed for single-ticket fetch |
| Config | `python-dotenv` + `.env` | Already used in `chapter_03/` |
| LLM | OpenAI-compatible API (Groq, DeepSeek, or Ollama) | Flexible; one interface for any provider |
| UI | Streamlit | Fast to build, already used in `chapter_03/`, `chapter_07/` |
| Testing | `pytest` + fixtures | Deterministic tools should be testable without network |
| Schema validation | `jsonschema` | Validate `ticket.json` and LLM output against JSON Schema |

---

## 7. GATE Conditions (Must Be GREEN to Write Code)

| GATE | Condition | Status |
|---|---|---|
| **GATE A** | All 5 Discovery Questions answered | 🔴 |
| **GATE B** | Data schemas frozen in `LLM.md` | 🔴 |
| **GATE C** | Blueprint reviewed and approved | 🔴 |

---

> **Next step:** Present Discovery Questions to the user. Once answered, populate `LLM.md` with schemas, then unlock `tools/`.