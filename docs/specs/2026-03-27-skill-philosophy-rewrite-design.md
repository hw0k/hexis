---
status: DONE
---

# Skill Philosophy Rewrite Design

> **Historical document.** This spec reflects the design state at the time of writing. `new-project-setup` has since been renamed to `setup-new-project`.

**Date:** 2026-03-27
**Scope:** Rewrite 4 existing skills to reflect hw0k's philosophy. 3 skills remain unchanged (exception-and-logging-principles, new-project-setup, sync-working-status).

---

## Point 0 — Description Field Changes

**Decision: No change.** Claude Code matches skills semantically from description content. Adding "invoke when..." trigger phrases would mix user-facing documentation with AI-hint noise. Current descriptions are sufficient.

---

## Skill 1 — `core-principles`

### Change 1: Principle 2 (Human Gate) — Expand Irreversible Operations List

Add the following to the irreversible operations list:

**AWS resources:**
- EC2 instance termination/deletion
- S3 bucket or object deletion
- RDS instance deletion
- IAM policy modification
- VPC / Security Group modification

**Linux machine operations:**
- `rm -rf`
- `dd`
- Partition formatting
- Stopping a systemd service
- Deleting crontab entries
- Overwriting `/etc` configuration files

### Change 2: Add Principle 5 — Prefer Official Methods

**Rule:** When an official document, official API, or official convention exists for a domain, follow it. When no official source exists, follow the de facto industry standard. Apply custom interpretations or methods only where official/standard coverage does not exist.

**Rationale:** Official specifications and standards encode consensus from domain experts. Deviating from them introduces maintenance overhead, integration friction, and unverifiable correctness.

**Compliant:**
- Using MDN-documented Web API patterns
- Using the AWS official SDK for resource management
- Following RFC specs for HTTP header handling

**Non-compliant:**
- Redefining HTTP status codes beyond their specified semantics
- Implementing a custom JWT parser when a well-audited library exists
- Creating AWS resources via raw API calls instead of the official CLI or SDK

**`principles-reviewer` trigger:** Any custom implementation in a domain where an official specification, SDK, or standard library exists and covers the requirement.

---

## Skill 2 — `general-naming-principles`

### Change 1: Language-Official Conventions as Default

The skill's rules no longer override language-official conventions. Instead:

- **Python:** PEP 8 — `snake_case` for variables/functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants
- **JS/TS:** `camelCase` for variables/functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants
- **Other languages:** Follow each language's official style guide

The skill defines only rules that are language-agnostic or fill gaps not covered by official conventions.

### Change 2: Consistency Rule (Universal)

Once a term is chosen for a concept, it must be used exclusively throughout the project. If `history` is chosen, then `details`, `log`, `records` for the same concept are forbidden. Decisions are made at first use; changes require full replacement.

### Change 3: Reserved Word Prohibition (Universal)

Do not use language keywords as identifiers (`class`, `type`, `default`, `import`, etc.). When a keyword collision is unavoidable, add a prefix or suffix that communicates intent (e.g., `userType`, `itemClass`).

### Change 4: File/Directory Naming

Language/framework official convention takes priority. When none exists, default to `kebab-case`.

### Removed

Rules that duplicate or conflict with language-official conventions are removed.

---

## Skill 3 — `http-api-principles`

### Change 1: Richardson Maturity Model Positioning

Level 2 (HTTP verbs + Resources) is the target. Level 3 (HATEOAS) is explicitly out of scope — the complexity overhead exceeds the benefit for most real-world cases. State this at the top of the skill.

### Change 2: URL Signature

Mandatory structure: `/api/{version}/{resource}`

- The URL must identify itself as an API: `api.example.com/*` or `example.com/api/*` (O), `example.com/*` (X)
- URI segments: `kebab-case`
- **Core ordering principle:** segments are ordered from least-to-most frequently changing — `api` → `version` → `resource`. This is the rationale for the structure, not arbitrary convention.

### Change 3: Query Parameters

- Use `camelCase`
- API server must be case-sensitive: `status=READY` and `status=ready` are distinct values

### Change 4: Request/Response Body

- `Content-Type: application/json` required
- JSON field names: `camelCase` (following JSON community convention)
- If the backend language uses `snake_case` (e.g., Python, Go with struct tags), use a serialization-layer converter to produce `camelCase` in the API output
  - Examples: `djangorestframework-camel-case` for Django, `json:"fieldName"` struct tags for Go

### Change 5: Enum Representation

Enums must be represented as strings. `status: 1` (X), `status: "READY"` (O). Numeric enums require external reference to interpret and are therefore prohibited.

### Change 6: Error Response

Reference RFC 9457 (Problem Details for HTTP APIs). Minimum required fields: `type`, `title`, `status`, `detail`.

### Change 7: Resource-Centric Mapping

APIs represent domain resources, not database tables. Internal implementation details (table structure, join strategy) must not leak into the API surface.

Example: `GET /api/v1/orders/{id}/items` — designed as a sub-resource of `Order`, not a direct exposure of an `order_items` table.

### Change 8: Consistency

The same concept must use the same name across the entire API (aligned with general-naming-principles consistency rule).

**Reference:** [Microsoft REST API Design Guidelines](https://learn.microsoft.com/ko-kr/azure/architecture/best-practices/api-design)

---

## Skill 4 — `conventional-commit`

### Change 1: Author Language Respect

The purpose of a commit message is clear communication of intent. If the team's primary language is Korean, Korean subject and body deliver more clarity than forced English. Language rules:

- **type, scope:** English only (tool-parsed)
- **subject, body:** Author's primary language permitted

Example:
```
feat(auth): OAuth2 로그인 플로우 추가

소셜 로그인 요청이 많아 Google/Kakao OAuth2를 우선 지원.
세션 방식 대신 JWT 발급으로 stateless 유지.
```

### Change 2: Issue Prefix

When a commit is linked to a GitHub Issue tracked in a Plan or Spec, include `#{issue-number}` in the subject.

Format: `type(scope): #{issue} description`

Issue number is optional — omit when no linked issue exists.

Example:
```
feat(auth): #525 OAuth2 로그인 플로우 추가
fix(api): #312 rate limit 헤더 누락 수정
```

### Change 3: commitlint Configuration Update

Both `.commitlintrc.yml` (repo root) and `skills/new-project-setup/.commitlintrc.yml` (template) must be kept in sync. `extends` is removed — all rules are inlined to eliminate the `@commitlint/config-conventional` package dependency:

```yaml
# Inlined from @commitlint/config-conventional — no package.json required
rules:
  body-leading-blank: [1, always]
  body-max-line-length: [2, always, 100]
  footer-leading-blank: [1, always]
  footer-max-line-length: [2, always, 100]
  header-max-length: [2, always, 100]
  header-trim: [2, always]
  subject-case: [0]        # Non-English subjects (Korean, etc.) allowed
  subject-empty: [2, never]
  subject-full-stop: [0]   # No trailing period rule
  type-case: [2, always, lower-case]
  type-empty: [2, never]
  type-enum:
    - 2
    - always
    - [build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test]
```
