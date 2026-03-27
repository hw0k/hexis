# /hw0k-workflow:commit

Prepare and create a commit following the Conventional Commits format.

## Steps

1. Run `git status` to see what has changed
2. Run `git diff` (or `git diff --cached` if already staged) to understand what changed
3. Stage the relevant files: `git add <files>`
4. Determine the commit type based on the changes:
   - New capability → `feat`
   - Bug fix → `fix`
   - Only docs changed → `docs`
   - Only tests changed → `test`
   - Restructure with no behavior change → `refactor`
   - Tooling/config → `chore` or `build` or `ci`
5. Write the commit message following `hw0k-workflow:conventional-commit` rules
6. Create the commit: `git commit -m "<message>"`

## Skill Reference

Use `hw0k-workflow:conventional-commit` for the full format reference including allowed types, rules, and examples.
