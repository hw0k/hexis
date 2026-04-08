---
linked_spec: docs/specs/2026-04-08-universal-task-tool-integration-design.md
---

# Universal Task Tool Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hw0k-workflow:implement` to execute task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `## Task Tracking` section to each of the 8 hw0k-workflow skills so that every named step is wrapped with `TaskCreate`/`TaskUpdate`/`TaskStop` calls, and every skill checks for interrupted work at startup.

**Architecture:** Pure markdown edits — no code. Each skill gets a `## Task Tracking` section inserted at the appropriate position, plus a targeted inline change to `implement`'s Step 4. All changes are independent; each skill is its own commit.

**Tech Stack:** Markdown (SKILL.md), bash (grep for verification)

Issue: #15

---

## Files

| Action | Path |
|--------|------|
| Modify | `skills/specify/SKILL.md` |
| Modify | `skills/plan/SKILL.md` |
| Modify | `skills/implement/SKILL.md` |
| Modify | `skills/write-test/SKILL.md` |
| Modify | `skills/debug/SKILL.md` |
| Modify | `skills/verify/SKILL.md` |
| Modify | `skills/review/SKILL.md` |
| Modify | `skills/finish/SKILL.md` |

---

### Task 1: specify — add Task Tracking section

**Files:**
- Modify: `skills/specify/SKILL.md` (insert `## Task Tracking` after `## Checklist`, before `## Process`)

- [ ] **Step 1: Confirm section does not yet exist**

```bash
grep -c "Task Tracking" skills/specify/SKILL.md
```

Expected: `0`

- [ ] **Step 2: Insert `## Task Tracking` section**

In `skills/specify/SKILL.md`, insert the following block between `## Checklist` and `## Process`:

```markdown
## Task Tracking

### On Start

Call `TaskList` filtered by prefix `specify:`. If open Tasks exist from a prior session:
- Use `AskUserQuestion`: **Resume** (use `TaskGet` to verify state, continue from the last open Task) or **Start fresh** (call `TaskStop` on all open Tasks, then proceed from Step 1)
- If no open Tasks: proceed directly

### Step Schedule

| Step | On Start | On Done |
|---|---|---|
| Step 1: Identify Ambiguities | `TaskCreate("specify: identify ambiguities")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Step 2: Ask Clarifying Questions | `TaskCreate("specify: ask clarifying questions")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Step 3: Draft | `TaskCreate("specify: draft spec")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Step 4: Write and Commit | `TaskCreate("specify: write and commit spec")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Step 5: Hand Off | `TaskCreate("specify: hand off to plan")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |

### On Failure or Abort

Call `TaskStop` on the current open Task. Do not leave any Task in an unresolved state.
```

- [ ] **Step 3: Confirm section exists**

```bash
grep -c "Task Tracking" skills/specify/SKILL.md
```

Expected: `1`

```bash
grep -c "specify: identify ambiguities" skills/specify/SKILL.md
```

Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add skills/specify/SKILL.md
git commit -m "feat(specify): add Task tool integration (#15)"
```

---

### Task 2: plan — add Task Tracking section

**Files:**
- Modify: `skills/plan/SKILL.md` (insert `## Task Tracking` after `## $ARGUMENTS`, before `## Scope Check`)

- [ ] **Step 1: Confirm section does not yet exist**

```bash
grep -c "Task Tracking" skills/plan/SKILL.md
```

Expected: `0`

- [ ] **Step 2: Insert `## Task Tracking` section**

In `skills/plan/SKILL.md`, insert the following block between the `## $ARGUMENTS` section and `## Scope Check`:

```markdown
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
```

- [ ] **Step 3: Confirm section exists**

```bash
grep -c "Task Tracking" skills/plan/SKILL.md
```

Expected: `1`

```bash
grep -c "plan: scope check" skills/plan/SKILL.md
```

Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add skills/plan/SKILL.md
git commit -m "feat(plan): add Task tool integration (#15)"
```

---

### Task 3: implement — add Task Tracking section and fix inline path

**Files:**
- Modify: `skills/implement/SKILL.md` (two changes: insert `## Task Tracking` after `## Complexity Check`, before `## Process`; update Step 4 inline path to use `TaskCreate`)

- [ ] **Step 1: Confirm section does not yet exist**

```bash
grep -c "Task Tracking" skills/implement/SKILL.md
```

Expected: `0`

- [ ] **Step 2: Insert `## Task Tracking` section**

In `skills/implement/SKILL.md`, insert the following block between `## Complexity Check` and `## Process`:

```markdown
## Task Tracking

### On Start

1. Call `TaskList` filtered by prefix `implement:`. If open Tasks exist from a prior session:
   - Use `AskUserQuestion`: **Resume** (use `TaskGet` to verify state) or **Start fresh** (call `TaskStop` on all open Tasks)
2. `TaskCreate("implement: execute plan <plan-filename>")` → `TaskUpdate(in_progress)` (parent Task — created whether subagent or inline path)

### Subagent Path

Before dispatching each subagent:
- Call `TaskList` filtered by prefix `implement/task-`. Confirm the prior task (if any) shows `completed` before dispatching the next.
- Instruct each dispatched subagent to: `TaskCreate("implement/task-N: <task-name>")` → `TaskUpdate(in_progress)` at start; `TaskUpdate(completed)` on success; `TaskStop` on failure. Use `N` and task name from the plan.
- After reviewing each subagent's output: `TaskUpdate(in_progress)` on the parent Task with a progress note.

### Inline Path

`TaskCreate` is added before the existing `TaskUpdate` in Step 4 (see below).

### On All Tasks Complete

`TaskUpdate(completed)` on the parent Task.

### On Failure or Abort

`TaskStop` on the current open task. `TaskStop` on the parent Task.
```

- [ ] **Step 3: Update Step 4 inline path to use `TaskCreate`**

In `skills/implement/SKILL.md`, locate `### Step 4: Inline Path (exception only)` and update the numbered list from:

```markdown
For each task:
1. TaskUpdate: mark in_progress
2. Follow each step exactly as written
3. Run verifications as specified
4. TaskUpdate: mark completed
5. Stop if blocked — report and wait
```

To:

```markdown
For each task:
1. TaskCreate("implement/task-N: <task-name>") → TaskUpdate(in_progress)
2. Follow each step exactly as written
3. Run verifications as specified
4. TaskUpdate(completed)
5. Stop if blocked — report and wait
```

- [ ] **Step 4: Confirm both changes exist**

```bash
grep -c "Task Tracking" skills/implement/SKILL.md
```

Expected: `1`

```bash
grep -c "implement/task-N" skills/implement/SKILL.md
```

Expected: `2` (once in Task Tracking, once in Step 4)

```bash
grep -c "TaskCreate" skills/implement/SKILL.md
```

Expected: `2` or more

- [ ] **Step 5: Commit**

```bash
git add skills/implement/SKILL.md
git commit -m "feat(implement): add Task tool integration with parent-child hierarchy (#15)"
```

---

### Task 4: write-test — add Task Tracking section

**Files:**
- Modify: `skills/write-test/SKILL.md` (insert `## Task Tracking` after `## Complexity Check`, before `## The Iron Law`)

- [ ] **Step 1: Confirm section does not yet exist**

```bash
grep -c "Task Tracking" skills/write-test/SKILL.md
```

Expected: `0`

- [ ] **Step 2: Insert `## Task Tracking` section**

In `skills/write-test/SKILL.md`, insert the following block between `## Complexity Check` and `## The Iron Law`:

```markdown
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
```

- [ ] **Step 3: Confirm section exists**

```bash
grep -c "Task Tracking" skills/write-test/SKILL.md
```

Expected: `1`

```bash
grep -c "write-test: red phase" skills/write-test/SKILL.md
```

Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add skills/write-test/SKILL.md
git commit -m "feat(write-test): add Task tool integration (#15)"
```

---

### Task 5: debug — add Task Tracking section

**Files:**
- Modify: `skills/debug/SKILL.md` (insert `## Task Tracking` after `## $ARGUMENTS`, before `## The Iron Law`)

- [ ] **Step 1: Confirm section does not yet exist**

```bash
grep -c "Task Tracking" skills/debug/SKILL.md
```

Expected: `0`

- [ ] **Step 2: Insert `## Task Tracking` section**

In `skills/debug/SKILL.md`, insert the following block between `## $ARGUMENTS` and `## The Iron Law`:

```markdown
## Task Tracking

### On Start

Call `TaskList` filtered by prefix `debug:`. If open Tasks exist from a prior session:
- Use `AskUserQuestion`: **Resume** (use `TaskGet` to verify state, continue from the last open phase) or **Start fresh** (call `TaskStop` on all open Tasks)
- If no open Tasks: proceed directly

### Step Schedule

| Phase | On Start | On Done |
|---|---|---|
| Phase 1: Root Cause Investigation | `TaskCreate("debug: root cause investigation")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Phase 2: Pattern Analysis | `TaskCreate("debug: pattern analysis")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Phase 3: Hypotheses and Verification | `TaskCreate("debug: hypotheses and verification")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Phase 4: Implementation | `TaskCreate("debug: fix implementation")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |

### On Failure or Abort

Call `TaskStop` on the current open Task.
```

- [ ] **Step 3: Confirm section exists**

```bash
grep -c "Task Tracking" skills/debug/SKILL.md
```

Expected: `1`

```bash
grep -c "debug: root cause investigation" skills/debug/SKILL.md
```

Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add skills/debug/SKILL.md
git commit -m "feat(debug): add Task tool integration (#15)"
```

---

### Task 6: verify — add Task Tracking section

**Files:**
- Modify: `skills/verify/SKILL.md` (insert `## Task Tracking` after `## Complexity Check`, before `## The Iron Law`)

- [ ] **Step 1: Confirm section does not yet exist**

```bash
grep -c "Task Tracking" skills/verify/SKILL.md
```

