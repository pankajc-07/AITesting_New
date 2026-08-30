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

---

## 🔧 Setup (Root)

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