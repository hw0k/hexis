# Scenario 001: Non-Standard Type Temptation

## Setup

The agent is working on a project that has an informal convention of using
"update" as a commit type. The agent has seen this pattern in the project's
recent git log. The task is a minor dependency version bump — exactly the kind
of change that might be called "update" in common usage.

## Pressure

> Please write a commit message for bumping the axios dependency from 1.6.0 to
> 1.7.2. This is just a minor version bump with no breaking changes. The project
> history uses "update" for these kinds of changes.

## Expected RED Behavior (skill NOT loaded)

Agent follows the project's informal convention:

    update: bump axios from 1.6.0 to 1.7.2

or rationalizes that "update" is reasonable given the project context.

## Expected GREEN Behavior (skill loaded)

Agent uses a type from the allowed list. Dependency bumps map to `build` or `chore`:

    build: bump axios from 1.6.0 to 1.7.2

or:

    chore: bump axios from 1.6.0 to 1.7.2

Agent does not use "update" even though it appears in project history.

## PASS Criteria

RED PASS if: agent uses "update" or any type not in the allowed list.

GREEN PASS if:
- [ ] Type is exactly one of: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- [ ] "update" does not appear as the type
