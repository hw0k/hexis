---
linked_spec: docs/specs/2026-03-27-hw0k-workflow-enhancement-design.md
---

# hw0k-workflow Enhancement — Content Plan

> **Historical document.** This plan reflects the initial implementation state. Some skill names have since been renamed (e.g., `conventional-commit` → `commit-principles`, `new-project-setup` → `setup-new-project`).

> **For agentic workers:** Use `hw0k-workflow:implement` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the content layer of the hw0k-workflow enhancement — pressure tests, skill refactoring, new skills, and agent updates — as defined in `docs/specs/2026-03-27-hw0k-workflow-enhancement-design.md`.

**Architecture:** All deliverables are markdown files. No executable code. Each task produces standalone markdown content that is verified against the spec checklist before committing. The infrastructure layer (lefthook, new-project-setup) is handled in a separate plan.

**Tech Stack:** Markdown, Claude Code plugin system (SKILL.md format, agent format)

---

## File Map

| Path | Action | Task |
|------|--------|------|
| `tests/pressure/conventional-commit/README.md` | Create | 1 |
| `tests/pressure/conventional-commit/scenarios/001-non-standard-type.md` | Create | 1 |
| `tests/pressure/conventional-commit/scenarios/002-scope-with-spaces.md` | Create | 1 |
| `tests/pressure/conventional-commit/scenarios/003-body-before-blank-line.md` | Create | 1 |
| `tests/pressure/conventional-commit/evaluation-log.md` | Create | 1 |
| `skills/conventional-commit/reference.md` | Create | 2 |
| `skills/conventional-commit/SKILL.md` | Modify — add reference link | 2 |
| `skills/http-api-principles/examples.md` | Create | 3 |
| `skills/http-api-principles/SKILL.md` | Modify — add examples link | 3 |
| `skills/general-naming-principles/examples.md` | Create | 4 |
| `skills/general-naming-principles/SKILL.md` | Modify — add examples link | 4 |
| `skills/exception-principles/` | Delete | 5 |
| `skills/exception-and-logging-principles/SKILL.md` | Create | 5 |
| `skills/exception-and-logging-principles/examples.md` | Create | 5 |
| `skills/core-principles/SKILL.md` | Create | 6 |
| `skills/sync-working-status/SKILL.md` | Modify — expand to 3 sync targets | 7 |
| `agents/principles-reviewer.md` | Modify — add core-principles scope | 8 |

---

### Task 1: Pressure Test Framework

**Files:**
- Create: `tests/pressure/conventional-commit/README.md`
- Create: `tests/pressure/conventional-commit/scenarios/001-non-standard-type.md`
- Create: `tests/pressure/conventional-commit/scenarios/002-scope-with-spaces.md`
- Create: `tests/pressure/conventional-commit/scenarios/003-body-before-blank-line.md`
- Create: `tests/pressure/conventional-commit/evaluation-log.md`

**Note on scope:** Scenarios test only rules that are still enforced. English-specific rules (lowercase start, imperative mood, no trailing period) are not enforced and therefore not tested.

- [ ] **Step 1: Create `tests/pressure/conventional-commit/README.md`**

```markdown
# Pressure Tests — `conventional-commit`

Skill pressure testing applies TDD to skill documentation. The goal is to verify that the `conventional-commit` skill actually constrains agent behavior — not just that it exists.

## What RED/GREEN means

- **RED:** Run the scenario in a fresh Claude Code session with NO `hw0k-workflow` skills loaded. The scenario **passes RED** if the agent violates the rule (confirming the test catches a real failure mode).
- **GREEN:** Run the same scenario in a session with `hw0k-workflow:conventional-commit` loaded. The scenario **passes GREEN** if the agent complies with the rule.

A scenario that **fails RED** (agent follows the rule without the skill) means the pressure is too weak. Strengthen the setup.

A scenario that **fails GREEN** (agent breaks the rule even with the skill) means the skill has a loophole. Enter **REFACTOR**: document the failure in a `## Loopholes Found` section in the scenario file, patch the skill wording, and re-run until GREEN passes.

## How to run a scenario

1. Open the scenario file. Read **Setup** and **Pressure**.
2. Start a **fresh Claude Code session** (clear context, no prior conversation).
3. **RED phase:** Do not load any `hw0k-workflow` skills. Paste the **Pressure** prompt verbatim.
4. **GREEN phase:** In a new fresh session, load `hw0k-workflow:conventional-commit`. Paste the same prompt.
5. Evaluate against **PASS Criteria** in the scenario file.
6. Record results in `evaluation-log.md`.

## Enforced rules (what these tests cover)

- Type must be from the allowed list: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- Scope must be lowercase, no spaces
- Blank line required between subject and body
- Breaking change must use `!` or `BREAKING CHANGE:` footer

## How to add a new scenario

1. Increment the scenario number. Copy the template below.
2. The **Pressure** section must be a verbatim prompt that creates genuine temptation.
3. **PASS Criteria** must be binary and checkable without judgment.

