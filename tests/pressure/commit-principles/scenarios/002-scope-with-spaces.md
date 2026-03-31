# Scenario 002: Scope With Spaces

## Setup

The agent is working in a monorepo where packages have human-readable names with
spaces (e.g., "User Service", "Order API"). The agent is explicitly told to use
the package name as the commit scope.

## Pressure

> Write a commit message for a bug fix in the "User Service" package. The fix
> prevents a null pointer crash when the user has no profile photo set.
> Make sure to include the package name as the commit scope.

## Expected RED Behavior (skill NOT loaded)

Agent uses the human-readable package name directly as the scope:

    fix(User Service): prevent null pointer crash when profile photo is not set

or uses PascalCase without spaces:

    fix(UserService): prevent null pointer crash when profile photo is not set

## Expected GREEN Behavior (skill loaded)

Agent converts the package name to a valid lowercase, no-space scope:

    fix(user-service): prevent null pointer crash when profile photo is not set

## PASS Criteria

RED PASS if: scope contains spaces, uppercase letters, or does not match `[a-z0-9][a-z0-9._-]*`.

GREEN PASS if:
- [ ] Scope is all lowercase
- [ ] Scope contains no spaces
- [ ] Scope contains only: letters, digits, hyphens, underscores, dots
- [ ] Scope starts with an alphanumeric character
