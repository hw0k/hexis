---
name: conventional-commit
description: Enforces Conventional Commits 1.0.0 format — type, scope, description rules, issue prefix, author language support, breaking change syntax, and examples
type: workflow
---

# Conventional Commit Format

## Format

```
<type>[optional scope]: [optional #{issue}] <description>

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
2. **Type and scope are English (ASCII).** They are tool-parsed — keep them lowercase ASCII.
3. **Description and body may be in the author's primary language.** The purpose of a commit message is clear communication of intent. A Korean description communicates more clearly than forced English for a Korean-speaking team.
4. **Description is imperative mood.** "add feature" / "기능 추가" not "added feature" / "기능을 추가했습니다".
5. **Description has no trailing period.**
6. **Scope is optional.** Use to clarify which subsystem changed: `feat(auth): ...`, `fix(api): ...`
7. **Issue prefix is optional.** When the commit is linked to a tracked issue, include `#{issue-number}` between the colon-space and the description: `feat(auth): #525 add OAuth2 login`. Omit when there is no linked issue.
8. **Breaking changes** use `!` after type/scope: `feat!: remove user endpoint`
   OR add footer `BREAKING CHANGE: <description>` for a longer explanation.
9. **Body is optional.** Separate from description with a blank line. Explain *why*, not *what*.
10. **Footers are optional.** `Co-Authored-By:`, `Refs:`, `Closes:`, `BREAKING CHANGE:`

## Good Examples

```
feat(auth): add OAuth2 login flow
feat(auth): #525 OAuth2 로그인 플로우 추가
feat(auth): OAuth2 로그인 플로우 추가
fix: prevent crash on empty user list
fix(api): #312 rate limit 헤더 누락 수정
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
feat: Added new feature      ← past tense
feat: new feature.           ← trailing period
FIX: bug fix                 ← uppercase type
update stuff                 ← no type, vague description
feature/add-login            ← branch name, not a commit message
feat: #525                   ← issue number without description
```

## Enforcement Checklist

Before committing, verify:
- [ ] Type is from the allowed list
- [ ] Type and scope are lowercase English (ASCII)
- [ ] Description is imperative mood
- [ ] No trailing period on description
- [ ] If linked to a tracked issue: `#{issue-number}` is included before the description
- [ ] If breaking change: `!` is present OR `BREAKING CHANGE:` footer is present
- [ ] Scope (if used) is lowercase and meaningful

## Extended Reference

For WIP commits, author language guidance, scope examples by project type, breaking change patterns, and revert commit guidance, see [reference.md](reference.md).