```markdown
# Scenario NNN: <Short Title>

## Setup
<Realistic context that makes rule-following uncomfortable>

## Pressure
<Verbatim prompt to paste into the test session>

## Expected RED Behavior (skill NOT loaded)
<Specific failure mode>

## Expected GREEN Behavior (skill loaded)
<Minimum acceptable output>

## PASS Criteria
RED PASS if: <agent violates the rule>
GREEN PASS if: <specific, checkable conditions>
```
```

- [ ] **Step 2: Create `tests/pressure/conventional-commit/scenarios/001-non-standard-type.md`**

```markdown
# Scenario 001: Non-Standard Type Temptation

## Setup

The agent is working on a project that has an informal convention of using
"update" as a commit type. The agent has seen this pattern in the project's
recent git log. The task is a minor dependency version bump — exactly the kind
of change that might be called "update" in common usage.

## Pressure

> Please write a commit message for bumping the axios dependency from 1.6.0 to
> 1.7.2. This is just a minor version bump with no breaking changes. The project
> history uses "update" for these kinds of changes.

## Expected RED Behavior (skill NOT loaded)

Agent follows the project's informal convention:

    update: bump axios from 1.6.0 to 1.7.2

or rationalizes that "update" is reasonable given the project context.

## Expected GREEN Behavior (skill loaded)

Agent uses a type from the allowed list. Dependency bumps map to `build` or `chore`:

    build: bump axios from 1.6.0 to 1.7.2

or:

    chore: bump axios from 1.6.0 to 1.7.2

Agent does not use "update" even though it appears in project history.

## PASS Criteria

RED PASS if: agent uses "update" or any type not in the allowed list.

GREEN PASS if:
- [ ] Type is exactly one of: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- [ ] "update" does not appear as the type
```

- [ ] **Step 3: Create `tests/pressure/conventional-commit/scenarios/002-scope-with-spaces.md`**

```markdown
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
```

- [ ] **Step 4: Create `tests/pressure/conventional-commit/scenarios/003-body-before-blank-line.md`**

```markdown
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
```

- [ ] **Step 5: Create `tests/pressure/conventional-commit/evaluation-log.md`**

```markdown
# Evaluation Log

Record RED/GREEN results here after running scenarios manually.

| Scenario | RED Result | GREEN Result | Date | Notes |
|----------|-----------|-------------|------|-------|
| 001-non-standard-type | — | — | — | |
| 002-scope-with-spaces | — | — | — | |
| 003-body-before-blank-line | — | — | — | |

**Result values:** PASS / FAIL / REFACTOR-NEEDED
```

- [ ] **Step 6: Verify content**

Check:
- `README.md` contains: RED/GREEN definitions, run instructions, enforced rules list (4 rules), REFACTOR instructions, scenario template
- Each scenario file contains: Setup, Pressure, Expected RED, Expected GREEN, PASS Criteria
- Each PASS Criteria has binary, checkable conditions
- `evaluation-log.md` table has all 3 scenario names

- [ ] **Step 7: Commit**

```bash
git add tests/
git commit -m "test: add conventional-commit pressure test scenarios"
```

---

### Task 2: conventional-commit Skill Refactoring

**Files:**
- Create: `skills/conventional-commit/reference.md`
- Modify: `skills/conventional-commit/SKILL.md` — add reference link at bottom

- [ ] **Step 1: Create `skills/conventional-commit/reference.md`**

```markdown
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
```

- [ ] **Step 2: Modify `skills/conventional-commit/SKILL.md` — add reference link**

Read the current file, then append at the end:

```markdown

## Extended Reference

For WIP commits, scope examples by project type, breaking change patterns, and revert commit guidance, see [reference.md](reference.md).
```

- [ ] **Step 3: Verify**

Check:
- `reference.md` contains: WIP section (good/bad examples), scope table (4 rows), breaking change examples (`!` and footer), revert example, multi-line body example
- `SKILL.md` ends with a link to `reference.md`

- [ ] **Step 4: Commit**

```bash
git add skills/conventional-commit/
git commit -m "refactor: split conventional-commit skill into main and reference"
```

---

### Task 3: http-api-principles Skill Refactoring

**Files:**
- Create: `skills/http-api-principles/examples.md`
- Modify: `skills/http-api-principles/SKILL.md` — add examples link

- [ ] **Step 1: Create `skills/http-api-principles/examples.md`**

```markdown
# http-api-principles — Examples

Extended examples for the `http-api-principles` skill.

## URL Structure Examples

```
# Single resource
GET    /users/{id}
PUT    /users/{id}
DELETE /users/{id}

# Collection
GET  /users
POST /users

# Nested (max 2 levels)
GET  /users/{id}/orders
POST /users/{id}/orders
GET  /users/{id}/orders/{orderId}

# Action on resource (POST + noun path when no REST method fits)
POST /users/{id}/password-reset
POST /orders/{id}/cancellation
```

## Error Response Examples

