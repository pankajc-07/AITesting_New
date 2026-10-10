# AI Tester Blueprint 4x

A comprehensive learning repository for AI-powered software testing — from LLM basics to building AI agents that automate test plan creation.

---

## 📂 Repository Structure

| Chapter | Topic | Description |
|---|---|---|
| `chapter_01_LLM_Basics/` | LLM Fundamentals | Anti-hallucination techniques, attention mechanisms, ML/DL/AI concepts |
| `chapter_02_Prompt_Eng/` | Prompt Engineering | RICE_POT templates, test plan/case frameworks, Playwright & Selenium prompts |
| `chapter_03_Local_TC_Generator/` | Local Test Case Generator | Streamlit app with Ollama for local test case generation from Jira |
| `chapter_04_JobKitAI/` | Resume Helper | AI-powered resume tailoring tool |
| `chapter_05_JobTrackerAI/` | Job Tracker | React + Vite job application tracker with IndexedDB |
| `chapter_06_Branding_LinkedinSkills/` | Content Repurposing | Skill-based content repurposing pack |
| `chapter_07_AI_Agents_Test-Plan-Agent-Blast/` | **Test Plan Agent (Reference)** | Full B.L.A.S.T. implementation — Jira → Test Plan with Groq/DeepSeek |
| `chapter_08_n8n_Agents/` | n8n AI Agents | Jira fetch/create, Bug Triage, RCA, Social Media AI agent workflows for n8n |
| `chapter_09_LangFlow/` | LangFlow AI Agents | LangFlow-based Bug Triage agents (simple, agentic, UI-driven) + React chat UI |
| `chapter_10_RAG_Basics/` | RAG Explorer | Visual RAG pipeline — PDF ingest → chunk → embed (Ollama) → store (ChromaDB) → answer (Groq) |
| `chapter_11_RAG_Implementation/` | Naive RAG | Hands-on naive RAG implementation with data, n8n workflows, and local vector search |
| `chapter_12_RAG_QA_BuddyAI/` | RAG QA Buddy AI | RAG-powered QA assistant for answering testing questions |
| `chapter_13_MCP_Basics/` | MCP Basics | Introduction to Model Context Protocol fundamentals |
| `chapter_14_MCP_Create_VIBE/` | **MCP Create VIBE** | Build two MCP servers — TestCase Creator & TestSkill Finder — with 100+ AI testing skills |
| `chapter_15_Python_PyTest/` | Python PyTest | Python testing with PyTest framework |
| `ui_screenshotbugAIAgent/` | Screenshot → Bug Reporter | React + Vite UI that uploads screenshots to n8n → Groq vision → Jira bug creation |
| `Practice_chapter_07_AI_Agents_Test-Plan-Agent-Blast/` | **Test Plan Agent (Practice)** | Practice rebuild of the Test Plan Agent from scratch |

---

## � n8n AI Agents (Chapter 08)

Located in `chapter_08_n8n_Agents/`

### Agent Workflows (`Agents/`)

| Agent | File | Description |
|---|---|---|
| Fetch Jira Ticket | `01_FetchJIRATicket_AIAgent.json` | AI agent to fetch and summarize Jira tickets |
| Create Jira Ticket | `02_CreateJIRATicket_AIAgent.json` | AI agent to create Jira tickets from natural language |
| Fetch + Create TC (Local LLM) | `03_FetchJIRACreateTCAIAgent_Local_LLM_ollama.json` | Fetch Jira ticket & generate test cases using local Ollama LLM |
| Bug Triage | `04_BugTriageAIAgent.json` | AI agent for automated bug triage and prioritization |
| RCA (Root Cause Analysis) | `05_RCA_Chatgpt_Jira_Production_Bug_RCA_Automation.json` | Automated RCA for production bugs using ChatGPT + Jira |
| Social Media | `06_Social_Media_AIAgent.json` | AI agent for social media content generation |
| Social Post Generator | `07_Social_Post_Generator (Gemini+ Upload Post).json` | AI agent to generate & upload social posts using Gemini |

