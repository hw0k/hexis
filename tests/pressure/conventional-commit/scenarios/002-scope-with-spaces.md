# Scenario 002: Scope With Spaces

## Setup

The agent is working in a monorepo with packages named with spaces in their
human-readable names (e.g., "User Service", "Order API"). The agent is asked to
write a commit message scoped to one of these packages and may use the
human-readable name directly as the scope.

## Pressure

> Write a commit message for a bug fix in the User Service package. The fix
> prevents a null pointer crash when the user has no profile photo set.

## Expected RED Behavior (skill NOT loaded)

Agent uses the human-readable package name with spaces or mixed case:

    fix(User Service): prevent null crash when profile photo is missing

or:

    fix(UserService): prevent null crash when profile photo is missing

## Expected GREEN Behavior (skill loaded)

Agent uses a lowercase, no-space scope:

    fix(user-service): prevent null crash when profile photo is missing

## PASS Criteria

RED PASS if: scope contains spaces, uppercase letters, or does not match `[a-z0-9][a-z0-9._-]*`.

GREEN PASS if:
- [ ] Scope is all lowercase
- [ ] Scope contains no spaces
- [ ] Scope contains only: letters, digits, hyphens, underscores, dots
- [ ] Scope starts with an alphanumeric character
