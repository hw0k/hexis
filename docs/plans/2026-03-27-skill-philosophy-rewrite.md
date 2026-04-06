---
linked_spec: docs/specs/2026-03-27-skill-philosophy-rewrite-design.md
---

# Skill Philosophy Rewrite Implementation Plan

> **Historical document.** This plan reflects the initial implementation state. Some skill names have since been renamed (e.g., `conventional-commit` → `commit-principles`, `new-project-setup` → `setup-new-project`).

> **For agentic workers:** Use `hw0k-workflow:implement` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite 4 existing hw0k-workflow skills to reflect the author's philosophy — language-official conventions as default, Korean-friendly commits, Richardson Level 2 APIs, and Prefer Official Methods as a core principle.

**Architecture:** Each task targets one skill directory. Skills are independent — any order works, but the spec recommends: core-principles → general-naming-principles → http-api-principles → conventional-commit.

**Tech Stack:** Markdown skill files. No automated tests — verification is spec-compliance review after each rewrite.

**Spec:** `docs/specs/2026-03-27-skill-philosophy-rewrite-design.md`

---

### Task 1: core-principles

**Files:**
- Modify: `skills/core-principles/SKILL.md`

- [ ] **Step 1: Read current file**

```bash
cat skills/core-principles/SKILL.md
```

- [ ] **Step 2: Define spec compliance checklist (the "test")**

After rewrite, verify ALL of the following are present:

```
[ ] Principle 2 irreversible list includes AWS resources:
    - EC2 instance termination/deletion
    - S3 bucket or object deletion
    - RDS instance deletion
    - IAM policy modification
    - VPC / Security Group modification
[ ] Principle 2 irreversible list includes Linux machine operations:
    - rm -rf
    - dd
    - Partition formatting
    - Stopping a systemd service
    - Deleting crontab entries
    - Overwriting /etc configuration files
[ ] Principle 5 "Prefer Official Methods" section exists
[ ] Principle 5 includes Rule, Rationale, Compliant, Non-compliant, trigger
[ ] Frontmatter description updated to mention 5 principles including "prefer official methods"
```

- [ ] **Step 3: Apply changes to `skills/core-principles/SKILL.md`**

Update the frontmatter description:

```yaml
---
name: core-principles
description: Five foundational principles governing all hw0k-workflow standards — environment independence, human gate for irreversible operations, static verification, don't reinvent the wheel, and prefer official methods
type: reference
---
```

Replace the "What counts as irreversible" block (currently ends at "Dropping or truncating a database table or collection") with:

```markdown
**What counts as irreversible:**
- `git push --force`, `git reset --hard`, `git branch -D`
- File deletion or overwrite of a file not tracked by version control
- Any write to a remote system: deploy, publish, database mutation
- Sending an external notification: email, webhook, Slack message
- Dropping or truncating a database table or collection
- **AWS resources:** EC2 instance termination/deletion, S3 bucket or object deletion, RDS instance deletion, IAM policy modification, VPC or Security Group modification
- **Linux machine operations:** `rm -rf`, `dd`, partition formatting, stopping a running systemd service, deleting crontab entries, overwriting files in `/etc`
```

Append after Principle 4 (before the final newline):

```markdown
---

## Principle 5 — Prefer Official Methods

**Rule:** When an official document, official API, or official convention exists for a domain, follow it. When no official source exists, follow the de facto industry standard. Apply custom interpretations or methods only where official or standard coverage does not exist.

**Rationale:** Official specifications and standards encode consensus from domain experts. Deviating from them introduces maintenance overhead, integration friction, and unverifiable correctness.

**Compliant:**
- Using MDN-documented Web API patterns
- Using the AWS official SDK for resource management
- Following RFC specifications for HTTP header handling
- Using a well-audited JWT library rather than writing a custom parser

**Non-compliant:**
- Redefining HTTP status codes beyond their specified semantics
- Implementing a custom JWT parser when a well-audited library exists and covers the requirement
- Creating AWS resources via raw API calls instead of the official CLI or SDK when the SDK is available

**`principles-reviewer` trigger:** Any custom implementation in a domain where an official specification, SDK, or standard library exists and covers the requirement.
```

- [ ] **Step 4: Verify spec compliance checklist**

Read the updated file and check every item in Step 2. All must be present.

```bash
cat skills/core-principles/SKILL.md
```

- [ ] **Step 5: Commit**