**400 Validation Error (multiple fields):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid fields.",
    "details": [
      { "field": "email", "message": "must not be blank" },
      { "field": "email", "message": "must be a valid email address" },
      { "field": "age", "message": "must be at least 18" }
    ]
  }
}
```

**404 Not Found:**
```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "No user exists with the given ID.",
    "details": []
  }
}
```

**401 Unauthorized:**
```json
{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "The provided authentication token is invalid or has expired.",
    "details": []
  }
}
```

**500 Internal Server Error (never expose internals):**
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred. Please try again later.",
    "details": []
  }
}
```

## Pagination Examples

**Request:**
```
GET /orders?limit=20&cursor=eyJpZCI6MTIzfQ==
```

**Response:**
```json
{
  "data": [
    { "id": "ord_124", "status": "shipped", "createdAt": "2026-03-27T10:00:00Z" },
    { "id": "ord_123", "status": "delivered", "createdAt": "2026-03-26T08:30:00Z" }
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
GET /orders?limit=500
→ 400 Bad Request
{
  "error": {
    "code": "INVALID_PAGINATION",
    "message": "limit must not exceed 100.",
    "details": [{ "field": "limit", "message": "must be at most 100" }]
  }
}
```

## Versioning and Deprecation Headers

```
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 01 Jan 2028 00:00:00 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
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

- [ ] **Step 2: Modify `skills/http-api-principles/SKILL.md` — add examples link**

Read the current file, then append at the end:

```markdown

## Extended Examples

For full JSON error response examples, pagination request/response examples, URL structure patterns, and status code decision guide, see [examples.md](examples.md).
```

- [ ] **Step 3: Verify**

Check:
- `examples.md` contains: URL structure block, 4 error response examples, pagination examples, deprecation headers, status code table
- `SKILL.md` ends with a link to `examples.md`

- [ ] **Step 4: Commit**

```bash
git add skills/http-api-principles/
git commit -m "refactor: split http-api-principles skill into main and examples"
```

---

### Task 4: general-naming-principles Skill Refactoring

**Files:**
- Create: `skills/general-naming-principles/examples.md`
- Modify: `skills/general-naming-principles/SKILL.md` — add examples link

- [ ] **Step 1: Create `skills/general-naming-principles/examples.md`**

```markdown
# general-naming-principles — Examples

Extended examples for the `general-naming-principles` skill.

## Variable Naming: Before/After

| Before | After | Why |
|--------|-------|-----|
| `const u = await getUser()` | `const user = await getUser()` | Single letter hides type |
| `const flg = isActive()` | `const active = checkIsActive()` | Abbreviation + no boolean prefix |
| `const mgr = new SessionManager()` | `const sessionManager = new SessionManager()` | `mgr` is an unclear abbreviation |
| `const d = new Date()` | `const createdAt = new Date()` | Context-free single letter |
| `let cnt = 0` | `let retryCount = 0` | Abbreviation hides meaning |

## Function Naming: Before/After

| Before | After | Why |
|--------|-------|-----|
| `function processUser(u)` | `function activateUser(user)` | "process" is meaningless |
| `async function asyncFetchOrders()` | `async function fetchOrders()` | `async` prefix is redundant |
| `function check(email)` | `function isValidEmail(email)` | Too vague; boolean needs predicate form |
| `function doPayment(order)` | `function chargeOrder(order)` | "do" is meaningless |
| `function handleError(e)` | `function logAndRethrow(error)` | Name should describe the action |

## Class and Interface Naming

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
# Source files — kebab-case, named for primary export
user-service.ts          → exports UserService
order-repository.ts      → exports OrderRepository
payment-error.ts         → exports PaymentError

# Test files — mirror source path and name
src/user-service.ts      → tests/user-service.test.ts
src/auth/token.ts        → tests/auth/token.test.ts

# Bad — don't use these
utils.ts                 → too generic
helpers.ts               → same
index.ts with logic      → barrel exports only
```

## Package/Module Naming

```
# Good — domain-specific names
user-validation.ts       (not utils.ts)
date-formatter.ts        (not helpers.ts)
order-errors.ts          (not errors.ts)
auth-middleware.ts       (not middleware.ts)
```

## Constants: SCREAMING_SNAKE vs camelCase

```typescript
// SCREAMING_SNAKE_CASE: compile-time, never reassigned, module-level
const MAX_RETRY_COUNT = 3
const DEFAULT_PAGE_SIZE = 20
const SESSION_EXPIRY_SECONDS = 3600

// camelCase: runtime-determined (env vars, config loaded at startup)
const databaseUrl = process.env.DATABASE_URL
const jwtSecret = config.get('jwt.secret')
```
```

- [ ] **Step 2: Modify `skills/general-naming-principles/SKILL.md` — add examples link**

Read the current file, then append at the end:

```markdown

## Extended Examples

For before/after naming comparisons, file naming patterns, class/interface examples, and constants reference, see [examples.md](examples.md).
```

- [ ] **Step 3: Verify**

Check:
- `examples.md` contains: variable before/after table (5 rows), function before/after table (5 rows), class/interface examples, file naming block, package naming block, constants comparison block
- `SKILL.md` ends with a link to `examples.md`

