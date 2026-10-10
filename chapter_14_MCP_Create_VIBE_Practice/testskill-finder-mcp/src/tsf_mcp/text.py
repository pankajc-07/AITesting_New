"""Text utilities: tokenization, synonym expansion."""

from __future__ import annotations

import re

WORD_RE = re.compile(r"[a-z0-9][a-z0-9+#.-]*", re.IGNORECASE)

SYNONYMS: dict[str, set[str]] = {
    "api": {"rest", "graphql", "endpoint", "http", "request", "response"},
    "ui": {"ux", "frontend", "gui", "interface", "visual"},
    "test": {"testing", "qa", "quality", "verify", "validate", "check"},
    "automation": {"automated", "auto", "script", "ci", "cd", "pipeline"},
    "bug": {"defect", "issue", "error", "failure", "fault", "problem"},
    "performance": {"load", "stress", "speed", "latency", "throughput", "benchmark"},
    "security": {"auth", "vulnerability", "penetration", "owasp", "injection", "xss"},
    "playwright": {"pw", "browser", "chromium", "firefox", "webkit"},
    "selenium": {"se", "webdriver", "grid", "driver"},
    "cypress": {"cy", "component", "e2e"},
    "mobile": {"android", "ios", "appium", "device", "tablet"},
    "accessibility": {"a11y", "aria", "wcag", "screen-reader", "keyboard"},
    "plan": {"planning", "strategy", "roadmap", "schedule"},
    "design": {"scenario", "technique", "approach", "method"},
    "report": {"reporting", "dashboard", "metrics", "analytics", "status"},
    "requirement": {"spec", "specification", "acceptance", "criteria", "story"},
    "jira": {"ticket", "issue", "atlassian", "backlog"},
    "llm": {"ai", "gpt", "model", "prompt", "evaluation", "eval", "rag"},
    "mcp": {"protocol", "server", "tool", "context"},
    "agent": {"bot", "autonomous", "workflow", "multi-agent"},
    "data": {"dataset", "generator", "fixture", "mock", "stub"},
    "regression": {"suite", "selector", "smoke", "sanity"},
    "ci": {"jenkins", "github-actions", "pipeline", "build"},
    "bdd": {"cucumber", "gherkin", "feature", "scenario"},
    "contract": {"schema", "openapi", "swagger", "pact"},
    "trace": {"tracing", "debug", "log", "monitor"},
    "flaky": {"flake", "unstable", "intermittent", "retry"},
    "locator": {"selector", "xpath", "css", "find"},
    "page": {"pom", "object", "model", "factory"},
    "visual": {"screenshot", "snapshot", "pixel", "compare"},
    "mock": {"stub", "fake", "intercept", "network"},
    "cross": {"browser", "matrix", "parallel"},
    "framework": {"scaffold", "architect", "structure", "setup"},
    "triage": {"prioritize", "classify", "sort", "categorize"},
    "rca": {"root-cause", "analysis", "investigate", "diagnose"},
    "retro": {"retrospective", "lessons", "learned", "improve"},
    "release": {"deploy", "ship", "production", "go-live"},
    "coverage": {"gap", "missing", "untested", "traceability"},
    "closure": {"sign-off", "complete", "finish", "wrap"},
    "hallucination": {"factuality", "accuracy", "grounding"},
    "prompt": {"injection", "jailbreak", "guardrail", "safety"},
    "load": {"k6", "jmeter", "locust", "concurrent", "users"},
    "owasp": {"top10", "zap", "burp", "dast", "sast"},
    "postman": {"collection", "newman", "runner"},
    "pytest": {"fixture", "parametrize", "mark", "conftest"},
    "restassured": {"java", "given", "when", "then"},
    "appium": {"mobile", "native", "hybrid"},
    "deepeval": {"metric", "score", "benchmark"},
}


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower() for m in WORD_RE.finditer(text)]


def expand(terms: list[str]) -> dict[str, float]:
    weights: dict[str, float] = {}
    for term in terms:
        weights[term] = weights.get(term, 0) + 1.0
        for syn in SYNONYMS.get(term, set()):
            weights[syn] = weights.get(syn, 0) + 0.6
    return weights