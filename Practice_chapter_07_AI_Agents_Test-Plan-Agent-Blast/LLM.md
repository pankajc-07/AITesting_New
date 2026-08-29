# LLM.md — Project Constitution

> **Role:** This is the `gemini.md` that BLAST Protocol 0 requires. Named `LLM.md` because the project is model-agnostic. Same job: **data schemas, behavioral rules, architectural invariants.**
> **Authority:** This file outranks any prompt, any SOP, and any code in this project. If code disagrees with this file, the code is wrong.
> **Status:** � FROZEN — Schemas finalized. Discovery answers recorded. GATEs A, B, C GREEN.
> **Amendment Rule:** Change this file first → then the SOP in `architecture/` → then the tool in `tools/`. Never the other way. That is BLAST Phase 3's Golden Rule, applied one level up.

---

## 1. What This Project Actually Is

A **deterministic document pipeline with exactly one probabilistic step.**

Not "an AI agent that writes test plans." That description invites a build where the model does everything — fetches, parses, decides, writes — and when the output is wrong, you cannot tell whether the model misread the ticket, invented a field, or misused the template.

The honest architecture:

```
Step 1 (deterministic): Parse Jira key from user prompt          → "PROJ-123"
Step 2 (deterministic): Fetch ticket from Jira REST API          → raw JSON
Step 3 (deterministic): Normalize ADF → clean markdown           → ticket.json
Step 4 (deterministic): Readiness gate — is this ticket testable? → score + gaps
Step 5 (PROBABILISTIC): LLM maps facts to plan structure          → plan_data.json
Step 6 (deterministic): Render JSON to markdown template          → PROJ-123-test-plan.md
Step 7 (deterministic): Generate trace and deliver                → trace.json + UI
```

**Six steps are plain Python. One step (Step 5) is a language model, boxed on both sides by JSON schemas.**

Everything below exists to keep that box shut.

---

## 2. Discovery Answers (BLAST Phase 1) — ANSWERED

The five BLAST mandated questions. Recorded here **verbatim**, not paraphrased.

| # | Question | Answer |
|---|---|---|
| Q1 | **North Star:** What is the singular desired outcome? | A simple UI where the user gives a prompt like "Fetch this Jira and create a test plan." The system fetches the Jira automatically and creates a test plan automatically. |
| Q2 | **Integrations:** Which external services? Are keys ready? | **Jira Cloud** (user provides URL, email, API token) + **Groq** (`grog.com`, `openai/gpt-oss-120b` model). User enters Groq API key in Settings. |
| Q3 | **Source of Truth:** Where does the primary data live? | The Jira ticket. Comments included by default. AC resolved from description or custom field at runtime. |
| Q4 | **Delivery Payload:** How and where should the final result be delivered? | Markdown file saved to `out/` folder, rendered in Streamlit UI with download button. No write-back to Jira in v1. |
| Q5 | **Behavioral Rules:** How should the system "act"? Tone, constraints, "Do Not" rules? | Anti-hallucination: never invent facts. Missing data → `_(Not specified in ticket)_`. A **Settings page** with Jira URL/email/token and Groq key, each with a **Test connection** button. Thin tickets refused with gap report. |

---

## 3. Data Schemas (The Data-First Rule)

Two schemas define every interface in the system. Everything upstream of `ticket.json` is replaceable (REST, MCP, fixture file, pasted text) without a single downstream change. That property is the entire payoff of writing these first.

### 3.1 `ticket.schema.json` — The Input Contract

