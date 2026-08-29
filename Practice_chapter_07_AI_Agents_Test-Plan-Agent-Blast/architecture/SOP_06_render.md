# SOP 06: Render

**Goal:** Convert JSON plan data → professional markdown test plan file. Deterministic Python only — the LLM never touches the template (BR-6).

**Input:** Plan data dict + ticket dict + optional model name.

**Logic:**
1. Render 14-section markdown from the plan JSON
2. Each section references its justified_by source
3. Missing sections get placeholder: `_(Not specified in ticket — requires clarification)_`
4. Write to `out/{KEY}-test-plan.md`
5. Generate trace.json in `out/`

**Output:** Markdown string + file on disk.

**14 Sections Rendered:**
1. Objective, 2. Scope (In/Out), 3. Test Environment, 4. Test Strategy, 5. Test Data, 6. Defect Reporting, 7. Entry Criteria, 8. Exit Criteria, 9. Test Deliverables, 10. Test Schedule, 11. Risks & Mitigations, 12. Tools, 13. Assumptions, 14. Trace Matrix

**Implementation:** `tools/render.py`