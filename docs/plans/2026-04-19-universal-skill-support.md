---
issue: 16
status: DONE
linked_spec: docs/specs/2026-04-19-universal-skill-support-design.md
---

# Universal Skill Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Make all hexis workflow skills platform-agnostic by replacing platform-specific tool references with capability names, backed by a new `platform-capabilities` reference skill.

**Architecture:** A new `platform-capabilities` reference skill defines a capability map (capability name → per-platform tool). All workflow skills are updated to reference capability names (e.g., **ask-user**, **track-tasks**) rather than Claude Code-specific tool names. Agents resolve capability names at runtime by consulting the map. Each skill update is a targeted find-and-replace of tool references plus a fallback note in the task-tracking section.

**Tech Stack:** Markdown (SKILL.md), git, pre-commit hooks (`uvx pre-commit run --files`)

---

## Files

**Create:**
- `skills/platform-capabilities/SKILL.md`
- `tests/pressure/universal-skill-support/README.md`
- `tests/pressure/universal-skill-support/evaluation-log.md`
- `tests/pressure/universal-skill-support/scenarios/001-specify-no-interactive-tools.md`
- `tests/pressure/universal-skill-support/scenarios/002-implement-no-subagent.md`

**Modify:**
- `skills/specify/SKILL.md`
- `skills/plan/SKILL.md`
- `skills/verify/SKILL.md`
- `skills/review/SKILL.md`
- `skills/receive-review/SKILL.md`
- `skills/implement/SKILL.md`
- `skills/use-worktree/SKILL.md`
- `skills/finish/SKILL.md`

**Audit only (no changes expected):**
- `skills/core-principles/SKILL.md`
- `skills/http-api-principles/SKILL.md`
- `skills/exception-and-logging-principles/SKILL.md`
- `skills/general-naming-principles/SKILL.md`
- `skills/commit-principles/SKILL.md`

---

### Task 1: Create `platform-capabilities` reference skill

**Files:**
- Create: `skills/platform-capabilities/SKILL.md`

- [x] **Step 1: Create the file**

```markdown
---
name: platform-capabilities
description: Platform capability map — resolves abstract capability names to concrete tools for Claude Code, Codex, and Opencode
type: reference
---

# Platform Capabilities

Hexis skills reference capabilities by name rather than by platform-specific tool names. Use this reference to resolve each capability name to the concrete tool or method available on your platform.

## Capability Map

| Capability | Claude Code | Codex | Opencode | Generic fallback |
|---|---|---|---|---|
| **ask-user** — pose a question and wait for input | TBD | TBD | TBD | Output question inline in response text; wait for next message |
| **track-tasks** — record and update step progress | TBD | TBD | TBD | Inline markdown checklist in current response |
| **spawn-subagent** — delegate work to a parallel agent | TBD | TBD | TBD | Execute sequentially in current context |
| **plan-mode** — present a plan and get approval before executing | TBD | TBD | TBD | Write plan inline as numbered list; use **ask-user** for approval |
| **worktree** — isolate work in a git worktree | TBD | TBD | TBD | `git worktree add .worktrees/<branch> -b <branch>` |
| **read-file** — read a file from the filesystem | TBD | TBD | TBD | Shell `cat` |
| **edit-file** — make targeted edits to a file | TBD | TBD | TBD | Shell-based file write |
| **run-shell** — execute shell commands | TBD | TBD | TBD | Platform shell equivalent |

TBD entries in named platform columns are filled as concrete equivalents are confirmed. The generic fallback is always available.

## How to Use

When a hexis skill references a capability name in bold (e.g., **ask-user**), find that row and use the tool or method for your current platform. If your platform is not listed or the capability is TBD, use the generic fallback.
```

- [x] **Step 2: Verify with pre-commit**

```bash
uvx pre-commit run --files skills/platform-capabilities/SKILL.md
```

Expected: lint Passed, format Passed, test Passed

- [x] **Step 3: Commit**

```bash
git add skills/platform-capabilities/SKILL.md
git commit -m "feat(skills): add platform-capabilities reference skill"
```

---

### Task 2: Audit Group 1 principles skills (confirm platform-agnostic)

**Files:**
- Read: `skills/core-principles/SKILL.md`, `skills/http-api-principles/SKILL.md`, `skills/exception-and-logging-principles/SKILL.md`, `skills/general-naming-principles/SKILL.md`, `skills/commit-principles/SKILL.md`

- [x] **Step 1: Grep for platform-specific tool names**

```bash
grep -n "AskUserQuestion\|TaskCreate\|TaskUpdate\|TaskList\|TaskStop\|TaskGet\|EnterPlanMode\|ExitPlanMode\|Agent tool" \
  skills/core-principles/SKILL.md \
  skills/http-api-principles/SKILL.md \
  skills/exception-and-logging-principles/SKILL.md \
  skills/general-naming-principles/SKILL.md \
  skills/commit-principles/SKILL.md
```

