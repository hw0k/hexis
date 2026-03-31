# Scenario 003: Imperative Mood Violation

## Setup

The agent is asked to write a commit message using the developer's own words,
which are in past tense. The agent may reproduce the past tense wording
verbatim when told to use "the following description."

## Pressure

> Write a commit message using this description exactly as written:
> "fixed the null pointer crash that occurred when a user had no profile photo set"

## Expected RED Behavior (skill NOT loaded)

Agent uses the provided past tense description as-is:

    fix: fixed the null pointer crash that occurred when a user had no profile photo set

or shortens but keeps past tense:

    fix: fixed null pointer crash when user has no profile photo

## Expected GREEN Behavior (skill loaded)

Agent converts to imperative mood despite being told to use the description "exactly":

    fix: fix null pointer crash when user has no profile photo

No past tense verb form in the description.

## PASS Criteria

RED PASS if: description contains a past tense verb ("fixed", "resolved", "corrected", etc.).

GREEN PASS if:
- [ ] Description is imperative mood ("fix", "prevent", "handle", etc.)
- [ ] No past tense verb form in the subject line description
- [ ] No trailing period

## Loopholes Found

_None yet._
