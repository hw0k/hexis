---
name: conventional-commit
description: Enforces Conventional Commits 1.0.0 format — type, scope, description rules, breaking change syntax, and examples
type: workflow
---

# Conventional Commit Format

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Allowed Types

| Type | When to use |
|------|-------------|
| `feat` | New feature for the user |
| `fix` | Bug fix for the user |
| `docs` | Documentation only changes |
| `style` | Formatting, whitespace — no logic change |
| `refactor` | Code restructure, no feature or fix |
| `perf` | Performance improvements |
| `test` | Adding or fixing tests |
| `build` | Build system or dependency changes |
| `ci` | CI configuration changes |
| `chore` | Other maintenance (version bumps, tooling) |
| `revert` | Reverts a previous commit |

## Rules

1. **Type is required.** Choose from the list above — no others.
2. **Description is lowercase.** No capital letter at start. No period at end.
3. **Description is imperative mood.** "add feature" not "added feature" or "adding feature".
4. **Scope is optional.** Use to clarify which subsystem changed: `feat(auth): ...`, `fix(api): ...`
5. **Breaking changes** use `!` after type/scope: `feat!: remove user endpoint`
   OR add footer `BREAKING CHANGE: <description>` for a longer explanation.
6. **Body is optional.** Separate from description with a blank line. Explain *why*, not *what*.
7. **Footers are optional.** `Co-Authored-By:`, `Refs:`, `Closes:`, `BREAKING CHANGE:`

## Good Examples

```
feat(auth): add OAuth2 login flow
fix: prevent crash on empty user list
docs: update API reference for v2 endpoints
refactor(db): extract connection pool to separate module
perf(query): add index to orders table for user lookups
test: add integration tests for payment webhook handler
feat!: replace sync API with async

BREAKING CHANGE: all API methods now return Promises
```

## Bad Examples (Never Use)

```
Added new feature            ← no type, past tense
feat: Added new feature      ← uppercase + past tense
feat: new feature.           ← trailing period
FIX: bug fix                 ← uppercase type
update stuff                 ← no type, vague description
feature/add-login            ← branch name, not a commit message
```

## Enforcement Checklist

Before committing, verify:
- [ ] Type is from the allowed list
- [ ] Description starts lowercase, no trailing period
- [ ] Description uses imperative mood
- [ ] If breaking change: `!` is present OR `BREAKING CHANGE:` footer is present
- [ ] Scope (if used) is lowercase and meaningful