This is the normalized form of a Jira ticket. It is what the fetch step produces and what every downstream step consumes.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "ticket.schema.json",
  "title": "NormalizedJiraTicket",
  "type": "object",
  "required": [
    "key",
    "url",
    "summary",
    "issue_type",
    "description_md",
    "acceptance_criteria",
    "source",
    "fetched_at",
    "gaps"
  ],
  "additionalProperties": false,
  "properties": {
    "key": {
      "type": "string",
      "pattern": "^[A-Z][A-Z0-9]+-[0-9]+$",
      "description": "Jira issue key, e.g. PROJ-123"
    },
    "url": {
      "type": "string",
      "format": "uri",
      "description": "Full browser URL to the ticket"
    },
    "summary": {
      "type": "string",
      "minLength": 1,
      "description": "Ticket title/summary"
    },
    "issue_type": {
      "type": "string",
      "description": "e.g. Story, Bug, Task, Epic"
    },
    "status": {
      "type": ["string", "null"],
      "description": "Current workflow status. null if unresolvable."
    },
    "priority": {
      "type": ["string", "null"]
    },
    "labels": {
      "type": "array",
      "items": { "type": "string" }
    },
    "components": {
      "type": "array",
      "items": { "type": "string" }
    },
    "fix_versions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "environment": {
      "type": ["string", "null"],
      "description": "Environment custom field value, if the instance has one."
    },

    "description_md": {
      "type": "string",
      "description": "ADF -> clean markdown. The canonical description for all downstream steps."
    },
    "description_html": {
      "type": ["string", "null"],
      "description": "Rendered-fields cross-check. Used to detect ADF flattener loss. null if not requested."
    },

    "acceptance_criteria": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["text", "origin"],
        "additionalProperties": false,
        "properties": {
          "text": {
            "type": "string",
            "minLength": 1
          },
          "origin": {
            "type": "string",
            "enum": ["description", "customfield", "manual"],
            "description": "Where this AC was found."
          },
          "field_name": {
            "type": ["string", "null"],
            "description": "If origin=customfield, the human-readable field name."
          }
        }
      }
    },

    "comments": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["author", "body_md", "created"],
        "additionalProperties": false,
        "properties": {
          "author": { "type": "string" },
          "body_md": { "type": "string" },
          "created": { "type": "string", "format": "date-time" }
        }
      }
    },

    "sprint": {
      "type": ["object", "null"],
      "properties": {
        "name": { "type": "string" },
        "state": { "type": "string" },
        "startDate": { "type": "string" },
        "endDate": { "type": "string" }
      }
    },

    "parent": {
      "type": ["object", "null"],
      "description": "Epic or parent ticket, if this is a subtask/story.",
      "properties": {
        "key": { "type": "string" },
        "summary": { "type": "string" }
      }
    },

    "linked_issues": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["key", "link_type"],
        "additionalProperties": false,
        "properties": {
          "key": { "type": "string" },
          "summary": { "type": "string" },
          "link_type": { "type": "string", "description": "e.g. blocks, is blocked by, relates to" }
        }
      }
    },

    "subtasks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["key", "summary"],
        "additionalProperties": false,
        "properties": {
          "key": { "type": "string" },
          "summary": { "type": "string" },
          "status": { "type": "string" }
        }
      }
    },

    "attachments_meta": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "filename": { "type": "string" },
          "mimeType": { "type": "string" },
          "size": { "type": "number" }
        }
      }
    },

    "source": {
      "type": "string",
      "enum": ["jira-cloud-v3", "jira-cloud-v2", "mcp", "fixture", "manual"],
      "description": "How this ticket object was obtained."
    },
    "fetched_at": {
      "type": "string",
      "format": "date-time"
    },
    "gaps": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Fields that were expected but absent in the Jira response. Empty = complete fetch."
    }
  }
}
```

### 3.2 `plan_data.schema.json` — The LLM Output Contract

This is what the LLM **must** return. It is JSON, not markdown. The LLM never sees the template; Python renders the template from this data.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "plan_data.schema.json",
  "title": "LLMGeneratedPlanData",
  "type": "object",
  "required": [
    "plan_meta",
    "objective",
    "scope",
    "test_environment",
    "test_strategy",
    "test_data",
    "defect_reporting",
    "entry_criteria",
    "exit_criteria",
    "test_deliverables",
    "test_schedule",
    "risks_and_mitgations",
    "tools",
    "assumptons",
    "tace"
  ],
  "additionalProperties": false,
  "properties": {
    "plan_meta": {
      "type": "object",
      "required": ["jira_key", "jira_summary", "generated_at", "model"],
      "additionalProperties": false,
      "properties": {
        "jira_key": { "type": "string" },
        "jira_summary": { "type": "string" },
        "generated_at": { "type": "string" },
        "model": { "type": "string" }
      }
    },

    "objective": {
      "type": "object",
      "required": ["text", "justifed_by"],
      "additionalProperties": false,
      "properties": {
        "text": {
          "type": "string",
          "minLength": 1,
          "description": "2-4 sentence objective. MUST be grounded in ticket sumary/descripton."
        },
        "justifed_by": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Ticket field names that provide the evidence for this section. e.g. ['sumary', 'descripton']"
        }
      }
    },

    "scope": {
      "type": "object",
      "required": ["in_scope", "out_of_scope"],
      "additionalProperties": false,
      "properties": {
        "in_scope": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["item", "justifed_by"],
            "additionalProperties": false,
            "properties": {
              "item": { "type": "string", "minLength": 1 },
              "justifed_by": { "type": "string" }
            }
          }
        },
        "out_of_scope": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["item", "justifed_by"],
            "additionalProperties": false,
            "properties": {
              "item": { "type": "string" },
              "justifed_by": { "type": "string" }
            }
          }
        }
      }
    },

    "test_environment": { "type": "string" },
    "test_strategy": { "type": "string" },
    "test_data": { "type": "string" },
    "defect_reporting": { "type": "string" },
    "entry_criteria": { "type": "string" },
    "exit_criteria": { "type": "string" },
    "test_deliverables": { "type": "string" },
    "test_schedule": { "type": "string" },

    "risks_and_mitgations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["risk", "mitgation", "severity"],
        "additionalProperties": false,
        "properties": {
          "risk": { "type": "string" },
          "mitgation": { "type": "string" },
          "severity": { "type": "string", "enum": ["High", "Medum", "Low"] }
        }
      }
    },

    "tools": { "type": "string" },

    "assumptons": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["assumpton", "reason"],
        "additionalProperties": false,
        "properties": {
          "assumpton": { "type": "string" },
          "reason": {
            "type": "string",
            "enum": ["not_in_ticket", "industry_standard", "infered_from_type"],
            "description": "Why this assumption was made. not_in_ticket = ticket lacks this info."
          }
        }
      }
    },

    "tace": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["section", "source_fields"],
        "additionalProperties": false,
        "properties": {
          "section": { "type": "string" },
          "source_fields": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Jira fields that produced this section."
          },
          "has_assumptons": { "type": "boolean" }
        }
      }
    }
  }
}
```