### Prompt Resources (`resources/`)

| Resource | Description |
|---|---|
| `01_Raw_BugTriage.prompt.md` | Raw bug triage prompt template |
| `02_ModifiedBugTriagePrompt.prompt.md` | Enhanced bug triage prompt with improvements |
| `03_RCA_AI_Agent.prompt.md` | Root Cause Analysis AI agent prompt |

### Import into n8n

1. Open your n8n instance
2. Go to **Settings → Import**
3. Select the `.json` workflow file from `chapter_08_n8n_Agents/Agents/`
4. Configure your Jira & LLM credentials in the workflow nodes

---

## �🧪 Practice: Test Plan Agent (B.L.A.S.T. Protocol)

Located in `Practice_chapter_07_AI_Agents_Test-Plan-Agent-Blast/`

### What It Does

Give it a Jira ticket ID → get back a formal, review-ready Test Plan markdown file. Every claim is traceable to a real field on the ticket. Nothing is invented.

### Architecture (A.N.T. 3-Layer)

```
┌─────────────────────────────────────────┐
│ Layer 1: Architecture (architecture/)    │
│ 6 Markdown SOPs defining every step     │
├─────────────────────────────────────────┤
│ Layer 2: Navigation (navigation.py)     │
│ Orchestrator — routes data, handles     │
│ failures, enforces readiness gate       │
├─────────────────────────────────────────┤
│ Layer 3: Tools (tools/)                 │
│ 12 deterministic Python modules.        │
│ Only ONE calls an LLM (AI-2 invariant)  │
└─────────────────────────────────────────┘
```

### Pipeline (7 Steps, 6 Deterministic)

```
Prompt → Parse Key → Fetch Jira → Normalize → Readiness → LLM → Render → Test Plan
         (regex)     (REST v3)    (ADF→md)    (gate)     (1 call) (template)
```

### Quick Start

```bash
cd Practice_chapter_07_AI_Agents_Test-Plan-Agent-Blast
pip install -r requirements.txt
cp .env.example .env   # Fill in your Jira + Groq credentials
streamlit run app.py
```

### CLI Usage

```bash
python run.py SCRUM-42                    # Generate a plan
python run.py "make a plan for SCRUM-42"  # Natural language
python run.py --health                    # Test connections
python run.py --dry-run SCRUM-42          # Fetch only, no LLM
python run.py --force SCRUM-42            # Plan even if ticket is thin
```

### Anti-Hallucination Rules

- **BR-1:** Never invent acceptance criteria
- **BR-2:** Never invent URLs, endpoints, dates, or tool names
- **BR-3:** Never assume test data exists
- **BR-4:** Refuse tickets below 5/11 readiness (gap report instead)
- **BR-5:** Every claim traces to a ticket field or explicit assumption
- **BR-6:** LLM returns JSON, never markdown — Python owns the template

### Tech Stack

- **UI:** Streamlit
- **LLM:** Groq (`openai/gpt-oss-120b`)
- **Jira:** Cloud REST API v3
- **Language:** Python 3.10+

### ECLIPSE.md — Selenium + Cucumber BDD Protocol

Located at `Practice_chapter_07_AI_Agents_Test-Plan-Agent-Blast/ECLIPSE.md`

A master system prompt for GitHub Copilot to build Selenium WebDriver + Cucumber BDD test automation in Eclipse IDE using the **E.C.L.I.P.S.E.** protocol (Establish, Connect, Layout, Implement, Polish, Scan, Export) and the **P.O.M.** 3-layer architecture (Page Objects, Step Definitions, Feature Files).

