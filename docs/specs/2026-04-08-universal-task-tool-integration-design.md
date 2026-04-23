---
issue: 15
plan: docs/plans/2026-04-08-universal-task-tool-integration.md
---

# Universal Task Tool Integration

## Problem

hw0k-workflow skills perform multi-step work with no structured task tracking. Long-running or interrupted executions are opaque — there is no way to know which step is in progress, resume from a specific point, or audit what completed. This is not limited to execute-phase skills; `specify` and `plan` also have named multi-step processes that suffer the same problem.

## What

Integrate the Task tool suite (`TaskCreate`, `TaskUpdate`, `TaskGet`, `TaskList`, `TaskStop`) into all hw0k-workflow skills that have named multi-step processes, at step granularity — one Task per named step.

**Scope expansion vs. issue #15 framing:** The original issue scoped this to execute-phase skills only (`implement`, `write-test`, `debug`, `verify`, `review`, `finish`). This spec expands adoption to `specify` and `plan` as well, for the same reason: both have structured multi-step processes where task tracking provides identical value.

## Tool Responsibilities

| Tool | When to Use |
|---|---|
| `TaskCreate` | At the start of each named step |
| `TaskUpdate` | To mark in_progress on start, completed on finish |
| `TaskGet` / `TaskList` | At skill start to detect interrupted work; before dispatching sub-steps |
| `TaskStop` | On failure, cancellation, or user abort |

## Task Granularity

**One Task per named step, not one Task per skill invocation.**

A "named step" is a discrete unit within a skill's process that has a clear start and end — e.g., "RED: Write failing test" in `write-test`, or "Draft spec" in `specify`. Each such step is its own Task.

Task lifecycle for each step:

```
TaskCreate("<skill>: <step-name>") → TaskUpdate(in_progress) → TaskUpdate(completed)
                                                          ↓ on failure
                                                      TaskStop
```

## Task Naming Convention

Task names follow the pattern: `<skill>: <step-name>`.

Examples:
- `specify: identify ambiguities`
- `write-test: red phase`
- `implement: execute plan 2026-04-08-feature.md`
- `implement/task-3: add authentication middleware`

This allows `TaskList` filtering by prefix at skill start.

## Resume Behavior (All Skills)

At the start of every skill invocation:

1. Call `TaskList` filtered by the current skill's name prefix
2. If open Tasks found from a prior session: surface them via `AskUserQuestion`
   - **Option A — Resume:** Continue from the last open Task (use `TaskGet` to verify exact state before proceeding)
   - **Option B — Start fresh:** Call `TaskStop` on all open Tasks, then create new Tasks from step 1
3. Proceed based on user choice
4. If no open Tasks found: proceed directly without prompting

## Per-Skill Integration

### specify

| Step | Task Name |
|---|---|
| Step 1: Identify Ambiguities | `specify: identify ambiguities` |
| Step 2: Ask Clarifying Questions | `specify: ask clarifying questions` |
| Step 3: Draft | `specify: draft spec` |
| Step 4: Write and Commit | `specify: write and commit spec` |
| Step 5: Hand Off | `specify: hand off to plan` |

### plan

| Step | Task Name |
|---|---|
| Scope Check | `plan: scope check` |
| File Structure | `plan: define file structure` |
| Task Writing | `plan: write tasks` |
| Self-Review | `plan: self-review` |
| Save and Commit | `plan: save and commit` |

### implement

Two-level Task hierarchy:

**Parent Task** — created by `implement` at start:
- Name: `implement: execute plan <plan-filename>`
- Updated when: dispatching each subagent, completing each review between subagents
- Stopped: on failure or cancellation before all tasks complete

**Child Tasks** — created by each dispatched subagent:
- Name: `implement/task-N: <task-name>` (using N from the plan, task-name from plan)
- The `implement` skill must instruct each dispatched subagent to create its own Task at the start of execution
- The subagent uses `TaskGet` to verify Task state before starting work, and `TaskStop` on failure
- Parent uses `TaskList` filtered by `implement/task-` prefix before dispatching the next subagent, to verify prior task completed successfully

**Inline path** (existing partial implementation, now extended):

| Step | Task Name |
|---|---|
| Per plan task | `implement/task-N: <task-name>` |

### write-test

| Phase | Task Name |
|---|---|
| RED: Write failing test | `write-test: red phase` |
| Verify RED | (part of red phase Task — no separate Task) |
| GREEN: Minimal implementation | `write-test: green phase` |
| Verify GREEN | (part of green phase Task — no separate Task) |
| REFACTOR: Clean up | `write-test: refactor phase` |

### debug

| Phase | Task Name |
|---|---|
| Phase 1: Root Cause Investigation | `debug: root cause investigation` |
| Phase 2: Pattern Analysis | `debug: pattern analysis` |
| Phase 3: Hypotheses and Verification | `debug: hypotheses and verification` |
| Phase 4: Implementation | `debug: fix implementation` |

### verify

| Check | Task Name |
|---|---|
| Type check | `verify: type check` |
| Lint | `verify: lint` |
| Tests | `verify: tests` |

Note: When `verify` is invoked as a sub-step by another skill (e.g., `review`, `finish`), it creates its own Tasks independently. No coordination needed.

### review

| Step | Task Name |
|---|---|
| Step 2: Collect git SHAs | `review: collect git SHAs` |
| Step 3: Principles review | `review: principles review` |
| Step 4: Handle results | `review: handle results` |

Note: Step 1 delegates to `hw0k-workflow:verify` which manages its own Tasks. No separate Task created in `review` for this step.

### finish

| Step | Task Name |
|---|---|
| Step 2: Handle uncommitted changes | `finish: handle uncommitted changes` |
| Step 3–4: Integration | `finish: integration` |
| Step 5: Clean up worktree | `finish: clean up worktree` |

Note: Step 1 delegates to `hw0k-workflow:verify`. No separate Task in `finish` for this step.

## Failure Behavior

On any failure or user abort within a skill:

1. Call `TaskStop` on the current open Task (the step that failed)
2. If the skill has a parent Task (e.g., implement): call `TaskStop` on the parent Task as well
3. Do not leave any Tasks in an unresolved (created or in_progress) state

A stopped Task is terminal — it cannot be resumed. If the user chooses to retry, a new Task is created.

## Out of Scope

- **`dispatch`:** Read-only state detection that completes in seconds. Task overhead is not justified.
- **`receive-review`:** Single decision point, not a multi-step process.
- **`use-worktree`:** Setup operation, single action.
- **`setup-new-project`:** Onboarding utility, not a repeating workflow.
- **Principle skills** (`commit-principles`, `core-principles`, etc.): Reference material, not processes.
- **`principles-reviewer` agent:** Not a skill.

## Done When

- [ ] All listed skills create Tasks at the step level on invocation
- [ ] Every listed skill checks `TaskList` at start and presents resume/fresh-start choice when open Tasks exist
- [ ] `TaskStop` is called on all failure and cancellation paths
- [ ] `implement` creates a parent Task and instructs each dispatched subagent to create a child Task
- [ ] `TaskGet`/`TaskList` is used before dispatching sub-steps in `implement` to verify prior task state
- [ ] No Task is left in an unresolved state after a skill exits (success or failure)
