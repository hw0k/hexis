# conventional-commit — Reference

Extended edge cases and examples for the `conventional-commit` skill.

## WIP Commits

WIP commits must still follow Conventional Commits format. There is no WIP exemption.

```
# Good — typed WIP
chore: wip auth flow
feat: wip add payment webhook handler

# Bad — no type
WIP
WIP: auth flow
wip: something
```

Use `chore: wip` for general work-in-progress. Use the actual type if the direction is already clear.

## Scope Examples by Context

Scopes reflect a subsystem, package, or layer — not a file name.

| Context | Good scope | Bad scope |
|---------|-----------|-----------|
| Backend service | `feat(auth):`, `fix(payments):`, `refactor(db):` | `feat(user.service.ts):` |
| Frontend app | `feat(checkout):`, `fix(navbar):` | `feat(App.tsx):` |
| Monorepo | `feat(api):`, `fix(web):`, `chore(infra):` | `feat(packages/api/src):` |
| Library | `feat(parser):`, `fix(serializer):` | `feat(index):` |

## Breaking Change Examples

**Using `!` (preferred for short explanations):**

```
feat!: remove v1 user endpoint
fix(api)!: change error response shape
```

**Using `BREAKING CHANGE:` footer (preferred for longer explanations):**

```
feat: migrate to async API

BREAKING CHANGE: all methods now return Promises. Replace synchronous
calls with await or .then() chains. See migration guide in README.
```

Both formats are valid. Use `!` for obvious breaks; use the footer when callers need migration guidance.

## Revert Commits

When using `git revert`, the generated message is exempt from format enforcement.
When writing a manual revert commit, use the `revert` type:

```
revert: remove broken payment retry logic

Refs: abc1234
```

## Multi-line Bodies

Body explains *why*, not *what*. The diff shows what changed.

```
refactor(auth): extract token validation to middleware

Token validation was duplicated across 4 route handlers. Extracting it
to middleware reduces duplication and ensures consistent error handling
across all authenticated routes.

Closes #42
```

Footer keywords: `Closes`, `Fixes`, `Refs`, `Co-Authored-By`, `BREAKING CHANGE`.
