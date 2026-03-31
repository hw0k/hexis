# hw0k-workflow

Heavily opinionated Claude Code plugin covering the full development workflow. Enforces consistent development standards regardless of device, agent, or tool.

## Plugin Structure

```
skills/          # User-invocable skills (hw0k-workflow:<name>)
agents/          # Agent definitions (hw0k-workflow:<name>)
commands/        # Slash commands
tests/pressure/  # Pressure test scenarios (RED/GREEN framework)
docs/specs/      # Design specs
docs/plans/      # Implementation plans
.githooks/       # Version-controlled git hooks (lefthook + commitlint)
```

## Skill Format

Each skill lives in `skills/<name>/SKILL.md` with frontmatter:

```yaml
---
name: <skill-name>
description: <one-line description used for skill matching>
type: workflow | reference | agent
---
```

Large skills split into a main `SKILL.md` (rules only) and a companion file:
- `reference.md` — edge cases, exemptions (e.g. `commit-principles/reference.md`)
- `examples.md` — code examples, before/after comparisons (e.g. `http-api-principles/examples.md`)

Flat directory only — nested skill directories are not supported by Claude Code.

## Git Hooks

This repo self-dogfoods its own hooks:

```bash
git config core.hooksPath .githooks
lefthook install --force
```

`lefthook install --force` generates `.githooks/commit-msg` and `.githooks/pre-commit` — these are gitignored artifacts, not tracked files. Run this command once after cloning.

Commit messages are validated by `bunx commitlint` against `.commitlintrc.yml`. Conventional Commits 1.0.0 with relaxed subject rules (no lowercase-start enforcement, no trailing-period enforcement).

When using `claude --worktree`, the generated hook scripts are automatically copied to the new worktree via `.worktreeinclude`. For manual `git worktree add`, run `lefthook install --force` inside the worktree.

## Pressure Tests

`tests/pressure/<skill-name>/` contains RED/GREEN scenario files. RED = behavior without skill loaded. GREEN = behavior with skill loaded. Log results in `evaluation-log.md`.

Run a scenario: open it, start a fresh Claude Code session, paste the Pressure prompt verbatim.

## Adding a New Skill

1. Create `skills/<name>/SKILL.md` with frontmatter
2. If the skill will exceed ~400 lines, plan a `reference.md` or `examples.md` split from the start
3. Add pressure test scenarios in `tests/pressure/<name>/`
4. If it's a principle skill, update `agents/principles-reviewer.md` scope
