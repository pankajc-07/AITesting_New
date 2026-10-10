# TestCreator MCP (TC MCP) — Build Plan

> **Status:** Planning | **Framework:** FastMCP | **Language:** Python 3.10+

---

## 1. What Are We Building?

A **TestCreator MCP Server** — a shareable MCP (Model Context Protocol) server that any QA engineer or developer can connect to their AI assistant (Claude Desktop, VS Code Copilot, Cursor, etc.) to:

- **Search** 5,000+ real VWO test cases by module, type, priority, browser, device, or keyword
- **Create** new test cases with structured fields and auto-generated IDs
- **Update** existing test cases (status, priority, steps, etc.)
- **Export** test cases to CSV, JSON, or Markdown
- **Plan** test coverage — see what's tested vs. what's missing per module
- **Validate** test case quality — check for missing fields, duplicate summaries, stale statuses

The data source is `data/vwo_5000_test_cases.csv` — 5,000 real-world test cases across 17 VWO modules.

---

## 2. CSV Data Profile (What We're Working With)

| Column | Type | Example | Cardinality |
|--------|------|---------|-------------|
| `Issue Type` | Enum | `Test` | 1 value |
| `Issue Key` | String | `VWO-1001` | 5,000 unique |
| `Summary` | String | `[SmartCode] Functional: ensure data collection` | 5,000 unique |
| `Description` | Text | `As a QA engineer, ensure the data collection...` | 5,000 unique |
| `Priority` | Enum | `Medium` | 4 values (Highest, High, Medium, Low) |
| `Component` | Enum | `SmartCode` | 17 modules |
| `Labels` | String | `smartcode functional regression` | ~50 unique |
| `Test Type` | Enum | `Functional` | 9 types |
| `Preconditions` | Text | `A VWO account with access to...` | varies |
| `Steps` | Text | `1. Log in... \| 2. Navigate...` | pipe-delimited |
| `Expected Result` | Text | `The data collection works as specified...` | varies |
| `Browser` | Enum | `Chrome 148` | 4 browsers |
| `Device` | Enum | `mobile (iOS)` | 4 devices |
| `Status` | Enum | `Ready` | 4 statuses |

### Key Distributions

| Dimension | Top Values |
|-----------|-----------|
| **Modules (17)** | Reports (333), Personalization (310), Feature Rollout (309), Surveys (307), Integrations (306) |
| **Test Types (9)** | Functional (1,516), Negative (810), UI/UX (515), API (415), Boundary (406) |
| **Priorities (4)** | Medium (2,198), High (1,546), Low (860), Highest (396) |
| **Statuses (4)** | Ready (2,234), Automated (1,594), Draft (757), Deprecated (415) |
| **Browsers (4)** | Safari 19 (1,308), Firefox 141 (1,267), Chrome 148 (1,233), Edge 148 (1,192) |
| **Devices (4)** | Desktop (1,266), Mobile Android (1,264), Mobile iOS (1,256), Tablet (1,214) |

---

## 3. Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                    AI Assistant                           │
│  (Claude Desktop / VS Code Copilot / Cursor)             │
└──────────────────────┬───────────────────────────────────┘
                       │ MCP Protocol (stdio)
┌──────────────────────▼───────────────────────────────────┐
│                 TC MCP Server (FastMCP)                   │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ SEARCH   │  │ AUTHOR   │  │ EXPORT   │  │ PLAN    │ │
│  │ Tools    │  │ Tools    │  │ Tools    │  │ Tools   │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘ │
│       │              │              │              │     │
│  ┌────▼──────────────▼──────────────▼──────────────▼───┐ │
│  │              Repository Layer                        │ │
│  │  (CSV-backed, in-memory index, Pydantic models)     │ │
│  └──────────────────────┬──────────────────────────────┘ │
│                         │                                │
│  ┌──────────────────────▼──────────────────────────────┐ │
│  │         data/vwo_5000_test_cases.csv                │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| MCP Framework | **FastMCP** | Clean decorator-based API, built-in tool/prompt/resource support |
| Data Models | **Pydantic v2** | Type-safe validation, serialization, auto-generated JSON schemas |
| Data Store | **CSV + in-memory index** | Zero dependencies, fast reads, easy to share (single file) |
| Search | **Python `filter` + regex** | Simple, fast enough for 5K rows, no external DB needed |
| Testing | **pytest** | Standard Python testing, fast, well-supported |

---

## 4. Tool Catalog — What the MCP Server Exposes

### 4.1 SEARCH & DISCOVERY Tools

These are the most-used tools — QA engineers will constantly search for existing test cases.