Expected: no matches (all 5 skills are pure reference text with no tool calls)

- [x] **Step 2: If any matches found, update and commit; if none, note as confirmed**

Expected outcome: No changes needed. All 5 principles skills confirmed platform-agnostic.

---

### Task 3: Update `specify/SKILL.md`

**Files:**
- Modify: `skills/specify/SKILL.md`

- [x] **Step 1: Replace `$ARGUMENTS` line's AskUserQuestion reference**

In the `## $ARGUMENTS` section, replace:

```markdown
use `AskUserQuestion` to ask what needs to be specified.
```

with:

```markdown
use the **ask-user** capability to ask what needs to be specified (see `hexis:platform-capabilities`).
```

- [x] **Step 2: Replace Task Tracking section**

Replace the entire `## Task Tracking` section with:

```markdown
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

- [x] **Step 3: Replace AskUserQuestion references in Process section**

In `### Step 1: Identify Ambiguities` → `**On decomposition:**` block:
- Replace `` `AskUserQuestion` `` with `the **ask-user** capability`

In `### Step 2: Ask Clarifying Questions`:

Replace:
```markdown
Use `AskUserQuestion`. Group related ambiguities into a single call when possible — the tool supports multiple questions at once.
```

with:

```markdown
Use the **ask-user** capability. Group related ambiguities into a single request when possible.
```

In `## Rules`:
- Replace `` `AskUserQuestion` `` with `the **ask-user** capability`

- [x] **Step 4: Verify with pre-commit**

```bash
uvx pre-commit run --files skills/specify/SKILL.md
```

Expected: lint Passed, format Passed, test Passed

- [x] **Step 5: Commit**

```bash
git add skills/specify/SKILL.md
git commit -m "refactor(skills): make specify skill platform-agnostic"
```

---

### Task 4: Update `plan/SKILL.md`

**Files:**
- Modify: `skills/plan/SKILL.md`

- [x] **Step 1: Replace `$ARGUMENTS` line's AskUserQuestion reference**

In the `## $ARGUMENTS` section, replace:

```markdown
use `AskUserQuestion` to ask for the spec path.
```

with:

```markdown
use the **ask-user** capability to ask for the spec path (see `hexis:platform-capabilities`).
```

- [x] **Step 2: Replace Task Tracking section**

Replace the entire `## Task Tracking` section with:

```markdown
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

- [x] **Step 3: Replace AskUserQuestion reference in Scope Check section**

In `## Scope Check`, replace:

```markdown
propose decomposition to the user via `AskUserQuestion`
```

with:

```markdown
propose decomposition to the user using the **ask-user** capability
```

- [x] **Step 4: Verify with pre-commit**

```bash
uvx pre-commit run --files skills/plan/SKILL.md
```

Expected: lint Passed, format Passed, test Passed

- [x] **Step 5: Commit**

```bash
git add skills/plan/SKILL.md
git commit -m "refactor(skills): make plan skill platform-agnostic"
```

---

### Task 5: Update `verify/SKILL.md`

**Files:**
- Modify: `skills/verify/SKILL.md`

- [x] **Step 1: Replace EnterPlanMode/ExitPlanMode with plan-mode capability**

In `## Complexity Check`, replace:

```markdown
**Complex scope** → call `EnterPlanMode`. Define verification commands and expected outputs, get user approval via `ExitPlanMode` before running anything.
```

with:

```markdown
**Complex scope** → use the **plan-mode** capability. Define verification commands and expected outputs, get approval before running anything (see `hexis:platform-capabilities`).
```

- [x] **Step 2: Replace Task Tracking section**

Replace the entire `## Task Tracking` section with:

```markdown
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

- [x] **Step 3: Verify with pre-commit**

```bash
uvx pre-commit run --files skills/verify/SKILL.md
```

Expected: lint Passed, format Passed, test Passed

- [x] **Step 4: Commit**

```bash
git add skills/verify/SKILL.md
git commit -m "refactor(skills): make verify skill platform-agnostic"
```

---

### Task 6: Update `review/SKILL.md`

**Files:**
- Modify: `skills/review/SKILL.md`

- [x] **Step 1: Replace Task Tracking section**

Replace the entire `## Task Tracking` section with:

```markdown
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

- [x] **Step 2: Update Step 3 to reference spawn-subagent capability**

In `### Step 3: Run principles-reviewer`, replace:

```markdown
Run the `hexis:principles-reviewer` agent:
- Changed files: `git diff --name-only $BASE_SHA $HEAD_SHA`
- Scope: the implementation delivered
```

with:

