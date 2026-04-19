---
name: write-test
description: Use when implementing a feature or fix — write failing tests before writing implementation code
type: workflow
---

# Write Test

## Overview

Test first. Confirm failure. Pass with minimal code.

**Core principle:** You cannot verify a test is correct unless you see it fail.

## $ARGUMENTS

If `$ARGUMENTS` describes a feature or function, use it as the starting context. Otherwise use `AskUserQuestion` to identify the target behavior.

## Complexity Check

Before starting, assess task complexity against these criteria (any one is sufficient):
- Changes span multiple files
- Approach is unclear (multiple valid approaches exist)
- Test design is non-obvious or requires architectural decisions

**Complex task** → call `EnterPlanMode`. Design the test approach and get user approval via `ExitPlanMode` before writing any code.
**Simple task** → proceed directly.

## Task Tracking

### On Start

Call `TaskList` filtered by prefix `write-test:`. If open Tasks exist from a prior session:
- Use `AskUserQuestion`: **Resume** (use `TaskGet` to verify state, continue from the last open phase) or **Start fresh** (call `TaskStop` on all open Tasks)
- If no open Tasks: proceed directly

### Step Schedule

| Phase | On Start | On Done |
|---|---|---|
| RED: Write failing test | `TaskCreate("write-test: red phase")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| GREEN: Minimal implementation | `TaskCreate("write-test: green phase")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| REFACTOR: Clean up | `TaskCreate("write-test: refactor phase")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |

Verify RED and Verify GREEN are part of their respective phase Tasks — no separate Task for each verify step.

### On Failure or Abort

Call `TaskStop` on the current open Task.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If you wrote code before a test: delete it and start over.

## Red-Green-Refactor

### RED — Write a failing test

One test, one behavior. Clear name. Real code (mocks only when unavoidable).

**For complex behavior or many edge cases:** `ultrathink` before designing test cases.

```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0
  const operation = () => {
    attempts++
    if (attempts < 3) throw new Error('fail')
    return 'success'
  }
  const result = await retryOperation(operation)
  expect(result).toBe('success')
  expect(attempts).toBe(3)
})
```

### Verify RED — It must fail

```bash
<test command> <test-file>
```

Confirm: test fails, failure message is what you expected (missing function, not a typo).

**If the test passes:** you are testing existing behavior. Fix the test.

### GREEN — Minimal code

Simplest code that makes the test pass. No extra features, no refactoring other code.

### Verify GREEN — It must pass

```bash
<test command> <test-file>
```

**P3 requirement:** Before claiming tests pass, cite actual test runner output. "Should pass" is not verification.

Confirm other tests still pass too.

### REFACTOR — Clean up

Only after GREEN is confirmed. Improve code without adding behavior.

## Pre-completion Checklist

- [ ] All new functions/methods have tests
- [ ] Each test was seen failing
- [ ] Failure reason was expected (missing function, not a typo)
- [ ] Minimal code written
- [ ] All tests pass — **cite actual output**
- [ ] Output is clean (no errors, no warnings)

Cannot check all items = process not followed. Start over.

## Completion

After all checklist items pass:

Invoke `hexis:sync-working-status`.

## When Stuck

| Problem | Solution |
|---|---|
| Don't know how to test it | Write the API you want first. Assertion first. |
| Test is too complex | Design is too complex. Simplify the interface. |
| Must mock everything | Code is too coupled. Use dependency injection. |