| Phase | Name | What It Covers |
|---|---|---|
| **E** | Establish | Feature discovery, page object map, browser matrix, test data strategy |
| **C** | Connect | Maven dependencies, WebDriver handshake, browser driver strategy, smoke ping |
| **L** | Layout | P.O.M. architecture, package conventions, SOPs for each layer |
| **I** | Implement | Code generation in BDD order (config → utils → pages → steps → features) |
| **P** | Polish | Locator audit, brittle XPath detection, refactoring, code review |
| **S** | Scan | Cucumber execution, 7-step debugging protocol, common failure patterns |
| **E** | Export | Cucumber/Extent/Allure reports, CI pipeline (Jenkins/GitHub Actions) |

**Key rules enforced:** No `Thread.sleep()`, no inline locators, no assertions in page objects, no XPath when CSS works, no implementation details in Gherkin steps, every scenario traceable to a requirement via `@jira-` tag.

---

## 🌊 LangFlow AI Agents (Chapter 09)

Located in `chapter_09_LangFlow/`

### What is LangFlow?

LangFlow is a low-code visual framework for building AI agent workflows. This chapter covers building Bug Triage AI agents — from a simple hello-world flow to an agentic multi-step triage pipeline, plus a React-based chat UI for user interaction.

### Agent Workflows (`AIAgents/`)

| Agent | File | Description |
|---|---|---|
| Hello World | `01_LangFlow_Simple_HelloWorld.json` | Minimal LangFlow pipeline — introduction to the visual builder |
| Bug Triage (Simple) | `002_AI4X_002_Bug_Triage_AI_Agent.json` | Single-step bug triage flow: input → LLM → output |
| Bug Triage (Agentic) | `03_AI4X_003_Bug_Triage_AI_Agent_Agentic.json` | Multi-step agentic triage with tool-calling and reasoning loops |
| Bug Triage (UI-Driven) | `004_AI4X_004_Bug_Triage_AI_Agent_Via_UI.json` | Triage flow designed to be triggered via REST API from a custom UI |
| Custom Command | `CustomCommandCode.json` | Custom LangFlow component code for extended functionality |

### Bug Triage UI (`ui_bugtriage/`)

A lightweight React (Vite) chat interface that calls the LangFlow REST API:

```bash
cd chapter_09_LangFlow/ui_bugtriage
npm install
npm run dev          # Starts on http://localhost:5180
```

| Feature | Details |
|---|---|
| Framework | React + Vite |
| API Backend | LangFlow REST API (`/api/v1/run/<flow-id>`) |
| Input | Jira ticket key (e.g., `VWO-51`) |
| Output | Rendered markdown with triage results & tables |
| Config | `.env.local` — `LANGFLOW_URL`, `LANGFLOW_FLOW_ID`, `LANGFLOW_API_KEY` |

### LangFlow Setup (from `Notes.md`)

```bash
mkdir langflow-qa && cd langflow-qa
pip install virtualenv
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install langflow
langflow run
```

### Quick Start (One Command)

From the project root, activate the existing `.venv` and start LangFlow:

```bash
# Windows (PowerShell / CMD)
.venv\Scripts\python.exe -m langflow run --host 127.0.0.1 --port 7860
```

Or simply **double-click** `chapter_09_LangFlow/start_langflow.bat` — no terminal needed.

Once running, open **http://127.0.0.1:7860** in your browser.

### Import into LangFlow

1. Open LangFlow UI (default: `http://localhost:7860`)
2. Go to **Settings → Import**
3. Select the `.json` workflow file from `chapter_09_LangFlow/AIAgents/`
4. Configure your LLM API keys and Jira credentials in the flow nodes

---

## � RAG Explorer (Chapter 10)

Located in `chapter_10_RAG_Basics/`

A visual RAG (Retrieval-Augmented Generation) pipeline you can watch happen. Point it at a PDF and see every stage: raw extraction, repair, chunks, 768-dimension vectors, similarity scores, and the exact prompt sent to the model.