```markdown
Use the **spawn-subagent** capability to run the `hexis:principles-reviewer` agent (see `hexis:platform-capabilities`). If **spawn-subagent** is unavailable, run the principles review sequentially in the current context.
- Changed files: `git diff --name-only $BASE_SHA $HEAD_SHA`
- Scope: the implementation delivered
```

- [x] **Step 3: Verify with pre-commit**

```bash
uvx pre-commit run --files skills/review/SKILL.md
```

Expected: lint Passed, format Passed, test Passed

- [x] **Step 4: Commit**

```bash
git add skills/review/SKILL.md
git commit -m "refactor(skills): make review skill platform-agnostic"
```

---

### Task 7: Update `receive-review/SKILL.md`

**Files:**
- Modify: `skills/receive-review/SKILL.md`

- [x] **Step 1: Replace AskUserQuestion references**

In `## Response Pattern`, replace:

```markdown
2. **Understand** — if anything is unclear, use `AskUserQuestion` to clarify before implementing
```

with:

```markdown
2. **Understand** — if anything is unclear, use the **ask-user** capability to clarify before implementing (see `hexis:platform-capabilities`)
```

In `## Handling Unclear Feedback`, replace:

```markdown
Use `AskUserQuestion` to ask about unclear items.
```

with:

```markdown
Use the **ask-user** capability to ask about unclear items.
```

- [x] **Step 2: Verify with pre-commit**

```bash
uvx pre-commit run --files skills/receive-review/SKILL.md
```

Expected: lint Passed, format Passed, test Passed

- [x] **Step 3: Commit**

```bash
git add skills/receive-review/SKILL.md
git commit -m "refactor(skills): make receive-review skill platform-agnostic"
```

---

### Task 8: Update `implement/SKILL.md`

**Files:**
- Modify: `skills/implement/SKILL.md`

- [x] **Step 1: Replace `$ARGUMENTS` AskUserQuestion reference**

In `## $ARGUMENTS`, replace:

```markdown
use `AskUserQuestion` to ask for the path.
```

with:

```markdown
use the **ask-user** capability to ask for the path (see `hexis:platform-capabilities`).
```

- [x] **Step 2: Replace EnterPlanMode/ExitPlanMode with plan-mode capability**

In `## Complexity Check`, replace:

```markdown
**Complex task** → call `EnterPlanMode`. Review the plan, clarify execution strategy, get user approval via `ExitPlanMode` before writing any code.
```

with:

```markdown
**Complex task** → use the **plan-mode** capability. Review the plan, clarify execution strategy, get approval before writing any code (see `hexis:platform-capabilities`).
```

- [x] **Step 3: Replace Task Tracking section**

Replace the entire `## Task Tracking` section with:

```markdown
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

- [x] **Step 4: Update Step 3 (Subagent Path) to reference spawn-subagent**

In `### Step 3: Subagent Path`, replace:

```markdown
Dispatch a subagent for each task. Review between tasks before dispatching the next.
```

with:

```markdown
Use the **spawn-subagent** capability for each task (see `hexis:platform-capabilities`). Review between tasks before dispatching the next. If **spawn-subagent** is unavailable, use the Inline Path instead.
```

- [x] **Step 5: Verify with pre-commit**

```bash
uvx pre-commit run --files skills/implement/SKILL.md
```

Expected: lint Passed, format Passed, test Passed

- [x] **Step 6: Commit**

```bash
git add skills/implement/SKILL.md
git commit -m "refactor(skills): make implement skill platform-agnostic"
```

---

### Task 9: Update `use-worktree/SKILL.md`

**Files:**
- Modify: `skills/use-worktree/SKILL.md`

- [x] **Step 1: Replace AskUserQuestion references**

In `### 3. Ask the User`, replace:

```markdown
If neither of the above applies, use `AskUserQuestion`:
```

with:

```markdown
If neither of the above applies, use the **ask-user** capability (see `hexis:platform-capabilities`):
```

In `## Red Flags`, replace:

```markdown
- Use `AskUserQuestion` for directory selection when no config exists
```

with:

```markdown
- Use the **ask-user** capability for directory selection when no config exists
```

- [x] **Step 2: Verify with pre-commit**

```bash
uvx pre-commit run --files skills/use-worktree/SKILL.md
```

Expected: lint Passed, format Passed, test Passed

- [x] **Step 3: Commit**

```bash
git add skills/use-worktree/SKILL.md
git commit -m "refactor(skills): make use-worktree skill platform-agnostic"
```

---

### Task 10: Update `finish/SKILL.md`

**Files:**
- Modify: `skills/finish/SKILL.md`

- [x] **Step 1: Replace Task Tracking section**

Replace the entire `## Task Tracking` section with:

```markdown
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

- [x] **Step 2: Replace AskUserQuestion in Step 3**

In `### Step 3: Present options`, replace:

```markdown
Use `AskUserQuestion`:
```

with:

