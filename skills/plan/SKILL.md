---
name: plan
description: Use after specifying is complete — writes detailed implementation plan from a spec
type: workflow
---

# Plan

## Overview

Write a detailed implementation plan from a spec. Real code, exact file paths, no placeholders.

## $ARGUMENTS

If `$ARGUMENTS` is a file path, read that spec and start. Otherwise ask the user for the spec path.

## Scope Check

After loading the spec, check whether the work can be split:
- Can each unit be developed with no shared in-progress state (no cross-unit file conflicts)?
- Can each unit be reviewed and merged independently?

If **both** conditions hold for N ≥ 2 units: propose decomposition to the user. Do not proceed until confirmed.

**On confirmed decomposition:**
1. Split the original Spec into N Spec files: `docs/specs/YYYY-MM-DD-<unit-name>-design.md`
2. Add superseded notice to original Spec: prepend `> **Superseded.** Decomposed into: [unit-a](path), [unit-b](path)`
3. Write N Plan files, each with `linked_spec` pointing to its new Spec

If no decomposition: single plan (continue below), with `linked_spec` pointing to the parent Spec.

## Plan Header (required)

Every plan must start with this header:

```markdown
---
issue: N
status: READY_TO_IMPLEMENT
linked_spec: docs/specs/YYYY-MM-DD-<topic>-design.md
---

# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. For TDD tasks, follow `hexis:testing-principles`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence]

**Architecture:** [2–3 sentences on approach]

**Tech Stack:** [Key technologies]

---
```

## File Structure

Before defining tasks, list files to be created or modified. One responsibility per file.

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

## Step Structure

````markdown
### Task N: [Name]

**Files:**
- Create: `exact/path/to/file.ts`
- Modify: `exact/path/to/existing.ts:123-145`

- [ ] **Step 1: Write failing test**

```typescript
test('specific behavior', () => {
  const result = fn(input)
  expect(result).toBe(expected)
})
```

- [ ] **Step 2: Confirm failure**

Run: `<exact test command>`
Expected: FAIL — "function not defined"

- [ ] **Step 3: Minimal implementation**

```typescript
function fn(input) {
  return expected
}
```

- [ ] **Step 4: Confirm pass**

Run: `<exact test command>`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add <files>
git commit -m "feat: add specific feature"
```
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

## No Placeholders

Never write: TBD, TODO, "add appropriate error handling", "write tests for the above", "similar to Task N".

Every code step must contain actual code.

## Self-Review

After writing: spec coverage, placeholder scan, type/method name consistency.

## Save

`docs/plans/YYYY-MM-DD-<feature>.md`. Commit: `docs: add <feature> plan`.

## Execution Handoff

After saving:
> "Plan saved to `docs/plans/<filename>`. Run `hexis:implement` to execute."