```bash
git add skills/core-principles/SKILL.md
git commit -m "feat(core-principles): add AWS/Linux irreversible operations and Principle 5"
```

---

### Task 2: general-naming-principles

**Files:**
- Rewrite: `skills/general-naming-principles/SKILL.md`
- Update: `skills/general-naming-principles/examples.md`

- [ ] **Step 1: Read current files**

```bash
cat skills/general-naming-principles/SKILL.md
cat skills/general-naming-principles/examples.md
```

- [ ] **Step 2: Define spec compliance checklist**

```
[ ] Frontmatter description updated to reflect language-agnostic approach
[ ] "Language-Official Conventions First" section present with table (Python, JS/TS, Go, Java, Rust)
[ ] Existing naming rules framed as supplements, not overrides of official conventions
[ ] Consistency Rule section: once a term is chosen, use exclusively; full replacement required
[ ] Consistency example showing /orders/{id}/history vs order.activityLog mismatch
[ ] Reserved Word Prohibition section with examples in at least 2 languages
[ ] File/Directory Naming section: language/framework first, kebab-case as fallback
[ ] Test file mirroring examples in multiple languages
[ ] examples.md labels TypeScript examples as TypeScript
```

- [ ] **Step 3: Write new `skills/general-naming-principles/SKILL.md`**

```markdown
---
name: general-naming-principles
description: Language-agnostic naming conventions — follow each language's official style guide first, with universal consistency and reserved-word rules on top
type: reference
---

# General Naming Principles

## Core Rule

A name should tell the reader **what** something is or does without requiring them to look at the implementation. If a name needs a comment to explain it, rename it.

## Language-Official Conventions First

Follow each language's official style guide as the primary rule. This skill does not override official conventions — it supplements them where they have gaps.

| Language | Variables / Functions | Classes | Constants | Reference |
|---|---|---|---|---|
| Python | `snake_case` | `PascalCase` | `UPPER_SNAKE_CASE` | PEP 8 |
| JavaScript / TypeScript | `camelCase` | `PascalCase` | `UPPER_SNAKE_CASE` | MDN / TS Handbook |
| Go | `camelCase` / `PascalCase` (by visibility) | `PascalCase` | `ALL_CAPS` or `camelCase` | Effective Go |
| Java | `camelCase` | `PascalCase` | `UPPER_SNAKE_CASE` | Google Java Style |
| Rust | `snake_case` | `PascalCase` | `UPPER_SNAKE_CASE` | Rust API Guidelines |

For languages not listed, follow the language's official style guide. When no official guide exists, follow the dominant community convention.

## Universal Rules (Language-Agnostic)

These apply in every language, supplementing the official convention.

### Descriptive Names

Names must communicate what something is or does. Abbreviations are prohibited unless universally recognized in the domain (`url`, `id`, `api`, `db`, `ctx`, `err`).

```python
# Python — Good
user_list = fetch_users()
is_authenticated = check_auth(token)
retry_count = 0

# Python — Bad
ul = fetch_users()
auth = check_auth(token)   # ambiguous: result? flag? service?
n = 0
```

```typescript
// TypeScript — Good
const userList = await fetchUsers()
const isAuthenticated = checkAuth(token)
const retryCount = 0

// TypeScript — Bad
const ul = await fetchUsers()
const auth = checkAuth(token)
const n = 0
```

### Boolean Prefix

Boolean variables and functions use a predicate prefix: `is`, `has`, `can`, `should`.

```python
is_active, has_permission, can_delete, should_retry   # Python
```
```typescript
isActive, hasPermission, canDelete, shouldRetry       // TypeScript
```

### Consistency

Once a term is chosen for a concept, use it exclusively across the entire project. If `history` is chosen, then `details`, `log`, `records` for the same concept are forbidden.

- Decisions are made at first use
- Changes require full replacement — no partial migrations
- Applies to: variable names, field names, URL segments, database column names, event names

```
# Bad — same concept, three different names
GET /orders/{id}/history   (API endpoint)
order.activityLog          (field name)
getOrderRecords()          (function name)

# Good — consistent term throughout
GET /orders/{id}/history
order.history
getOrderHistory()
```

### Reserved Word Prohibition

Do not use language keywords as identifiers. When a keyword collision is unavoidable, add a prefix or suffix that communicates intent.

```python
# Python — Bad
type = "admin"        # shadows built-in
class = "premium"     # SyntaxError

