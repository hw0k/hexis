# /hw0k-workflow:sync

Synchronize current work state across Local and GitHub.

## Steps

1. Assess local git state: `git status`, `git log --oneline -5`, `git branch -vv`
2. Assess GitHub state for the current branch — check PR status, CI, open review threads, linked issue
3. Resolve any discrepancies found (push, update PR, mark resolved threads, close issue)
4. Update the PR description if it no longer reflects what was built
5. Confirm all sync items are complete

## Skill Reference

Use `hw0k-workflow:sync-working-status` for the full step-by-step guide including the discrepancy resolution table and confirmation checklist.
