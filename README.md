# hw0k-workflow

A heavily opinionated Claude Code plugin covering the full development workflow — from spec to merge.

## Skills

### Workflow Skills

| Skill | Purpose |
|-------|---------|
| `hw0k-workflow:specify` | Turn blurry inputs into precise, actionable specs |
| `hw0k-workflow:plan` | Write detailed implementation plans from specs |
| `hw0k-workflow:implement` | Execute implementation plans (subagent-first) |
| `hw0k-workflow:use-worktree` | Set up isolated git worktree for feature work |
| `hw0k-workflow:write-test` | TDD — write failing tests before implementation |
| `hw0k-workflow:debug` | Systematic root cause investigation before fixing |
| `hw0k-workflow:verify` | Evidence-based completion verification |
| `hw0k-workflow:review` | Principles review gate before merge |
| `hw0k-workflow:receive-review` | Technical evaluation of review feedback |
| `hw0k-workflow:finish` | Branch completion — commit, PR, or merge |

### Principle Skills

| Skill | Purpose |
|-------|---------|
| `hw0k-workflow:core-principles` | Five foundational principles (P1–P5) |
| `hw0k-workflow:commit-principles` | Conventional Commits 1.0.0 enforcement |
| `hw0k-workflow:http-api-principles` | HTTP API design standards |
| `hw0k-workflow:exception-and-logging-principles` | Exception handling and logging standards |
| `hw0k-workflow:general-naming-principles` | Naming conventions |

### Setup Skills

| Skill | Purpose |
|-------|---------|
| `hw0k-workflow:new-project-setup` | Onboard a project — lefthook, commitlint, git hooks |

## Agents

| Agent | Purpose |
|-------|---------|
| `hw0k-workflow:principles-reviewer` | Review code against all five principle skills |

## Install

```bash
/plugin install hw0k-workflow --plugin-dir github:hw0k/hw0k-workflow
```

## Project CLAUDE.md Setup

For hw0k-workflow skills to activate automatically, add this directive to your project or global `CLAUDE.md`:

```markdown
## hw0k-workflow

Any task that matches a hw0k-workflow skill MUST use it. Check before responding.

| Situation | Skill |
|---|---|
| Requirement or task is vague | `hw0k-workflow:specify` |
| Need an implementation plan | `hw0k-workflow:plan` |
| Writing code | `hw0k-workflow:write-test` |
| Debugging | `hw0k-workflow:debug` |
| Claiming completion | `hw0k-workflow:verify` |
| Before merge | `hw0k-workflow:review` |
| Receiving review feedback | `hw0k-workflow:receive-review` |
| Branch done | `hw0k-workflow:finish` |
```

For git hooks and commitlint setup, run `hw0k-workflow:new-project-setup`.

## Design

Skills activate via the Claude Code `Skill` tool. Principle skills are referenced by `principles-reviewer` automatically. Workflow skills are invoked explicitly or triggered by CLAUDE.md directives.