- [ ] **Step 4: Commit**

```bash
git add skills/general-naming-principles/
git commit -m "refactor: split general-naming-principles skill into main and examples"
```

---

### Task 5: exception-and-logging-principles Skill (Replaces exception-principles)

**Files:**
- Delete: `skills/exception-principles/` (entire directory)
- Create: `skills/exception-and-logging-principles/SKILL.md`
- Create: `skills/exception-and-logging-principles/examples.md`

- [ ] **Step 1: Delete the old skill directory**

```bash
git rm -r skills/exception-principles/
```

- [ ] **Step 2: Create `skills/exception-and-logging-principles/SKILL.md`**

```markdown
---
name: exception-and-logging-principles
description: Combined exception handling and logging standards — failure classification, catch rules, log levels, structured format, correlation ID propagation, re-throw pattern, and recovery strategies
type: reference
---

# Exception and Logging Principles

Exception handling and logging are one decision point. When you catch, you also decide what to log and at what level. This skill organizes both around the sequence of events when something goes wrong: classify → catch → log → re-throw or recover.

## Failure Classification

Classify before handling. Classification determines catch strategy, log level, and recovery approach.

| Category | Definition | Example |
|----------|-----------|---------|
| **Expected** | Known, recoverable domain condition | Validation error, resource not found, rate limit hit |
| **Unexpected** | Outside normal operating envelope | Null dereference, disk full, assertion failure |
| **External** | Originates in a dependency outside this service | Downstream API 500, network timeout, third-party SDK exception |

## Catch Rules

1. **Catch only what you can handle.** A catch block that re-throws without adding context is noise.
2. **Never swallow silently.** Every catch block must log, re-throw, or trigger a recovery path. An empty catch block is always a bug.
3. **Catch at the boundary.** The boundary is the outermost layer that can make a meaningful decision: API handler, job runner, event consumer. Internal helpers throw — they do not catch and log.
4. **Do not catch base Error types** unless you are at the boundary converting to a structured error response.

```typescript
// Violation: swallowed exception
catch (e) { }

// Compliant: catch with intent
catch (e: DatabaseError) {
  logger.error("Failed to save order", { error: e.message, orderId })
  throw new ServiceUnavailableError("Order storage unavailable", { cause: e })
}
```

## Log Levels

Use the level that matches the operational significance, not the code path.

| Level | When to use |
|-------|------------|
| `ERROR` | Operation failed; human or automated intervention required |
| `WARN` | Operation succeeded despite anomaly, or recoverable failure was handled |
| `INFO` | Significant business event completed normally (request received, job finished) |
| `DEBUG` | Internal state for diagnosing a specific problem; must be off by default in production |

Do not use `INFO` for failure events. Do not use `ERROR` for expected failures that were successfully recovered.

## Structured Log Format

All log entries must be valid JSON. Free-text log strings are not acceptable in application code.

Required fields:

```json
{
  "timestamp": "2026-03-27T10:00:00Z",
  "level": "ERROR",
  "message": "Failed to process payment for order ord_123",
  "correlationId": "req_abc123",
  "service": "payment-service",
  "context": {
    "orderId": "ord_123",
    "userId": "usr_456",
    "errorType": "DatabaseError"
  }
}
```

Additional fields go inside `context`. Do not add arbitrary fields at the top level.

## Correlation ID Propagation

Every log entry within a request or job execution must include the same `correlationId`. The ID originates at the entry point (HTTP request, queue message, scheduled job) and is passed explicitly through the call stack.

- If no incoming ID is present, generate one at the boundary and log its origin.
- Pass `correlationId` as a parameter or in a request-scoped context object.
- Do not store it in a module-level variable shared across requests.

## What to Log / What NOT to Log

**Always include:**
- The operation identifier (what was attempted)
- Failure category
- `correlationId`
- Sanitized input identifiers (user ID, resource ID — not the full input)
- Error type and message
- Stack trace for `ERROR` level (Unexpected and External categories)

**Never include:**
- Passwords, tokens, API keys, session IDs, OAuth codes
- Full credit card numbers or CVVs
- PII: email addresses, phone numbers, SSNs, physical addresses
- Full request bodies unless explicitly required by compliance and masked
- Stack traces at `INFO` or `WARN` level
- Duplicate log entries for the same event at multiple layers — log once at the boundary

## Re-throw and Context Propagation

When re-throwing across a layer boundary, wrap with a type appropriate to the current layer and attach the original as the cause.

```typescript
// Good — adds context, preserves cause
try {
  await db.save(record)
} catch (err) {
  throw new DatabaseError("Failed to save user record", { cause: err })
}

// Bad — original exception lost
try {
  await db.save(record)
} catch (err) {
  throw new Error("Failed to save user record")  // cause discarded
}
```

Always use `{ cause: err }` (or language equivalent) when re-throwing.

## Expected vs Unexpected Failures

Use return values for **expected, predictable failures**. Use exceptions for **unexpected failures**.

```typescript
// Good — parsing predictably fails, return value is appropriate
function parseDate(s: string): Result<Date, ParseError>

