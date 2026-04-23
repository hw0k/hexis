---
issue: 27
---

# TDD Workflow Restructure — Remove write-test, add testing-principles

## Problem

`hexis:write-test` is a disconnected workflow step. `hexis:plan` already writes TDD-style step structures (failing test → confirm failure → minimal impl → confirm pass → commit), and `hexis:dispatch` routes directly from plan → implement without routing through write-test. The skill duplicates intent without adding a meaningful gate.

Additionally, testing knowledge is currently siloed in write-test, making it inaccessible to plan (when designing steps) and implement (when executing them).

## Goal

1. Delete `hexis:write-test` entirely.
2. Embed conditional TDD into `hexis:plan` — each task in a plan decides whether TDD applies.
3. Create `hexis:testing-principles` as a reference skill containing testing knowledge usable by plan, implement, and the principles reviewer.
4. Update `hexis:implement` to reference testing-principles when executing TDD steps.
5. Add testing-principles to the principles-reviewer scope.

## Changes

### 1. Delete `skills/write-test/`

Delete the entire directory. No stub or redirect left behind.

### 2. New skill: `skills/testing-principles/SKILL.md`

Type: `reference`

Scope — covers everything needed to write good tests across the hexis workflow:

**Red-Green-Refactor cycle** (from write-test)
- RED: Write one failing test, one behavior, real code over mocks
- Verify RED: test must fail with an expected message (missing function, not a typo)
- GREEN: minimal code that makes the test pass — no extras
- Verify GREEN: test must pass, cite actual runner output ("should pass" is not verification)
- REFACTOR: improve without adding behavior, only after GREEN confirmed

**Iron Law** (from write-test)
- No production code without a failing test first
- If code was written before a test: delete it and start over

**Test type selection criteria** (new)
- Unit test: pure functions, isolated business logic, single-module behavior — default choice
- Integration test: behavior that spans module boundaries, I/O (database, filesystem, HTTP) — use when unit test would require mocking the actual subject
- E2E test: critical user flows only — expensive, fragile, use sparingly
- Rule: prefer the lowest-level test that meaningfully validates the behavior

**Mock guidelines** (expanded from write-test)
- Mock external I/O (HTTP, DB, filesystem) at the boundary, not deep inside
- Never mock the module under test
- If a test requires mocking more than 2 dependencies: the design is too coupled — refactor first
- Prefer real implementations (in-memory DB, test fixtures) over mocks when feasible

**Test naming**
- Name describes behavior, not implementation: `retries failed operations 3 times` not `test_retry_fn`
- Pattern: `[subject] [action/condition] [expected outcome]`

**Coverage**
- Behavior coverage over line coverage: every distinct code path must have a named behavior test
- Do not chase 100% line coverage — test behavior, not lines
- Untested edge cases are bugs waiting to happen: test boundaries explicitly

**What not to test**
- Implementation details (private methods, internal variable names)
- External library behavior (assume libraries work)
- Type-only changes (compiler already catches these)
- Framework boilerplate (routing wiring, DI container setup)

### 3. Modify `skills/plan/SKILL.md` — conditional TDD

Add a **TDD Applicability** section after File Structure and before Task Size.

#### TDD Applicability

For each task in the plan, determine whether TDD applies before writing steps.

**TDD applies when the task involves:**
- New functions, classes, or modules
- Changes to existing logic (bug fixes, behavior changes)
- New or modified API endpoints

**TDD does not apply when the task involves only:**
- Configuration files (env, package.json, tsconfig, etc.)
- Documentation, skill files, or markdown
- Database migration files (these are verified by running the migration)
- Type-only refactoring (no behavior change)
- UI layout/styling with no associated business logic

#### TDD Step Structure (when TDD applies)

The current default step structure stays as-is:
```
- [ ] Step 1: Write failing test
- [ ] Step 2: Confirm failure (run: <command>, Expected: FAIL — "<message>")
- [ ] Step 3: Minimal implementation
- [ ] Step 4: Confirm pass (run: <command>, Expected: PASS)
- [ ] Step 5: Commit
```

Add a reference to `hexis:testing-principles` in the plan header note:
> For agentic workers: REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. For TDD tasks, follow `hexis:testing-principles`.

#### Non-TDD Step Structure (when TDD does not apply)

For tasks where TDD does not apply, use a simpler step structure:
```
- [ ] Step 1: Implement
- [ ] Step 2: Verify (run: <exact command>, Expected: <expected output>)
- [ ] Step 3: Commit
```

The plan must label each task clearly: include `[TDD]` or `[No TDD — <reason>]` in the task name or a brief note at the top of the task.

### 4. Modify `skills/implement/SKILL.md`

In the "Notes" section, add:
> For tasks marked `[TDD]`, follow the Red-Green-Refactor cycle from `hexis:testing-principles`. The failing test must be seen to fail before writing implementation code.

No other changes to implement — it executes what the plan says.

### 5. Modify `agents/principles-reviewer.md`

Add `hexis:testing-principles` as the fifth review area:

**Scope:** Add a fifth item:
> 5. **Testing** (`hexis:testing-principles`) — TDD applicability judgment in plans, Iron Law compliance, mock usage, test naming, coverage approach

**Before You Start:** Add `hexis:testing-principles` to the read list.

**Output Format:** Add a Testing section to the output structure.

Note: testing-principles is a reference skill, not a process enforcement skill — violations here are about test quality and TDD skips without `[No TDD — <reason>]` justification.

## Out of Scope

- Changes to `hexis:dispatch` routing — dispatch already routes plan → implement; write-test was never in the routing table
- Changes to `hexis:specify` — TDD is a plan/implement concern
- Changes to `hexis:verify` — post-implementation verification is separate

## Done Criteria

- `skills/write-test/` directory does not exist
- `skills/testing-principles/SKILL.md` exists with all sections listed above
- `skills/plan/SKILL.md` includes TDD applicability criteria and both TDD/non-TDD step structures
- `skills/implement/SKILL.md` references testing-principles for TDD tasks
- `agents/principles-reviewer.md` includes testing-principles in scope and output
- All changes committed; no references to `hexis:write-test` remain in the repo
