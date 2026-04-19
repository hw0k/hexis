---
name: verify
description: Use before claiming any work is complete, fixed, or passing — requires running verification commands and confirming output
type: workflow
---

# Verify

## Overview

A claim without evidence is a lie.

**Core principle:** Evidence first. Completion claims second.

## $ARGUMENTS

If `$ARGUMENTS` describes the verification scope, use it. Otherwise infer from current context.

## Complexity Check

Before starting, assess scope complexity against these criteria (any one is sufficient):
- Verification spans multiple subsystems
- Success criteria are ambiguous
- Multiple verification strategies are applicable

**Complex scope** → call `EnterPlanMode`. Define verification commands and expected outputs, get user approval via `ExitPlanMode` before running anything.
**Simple scope** → proceed directly.

## Task Tracking

### On Start

Call `TaskList` filtered by prefix `verify:`. If open Tasks exist from a prior session:
- Use `AskUserQuestion`: **Resume** (use `TaskGet` to verify state) or **Start fresh** (call `TaskStop` on all open Tasks)
- If no open Tasks: proceed directly

### Step Schedule

| Check | On Start | On Done |
|---|---|---|
| Type check | `TaskCreate("verify: type check")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Lint | `TaskCreate("verify: lint")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Tests | `TaskCreate("verify: tests")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |

Only create a Task for checks that are applicable. Skip a Task entirely if the check is declared inapplicable.

When `verify` is invoked as a sub-step by another skill (`review`, `finish`), it manages its own Tasks independently — no coordination with the calling skill needed.

### On Failure or Abort

Call `TaskStop` on the current open Task.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not run verification commands in this message, you cannot claim completion.

## Verification Sequence

Run in order. All must pass before claiming completion.

**1. Type check** (if applicable)
```
Run: <typecheck command>
Expected: 0 errors
```

**2. Lint** (if applicable)
```
Run: <lint command>
Expected: 0 errors/warnings
```

**3. Tests**
```
Run: <test command>
Expected: all pass, 0 failures
```

If no static tool exists for the domain, declare it explicitly: "No static validator available for this format. Manual review required."

## P3 Requirement

All verification claims must cite tool output.

**Forbidden phrases:**
- "looks right"
- "should work"
- "seems correct"
- "probably fine"

## Gate Function

```
Before claiming completion:
1. IDENTIFY: which command proves this claim?
2. RUN: full command (fresh, complete)
3. READ: full output, exit code, failure count
4. VERIFY: does the output confirm the claim?
   - NO: state actual status with evidence
   - YES: proceed to step 5
5. SYNC: invoke hexis:sync-working-status
6. ONLY THEN: claim
```

## On Failure

If any check fails: fix it and re-run the full sequence. Do not selectively re-run individual checks.