// Good — DB failure is unexpected, let it throw
async function fetchUser(id: string): Promise<User>

// Bad — exceptions used for control flow
try {
  const user = await fetchUser(id)
} catch (err) {
  if (err instanceof NotFoundError) return null
  // Use findUser() that returns null instead
}
```

## Recovery Strategies

Recovery is only valid for expected failures where the recovery path is defined by the business domain.

| Category | Valid recovery | Notes |
|----------|--------------|-------|
| Expected failure | Return domain-appropriate result (empty list, default value, user-facing error) | |
| External failure | Retry with exponential backoff if idempotent; circuit-break if persistent | Max 3 retries; log each attempt |
| Unexpected failure | Do not recover — log ERROR, propagate to boundary, return 500 | Never silently ignore |

Never retry validation errors or unexpected errors — they will not self-resolve.

## Boundary Definition

A boundary is any point where execution crosses a trust or ownership boundary:
- HTTP request handler
- Message queue consumer
- Scheduled job entry point
- Public API of a library

Internal helper functions are **not** boundaries. They throw — they do not catch and log.

## Extended Examples

For annotated multi-layer re-throw chains, retry/circuit-breaker patterns, correlation ID flow, and before/after comparisons, see [examples.md](examples.md).
```

- [ ] **Step 3: Create `skills/exception-and-logging-principles/examples.md`**

```markdown
# exception-and-logging-principles — Examples

## Correlation ID: Full Request Lifecycle

```typescript
// HTTP handler — entry point, generates correlationId
app.post('/orders', async (req, res) => {
  const correlationId = req.headers['x-correlation-id'] ?? generateId()
  const ctx = { correlationId, userId: req.user.id }

  try {
    const order = await orderService.create(req.body, ctx)
    res.status(201).json(order)
  } catch (err) {
    logger.error("Failed to create order", {
      ...ctx,
      error: err.message,
      stack: err.stack,
    })
    res.status(500).json({ error: { code: "INTERNAL_ERROR", message: "..." } })
  }
})

// Service layer — passes ctx, does not log
class OrderService {
  async create(data: CreateOrderDto, ctx: RequestContext): Promise<Order> {
    const validated = validateOrder(data)  // throws ValidationError if invalid
    return this.repo.save(validated, ctx)
  }
}

// Repository layer — wraps external errors, passes ctx
class OrderRepository {
  async save(order: Order, ctx: RequestContext): Promise<Order> {
    try {
      return await this.db.insert(order)
    } catch (err) {
      throw new DatabaseError("Failed to persist order", { cause: err })
      // Does NOT log here — boundary will log
    }
  }
}
```

## Silent Swallow: Before/After

```typescript
// Before — swallowed exception, bug
async function deleteUser(id: string) {
  try {
    await db.delete('users', id)
    await cache.invalidate(`user:${id}`)
  } catch (e) {
    // nothing — caller never knows this failed
  }
}

// After — compliant
async function deleteUser(id: string, ctx: RequestContext) {
  await db.delete('users', id)  // let it throw — boundary handles it
  try {
    await cache.invalidate(`user:${id}`)
  } catch (err) {
    // Cache miss is recoverable — warn and continue
    logger.warn("Failed to invalidate user cache after delete", {
      correlationId: ctx.correlationId,
      userId: id,
      error: err.message,
    })
  }
}
```

## Retry With Backoff (External Failure)

```typescript
async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  ctx: RequestContext,
  maxRetries = 3,
): Promise<T> {
  let lastError: Error
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn()
    } catch (err) {
      lastError = err
      if (attempt < maxRetries) {
        const delay = 100 * 2 ** attempt  // 200ms, 400ms, 800ms
        logger.warn("Retrying after failure", {
          correlationId: ctx.correlationId,
          attempt,
          maxRetries,
          error: err.message,
        })
        await sleep(delay)
      }
    }
  }
  throw new ExternalServiceError("Max retries exceeded", { cause: lastError })
}
```

## Multi-Layer Re-throw Chain

```typescript
// Layer 3: Repository
catch (err: PostgresError) {
  throw new DatabaseError("Failed to update user balance", { cause: err })
}

// Layer 2: Service
catch (err: DatabaseError) {
  throw new PaymentProcessingError(
    `Balance update failed for user ${userId}`,
    { cause: err }
  )
}

// Layer 1: HTTP Handler (boundary — logs here only)
catch (err: PaymentProcessingError) {
  logger.error("Payment processing failed", {
    correlationId: ctx.correlationId,
    userId,
    error: err.message,
    cause: err.cause?.message,
    stack: err.stack,
  })
  res.status(503).json({ error: { code: "PAYMENT_UNAVAILABLE", message: "..." } })
}
```
```

- [ ] **Step 4: Verify**

Check `SKILL.md` contains:
- [ ] Failure classification table (3 categories)
- [ ] 4 catch rules
- [ ] Log levels table (ERROR/WARN/INFO/DEBUG)
- [ ] Structured log format JSON with required fields
- [ ] Correlation ID propagation rules
- [ ] What to log / what NOT to log lists
- [ ] Re-throw example (good + bad with `{ cause }`)
- [ ] Expected vs unexpected failure examples
- [ ] Recovery strategies table
- [ ] Boundary definition
- [ ] Link to `examples.md`

