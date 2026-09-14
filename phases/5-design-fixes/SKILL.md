---
name: kryptonite-phase-5-design-fixes
description: For every confirmed finding, design a minimal fix diff plus a vuln-closed test and a feature-intact test, without applying anything.
---

# Phase 5 — Design Fixes

This phase designs; it never applies. Every output here is a proposal —
diff text and test text — that a human reviews in Phase 6. Nothing in this
phase touches the target app's working tree.

## Inputs

- **Ranked, confirmed findings list** from Phase 4: Findings with
  `status: "confirmed"` (or orchestrator-selected `plausible`), each with
  its re-derived `severity`/`exploitability` and looked-up `priority`,
  sorted P0 → P3.
- **Codebase context**: pointers into the target app's source tree for each
  Finding's `surface`, plus the app's existing test suite/conventions
  (framework, file layout, naming) captured during Phase 1 recon.

## Procedure

1. **Order the work by priority.** Process Findings P0 first, then P1, P2,
   P3 — dispatch order should let the user see the highest-stakes fixes
   soonest at the Phase 6 gate, even though all proposals for this round
   are typically produced before that gate opens.

2. **Dispatch one fixer subagent per confirmed Finding**, using the
   **FIXER** prompt block in `references/agent-prompts.md`, filling in:
   - `[CONFIRMED_FINDING]` — the single Finding object (schema-valid per
     `references/finding-schema.md`) this subagent designs a fix for.
   - `[CODEBASE_CONTEXT]` — the relevant source files for that Finding's
     `surface`, the existing test suite/conventions, and any
     framework-specific constraints.
   Independent Findings can be dispatched in parallel (the standing
   "deploy agents for parallel work" permission applies here too). Findings
   that touch the same file or the same surface should be sequenced or
   explicitly cross-referenced, so two fixers don't independently propose
   conflicting diffs against the same lines — if that happens anyway,
   reconcile before Phase 6 by re-dispatching one fixer with the other's
   diff as additional context.

3. **Enforce the fixer rules while agents run** (restated from
   `references/agent-prompts.md`):
   - **Do NOT apply the fix.** No file is edited, saved, or committed by a
     fixer subagent — output is text only (diff + tests + risk note).
   - **Minimal diff.** Close the specific weakness in `surface` with the
     smallest change that does it; no unrelated refactors, renames, or
     drive-by cleanup.
   - **Never regress the feature.** The fix must close the weakness
     without breaking the legitimate behavior that surface exists to serve
     — this is the same guardrail principle Phase 1's baseline exists to
     protect, applied at design time.
   - **Exactly two tests**, no more, no fewer:
     - a **vuln-closed test** that reproduces the Finding's `repro` (or the
       smallest faithful equivalent) against the proposed fix and asserts
       the weakness no longer holds;
     - a **feature-intact test** that exercises the same surface with
       legitimate input and asserts the feature still works — this test
       must fail on the unfixed code and pass after the fix.
   - **Match existing conventions** — the app's own test framework, style,
     and file layout; no new testing library introduced for one fix.

4. **Collect each fixer's three outputs**, in order: the unified diff
   (`--- a/path` / `+++ b/path`), the two labeled test functions
   (`# vuln-closed: ...` / `# feature-intact: ...`), and the risk paragraph
   (blast radius, what the two tests don't cover, residual concerns).
   Attach each proposal to its Finding's `id`.

5. **Sanity-check every proposal before it reaches the gate:**
   - The diff touches only files relevant to the Finding's `surface` — flag
     (don't silently trim) anything that looks like scope creep.
   - Both required tests are present and each is labeled correctly; a
     fixer that produced only one test, or two vuln-closed tests, is
     re-dispatched with that gap called out.
   - The risk paragraph is non-empty and names something concrete, not a
     generic "no risk" — if a fixer claims zero risk, ask it to justify
     that against what the feature-intact test does *not* cover.
   - No proposal contains a written-to-disk change — this is a text
     proposal, not a working-tree diff already applied; if a fixer's
     transcript shows it edited a file, discard the proposal and
     re-dispatch with the rule restated.

6. **Assemble per-finding fix packages.** For every confirmed Finding now
   carrying a sanity-checked proposal, bundle: the Finding object, its
   `priority`, the diff, the two tests, and the risk note. This bundle is
   exactly what Phase 6 presents.

## Outputs

- **Proposed fix packages**, one per confirmed Finding processed this
  round: `{finding, priority, diff, vuln_closed_test, feature_intact_test,
  risk_note}`. No working-tree change has occurred — everything here is
  text pending approval.
- Any Finding a fixer could not produce a safe minimal fix for (e.g. the
  fix would require an architectural change out of scope for this run) is
  passed forward without a diff, flagged for the user to see at the gate as
  "needs manual design" rather than silently dropped.

## Gate / loop rule

No approval gate in this phase — that's Phase 6. The internal rule: a fix
package with a missing test, an unlabeled test, or evidence the fixer wrote
to disk does not advance; it is corrected or re-dispatched until it meets
the checklist in step 5.

## Next phase

Proceed to `phases/6-approval-gate/SKILL.md`, handing it the full set of
proposed fix packages in priority order (P0 → P3).
