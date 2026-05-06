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

Before anything else, tell the user that dispatch is active and that the CLAUDE.md routing rules are being enforced for this session.

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

Ask the user which issue number they are working on. Accept either a numeric issue number or an explicit indication that this is brand-new work with no issue yet.

- Number provided → use as `N`, proceed to Step 1b
- No issue / brand-new work → invoke `hexis:specify`

**Step 1b — with issue number `N`:**

Run in parallel:

```bash
hexis status read N --json
gh pr list --head $(git branch --show-current) --json number,state,isDraft,reviewDecision,statusCheckRollup --limit 1
```

Where `N` is the literal issue number (e.g., for issue 20: `hexis status read 20 --json`).

Collect:
- `status`: the full JSON object from `hexis status read --json` (contains `state`, `issue`, `plan_tasks`, `checks`, `blocking`)
- `pr`: the PR object from `gh`, or empty if none

## Step 2: Routing

Apply the **first matching rule** in this order:

| Rule | Condition | Next Skill |
|------|-----------|-----------|
| 1 | `git status --short` output is non-empty | `sync-working-status` |
| 2 | `status.state` is `NEEDS_SPEC` | `specify` |
| 3 | `status.state` is `NEEDS_PLAN` | `plan` |
| 4 | `status.state` is `IN_PROGRESS` | `implement` |
| 5 | `status.state` is `NEEDS_VERIFY` | `verify` |
| 6 | `status.state` is `DONE` AND no open PR | — (stop: tell the user that issue #N is already complete and there is nothing to dispatch) |
| 7 | PR open AND any check is failing | `verify` |
| 8 | PR open AND all checks passing AND review not approved | `review` |
| 9 | PR open AND approved | `finish` |
| 10 | PR merged | — (stop, see below) |

**Rule 1 — sync-working-status special handling:**

Tell the user that uncommitted changes were detected, that `hexis:sync-working-status` is being run now, and that they should re-run `hexis:dispatch` after it finishes.

Invoke `hexis:sync-working-status`. Do NOT continue routing after sync — stop dispatch here. The user re-invokes dispatch manually.

**Rule 10 — PR merged:**

Tell the user that the PR for issue #N is already merged, the work is complete, and there is nothing left to dispatch.

Stop. Do not invoke any skill.

## Step 3: Dispatch Output

For all rules except Rule 1 and Rule 8, briefly tell the user the detected state and which `hexis:<skill>` will be invoked next.

Then immediately invoke the determined skill. No confirmation prompt.

## Notes

- `hexis status read` is the authoritative source for issue state. The LLM does not infer state from file presence independently — CLI output determines routing.
- Multiple issues on one branch: dispatch uses the first integer found in the branch name. If this is wrong, pass the correct issue number when asked.
