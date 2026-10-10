# TestCreator MCP (TC MCP)

A FastMCP server for searching, creating, updating, exporting, and planning VWO test cases — 5,000 real test cases across 17 modules.

## Quick Start

```bash
cd testcase_Creator_mcp
uv sync
uv run tc-mcp
```

## MCP Connection String

### For Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "testcase-creator": {
      "command": "uv",
      "args": [
        "--directory",
        "D:/AITesterBlueprint4x/LearningAITesterBlueprint4x/chapter_14_MCP_Create_VIBE_Practice/testcase_Creator_mcp",
        "run",
        "tc-mcp"
      ]
    }
  }
}
```

### For VS Code Copilot (`.vscode/mcp.json`)

```json
{
  "servers": {
    "testcase-creator": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "D:/AITesterBlueprint4x/LearningAITesterBlueprint4x/chapter_14_MCP_Create_VIBE_Practice/testcase_Creator_mcp",
        "run",
        "tc-mcp"
      ]
    }
  }
}
```

### Enable Write Operations

Set the environment variable to allow creating/updating test cases:

```json
{
  "mcpServers": {
    "testcase-creator": {
      "command": "uv",
      "args": [
        "--directory",
        "D:/AITesterBlueprint4x/LearningAITesterBlueprint4x/chapter_14_MCP_Create_VIBE_Practice/testcase_Creator_mcp",
        "run",
        "tc-mcp",
        "--allow-write"
      ]
    }
  }
}
```

## Tools (18)

### Search & Discovery (6)
| Tool | Description |
|------|-------------|
| `search_test_cases` | Search by module, priority, type, browser, device, status, keyword |
| `get_test_case` | Get full details by Issue Key (e.g. VWO-1001) |
| `list_modules` | List all 17 VWO modules with test case counts |
| `list_test_types` | List all 9 test types with counts |
| `get_test_case_count` | Aggregate counts by any dimension |
| `find_related_test_cases` | Find tests in same module + type |

### Authoring (4)
| Tool | Description |
|------|-------------|
| `create_test_case` | Create new test case with auto-generated VWO key |
| `update_test_case` | Update fields of an existing test case |
| `update_test_case_status` | Quick status change |
| `delete_test_case` | Soft-delete (mark as Deprecated) |

### Export (2)
| Tool | Description |
|------|-------------|
| `export_test_cases` | Export filtered results as JSON, CSV, or Markdown |
| `export_test_case` | Export single test case as formatted Markdown |

### Planning (3)
| Tool | Description |
|------|-------------|
| `get_coverage_report` | Per-module coverage by type, priority, status |
| `get_coverage_gaps` | Find modules missing specific test types/priorities |
| `generate_test_plan_outline` | Structured test plan outline for a module |

### Quality (3)
| Tool | Description |
|------|-------------|
| `validate_test_case` | Check completeness and quality issues |
| `find_duplicates` | Detect similar test cases by summary text |
| `get_stale_test_cases` | List Draft and Deprecated test cases |

## Data

- **Source:** `../data/vwo_5000_test_cases.csv`
- **Records:** 5,000 test cases
- **Modules:** 17 (Reports, Personalization, Feature Rollout, Surveys, Integrations, etc.)
- **Test Types:** 9 (Functional, Negative, UI/UX, API, Boundary, Regression, Security, Accessibility, Performance)
- **Browsers:** Chrome 148, Edge 148, Firefox 141, Safari 19
- **Devices:** desktop, mobile (Android), mobile (iOS), tablet