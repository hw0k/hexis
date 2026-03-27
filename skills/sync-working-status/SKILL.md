---
name: sync-working-status
description: Synchronizes current work state between local git state and GitHub — checks PR status, resolves discrepancies, and confirms everything reflects actual progress
type: workflow
---

# Sync Working Status

## Purpose

Keep work state consistent between local git and GitHub (PRs, issues, labels) so that anyone — or any future agent — picking up this work has an accurate picture.

## When to Run

- Before switching to a different task or branch
- After completing a significant chunk of work
- When returning to a branch after time away
- Before requesting a code review or converting a draft PR

## Steps

### 1. Assess Local State

```bash
git status              # uncommitted changes
git log --oneline -5    # recent commits not yet in PR
git branch -vv          # branch tracking + ahead/behind count
```

Note:
- Are there uncommitted changes that should be committed first?
- How many commits are ahead of the remote?

### 2. Assess GitHub State

For the current branch, check the associated PR (if any):

- **PR status:** draft / open / needs review / changes requested / approved / merged / closed
- **CI status:** passing / failing / pending
- **Open review threads:** any unresolved comments?
- **Linked issue:** still open? still accurate?

If no PR exists yet and the branch has commits, note whether one should be created.

### 3. Resolve Discrepancies

| Local state | GitHub state | Action |
|-------------|--------------|--------|
| Commits ahead, not pushed | PR shows old state | Push: `git push` |
| Work is done | PR is still draft | Convert to "Ready for review" |
| All review comments addressed | Threads still open | Mark threads resolved on GitHub |
| Work complete | Linked issue still open | Close issue, add closing reference to PR |
| No PR | Feature complete | Create PR with accurate description |
| PR description outdated | Describes planned work, not actual | Update PR description to reflect what was done |

### 4. Update PR Description (if applicable)

A PR description should reflect the current state of the work, not just the original intent. Update it to include:
- What was actually done (not just the plan)
- Any known issues or deferred work
- How to test the changes

### 5. Confirm Sync Complete

Before declaring sync done, verify:
- [ ] All intended commits are pushed to remote
- [ ] PR status matches actual readiness (not stuck in draft)
- [ ] No unresolved review threads from addressed feedback
- [ ] Linked issue status matches work state
- [ ] PR description accurately describes what was built
