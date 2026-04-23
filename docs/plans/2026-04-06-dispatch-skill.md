---
issue: 10
status: DONE
linked_spec: docs/specs/2026-04-06-dispatch-skill-design.md
---

# hw0k-workflow:dispatch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hw0k-workflow:implement` to execute task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `hw0k-workflow:dispatch` — a state-aware skill that detects current workflow position and directly invokes the correct next skill, enforcing hw0k-workflow at any point in a session.

**Architecture:** Single `SKILL.md` file that encodes state detection logic (git + docs + GitHub) and a priority-ordered routing table. No code — skill behavior is encoded as agent instructions in Markdown. Supporting changes update `specify` to embed issue numbers, and add `dispatch` to the global CLAUDE.md routing table so users know when to invoke it.

**Tech Stack:** Markdown (SKILL.md), bash (git, grep, gh CLI for state detection in skill instructions)

Issue: #10

---

## Files

| Action | Path |
|--------|------|
| Create | `skills/dispatch/SKILL.md` |
| Create | `tests/pressure/dispatch/README.md` |
| Create | `tests/pressure/dispatch/evaluation-log.md` |
| Create | `tests/pressure/dispatch/scenarios/001-no-spec-routes-to-specify.md` |
| Create | `tests/pressure/dispatch/scenarios/002-spec-no-plan-routes-to-plan.md` |
| Create | `tests/pressure/dispatch/scenarios/003-dirty-tree-routes-to-sync.md` |
| Create | `tests/pressure/dispatch/scenarios/004-enforcement-header.md` |
| Modify | `skills/specify/SKILL.md` (Step 4 — add issue number convention) |
| Modify | `/home/hw0k-win11-wsl/.claude/CLAUDE.md` (routing table) |

---

### Task 1: Pressure test infrastructure — README and evaluation log

**Files:**
- Create: `tests/pressure/dispatch/README.md`
- Create: `tests/pressure/dispatch/evaluation-log.md`

- [x] **Step 1: Write failing test — confirm no dispatch test directory exists**

```bash
ls tests/pressure/dispatch/ 2>/dev/null || echo "FAIL: directory does not exist yet"
```

Expected: `FAIL: directory does not exist yet`

- [x] **Step 2: Create README.md**

```markdown
# Pressure Tests — `hw0k-workflow:dispatch`

Skill pressure testing applies TDD to skill documentation. Verifies that `dispatch` actually constrains agent behavior — not just that it exists.

## What RED/GREEN means

- **RED:** Run the scenario in a fresh Claude Code session with NO `hw0k-workflow` skills loaded. Passes RED if the agent fails to route correctly (confirms the test catches a real gap).
- **GREEN:** Run the same scenario with `hw0k-workflow:dispatch` loaded. Passes GREEN if the agent detects state, outputs the enforcement header, and invokes the correct next skill.

## How to run a scenario

1. Open the scenario file. Read **Setup** and **Pressure**.
2. Start a **fresh Claude Code session** (clear context, no prior conversation).
3. **RED phase:** Do not load any `hw0k-workflow` skills. Paste the **Pressure** prompt verbatim.
4. **GREEN phase:** In a new fresh session, load `hw0k-workflow:dispatch`. Paste the same prompt.
5. Evaluate against **PASS Criteria** in the scenario file.
6. Record results in `evaluation-log.md`.

## Enforced rules (what these tests cover)

- Enforcement header appears on every dispatch run
- Routes to `specify` when no spec file contains `#N`
- Routes to `plan` when spec exists but no plan file contains `#N`
- Routes to `sync-working-status` when git status is dirty (non-empty output)
- Does NOT auto-resume after `sync-working-status` — user must re-invoke dispatch
```

- [x] **Step 3: Create evaluation-log.md**

```markdown
# Evaluation Log — `hw0k-workflow:dispatch`

| Date | Scenario | RED result | GREEN result | Notes |
|------|----------|-----------|-------------|-------|
| — | — | — | — | Not yet evaluated |
```

- [x] **Step 4: Confirm files exist**

```bash
ls tests/pressure/dispatch/
```

Expected: `README.md  evaluation-log.md`

- [x] **Step 5: Commit**

```bash
git add tests/pressure/dispatch/README.md tests/pressure/dispatch/evaluation-log.md
git commit -m "test: add dispatch pressure test infrastructure"
```

---

### Task 2: Pressure test scenarios

**Files:**
- Create: `tests/pressure/dispatch/scenarios/001-no-spec-routes-to-specify.md`
- Create: `tests/pressure/dispatch/scenarios/002-spec-no-plan-routes-to-plan.md`
- Create: `tests/pressure/dispatch/scenarios/003-dirty-tree-routes-to-sync.md`
- Create: `tests/pressure/dispatch/scenarios/004-enforcement-header.md`

- [x] **Step 1: Confirm scenarios directory does not exist yet**

```bash
ls tests/pressure/dispatch/scenarios/ 2>/dev/null || echo "FAIL: directory does not exist yet"
```

Expected: `FAIL: directory does not exist yet`

- [x] **Step 2: Write scenario 001 — no spec routes to specify**

```markdown
# Scenario 001: No Spec — Routes to `specify`

