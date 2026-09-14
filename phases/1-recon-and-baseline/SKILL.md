---
name: kryptonite-phase-1-recon
description: Detect the target app's stack, map its attack surface, and capture a feature baseline that every later fix must keep green.
---

# Phase 1 — Recon & Baseline

This is the first phase of the kryptonite attack-and-harden loop (see the
orchestrator at `SKILL.md`). It never attacks anything — it only observes.
Everything downstream depends on what this phase captures: a wrong or
incomplete surface map means Phase 2 designs scenarios against the wrong
target, and a thin feature baseline means Phase 7 can't tell a real
regression from noise.

## Inputs

- The target app's repository root (path given by the user, or the current
  working directory if kryptonite was invoked from inside it).
- Optionally, a `.kryptonite.md` config file at the repo root pinning stack,
  run command, and out-of-scope surfaces — read it first if present and
  prefer its answers over auto-detection where they conflict.
- Nothing from a prior phase — this is the entry point.

## Procedure

1. **Detect the stack.**
   Run `python scripts/detect_stack.py <target-root>`. It returns JSON:
   `kind` (`api` | `web` | `mobile` | `unknown`), `languages`, `runnable`,
   and `signals` (the marker files that led to the verdict). Record this
   verbatim — later phases and the final report cite it.

2. **Determine how to run the app.**
   - If `runnable` is true, use the `run` skill to find or infer how to
     start the app locally (dev server, container, CLI entry point). Start
     it and confirm it's reachable (HTTP 200 on a root/health route, a CLI
     `--help` that exits 0, etc.).
   - If the app can't be run locally (no start command discoverable, missing
     runtime, or the target root is a library with no standalone server),
     mark this run **static-only** and note why. Every later phase must
     branch on this: static-only runs use code-level probes and static
     analysis instead of live attacks.
   - Never point any run command at a production host, a shared staging
     environment, or infrastructure the user doesn't own. Local/test only.

3. **Map the surface.** Walk the codebase and (if running) the live app to
   produce a **surface map** covering:
   - **Routes/endpoints** — every HTTP route, RPC method, CLI subcommand, or
     public function/class that accepts external input.
   - **Inputs** — for each surface, the parameters/body/headers/args it
     accepts and their expected types/formats.
   - **Data stores** — databases, caches, queues, filesystems, or
     third-party APIs the app reads from or writes to.
   - **External dependencies** — third-party services, SDKs, and APIs the
     app calls out to.
   - **Auth model** — how the app authenticates and authorizes requests
     (session, token, API key, none), and which surfaces are
     public/authenticated/privileged.
   - **Trust boundaries** — every point where data crosses from a less
     trusted context to a more trusted one (user input → DB query, client →
     server, third-party webhook → internal handler, etc.).
   - **Config/secrets** — env vars, config files, and where secrets are
     expected to live (and confirm none are committed to the repo).
   For each item, mark it **in-scope** or **out-of-scope** (third-party
   payment providers, systems the user doesn't own, anything the user
   flagged in `.kryptonite.md`). Out-of-scope items are still listed, never
   silently dropped — Phase 8's report cites them.

4. **Capture the feature baseline.** This is the regression guardrail for
   the entire run — treat it as the most important output of this phase.
   - For a web/API app, use the `webapp-testing` skill to drive the running
     app through its actual current behavior: the primary user flows, the
     main happy paths for each in-scope route, and any behavior the user
     specifically says must not break.
   - For a CLI/library app, or when the app is static-only, use the `run`
     skill to exercise entry points directly and capture expected
     input/output pairs.
   - Write each captured behavior as a **characterization test**: a
     concrete, runnable test that asserts what the app does *today*,
     independent of whether that behavior is "correct" — the baseline
     records current behavior, not desired behavior. Use whatever test
     framework/runner the repo already uses; if none exists, add the
     smallest possible harness in the target app's own test directory
     convention.
   - Run the full baseline suite once now and confirm every test passes
     against the untouched app. A baseline test that doesn't pass on the
     unmodified app is not a valid guardrail — fix the test, not the app.
   - Baseline coverage should span every in-scope surface from step 3 at
     least once: if a route has no baseline test, Phase 7 has no way to
     know a fix against it broke something.

5. **Assemble the recon output.** Write two artifacts to the run's working
   notes (a scratch location the orchestrator controls, not the target
   repo):
   - `surface-map.md` — the structured inventory from step 3, plus the
     stack-detection JSON from step 1 and the runnable/static-only
     determination from step 2.
   - The baseline suite itself, living in the target app's own test tree
     (so it runs with the app's normal test command), plus a short
     `baseline-manifest.md` listing every test added, the surface it
     covers, and the exact command used to run the whole suite.

## Outputs

- **Surface map** (`surface-map.md`): stack, runnable/static-only status,
  routes/inputs/data-stores/external-deps/auth-model/trust-boundaries/
  config-secrets, each marked in-scope or out-of-scope.
- **Feature baseline suite**: characterization tests committed into the
  target app's test tree, all passing against the current, unmodified app,
  plus `baseline-manifest.md` naming the run command Phase 7 will reuse
  verbatim.

## Gate / loop rule

No gate in this phase — it is observation only, nothing is proposed or
attacked yet. The one hard requirement: do not proceed to Phase 2 until the
full baseline suite has been run once and is green. A baseline that isn't
known-green on the untouched app cannot function as a regression guardrail
later.

## Next phase

Proceed to `phases/2-scenario-design/SKILL.md`, handing it the surface map
and a pointer to the baseline suite and its run command.
