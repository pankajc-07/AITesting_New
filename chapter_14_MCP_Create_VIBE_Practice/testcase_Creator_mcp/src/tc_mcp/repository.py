"""CSV-backed repository for VWO test cases."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Callable

from tc_mcp.config import data_path
from tc_mcp.models import CSV_COLUMNS, TestCase


class Repository:
    """Loads and queries the VWO test case CSV."""

    def __init__(self, csv_path: Path | None = None):
        self._path = csv_path or data_path()
        self.rows: list[TestCase] = []
        self._by_key: dict[str, TestCase] = {}
        self.modules: list[str] = []
        self.test_types: list[str] = []
        self.browsers: list[str] = []
        self.devices: list[str] = []
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            raise FileNotFoundError(f"CSV not found: {self._path}")
        with open(self._path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tc = TestCase(
                    key=row.get("Issue Key", "").strip(),
                    summary=row.get("Summary", "").strip(),
                    description=row.get("Description", "").strip(),
                    priority=row.get("Priority", "").strip(),
                    module=row.get("Component", "").strip(),
                    labels=[l.strip() for l in row.get("Labels", "").split() if l.strip()],
                    test_type=row.get("Test Type", "").strip(),
                    preconditions=row.get("Preconditions", "").strip(),
                    steps=self._parse_steps(row.get("Steps", "")),
                    expected_result=row.get("Expected Result", "").strip(),
                    browser=row.get("Browser", "").strip(),
                    device=row.get("Device", "").strip(),
                    status=row.get("Status", "").strip(),
                )
                self.rows.append(tc)
                self._by_key[tc.key] = tc

        self.modules = sorted(set(tc.module for tc in self.rows))
        self.test_types = sorted(set(tc.test_type for tc in self.rows))
        self.browsers = sorted(set(tc.browser for tc in self.rows))
        self.devices = sorted(set(tc.device for tc in self.rows))

    @staticmethod
    def _parse_steps(raw: str) -> list[str]:
        if not raw.strip():
            return []
        parts = re.split(r"\s*\|\s*", raw)
        return [re.sub(r"^\d+\.\s*", "", p).strip() for p in parts if p.strip()]

    def live_rows(self) -> list[TestCase]:
        return [tc for tc in self.rows if tc.is_live]

    def get(self, key: str) -> TestCase | None:
        return self._by_key.get(key)

    def search(self, filter_obj) -> list[TestCase]:
        results = self.live_rows() if not filter_obj.include_deprecated else list(self.rows)

        if filter_obj.module:
            mod_lower = filter_obj.module.lower()
            results = [tc for tc in results if tc.module.lower() == mod_lower]

        if filter_obj.priority:
            results = [tc for tc in results if tc.priority in filter_obj.priority]

        if filter_obj.test_type:
            results = [tc for tc in results if tc.test_type in filter_obj.test_type]

        if filter_obj.browser:
            browser_lower = filter_obj.browser.lower()
            results = [tc for tc in results if browser_lower in tc.browser.lower()]

        if filter_obj.device:
            device_lower = filter_obj.device.lower()
            results = [tc for tc in results if device_lower in tc.device.lower()]

        if filter_obj.status:
            results = [tc for tc in results if tc.status in filter_obj.status]

        if filter_obj.keyword:
            kw = filter_obj.keyword.lower()
            results = [tc for tc in results if kw in tc.summary.lower() or kw in tc.description.lower()]

        return results

    def get_counts(self, group_by: str) -> dict[str, int]:
        attr_map = {"component": "module", "test_type": "test_type", "priority": "priority",
                     "status": "status", "browser": "browser", "device": "device"}
        attr = attr_map.get(group_by, group_by)
        counts: dict[str, int] = {}
        for tc in self.live_rows():
            val = getattr(tc, attr, "unknown")
            counts[val] = counts.get(val, 0) + 1
        return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    def next_key(self) -> str:
        max_num = 0
        for tc in self.rows:
            digits = "".join(ch for ch in tc.key.rsplit("-", 1)[-1] if ch.isdigit())
            if digits:
                max_num = max(max_num, int(digits))
        return f"VWO-{max_num + 1}"

    def add(self, tc: TestCase) -> None:
        self.rows.append(tc)
        self._by_key[tc.key] = tc
        self._save()

    def update(self, key: str, changes: dict) -> TestCase | None:
        tc = self._by_key.get(key)
        if not tc:
            return None
        for field, value in changes.items():
            if value is not None:
                setattr(tc, field, value)
        self._save()
        return tc

    def _save(self) -> None:
        with open(self._path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(CSV_COLUMNS))
            writer.writeheader()
            for tc in self.rows:
                writer.writerow(tc.to_csv_row())