## Setup

The agent is on branch `feat/10-add-dispatch`. No file in `docs/specs/` contains `#10`. The user wants to start work.

## Pressure

> I'm working on issue #10. I'm on branch feat/10-add-dispatch. Help me figure out what to do next.

## Expected RED Behavior (skill NOT loaded)

Agent gives an ad-hoc response: asks what the feature is, jumps to implementation, or suggests writing code without routing. No structured state detection.

## Expected GREEN Behavior (skill loaded)

1. Outputs enforcement header: "hw0k-workflow:dispatch — active / Routing rules: CLAUDE.md skill table enforced for this session."
2. Runs `git branch --show-current`, `git status --short`, searches `docs/specs/` for `#10`
3. Finds no spec file, outputs: "State: no spec found for #10. Dispatching → hw0k-workflow:specify"
4. Immediately invokes `hw0k-workflow:specify`

## PASS Criteria

RED PASS if: agent does not detect `#10`, does not search `docs/specs/`, and does not invoke `hw0k-workflow:specify`.

GREEN PASS if:
- [ ] Enforcement header appears at start of output
- [ ] Agent searches for `#10` in `docs/specs/`
- [ ] Agent outputs "Dispatching → hw0k-workflow:specify" (or equivalent)
- [ ] Agent invokes `hw0k-workflow:specify` immediately after
```

- [x] **Step 3: Write scenario 002 — spec exists, no plan**

```markdown
# Scenario 002: Spec Exists, No Plan — Routes to `plan`

## Setup

The agent is on branch `feat/10-add-dispatch`. `docs/specs/2026-04-06-dispatch-skill-design.md` contains `#10`. No file in `docs/plans/` contains `#10`. Git is clean.

## Pressure

> I'm on feat/10-add-dispatch. I've already written the spec. What's next?

## Expected RED Behavior (skill NOT loaded)

Agent says "let's start implementing" or asks about requirements. Does not check `docs/plans/` for a plan file.

## Expected GREEN Behavior (skill loaded)

1. Outputs enforcement header.
2. Runs state detection: `git status --short` returns empty (clean). Searches `docs/specs/` for `#10` — finds the file. Searches `docs/plans/` for `#10` — finds nothing.
3. Outputs: "State: spec exists for #10, no plan found. Dispatching → hw0k-workflow:plan"
4. Immediately invokes `hw0k-workflow:plan`.

## PASS Criteria

RED PASS if: agent does not check `docs/plans/` for `#10` and does not invoke `hw0k-workflow:plan`.

GREEN PASS if:
- [ ] Enforcement header appears
- [ ] Agent confirms git is clean before checking docs
- [ ] Agent searches `docs/plans/` for `#10`
- [ ] Agent outputs "Dispatching → hw0k-workflow:plan"
- [ ] Agent invokes `hw0k-workflow:plan` immediately
```

- [x] **Step 4: Write scenario 003 — dirty tree routes to sync**

```markdown
# Scenario 003: Dirty Working Tree — Routes to `sync-working-status`

## Setup

The agent is on branch `feat/10-add-dispatch`. `git status --short` returns non-empty output (modified files). Both spec and plan exist for `#10`.

## Pressure

> I've been working on feat/10-add-dispatch. Some files are modified. Help me figure out what to do next.

## Expected RED Behavior (skill NOT loaded)

Agent either ignores uncommitted changes or offers to commit them, without routing to `sync-working-status`. May jump straight to next implementation step.

## Expected GREEN Behavior (skill loaded)

1. Outputs enforcement header.
2. Runs `git status --short` — sees non-empty output.
3. Outputs: "State: uncommitted changes detected. Running hw0k-workflow:sync-working-status. After it completes, re-run hw0k-workflow:dispatch to continue."
4. Invokes `hw0k-workflow:sync-working-status`.
5. Does NOT continue with dispatch routing after sync — explicitly tells user to re-run dispatch.

## PASS Criteria

RED PASS if: agent does not invoke `sync-working-status` and does not instruct re-running dispatch.

GREEN PASS if:
- [ ] Enforcement header appears
- [ ] Agent runs `git status --short` and detects non-empty output
- [ ] Agent invokes `hw0k-workflow:sync-working-status`
- [ ] Agent explicitly states user must re-run `hw0k-workflow:dispatch` after sync
- [ ] Agent does NOT auto-continue with other routing after sync
```

- [x] **Step 5: Write scenario 004 — enforcement header**

```markdown
# Scenario 004: Enforcement Header Always Appears

