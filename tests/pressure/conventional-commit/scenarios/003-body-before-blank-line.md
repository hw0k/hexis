# Scenario 003: Body Without Blank Line Separator

## Setup

The agent is writing a commit with a body explaining the reasoning behind a
refactor. The agent is focused on the content of the explanation and may omit
the required blank line between the subject and body.

## Pressure

> Write a commit message for a refactoring that extracts the database connection
> pool into a separate module. The reason is that three different services were
> each creating their own pools, causing resource exhaustion under load. Please
> include a brief explanation of why this was done.

## Expected RED Behavior (skill NOT loaded)

Agent writes a commit without a blank line separating subject from body:

    refactor(db): extract connection pool to separate module
    Three services were creating independent pools, causing resource exhaustion
    under load. Centralizing pool creation reduces connection overhead.

## Expected GREEN Behavior (skill loaded)

Agent separates subject from body with exactly one blank line:

    refactor(db): extract connection pool to separate module

    Three services were creating independent pools, causing resource exhaustion
    under load. Centralizing pool creation reduces connection overhead.

## PASS Criteria

RED PASS if: body follows immediately after subject line with no blank line.

GREEN PASS if:
- [ ] There is exactly one blank line between the subject line and the body
- [ ] Subject line is valid Conventional Commits format
- [ ] Body starts on the third line (line 1: subject, line 2: blank, line 3+: body)
