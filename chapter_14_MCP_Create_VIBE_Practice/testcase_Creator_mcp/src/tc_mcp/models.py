"""Data models for TC MCP."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from pydantic import BaseModel, Field

Priority = Literal["Highest", "High", "Medium", "Low"]
Status = Literal["Ready", "Automated", "Draft", "Deprecated"]
TestType = Literal[
    "Functional", "Negative", "UI/UX", "API", "Boundary",
    "Regression", "Security", "Accessibility", "Performance",
]

PRIORITY_RANK = {"Low": 1, "Medium": 2, "High": 3, "Highest": 4}

CSV_COLUMNS = (
    "Issue Type", "Issue Key", "Summary", "Description", "Priority",
    "Component", "Labels", "Test Type", "Preconditions", "Steps",
    "Expected Result", "Browser", "Device", "Status",
)


@dataclass(slots=True)
class TestCase:
    __test__ = False

    key: str
    summary: str
    description: str
    priority: str
    module: str
    labels: list[str]
    test_type: str
    preconditions: str
    steps: list[str]
    expected_result: str
    browser: str
    device: str
    status: str
    issue_type: str = "Test"

    @property
    def priority_rank(self) -> int:
        return PRIORITY_RANK.get(self.priority, 0)

    @property
    def is_live(self) -> bool:
        return self.status != "Deprecated"

    def compact(self) -> dict[str, Any]:
        return {
            "key": self.key, "summary": self.summary, "module": self.module,
            "priority": self.priority, "test_type": self.test_type,
            "status": self.status, "browser": self.browser, "device": self.device,
        }

    def full(self) -> dict[str, Any]:
        return {
            **self.compact(),
            "description": self.description,
            "preconditions": self.preconditions,
            "steps": self.steps,
            "expected_result": self.expected_result,
            "labels": self.labels,
        }

    def steps_text(self) -> str:
        return " | ".join(f"{i}. {step}" for i, step in enumerate(self.steps, start=1))

    def to_csv_row(self) -> dict[str, str]:
        return {
            "Issue Type": self.issue_type,
            "Issue Key": self.key,
            "Summary": self.summary,
            "Description": self.description,
            "Priority": self.priority,
            "Component": self.module,
            "Labels": " ".join(self.labels),
            "Test Type": self.test_type,
            "Preconditions": self.preconditions,
            "Steps": self.steps_text(),
            "Expected Result": self.expected_result,
            "Browser": self.browser,
            "Device": self.device,
            "Status": self.status,
        }


class TestFilter(BaseModel):
    __test__ = False
    module: str | None = Field(None, description="Module name, e.g. 'Reports'. Case-insensitive.")
    priority: list[Priority] | None = Field(None, description="Priorities to include.")
    test_type: list[TestType] | None = Field(None, description="Test types to include.")
    browser: str | None = Field(None, description="Browser, e.g. 'Chrome 148'.")
    device: str | None = Field(None, description="Device, e.g. 'desktop', 'mobile (iOS)'.")
    status: list[Status] | None = Field(None, description="Statuses to include.")
    keyword: str | None = Field(None, description="Free-text search in summary and description.")
    include_deprecated: bool = Field(False, description="Include Deprecated tests (hidden by default).")


class TestCaseDraft(BaseModel):
    __test__ = False
    module: str = Field(..., description="Module name, e.g. 'Reports'.")
    test_type: TestType
    priority: Priority
    summary: str = Field(..., description="Format: '[Module] Test Type: action', e.g. '[Reports] Boundary: test limits of scheduled email'.")
    preconditions: str = Field(..., min_length=5, description="Setup needed before step 1.")
    steps: list[str] = Field(..., min_length=1, max_length=20, description="Ordered steps without numbering.")
    expected_result: str = Field(..., min_length=5, description="One specific, checkable outcome.")
    browser: str = Field(..., description="e.g. 'Chrome 148'.")
    device: str = Field(..., description="e.g. 'desktop'.")
    description: str | None = Field(None, description="Optional. Auto-generated when omitted.")
    status: Status = "Draft"


class TestCaseChanges(BaseModel):
    __test__ = False
    summary: str | None = None
    description: str | None = None
    priority: Priority | None = None
    status: Status | None = None
    test_type: TestType | None = None
    preconditions: str | None = None
    steps: list[str] | None = None
    expected_result: str | None = None
    browser: str | None = None
    device: str | None = None