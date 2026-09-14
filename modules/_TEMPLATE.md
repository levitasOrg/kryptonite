---
name: module-slug-here
description: "One-sentence summary of what this module attacks and why it matters."
applies-to: [web, api, cli, mobile, language:python, framework:django]
---

# Module Name

<!--
This is the drop-in contract for a kryptonite attack module. Copy this file,
rename it to `modules/<your-dimension>.md`, fill in the frontmatter and all
seven body sections below, then delete this comment block. Phase 2
(`phases/2-scenario-design/SKILL.md`) reads every `modules/*.md` file, matches
its `applies-to` list against the surface map's detected stack, and — if
matched — turns this module's Probes into concrete, target-specific
scenarios. Phase 3 (`phases/3-attack-loop/SKILL.md`) dispatches one attacker
subagent per selected module (or scenario cluster) to run those scenarios and
emit Finding objects shaped per `references/finding-schema.md`.

Frontmatter requirements:
- `name`        — short slug, matches the filename stem and becomes the
                   Finding's `dimension` value.
- `description` — one sentence, shown to the user during module selection.
- `applies-to`  — EXACT field name Phase 2 matches on. A flat list of stack
                   signals: surface kind (web/api/cli/mobile/desktop), and/or
                   `language:<x>` / `framework:<x>` tags. Match is
                   any-overlap, not all-required — list every signal that
                   makes this module relevant, not just the narrowest one.
-->

## Purpose

<!-- One line: what class of weakness this module exists to surface, and why it matters for a shipped app. -->

## Applies-to (detail)

<!-- One line: spell out, in prose, what the frontmatter `applies-to` tags mean in practice — which stacks/surfaces this targets and which it explicitly does not. -->

## Probes

<!-- One line: the instruction is to list concrete, named techniques here — not a description of "testing," but the actual probes an attacker subagent runs, each specific enough to adapt to a real route/parameter/field without guessing. -->

## What "safe" looks like

<!-- One line: describe, per probe (or per probe group), the observable behavior a hardened app exhibits — precise enough that pass/fail needs no judgment call. -->

## Severity rubric

<!-- One line: map this module's specific failure modes to the `critical`/`high`/`medium`/`low`/`info` levels from `references/severity.md`, so scenario authors don't have to guess a severity from scratch. -->

## Detection method

<!-- One line: state how an attacker/verifier agent confirms a probe failed — status codes, response diffs, timing thresholds, log lines, resource metrics — concrete enough to populate a Finding's `evidence` field. -->

## References

<!-- One line: name the existing skills, standards, or docs this module's probes are drawn from, so an agent can pull deeper technique detail on demand. -->
