---
name: kryptonite-phase-4-verify-findings
description: Adversarially reproduce every candidate Finding, dedupe, and rank confirmed findings by severity times exploitability into a priority.
---

# Phase 4 — Verify Findings

Attacker subagents in Phase 3 report what they believe they saw. This phase
does not trust that on faith — it reproduces each candidate independently,
kills false positives, merges duplicates, and assigns the authoritative
`severity`/`exploitability`/`status` that everything downstream relies on.

## Inputs

- **Validated candidate Findings** from Phase 3: a JSON array of Finding
  objects, `status: "candidate"`, schema-valid per
  `references/finding-schema.md`.
- **Environment details** from Phase 1/3: how to reach the same app the
  attackers used (or the same static-analysis context), so verification
  reproduces against an identical target.

## Procedure

1. **Partition candidates for verification.** Group candidates so each
   verifier subagent gets a coherent batch to work through — typically by
   `dimension` (mirroring the Phase 3 clusters), or by `surface` when many
   candidates across dimensions hit the same surface and are likely
   duplicates that benefit from one verifier seeing them together.

2. **Dispatch verifier subagents in parallel**, one per batch, using the
   **VERIFIER** prompt block in `references/agent-prompts.md`, filling in:
   - `[CANDIDATE_FINDINGS]` — that batch's JSON array of candidates.
   - `[ENV_DETAILS]` — the same reach-the-app details Phase 3 used, so
     reproduction happens against an equivalent target from a clean state.

3. **Enforce the verifier rules while agents run** (restated from
   `references/agent-prompts.md`):
   - Reproduce independently from each candidate's `repro` steps — never
     accept the attacker's `evidence` on faith.
   - Same local/test-only, no-destructive-action constraints as attackers.
   - Dedupe same-root-cause candidates into one Finding before finishing;
     note merged-away ids in `evidence`.
   - Be skeptical, not credulous or dismissive: `confirmed` requires an
     independent repro; `plausible` requires a credible mechanism without a
     forced clean repro; `rejected` requires positive evidence the issue
     doesn't hold.

4. **Collect verifier output.** Each verifier returns a JSON array of
   Findings with `status` set to `confirmed`, `plausible`, or `rejected`
   (never left as `candidate`), `severity` and `exploitability` re-derived
   from what the verifier actually observed, plus a one-line summary:
   candidates in → confirmed/plausible/rejected/merged-as-duplicate counts.
   Merge all batches into one combined verified list.

5. **Cross-batch dedupe.** Verifiers only dedupe within their own batch.
   Scan the combined list for near-duplicates that landed in different
   batches (same `surface` and materially the same underlying weakness,
   even if `dimension` differs — e.g. a rate-limit gap found by both
   `api-abuse-and-limits` and `load-chaos-resilience`). Merge these the
   same way a verifier would: keep the clearer Finding, note the merged-away
   `id` in `evidence`.

6. **Rank by severity × exploitability.** For every Finding with
   `status: "confirmed"` or `"plausible"`, look up its `severity` and
   `exploitability` pair in the matrix in `references/severity.md` to
   derive its **priority** (`P0`–`P3`). Priority is not a Finding field —
   record it alongside the Finding (e.g. a parallel `priority` map keyed by
   `id`) for use in Phase 5 ordering and the Phase 8 report table.

7. **Sort and summarize.** Produce the final ranked list sorted P0 → P3
   (ties broken by `severity` then `exploitability`), and a summary: total
   candidates in, total confirmed, total plausible, total rejected, total
   merged.

## Outputs

- **Ranked, confirmed findings list**: every Finding with a final
  `status` (`confirmed`, `plausible`, or `rejected`), re-derived
  `severity`/`exploitability`, deduped across all batches, each with its
  looked-up `priority` recorded alongside it, sorted P0 → P3.
- Rejected Findings are **kept, not discarded** — they still carry
  `status: "rejected"` and travel forward to Phase 8's audit trail, but
  they do not proceed into Phase 5's fix design.
- Verification summary counts (candidates in → confirmed/plausible/
  rejected/merged) for the eventual readiness report.

## Gate / loop rule

No user-facing gate — verification is an internal adversarial check, not a
decision point for the user. The hard rule: no Finding advances to Phase 5
without an explicit `status` of `confirmed` or `plausible` assigned by a
verifier (never a candidate's self-reported status carried forward
unchanged), and every `severity`/`exploitability` pair feeding Phase 5's
ordering must be the verifier's re-derived value, not the attacker's
first-pass estimate.

## Next phase

Proceed to `phases/5-design-fixes/SKILL.md`, handing it the ranked list of
`confirmed` (and any orchestrator-selected `plausible`) Findings, in P0 → P3
order, plus the full list (including `rejected`) for the eventual report.