| # | Tool Name | What It Does | Key Parameters |
|---|-----------|-------------|----------------|
| 1 | `search_test_cases` | Full-text + field-filtered search across all 5,000 test cases | `query` (keyword), `component`, `test_type`, `priority`, `status`, `browser`, `device`, `limit` |
| 2 | `get_test_case` | Fetch a single test case by its Issue Key | `issue_key` (e.g., `VWO-1001`) |
| 3 | `list_components` | List all 17 VWO modules with test case counts | none |
| 4 | `list_test_types` | List all 9 test types with counts | none |
| 5 | `get_test_case_count` | Get aggregate counts by any dimension | `group_by` (component, test_type, priority, status, browser, device) |
| 6 | `find_related_test_cases` | Find test cases related to a given one (same module + type) | `issue_key` |

### 4.2 AUTHORING Tools

These let QAs create and modify test cases directly through their AI assistant.

| # | Tool Name | What It Does | Key Parameters |
|---|-----------|-------------|----------------|
| 7 | `create_test_case` | Create a new test case with auto-generated Issue Key | `summary`, `description`, `priority`, `component`, `test_type`, `preconditions`, `steps`, `expected_result`, `browser`, `device` |
| 8 | `update_test_case` | Update fields of an existing test case | `issue_key`, then any subset of fields to update |
| 9 | `update_test_case_status` | Quick status change (Ready → Automated, Draft → Ready, etc.) | `issue_key`, `new_status` |
| 10 | `delete_test_case` | Soft-delete (mark as Deprecated) a test case | `issue_key` |

### 4.3 EXPORT Tools

Share test cases with the team in different formats.

| # | Tool Name | What It Does | Key Parameters |
|---|-----------|-------------|----------------|
| 11 | `export_test_cases` | Export filtered test cases to CSV, JSON, or Markdown | `format` (csv/json/md), `component`, `test_type`, `status`, `output_path` |
| 12 | `export_test_case` | Export a single test case as formatted Markdown | `issue_key` |

### 4.4 PLANNING & COVERAGE Tools

Strategic tools for test managers and leads.

| # | Tool Name | What It Does | Key Parameters |
|---|-----------|-------------|----------------|
| 13 | `get_coverage_report` | Per-module coverage: count by test type, priority, status | `component` (optional, all if omitted) |
| 14 | `get_coverage_gaps` | Identify modules with zero test cases for a given test type or priority | `test_type`, `priority` |
| 15 | `generate_test_plan_outline` | Generate a structured test plan outline for a module | `component`, `include_test_types` |

### 4.5 QUALITY & VALIDATION Tools

Ensure test case quality and consistency.

| # | Tool Name | What It Does | Key Parameters |
|---|-----------|-------------|----------------|
| 16 | `validate_test_case` | Check a test case for completeness (missing fields, short steps, etc.) | `issue_key` |
| 17 | `find_duplicates` | Find potentially duplicate test cases by similar summary | `component` (optional), `threshold` |
| 18 | `get_stale_test_cases` | Find Draft or Deprecated test cases older than N days | `days` (default 30) |

---

## 5. Project Structure

```
chapter_14_MCP_Create_VIBE_Practice/
├── 00_Objective.md                    # Chapter objective
├── 01_TestCreatorMCP.plan.md          # ← THIS FILE
├── data/
│   └── vwo_5000_test_cases.csv        # 5,000 test cases (source of truth)
├── testcase-creator-mcp/              # The MCP server project
│   ├── pyproject.toml                 # Dependencies: fastmcp, pydantic, pytest
│   ├── README.md                      # Setup & usage instructions
│   ├── src/
│   │   └── tc_mcp/
│   │       ├── __init__.py
│   │       ├── server.py              # FastMCP server entry point
│   │       ├── config.py              # Paths, constants, settings
│   │       ├── models.py              # Pydantic models (TestCase, SearchFilter, etc.)
│   │       ├── repository.py          # CSV read/write, in-memory index, queries
│   │       ├── resolver.py            # Path resolution (find data file)
│   │       ├── validation.py          # Test case quality checks
│   │       ├── ranking.py             # Relevance scoring for search results
│   │       ├── prompts.py             # MCP prompt templates
│   │       ├── resources.py           # MCP resource URIs
│   │       └── tools/
│   │           ├── __init__.py
│   │           ├── search.py          # Tools 1-6: search & discovery
│   │           ├── authoring.py       # Tools 7-10: create, update, delete
│   │           ├── export.py          # Tools 11-12: CSV/JSON/MD export
│   │           ├── planning.py        # Tools 13-15: coverage & planning
│   │           └── quality.py         # Tools 16-18: validation & quality
│   └── tests/
│       ├── conftest.py                # Shared fixtures (sample data, temp CSV)
│       ├── test_repository.py         # Repository layer tests
│       ├── test_tools_search.py       # Search tool tests
│       ├── test_tools_authoring.py    # Authoring tool tests
│       ├── test_tools_export.py       # Export tool tests
│       ├── test_tools_planning.py     # Planning tool tests
│       └── test_tools_quality.py      # Quality tool tests
```