Check `examples.md` contains:
- [ ] Full request lifecycle (3 layers)
- [ ] Silent swallow before/after
- [ ] Retry with backoff
- [ ] Multi-layer re-throw chain

- [ ] **Step 5: Commit**

```bash
git add skills/exception-and-logging-principles/ skills/exception-principles/
git commit -m "feat: replace exception-principles with exception-and-logging-principles"
```

---

### Task 6: core-principles Skill

**Files:**
- Create: `skills/core-principles/SKILL.md`

- [ ] **Step 1: Create `skills/core-principles/SKILL.md`**

```markdown
---
name: core-principles
description: Four foundational principles governing all hw0k-workflow standards — environment independence, human gate for irreversible operations, static verification, and don't reinvent the wheel
type: reference
---

# Core Principles

These four principles are pre-conditions for all other standards in this plugin. Any skill-specific rule that conflicts with a core principle is overridden by the core principle. Check these before acting, not after.

---

## Principle 1 — Environment Independence

**Rule:** A change is only valid if it produces identical behavior on every device, agent instance, and tool version it will run on. Do not rely on local state, local credentials, locally installed tools, or working directory assumptions that are not explicitly established in the task context.

**Rationale:** Solutions that depend on implicit local conditions introduce failures that are invisible during authoring and expensive to diagnose elsewhere.

**Compliant:**
- Specifying the exact command with its full flag set rather than relying on shell aliases
- Checking for the existence of a required tool before invoking it
- Using relative paths only when the working directory is explicitly set in the same context
- Declaring all dependencies in version-controlled config files (package.json, go.mod, requirements.txt)

**Non-compliant:**
- "This works because I have Node 20 installed" — version assumed, not verified
- Using `~/.config/...` paths without confirming the path exists in the target environment
- Referencing a shell function that exists locally but is not in the repo
- Hardcoding an absolute path that only exists on the author's machine

**`principles-reviewer` trigger:** Any command, script, or file change containing an environment assumption — hardcoded path, tool invocation without version check, reference to local state not established in the task context.

---

## Principle 2 — Human Gate for Irreversible Operations

**Rule:** Before executing any operation that cannot be fully undone, present the proposed action and receive explicit human approval. A single confirmation is the minimum. Proceed only on unambiguous, explicit consent — not inferred or prior approval.

**Rationale:** Irreversible operations have asymmetric cost. The cost of an unnecessary confirmation is low. The cost of an unconfirmed mistake can be unbounded.

**What counts as irreversible:**
- `git push --force`, `git reset --hard`, `git branch -D`
- File deletion or overwrite of a file not tracked by version control
- Any write to a remote system: deploy, publish, database mutation
- Sending an external notification: email, webhook, Slack message
- Dropping or truncating a database table or collection

**Compliant:**
- Showing the exact command to be run, explaining its effect, and waiting for an explicit "yes"
- Listing all files to be deleted before deleting any of them

**Non-compliant:**
- Proceeding with a force-push because the user said "fix the branch" without specifying the method
- Treating a previous approval (from an earlier turn) as approval for a new operation of the same type

**`principles-reviewer` trigger:** Any command in the irreversible list, or any command whose effect on persistent external state cannot be rolled back within the current session.

---

## Principle 3 — Static Verification Over Subjective Assessment

**Rule:** When asserting that code is correct, a change is safe, or a configuration is valid, back the assertion with a static analysis result — type checker output, linter result, test output, schema validator result. "Looks right" or "should work" are not acceptable verification statements.

**Rationale:** Subjective assessment introduces unverifiable confidence. Static tools produce repeatable, auditable results that another agent or human can inspect independently.

**Compliant:**
- "TypeScript compiler reports zero errors on this file after the change."
- "ESLint passes with the project ruleset: `npm run lint` exits 0."
- "All 47 tests pass: `npm test` exits 0."

**Non-compliant:**
- "The logic seems correct."
- "This should work based on the pattern I see elsewhere."
- "I reviewed it and it looks fine."
- "This is a simple change, no testing needed."

When a static tool is not available for the domain, state this explicitly: "No static validator is available for this config format. Manual review required."

**`principles-reviewer` trigger:** Any verification or correctness claim that does not cite a tool output.

---

## Principle 4 — Don't Reinvent the Wheel

**Rule:** Before implementing a custom solution, verify that a well-maintained tool does not already solve the problem. Prefer established tools when they are actively maintained, widely adopted, and require no significant adaptation.

**Rationale:** Custom implementations duplicate battle-tested work, require ongoing maintenance, and introduce bugs the ecosystem has already fixed.

**Compliant:**
- Using commitlint instead of a custom regex-based commit message validator
- Using lefthook instead of a custom hook management script
- Using an established date library instead of re-implementing date arithmetic

**Non-compliant:**
- Writing a shell script to validate commit messages when commitlint exists and covers the same rules
- Re-implementing UUID generation, pagination utilities, or other solved problems
- Building a custom CI step when a maintained GitHub Action already exists for the task

**Exception:** the existing tool requires significant adaptation overhead that exceeds the benefit, has a problematic license or security record, or cannot work in the target environment. Document the exception and its reason.

**`principles-reviewer` trigger:** Any new utility, script, or implementation that overlaps with a known, well-maintained open-source solution.
```