# Python — Good
user_type = "admin"
user_class = "premium"
```

```typescript
// TypeScript — Bad
const type = "admin"      // conflicts with built-in type keyword
const class = "premium"   // SyntaxError

// TypeScript — Good
const userType = "admin"
const userClass = "premium"
```

## File and Directory Naming

Language or framework convention takes priority. When none exists, default to `kebab-case`.

| Language / Ecosystem | Convention | Example |
|---|---|---|
| Python | `snake_case` | `user_service.py` |
| JavaScript / TypeScript | `kebab-case` | `user-service.ts` |
| Go | `snake_case` | `user_service.go` |
| Java | `PascalCase` | `UserService.java` |

Test files mirror the source path and name, using the language convention for test suffixes:
- Python: `user_service.py` → `test_user_service.py`
- TypeScript: `user-service.ts` → `user-service.test.ts`
- Go: `user_service.go` → `user_service_test.go`
- Java: `UserService.java` → `UserServiceTest.java`

## Functions and Methods

- **Verb + noun**: `createUser`, `fetchOrders`, `validateEmail`, `calculateTotal`
- **Query functions** (return values, no side effects): `getUser`, `findById`, `calculateTotal`
- **Command functions** (side effects): `saveUser`, `deleteOrder`, `sendEmail`
- **Boolean functions** use predicate form: `isValid`, `hasExpired`, `canAccess`
- Async functions do not need an `async` prefix — the return type communicates it

## Classes, Types, and Interfaces

- `PascalCase` in all languages that have class constructs
- No `I` prefix for interfaces: `UserRepository` not `IUserRepository`
- No `Abstract` prefix: `BaseRepository` not `AbstractRepository`
- Suffix communicates role: `UserService`, `UserRepository`, `UserController`, `UserError`, `UserEvent`, `UserDto`

## Packages and Modules

- Follow language convention (see table above)
- **Domain-specific, not generic** — avoid `utils`, `helpers`, `common`, `shared`
  - ✅ `user_validation.py` not `utils.py`
  - ✅ `date-formatter.ts` not `helpers.ts`
- If you find yourself reaching for a `utils` file, ask whether the function belongs in the domain module that uses it most.

## Extended Examples

For before/after naming comparisons by language and class/interface examples, see [examples.md](examples.md).
```

- [ ] **Step 4: Update `skills/general-naming-principles/examples.md`**

Replace the existing content with:

```markdown
# general-naming-principles — Examples

Extended examples for the `general-naming-principles` skill.

## Variable Naming: Before/After (TypeScript)

| Before | After | Why |
|--------|-------|-----|
| `const u = await getUser()` | `const user = await getUser()` | Single letter hides type |
| `const flg = isActive()` | `const isActive = checkIsActive()` | Abbreviation + no boolean prefix |
| `const mgr = new SessionManager()` | `const sessionManager = new SessionManager()` | `mgr` is an unclear abbreviation |
| `const d = new Date()` | `const createdAt = new Date()` | Context-free single letter |
| `let cnt = 0` | `let retryCount = 0` | Abbreviation hides meaning |

## Variable Naming: Before/After (Python)

| Before | After | Why |
|--------|-------|-----|
| `u = get_user()` | `user = get_user()` | Single letter hides type |
| `flg = is_active()` | `is_active = check_is_active()` | Abbreviation + no boolean prefix |
| `mgr = SessionManager()` | `session_manager = SessionManager()` | `mgr` is unclear |
| `d = datetime.now()` | `created_at = datetime.now()` | Context-free single letter |
| `cnt = 0` | `retry_count = 0` | Abbreviation hides meaning |

## Function Naming: Before/After (TypeScript)

| Before | After | Why |
|--------|-------|-----|
| `function processUser(u)` | `function activateUser(user)` | "process" is meaningless |
| `async function asyncFetchOrders()` | `async function fetchOrders()` | `async` prefix is redundant |
| `function check(email)` | `function isValidEmail(email)` | Too vague; boolean needs predicate form |
| `function doPayment(order)` | `function chargeOrder(order)` | "do" is meaningless |
| `function handleError(e)` | `function logAndRethrow(error)` | Name should describe the action |

## Class and Interface Naming (TypeScript)

```typescript
// Good
class UserService {}           // business logic
class UserRepository {}        // data access
class UserController {}        // HTTP handler
class UserNotFoundError {}     // domain error
class UserCreatedEvent {}      // event type
class CreateUserDto {}         // data transfer object

