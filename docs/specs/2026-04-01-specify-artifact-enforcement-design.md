---
---

# Specify Skill — Artifact Enforcement Design

**Date:** 2026-04-01
**Status:** Approved
**Issue:** hw0k/claude-hw0k-workflow#1

---

## Problem

`hw0k-workflow:specify` can complete without writing a spec file to `docs/specs/`. The two-stage artifact flow (spec file → plan hand-off) is not enforced. Two concrete failure modes observed in production:

1. **ExitPlanMode rejected → spec abandoned:** When ExitPlanMode is rejected mid-flow, there is no recovery path. The spec-writing step is silently dropped and the flow jumps to implementation.
2. **Plan file conflated with spec file:** The draft in `~/.claude/plans/` is a temporary approval vehicle, but agents treat it as the output artifact and skip writing `docs/specs/`.

## Behavior After Fix

- The spec file (`docs/specs/YYYY-MM-DD-<topic>-design.md`) **must** exist and be committed before `hw0k-workflow:plan` is invoked — no exceptions.
- The plan file draft is explicitly labeled as temporary (not the output artifact).
- If ExitPlanMode is rejected → return to Step 3 (re-draft). Do not abandon the spec-writing step.
- If the user explicitly requests to skip the spec file → `AskUserQuestion` human gate confirms. If confirmed, the skip is noted explicitly.

## Change

**One file only: `skills/specify/SKILL.md`**

### 1. Clarify Step 3 — plan file is draft, not spec

Add a note under Step 3 that the plan file is a temporary approval draft only. The real output artifact is `docs/specs/`. These are two separate things.

### 2. Strengthen Step 4 — MANDATORY label + immediate action

Current:
> After approval, write to `docs/specs/YYYY-MM-DD-<topic>-design.md`.

Replacement:
> **MANDATORY — do this immediately after approval, before anything else:** Write to `docs/specs/YYYY-MM-DD-<topic>-design.md` and commit.

### 3. Add HARD-GATE at Step 5

Before invoking `hw0k-workflow:plan`, add an explicit gate:

> **HARD-GATE:** Before invoking `hw0k-workflow:plan`, verify the spec file exists: check `docs/specs/` and confirm the file is present and committed. If it is not, write it now — do not proceed without it.

### 4. Add ExitPlanMode-rejected recovery rule

New rule in the Rules section:
> If ExitPlanMode is rejected: return to Step 3 and re-draft. Do NOT skip to implementation.

### 5. Add user-skip confirmation rule

New rule in the Rules section:
> If the user requests to skip writing the spec file: use `AskUserQuestion` to confirm. Only skip with explicit confirmation. Note the skip explicitly so the user knows no spec artifact was produced.

## Out of Scope

- `plan/SKILL.md` — not changed
- New files or new tools
- Changes to ExitPlanMode tool behavior
- Verification gates inside the plan skill itself

## Done When

1. `specify/SKILL.md` has an explicit HARD-GATE at Step 5
2. Plan file draft is clearly labeled as NOT the output artifact in Step 3
3. Step 4 is labeled MANDATORY with "immediately, before anything else" language
4. ExitPlanMode-rejected recovery path is in the Rules section
5. User-skip confirmation gate is in the Rules section