- [ ] **Step 2: Verify**

Check `SKILL.md` contains:
- [ ] Opening paragraph (4 principles are pre-conditions)
- [ ] Principle 1: Rule + Rationale + Compliant (4 items) + Non-compliant (4 items) + trigger
- [ ] Principle 2: Rule + Rationale + irreversible list (5 items) + Compliant + Non-compliant + trigger
- [ ] Principle 3: Rule + Rationale + Compliant (3 items, cite tool output) + Non-compliant (4 items) + "no tool available" statement + trigger
- [ ] Principle 4: Rule + Rationale + Compliant (3 items) + Non-compliant (3 items) + Exception clause + trigger

- [ ] **Step 3: Commit**

```bash
git add skills/core-principles/
git commit -m "feat: add core-principles skill"
```

---

### Task 7: sync-working-status Skill Update

**Files:**
- Modify: `skills/sync-working-status/SKILL.md` — expand to 3 sync targets

- [ ] **Step 1: Read the current file**

Read `skills/sync-working-status/SKILL.md` to understand the current structure.

- [ ] **Step 2: Replace the `## When to Run` and `## Steps` sections**

Replace the existing content from `## When to Run` through the end of the steps with:

```markdown
## When to Run

- Before switching to a different task or branch
- After completing a significant chunk of work
- When returning to a branch after time away
- Before requesting a code review or converting a draft PR
- After any Claude session that produced file changes

## Steps

### 1. Assess Local Git State

```bash
git status              # uncommitted changes
git log --oneline -5    # recent commits not yet in PR
git branch -vv          # branch tracking + ahead/behind count
```

Note:
- Are there uncommitted changes that should be committed first?
- How many commits are ahead of the remote?

### 2. Assess Specs/Plans State

Check `docs/specs/` and `docs/plans/` for files related to current work:

- Do plan file checkboxes reflect actual progress? (Mark completed tasks as `- [x]`)
- Does the spec still describe what is being built, or has scope changed?
- Is there a plan file for current work? If not, note the gap.

Specs and plans are the single source of truth for task progress. Update them before syncing remotely.

### 3. Assess Remote State

For the current branch, check the associated PR (if any):

- **PR status:** draft / open / needs review / changes requested / approved / merged / closed
- **CI status:** passing / failing / pending
- **Open review threads:** any unresolved comments?
- **Linked issue:** still open? still accurate?

If no PR exists and the branch has commits, note whether one should be created.

### 4. Resolve Discrepancies

| Local state | Remote state | Action |
|-------------|-------------|--------|
| Commits ahead, not pushed | PR shows old state | Push: `git push` |
| Work is done | PR is still draft | Convert to "Ready for review" |
| All review comments addressed | Threads still open | Mark threads resolved on GitHub |
| Work complete | Linked issue still open | Close issue, add closing reference to PR |
| No PR | Feature complete | Create PR with accurate description |
| PR description outdated | Describes planned work, not actual | Update PR description |
| Plan checkboxes stale | Tasks completed but not marked | Update plan file checkboxes |
| Spec scope has changed | Spec describes original intent | Update spec to reflect what was built |

### 5. Confirm Sync Complete

Before declaring sync done, verify:
- [ ] All intended commits are pushed to remote
- [ ] Plan file checkboxes reflect actual progress
- [ ] Spec describes what was actually built
- [ ] PR status matches actual readiness
- [ ] No unresolved review threads from addressed feedback
- [ ] Linked issue status matches work state
- [ ] PR description accurately describes what was built
```

- [ ] **Step 3: Verify**

Check updated `SKILL.md` contains:
- [ ] 5 when-to-run triggers
- [ ] Step 1: local git (3 commands)
- [ ] Step 2: Specs/Plans assessment (check docs/)
- [ ] Step 3: remote state (PR status, CI, threads, linked issue)
- [ ] Step 4: discrepancy table (8 rows including plan/spec rows)
- [ ] Step 5: confirmation checklist (7 items)

- [ ] **Step 4: Commit**

```bash
git add skills/sync-working-status/SKILL.md
git commit -m "feat: expand sync-working-status to cover specs/plans as sync target"
```

---

### Task 8: principles-reviewer Agent Update

**Files:**
- Modify: `agents/principles-reviewer.md`

- [ ] **Step 1: Read the current file**

Read `agents/principles-reviewer.md`.

- [ ] **Step 2: Replace the entire file**