// Bad
interface IUserRepository {}   // no I prefix
abstract class AbstractRepo {} // no Abstract prefix
class UserManager {}           // Manager is vague
class UserHelper {}            // Helper is vague
```

## File Naming Examples

```
# TypeScript — kebab-case, named for primary export
user-service.ts          → exports UserService
order-repository.ts      → exports OrderRepository
user-service.test.ts     ← mirrors user-service.ts

# Python — snake_case
user_service.py          → exports UserService
test_user_service.py     ← mirrors user_service.py

# Go — snake_case
user_service.go
user_service_test.go     ← mirrors user_service.go

# Java — PascalCase
UserService.java
UserServiceTest.java     ← mirrors UserService.java
```

## Consistency: Good vs. Bad

```
# Bad — same concept, different names across the codebase
GET /orders/{id}/history     (API endpoint)
order.activityLog            (model field)
getOrderRecords()            (function name)
order_details table          (DB table)

# Good — "history" used consistently
GET /orders/{id}/history
order.history
getOrderHistory()
order_history table
```

## Constants: SCREAMING_SNAKE vs camelCase (TypeScript)

```typescript
// SCREAMING_SNAKE_CASE: compile-time, never reassigned, module-level
const MAX_RETRY_COUNT = 3
const DEFAULT_PAGE_SIZE = 20
const SESSION_EXPIRY_SECONDS = 3600

// camelCase: runtime-determined (env vars, config loaded at startup)
const databaseUrl = process.env.DATABASE_URL
const jwtSecret = config.get('jwt.secret')
```

## Constants (Python)

```python
# UPPER_SNAKE_CASE: module-level constants per PEP 8
MAX_RETRY_COUNT = 3
DEFAULT_PAGE_SIZE = 20
SESSION_EXPIRY_SECONDS = 3600

# Runtime-determined — still UPPER_SNAKE_CASE in Python (PEP 8)
DATABASE_URL = os.environ["DATABASE_URL"]
JWT_SECRET = config.get("jwt.secret")
```
```

- [ ] **Step 5: Verify spec compliance checklist**

Read both files and check every item in Step 2.

```bash
cat skills/general-naming-principles/SKILL.md
cat skills/general-naming-principles/examples.md
```

- [ ] **Step 6: Commit**

```bash
git add skills/general-naming-principles/SKILL.md skills/general-naming-principles/examples.md
git commit -m "feat(general-naming): language-official conventions first, add consistency and reserved-word rules"
```

---

### Task 3: http-api-principles

**Files:**
- Rewrite: `skills/http-api-principles/SKILL.md`
- Rewrite: `skills/http-api-principles/examples.md`

- [ ] **Step 1: Read current files**

```bash
cat skills/http-api-principles/SKILL.md
cat skills/http-api-principles/examples.md
```

- [ ] **Step 2: Define spec compliance checklist**

```
[ ] Frontmatter description updated
[ ] Richardson Level 2 target stated; Level 3 explicitly out of scope
[ ] URL signature /api/{version}/{resource} required
[ ] "URL must identify itself as an API" rule with examples
[ ] URL ordering principle (least-to-most frequently changing) stated
[ ] URI segments kebab-case
[ ] Query parameters camelCase
[ ] API server case-sensitive note
[ ] Content-Type: application/json required
[ ] JSON field names camelCase
[ ] snake_case backend → camelCase converter required (with examples for Python/Go/Spring)
[ ] Enum as strings (not integers) — with bad/good example
[ ] Error response references RFC 9457 with type/title/status/detail fields
[ ] Resource-centric mapping section (not table-centric)
[ ] Consistency section cross-referencing general-naming-principles
[ ] Microsoft REST API Guidelines reference link
[ ] examples.md URLs all use /api/v1/... signature
[ ] examples.md error responses use RFC 9457 format
[ ] examples.md includes enum example
[ ] examples.md includes query parameter example
```

- [ ] **Step 3: Write new `skills/http-api-principles/SKILL.md`**

