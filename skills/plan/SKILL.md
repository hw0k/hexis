---
name: plan
description: Use after specifying is complete — writes detailed implementation plan from a spec
type: workflow
---

# Plan

## Overview

Write a detailed implementation plan from a spec. Real code, exact file paths, no placeholders.

**Announce at start:** "I'm using the hexis:plan skill to create the implementation plan."

## $ARGUMENTS

If `$ARGUMENTS` is a file path, read that spec and start. Otherwise use `AskUserQuestion` to ask for the spec path.

## Task Tracking

### On Start

Call `TaskList` filtered by prefix `plan:`. If open Tasks exist from a prior session:
- Use `AskUserQuestion`: **Resume** (use `TaskGet` to verify state, continue from the last open Task) or **Start fresh** (call `TaskStop` on all open Tasks, then proceed from Scope Check)
- If no open Tasks: proceed directly

### Step Schedule

| Step | On Start | On Done |
|---|---|---|
| Scope Check | `TaskCreate("plan: scope check")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| File Structure | `TaskCreate("plan: define file structure")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Task Writing | `TaskCreate("plan: write tasks")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Self-Review | `TaskCreate("plan: self-review")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Save and Commit | `TaskCreate("plan: save and commit")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |

### On Failure or Abort

Call `TaskStop` on the current open Task.

## Scope Check

After loading the spec, check whether the work can be split:
- Can each unit be developed with no shared in-progress state (no cross-unit file conflicts)?
- Can each unit be reviewed and merged independently?

If **both** conditions hold for N ≥ 2 units: propose decomposition to the user via `AskUserQuestion`. Do not proceed until confirmed.

**On confirmed decomposition:**
1. Split the original Spec into N Spec files: `docs/specs/YYYY-MM-DD-<unit-name>-design.md`
2. Add superseded notice to original Spec: prepend `> **Superseded.** Decomposed into: [unit-a](path), [unit-b](path)`
3. Write N Plan files, each with `linked_spec` pointing to its new Spec

If no decomposition: single plan (continue below), with `linked_spec` pointing to the parent Spec.

## Plan Header (required)

Every plan must start with this header:

```markdown
---
linked_spec: docs/specs/YYYY-MM-DD-<topic>-design.md
---

# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence]

**Architecture:** [2–3 sentences on approach]

**Tech Stack:** [Key technologies]

---
```

## File Structure

Before defining tasks, list files to be created or modified. One responsibility per file.

**ultrathink** before decomposing tasks — never skip this.

## Task Size

Each task: one action, 2–5 minutes. Steps: write failing test → confirm failure → minimal implementation → confirm pass → commit.

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
