# hw0k-workflow

A heavily opinionated Claude Code plugin that covers the full development workflow.

hw0k-workflow defines both workflow process and coding standards.

## Skills

| Skill | Namespace | Purpose |
|-------|-----------|---------|
| Conventional Commit | `hw0k-workflow:conventional-commit` | Enforce Conventional Commits 1.0.0 format |
| Sync Working Status | `hw0k-workflow:sync-working-status` | Sync work state across Local/GitHub |
| HTTP API Principles | `hw0k-workflow:http-api-principles` | HTTP API design standards |
| Exception Principles | `hw0k-workflow:exception-principles` | Exception handling standards |
| General Naming Principles | `hw0k-workflow:general-naming-principles` | Naming conventions |

## Commands

| Command | Purpose |
|---------|---------|
| `/hw0k-workflow:commit` | Create a commit following Conventional Commits format |
| `/hw0k-workflow:sync` | Synchronize work state across Local and GitHub |

## Agents

| Agent | Purpose |
|-------|---------|
| `principles-reviewer` | Review code against all three principle skills simultaneously |

## Install

```bash
/plugin install hw0k-workflow --plugin-dir github:hw0k/hw0k-workflow
```

## Design

Principle skills (`http-api-principles`, `exception-principles`, `general-naming-principles`) are referenced automatically by Claude when developing. Workflow skills (`conventional-commit`, `sync-working-status`) are also exposed as commands because they are user-initiated actions tied to specific development cycle events.
