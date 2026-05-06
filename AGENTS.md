# hexis

Heavily opinionated plugin covering the full development workflow — from spec to merge. Enforces consistent development standards regardless of device, agent, or tool.

## Plugin Structure

```
skills/          # User-invocable skills (hexis:<name>)
agents/          # Agent definitions (hexis:<name>)
commands/        # Slash commands
tests/pressure/  # Pressure test scenarios (RED/GREEN framework)
docs/specs/      # Design specs
docs/plans/      # Implementation plans
.githooks/       # Version-controlled git hooks (pre-commit + commitlint)
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

Flat directory only — nested skill directories are not supported.

## Git Hooks

This repo self-dogfoods its own hooks:

```bash
uvx pre-commit install
uvx pre-commit install --hook-type commit-msg
```

Run these once after cloning. Hooks install to `.git/hooks/` — no `core.hooksPath` configuration needed.

Commit messages are validated by `bunx commitlint` against `.commitlintrc.yml`. Conventional Commits 1.0.0 with relaxed subject rules (no lowercase-start enforcement, no trailing-period enforcement).

When creating a git worktree, run `uvx pre-commit install && uvx pre-commit install --hook-type commit-msg` inside the worktree.

## Pressure Tests

`tests/pressure/<skill-name>/` contains RED/GREEN scenario files. RED = behavior without skill loaded. GREEN = behavior with skill loaded. Log results in `evaluation-log.md`.

Run a scenario: open it, start a fresh Claude Code session, paste the Pressure prompt verbatim.

## Public-Facing Language

**English is the default language for all public-facing artifacts in this repository unless an explicit exception is defined.**

**Public-facing artifacts include:**
- Repository documents and markdown files
- Skill files, agent definitions, plans, specs, tests, and code comments
- Commit messages and commit history
- GitHub issues, pull requests, review comments, and discussion text
- Code identifiers, configuration keys, CLI examples, and user-facing copy stored in the repository

This includes `docs/specs/`, `docs/plans/`, `skills/`, `agents/`, and `tests/`.

**Explicit exclusions:**
- Direct chat responses to the user inside the current agent session, which follow the higher-priority session language rule
- Exact quoted text that must preserve its original language
- External interfaces that are already defined in another language and cannot be renamed safely

When in doubt, treat the artifact as public-facing and write it in English.

## Adding a New Skill

1. Create `skills/<name>/SKILL.md` with frontmatter
2. If the skill will exceed ~400 lines, plan a `reference.md` or `examples.md` split from the start
3. Add pressure test scenarios in `tests/pressure/<name>/`
4. If it's a principle skill, update `agents/principles-reviewer.md` scope
