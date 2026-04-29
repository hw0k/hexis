---
issue: 32
status: READY_TO_IMPLEMENT
linked_spec: docs/specs/2026-04-29-remove-platform-capabilities-design.md
---

# Remove Platform-Capabilities Abstraction — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Delete the `platform-capabilities` skill and remove all capability-name references from every hexis skill file, replacing them with plain natural language.

**Architecture:** Pure text editing across 10 markdown files. No code logic, no tests. All 8 tasks are independent with no cross-file dependencies — dispatch in parallel. Task 1 deletes the skill directory; Tasks 2–8 edit the skills that referenced it.

**Tech Stack:** Markdown only

---

## File Structure

| Action | Path |
|---|---|
| Delete | `skills/platform-capabilities/` (entire directory) |
| Modify | `skills/specify/SKILL.md` |
| Modify | `skills/plan/SKILL.md` |
| Modify | `skills/implement/SKILL.md` |
| Modify | `skills/verify/SKILL.md` |
| Modify | `skills/review/SKILL.md` |
| Modify | `skills/finish/SKILL.md` |
| Modify | `skills/dispatch/SKILL.md` |
| Modify | `skills/use-worktree/SKILL.md` |
| Modify | `skills/receive-review/SKILL.md` |

---

### Task 1: Delete platform-capabilities skill [No TDD — deleting a directory]

**Files:**
- Delete: `skills/platform-capabilities/`

- [ ] **Step 1: Implement**

```bash
git rm -rf skills/platform-capabilities/
```

- [ ] **Step 2: Verify**

Run: `ls skills/platform-capabilities/ 2>&1`
Expected: `ls: skills/platform-capabilities/: No such file or directory`

- [ ] **Step 3: Commit**

```bash
git commit -m "refactor(skills): delete platform-capabilities skill (#32)"
```

---

### Task 2: Update skills/specify/SKILL.md [No TDD — markdown]

**Files:**
- Modify: `skills/specify/SKILL.md`

- [ ] **Step 1: Implement**

**Edit 1** — `$ARGUMENTS` section. Replace:
```
Otherwise use the **ask-user** capability to ask what needs to be specified (see `hexis:platform-capabilities`).
```
With:
```
Otherwise ask the user what needs to be specified.
```

**Edit 2** — Checklist. Replace:
```
- [ ] Ask clarifying questions (AskUserQuestion)
```
With:
```
- [ ] Ask clarifying questions
```

**Edit 3** — Remove entire Task Tracking section. Delete:
```
## Task Tracking

### On Start

Use the **track-tasks** capability filtered by prefix `specify:`. If open tasks exist from a prior session:
- Use the **ask-user** capability: **Resume** (verify state of last open task, continue from it) or **Start fresh** (stop all open tasks, then proceed from Step 1)
- If no open tasks: proceed directly

> **Fallbacks:** If **track-tasks** is unavailable, maintain a markdown checklist in the current response. If **ask-user** is unavailable, output the question inline and wait for the next message.

### Step Schedule

| Step | On Start | On Done |
|---|---|---|
| Step 1: Identify Ambiguities | **track-tasks**: create "specify: identify ambiguities" → mark in_progress | mark completed |
| Step 2: Ask Clarifying Questions | **track-tasks**: create "specify: ask clarifying questions" → mark in_progress | mark completed |
| Step 3: Draft | **track-tasks**: create "specify: draft spec" → mark in_progress | mark completed |
| Step 4: Write and Commit | **track-tasks**: create "specify: write and commit spec" → mark in_progress | mark completed |
| Step 5: Hand Off | **track-tasks**: create "specify: hand off to plan" → mark in_progress | mark completed |

### On Failure or Abort

Use **track-tasks** to stop the current open task. Do not leave any task in an unresolved state.
```

**Edit 4** — Decomposition bullet. Replace:
```
1. Propose the N units to the user using the **ask-user** capability. Do not proceed until confirmed.
```
With:
```
1. Propose the N units to the user. Do not proceed until confirmed.
```

**Edit 5** — Step 2 opener. Replace:
```
Use the **ask-user** capability. Group related ambiguities into a single request when possible.
```
With:
```
Ask the user. Group related ambiguities into a single request when possible.
```

**Edit 6** — Rules section. Replace:
```
- If the user requests to skip writing the spec file: use the **ask-user** capability to confirm. Only proceed without a spec file with explicit user confirmation, and note the skip explicitly.
```
With:
```
- If the user requests to skip writing the spec file: ask the user to confirm. Only proceed without a spec file with explicit user confirmation, and note the skip explicitly.
```

- [ ] **Step 2: Verify**

Run: `grep -n "ask-user\|track-tasks\|platform-capabilities\|AskUserQuestion" skills/specify/SKILL.md`
Expected: no output