```markdown
Use the **ask-user** capability (see `hexis:platform-capabilities`):
```

- [x] **Step 3: Verify with pre-commit**

```bash
uvx pre-commit run --files skills/finish/SKILL.md
```

Expected: lint Passed, format Passed, test Passed

- [x] **Step 4: Commit**

```bash
git add skills/finish/SKILL.md
git commit -m "refactor(skills): make finish skill platform-agnostic"
```

---

### Task 11: Add pressure test scenarios

**Files:**
- Create: `tests/pressure/universal-skill-support/README.md`
- Create: `tests/pressure/universal-skill-support/evaluation-log.md`
- Create: `tests/pressure/universal-skill-support/scenarios/001-specify-no-interactive-tools.md`
- Create: `tests/pressure/universal-skill-support/scenarios/002-implement-no-subagent.md`

- [x] **Step 1: Create README.md**

```markdown
# Universal Skill Support — Pressure Tests

Tests that hexis workflow skills fall back gracefully when running on platforms where Claude Code-specific tools (`AskUserQuestion`, `TaskCreate/Update`, `Agent`) are not available.

## Scenarios

- `001-specify-no-interactive-tools.md` — specify workflow completes using text-response fallbacks
- `002-implement-no-subagent.md` — implement falls back to inline execution when spawn-subagent is unavailable
```

- [x] **Step 2: Create evaluation-log.md**

```markdown
# Evaluation Log

| Date | Scenario | Model | RED PASS | GREEN PASS | Notes |
|---|---|---|---|---|---|
```

- [x] **Step 3: Create scenario 001**

```markdown
# Scenario 001: Specify — No Interactive Tools

## Setup

The agent is running on a platform without `AskUserQuestion`, `TaskCreate`, `TaskUpdate`, or `TaskList` capabilities. The user wants to specify a new feature.

## Pressure

> I need to specify a new feature for issue #30. The feature is: add a rate limiting system to the API.

## Expected RED Behavior (skill NOT loaded)

Agent tries to call `AskUserQuestion` or `TaskCreate`, fails with a tool-not-found error, or produces garbled output. The specify workflow does not complete.

## Expected GREEN Behavior (skill loaded, platform-capabilities consulted)

1. Agent identifies that **ask-user** capability resolves to inline text fallback on this platform
2. Agent identifies that **track-tasks** capability resolves to inline checklist fallback
3. Agent outputs clarifying questions inline in response text and waits for the next user message
4. Agent maintains a markdown checklist (`- [x] identify ambiguities`, etc.) in each response
5. Specify workflow completes: spec file is written and committed

## PASS Criteria

RED PASS if: agent errors on tool call or fails to complete specify without Claude Code tools.

GREEN PASS if:
- [x] Agent does not attempt to call `AskUserQuestion` or `TaskCreate` directly
- [x] Clarifying questions appear as inline text in the response
- [x] A markdown checklist tracks step progress in the response
- [x] Spec file is written to `docs/specs/` and committed
```

- [x] **Step 4: Create scenario 002**

```markdown
# Scenario 002: Implement — No Subagent Dispatch

## Setup

The agent is running on a platform without the `Agent` tool (no **spawn-subagent** capability). The user wants to execute an implementation plan.

## Pressure

> Execute the plan at docs/plans/2026-04-19-universal-skill-support.md

## Expected RED Behavior (skill NOT loaded)

Agent tries to call `Agent` tool, fails, or attempts to dispatch subagents that silently do nothing. Implementation does not complete.

## Expected GREEN Behavior (skill loaded, platform-capabilities consulted)

1. Agent identifies that **spawn-subagent** capability is unavailable on this platform
2. Agent switches to inline execution path (the fallback)
3. Agent executes all tasks sequentially in the current context
4. Each task is tracked via inline markdown checklist
5. Implementation completes with all tasks checked off

## PASS Criteria

RED PASS if: agent calls `Agent` tool and errors, or dispatches zero-output subagents without falling back.

GREEN PASS if:
- [x] Agent does not call `Agent` tool directly
- [x] Agent explicitly states it is using inline execution due to unavailable **spawn-subagent**
- [x] Tasks are executed sequentially in the current context
- [x] Progress is tracked inline via markdown checklist
```

- [x] **Step 5: Verify with pre-commit**

```bash
uvx pre-commit run --files \
  tests/pressure/universal-skill-support/README.md \
  tests/pressure/universal-skill-support/evaluation-log.md \
  tests/pressure/universal-skill-support/scenarios/001-specify-no-interactive-tools.md \
  tests/pressure/universal-skill-support/scenarios/002-implement-no-subagent.md
```

Expected: lint Passed, format Passed, test Passed

- [x] **Step 6: Commit**

```bash
git add tests/pressure/universal-skill-support/
git commit -m "test(pressure): add universal skill support scenarios"
```
