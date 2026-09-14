---
name: kryptonite-phase-8-readiness-report
description: Emit the final GO/NO-GO readiness report summarizing what was attacked, found, fixed, and left as residual risk.
---

# Phase 8 — Readiness Report

This is the last phase of the run: it produces one deliverable, the
readiness report, and does not attack, fix, or apply anything itself. It
synthesizes everything captured across Phases 1–7 into the template at
`references/readiness-report.md` and renders a GO/NO-GO verdict.

## Inputs

- **Surface map** (`surface-map.md`) and stack-detection result, from
  Phase 1.
- **Attack plan** (`attack-plan.md`) — modules run and skipped, from
  Phase 2.
- **Full Findings list** (all statuses: `confirmed`, `plausible`,
  `rejected`) with final `severity`/`exploitability`/`priority`, from
  Phase 4.
- **Proposed fix packages** (diffs + tests) for every Finding that reached
  fix design, from Phase 5.
- **Approval record** (`approved` / `rejected` / `edited`) per Finding,
  from Phase 6.
- **Per-finding disposition record** (`applied+closed`,
  `applied+reverted:baseline-regression`,
  `applied+reverted:fix-ineffective`, `rejected`,
  `not-applied:needs-manual-design`) and the harden-round count used, from
  Phase 7.

## Procedure

1. **Copy the template verbatim.** Start from the fenced template in
   `references/readiness-report.md` and fill in every section — do not
   omit one; where a section truly doesn't apply, write "N/A" with a
   one-line reason rather than deleting it.

2. **Fill in the Summary.**
   - **Verdict** — determine per the GO/NO-GO rule in step 7 below (fill
     this in last, then come back and set it here).
   - **Run scope** — stack detected in Phase 1, and whether the run was
     live (runnable) or static-only.
   - **Modules run** — the selected modules from Phase 2's `attack-plan.md`
     (not the skipped ones — those appear under Attacked surfaces /
     Out-of-scope).
   - **Findings** — total discovered (all candidates from Phase 3) →
     confirmed (Phase 4) → fixed (Phase 7 `applied+closed` count) →
     residual (everything else still open).
   - **Headline risk** — the single highest-priority open item after
     Phase 7 (the top of the Residual risks table below), or "none
     outstanding" if nothing remains open.

3. **Fill in Attacked surfaces**, from the Phase 1 surface map and Phase 2
   plan: every in-scope surface that was actually exercised, which
   dimension(s) touched it, and any relevant note (auth-gated, rate-limit
   tested, static-only probe, etc.). List **out-of-scope** surfaces
   separately with the reason they were excluded (carried from Phase 1's
   in-scope/out-of-scope marking).

4. **Fill in Findings by priority.** One row per Finding that reached
   Phase 4, sorted P0 first, using the exact field names from
   `references/finding-schema.md` (`id`, `dimension`, `title`, `severity`,
   `exploitability`) plus the looked-up `priority` (from
   `references/severity.md`) and final `status`. Include `rejected`
   Findings too — they're part of the audit trail, not hidden.

5. **Fill in Fixes applied.** One row per Finding with disposition
   `applied+closed` in Phase 7: a short fix summary (from the fixer's diff
   and risk note), the files changed, the names of the two tests added,
   and who approved it (from the Phase 6 approval record — user + date if
   captured, otherwise "user" with the run's date).

6. **Fill in Residual risks.** One row per Finding that is **not**
   `applied+closed`: `rejected` (Phase 6), `not-applied:needs-manual-design`
   (Phase 5/6), `applied+reverted:baseline-regression`, or
   `applied+reverted:fix-ineffective` (Phase 7), plus anything left open
   because the Phase 7 harden-round cap was hit. For each: its `priority`,
   why it wasn't fixed (state the actual reason — rejected by user,
   reverted for a named regression, fix ineffective, round cap reached,
   etc.), and what would need to change to revisit it (e.g. "user
   risk-accepts and re-approves," "needs a design change out of scope for
   this run," "re-run Phase 7 for one more round").

7. **Determine the GO/NO-GO verdict and complete the checklist.**
   - Walk each checklist item (env & secrets, rate limits, observability,
     error handling, dependency health, data safety) and check it only if
     nothing in the Findings/Residual risks tables contradicts it at P0/P1.
     An unchecked box must have an inline reason pointing at the specific
     Finding `id` backing it, or an explicit statement of what wasn't
     assessed this run (e.g. no dependency-health module was in scope).
   - **Verdict rule:**
     - **NO-GO** if any `P0` Finding remains open (any disposition other
       than `applied+closed`) and the user has not explicitly
       risk-accepted it.
     - **GO WITH CONDITIONS** if only `P1` Findings remain open (again,
       unless explicitly risk-accepted, in which case treat as GO with the
       acceptance recorded), or if a checklist box is unchecked for a
       reason short of an open P0/P1.
     - **GO** if every P0/P1 Finding reached `applied+closed`, and the
       checklist is fully checked with no unresolved P0/P1 backing any
       gap.
   - Record any explicit user risk-acceptance inline in the Residual risks
     table row it applies to, not just in the verdict line — the report
     should be self-contained evidence of why the verdict is what it is.

8. **Complete Sign-off.** Prepared-by is this run/session; Reviewed-by is
   the user; Date is the run's completion date.

9. **Deliver the report to the user** as the final artifact of this
   kryptonite run — this is the terminal output of the whole loop, not an
   internal working note like the surface map or attack plan.

## Outputs

- **Readiness Report** (per `references/readiness-report.md`): Summary,
  Attacked surfaces, Findings by priority, Fixes applied, Residual risks,
  GO/NO-GO checklist, and Sign-off — fully populated, no template
  placeholders left unfilled.

## Gate / loop rule

No gate and no loop here — this phase is a synthesis and delivery step.
There is nothing further for kryptonite to decide or attack in this run;
any follow-up (chasing a residual risk, re-running after the user makes
changes, extending scope) is a **new** kryptonite run starting again at
Phase 1, not a continuation of this one.

## Next phase

None — this is the final phase. The kryptonite run is complete once the
Readiness Report has been delivered. A future run (to chase residual risk,
verify after unrelated changes, or extend scope) starts over at
`phases/1-recon-and-baseline/SKILL.md`.
