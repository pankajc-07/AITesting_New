# SOP 05: Build Plan (THE ONE PROBABILISTIC STEP)

**Goal:** Use the LLM to map ticket facts onto a structured JSON plan. This is the ONLY step that calls a model (AI-2).

**Input:** Normalized ticket dict.

**Logic:**
1. Build system prompt with anti-hallucination rules (BR-1 through BR-5)
2. Build user message: ticket data + JSON schema
3. Call LLM with temperature=0.3 (BR-8), response_format=json_object
4. Validate JSON against required fields
5. Retry once on failure (BR-9)
6. Return (plan_data, usage)

**Output:** `(plan_data: dict, usage: dict)` where plan_data conforms to plan.schema.json

**Rules Enforced:**
- BR-1: Never invent AC
- BR-2: Never invent URLs, endpoints, dates
- BR-3: Never assume test data exists
- BR-6: Returns JSON, not markdown

**Implementation:** `tools/plan_build.py`