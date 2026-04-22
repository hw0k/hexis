---
name: testing-principles
description: Testing standards — Red-Green-Refactor, test type selection, mock guidelines, naming, and coverage approach
type: reference
---

# Testing Principles

## Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If code was written before a test: delete it and start over.

## Red-Green-Refactor

### RED — Write a failing test

One test, one behavior. Clear name. Real code over mocks.

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

**Verify RED:** Run the test. It must fail with the expected message (missing function, not a typo). If it passes: you are testing existing behavior. Fix the test.

### GREEN — Minimal code

Simplest code that makes the test pass. No extra features, no refactoring other code.

**Verify GREEN:** Run the test. Cite actual test runner output. "Should pass" is not verification. Confirm other tests still pass too.

### REFACTOR — Clean up

Only after GREEN is confirmed. Improve code without adding behavior.

## Test Type Selection

Prefer the lowest-level test that meaningfully validates the behavior.

| Type | When to use |
|---|---|
| Unit | Pure functions, isolated business logic, single-module behavior — default choice |
| Integration | Behavior spanning module boundaries, I/O (database, filesystem, HTTP) — use when a unit test would require mocking the actual subject |
| E2E | Critical user flows only — expensive and fragile, use sparingly |

## Mock Guidelines

- Mock external I/O (HTTP, DB, filesystem) at the boundary, not deep inside
- Never mock the module under test
- If a test requires mocking more than 2 dependencies: the design is too coupled — refactor first
- Prefer real implementations (in-memory DB, test fixtures) over mocks when feasible

## Test Naming

Name describes behavior, not implementation.

Pattern: `[subject] [action/condition] [expected outcome]`

- `retries failed operations 3 times` ✓
- `test_retry_fn` ✗

## Coverage

- Behavior coverage over line coverage: every distinct code path must have a named behavior test
- Do not chase 100% line coverage — test behavior, not lines
- Test boundaries explicitly: edge cases are bugs waiting to happen

## What Not to Test

- Implementation details (private methods, internal variable names)
- External library behavior (assume libraries work)
- Type-only changes (compiler already catches these)
- Framework boilerplate (routing wiring, DI container setup)
