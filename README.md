# kryptonite

Superpowers builds systems; `kryptonite` breaks them across every dimension, then hardens them — without regressing features. This is a collection of interlocking skills that attack a working app to failure, verify findings adversarially, design minimal fixes with regression tests, and deliver a production-readiness verdict.

## The 8-Phase Attack-and-Harden Loop

1. **Recon & Baseline** — Detect stack and map surfaces; capture feature baseline as regression guardrail
2. **Scenario Design (GATE)** — Design concrete attack scenarios per applicable module; review before execution
3. **Attack Loop** — Dispatch parallel attacker agents; live attacks and static probes per dimension
4. **Verify Findings** — Adversarially reproduce each finding; dedupe and rank by severity × exploitability
5. **Design Fixes** — Per confirmed finding, propose minimal fix plus two regression tests
6. **Approval Gate** — Present diffs, tests, and risk; user approves before any code change
7. **Apply & Re-verify** — Apply approved fixes; re-run feature baseline and attack surface; loop if needed
8. **Readiness Report** — Deliver hardened state, GO/NO-GO checklist, and residual risk assessment

## Scope & Guardrails

- **Fix autonomy:** Fixes are proposed and shown as diffs before applied — never auto-applied to the working tree.
- **Deploy scope:** Operates in local/test environment only; never touches live infrastructure or production.
- **Target breadth:** Detects and adapts to any app stack (web, API, mobile, CLI, library); falls back to static analysis when runtime is unavailable.
- **Runtime strategy:** Runs the app if possible for live attacks; uses static analysis + code-level probes as fallback.

## Install

Run `scripts/install.sh` (added in a later task) to symlink kryptonite into your Claude Code skills directory and enable the orchestrator skill.

## Attack Modules

The attack catalog is extensible. Core dimensions include security penetration testing, API abuse and limits, load and chaos resilience, and data/logic integrity. Real-world-readiness modules (config, observability, failure UX, supply chain, privacy, cost, accessibility) extend coverage — add a new `.md` module to add a dimension.

## Key Contracts

- **Finding schema** (`references/finding-schema.md`) — canonical JSON object for all findings across phases
- **Severity rubric** (`references/severity.md`) — severity × exploitability ranking
- **Fix contract** — every fix ships with two tests (vulnerability closed + feature intact); cannot merge unless feature baseline is green
- **Readiness report** (`references/readiness-report.md`) — final GO/NO-GO output and residual-risk summary
