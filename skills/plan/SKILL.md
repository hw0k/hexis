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

If `$ARGUMENTS` is a file path, read that spec and start. Otherwise use the **ask-user** capability to ask for the spec path (see `hexis:platform-capabilities`).

## Task Tracking

### On Start

Use the **track-tasks** capability filtered by prefix `plan:`. If open tasks exist from a prior session:
- Use the **ask-user** capability: **Resume** (verify state of last open task, continue from it) or **Start fresh** (stop all open tasks, then proceed from Scope Check)
- If no open tasks: proceed directly

> **Fallbacks:** If **track-tasks** is unavailable, maintain a markdown checklist in the current response. If **ask-user** is unavailable, output the question inline and wait for the next message.

### Step Schedule

| Step | On Start | On Done |
|---|---|---|
| Scope Check | **track-tasks**: create "plan: scope check" → mark in_progress | mark completed |
| File Structure | **track-tasks**: create "plan: define file structure" → mark in_progress | mark completed |
| Task Writing | **track-tasks**: create "plan: write tasks" → mark in_progress | mark completed |
| Self-Review | **track-tasks**: create "plan: self-review" → mark in_progress | mark completed |
| Save and Commit | **track-tasks**: create "plan: save and commit" → mark in_progress | mark completed |

### On Failure or Abort

Use **track-tasks** to stop the current open task.

## Scope Check

After loading the spec, check whether the work can be split:
- Can each unit be developed with no shared in-progress state (no cross-unit file conflicts)?
- Can each unit be reviewed and merged independently?

If **both** conditions hold for N ≥ 2 units: propose decomposition to the user using the **ask-user** capability. Do not proceed until confirmed.

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