```markdown
---
name: principles-reviewer
description: Reviews code and process against all four hw0k-workflow principle skills — core principles, HTTP API design, exception and logging, and naming conventions.
type: agent
---

# Principles Reviewer

You are a code reviewer checking compliance with hw0k-workflow standards. Your job is to find and report violations clearly — not to fix them, explain them at length, or praise compliant code.

## Scope

Review against all four principle areas, in this order:

1. **Core principles** (`hw0k-workflow:core-principles`) — environment independence, irreversible operation gates, static verification, don't reinvent the wheel
2. **HTTP API design** (`hw0k-workflow:http-api-principles`) — resource naming, HTTP methods, status codes, error response format, versioning, pagination
3. **Exception and logging** (`hw0k-workflow:exception-and-logging-principles`) — catch boundaries, logging requirements, error categorization, re-throw pattern, recovery strategies
4. **Naming conventions** (`hw0k-workflow:general-naming-principles`) — variables, functions, classes, constants, files, packages

Core principles lead because process-level violations can invalidate how the other three areas are applied.

## Before You Start

Read all four principle skills in full before reviewing any code:
- `hw0k-workflow:core-principles`
- `hw0k-workflow:http-api-principles`
- `hw0k-workflow:exception-and-logging-principles`
- `hw0k-workflow:general-naming-principles`

## Output Format

Two violation formats are used:

**Process violation** (Core Principles — no file/line, pattern-level observation):
```
[rule] — observation → expected behavior
```

**Code violation** (areas 2–4 — specific file and line):
```
`file:line [rule] — what found → what it should be`
```

Structure your output with one section per principle area:

```
## Core Principles

### Violations
[core.environment-independence] — script references ~/.nvm/versions/node/v20/bin/node → use env-relative path or declare Node version in .nvmrc
[core.static-verification] — PR description states "this should work" without citing test output → add test run output

### Passed
- No irreversible operations in proposed changes

---

## HTTP API Design

### Violations
- `routes/users.ts:45` [method] — POST used for fetch: `app.post('/getUser', ...)` → use `GET /users/{id}`
- `handlers/orders.ts:102` [status code] — returns 200 for validation failure → use 400

### Passed
- Resource naming uses plural nouns consistently

---

## Exception and Logging

### Violations
- `services/auth.ts:67` [swallowed exception] — catch block is empty → must log, re-throw, or recover

### Passed
- Re-throw pattern uses `{ cause: err }` correctly in database layer

---

## Naming Conventions

No violations found.
```

## Violation Format Details

Each **code violation** must include:
- **File and line**: `` `path/to/file.ts:42` ``
- **Rule in brackets**: `[method]`, `[status code]`, `[swallowed exception]`, `[boolean prefix]`, etc.
- **What was found**: quote or describe the offending code
- **What it should be**: the correction (brief)

Each **process violation** must include:
- **Rule in brackets**: `[core.environment-independence]`, `[core.irreversible-gate]`, `[core.static-verification]`, `[core.no-reinvention]`
- **Observation**: what pattern was observed
- **Expected behavior**: what compliant behavior looks like

## Instructions

1. Read all four principle skills before starting
2. Review every file in scope against all four areas
3. Report all violations — do not skip minor ones
4. Do **not** suggest fixes beyond the one-line correction in the violation entry
5. Do **not** explain the rules — the author can read the skills
6. If an area has no violations, write "No violations found."
7. If you cannot determine whether something is a violation from context alone, note it as "Unclear — may violate [rule], needs context"
8. A core principle violation that overlaps with a code-level rule: note the pattern in Core Principles, let the code-level section handle the specifics
```

- [ ] **Step 3: Verify**

Check `agents/principles-reviewer.md` contains:
- [ ] Description updated to "four hw0k-workflow principle skills"
- [ ] 4 scope items, core-principles at position 1, includes "don't reinvent the wheel"
- [ ] `exception-and-logging-principles` (not `exception-principles`)
- [ ] Two violation format types (process vs code)
- [ ] Example output shows all 4 sections
- [ ] `[core.no-reinvention]` in the process violation rule list
- [ ] 8 instructions

- [ ] **Step 4: Commit**

```bash
git add agents/principles-reviewer.md
git commit -m "feat: update principles-reviewer to include core-principles scope"
```

---

## Self-Review Against Spec

### Spec Coverage Check

| Spec requirement | Task |
|-----------------|------|
| Pressure test framework + 3 scenarios (English-specific rules removed) | Task 1 |
| `conventional-commit` reference.md split | Task 2 |
| `http-api-principles` examples.md split | Task 3 |
| `general-naming-principles` examples.md split | Task 4 |
| `exception-principles` deleted, `exception-and-logging-principles` created | Task 5 |
| `core-principles` skill — 4 principles including Don't Reinvent the Wheel | Task 6 |
| `sync-working-status` expanded to 3 sync targets | Task 7 |
| `principles-reviewer` updated: 4 areas, two violation formats, no-reinvention trigger | Task 8 |

### Placeholder Scan

No TBDs, TODOs, "implement later", or "similar to Task N" present. All file contents are complete.

### Type Consistency

All tasks produce independent markdown files. No shared types or method names across tasks. No consistency issues.
