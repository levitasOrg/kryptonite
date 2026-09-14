---
name: kryptonite-phase-7-apply-and-reverify
description: Apply approved fixes, re-run the full feature baseline as a regression block, re-attack each closed finding's surface, and loop into fresh attack on touched surfaces up to 3 harden rounds.
---

# Phase 7 — Apply & Re-verify

This is the only phase authorized to write to the target app's working
tree, and only for what Phase 6 explicitly approved. Applying a fix is the
easy part; this phase's real job is proving the fix didn't break anything
that worked before, and that it actually closed what it claims to close —
then deciding whether another round is warranted.

## Inputs

- **Approval record** and **approved fix packages** (diffs + two tests
  each) from Phase 6.
- **Feature baseline suite** and its run command, from Phase 1
  (`baseline-manifest.md`).
- **Verified Findings** from Phase 4, specifically the `repro` steps for
  each Finding being fixed this round, so its attack can be re-run.
- Current **harden-round counter** — `1` on first entry to this phase for a
  given run; incremented each time this phase loops back from step 5.

## Procedure

1. **Apply approved fixes.** For each approved fix package, apply its diff
   to the target app's working tree exactly as approved (the literal text
   from Phase 6, including any edit-round revision), and add its two tests
   into the app's test tree per its existing conventions. Apply fixes for
   this round as a batch, but keep a per-finding record of exactly which
   diff landed — re-verification is per-finding even though application is
   batched.
   - If two approved diffs conflict at apply time (rare — Phase 5 step 2
     should have caught this), stop and surface the conflict to the user
     rather than guessing a merge.

2. **Re-run the full feature baseline — every test, every time.**
   Use the exact command from `baseline-manifest.md`, not a subset. This is
   non-negotiable: a single baseline test failure **blocks this round's
   fixes**, full stop.
   - If the baseline is fully green, continue to step 3.
   - If **any** baseline test fails, treat this as a regression, not a
     finding: identify which applied fix(es) correlate with the failure
     (bisect if more than one fix landed this round and the failure isn't
     obviously attributable), revert that fix's diff and its two new tests
     from the working tree, and record it as **not applied** — its
     Finding's disposition reverts to the Phase 6 record's "approved but
     blocked by baseline regression," which Phase 8 reports as a residual
     risk with the reason stated. Fixes that didn't correlate with the
     failure stay applied. Re-run the full baseline again after any
     revert to confirm it's green before continuing.

3. **Re-run each closed finding's original attack.** For every Finding
   whose fix survived step 2, re-run its `repro` steps from
   `references/finding-schema.md`-shaped data (the same steps the verifier
   used in Phase 4) against the now-patched app.
   - If the weakness no longer reproduces, mark that Finding **closed**
     this round.
   - If it still reproduces, the fix failed to close the issue: revert its
     diff and tests the same way as a baseline regression (step 2), mark
     the Finding **not closed**, and record why (fix was applied but
     ineffective) for Phase 8.
   - Run both the vuln-closed and feature-intact tests the fixer wrote for
     this Finding as part of this check — they should now both pass; if
     either doesn't, treat it the same as a failed re-attack.

4. **Check for newly opened surfaces.** For each Finding closed in step 3,
   review whether its diff introduced anything that wasn't in Phase 1's
   surface map: a new parameter, a new code path, a new dependency, a
   changed trust boundary (e.g. a new validation function that itself
   parses untrusted input, a new config flag, a new internal endpoint used
   by the fix). If so, note the **touched area** precisely (the new or
   changed surface, not the whole app).

5. **Decide whether to loop.** 
   - If step 4 found no newly opened surfaces for any fix applied this
     round, this round is done — proceed to step 6.
   - If step 4 found newly opened surface(s), and the harden-round counter
     is **below 3**, increment the counter and loop back to
     `phases/3-attack-loop/SKILL.md`, scoped **only** to the touched
     area(s) identified in step 4 (not a full re-run of the whole attack
     plan) — dispatch attacker subagents against just that surface, then
     flow back through Phases 4, 5, 6, and this phase again for whatever
     new Findings that produces.
   - If step 4 found newly opened surface(s) but the harden-round counter
     has already **reached 3**, do not loop again. Stop here: record every
     remaining open item (newly opened surfaces not yet attacked, and any
     Finding still open) as residual risk for Phase 8, explicitly noting
     the round cap was hit.

6. **Finalize this run's apply state.** Once no further looping is needed
   (or the cap stopped it), assemble the final record: every Finding's
   disposition (`applied+closed`, `applied+reverted:baseline-regression`,
   `applied+reverted:fix-ineffective`, `rejected` [carried from Phase 6],
   or `not-applied:needs-manual-design` [carried from Phase 6]), the
   harden-round count actually used, and confirmation the full baseline is
   green in the final state of the working tree.

## Outputs

- **Applied, baseline-green working tree**: only fixes that survived both
  the baseline re-run and the re-attack are left in place.
- **Per-finding disposition record**: final status of every Finding that
  reached this phase, feeding directly into Phase 8's "Fixes applied" and
  "Residual risks" tables.
- **Harden-round count** used this run (1–3), and, if the cap was hit with
  open items remaining, an explicit note of what's still open and why the
  loop stopped.

## Gate / loop rule

- **Baseline guardrail (hard block, every round):** any single feature
  baseline test failure blocks that round's offending fix(es) — never
  weakened, never overridden, never deferred "to fix later."
- **Re-attack requirement:** a fix is only considered to have closed a
  Finding if its original attack no longer reproduces against the patched
  app — an applied diff that doesn't stop the re-attack is reverted, not
  reported as fixed.
- **HARDEN-ROUND CAP = 3.** The apply → baseline-check → re-attack →
  new-surface-check cycle runs at most 3 times per run. On hitting the cap
  with open items, stop looping and hand everything remaining to Phase 8 as
  residual risk requiring explicit user risk-acceptance — kryptonite does
  not chase a fully clean result indefinitely.

## Next phase

When this phase completes without looping further (either nothing left to
attack, or the round cap was reached), proceed to
`phases/8-readiness-report/SKILL.md`, handing it the per-finding disposition
record, the harden-round count used, and the final baseline-green state of
the working tree.