## Setup

Any state — clean branch, with or without spec/plan. The user invokes dispatch.

## Pressure

> Run hw0k-workflow:dispatch.

## Expected RED Behavior (skill NOT loaded)

Agent either does nothing, asks what to do, or proceeds without outputting any workflow enforcement header.

## Expected GREEN Behavior (skill loaded)

The very first output is:
```
hw0k-workflow:dispatch — active
Routing rules: CLAUDE.md skill table enforced for this session.
```

This appears before any state detection output.

## PASS Criteria

RED PASS if: no enforcement header appears in the output.

GREEN PASS if:
- [ ] "hw0k-workflow:dispatch — active" appears in the first output block
- [ ] "Routing rules: CLAUDE.md skill table enforced for this session." appears in the first output block
- [ ] Both lines appear BEFORE any state detection results
```

- [x] **Step 6: Confirm all 4 scenario files exist**

```bash
ls tests/pressure/dispatch/scenarios/
```

Expected: 4 files — `001-no-spec-routes-to-specify.md`, `002-spec-no-plan-routes-to-plan.md`, `003-dirty-tree-routes-to-sync.md`, `004-enforcement-header.md`

- [x] **Step 7: Commit**

```bash
git add tests/pressure/dispatch/scenarios/
git commit -m "test: add dispatch pressure test scenarios (#10)"
```

---

### Task 3: Create `skills/dispatch/SKILL.md`

**Files:**
- Create: `skills/dispatch/SKILL.md`

- [x] **Step 1: Verify skill does not exist yet**

```bash
ls skills/dispatch/SKILL.md 2>/dev/null || echo "FAIL: skill does not exist yet"
```

Expected: `FAIL: skill does not exist yet`

- [x] **Step 2: Write `skills/dispatch/SKILL.md`**

```markdown
---
name: dispatch
description: State-aware workflow router — detects current position in the hw0k-workflow and directly invokes the correct next skill
type: workflow
---

# Dispatch

## Overview

`dispatch` is a state-aware workflow enforcer. It detects where you are in the hw0k-workflow and immediately invokes the correct next skill — no manual routing required.

Invoke at any point: session start, after returning from a break, when unsure of next step.

**IMPORTANT:** dispatch does not modify files, commit, or push. It is read-only until the invoked skill takes over.

## On Every Run

Output this header before anything else:

```
hw0k-workflow:dispatch — active
Routing rules: CLAUDE.md skill table enforced for this session.
```

## Step 1: State Detection

Run in parallel:

```bash
git branch --show-current
git status --short
git log --oneline -5
```

**Extract issue number from branch name:**

Take the branch name substring after the last `/`, then extract the first contiguous sequence of digits.

- `feat/10-add-dispatch` → `10`
- `fix/123-bug-name` → `123`
- `main` → no issue detected
- `chore/refactor-no-number` → no issue detected

**If no issue number detected:**

Use `AskUserQuestion` to ask: "What issue number are you working on? Enter the number, or 'none' if starting new work."

- Number provided → use as `N`, proceed to Step 1b
- "none" → invoke `hw0k-workflow:specify`

**Step 1b — with issue number `N`:**

Run in parallel:

```bash
grep -rl "#N" docs/specs/ 2>/dev/null
grep -rl "#N" docs/plans/ 2>/dev/null
gh pr list --head $(git branch --show-current) --json number,state,isDraft,reviewDecision,statusCheckRollup --limit 1
```

Collect:
- `spec_found`: true if any file in `docs/specs/` contains `#N`
- `plan_found`: true if any file in `docs/plans/` contains `#N`
- `pr`: the PR object from `gh`, or empty if none

## Step 2: Routing

Apply the **first matching rule** in this order:

| Rule | Condition | Next Skill |
|------|-----------|-----------|
| 1 | `git status --short` output is non-empty | `sync-working-status` |
| 2 | `spec_found` is false | `specify` |
| 3 | `spec_found` is true AND `plan_found` is false | `plan` |
| 4 | `plan_found` is true AND (no PR exists OR PR is draft) | `implement` |
| 5 | PR open AND any check is failing | `verify` |
| 6 | PR open AND all checks passing AND review not approved | `review` |
| 7 | PR open AND approved | `finish` |
| 8 | PR merged | — (stop, see below) |

**Rule 1 — sync-working-status special handling:**

Output:
```
State: uncommitted changes detected. Running hw0k-workflow:sync-working-status.
After it completes, re-run hw0k-workflow:dispatch to continue.
```

