# Readiness Report Template

The final deliverable of the attack-and-harden loop (Phase 8). One report is
produced per run. Copy the fenced template below verbatim and fill in every
section — do not omit a section, write "N/A" with a one-line reason if it
truly does not apply.

Priorities (`P0`–`P3`) come from `references/severity.md`; Finding fields
(`id`, `dimension`, `title`, `severity`, `exploitability`, `status`, etc.)
come from `references/finding-schema.md`.

````markdown
# Readiness Report — <app name> — <YYYY-MM-DD>

## Summary

- **Verdict:** GO | NO-GO | GO WITH CONDITIONS
- **Run scope:** <stack detected, environment attacked (local/test only)>
- **Modules run:** <list of attack dimensions exercised, e.g. security-pentest, api-abuse-and-limits, load-chaos, data-logic-integrity, ...>
- **Findings:** <total> discovered → <n> confirmed → <n> fixed → <n> residual
- **Headline risk:** <one or two sentences on the single biggest remaining risk, or "none outstanding">

## Attacked surfaces

<Every route, endpoint, function, data store, or auth boundary that was
in-scope and exercised, plus what was explicitly out-of-scope and why.>

| Surface | Type | Dimension(s) exercised | Notes |
|---------|------|-------------------------|-------|
| <e.g. /api/users/search> | HTTP endpoint | security-pentest, api-abuse-and-limits | <e.g. auth-gated, rate limit tested> |

**Out of scope:** <surfaces explicitly excluded, e.g. third-party payment provider, prod infra, and why>

## Findings by priority

| id | dimension | title | severity | exploitability | priority | status |
|----|-----------|-------|----------|-----------------|----------|--------|
| finding-20260914-001 | security-pentest | SQL injection in user search endpoint | critical | trivial | P0 | confirmed |

<Sort by priority ascending (P0 first). One row per Finding, including
`rejected` ones kept for the audit trail — status makes disposition clear.>

## Fixes applied

<For each finding that reached a shipped fix: what changed, why it's
minimal, and the two tests that back it (vuln-closed + feature-intact).>

| Finding id | Fix summary | Files changed | Tests added | Approved by |
|------------|-------------|----------------|-------------|-------------|
| finding-20260914-001 | Parameterized the search query | api/users.py | test_search_rejects_sql_injection, test_search_still_returns_matches | <user, date> |

## Residual risks

<Every confirmed finding that was NOT fixed — P2/P3 by default, or any
priority the user explicitly chose to risk-accept. State why it was left
open and what would need to change to revisit it.>

| Finding id | Priority | Reason not fixed | Revisit trigger |
|------------|----------|-------------------|------------------|
| finding-20260914-004 | P3 | Cosmetic; no exploitable path | Re-run if surface changes |

## GO / NO-GO checklist

All boxes should be checked before a GO verdict. An unchecked box with no
P0/P1 finding backing it must have an inline reason.

- [ ] **Env & secrets** — no secrets committed or logged; required env vars documented and validated at startup; `.env`/credentials excluded from version control.
- [ ] **Rate limits** — abuse-prone endpoints (auth, search, write, expensive compute) enforce rate limiting or equivalent throttling.
- [ ] **Observability** — errors and key events are logged with enough context to diagnose in production; no silent failures.
- [ ] **Error handling** — failures degrade gracefully (no stack traces or internals leaked to users); all expected failure modes return sane responses.
- [ ] **Dependency health** — no known-critical CVEs in direct dependencies; lockfile committed; dependency versions pinned.
- [ ] **Data safety** — writes are validated and scoped to the authenticated actor; destructive operations are reversible or confirmed; backups/migrations are safe to re-run.

## Sign-off

- **Prepared by:** <agent/session>
- **Reviewed by:** <user>
- **Date:** <YYYY-MM-DD>
````