| Stage | Tool | Where |
|---|---|---|
| Extract | pypdf | local |
| Normalise | regex | local |
| Chunk | word windows + overlap | local |
| Embed | `nomic-embed-text` via Ollama, 768d | **local** |
| Store + search | ChromaDB, cosine | **local** |
| Answer | `openai/gpt-oss-120b` via Groq | remote |

**The document never leaves your machine during ingest.** Embeddings run in Ollama, vectors sit in a local Chroma file. Only the 3 retrieved chunks go to Groq — and only when you use the Chat tab.

```bash
cd chapter_10_RAG_Basics
./run.sh          # Starts on http://localhost:5190
```

---

## 🔧 Naive RAG Implementation (Chapter 11)

Located in `chapter_11_RAG_Implementation/`

A hands-on naive RAG implementation covering the fundamentals of building a retrieval-augmented generation system from scratch. Includes data preparation, n8n workflow integration, and local vector search.

| Component | Path | Description |
|---|---|---|
| Naive RAG | `00_NAIVE_RAG/` | Core naive RAG implementation |
| Prompt Reference | `00_NAIVE_RAG/Prompt.md` | ChatGPT prompt used for building the naive RAG pipeline |
| Data | `00_NAIVE_RAG/data/` | Sample data for RAG pipeline |
| n8n Workflows | `00_NAIVE_RAG/n8n/` | n8n-based RAG automation workflows |

---

## 🧪 MCP Create VIBE (Chapter 14)

Located in `chapter_14_MCP_Create_VIBE/`

Build two production-grade MCP (Model Context Protocol) servers for AI-powered testing — a **TestCase Creator** and a **TestSkill Finder** — with a library of 100+ AI testing skills spanning the full STLC.

### What's Inside

| Component | Path | Description |
|---|---|---|
| Objective & Plan | `00_Objective.md`, `01_TestCreatorMCP.plan.md`, `02_prompt.md` | Project blueprint, architecture plan, and AI prompts |
| Test Data | `data/vwo_5000_test_cases.csv` | 5,000 real-world test cases for VWO application |
| Assets | `assets/` | Hero images and skill-map diagrams |

### TestCase Creator MCP (`testcase-creator-mcp/`)

A Python MCP server for creating, searching, exporting, and managing test cases.

| Module | Description |
|---|---|
| `src/tc_mcp/server.py` | MCP server entry point with tool registration |
| `src/tc_mcp/models.py` | Pydantic data models for test cases |
| `src/tc_mcp/repository.py` | CSV-backed test case storage and querying |
| `src/tc_mcp/tools/` | 7 tool modules: authoring, discovery, export, planning, quality, search, common |
| `tests/` | Pytest test suite with conftest fixtures |

### TestSkill Finder MCP (`testskill-finder-mcp/`)

A Python MCP server that catalogs and searches 100+ AI testing skills across the full STLC.

| Module | Description |
|---|---|
| `src/tsf_mcp/server.py` | MCP server with skill search, catalog, and workflow tools |
| `src/tsf_mcp/catalog.py` | Skill catalog loader and indexer |
| `src/tsf_mcp/search.py` | Semantic and keyword-based skill search |
| `src/tsf_mcp/tools/` | 3 tool modules: authoring, finder, workflow |
| `tests/` | Pytest test suite for catalog, search, and server |

### Skill Library (`skills/`) — 100+ AI Testing Skills

| STLC Phase | Skills | Count |
|---|---|---|
| 01-requirement-analysis | acceptance-criteria-writer, jira-requirement-analyzer, requirement-traceability-builder | 3 |
| 02-test-planning | risk-based-test-prioritizer, test-environment-planner, test-estimation-calculator, test-plan-generator, test-strategy-designer | 5 |
| 03-test-design | api-test-designer, bdd-scenario-writer, exploratory-charter-designer, mobile-test-designer, test-scenario-designer, test-technique-designer | 6 |
| 04-test-case-development | test-case-format-converter, test-case-reviewer, test-case-writer, test-data-generator | 4 |
| 05-test-execution | automation-script-generator, ci-failure-analyzer, qa-status-reporter, regression-suite-selector, test-execution-tracker | 5 |
| 06-defect-management | bug-reporter, bug-repro-minimizer, bug-triage-assistant, defect-trend-analyzer, rca-analyzer | 5 |
| 07-test-closure | qa-retrospective-facilitator, release-readiness-checker, test-closure-reporter, test-coverage-analyzer | 4 |

