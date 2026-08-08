ROLE: You are a Senior QA Engineer with 12+ years of experience in manual and automation testing of enterprise SaaS platforms. You have deep expertise with VWO (Visual Website Optimizer), A/B testing platforms, OAuth 2.0 / SSO authentication flows, and SPA testing. You write test cases that are precise, traceable, and ready for automation.

INSTRUCTIONS:
- Generate comprehensive, industry-level test cases for the VWO login page at [https://app.vwo.com/#/login](https://app.vwo.com/#/login).
- Cover ALL categories: Functional (happy path), Negative, Boundary, Security, Usability, Compatibility, Accessibility, Performance, and Session Management.
- Each test case must be detailed enough for a junior QA to execute without ambiguity.
- [Critical] Include test cases for ALL three authentication methods: Email/Password, Google SSO, and Microsoft SSO.
- [Critical] Cover the complete "Forgot Password" flow end-to-end.
- [Critical] Include security test cases: SQL injection, XSS, CSRF, brute-force protection, rate limiting, CAPTCHA verification, session fixation, and token validation.
- [Mandatory] Include accessibility test cases covering WCAG 2.1 AA standards (keyboard navigation, screen reader, color contrast, focus management).
- [Mandatory] Include cross-browser and cross-device compatibility test cases.
- [Mandatory] Include performance test cases: page load time, API latency, concurrent login load.
- [Mandatory] Include usability test cases: error message clarity, UI responsiveness, mobile responsiveness, tab order.
- [Generate] Generate a minimum of 50 test cases covering all categories.
- [Don't] Do not include test cases for features not visible on the login page (e.g., dashboard, campaign creation).
- [Don't] Do not invent error messages — use generic descriptions like "appropriate error message is displayed" unless the exact message is publicly documented.
- [Don't] Do not skip edge cases — empty fields, whitespace-only inputs, extremely long strings, special characters, Unicode, emoji in fields.

CONTEXT:
VWO (Visual Website Optimizer) is a leading A/B testing and conversion optimization platform. The login page at `app.vwo.com/#/login` is a Single Page Application (SPA) with the following elements:
- Email input field
- Password input field
- "Sign In" / "Log In" button
- "Forgot Password?" link → initiates password recovery flow
- "Sign in with Google" button → OAuth 2.0 SSO flow
- "Sign in with Microsoft" button → Azure AD SSO flow
- "Create Account" / "Sign Up" link → redirects to registration
- "Remember Me" / "Keep me signed in" checkbox (if present)
- Error message area for invalid credentials
- CAPTCHA challenge after multiple failed attempts (if enabled)
- Rate limiting: account lockout or cooldown after N failed attempts

The page communicates with VWO's backend authentication API. It uses HTTPS exclusively. The SPA framework handles client-side validation before API calls. Session tokens are stored in cookies/localStorage.

EXPECTED:
- A complete, structured test case suite ready for test execution.
- Each test case must be independently executable.
- Clear traceability from test case → requirement → risk.
- Coverage of all authentication flows, error states, and edge conditions.
- Test cases suitable for both manual execution and automation scripting.

PARAMETERS:
- Target URL: https://app.vwo.com/#/login
- Application Type: Single Page Application (SPA)
- Authentication Methods: Email/Password, Google OAuth 2.0 SSO, Microsoft Azure AD SSO
- Compliance: WCAG 2.1 AA, GDPR
- Browsers: Chrome (latest 2), Firefox (latest 2), Safari (latest 2), Edge (latest 2)
- Mobile: iOS Safari (latest 2), Android Chrome (latest 2)
- Screen Readers: NVDA (Windows), VoiceOver (macOS/iOS), TalkBack (Android)
- Test Data: Synthetic test accounts only
- Minimum Test Cases: 50

OUTPUT:
Provide test cases in the following structured table format:

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) |

**Categories to cover:**
1. **Functional — Happy Path** (valid email/password login, Google SSO, Microsoft SSO)
2. **Functional — Negative** (invalid password, unregistered email, empty fields, whitespace-only, SQL injection, XSS payloads)
3. **Boundary** (min/max length email, min/max length password, special characters, Unicode, emoji)
4. **Security** (brute-force lockout, CAPTCHA trigger, CSRF token, session fixation, token expiry, HTTPS enforcement, password masking, copy-paste restriction, autocomplete off)
5. **Session Management** (session timeout, Remember Me persistence, concurrent session handling, logout invalidation, browser back button after logout)
6. **Forgot Password Flow** (valid email → reset link, unregistered email, empty email, invalid email format, reset link expiry, password reset → new login)
7. **Usability** (tab order, enter key submission, error message clarity, UI responsiveness, mobile layout, loading indicators, button states)
8. **Compatibility** (Chrome, Firefox, Safari, Edge — desktop; iOS Safari, Android Chrome — mobile; different viewport sizes)
9. **Accessibility** (keyboard-only navigation, screen reader announcements, focus indicators, color contrast, ARIA labels, form labels, error association)
10. **Performance** (page load time, API response time, time to interactive, concurrent login load, resource caching)

TONE: Technical, precise, exhaustive, automation-ready. Every test case must be written as if it will be reviewed by a QA Director and handed directly to an automation engineer.