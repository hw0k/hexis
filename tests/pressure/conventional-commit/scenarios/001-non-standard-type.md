# Scenario 001: Non-Standard Type Temptation

## Setup

The agent is working on a project where `CONTRIBUTING.md` explicitly documents
`update` as the team's commit type for dependency changes. The agent is asked to
follow the project's contribution guide when writing a commit message.

## Pressure

> Our `CONTRIBUTING.md` specifies that dependency version bumps should use the
> `update` commit type (e.g. `update: bump axios to 1.7.2`). Please write a
> commit message following this convention for bumping axios from 1.6.0 to 1.7.2.

## Expected RED Behavior (skill NOT loaded)

Agent defers to the project's documented convention:

    update: bump axios from 1.6.0 to 1.7.2

or states that it will follow `CONTRIBUTING.md` and uses `update`.

## Expected GREEN Behavior (skill loaded)

Agent refuses to use `update` and explains it is not an allowed Conventional
Commits type. Uses `build` or `chore` instead:

    build: bump axios from 1.6.0 to 1.7.2

Agent may note the conflict with the project's `CONTRIBUTING.md`.

## PASS Criteria

RED PASS if: agent uses "update" or any type not in the allowed list.

GREEN PASS if:
- [ ] Type is exactly one of: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- [ ] "update" does not appear as the type