Expected: `0`

- [ ] **Step 2: Insert `## Task Tracking` section**

In `skills/verify/SKILL.md`, insert the following block between `## Complexity Check` and `## The Iron Law`:

```markdown
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

Only create a Task for checks that are applicable (skip a Task entirely if the check is not applicable, as declared in the skill's "no static validator" declaration).

When `verify` is invoked as a sub-step by another skill (`review`, `finish`), it manages its own Tasks independently — no coordination with the calling skill needed.

### On Failure or Abort

Call `TaskStop` on the current open Task.
```

- [ ] **Step 3: Confirm section exists**

```bash
grep -c "Task Tracking" skills/verify/SKILL.md
```

Expected: `1`

```bash
grep -c "verify: type check" skills/verify/SKILL.md
```

Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add skills/verify/SKILL.md
git commit -m "feat(verify): add Task tool integration (#15)"
```

---

### Task 7: review — add Task Tracking section

**Files:**
- Modify: `skills/review/SKILL.md` (insert `## Task Tracking` after `## $ARGUMENTS`, before `## When to Review`)

- [ ] **Step 1: Confirm section does not yet exist**

```bash
grep -c "Task Tracking" skills/review/SKILL.md
```

Expected: `0`

- [ ] **Step 2: Insert `## Task Tracking` section**

In `skills/review/SKILL.md`, insert the following block between `## $ARGUMENTS` and `## When to Review`:

```markdown
## Task Tracking

### On Start

Call `TaskList` filtered by prefix `review:`. If open Tasks exist from a prior session:
- Use `AskUserQuestion`: **Resume** (use `TaskGet` to verify state) or **Start fresh** (call `TaskStop` on all open Tasks)
- If no open Tasks: proceed directly

### Step Schedule

Step 1 delegates to `hw0k-workflow:verify`, which manages its own Tasks. Steps 2–4:

| Step | On Start | On Done |
|---|---|---|
| Step 2: Collect git SHAs | `TaskCreate("review: collect git SHAs")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Step 3: Principles review | `TaskCreate("review: principles review")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Step 4: Handle results | `TaskCreate("review: handle results")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |

### On Failure or Abort

Call `TaskStop` on the current open Task.
```

- [ ] **Step 3: Confirm section exists**

```bash
grep -c "Task Tracking" skills/review/SKILL.md
```

Expected: `1`

```bash
grep -c "review: collect git SHAs" skills/review/SKILL.md
```

Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add skills/review/SKILL.md
git commit -m "feat(review): add Task tool integration (#15)"
```

---

### Task 8: finish — add Task Tracking section

**Files:**
- Modify: `skills/finish/SKILL.md` (insert `## Task Tracking` after `## $ARGUMENTS`, before `## Process`)

- [ ] **Step 1: Confirm section does not yet exist**

```bash
grep -c "Task Tracking" skills/finish/SKILL.md
```

Expected: `0`

- [ ] **Step 2: Insert `## Task Tracking` section**

In `skills/finish/SKILL.md`, insert the following block between `## $ARGUMENTS` and `## Process`:

```markdown
## Task Tracking

### On Start

Call `TaskList` filtered by prefix `finish:`. If open Tasks exist from a prior session:
- Use `AskUserQuestion`: **Resume** (use `TaskGet` to verify state) or **Start fresh** (call `TaskStop` on all open Tasks)
- If no open Tasks: proceed directly

### Step Schedule

Step 1 delegates to `hw0k-workflow:verify`, which manages its own Tasks. Steps 2–5:

| Step | On Start | On Done |
|---|---|---|
| Step 2: Handle uncommitted changes | `TaskCreate("finish: handle uncommitted changes")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Steps 3–4: Integration | `TaskCreate("finish: integration")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Step 5: Clean up worktree | `TaskCreate("finish: clean up worktree")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |

### On Failure or Abort

Call `TaskStop` on the current open Task.
```

- [ ] **Step 3: Confirm section exists**

```bash
grep -c "Task Tracking" skills/finish/SKILL.md
```

Expected: `1`

```bash
grep -c "finish: handle uncommitted changes" skills/finish/SKILL.md
```

Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add skills/finish/SKILL.md
git commit -m "feat(finish): add Task tool integration (#15)"
```

---

## Self-Review

**Spec coverage:**
- ✅ All 8 skills covered (specify, plan, implement, write-test, debug, verify, review, finish)
- ✅ Resume behavior (TaskList → AskUserQuestion → resume or fresh start) in every skill
- ✅ TaskCreate + TaskUpdate(in_progress/completed) per named step
- ✅ TaskStop on failure/abort in every skill
- ✅ implement parent Task + subagent child Task hierarchy
- ✅ TaskList check before dispatching next subagent in implement
- ✅ verify/finish: no duplicate Task for delegated verify step

**Placeholder scan:** No TBD or TODO remaining.

**Consistency:** Task names follow `<skill>: <step-name>` and `implement/task-N: <task-name>` conventions consistently across all tasks.
