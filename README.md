# hw0k-workflow

A heavily opinionated Claude Code plugin covering the full development workflow — from spec to merge.

## Quick Start

```bash
# 1. Install the plugin
/plugin install hw0k-workflow --plugin-dir github:hw0k/claude-hw0k-workflow

# 2. Onboard your project (run once per repo)
/setup-new-project

# 3. Start working — let dispatch route you
/dispatch
```

> **Tip:** When in doubt, run `dispatch`. It reads your current state and invokes the right skill automatically.

## Workflow

Skills follow a linear flow. Each skill hands off to the next.

```
specify → plan → [use-worktree] → write-test → implement → verify → review → finish
```

| Situation | Skill to invoke |
|-----------|----------------|
| Unsure of next step / resuming work | `dispatch` |
| Requirement or task is vague | `specify` |
| Need an implementation plan | `plan` |
| Starting feature work in isolation | `use-worktree` |
| Writing code (TDD) | `write-test` |
| Executing an implementation plan | `implement` |
| Debugging a failure | `debug` |
| Claiming work is done | `verify` |
| Before merging | `review` |
| Received code review feedback | `receive-review` |
| Branch is complete | `finish` |

## Skills

### Workflow Skills

| Skill | When to use |
|-------|-------------|
| `hw0k-workflow:dispatch` | Session start, resuming work, or when unsure of the next step — reads current state and routes automatically |
| `hw0k-workflow:specify` | Any time a requirement, task, or idea is blurry — produces an unambiguous, actionable spec |
| `hw0k-workflow:plan` | After spec is complete — produces a step-by-step implementation plan with checkboxes |
| `hw0k-workflow:use-worktree` | Before executing a plan — sets up an isolated git worktree for the feature branch |
| `hw0k-workflow:write-test` | Before writing implementation code — writes failing tests first (TDD gate) |
| `hw0k-workflow:implement` | When a written plan exists — executes it task-by-task, subagent-first |
| `hw0k-workflow:debug` | On any bug, test failure, or unexpected behavior — investigates root cause before proposing a fix |
| `hw0k-workflow:verify` | Before claiming any work is complete — runs verification commands and confirms actual output |
| `hw0k-workflow:review` | Before merging — runs the principles reviewer against all changes |
| `hw0k-workflow:receive-review` | When review feedback arrives — technical evaluation before accepting or rejecting suggestions |
| `hw0k-workflow:finish` | When implementation is verified and reviewed — commits, opens a PR, or merges |
| `hw0k-workflow:sync-working-status` | To check alignment between local git, specs/plans, and remote GitHub |

### Principle Skills

Reference standards enforced across the workflow.

| Skill | Covers |
|-------|--------|
| `hw0k-workflow:core-principles` | Five foundational principles (environment independence, human gate, static verification, no reinvention, prefer official methods) |
| `hw0k-workflow:commit-principles` | Conventional Commits 1.0.0 — type, scope, description rules, breaking change syntax |
| `hw0k-workflow:http-api-principles` | HTTP API design — Richardson Level 2, `/api/{version}/{resource}`, JSON camelCase, RFC 9457 errors |
| `hw0k-workflow:exception-and-logging-principles` | Exception handling and structured logging — failure classification, log levels, correlation IDs |
| `hw0k-workflow:general-naming-principles` | Language-agnostic naming conventions — follow each language's official style guide, consistency rules |

### Setup Skills

| Skill | Purpose |
|-------|---------|
| `hw0k-workflow:setup-new-project` | Onboard a project — installs pre-commit hooks, configures commitlint, sets up CLAUDE.md directives |

## Agents

| Agent | Purpose |
|-------|---------|
| `hw0k-workflow:principles-reviewer` | Reviews code against all five principle skills — invoked automatically by `hw0k-workflow:review` |

## Install

```bash
/plugin install hw0k-workflow --plugin-dir github:hw0k/claude-hw0k-workflow
```

Then run the setup skill once per project:

```bash
/hw0k-workflow:setup-new-project
```

This installs git hooks (pre-commit + commitlint) and adds CLAUDE.md directives so the workflow triggers automatically.

## Design

Skills activate via the Claude Code `Skill` tool. Principle skills are referenced by `principles-reviewer` automatically. Workflow skills are invoked explicitly or triggered by CLAUDE.md directives.

Each skill lives in `skills/<name>/SKILL.md`. Large skills split into a main file and a companion `reference.md` or `examples.md`.