```markdown
---
name: http-api-principles
description: Opinionated HTTP API design standards — Richardson Level 2, /api/{version}/{resource} URL signature, JSON camelCase, RFC 9457 errors, and resource-centric modeling
type: reference
---

# HTTP API Design Principles

## Maturity Target

Target **Richardson Maturity Model Level 2** — HTTP verbs and resources. Level 3 (HATEOAS) is explicitly out of scope; complexity overhead exceeds practical benefit for most production APIs.

## URL Structure

**Required signature:** `/api/{version}/{resource}`

- The URL must identify itself as an API:
  - ✅ `api.example.com/v1/users`
  - ✅ `booking-api.example.com/v1/orders`
  - ✅ `example.com/api/v1/users`
  - ❌ `example.com/users` — not identifiable as an API from the URL alone
- **Ordering principle:** segments go from least-to-most frequently changing — `api` → `version` → `resource`. This is the rationale for the structure, not arbitrary convention.
- URI segments: **kebab-case**
- Nest to show ownership, max 2 levels deep: `/api/v1/orders/{id}/items`
- Use **plural nouns** for collections: `/users`, `/orders`, `/products`
- **Never use verbs in URLs:**
  - ❌ `/api/v1/getUser`, `/api/v1/createOrder`
  - ✅ `GET /api/v1/users/{id}`, `POST /api/v1/orders`
- IDs belong in the path, not the query: `/api/v1/users/{userId}` not `/api/v1/users?id={userId}`

## Query Parameters

- Use **camelCase**: `?pageSize=20`, `?sortBy=createdAt`, `?includeArchived=true`
- API server must be **case-sensitive**: `?status=READY` and `?status=ready` are distinct values
- Boolean params: `true` / `false` strings

## HTTP Methods

| Method | Use case | Idempotent | Request body |
|--------|----------|------------|--------------|
| `GET` | Fetch resource(s) | Yes | No |
| `POST` | Create a resource | No | Yes |
| `PUT` | Replace resource entirely | Yes | Yes |
| `PATCH` | Partial update | No | Yes |
| `DELETE` | Remove resource | Yes | No |

Rules:
- Never use `POST` where `PUT` or `PATCH` belongs
- Never use `GET` for mutations — even if it feels convenient
- `PUT` replaces the full resource; `PATCH` updates specific fields

## Request/Response Body

- `Content-Type: application/json` required on all requests and responses with a body
- JSON field names: **camelCase** (`userId`, `createdAt`, `orderItems`)
- If the backend language uses `snake_case`, convert at the serialization layer:
  - Python/Django: `djangorestframework-camel-case`
  - Go: `json:"fieldName"` struct tags
  - Spring Boot: `spring.jackson.property-naming-strategy=LOWER_CAMEL_CASE`
- Dates in ISO 8601 UTC: `"2026-03-27T10:00:00Z"`
- Never expose internal database IDs as the primary public identifier — use UUIDs or opaque IDs

## Enum Values

Represent enums as **strings**, not integers.

- ❌ `"status": 1` — requires external reference to interpret
- ✅ `"status": "READY"` — self-documenting

## Status Codes

| Code | Meaning | When to use |
|------|---------|-------------|
| `200` | OK | Successful GET, PUT, PATCH with response body |
| `201` | Created | Successful POST that created a resource |
| `204` | No Content | Successful DELETE, or PATCH/PUT with no response body |
| `400` | Bad Request | Malformed input, validation error |
| `401` | Unauthorized | Missing or invalid authentication token |
| `403` | Forbidden | Authenticated but lacks permission for this resource |
| `404` | Not Found | Resource does not exist |
| `409` | Conflict | Duplicate resource, optimistic lock conflict |
| `422` | Unprocessable Entity | Syntactically valid but semantically invalid |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Unexpected server-side failure |

Never use `200` for errors. Never use `500` for client errors.

## Error Response Format

Follow **RFC 9457 (Problem Details for HTTP APIs)**. Minimum required fields:

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The request contains invalid fields.",
  "errors": [
    { "field": "email", "message": "must not be blank" }
  ]
}
```

- `type`: URI identifying the error class (absolute URL or relative path)
- `title`: human-readable summary, same for all instances of this error type
- `status`: HTTP status code as integer
- `detail`: human-readable explanation of this specific occurrence
- Additional members allowed (e.g., `errors` for field-level details)

Never expose stack traces, internal error codes, or database error messages.

## Resource-Centric Mapping

APIs represent **domain resources**, not database tables. Internal implementation details (table structure, JOIN strategy, column names) must not leak into the API surface.

- ✅ `GET /api/v1/orders/{id}/items` — `items` is a sub-resource of `Order`
- ❌ Exposing an `order_items` table directly with DB column names as field names

Design the API around the domain model. The database is an implementation detail.