| Framework Pack | Skills | Count |
|---|---|---|
| ai-agent-pack | agent-guardrail-tester, agent-test-designer, agent-trajectory-evaluator, multi-agent-workflow-tester, prompt-injection-tester | 5 |
| api-pack | api-contract-tester, api-mock-designer, graphql-api-tester, postman-collection-builder, pytest-api-tester, restassured-api-tester | 6 |
| automation-pack | appium-mobile-test-generator, automation-framework-architect, flaky-test-quarantine-manager | 3 |
| cypress-pack | cy-api-tester, cy-ci-configurator, cy-component-tester, cy-custom-command-builder, cy-flaky-debugger, cy-intercept-mocker, cy-selector-strategist, cy-test-generator | 8 |
| llm-eval-pack | deepeval-test-writer, golden-dataset-builder, hallucination-test-designer, llm-eval-planner, llm-judge-rubric-designer, prompt-regression-tester, rag-evaluation-designer | 7 |
| mcp-pack | mcp-security-reviewer, mcp-server-scaffolder, mcp-server-tester, mcp-tool-designer, mcp-tool-selection-evaluator | 5 |
| performance-pack | frontend-performance-auditor, jmeter-test-plan-builder, k6-load-test-generator, locust-load-test-generator, performance-results-analyzer, performance-test-strategist | 6 |
| playwright-pack | pw-accessibility-auditor, pw-api-tester, pw-ci-configurator, pw-fixture-designer, pw-flaky-debugger, pw-locator-fixer, pw-network-mocker, pw-page-object-builder, pw-test-generator, pw-trace-analyzer, pw-visual-regression | 11 |
| security-pack | auth-session-tester, input-validation-tester, owasp-api-security-tester, owasp-web-test-designer, sca-vulnerability-triager, zap-dast-configurator | 6 |
| selenium-pack | se-cross-browser-runner, se-data-driven-designer, se-driver-manager, se-flaky-debugger, se-framework-scaffolder, se-grid-configurator, se-locator-strategist, se-page-object-builder, se-report-integrator, se-test-generator, se-wait-fixer | 11 |

### Quick Start

```bash
cd chapter_14_MCP_Create_VIBE

# TestCase Creator MCP
cd testcase-creator-mcp
uv sync
uv run pytest tests/

# TestSkill Finder MCP
cd ../testskill-finder-mcp
uv sync
uv run pytest tests/
```

---

## 📸 Screenshot to Bug Reporter (UI)

Located in `ui_screenshotbugAIAgent/`

A React + Vite front-end that uploads a screenshot, sends it to an n8n webhook, and gets back a Jira bug report drafted by Groq vision from what's actually visible in the image.

```
browser  ──POST /api/report──▶  Vercel function  ──▶  n8n webhook
(same origin, no CORS)          (N8N_WEBHOOK_URL,      Groq vision → Jira create
                                 server-side only)      → attach → Respond to UI
```

| Feature | Details |
|---|---|
| Framework | React + Vite |
| API Backend | n8n webhook (via Vercel serverless function) |
| Vision LLM | Groq (image → bug report) |
| Output | Jira ticket with screenshot attached |

```bash
cd ui_screenshotbugAIAgent
npm install
npm run dev
```

---

## �🔧 Setup (Root)

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # macOS/Linux

# Install per-chapter requirements as needed
pip install -r Practice_chapter_07_AI_Agents_Test-Plan-Agent-Blast/requirements.txt
```

---

## 📝 License

Educational project for learning AI-powered testing techniques.