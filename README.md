# hw0k-workflow

A heavily opinionated Claude Code plugin covering the full development workflow — from spec to merge.

## Skills

### Workflow Skills

| Skill | Purpose |
|-------|---------|
| `hw0k-workflow:dispatch` | State-aware router — detects workflow position and invokes the correct next skill |
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
| `hw0k-workflow:setup-new-project` | Onboard a project — lefthook, commitlint, git hooks |

## Agents

| Agent | Purpose |
|-------|---------|
| `hw0k-workflow:principles-reviewer` | Review code against all five principle skills |

## Install

```bash
/plugin install hw0k-workflow --plugin-dir github:hw0k/hw0k-workflow
```

## Setup

Run `hw0k-workflow:setup-new-project` after installing. It configures git hooks, commitlint, and CLAUDE.md directives for the current project.

## Design

Skills activate via the Claude Code `Skill` tool. Principle skills are referenced by `principles-reviewer` automatically. Workflow skills are invoked explicitly or triggered by CLAUDE.md directives.
