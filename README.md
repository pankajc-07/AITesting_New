# AITester Blueprint 4x

AI-powered test automation blueprint.

## Overview

AITester Blueprint 4x — where we learn about:
- AI Agents
- MCPs (Model Context Protocol)
- RAG (Retrieval-Augmented Generation)
- LLM Evaluations
- LangChain
- LangFlow
- ATAN (AI Test Automation Network)
- Prompt Engineering (RICE POT framework)
- And many more things that make us AI-powered testers

---

## Project Structure

```
AITesterBlueprint4x/
├── chapter_01_LLM_Basics/          # LLM fundamentals, attention mechanisms, anti-hallucination
├── chapter_02_Prompt_Eng/          # Prompt engineering with RICE POT framework
│   ├── prompt_templates/           # Reusable prompt templates (testcase_creator, STLC)
│   └── RICE_POT_PlaywrightFramework/  # Enterprise Playwright + TypeScript framework
├── chapter_03_Local_TC_Genarator/  # Local Test Case Generator with Streamlit + Ollama
│   ├── src/                        # Application source code
│   │   ├── app.py                  # Main chat screen (Streamlit)
│   │   ├── pages/settings.py       # Settings configuration screen
│   │   ├── config_store.py         # Settings persistence layer
│   │   ├── jira_client.py          # Jira REST API wrapper
│   │   ├── llm_client.py           # Ollama + Groq LLM orchestrator
│   │   └── plan.md                 # Architecture & implementation plan
│   └── Templates/                  # LLM prompt templates
└── README.md
```

---

## RICE POT Playwright Framework

Enterprise-grade **Playwright + TypeScript** automation framework for Salesforce login testing, built using the RICE POT prompt engineering methodology.

### Tech Stack

| Layer | Technology |
|---|---|
| **Language** | TypeScript (ES2022, strict mode) |
| **Test Runner** | Playwright Test (`@playwright/test`) |
| **Browsers** | Chromium, Firefox, WebKit |
| **Locator Strategy** | Playwright semantic locators (`getByLabel`, `getByRole`, `getByText`) with xpath fallback |
| **Design Pattern** | Page Object Model (POM) |
| **Config** | Environment variables (`process.env`) |
| **Reporting** | HTML report + list reporter + screenshot/trace on failure |

### Quick Start

```bash
cd chapter_02_Prompt_Eng/RICE_POT_PlaywrightFramework

# Install dependencies
npm install

# Install Playwright browsers
npx playwright install chromium

# Set credentials (never hardcode!)
set SF_USERNAME=your@email.com
set SF_PASSWORD=yourpassword

# Run tests
npm test                 # headless, all browsers
npm run test:headed      # with browser UI
npm run test:debug       # step-through debugging
npm run test:report      # view HTML report
npm run lint             # TypeScript type-check
```

### Test Coverage (8 test cases)

| Suite | Tests |
|---|---|
| **valid-login.spec.ts** | UI elements render, Remember Me toggle, valid credentials → redirect |
| **invalid-login.spec.ts** | Wrong password, empty username, empty password, both empty, invalid email format |

### Framework Architecture

```
RICE_POT_PlaywrightFramework/
├── package.json
├── playwright.config.ts        # Multi-browser, timeout, screenshot/trace config
├── tsconfig.json               # Strict TypeScript config
└── src/
    ├── config/
    │   └── env.config.ts       # Env-var based configuration
    ├── fixtures/
    │   └── base-fixture.ts     # Extended test fixture with auto LoginPage init
    ├── pages/
    │   └── LoginPage.ts        # Page Object — 12 reusable action methods
    ├── tests/
    │   ├── valid-login.spec.ts
    │   └── invalid-login.spec.ts
    └── utils/
        └── test-helpers.ts     # generateRandomString, isValidEmailFormat
```

---

## Chapter 3: Local Test Case Generator (Streamlit + Ollama)

A **two-screen Streamlit application** that generates test cases from Jira tickets using a local LLM (Ollama) with automatic cloud fallback (Groq).

### Features

| Feature | Description |
|---|---|
| 💬 **Chat Interface** | ChatGPT-style UI — type a Jira key, get test cases |
| ⚙️ **Settings Screen** | Configure Jira credentials, LLM provider, API keys |
| 🦙 **Local LLM** | Uses Ollama (`gemma3:1b`) running locally — private & free |
| ☁️ **Cloud Fallback** | Auto-switches to Groq if Ollama is unavailable |
| 🔗 **Jira Integration** | Fetches ticket summary, description & acceptance criteria via REST API |
| 📥 **Download** | Export generated test cases as Markdown |

### Quick Start

```bash
cd chapter_03_Local_TC_Genarator/src

# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials (see .env.example)
# JIRA_BASE_URL=https://your-company.atlassian.net
# JIRA_EMAIL=you@company.com
# JIRA_API_TOKEN=your-jira-api-token
# GROQ_API_KEY=gsk_...  (optional, for fallback)

# Make sure Ollama is running with gemma3:1b
ollama serve

# Launch the app
streamlit run app.py
```

### Architecture

```
User: "create test cases for QA-102"
  → app.py parses Jira key
  → jira_client.py fetches ticket via REST API
  → Template merged with ticket data
  → llm_client.py: Ollama (default) or Groq (fallback)
  → Test cases rendered in chat with download option
```

### Tech Stack

| Layer | Technology |
|---|---|
| **UI** | Streamlit |
| **LLM (Primary)** | Ollama — `gemma3:1b` |
| **LLM (Fallback)** | Groq — `llama-3.1-8b-instant` |
| **Jira API** | REST API v2 (Basic Auth) |
| **Config** | `.env` + `settings.json` |

---

## License

MIT