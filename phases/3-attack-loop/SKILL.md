---
name: kryptonite-phase-3-attack-loop
description: Dispatch parallel attacker subagents, one per module or scenario cluster, to produce schema-valid candidate Findings from the approved attack plan.
---

# Phase 3 — Attack Loop

This phase executes the plan Phase 2 got approved — nothing more, nothing
less. Each attacker subagent runs exactly one cluster's scenarios and
reports candidate Findings; it never fixes anything and never expands scope
beyond what Phase 2 approved.

## Inputs

- **Approved attack plan** (`attack-plan.md`) from Phase 2: the full
  scenario list (target surface, probe, expected-safe behavior, detection
  criteria, severity-if-failed) and the dispatch clustering.
- **Surface map** (`surface-map.md`) from Phase 1: in-scope/out-of-scope
  boundaries and the runnable/static-only determination.
- **Environment details** from Phase 1: how to reach the running app (base
  URL, test credentials, start command), or, for static-only runs, the
  target repo root and language/framework context.

## Procedure

1. **Confirm the environment.** If the app is runnable, start it (reuse the
   `run` skill / the command captured in Phase 1) and verify it's reachable
   before dispatching a single attacker — a subagent racing a not-yet-ready
   server produces noise, not findings. If static-only, confirm the target
   repo root and relevant source paths are accessible to subagents instead.

2. **Dispatch attacker subagents in parallel, one per cluster.** For each
   cluster in the approved plan, dispatch a subagent using the **ATTACKER**
   prompt block in `references/agent-prompts.md`, filling in:
   - `[SURFACE_MAP]` — the in-scope/out-of-scope surface inventory,
     restricted to what this cluster's scenarios target.
   - `[MODULE_PLAYBOOK]` — the single module (or merged pair, per the
     clustering) this subagent owns, plus its Phase 2 scenarios (probe,
     expected-safe behavior, detection criteria, severity-if-failed) — the
     subagent follows the concrete scenarios, not the raw module playbook
     from scratch.
   - `[ENV_DETAILS]` — the base URL/credentials/start command for a live
     run, or the static-analysis context for a static-only run.
   Dispatch all clusters' subagents in a single batch so they run
   concurrently — this is the standing "deploy agents for parallel work"
   permission; there is no need to run clusters one at a time unless a
   cluster's probes would interfere with another's (e.g. both mutate the
   same shared state) — in that case, sequence only the conflicting pair
   and parallelize the rest.

3. **Enforce the attacker rules while agents run** (restated from
   `references/agent-prompts.md`, this orchestrator is responsible for
   having set them up correctly in the dispatch):
   - Local/test environment only — never a production host.
   - Out-of-scope surfaces are off limits, even indirectly.
   - No destructive actions — read-only or reversible probes; disposable
     test data, cleaned up afterward.
   - No real secrets or real PII — synthetic data and the given test
     credentials only.
   - A probe that succeeds unexpectedly gets captured as evidence and the
     agent moves on — it does not chain into a larger live exploit.

4. **Collect each subagent's output.** Every attacker emits a JSON array of
   candidate Findings (or `[]` with a note on techniques run clean). Gather
   all arrays into one combined candidate list for this run.

5. **Validate every candidate Finding.** Write the combined candidate list
   to a JSON file and run:
   ```
   python scripts/validate_findings.py <candidates-file>
   ```
   The script checks all nine required fields (`id`, `dimension`, `title`,
   `surface`, `repro`, `evidence`, `severity`, `exploitability`, `status`)
   are present and that `severity`/`exploitability`/`status` are valid enum
   values, and exits non-zero with per-index error lines if not.
   - If it reports errors, send the offending Finding(s) back to the
     originating attacker subagent to correct (missing field, bad enum
     value, `repro` not a list) — do not hand-edit an attacker's Finding
     yourself, since you weren't the one who ran the probe.
   - Re-run the validator after corrections until it exits 0 (or the
     remaining errors are acknowledged as unfixable and those specific
     Findings are dropped with a note in the run log).

6. **Sanity-check scope adherence.** Spot-check that every candidate's
   `surface` field names an in-scope surface from the surface map, and that
   `dimension` matches the module that produced it. Any candidate naming an
   out-of-scope surface is dropped and logged — the attacker rules should
   have prevented this, but this phase is the backstop.

## Outputs

- **Validated candidate Findings**: a JSON array of Finding objects, every
  one schema-valid per `references/finding-schema.md` and confirmed
  `status: "candidate"`, ready for Phase 4. Includes attacker subagents'
  clean-run notes for clusters that produced `[]`, so Phase 8 can later
  state what was attacked and found nothing.

## Gate / loop rule

No user-facing gate in this phase — the gate already happened in Phase 2.
The internal loop is step 5: candidates are not allowed to leave this phase
until `scripts/validate_findings.py` passes clean (or remaining failures are
explicitly dropped with a logged reason). Do not pass schema-invalid
Findings forward to Phase 4.

## Next phase

Proceed to `phases/4-verify-findings/SKILL.md`, handing it the validated
candidate Findings array and the same environment details used here.