## Consistency

The same concept must use the same name across the entire API. Align with the `general-naming-principles` consistency rule.

```
# Bad — same concept, inconsistent names
GET /api/v1/orders?userId=123
GET /api/v1/products?user_id=123   ← inconsistent field name AND casing

# Good
GET /api/v1/orders?userId=123
GET /api/v1/products?userId=123
```

## Versioning

- Version in the URL path as part of the required signature: `/api/v1/...`
- Increment major version only for **breaking changes** (removed fields, changed semantics)
- Keep old versions alive for at least one deprecation cycle
- Advertise deprecation with response headers:
  ```
  Deprecation: true
  Sunset: Sat, 01 Jan 2028 00:00:00 GMT
  ```

## Pagination

Use cursor-based pagination for all list endpoints:

```json
{
  "data": [ ... ],
  "pagination": {
    "cursor": "eyJpZCI6MTIzfQ==",
    "hasMore": true,
    "limit": 20
  }
}
```

- Default page size: 20
- Maximum page size: 100
- Reject requests with `limit > 100` with a `400`
- Never return unbounded collections — all list endpoints must be paginated

## Reference

[Microsoft REST API Design Guidelines](https://learn.microsoft.com/ko-kr/azure/architecture/best-practices/api-design)

## Extended Examples

For URL structure examples, error response variations, enum and query parameter examples, pagination examples, and status code decision guide, see [examples.md](examples.md).
```

- [ ] **Step 4: Write new `skills/http-api-principles/examples.md`**

```markdown
# http-api-principles — Examples

Extended examples for the `http-api-principles` skill.

## URL Structure Examples

```
# Single resource
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
DELETE /api/v1/users/{id}

# Collection
GET  /api/v1/users
POST /api/v1/users

# Nested (max 2 levels)
GET  /api/v1/users/{id}/orders
POST /api/v1/users/{id}/orders
GET  /api/v1/users/{id}/orders/{orderId}

# kebab-case multi-word resources
GET  /api/v1/user-profiles
GET  /api/v1/order-items/{id}

# Action on resource (POST + noun path when no REST method fits)
POST /api/v1/users/{id}/password-reset
POST /api/v1/orders/{id}/cancellation
```

## Query Parameter Examples

```
# camelCase, case-sensitive
GET /api/v1/orders?pageSize=20&sortBy=createdAt&includeArchived=false
GET /api/v1/products?categoryId=42&status=ACTIVE
GET /api/v1/users?cursor=eyJpZCI6MTIzfQ==&pageSize=20

# status=ACTIVE and status=active are different values — server is case-sensitive
```

## Enum Examples

```json
// Bad — requires external reference to interpret the integer values
{ "status": 1, "priority": 3 }

// Good — self-documenting
{ "status": "ACTIVE", "priority": "HIGH" }
```

## Error Response Examples (RFC 9457)

**400 Validation Error (multiple fields):**
```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The request contains invalid fields.",
  "errors": [
    { "field": "email", "message": "must not be blank" },
    { "field": "email", "message": "must be a valid email address" },
    { "field": "age", "message": "must be at least 18" }
  ]
}
```

**404 Not Found:**
```json
{
  "type": "https://api.example.com/errors/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "No user exists with the given ID."
}
```

**401 Unauthorized:**
```json
{
  "type": "https://api.example.com/errors/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "The provided authentication token is invalid or has expired."
}
```

**500 Internal Server Error (never expose internals):**
```json
{
  "type": "https://api.example.com/errors/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred. Please try again later."
}
```

## Pagination Examples

**Request:**
```
GET /api/v1/orders?pageSize=20&cursor=eyJpZCI6MTIzfQ==
```

**Response:**
```json
{
  "data": [
    { "id": "ord_124", "status": "SHIPPED", "createdAt": "2026-03-27T10:00:00Z" },
    { "id": "ord_123", "status": "DELIVERED", "createdAt": "2026-03-26T08:30:00Z" }
  ],
  "pagination": {
    "cursor": "eyJpZCI6MTIzfQ==",
    "hasMore": false,
    "limit": 20
  }
}
```

**Reject over-limit:**
```
GET /api/v1/orders?pageSize=500
→ 400 Bad Request

{
  "type": "https://api.example.com/errors/invalid-pagination",
  "title": "Invalid Pagination",
  "status": 400,
  "detail": "pageSize must not exceed 100.",
  "errors": [{ "field": "pageSize", "message": "must be at most 100" }]
}
```

## Versioning and Deprecation Headers

```
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 01 Jan 2028 00:00:00 GMT
Link: <https://api.example.com/api/v2/users>; rel="successor-version"
```

## Status Code Decision Guide

| Situation | Code |
|-----------|------|
| GET success with body | 200 |
| POST created resource | 201 |
| DELETE success / PUT with no body | 204 |
| Missing required field | 400 |
| Invalid format | 400 |
| No auth token | 401 |
| Valid token, wrong permissions | 403 |
| Resource not found | 404 |
| Duplicate resource | 409 |
| Syntactically valid but semantically wrong | 422 |
| Rate limit | 429 |
| Unexpected server failure | 500 |
| Downstream dependency unavailable | 503 |
```

- [ ] **Step 5: Verify spec compliance checklist**

```bash
cat skills/http-api-principles/SKILL.md
cat skills/http-api-principles/examples.md
```

Check every item in Step 2.

- [ ] **Step 6: Commit**

```bash
git add skills/http-api-principles/SKILL.md skills/http-api-principles/examples.md
git commit -m "feat(http-api): Richardson L2 positioning, URL signature, RFC 9457, resource-centric design"
```

---

### Task 4: conventional-commit

**Files:**
- Modify: `skills/conventional-commit/SKILL.md`
- Update: `skills/conventional-commit/reference.md`

- [ ] **Step 1: Read current files**

```bash
cat skills/conventional-commit/SKILL.md
cat skills/conventional-commit/reference.md
```

- [ ] **Step 2: Define spec compliance checklist**

```
[ ] Rules section: type/scope must be English, description/body may be author's primary language
[ ] Rationale for language rule stated (purpose = clear communication of intent)
[ ] Issue prefix rule: #{issue-number} after ": " when linked to a tracked issue, optional
[ ] Format example showing issue prefix: "feat(auth): #525 OAuth2 로그인 플로우 추가"
[ ] Korean commit example in Good Examples section
[ ] Rule 2 (description lowercase) updated — no longer enforces English-only
[ ] Enforcement checklist updated to reflect new rules
[ ] reference.md: WIP section shows Korean example
[ ] reference.md: Author Language section added
```

- [ ] **Step 3: Write new `skills/conventional-commit/SKILL.md`**

```markdown
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

For WIP commits, scope examples by project type, breaking change patterns, and revert commit guidance, see [reference.md](reference.md).
```

- [ ] **Step 4: Update `skills/conventional-commit/reference.md`**

Add an "Author Language" section at the top (after the title/intro), and update the WIP section to include a Korean example:

Insert after the first line (`# conventional-commit — Reference` and intro):

```markdown
## Author Language

Type and scope are English — they are parsed by tools (commitlint, changelog generators). Everything else may be in the team's primary language.

```
# English team
feat(auth): add OAuth2 login flow
fix(api): fix rate limit header missing

# Korean team — equally valid
feat(auth): OAuth2 로그인 플로우 추가
fix(api): rate limit 헤더 누락 수정

# Mixed (scope stays English, description in Korean)
feat(auth): #525 소셜 로그인 Google/Kakao 지원 추가

# Body in Korean — fully valid
feat(auth): OAuth2 로그인 플로우 추가

소셜 로그인 요청이 많아 Google/Kakao OAuth2를 우선 지원.
세션 방식 대신 JWT 발급으로 stateless 유지.
```
```

Also update the WIP section to add a Korean example:

```markdown
## WIP Commits

WIP commits must still follow Conventional Commits format. There is no WIP exemption.

```
# Good — typed WIP (English)
chore: wip auth flow
feat: wip add payment webhook handler

# Good — typed WIP (Korean)
chore: wip 인증 플로우
feat: wip 결제 웹훅 핸들러 추가

# Bad — no type
WIP
WIP: auth flow
wip: something
```

Use `chore: wip` for general work-in-progress. Use the actual type if the direction is already clear.
```

- [ ] **Step 5: Verify spec compliance checklist**

```bash
cat skills/conventional-commit/SKILL.md
cat skills/conventional-commit/reference.md
```

Check every item in Step 2.

- [ ] **Step 6: Commit**

```bash
git add skills/conventional-commit/SKILL.md skills/conventional-commit/reference.md
git commit -m "feat(conventional-commit): allow author language and add issue prefix rule"
```
