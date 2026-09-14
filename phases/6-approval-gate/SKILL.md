---
name: kryptonite-phase-6-approval-gate
description: Present each proposed fix (diff, two tests, severity, risk) to the user and record an explicit approve, reject, or edit decision before anything touches the working tree.
---

# Phase 6 — Approval Gate (GATE)

This is the last checkpoint before the target app's working tree changes.
Every fix package from Phase 5 is a proposal, not a change. Nothing in this
phase applies a diff — it only presents, discusses, and records a decision.
This is the propose-then-approve model that governs the entire kryptonite
loop.

## Inputs

- **Proposed fix packages** from Phase 5, one per confirmed Finding, in
  priority order (P0 → P3): `{finding, priority, diff, vuln_closed_test,
  feature_intact_test, risk_note}`.
- Any Findings Phase 5 flagged as "needs manual design" (no safe minimal
  fix produced) — these are presented too, without a diff, so the user
  knows they exist and can decide how to handle them outside this run.

## Procedure

1. **Present fix packages in priority order**, P0 first. For each Finding,
   show:
   - The Finding itself: `id`, `dimension`, `title`, `surface`, `severity`,
     `exploitability`, and derived `priority`.
   - The **diff** exactly as the fixer produced it (unified diff format,
     unmodified).
   - Both **tests**, each labeled (`# vuln-closed: ...` /
     `# feature-intact: ...`), full text.
   - The **risk note** — blast radius, what the two tests don't cover,
     residual concerns.
   Do not summarize or paraphrase the diff/tests away — the user is
   approving the literal text that Phase 7 will apply verbatim.

2. **Ask for an explicit decision per finding.** For each fix package, the
   decision is exactly one of:
   - **Approve** — apply this diff and these tests as-is in Phase 7.
   - **Reject** — do not apply anything for this Finding; it carries
     forward to Phase 8 as a residual risk (its `status` stays
     `confirmed`/`plausible`, but no fix is applied).
   - **Edit** — the user requests a change to the diff, the tests, or both.
     Send the requested change back to Phase 5's fixer flow (re-dispatch a
     fixer subagent with the user's edit request as additional context),
     produce a revised fix package, and present it again at this same gate
     — do not treat an edit request as an approval of the original.
   Do not infer a decision from silence or from approval of a different
   Finding — batch approval across the full set is fine if the user
   explicitly grants it ("approve all P0/P1"), but a blanket assumption
   without that explicit statement is not sufficient.

3. **Record every decision** against the Finding's `id`: `approved`,
   `rejected`, or `edited` (with the edit's outcome — either a subsequently
   approved revision, or ultimately rejected/still pending). This record is
   what Phase 7 reads to know what it's allowed to touch, and what Phase 8
   cites in the "Fixes applied" / "Residual risks" tables (the report
   template's "Approved by" column comes from here).

4. **Handle "needs manual design" Findings.** These have no diff to
   approve. Record the user's disposition explicitly: accept as residual
   risk (goes to Phase 8 as such), or flag for out-of-band manual work
   (still goes to Phase 8's residual risks, with a note that it needs
   follow-up outside this run). Either way, nothing here gets applied by
   Phase 7 since there's no diff.

5. **Do not proceed until every fix package presented in step 1 has a
   recorded decision.** Partial runs (some findings decided, others left
   hanging) are not valid input to Phase 7 — Phase 7 needs a complete,
   unambiguous approval record to know its exact scope of work.

## Outputs

- **Approval record**: for every Finding processed in this phase, its
  final decision (`approved` / `rejected` / `edited→<approved|rejected>`)
  and, for every `approved` decision, the exact diff and two tests to
  apply — which may be the original Phase 5 proposal or a revised one from
  an edit round.
- The set of **approved fix packages** — only these are handed to Phase 7's
  apply step. Rejected and still-unresolved "needs manual design" items are
  NOT handed to Phase 7 for application; they flow directly toward the
  Phase 8 residual-risk table instead.

## Gate

**This entire phase is the gate.** No diff is applied to the working tree
here or in any prior phase — Phase 7 is the only phase authorized to write
to the target app, and it may write only what this phase's approval record
authorizes. If the user rejects or defers a fix package, kryptonite does
not apply it, does not silently retry it, and does not treat rejection as
something to route around — it is a final decision for this run, revisited
only if the user explicitly asks for a new run or a new edit round.

## Next phase

Proceed to `phases/7-apply-and-reverify/SKILL.md`, handing it the approval
record and the set of approved fix packages (diffs + tests) to apply.
