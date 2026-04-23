---
linked_spec: docs/specs/2026-04-22-tdd-workflow-restructure-design.md
issue: 27
---

# TDD Workflow Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove `hexis:write-test`, create `hexis:testing-principles`, and embed conditional TDD into `hexis:plan`.

**Architecture:** All changes are markdown/skill file edits — no production code, no tests required. Each task modifies exactly one file (or deletes one directory). Tasks are independent with no cross-task data dependencies, so all five can be dispatched in parallel.

**Tech Stack:** Markdown, hexis skill format (YAML frontmatter + markdown body)

---

## File Structure

- Delete: `skills/write-test/` (entire directory)
- Create: `skills/testing-principles/SKILL.md`
- Modify: `skills/plan/SKILL.md` — header note, Task Size, Step Structure sections
- Modify: `skills/implement/SKILL.md` — Notes section
- Modify: `agents/principles-reviewer.md` — Scope, Before You Start, Output Format, Instructions

---

### Task 1: Delete skills/write-test/ [No TDD — deleting documentation directory]

**Files:**
- Delete: `skills/write-test/SKILL.md` and directory

- [ ] **Step 1: Implement**

```bash
rm -rf skills/write-test
```

- [ ] **Step 2: Verify**

```bash
ls skills/ | grep write-test
```

Expected: no output (directory gone)

- [ ] **Step 3: Commit**

```bash
git add -A skills/write-test
git commit -m "refactor(write-test): remove skill — merged into plan + testing-principles (#27)"
```

---

### Task 2: Create skills/testing-principles/SKILL.md [No TDD — creating documentation file]

**Files:**
- Create: `skills/testing-principles/SKILL.md`

- [ ] **Step 1: Implement**

Create `skills/testing-principles/SKILL.md` with this exact content:

```markdown
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
```

- [ ] **Step 2: Verify**

```bash
head -5 skills/testing-principles/SKILL.md
```

Expected:
```
---
name: testing-principles
description: Testing standards — Red-Green-Refactor, test type selection, mock guidelines, naming, and coverage approach
type: reference
---
```

- [ ] **Step 3: Commit**

```bash
git add skills/testing-principles/SKILL.md
git commit -m "feat(testing-principles): add testing standards reference skill (#27)"
```

---

### Task 3: Modify skills/plan/SKILL.md [No TDD — modifying skill documentation]

**Files:**
- Modify: `skills/plan/SKILL.md`

Three edits, applied in order:

**Edit A — Plan header note** (line 69): Add testing-principles reference.

- [ ] **Step 1: Implement Edit A**

Replace in `skills/plan/SKILL.md`:

```
> **For agentic workers:** REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. Steps use checkbox (`- [ ]`) syntax for tracking.
```

With:

```
> **For agentic workers:** REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. For TDD tasks, follow `hexis:testing-principles`. Steps use checkbox (`- [ ]`) syntax for tracking.
```

**Edit B — Add TDD Applicability section** between File Structure (line 84) and Task Size (line 86):

Replace:

```
**ultrathink** before decomposing tasks — never skip this.

## Task Size

Each task: one action, 2–5 minutes. Steps: write failing test → confirm failure → minimal implementation → confirm pass → commit.
```

With:

```
**ultrathink** before decomposing tasks — never skip this.

## TDD Applicability

For each task, determine whether TDD applies before writing steps.

**TDD applies when the task involves:**
- New functions, classes, or modules
- Changes to existing logic (bug fixes, behavior changes)
- New or modified API endpoints

**TDD does not apply when the task involves only:**
- Configuration files (env, package.json, tsconfig, etc.)
- Documentation, skill files, or markdown
- Database migration files (verified by running the migration)
- Type-only refactoring (no behavior change)
- UI layout/styling with no associated business logic

Label each task `[TDD]` or `[No TDD — <reason>]` in the task name.

## Task Size

Each task: one action, 2–5 minutes. Use the TDD or non-TDD step structure below based on the task label.
```

**Edit C — Add non-TDD step structure** after the existing TDD step structure (after the closing ```````` on line 132):

Replace:

````
````
````

(the closing ```````` of the Step Structure code block)

With:

`````
````

### Non-TDD Step Structure

For tasks labeled `[No TDD — <reason>]`:

````markdown
### Task N: [Name] [No TDD — <reason>]

**Files:**
- Create/Modify/Delete: `exact/path/to/file`

- [ ] **Step 1: Implement**

[exact changes — no placeholders]

- [ ] **Step 2: Verify**

Run: `<exact command>`
Expected: `<exact expected output>`

- [ ] **Step 3: Commit**

```bash
git add <files>
git commit -m "type: description (#issue)"
```
````
`````

- [ ] **Step 2: Verify**