- [ ] **Step 3: Commit**

```bash
git add skills/specify/SKILL.md
git commit -m "refactor(specify): remove platform-capabilities abstraction (#32)"
```

---

### Task 3: Update skills/plan/SKILL.md [No TDD — markdown]

**Files:**
- Modify: `skills/plan/SKILL.md`

- [ ] **Step 1: Implement**

**Edit 1** — `$ARGUMENTS` section. Replace:
```
Otherwise use the **ask-user** capability to ask for the spec path (see `hexis:platform-capabilities`).
```
With:
```
Otherwise ask the user for the spec path.
```

**Edit 2** — Remove entire Task Tracking section. Delete:
```
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
```

**Edit 3** — Scope Check section. Replace:
```
If **both** conditions hold for N ≥ 2 units: propose decomposition to the user using the **ask-user** capability. Do not proceed until confirmed.
```
With:
```
If **both** conditions hold for N ≥ 2 units: propose decomposition to the user. Do not proceed until confirmed.
```

- [ ] **Step 2: Verify**

Run: `grep -n "ask-user\|track-tasks\|platform-capabilities" skills/plan/SKILL.md`
Expected: no output

- [ ] **Step 3: Commit**

```bash
git add skills/plan/SKILL.md
git commit -m "refactor(plan): remove platform-capabilities abstraction (#32)"
```

---

### Task 4: Update skills/implement/SKILL.md [No TDD — markdown]

**Files:**
- Modify: `skills/implement/SKILL.md`

- [ ] **Step 1: Implement**

**Edit 1** — `$ARGUMENTS` section. Replace:
```
Otherwise use the **ask-user** capability to ask for the path (see `hexis:platform-capabilities`).
```
With:
```
Otherwise ask the user for the plan file path.
```

**Edit 2** — Complexity Check. Replace:
```
**Complex task** → use the **plan-mode** capability. Review the plan, clarify execution strategy, get approval before writing any code (see `hexis:platform-capabilities`).
```
With:
```
**Complex task** → present a plan and get user approval before writing any code.
```

**Edit 3** — Remove entire Task Tracking section. Delete:
```
## Task Tracking

### On Start

1. Use the **track-tasks** capability filtered by prefix `implement:`. If open tasks exist from a prior session:
   - Use the **ask-user** capability: **Resume** (verify state of last open task) or **Start fresh** (stop all open tasks)
2. **track-tasks**: create "implement: execute plan <plan-filename>" → mark in_progress (parent task — created regardless of subagent or inline path)

> **Fallbacks:** If **track-tasks** is unavailable, maintain a markdown checklist in the current response. If **ask-user** is unavailable, output the question inline and wait for the next message.

### Subagent Path

Before dispatching each subagent:
- Use **track-tasks** filtered by prefix `implement/task-`. Confirm the prior task (if any) shows completed before dispatching the next.
- Instruct each dispatched subagent to use **track-tasks**: create "implement/task-N: <task-name>" → mark in_progress at start; mark completed on success; stop on failure. Use `N` and task name from the plan.
- After reviewing each subagent's output: update the parent task with a progress note.

### Inline Path

**track-tasks**: create task before the existing update in Step 4 (see below).

### On All Tasks Complete

Use **track-tasks** to mark the parent task completed.

### On Failure or Abort

Use **track-tasks** to stop the current open task and the parent task.
```

**Edit 4** — Step 0: Branch Check. Replace:
```
Check the current branch. If it is `main` or `master`, use the **ask-user** capability to ask the user whether to proceed on this branch or switch to a feature branch. Do not proceed until the user explicitly confirms. This check is mandatory even if the user invoked the skill directly.
```
With:
```
Check the current branch. If it is `main` or `master`, ask the user whether to proceed on this branch or switch to a feature branch. Do not proceed until the user explicitly confirms. This check is mandatory even if the user invoked the skill directly.
```

**Edit 5** — Step 3: Subagent Path opener. Replace:
```
Use the **spawn-subagent** capability for each task (see `hexis:platform-capabilities`). If **spawn-subagent** is unavailable, use the Inline Path instead.
```
With:
```
Dispatch a subagent for each task.
```

**Edit 6** — Step 4: Inline Path enumerated steps. Replace:
```
For each task:
1. TaskCreate("implement/task-N: <task-name>") → TaskUpdate(in_progress)
2. Follow each step exactly as written
3. Run verifications as specified
4. TaskUpdate(completed)
5. Stop if blocked — report and wait
```
With:
```
For each task:
1. Follow each step exactly as written
2. Run verifications as specified
3. Stop if blocked — report and wait
```

- [ ] **Step 2: Verify**

Run: `grep -n "ask-user\|track-tasks\|spawn-subagent\|plan-mode\|platform-capabilities\|TaskCreate\|TaskUpdate" skills/implement/SKILL.md`
Expected: no output

