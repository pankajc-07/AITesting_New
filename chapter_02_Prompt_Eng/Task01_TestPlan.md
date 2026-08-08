ROLE: You are a Senior QA Architect with 15+ years of experience in enterprise SaaS testing. You specialize in A/B testing platforms, conversion optimization tools, and have deep expertise with VWO (Visual Website Optimizer). You have designed test strategies for Fortune 500 companies and understand GDPR, SOC2, and ISO 27001 compliance requirements.

INSTRUCTIONS:
- Generate a comprehensive, industry-level Test Plan for the VWO login page at [https://app.vwo.com/#/login](https://app.vwo.com/#/login).
- The Test Plan must follow IEEE 829 standards and cover all phases of the testing lifecycle.
- Include a detailed Test Strategy covering scope, objectives, test levels, and entry/exit criteria.
- Define the testing approach for functional, non-functional, security, usability, compatibility, and accessibility testing.
- Specify the test environment requirements, tools, and infrastructure needed.
- Include a risk assessment matrix with mitigation strategies for identified risks.
- Define the test deliverables, schedule, and resource allocation.
- Cover SSO authentication flows (Google, Microsoft), password-based login, and session management.
- Address GDPR compliance for user data handling during testing.
- Include a traceability matrix mapping requirements to test scenarios.
- [Critical] Define clear entry and exit criteria for each test phase.
- [Critical] Include a defect management workflow and severity classification.
- [Mandatory] Specify browser/OS compatibility matrix for cross-browser testing.
- [Mandatory] Include performance benchmarks (page load time, API response time, concurrent user load).
- [Don't] Do not include actual test cases — this is a Test Plan, not test execution scripts.
- [Don't] Do not make assumptions about VWO's internal architecture beyond what is publicly visible.

CONTEXT:
VWO (Visual Website Optimizer) is a leading A/B testing and conversion optimization platform used by enterprises worldwide. The login page at `app.vwo.com/#/login` is the gateway to the VWO application. It supports:
- Email/password authentication
- SSO via Google OAuth
- SSO via Microsoft Azure AD
- "Forgot Password" recovery flow
- "Create Account" / "Sign Up" redirection
- Session timeout and persistent login (Remember Me)
- CAPTCHA after multiple failed attempts
- Rate limiting on login attempts

The login page is a Single Page Application (SPA) built with a modern JavaScript framework. It communicates with VWO's backend authentication APIs. The page must work across Chrome, Firefox, Safari, and Edge on desktop, and mobile browsers on iOS and Android.

EXPECTED:
- A complete Test Plan document with all sections defined by IEEE 829.
- Clear, actionable testing strategy that a QA team can execute immediately.
- Risk-based prioritization of test efforts.
- Measurable success criteria for each test phase.
- No ambiguity — every section must have concrete deliverables.

PARAMETERS:
- Target URL: https://app.vwo.com/#/login
- Application Type: Single Page Application (SPA)
- Authentication Methods: Email/Password, Google SSO, Microsoft SSO
- Compliance: GDPR, SOC2
- Browsers: Chrome (latest 2), Firefox (latest 2), Safari (latest 2), Edge (latest 2)
- Mobile: iOS Safari (latest 2), Android Chrome (latest 2)
- Performance SLA: Login page load < 3 seconds, API response < 2 seconds
- Test Data: Use synthetic test accounts only — no production user data
- Test Environment: Staging/UAT environment preferred; production smoke tests only

OUTPUT:
Provide the Test Plan in the following structured format:

1. **Test Plan Identifier** — Unique ID, version, date
2. **Introduction** — Purpose, scope, objectives
3. **Test Items** — Features/modules in scope and out of scope
4. **Features to be Tested** — Detailed feature list with priority
5. **Features Not to be Tested** — Explicit exclusions with rationale
6. **Test Strategy / Approach** — Test levels (unit, integration, system, UAT), test types (functional, non-functional, security, usability, compatibility, accessibility), test design techniques
7. **Test Environment** — Hardware, software, network, tools, test data
8. **Entry and Exit Criteria** — Per test phase
9. **Test Deliverables** — Documents, reports, artifacts
10. **Risk Assessment Matrix** — Risk ID, description, probability, impact, mitigation
11. **Test Schedule** — Phases, milestones, estimated effort
12. **Resource Planning** — Roles, responsibilities, skill requirements
13. **Defect Management** — Severity classification, workflow, SLAs
14. **Traceability Matrix** — Requirements → Test scenarios mapping
15. **Approvals** — Stakeholder sign-off checklist

TONE: Technical, precise, enterprise-grade, audit-ready. Write as if this Test Plan will be reviewed by a CTO and an external auditor.