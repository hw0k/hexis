---
issue: 10
status: DONE
checks:
  - item: "`skills/dispatch/SKILL.md` exists with correct frontmatter"
    done: true
  - item: "Skill detects state from git branch, git status, docs/specs/, docs/plans/, and GitHub PR"
    done: true
  - item: "Routes to the correct next skill based on routing table (first-match)"
    done: true
  - item: "Directly invokes the next skill — not just recommends"
    done: true
  - item: "Works correctly when invoked at any point in the workflow"
    done: true
  - item: "Outputs workflow enforcement header on every run"
    done: true
  - item: "`sync-working-status` path instructs re-run instead of auto-resuming"
    done: true
  - item: "\"No issue detected\" path asks user before defaulting to `specify`"
    done: true
---

# hw0k-workflow:dispatch Skill Design

## Problem

hw0k-workflow defines a clear skill routing table, but the agent has no mechanism to enforce it at any arbitrary point in a session. Users must manually decide which skill to invoke next — this creates gaps where the wrong skill is used, or no skill is used at all.

There is also no single point where the agent acknowledges it is operating under hw0k-workflow rules.

## What

A new skill `hw0k-workflow:dispatch` that:

1. Detects the current workflow state from git, docs, and GitHub
2. Determines the correct next skill based on that state
3. Directly invokes that skill — not just recommends it

`dispatch` can be invoked at **any point** in a session. It is not limited to session start. Its output is always the same: current state summary + immediate skill invocation.

## Behavior

### Step 1: State Detection

Run these commands in parallel:

```bash
git branch --show-current
git status --short
git log --oneline -5
```

**Extract issue number from branch name:**
- Pattern: first integer sequence found after the last `/` separator
  - `feat/10-add-dispatch` → `10`
  - `fix/123-something` → `123`
  - `main`, `chore/no-number` → no issue detected

**If no issue number detected:**
- Ask user: "What issue number are you working on? (Enter 'none' if starting new work)"
- If number provided: use it and continue
- If "none": invoke `hw0k-workflow:specify`

**With issue number `N`:**
- Search `docs/specs/` for files containing `#N` in their content
- Search `docs/plans/` for files containing `#N` in their content
- Run: `gh pr list --head $(git branch --show-current) --json number,state,isDraft,reviewDecision,statusCheckRollup --limit 1`

### Step 2: Routing

Apply the **first matching rule** in order:

| Condition | Next Skill |
|-----------|-----------|
| Uncommitted changes exist (`git status --short` non-empty) | `sync-working-status` |
| No spec file found for issue `#N` | `specify` |
| Spec exists, no plan file found for issue `#N` | `plan` |
| Plan exists, no open PR | `implement` |
| PR exists and is draft | `implement` |
| PR open, checks failing | `verify` |
| PR open, checks passing, review not approved | `review` |
| PR open, approved | `finish` |
| PR merged | Output: "Work for #N is complete. Nothing to dispatch." — stop |

**sync-working-status special case:**
After determining `sync-working-status` is needed, output:
> "State: uncommitted changes detected. Running hw0k-workflow:sync-working-status first. After it completes, re-run hw0k-workflow:dispatch to continue."

Then invoke `sync-working-status`. Do NOT auto-resume dispatch — the user re-invokes manually.

### Step 3: Invoke

State the routing decision clearly before invoking:

```
State: <one-line summary>
Dispatching → hw0k-workflow:<skill>
```

Then immediately invoke the determined skill. No confirmation prompt — dispatch is a workflow enforcer, not a menu.

## Workflow Enforcement Header

At the start of every dispatch run, output:

```
hw0k-workflow:dispatch — active
Routing rules: CLAUDE.md skill table enforced for this session.
```

This serves as the explicit acknowledgment that hw0k-workflow rules are in effect.

## Out of Scope

- Modifying any files (dispatch is read-only before invoking the next skill)
- Substituting for any individual skill's internal logic
- Handling multiple concurrent issues on a single branch
- Detecting partial completion within a skill (e.g., which plan tasks are checked)

## Issue Number in Spec/Plan Files

For dispatch to find spec/plan files by issue number, those files must reference the issue number. Convention: include `Issue: #N` in the file header (as this spec does). The `specify` skill should embed this when creating new spec files.