- [ ] **Step 3: Commit**

```bash
git add skills/implement/SKILL.md
git commit -m "refactor(implement): remove platform-capabilities abstraction (#32)"
```

---

### Task 5: Update skills/verify/SKILL.md [No TDD — markdown]

**Files:**
- Modify: `skills/verify/SKILL.md`

- [ ] **Step 1: Implement**

**Edit 1** — Complexity Check. Replace:
```
**Complex scope** → use the **plan-mode** capability. Define verification commands and expected outputs, get approval before running anything (see `hexis:platform-capabilities`).
```
With:
```
**Complex scope** → present a verification plan and get user approval before running anything.
```

**Edit 2** — Remove entire Task Tracking section. Delete:
```
## Task Tracking

### On Start

Use the **track-tasks** capability filtered by prefix `verify:`. If open tasks exist from a prior session:
- Use the **ask-user** capability: **Resume** (verify state of last open task) or **Start fresh** (stop all open tasks)
- If no open tasks: proceed directly

> **Fallbacks:** If **track-tasks** is unavailable, maintain a markdown checklist in the current response. If **ask-user** is unavailable, output the question inline and wait for the next message.

### Step Schedule

| Check | On Start | On Done |
|---|---|---|
| Type check | **track-tasks**: create "verify: type check" → mark in_progress | mark completed |
| Lint | **track-tasks**: create "verify: lint" → mark in_progress | mark completed |
| Tests | **track-tasks**: create "verify: tests" → mark in_progress | mark completed |

Only create a task for checks that are applicable. Skip a task entirely if the check is declared inapplicable.

When `verify` is invoked as a sub-step by another skill (`review`, `finish`), it manages its own tasks independently — no coordination with the calling skill needed.

### On Failure or Abort

Use **track-tasks** to stop the current open task.
```

- [ ] **Step 2: Verify**

Run: `grep -n "ask-user\|track-tasks\|plan-mode\|platform-capabilities" skills/verify/SKILL.md`
Expected: no output

- [ ] **Step 3: Commit**

```bash
git add skills/verify/SKILL.md
git commit -m "refactor(verify): remove platform-capabilities abstraction (#32)"
```

---

### Task 6: Update skills/review/SKILL.md [No TDD — markdown]

**Files:**
- Modify: `skills/review/SKILL.md`

- [ ] **Step 1: Implement**

**Edit 1** — Remove entire Task Tracking section. Delete:
```
## Task Tracking

### On Start

Use the **track-tasks** capability filtered by prefix `review:`. If open tasks exist from a prior session:
- Use the **ask-user** capability: **Resume** (verify state of last open task) or **Start fresh** (stop all open tasks)
- If no open tasks: proceed directly

> **Fallbacks:** If **track-tasks** is unavailable, maintain a markdown checklist in the current response. If **ask-user** is unavailable, output the question inline and wait for the next message.

### Step Schedule

Step 1 delegates to `hexis:verify`, which manages its own tasks. Steps 2–4:

| Step | On Start | On Done |
|---|---|---|
| Step 2: Collect git SHAs | **track-tasks**: create "review: collect git SHAs" → mark in_progress | mark completed |
| Step 3: Principles review | **track-tasks**: create "review: principles review" → mark in_progress | mark completed |
| Step 4: Handle results | **track-tasks**: create "review: handle results" → mark in_progress | mark completed |

### On Failure or Abort

Use **track-tasks** to stop the current open task.
```

**Edit 2** — Step 3: Run principles-reviewer. Replace:
```
Use the **spawn-subagent** capability to run the `hexis:principles-reviewer` agent (see `hexis:platform-capabilities`). If **spawn-subagent** is unavailable, run the principles review sequentially in the current context.
```
With:
```
Run the `hexis:principles-reviewer` agent.
```

- [ ] **Step 2: Verify**

Run: `grep -n "ask-user\|track-tasks\|spawn-subagent\|platform-capabilities" skills/review/SKILL.md`
Expected: no output

- [ ] **Step 3: Commit**

```bash
git add skills/review/SKILL.md
git commit -m "refactor(review): remove platform-capabilities abstraction (#32)"
```

---

### Task 7: Update skills/finish/SKILL.md [No TDD — markdown]

**Files:**
- Modify: `skills/finish/SKILL.md`

- [ ] **Step 1: Implement**