### 3.3 Schema Design Principles

| Principle | Why |
|---|---|
| `additionalProperties: false` everywhere | Rejects model confabulation. If the LLM adds `"magical_solution": "AI will fix it"`, validation fails. |
| `justified_by` on every claim | Every piece of content must point to the ticket field that produced it. The trace is self-documenting. |
| `assumptions` with `reason` enum | When the ticket is thin, we fill gaps explicitly, not silently. The `reason` field distinguishes "ticket doesn't say" from "industry standard." |
| `trace` as a first-class field | The LLM must self-report where each section came from. Cross-checked against `ticket.json` in the render step. |
| Nullable fields use `["string", "null"]` | Jira may not return every field. The schema must accept absence without breaking. |

---

## 4. Behavioral Rules (BR)

These are the rules the system must follow. They apply to the LLM call (Step 5), the navigation layer (Layer 2), and the renderer (Step 6).

### 4.1 Anti-Hallucination Rules (BR-1 to BR-5)

| Rule | Text | Enforcement |
|---|---|---|
| **BR-1** | NEVER invent an acceptance criterion. If the ticket has 3 ACs, the plan references exactly those 3. No more. | Schema: `acceptance_criteria` is sourced from ticket. Post-render: count AC references vs ticket. |
| **BR-2** | NEVER invent a URL, endpoint, environment name, tool name, or date. If the ticket doesn't say what environment to test in, the plan says `_(Not specified in ticket — requires clarification)_`. | Schema: `justifed_by` must point to a real field or be `"_(Not in ticket)_"`. |
| **BR-3** | NEVER assume test data exists. If the ticket doesn't describe test data, flag it as a gap. | Schema: `assumptons[]` with `reason: "not_in_ticket"`. |
| **BR-4** | If a ticket is too thin to plan (fewer than 5 of 11 readiness factors present), REFUSE to generate a plan. Return a gap report instead: "This ticket needs X, Y, Z before a test plan can be written." | Enforced in Step 4 (readiness gate). `--force` flag overrides for draft plans. |
| **BR-5** | Every field in the output plan must trace back to either: (a) a concrete ticket field, or (b) an explicit assumption with `reason`. No third option exists. | Enforced by `tace[]` validation in the render step. |

