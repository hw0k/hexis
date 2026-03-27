---
name: sync-working-status
description: Synchronizes current work state across three targets — local git, specs/plans, and remote GitHub — checks PR status, resolves discrepancies, and confirms everything reflects actual progress
type: workflow
---

# Sync Working Status

## Purpose

Keep work state consistent across local git, specs/plans, and GitHub so that anyone — or any future agent — picking up this work has an accurate picture.

## When to Run

- Before switching to a different task or branch
- After completing a significant chunk of work
- When returning to a branch after time away
- Before requesting a code review or converting a draft PR
- After any Claude session that produced file changes

## Steps

### 1. Assess Local Git State

```bash
git status              # uncommitted changes
git log --oneline -5    # recent commits not yet in PR
git branch -vv          # branch tracking + ahead/behind count
```

Note:
- Are there uncommitted changes that should be committed first?
- How many commits are ahead of the remote?

### 2. Assess Specs/Plans State

Check `docs/specs/` and `docs/plans/` for files related to current work:

- Do plan file checkboxes reflect actual progress? (Mark completed tasks as `- [x]`)
- Does the spec still describe what is being built, or has scope changed?
- Is there a plan file for current work? If not, note the gap.

Specs and plans are the single source of truth for task progress. Update them before syncing remotely.

### 3. Assess Remote State

For the current branch, check the associated PR (if any):

- **PR status:** draft / open / needs review / changes requested / approved / merged / closed
- **CI status:** passing / failing / pending
- **Open review threads:** any unresolved comments?
- **Linked issue:** still open? still accurate?

If no PR exists and the branch has commits, note whether one should be created.

### 4. Resolve Discrepancies

| Local state | Remote state | Action |
|-------------|-------------|--------|
| Commits ahead, not pushed | PR shows old state | Push: `git push` |
| Work is done | PR is still draft | Convert to "Ready for review" |
| All review comments addressed | Threads still open | Mark threads resolved on GitHub |
| Work complete | Linked issue still open | Close issue, add closing reference to PR |
| No PR | Feature complete | Create PR with accurate description |
| PR description outdated | Describes planned work, not actual | Update PR description |
| Plan checkboxes stale | Tasks completed but not marked | Update plan file checkboxes |
| Spec scope has changed | Spec describes original intent | Update spec to reflect what was built |

### 5. Confirm Sync Complete

Before declaring sync done, verify:
- [ ] All intended commits are pushed to remote
- [ ] Plan file checkboxes reflect actual progress
- [ ] Spec describes what was actually built
- [ ] PR status matches actual readiness
- [ ] No unresolved review threads from addressed feedback
- [ ] Linked issue status matches work state
- [ ] PR description accurately describes what was built