Invoke `hw0k-workflow:sync-working-status`. Do NOT continue routing after sync — stop dispatch here. The user re-invokes dispatch manually.

**Rule 8 — PR merged:**

Output:
```
State: PR for #N is merged. Work is complete. Nothing to dispatch.
```

Stop. Do not invoke any skill.

## Step 3: Dispatch Output

For all rules except Rule 1 and Rule 8, output before invoking:

```
State: <one-line summary of detected state>
Dispatching → hw0k-workflow:<skill>
```

Then immediately invoke the determined skill. No confirmation prompt.

## Notes

- If spec/plan files do not embed `Issue: #N` in their content, dispatch cannot locate them — they are treated as non-existent, and dispatch routes to `specify` or `plan` accordingly.
- Multiple issues on one branch: dispatch uses the first integer found in the branch name. If this is wrong, pass the correct issue number when asked.
```

- [x] **Step 3: Verify SKILL.md covers all scenario GREEN criteria**

```bash
grep -c "hw0k-workflow:dispatch — active" skills/dispatch/SKILL.md
grep -c "first matching rule" skills/dispatch/SKILL.md
grep -c "sync-working-status" skills/dispatch/SKILL.md
grep -c "re-run hw0k-workflow:dispatch" skills/dispatch/SKILL.md
grep -c "AskUserQuestion" skills/dispatch/SKILL.md
```

Expected: each command returns `1` or more

- [x] **Step 4: Commit**

```bash
git add skills/dispatch/SKILL.md
git commit -m "feat: add hw0k-workflow:dispatch skill (#10)"
```

---

### Task 4: Update `skills/specify/SKILL.md` — issue number convention

**Files:**
- Modify: `skills/specify/SKILL.md` (Step 4 section, lines ~63–69)

- [x] **Step 1: Read current Step 4 content**

```bash
grep -n "Step 4\|Write to\|Commit" skills/specify/SKILL.md
```

Expected: lines showing current Step 4 text.

- [x] **Step 2: Add issue number convention to Step 4**

In `skills/specify/SKILL.md`, locate Step 4 and update it to:

```markdown
### Step 4: Write and Commit

**MANDATORY — do this immediately after approval, before anything else.**

Write to `docs/specs/YYYY-MM-DD-<topic>-design.md`. The file must begin with:

```markdown
# <Title>

Issue: #N
```

Where `N` is the GitHub issue number this spec addresses. If there is no associated issue, omit the `Issue:` line. This line is required for `hw0k-workflow:dispatch` to locate the spec by issue number.

Commit: `docs: add <topic> spec`

Do NOT proceed to Step 5 until the spec file exists and is committed.
```

- [x] **Step 3: Verify the change**

```bash
grep -A8 "Step 4: Write and Commit" skills/specify/SKILL.md
```

Expected: output includes "Issue: #N" and the dispatch reference.

- [x] **Step 4: Commit**

```bash
git add skills/specify/SKILL.md
git commit -m "feat(specify): add issue number convention for dispatch compatibility (#10)"
```

---

### Task 5: Update global CLAUDE.md routing table

**Files:**
- Modify: `/home/hw0k-win11-wsl/.claude/CLAUDE.md`

- [x] **Step 1: Read current routing table**

```bash
grep -n "Situation\|dispatch\|Skill" /home/hw0k-win11-wsl/.claude/CLAUDE.md
```

Expected: routing table lines, no dispatch entry.

- [x] **Step 2: Add dispatch row to the routing table**

In `/home/hw0k-win11-wsl/.claude/CLAUDE.md`, update the skill routing table to add one row:

Before:
```markdown
| Situation | Skill |
|---|---|
| Requirement or task is vague | `hw0k-workflow:specify` |
```

After:
```markdown
| Situation | Skill |
|---|---|
| Unsure of next step / resuming work | `hw0k-workflow:dispatch` |
| Requirement or task is vague | `hw0k-workflow:specify` |
```

- [x] **Step 3: Verify the change**

```bash
grep "dispatch" /home/hw0k-win11-wsl/.claude/CLAUDE.md
```

Expected: `| Unsure of next step / resuming work | \`hw0k-workflow:dispatch\` |`

- [x] **Step 4: Commit**

```bash
git add /home/hw0k-win11-wsl/.claude/CLAUDE.md
git commit -m "feat(config): add dispatch to skill routing table in global CLAUDE.md (#10)"
```

---

## Completion

After all 5 tasks:

```bash
ls skills/dispatch/SKILL.md
ls tests/pressure/dispatch/scenarios/
grep "dispatch" /home/hw0k-win11-wsl/.claude/CLAUDE.md
grep "Issue: #N" skills/specify/SKILL.md
```

All commands should return expected output. Then invoke `hw0k-workflow:sync-working-status` and `hw0k-workflow:finish`.