```bash
grep -n "TDD Applicability\|No TDD\|testing-principles" skills/plan/SKILL.md
```

Expected: lines containing "TDD Applicability", "No TDD", and "testing-principles" all present.

- [ ] **Step 3: Commit**

```bash
git add skills/plan/SKILL.md
git commit -m "feat(plan): add conditional TDD — applicability criteria and non-TDD step structure (#27)"
```

---

### Task 4: Modify skills/implement/SKILL.md [No TDD — modifying skill documentation]

**Files:**
- Modify: `skills/implement/SKILL.md:103-105`

- [ ] **Step 1: Implement**

Replace in `skills/implement/SKILL.md`:

```
## Notes

- Never start implementation on main/master without explicit user consent
```

With:

```
## Notes

- Never start implementation on main/master without explicit user consent
- For tasks marked `[TDD]`, follow the Red-Green-Refactor cycle from `hexis:testing-principles`. The failing test must be seen to fail before writing implementation code.
```

- [ ] **Step 2: Verify**

```bash
tail -5 skills/implement/SKILL.md
```

Expected: last lines include the testing-principles reference.

- [ ] **Step 3: Commit**

```bash
git add skills/implement/SKILL.md
git commit -m "feat(implement): reference testing-principles for TDD task execution (#27)"
```

---

### Task 5: Modify agents/principles-reviewer.md [No TDD — modifying agent documentation]

**Files:**
- Modify: `agents/principles-reviewer.md`

Four edits:

**Edit A — frontmatter description**: Replace "official methods compliance" with "testing standards" to accurately reflect the actual five skills.

**Edit B — Scope list**: Add 5th item.

**Edit C — Before You Start list**: Add `hexis:testing-principles`.

**Edit D — Output Format example**: Add Testing section.

- [ ] **Step 1: Implement**

**Edit A:** Replace in `agents/principles-reviewer.md`:

```
description: Reviews code and process against all five hexis principle skills — core principles, HTTP API design, exception and logging, naming conventions, and official methods compliance.
```

With:

```
description: Reviews code and process against all five hexis principle skills — core principles, HTTP API design, exception and logging, naming conventions, and testing standards.
```

**Edit B:** Replace:

```
4. **Naming conventions** (`hexis:general-naming-principles`) — variables, functions, classes, constants, files, packages

Core principles lead because process-level violations can invalidate how the other four areas are applied.
```

With:

```
4. **Naming conventions** (`hexis:general-naming-principles`) — variables, functions, classes, constants, files, packages
5. **Testing** (`hexis:testing-principles`) — TDD applicability in plans, Iron Law compliance, mock usage, test naming, coverage approach

Core principles lead because process-level violations can invalidate how the other four areas are applied.
```

**Edit C:** Replace:

```
Read all five principle skills in full before reviewing any code:
- `hexis:core-principles`
- `hexis:http-api-principles`
- `hexis:exception-and-logging-principles`
- `hexis:general-naming-principles`
```

With:

```
Read all five principle skills in full before reviewing any code:
- `hexis:core-principles`
- `hexis:http-api-principles`
- `hexis:exception-and-logging-principles`
- `hexis:general-naming-principles`
- `hexis:testing-principles`
```

**Edit D:** In the Output Format example block, after the Naming Conventions section, append a Testing section. Replace:

```
## Naming Conventions

No violations found.
```

With:

```
## Naming Conventions

No violations found.

---

## Testing

### Violations
[testing.iron-law] — task writes production code with no preceding test step and no `[No TDD]` label → add `[TDD]` label and failing test step, or justify skip with `[No TDD — <reason>]`

### Passed
- All TDD tasks include failing-test confirmation step
```

- [ ] **Step 2: Verify**

```bash
grep -n "testing-principles\|Testing\|No TDD" agents/principles-reviewer.md
```

Expected: lines containing "testing-principles" in Scope and Before You Start, "Testing" as a section header, and the violation example present.

- [ ] **Step 3: Commit**

```bash
git add agents/principles-reviewer.md
git commit -m "feat(principles-reviewer): add testing-principles as 5th review area (#27)"
```

---

### Task 6: Verify no remaining write-test references [No TDD — verification only]

**Files:** read-only scan

- [ ] **Step 1: Implement**

```bash
grep -r "write-test\|hexis:write-test" . --include="*.md" --exclude-dir=".git" --exclude-dir="docs/specs" --exclude-dir="docs/plans"
```

- [ ] **Step 2: Verify**

Expected: no output. If any matches appear, open each file and remove the reference.

- [ ] **Step 3: Commit**

If any files were cleaned up:
```bash
git add <affected files>
git commit -m "chore: remove remaining write-test references (#27)"
```

If no files needed cleanup: no commit required.
