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

## License

MIT