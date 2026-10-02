# kryptonite

[![test](https://github.com/levitasOrg/kryptonite/actions/workflows/test.yml/badge.svg)](https://github.com/levitasOrg/kryptonite/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A [Claude Code](https://claude.com/claude-code) skill that **breaks a working app on purpose, then hardens it — without regressing a single feature.**

Most skills help you *build*. kryptonite is the other half: point it at an app that already works and say *"harden this"*, *"red-team this"*, *"stress-test this"* or *"make this production-ready"*. It attacks the app across 11 dimensions, proves every finding, proposes minimal fixes with tests, waits for your approval, and ends with a GO / NO-GO verdict.

## Why it's safe to point at your code

- **Propose, then approve.** Phases 1–5 only observe, attack and design. Nothing in your working tree changes until you approve each fix in Phase 6.
- **Feature baseline.** Phase 1 records what the app does right today as a regression suite. Every fix must keep it green, or the round is blocked.
- **Local and test environments only.** It never touches live infrastructure or production data. With only production available, it falls back to static analysis.
- **Bounded.** At most 3 fix-and-re-attack rounds. Anything still open is reported as residual risk, not chased forever.

## The 8-phase loop

| # | Phase | What happens |
|---|-------|--------------|
| 1 | Recon & baseline | Detect the stack, map every surface, capture the feature baseline |
| 2 | Scenario design | Pick the modules that apply, write concrete attacks — **you approve the plan** |
| 3 | Attack | Parallel attacker subagents, one per module or scenario cluster |
| 4 | Verify | Each finding is reproduced adversarially, deduped, ranked P0–P3 |
| 5 | Design fixes | Minimal diff + two tests per finding (hole closed, feature intact) |
| 6 | Approval gate | **You approve, reject or edit each fix** |
| 7 | Apply & re-verify | Apply, re-run the baseline, re-attack the touched surface |
| 8 | Readiness report | GO / NO-GO, fixes applied, residual risk |

## Attack modules

| Module | Finds |
|--------|-------|
| `security-pentest` | Auth bypass, IDOR, injection, SSRF, leaked secrets |
| `api-abuse-and-limits` | Rate-limit bypass, payload bombs, token reuse, idempotency races |
| `load-chaos-resilience` | Latency under load, resource exhaustion, retry storms, crash recovery |
| `data-logic-integrity` | Fuzz inputs, double-spend races, corrupt data, unsafe migrations, broken invariants |
| `config-and-secrets` | Hard-coded config, env drift, default credentials, over-broad IAM |
| `observability-operability` | Silent failures, missing health checks, PII in logs |
| `failure-ux-degradation` | Leaked stack traces, partial failures, broken empty / loading / error states |
| `supply-chain-deps` | Vulnerable or unpinned dependencies, lockfile integrity, licences, SBOM, provenance |
| `privacy-compliance` | PII handling, retention and erasure, consent, audit trails, GDPR / CCPA gaps |
| `cost-efficiency` | N+1 queries, unbounded results, missing caching, memory leaks, cost bombs |
| `accessibility-i18n` | WCAG 2.2 basics, Unicode / RTL, time zones and DST, locale formatting |

Add a dimension by copying [`modules/_TEMPLATE.md`](modules/_TEMPLATE.md) — no other file needs to change. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Install

```bash
git clone https://github.com/levitasOrg/kryptonite.git
cd kryptonite
./scripts/install.sh
```

This symlinks the repo into `~/.claude/skills/kryptonite`. Run `git pull` to update.

Then, in Claude Code, inside the app you want to test:

```
harden this app
```

### Optional per-app config

Copy [`.kryptonite.example.md`](.kryptonite.example.md) into the target app as `.kryptonite.md` to pin the run command, base URL, stack, and anything out of scope. Every field is optional; anything you leave out is auto-detected.

### Requirements

- Claude Code with subagent support
- Python 3.9+ for the helper scripts (standard library only)

Modules name other skills (for example `security-audit` or `accessibility-audit`) as places to get deeper technique detail. Those are optional — kryptonite runs without them.

## Layout

```
SKILL.md            orchestrator — entry point and core rules
phases/             one skill per phase (1–8)
modules/            attack catalog, one .md per dimension
references/         finding schema, severity rubric, agent prompts, report template
scripts/            detect_stack.py, validate_findings.py, install.sh, tests
```

## Responsible use

Only run kryptonite against software you own or are explicitly authorised to test. See [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