**Edit 1** — Remove entire Task Tracking section. Delete:
```
## Task Tracking

### On Start

Use the **track-tasks** capability filtered by prefix `finish:`. If open tasks exist from a prior session:
- Use the **ask-user** capability: **Resume** (verify state of last open task) or **Start fresh** (stop all open tasks)
- If no open tasks: proceed directly

> **Fallbacks:** If **track-tasks** is unavailable, maintain a markdown checklist in the current response. If **ask-user** is unavailable, output the question inline and wait for the next message.

### Step Schedule

Step 1 delegates to `hexis:verify`, which manages its own tasks. Steps 2–5:

| Step | On Start | On Done |
|---|---|---|
| Step 2: Handle uncommitted changes | **track-tasks**: create "finish: handle uncommitted changes" → mark in_progress | mark completed |
| Steps 3–4: Integration | **track-tasks**: create "finish: integration" → mark in_progress | mark completed |
| Step 5: Clean up worktree | **track-tasks**: create "finish: clean up worktree" → mark in_progress | mark completed |

### On Failure or Abort

Use **track-tasks** to stop the current open task.
```

**Edit 2** — Step 3: Present options opener. Replace:
```
Use the **ask-user** capability (see `hexis:platform-capabilities`):
```
With:
```
Ask the user:
```

- [ ] **Step 2: Verify**

Run: `grep -n "ask-user\|track-tasks\|platform-capabilities" skills/finish/SKILL.md`
Expected: no output

- [ ] **Step 3: Commit**

```bash
git add skills/finish/SKILL.md
git commit -m "refactor(finish): remove platform-capabilities abstraction (#32)"
```

---

### Task 8: Update dispatch, use-worktree, receive-review [No TDD — markdown, small edits batched]

**Files:**
- Modify: `skills/dispatch/SKILL.md`
- Modify: `skills/use-worktree/SKILL.md`
- Modify: `skills/receive-review/SKILL.md`

- [ ] **Step 1: Implement**

**dispatch — Edit 1** — ask-user reference. Replace:
```
Use the **ask-user** capability to ask: "What issue number are you working on? Enter the number, or 'none' if starting new work." (see `hexis:platform-capabilities`)
```
With:
```
Ask the user: "What issue number are you working on? Enter the number, or 'none' if starting new work."
```

**use-worktree — Edit 1** — Directory Selection → Ask the User section opener. Replace:
```
If neither of the above applies, use the **ask-user** capability (see `hexis:platform-capabilities`):
```
With:
```
If neither of the above applies, ask the user:
```

**use-worktree — Edit 2** — Red Flags / Always section. Replace:
```
- Use the **ask-user** capability for directory selection when no config exists
```
With:
```
- Ask the user for directory selection when no config exists
```

**receive-review — Edit 1** — Response Pattern step 2. Replace:
```
2. **Understand** — if anything is unclear, use the **ask-user** capability to clarify before implementing (see `hexis:platform-capabilities`)
```
With:
```
2. **Understand** — if anything is unclear, ask the user to clarify before implementing
```

**receive-review — Edit 2** — Handling Unclear Feedback. Replace:
```
Use the **ask-user** capability to ask about unclear items.
```
With:
```
Ask the user about unclear items.
```

- [ ] **Step 2: Verify**

Run: `grep -n "ask-user\|track-tasks\|platform-capabilities" skills/dispatch/SKILL.md skills/use-worktree/SKILL.md skills/receive-review/SKILL.md`
Expected: no output

- [ ] **Step 3: Commit**

```bash
git add skills/dispatch/SKILL.md skills/use-worktree/SKILL.md skills/receive-review/SKILL.md
git commit -m "refactor(skills): remove platform-capabilities from dispatch, use-worktree, receive-review (#32)"
```

---

## Final Verification

After all tasks complete, run across all modified files:

```bash
grep -r "\*\*ask-user\*\*\|\*\*track-tasks\*\*\|\*\*spawn-subagent\*\*\|\*\*plan-mode\*\*\|hexis:platform-capabilities\|TaskCreate\|TaskUpdate" skills/ --include="*.md"
```

Expected: no output.

---

## Self-Review

**Spec coverage:**
- Task 1: `platform-capabilities/` deleted ✓
- Tasks 2–7: Task Tracking sections removed from specify, plan, implement, verify, review, finish ✓
- Tasks 2–8: `**ask-user**` replaced in all 9 skill files ✓
- Task 4: `**plan-mode**` replaced in implement ✓
- Task 4: `**spawn-subagent**` replaced in implement ✓
- Task 4: `TaskCreate`/`TaskUpdate` removed from Inline Path ✓
- Task 5: `**plan-mode**` replaced in verify ✓
- Task 6: `**spawn-subagent**` replaced in review ✓
- Task 7: `**ask-user**` replaced in finish ✓
- `agents/principles-reviewer.md`: confirmed no platform-capabilities reference — no change needed ✓

**Placeholder scan:** No TBD or TODO in plan.

**Consistency:** All grep verify commands use consistent pattern. All commit messages follow `refactor(<scope>): remove platform-capabilities abstraction (#32)`.
