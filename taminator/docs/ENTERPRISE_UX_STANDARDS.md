# Enterprise UX Standards — Taminator and Internal TAM Tools

This document defines the developer standard for user experience in Taminator and similar internal tools. The goal is **enterprise-grade** quality: reliable, clear, secure, and consistent for TAMs and stakeholders.

---

## 1. User experience (UX) principles

### 1.1 Clarity first
- **Labels and copy:** Use plain language. Avoid jargon unless it is standard for the audience (e.g. "RFE," "JIRA"). Prefer "Generate Reports" over "Reports," "Customer Search" over "Customer," "Settings" over "Config" when it improves clarity.
- **One primary action per screen:** The main task (e.g. generate or check a report) is obvious. Secondary actions (Settings, Library, User Guide) are available but do not compete with the primary flow.
- **Progressive disclosure:** Show only what is needed for the current step. Advanced or optional options (tokens, VPN check) live in Settings or secondary panels.

### 1.2 Feedback and state
- **Always show state:** Status indicators (VPN, tokens) must reflect real state: green when connected/configured, red when not. Use a neutral (e.g. gray) only for "checking" or "unknown."
- **Immediate feedback:** Buttons show loading state (disabled + "Running…" or spinner) while work is in progress. Results (success, error, or output) appear in a dedicated area without replacing critical controls.
- **Errors are actionable:** Error messages say what went wrong and what the user can do (e.g. "Connect to Red Hat VPN," "Configure JIRA token in Settings").

### 1.3 Consistency
- **Navigation:** Primary nav (Generate Reports, Library, Settings) is in one place and behaves the same across the app. External links (User Guide, Repository) open in a new tab and are clearly distinct.
- **Actions:** Primary actions (e.g. "Check report," "Update report") use the same button style; secondary actions use a secondary style. Destructive actions are clearly marked.
- **Terminology:** Use the same terms in UI, docs, and CLI (e.g. "customer," "report," "token type").

---

## 2. Accessibility (a11y)

- **Semantic HTML:** Use correct elements (`label` for inputs, `button` for actions, `nav` for navigation). Avoid divs/spans for interactive controls.
- **Focus and keyboard:** All actions are reachable and usable via keyboard. Focus order is logical. No keyboard traps.
- **Screen readers:** Status changes (e.g. indicators, results) are announced where appropriate (`aria-live`, `aria-label`). Decorative-only elements can be hidden from assistive tech.
- **Color and contrast:** Status (green/red) is not the only differentiator; pair with text or icons so color-blind users can distinguish state. Contrast meets WCAG 2.1 Level AA where feasible.
- **Forms:** Every input has an associated label. Validation errors are associated with the field and announced.

---

## 3. Error handling and reliability

- **No silent failures:** If an API call or backend step fails, the UI shows an error message. Do not leave the user with a blank state or stale "success" when something failed.
- **Graceful degradation:** If an optional feature is unavailable (e.g. Hydra search when token is missing), show a clear message and still allow core flows (e.g. manual customer entry, test data).
- **Timeouts and loading:** Long-running operations have a timeout and a loading state. On timeout, show a clear message and suggest retry or checking VPN/connectivity.
- **Validation:** Validate input before submit (e.g. "Enter a customer name or check Use test data"). Show validation errors next to the field or at the top of the form, not only in the console.

---

## 4. Security and privacy

- **Tokens and secrets:** Tokens are never logged or exposed in the UI beyond "configured" vs "not configured." Token input fields use `type="password"` and are not pre-filled from storage in the DOM.
- **Storage:** Tokens stored on disk (e.g. `~/.config/taminator/ui_tokens.json`) use restrictive permissions (e.g. 0o600). Prefer keyring when available; document how tokens are used and stored.
- **Network:** The app assumes use on Red Hat VPN for real customer data. Do not send tokens or customer data to third-party endpoints; use only Red Hat / internal APIs as intended.
- **HTTPS:** When the UI is served over the network (not only localhost), use HTTPS. For local-only serve, document that it is for development or trusted environments.

---

## 5. Performance and responsiveness

- **Responsive layout:** The UI is usable on common desktop sizes and does not assume a single resolution. Avoid horizontal scroll for core content; wrap or stack elements as needed.
- **Debounce and throttle:** Search and other frequent inputs (e.g. customer search) use debouncing to avoid excessive API calls. Indicator refresh does not hammer the server.
- **Caching:** When safe, cache read-only or slowly changing data (e.g. token status) for a short period to reduce load and improve perceived speed.

---

## 6. API and integration contract

- **REST and JSON:** Web APIs use JSON request/response. Use standard HTTP status codes (200, 400, 404, 500). Error responses include a consistent shape (e.g. `{ "ok": false, "error": "message" }`).
- **Idempotency and clarity:** POST endpoints that change state are clearly documented. Prefer GET for read-only operations. Use the same auth (tokens, env) as the CLI for parity.
- **Versioning and compatibility:** When changing API contracts, preserve backward compatibility or version the API so existing clients do not break unexpectedly.

---

## 7. Documentation and discoverability

- **User Guide:** A single, up-to-date User Guide (or README) is linked from the UI. It covers: how to run the app, how to configure VPN and tokens, how to generate a report, and where to get help.
- **Repository link:** The UI links to the project repository (landing page) so users can open issues, read docs, and see the source.
- **In-app hints:** Where helpful, short hints (e.g. "Use test data (no JIRA)" or "Saved to ~/.config/taminator/...") reduce the need to leave the app for basic tasks.

---

## 8. Checklist for new features and changes

Before shipping UI or API changes, verify:

- [ ] Labels and copy are clear and consistent with this standard.
- [ ] Status and errors are visible and actionable; no silent failures.
- [ ] New controls are keyboard-accessible and have appropriate labels/aria.
- [ ] Tokens and secrets are never logged or exposed.
- [ ] Long or frequent operations are debounced/throttled and show loading state.
- [ ] User Guide or README is updated if the user flow or configuration changes.
- [ ] CLI and browser stay in parity where the feature applies to both.

---

## 9. Scope and ownership

- **Applies to:** Taminator browser UI, `tam-rfe` CLI UX (messages, prompts, errors), and any new internal TAM tools that share the same product direction.
- **Updates:** This standard is updated when the team agrees on a change (e.g. new a11y requirement, new security practice). Propose changes via merge request or issue with the label or title indicating "UX standard."
- **Reference:** Product strategy (e.g. `PRODUCT_STRATEGY.md`) and onboarding docs should point to this document for "how we build enterprise-grade UX."
