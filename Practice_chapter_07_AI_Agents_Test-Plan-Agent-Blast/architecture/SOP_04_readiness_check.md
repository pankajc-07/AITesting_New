# SOP 04: Readiness Check

**Goal:** Determine if a ticket has enough information to create a meaningful test plan. Refuse tickets that score below 5/11 (BR-4).

**Input:** Normalized ticket dict from SOP 03.

**Logic:** Score 11 factors (1 point each):
1. Has summary
2. Has description
3. Has acceptance criteria
4. Has issue type
5. Has status
6. Has components or labels
7. Has fix versions
8. Has environment info
9. Has parent/epic
10. Has linked issues
11. Has comments

**Output:** `{"score": N, "max": 11, "threshold": 5, "plannable": bool, "blockers": [...], "gaps": [...]}`

**Edge Cases:** `--force` flag overrides the threshold to generate a draft plan anyway.

**Implementation:** `tools/readiness.py`