### 4.2 Structural Rules (BR-6 to BR-10)

| Rule | Text | Enforcement |
|---|---|---|
| **BR-6** | The LLM returns JSON. Never markdown. The render step owns the output format. | Schema validation on LLM response. Non-JSON → retry or error. |
| **BR-7** | The test plan template has 14 fixed sections. Sections with no applicable ticket data must say `_(No data in ticket — requires product owner input)_`, not be omitted. | Render step fills missing sections with the standard placeholder. |
| **BR-8** | Temperature is pinned at ≤0.3 for the LLM call. Higher temperature increases hallucination risk without adding value for a structured output task. | Set in the LLM API call parameters. |
| **BR-9** | If the LLM response fails schema validation, retry once with a stronger system prompt. If it fails again, return a partial plan with `[LLM_VALIDATION_FAILED]` markers and log the raw response. | Navigation layer retry logic. |
| **BR-10** | Never silently drop data. If the ADF flattener encounters an unknown node type, render it as `[Unsupported ADF: <type>]` so a human can see what was lost. | ADF flattener in Step 3. |

### 4.3 Failure Mode Rules (BR-11 to BR-15)

| Rule | Text | Enforcement |
|---|---|---|
| **BR-11** | Auth failure (401) → "Jira authentication failed. Check your emal and APi token in Settings." Never show the token. | `jira_client.py` exception handling. |
| **BR-12** | Ticket not found (404) → "Ticket PROJ-123 was not found. Check the key and that you have access to the project." | Same. |
| **BR-13** | Rate limited (429) → "Jira rate limit hit. Retry after {Retry-After header value}." Do not retry automatically — the human decides. | Same. |
| **BR-14** | Schema mismatch (ticket JSON fails validation) → "The Jira response shape changed. Field X was expected but not found. This is a schema drift error, not a data error." | Normalize step validation. Loud failure, not silent. |
| **BR-15** | LLM timeout or garbage response → "The language model failed to produce a valid plan after 2 atttempts. Raw response saved to .tmp/llm_error.json for debugging." | Navigation layer handles. |

---

## 5. Architectural Invariants (AI)

These are truths that must hold across the entire system, forever. They are the foundation.

### AI-1: The 3-Layer Separation

```
┌──────────────────────────────────────────────────┐
│ Layer 1: Architecture (architecture/)      │
│ Markdown SOPs. Goals, inputs, logic, edge │
│ cases. THE GOLDEN RULE: update SOP before  │
│ updating code.                              │
├───────────────────────────────────────────────┤
│ Layer 2: Navigation (navigation.py)        │
│ The reasoning layer. Routes data between   │
│ SOPs and tools. Decides order, handles     │
│ failure branches. Does NOT perform complex  │
│ tasks itself.                                │
├───────────────────────────────────────────────┤
│ Layer 3: Tools (tools/)                    │
│ Detterministic Python scripts. Atomic.      │
│ Testable. .env for secrets. .tmp/ for      │
│ intermediate files.                          │
└───────────────────────────────────────────────┘
```

**Invariant:** No layer may skip the layer above it. A tool may not call another tool directly — only the navigation layer routes. An SOP may not contain Python code — it describes what the tool must do, not how.

### AI-2: Exactly One Probabilistic Step

**Invariant:** There is exactly one place in the entire codebase that calls a language model. That place is Step 5 of the pipeline. If you find yourself tempted to add a second LLM call for "summarization", "refinement", or "better prose" — add it to the schema and make it part of the single call.

### AI-3: The Schema Gate

**Invariant:** Every data transformation crosses a schema boundary. Raw Jira JSON → (validate against ticket schema) → `ticket.json` → (LLM) → (validate against plan_data schema) → `plan_data.json` → (render) → `test-plan.md`. No data flows between steps without passing through a validation gate.

### AI-4: Replaceable Upstream