---

## 6. Key Design Decisions

### 6.1 Why FastMCP?

| Feature | Benefit |
|---------|---------|
| `@mcp.tool()` decorator | Clean, minimal boilerplate — one decorator per tool |
| Auto-generated JSON schemas | From Pydantic model type hints — no manual schema writing |
| Built-in `mcp.run()` | stdio transport works out of the box with Claude Desktop |
| Prompt & Resource support | We can add reusable prompt templates and data resources |

### 6.2 Why CSV + In-Memory Index?

- **Zero dependencies** — no SQLite, no PostgreSQL, no Docker
- **Shareable** — one CSV file is the entire database
- **Fast enough** — 5,000 rows with Python dict lookups is sub-millisecond
- **Git-friendly** — CSV diffs are readable

### 6.3 Search Strategy

For 5,000 records, we don't need Elasticsearch or vector DBs. A simple approach:

1. **Exact filters first** — component, test_type, priority, status, browser, device
2. **Keyword search** — case-insensitive substring match on summary + description
3. **Ranking** — score by: exact match > prefix match > substring match > description match
4. **Pagination** — `limit` + `offset` for large result sets

### 6.4 Auto-Generated Issue Keys

New test cases get auto-generated keys: `VWO-{max_existing + 1}`. The server scans the CSV to find the highest existing key number.

---

## 7. MCP Configuration (claude_desktop_config.json)

```json
{
  "mcpServers": {
    "testcase-creator": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/path/to/chapter_14_MCP_Create_VIBE_Practice/testcase-creator-mcp",
        "run",
        "tc-mcp"
      ]
    }
  }
}
```

The `tc-mcp` console script is defined in `pyproject.toml`:
```toml
[project.scripts]
tc-mcp = "tc_mcp.server:main"
```

---

## 8. Example Tool Interactions

### Search: "Find all high-priority security tests for Reports on Chrome"

```
AI Assistant calls: search_test_cases(
    component="Reports",
    test_type="Security",
    priority="High",
    browser="Chrome 148"
)
→ Returns 8 matching test cases
```

### Create: "Add a new functional test for SmartCode on Safari desktop"

```
AI Assistant calls: create_test_case(
    summary="[SmartCode] Functional: verify code snippet injection",
    priority="High",
    component="SmartCode",
    test_type="Functional",
    browser="Safari 19",
    device="desktop",
    steps="1. Log in to VWO | 2. Open SmartCode | 3. Add a new snippet | 4. Save and verify",
    expected_result="The snippet is saved and appears in the snippet list"
)
→ Returns: Created VWO-5001
```

### Coverage: "What's the test coverage for Funnels module?"

```
AI Assistant calls: get_coverage_report(component="Funnels")
→ Returns:
  Total: 278 test cases
  By Type: Functional(85), Negative(45), UI/UX(42), API(30), ...
  By Priority: High(120), Medium(98), Low(40), Highest(20)
  By Status: Ready(150), Automated(80), Draft(30), Deprecated(18)
```

---

## 9. Implementation Phases

| Phase | What | Estimated Effort |
|-------|------|-----------------|
| **Phase 1: Foundation** | Project scaffold, Pydantic models, CSV repository, config | 1 session |
| **Phase 2: Search** | All 6 search/discovery tools + ranking | 1 session |
| **Phase 3: Authoring** | Create, update, delete tools + auto-ID generation | 1 session |
| **Phase 4: Export** | CSV/JSON/Markdown export tools | 1 session |
| **Phase 5: Planning** | Coverage reports, gap analysis, test plan outlines | 1 session |
| **Phase 6: Quality** | Validation, duplicate detection, stale case finder | 1 session |
| **Phase 7: Polish** | MCP prompts, resources, README, tests, config | 1 session |

---

## 10. Success Criteria

- [ ] All 18 tools are registered and callable via MCP
- [ ] Search returns relevant results in < 100ms for 5K records
- [ ] New test cases are persisted to CSV immediately
- [ ] Export produces valid CSV, JSON, and Markdown
- [ ] Coverage reports are accurate and complete
- [ ] All tools have pytest tests with > 80% coverage
- [ ] Server starts and connects to Claude Desktop without errors
- [ ] README includes setup instructions and tool reference