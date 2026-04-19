# hexis

A heavily opinionated Claude Code plugin covering the full development workflow — from spec to merge.

## Quick Start

```bash
# 1. Install the plugin
/plugin install hexis --plugin-dir github:hw0k/hexis

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
| `hexis:dispatch` | Session start, resuming work, or when unsure of the next step — reads current state and routes automatically |
| `hexis:specify` | Any time a requirement, task, or idea is blurry — produces an unambiguous, actionable spec |
| `hexis:plan` | After spec is complete — produces a step-by-step implementation plan with checkboxes |
| `hexis:use-worktree` | Before executing a plan — sets up an isolated git worktree for the feature branch |
| `hexis:write-test` | Before writing implementation code — writes failing tests first (TDD gate) |
| `hexis:implement` | When a written plan exists — executes it task-by-task, subagent-first |
| `hexis:debug` | On any bug, test failure, or unexpected behavior — investigates root cause before proposing a fix |
| `hexis:verify` | Before claiming any work is complete — runs verification commands and confirms actual output |
| `hexis:review` | Before merging — runs the principles reviewer against all changes |
| `hexis:receive-review` | When review feedback arrives — technical evaluation before accepting or rejecting suggestions |
| `hexis:finish` | When implementation is verified and reviewed — commits, opens a PR, or merges |
| `hexis:sync-working-status` | To check alignment between local git, specs/plans, and remote GitHub |

### Principle Skills

Reference standards enforced across the workflow.

| Skill | Covers |
|-------|--------|
| `hexis:core-principles` | Five foundational principles (environment independence, human gate, static verification, no reinvention, prefer official methods) |
| `hexis:commit-principles` | Conventional Commits 1.0.0 — type, scope, description rules, breaking change syntax |
| `hexis:http-api-principles` | HTTP API design — Richardson Level 2, `/api/{version}/{resource}`, JSON camelCase, RFC 9457 errors |
| `hexis:exception-and-logging-principles` | Exception handling and structured logging — failure classification, log levels, correlation IDs |
| `hexis:general-naming-principles` | Language-agnostic naming conventions — follow each language's official style guide, consistency rules |

### Setup Skills

| Skill | Purpose |
|-------|---------|
| `hexis:setup-new-project` | Onboard a project — installs pre-commit hooks, configures commitlint, sets up CLAUDE.md directives |

## Agents

| Agent | Purpose |
|-------|---------|
| `hexis:principles-reviewer` | Reviews code against all five principle skills — invoked automatically by `hexis:review` |

## Install

```bash
/plugin install hexis --plugin-dir github:hw0k/hexis
```

Then run the setup skill once per project:

```bash
/hexis:setup-new-project
```

This installs git hooks (pre-commit + commitlint) and adds CLAUDE.md directives so the workflow triggers automatically.

## Design

Skills activate via the Claude Code `Skill` tool. Principle skills are referenced by `principles-reviewer` automatically. Workflow skills are invoked explicitly or triggered by CLAUDE.md directives.

Each skill lives in `skills/<name>/SKILL.md`. Large skills split into a main file and a companion `reference.md` or `examples.md`.
