---
plan: docs/plans/2026-04-01-issues-2-3-4-plan-mode-sync-pre-commit.md
---

# Plan Mode Migration to Executing Task Skills

## Problem

`specify` and `plan` skills currently use EnterPlanMode/ExitPlanMode, which conflicts with plan mode's intent.

Plan mode's purpose: **human gate for complex tasks** — a person approves the approach before actual code changes are made. Specify and plan are already planning activities that produce documents (spec/plan files), so applying plan mode to them creates a "plan for the plan," which is redundant.

## What

### Remove EnterPlanMode/ExitPlanMode from

- `skills/specify/SKILL.md` — remove plan mode calls and related checklist items
- `skills/plan/SKILL.md` — remove plan mode calls and related checklist items

### Add EnterPlanMode/ExitPlanMode to

- `skills/write-test/SKILL.md`
- `skills/implement/SKILL.md`
- `skills/verify/SKILL.md`

## Gate Rule

```
Complex task → use plan mode (human gate before execution)
Simple task  → skip plan mode (proceed directly)
```

**Complex criteria (any one is sufficient):**
- Changes span multiple files
- Approach is unclear (multiple valid approaches exist)
- Architectural or structural decisions required
- Test design is non-obvious

## Out of Scope

- No other logic changes to specify or plan skills
- No changes to human gate mechanisms other than plan mode

## Done When

- [ ] `specify` and `plan` skills have no EnterPlanMode/ExitPlanMode references
- [ ] `write-test`, `implement`, `verify` skills enter plan mode based on complexity criteria
