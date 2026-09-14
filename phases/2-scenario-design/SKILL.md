---
name: kryptonite-phase-2-scenario-design
description: Select applicable attack modules and design concrete, reviewable attack scenarios from the surface map, then gate on user approval before any attack runs.
---

# Phase 2 — Scenario Design (GATE)

This phase turns the Phase 1 surface map into a concrete, written attack
plan — and stops. No attack technique runs until the user has seen and
approved this plan. This mirrors `writing-plans` + spec self-review: design
before you break.

## Inputs

- **Surface map** (`surface-map.md`) from Phase 1: stack, runnable/
  static-only status, and the routes/inputs/data-stores/external-deps/
  auth-model/trust-boundaries/config-secrets inventory, each marked
  in-scope or out-of-scope.
- **Baseline manifest** (`baseline-manifest.md`) from Phase 1: what the
  feature baseline covers and how to run it — scenario design should note,
  per scenario, which baseline test(s) already cover the surface being
  attacked, so Phase 7 knows what protects it.

## Procedure

1. **Select applicable modules.** Read every playbook in `modules/*.md`.
   For each, check its `applies-to` (stack signals) field against the
   surface map's stack-detection result and surface inventory. Keep a
   module only if the app actually exposes the kind of surface that module
   targets (e.g. skip `accessibility-i18n` for a headless API with no UI;
   skip `mobile`-specific probes for a pure web backend). Record which
   modules were selected and which were skipped, with a one-line reason
   for each skip — this list itself is part of the plan and is reviewed
   for coverage gaps.

2. **Design concrete scenarios per selected module.** For every selected
   module, walk its playbook's probes and, for each one that has an
   in-scope surface to target, write a scenario with:
   - **Target surface(s)** — the specific in-scope route/endpoint/function/
     data store/auth boundary from the surface map this scenario probes.
   - **What to probe / how** — the concrete technique, adapted from the
     module playbook to this app's actual inputs (not a generic
     description — name the real parameter, header, or field).
   - **Expected-safe behavior** — what a hardened app does when this probe
     runs (reject, sanitize, rate-limit, degrade gracefully, etc.) —
     stated precisely enough that an attacker agent can tell pass from
     fail without judgment calls.
   - **Detection criteria** — the observable signal that distinguishes
     "safe" from "weak": a status code, a response shape, a timing
     threshold, a log line, a resource metric. Vague criteria ("seems
     wrong") are not acceptable — rewrite until it's a concrete check.
   - **Severity if failed** — a first-pass `severity` estimate
     (`critical`|`high`|`medium`|`low`|`info`, per
     `references/severity.md`) for what it means if this scenario finds a
     real weakness. This is a planning estimate; Phase 4 verifiers assign
     the authoritative value.
   Do not design scenarios against out-of-scope surfaces, even if a module
   playbook would normally cover them.

3. **Cluster scenarios for dispatch.** Group the finished scenarios into
   clusters Phase 3 will hand to parallel attacker subagents — normally one
   cluster per module, but split a module into multiple clusters if it has
   enough scenarios that one subagent's task would be unreasonably large,
   or merge two thin modules' scenarios into one cluster if each has very
   few. Note the clustering in the plan; Phase 3 uses it directly.

4. **Self-review the plan for coverage and consistency** before presenting
   it, mirroring `writing-plans`:
   - Does every in-scope surface from the surface map appear in at least
     one scenario, or is its omission explicitly justified (e.g. covered
     indirectly, genuinely low-value)?
   - Does every scenario have a real (not templated) target surface,
     precise detection criteria, and a severity estimate?
   - Are static-only runs (per Phase 1's runnable determination) reflected
     — scenarios for a static-only target must be code-level probes /
     static analysis, not live-request techniques?
   - Is the module-skip list justified and does it not silently drop an
     obviously-applicable dimension (e.g. skipping `security-pentest` on
     an app with authenticated endpoints would be a red flag)?
   Fix gaps found during self-review before moving to the gate.

5. **Write the attack plan doc.** Assemble everything above into a single
   `attack-plan.md`: modules selected/skipped with reasons, the full
   scenario list grouped by cluster, and the dispatch clustering for
   Phase 3.

## Outputs

- **Attack plan doc** (`attack-plan.md`): selected/skipped modules with
  reasons, every scenario (target surface, probe, expected-safe behavior,
  detection criteria, severity-if-failed), and the attacker-dispatch
  clustering.

## Gate

**Present `attack-plan.md` to the user before any attack executes.** Show
the module selection, the full scenario list, and the clustering. The user
may approve as-is, request scenarios be added/removed/narrowed, or reject
the plan and send it back for revision. Do not proceed to Phase 3 without
an explicit go-ahead on this plan — this is the same propose-then-approve
discipline as the Phase 6 fix gate, applied to what gets attacked in the
first place.

## Next phase

Once the plan is approved, proceed to `phases/3-attack-loop/SKILL.md`,
handing it the approved `attack-plan.md` (scenario list + clustering) and
the environment details captured in Phase 1.