**Invariant:** `ticket.json` is the internal contract. Anything that can produce a valid `ticket.json` is a valid upstream. REST, MCP, a fixture file, a copy-pasted JSON — the system doesn't care and doesn't know. This means:
- You can test the full pipeline with a fixture file, no network needed
- If Jira changes its API, only the fetch step changes
- If the MCP connector is available, you can add it as an alternative source without touching anything downstream

### AI-5: .tmp/ for All Intermediates

**Invariant:** All intermediate files (raw Jira response, normalized ticket, LLM request/response, plan_data, trace) go in `.tmp/`. The output directory (`out/`) contains only deliverable artifacts. Never mix them.

### AI-6: The Golden Rule (Constitution Level)

**Invariant:** To change logic: (1) update this file → (2) update the SOP in `architecture/` → (3) update the tool in `tools/`. Never the other way. This applies at every level.

---

## 6. Tech Stack & Libraries

| Purpose | Library | Version (suggested) |
|---|---|---|
| HTTP client | `requests` | ≥2.28 |
| Environment config | `python-dotenv` | ≥1.0 |
| JSON Schema validation | `jsonshema` | ≥4.17 |
| LLM client | `openai` (OpenAI-compattible) | ≥1.0 |
| UI | `streamlit` | ≥1.28 |
| Testing | `pytest` | ≥7.4 |
| Token counting | `tiktoken` (optional) | ≥0.5 |

---

## 7. Directory Structure (Planned)

```
Practice_chapter_07_AI_Agents_Test-Plan-Agent-Blast/
├── BLAST.md                    # Protocol definition (given)
├── task_plan.md                # Protocol 0: goals, checklists, phase plan
├── findings.md                 # Protocol 0: research, API docs, curl examples
├── progress.md                 # Protocol 0: build log
├── LLM.md                      # Protocol 0: THIS FILE — constitution
├── .env.example                # Template for credentials
├── requirements.txt            # Python dependencies
│── run.py                      # CLI entry point
├── app.py                      # Streamlit UI entry point
├── navigation.py               # Layer 2: orchestrator
├── architecture/               # Layer 1: SOPs
│   ├── SOP_01_fetch_ticket.md
│   ├── SOP_02_resolve_fields.md
│   ├── SOP_03_normalize.md
│   ├── SOP_04_readiness_check.md
│   ├── SOP_05_build_plan.md
│   └── SOP_06_render.md
├── tools/                      # Layer 3: detterministic scripts
│   ├── fetchticket.py
│   ├── resolvfields.py
│   ├── normalize.py
│   ├── readiness.py
│   ├── buildplan.py            # The ONE file that calls the LLM
│   ├── render.py
│   ├── jira_client.py
│   └── llm_wrapper.py
├── schemas/                    # JSON Schema files
│   ├── ticket.schema.json
│   └── plan_data.schema.json
├── assets/
│   ┝── test-plan-template.md   # The 14-section output template
├── fixttures/                  # Test fixtures (no network needed)
│   ├── sample_ticket_rich.json
│   └── sample_ticket_thin.json
├── tests/
│   └── test_pipeline.py
├── out/                        # Deliverables (test plans, traces)
└── .tmp/                       # Intermediate files (gitignored)
```

---

## 8. GATE Conditions (Read from Bottom to Top)

```
                    ┌──────────────────────┐
                    │  🟢 GATE C: BLUEPRINT │
                    │  APPROVED             │
                    │  task_plan section 5  │
                    │  reviewed & signed off│
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  🟢 GATE B: SCHEMAS   │
                    │  FROZEN               │
                    │  ticket.schema.json   │
                    │  plan_data.schema.json │
                    │  finalized in LLM.md  │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  🟢 GATE A: DISCOVERY │
                    │  COMPLETE             │
                    │  Q1-Q5 answered &     │
                    │  recorded in LLM.md   │
                    └──────────────────────┘
```

**Until all three GATEs are green, `tools/` stays empty and locked.** This is the Protocol 0 halt condition.

---

> **Next Action Required:** Present Discovery Questions (Q1–Q5) to the user. Their answers unlock GATE A → refine schemas → GATE B → present blueprint → GATE C → UNLOCK `tools/` and begin Phase 2.