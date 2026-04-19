---
name: dispatch
description: State-aware workflow router — detects current position in the hexis and directly invokes the correct next skill
type: workflow
---

# Dispatch

## Overview

`dispatch` is a state-aware workflow enforcer. It detects where you are in the hexis and immediately invokes the correct next skill — no manual routing required.

Invoke at any point: session start, after returning from a break, when unsure of next step.

**IMPORTANT:** dispatch does not modify files, commit, or push. It is read-only until the invoked skill takes over.

## On Every Run

Output this header before anything else:

```
hexis:dispatch — active
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
- "none" → invoke `hexis:specify`

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
State: uncommitted changes detected. Running hexis:sync-working-status.
After it completes, re-run hexis:dispatch to continue.
```

Invoke `hexis:sync-working-status`. Do NOT continue routing after sync — stop dispatch here. The user re-invokes dispatch manually.

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
Dispatching → hexis:<skill>
```

Then immediately invoke the determined skill. No confirmation prompt.

## Notes

- If spec/plan files do not embed `Issue: #N` in their content, dispatch cannot locate them — they are treated as non-existent, and dispatch routes to `specify` or `plan` accordingly.
- Multiple issues on one branch: dispatch uses the first integer found in the branch name. If this is wrong, pass the correct issue number when asked.
