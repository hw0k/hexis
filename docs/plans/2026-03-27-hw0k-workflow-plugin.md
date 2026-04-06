---
linked_spec: docs/specs/2026-03-27-hw0k-workflow-plugin-design.md
---

# hw0k-workflow Plugin Implementation Plan

> **Historical document.** This plan reflects the initial implementation state. Some skill names have since been renamed (e.g., `conventional-commit` → `commit-principles`, `new-project-setup` → `setup-new-project`).

> **For agentic workers:** Use `hw0k-workflow:implement` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the hw0k-workflow Claude Code plugin — skills, commands, and an agent that enforce opinionated development standards (commit format, status sync, HTTP API design, exception handling, naming conventions).

**Architecture:** All deliverables are markdown files consumed by Claude Code. Skills guide Claude's behavior passively (reference guides); commands expose user-triggered actions; the principles-reviewer agent consolidates all three principle checks into a single review. No executable code — verification is content review against the spec.

**Tech Stack:** Markdown (SKILL.md / command / agent format), Claude Code plugin system, Conventional Commits 1.0.0

---

## File Map

| Path | Action | Responsibility |
|------|--------|----------------|
| `.claude-plugin/plugin.json` | Create | Plugin metadata |
| `README.md` | Create | Plugin documentation |
| `skills/conventional-commit/SKILL.md` | Create | Conventional Commits 1.0.0 enforcement guide |
| `skills/sync-working-status/SKILL.md` | Create | Local git + GitHub status sync guide |
| `skills/http-api-principles/SKILL.md` | Create | HTTP API design standards |
| `skills/exception-principles/SKILL.md` | Create | Exception handling standards |
| `skills/general-naming-principles/SKILL.md` | Create | Naming conventions |
| `commands/commit.md` | Create | `/hw0k-workflow:commit` slash command |
| `commands/sync.md` | Create | `/hw0k-workflow:sync-working-status` slash command |
| `agents/principles-reviewer.md` | Create | Principles review agent |

---

### Task 1: Plugin Infrastructure

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `README.md`

- [ ] **Step 1: Create `.claude-plugin/plugin.json`**

```json
{
  "name": "hw0k-workflow",
  "description": "Heavily opinionated common workflow plugin for Claude — covering the full development workflow — from spec to merge.",
  "version": "0.1.0",
  "keywords": [
    "workflow",
    "conventional-commit",
    "http-api",
    "principles",
    "opinionated"
  ]
}
```

- [ ] **Step 2: Create `README.md`**

```markdown
# hw0k-workflow

A heavily opinionated Claude Code plugin covering the full development workflow — from spec to merge.

## Skills

| Skill | Namespace | Purpose |
|-------|-----------|---------|
| Conventional Commit | `hw0k-workflow:conventional-commit` | Enforce Conventional Commits 1.0.0 format |
| Sync Working Status | `hw0k-workflow:sync-working-status` | Sync work state across Local/GitHub |
| HTTP API Principles | `hw0k-workflow:http-api-principles` | HTTP API design standards |
| Exception Principles | `hw0k-workflow:exception-principles` | Exception handling standards |
| General Naming Principles | `hw0k-workflow:general-naming-principles` | Naming conventions |

## Commands

| Command | Purpose |
|---------|---------|
| `/hw0k-workflow:commit` | Create a commit following Conventional Commits format |
| `/hw0k-workflow:sync-working-status` | Synchronize work state across Local and GitHub |

## Agents

| Agent | Purpose |
|-------|---------|
| `principles-reviewer` | Review code against all three principle skills simultaneously |

## Install

```bash
/plugin install hw0k-workflow --plugin-dir github:hw0k/hw0k-workflow
```

## Design

Principle skills (`http-api-principles`, `exception-principles`, `general-naming-principles`) are referenced automatically by Claude when developing. Workflow skills (`conventional-commit`, `sync-working-status`) are also exposed as commands because they are user-initiated actions tied to specific development cycle events.
```

- [ ] **Step 3: Verify content**

Check:
- `plugin.json` `name` is `"hw0k-workflow"`, `version` is `"0.1.0"`, has all 5 keywords from spec
- `README.md` lists all 5 skills, 2 commands, 1 agent with correct namespaces

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/plugin.json README.md
git commit -m "chore: add plugin metadata and README"
```

---

### Task 2: conventional-commit Skill

**Files:**
- Create: `skills/conventional-commit/SKILL.md`

- [ ] **Step 1: Create `skills/conventional-commit/SKILL.md`**

```markdown
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
```

- [ ] **Step 2: Verify content**

Check the file contains: allowed type table, all 7 rules, good + bad examples, enforcement checklist. No placeholder text.

- [ ] **Step 3: Commit**

```bash
git add skills/conventional-commit/SKILL.md
git commit -m "feat: add conventional-commit skill"
```

---

### Task 3: commit Command

**Files:**
- Create: `commands/commit.md`

- [ ] **Step 1: Create `commands/commit.md`**

```markdown
# /hw0k-workflow:commit

Prepare and create a commit following the Conventional Commits format.

## Steps

1. Run `git status` to see what has changed
2. Run `git diff` (or `git diff --cached` if already staged) to understand what changed
3. Stage the relevant files: `git add <files>`
4. Determine the commit type based on the changes:
   - New capability → `feat`
   - Bug fix → `fix`
   - Only docs changed → `docs`
   - Only tests changed → `test`
   - Restructure with no behavior change → `refactor`
   - Tooling/config → `chore` or `build` or `ci`
5. Write the commit message following `hw0k-workflow:conventional-commit` rules
6. Create the commit: `git commit -m "<message>"`

## Skill Reference

Use `hw0k-workflow:conventional-commit` for the full format reference including allowed types, rules, and examples.
```

- [ ] **Step 2: Verify content**

Check the file: describes all 6 steps, references the conventional-commit skill, includes type-selection guidance.

- [ ] **Step 3: Commit**

```bash
git add commands/commit.md
git commit -m "feat: add commit command"
```

---

### Task 4: sync-working-status Skill

**Files:**
- Create: `skills/sync-working-status/SKILL.md`

- [ ] **Step 1: Create `skills/sync-working-status/SKILL.md`**

```markdown
---
name: sync-working-status
description: Synchronizes current work state between local git state and GitHub — checks PR status, resolves discrepancies, and confirms everything reflects actual progress
type: workflow
---

# Sync Working Status

## Purpose

Keep work state consistent between local git and GitHub (PRs, issues, labels) so that anyone — or any future agent — picking up this work has an accurate picture.

## When to Run

- Before switching to a different task or branch
- After completing a significant chunk of work
- When returning to a branch after time away
- Before requesting a code review or converting a draft PR

## Steps

### 1. Assess Local State

```bash
git status              # uncommitted changes
git log --oneline -5    # recent commits not yet in PR
git branch -vv          # branch tracking + ahead/behind count
```

Note:
- Are there uncommitted changes that should be committed first?
- How many commits are ahead of the remote?

### 2. Assess GitHub State

For the current branch, check the associated PR (if any):

- **PR status:** draft / open / needs review / changes requested / approved / merged / closed
- **CI status:** passing / failing / pending
- **Open review threads:** any unresolved comments?
- **Linked issue:** still open? still accurate?

If no PR exists yet and the branch has commits, note whether one should be created.

### 3. Resolve Discrepancies

| Local state | GitHub state | Action |
|-------------|--------------|--------|
| Commits ahead, not pushed | PR shows old state | Push: `git push` |
| Work is done | PR is still draft | Convert to "Ready for review" |
| All review comments addressed | Threads still open | Mark threads resolved on GitHub |
| Work complete | Linked issue still open | Close issue, add closing reference to PR |
| No PR | Feature complete | Create PR with accurate description |
| PR description outdated | Describes planned work, not actual | Update PR description to reflect what was done |

### 4. Update PR Description (if applicable)

A PR description should reflect the current state of the work, not just the original intent. Update it to include:
- What was actually done (not just the plan)
- Any known issues or deferred work
- How to test the changes

### 5. Confirm Sync Complete

Before declaring sync done, verify:
- [ ] All intended commits are pushed to remote
- [ ] PR status matches actual readiness (not stuck in draft)
- [ ] No unresolved review threads from addressed feedback
- [ ] Linked issue status matches work state
- [ ] PR description accurately describes what was built
```

- [ ] **Step 2: Verify content**

Check: purpose section, 5 when-to-run triggers, all 5 numbered steps, discrepancy resolution table (6 rows), confirmation checklist.

- [ ] **Step 3: Commit**

```bash
git add skills/sync-working-status/SKILL.md
git commit -m "feat: add sync-working-status skill"
```

---

### Task 5: sync Command

**Files:**
- Create: `commands/sync.md`

- [ ] **Step 1: Create `commands/sync.md`**

```markdown
# /hw0k-workflow:sync-working-status

Synchronize current work state across Local and GitHub.

## Steps

1. Assess local git state: `git status`, `git log --oneline -5`, `git branch -vv`
2. Assess GitHub state for the current branch — check PR status, CI, open review threads, linked issue
3. Resolve any discrepancies found (push, update PR, mark resolved threads, close issue)
4. Update the PR description if it no longer reflects what was built
5. Confirm all sync items are complete

## Skill Reference

Use `hw0k-workflow:sync-working-status` for the full step-by-step guide including the discrepancy resolution table and confirmation checklist.
```

- [ ] **Step 2: Verify content**

Check: 5 steps present, references the sync-working-status skill.

- [ ] **Step 3: Commit**

```bash
git add commands/sync.md
git commit -m "feat: add sync command"
```

---

### Task 6: http-api-principles Skill

**Files:**
- Create: `skills/http-api-principles/SKILL.md`

- [ ] **Step 1: Create `skills/http-api-principles/SKILL.md`**

```markdown
---
name: http-api-principles
description: Opinionated HTTP API design standards — resource naming, HTTP methods, status codes, error response format, versioning, and pagination
type: reference
---

# HTTP API Design Principles

## Resource Naming

- Use **plural nouns** for collections: `/users`, `/orders`, `/products`
- Use **kebab-case** for multi-word resources: `/user-profiles`, `/order-items`
- Nest to show ownership, max 2 levels deep: `/users/{id}/orders`
- **Never use verbs in URLs:**
  - ❌ `/getUser`, `/createOrder`, `/deleteAccount`
  - ✅ `GET /users/{id}`, `POST /orders`, `DELETE /accounts/{id}`
- IDs belong in the path, not the query: `/users/{userId}` not `/users?id={userId}`

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

All error responses must use this exact structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email address is required.",
    "details": [
      { "field": "email", "message": "must not be blank" },
      { "field": "email", "message": "must be a valid email address" }
    ]
  }
}
```

- `code`: machine-readable identifier, SCREAMING_SNAKE_CASE
- `message`: human-readable, complete sentence, ends with period
- `details`: optional array, used when multiple field-level errors exist

Never expose stack traces, internal error codes, or database error messages in the response.

## Versioning

- Version in the URL path: `/v1/users`, `/v2/orders`
- Increment the major version only for **breaking changes** (removed fields, changed semantics)
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

## Request/Response Conventions

- `Content-Type: application/json` on all requests and responses with a body
- Field names in camelCase: `userId`, `createdAt`, `orderItems`
- Dates in ISO 8601 UTC: `"2026-03-27T10:00:00Z"`
- Never expose internal database IDs as the primary public identifier — use UUIDs or opaque IDs
```

- [ ] **Step 2: Verify content**

Check: resource naming section (with ✅/❌ examples), HTTP methods table, status codes table (10+ entries), error response JSON example, versioning rules, pagination JSON example.

- [ ] **Step 3: Commit**

```bash
git add skills/http-api-principles/SKILL.md
git commit -m "feat: add http-api-principles skill"
```

---

### Task 7: exception-principles Skill

**Files:**
- Create: `skills/exception-principles/SKILL.md`

- [ ] **Step 1: Create `skills/exception-principles/SKILL.md`**

```markdown
---
name: exception-principles
description: Opinionated exception handling standards — when to catch, how to log, error categorization, re-throw pattern, and recovery strategies
type: reference
---

# Exception Handling Principles

## Core Rules

1. **Catch only what you can handle.** If you cannot recover or add meaningful context, do not catch — let it propagate.
2. **Never swallow exceptions silently.** Every catch block must either re-throw, log, or return an error value. An empty catch block is always a bug.
3. **Log at the boundary.** Log once where the exception is finally handled, not at every level it passes through.
4. **Distinguish error categories.** Validation errors (user fault), operational errors (infrastructure fault), and programming errors (our fault) require different handling strategies.

## Error Categories

| Category | Examples | Response code | Log level | Stack trace |
|----------|---------|---------------|-----------|-------------|
| **Validation** | Missing field, invalid format, out-of-range value | 400/422 | None | No |
| **Not Found** | Resource doesn't exist | 404 | None | No |
| **Auth** | Invalid token, expired session, insufficient permission | 401/403 | WARN | No |
| **Operational** | DB down, network timeout, external API failure | 503 | ERROR | Yes |
| **Programming** | Null dereference, type error, assertion failure | 500 | ERROR | Yes |

## What to Log

Every logged exception must include:
- Error message
- Stack trace (for operational and programming errors)
- Request ID / correlation ID
- User ID (if authenticated and relevant)
- Relevant sanitized inputs (never passwords, tokens, or PII)

```typescript
// Good
logger.error("Failed to process payment", {
  error: err.message,
  stack: err.stack,
  requestId: ctx.requestId,
  userId: ctx.userId,
  orderId: order.id,
})

// Bad — no context
console.log(err)

// Bad — no detail
logger.error("Error occurred")

// Bad — logs at every level
try {
  await processPayment(order)
} catch (err) {
  logger.error("payment error", err)  // ← log here AND in the caller = duplicate
  throw err
}
```

## What NOT to Log

Never include in log output:
- Passwords, API tokens, session IDs, OAuth codes
- Full credit card numbers or CVVs
- PII: email addresses, phone numbers, physical addresses, SSNs
- Stack traces for validation errors (expected user mistakes, not bugs)

## Re-throw With Context

When catching to add context without fully handling, preserve the original exception chain:

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

Always use `{ cause: err }` (or language-equivalent) when re-throwing.

## Expected vs Unexpected Failures

Use return values for **expected, predictable failures**. Use exceptions for **unexpected failures**.

```typescript
// Good — parsing predictably fails, use return value
function parseDate(s: string): Result<Date, ParseError>

// Good — DB failure is unexpected, let it throw
async function fetchUser(id: string): Promise<User>

// Bad — exceptions for control flow
try {
  const user = await fetchUser(id)
} catch (err) {
  if (err instanceof NotFoundError) return null  // use findUserById that returns null instead
}
```

## Recovery Strategies

| Situation | Strategy | Notes |
|-----------|----------|-------|
| Transient network/DB failure | Retry with exponential backoff | Max 3 retries; log each attempt |
| Repeated failures from same dependency | Circuit breaker | Fail fast; don't hammer a down service |
| Non-critical feature fails | Fallback to degraded behavior | Only if degraded UX is acceptable |
| Validation error | Return error, no retry | User must fix input; retrying changes nothing |
| Programming error | Fail fast, alert | Never silently ignore; fix the bug |

Never retry validation errors or programming errors — they will not self-resolve.
```

- [ ] **Step 2: Verify content**

Check: 4 core rules, error categories table (5 rows with log level + stack trace columns), good/bad logging examples, what-not-to-log list, re-throw example (good + bad), expected vs unexpected failure examples, recovery strategies table.

- [ ] **Step 3: Commit**

```bash
git add skills/exception-principles/SKILL.md
git commit -m "feat: add exception-principles skill"
```

---

### Task 8: general-naming-principles Skill

**Files:**
- Create: `skills/general-naming-principles/SKILL.md`

- [ ] **Step 1: Create `skills/general-naming-principles/SKILL.md`**

```markdown
---
name: general-naming-principles
description: Opinionated naming conventions — variables, functions, classes, constants, files, and packages, with good/bad examples for each
type: reference
---

# General Naming Principles

## Core Rule

A name should tell the reader **what** something is or does without requiring them to look at the implementation. If a name needs a comment to explain it, rename it.

## Variables

- **camelCase** for mutable variables: `userList`, `orderCount`, `activeSession`
- **Descriptive nouns**: `user` not `u`, `errorMessage` not `msg`, `retryCount` not `n`
- **Boolean prefix with `is`, `has`, `can`, `should`**: `isActive`, `hasPermission`, `canDelete`, `shouldRetry`
- **Avoid single letters** except loop indices (`i`, `j`) and established conventions (`err`, `ctx`, `req`, `res`)
- **No abbreviations** unless universally known: `url`, `id`, `db`, `api`, `ctx` are fine — `usr`, `mgr`, `svc`, `cfg` are not

```typescript
// Good
const userList = await fetchUsers()
const isAuthenticated = checkAuth(token)
const hasPermission = user.roles.includes("admin")
const retryCount = 0

// Bad
const ul = await fetchUsers()
const auth = checkAuth(token)
const perm = user.roles.includes("admin")
const n = 0
```

## Functions and Methods

- **Verb + noun**: `createUser`, `fetchOrders`, `validateEmail`, `calculateTotal`
- **Query functions** (return values, no side effects): `getUser`, `findById`, `calculateTotal`, `formatDate`
- **Command functions** (side effects): `saveUser`, `deleteOrder`, `sendEmail`, `publishEvent`
- **Boolean functions** use predicate form: `isValid`, `hasExpired`, `canAccess`, `meetsRequirements`
- **Async functions** do not need an `async` prefix — the return type communicates it

```typescript
// Good
async function fetchUserById(id: string): Promise<User>
function validateEmail(email: string): boolean
function createOrderFromCart(cart: Cart): Order
async function sendWelcomeEmail(user: User): Promise<void>

// Bad
async function asyncGetUser(id: string)  // async prefix is redundant
function check(email: string): boolean   // too vague
function doOrder(cart: Cart): Order      // "do" is meaningless
function processUser(user: User)         // "process" tells nothing
```

## Classes, Types, and Interfaces

- **PascalCase**: `UserService`, `OrderRepository`, `PaymentError`, `SessionToken`
- **No `I` prefix for interfaces**: `UserRepository` not `IUserRepository`
- **No `Abstract` prefix**: `BaseRepository` not `AbstractRepository`
- **Suffix communicates role**:
  - `UserService` — business logic
  - `UserRepository` — data access
  - `UserController` — HTTP handler
  - `UserError` — domain error
  - `UserEvent` — event type
  - `UserDto` — data transfer object

## Constants

- **SCREAMING_SNAKE_CASE** for compile-time constants (never reassigned, module-level values):
  ```typescript
  const MAX_RETRY_COUNT = 3
  const DEFAULT_PAGE_SIZE = 20
  const SESSION_EXPIRY_SECONDS = 3600
  ```
- **camelCase** for runtime-determined "constants" (env vars, config loaded at startup):
  ```typescript
  const databaseUrl = process.env.DATABASE_URL
  const jwtSecret = config.get("jwt.secret")
  ```

## Files

- **kebab-case** for all file names: `user-service.ts`, `order-repository.ts`, `payment-error.ts`
- **File name matches its primary export**: `user-service.ts` exports `UserService`
- **Test files mirror source path and name**: `src/user-service.ts` → `tests/user-service.test.ts`
- **Index files for barrel exports only** — never put logic in `index.ts`

## Packages and Modules

- **kebab-case**: `my-library`, `order-service`, `auth-middleware`
- **Domain-specific, not generic** — avoid names like `utils`, `helpers`, `common`, `shared`:
  - ✅ `user-validation.ts` not `utils.ts`
  - ✅ `date-formatter.ts` not `helpers.ts`
  - ✅ `order-errors.ts` not `errors.ts`
- If you find yourself reaching for a `utils` file, ask whether the function belongs in the domain module that uses it most.
```

- [ ] **Step 2: Verify content**

Check: core rule statement, variables section (camelCase, boolean prefix, no-abbreviation rule with examples), functions section (verb+noun, query/command/boolean with examples), classes section (PascalCase, no I-prefix, suffix-by-role), constants section (SCREAMING_SNAKE vs camelCase), files section (kebab-case, test mirroring), packages section (no utils advice).

- [ ] **Step 3: Commit**

```bash
git add skills/general-naming-principles/SKILL.md
git commit -m "feat: add general-naming-principles skill"
```

---

### Task 9: principles-reviewer Agent

**Files:**
- Create: `agents/principles-reviewer.md`

- [ ] **Step 1: Create `agents/principles-reviewer.md`**

```markdown
---
name: principles-reviewer
description: Reviews code against all three hw0k-workflow principle skills simultaneously — HTTP API design, exception handling, and naming conventions.
type: agent
---

# Principles Reviewer

You are a code reviewer checking compliance with hw0k-workflow standards. Your job is to find and report violations clearly — not to fix them, explain them at length, or praise compliant code.

## Scope

Review against all three principle areas:

1. **HTTP API design** (`hw0k-workflow:http-api-principles`) — resource naming, HTTP methods, status codes, error response format, versioning, pagination
2. **Exception handling** (`hw0k-workflow:exception-principles`) — catch boundaries, logging requirements, error categorization, re-throw pattern, recovery strategies
3. **Naming conventions** (`hw0k-workflow:general-naming-principles`) — variables, functions, classes, constants, files, packages

## Before You Start

Read the three principle skills in full before reviewing any code:
- `hw0k-workflow:http-api-principles`
- `hw0k-workflow:exception-principles`
- `hw0k-workflow:general-naming-principles`

## Output Format

Structure your output with one section per principle area:

```
## HTTP API Design

### Violations
- `routes/users.ts:45` [method] — POST used for fetch: `app.post('/getUser', ...)` → use `GET /users/{id}`
- `handlers/orders.ts:102` [status code] — returns 200 for validation failure → use 400

### Passed
- Resource naming uses plural nouns consistently (`/users`, `/orders`)

---

## Exception Handling

### Violations
- `services/auth.ts:67` [swallowed exception] — catch block is empty, exception discarded
- `services/payment.ts:134` [log level] — validation error logged at ERROR level → no log or WARN only

### Passed
- Re-throw pattern uses `{ cause: err }` correctly in database layer

---

## Naming Conventions

No violations found.
```

## Violation Format

Each violation must include:
- **File and line**: `` `path/to/file.ts:42` ``
- **Rule in brackets**: `[method]`, `[status code]`, `[swallowed exception]`, `[boolean prefix]`, etc.
- **What was found**: quote or describe the offending code
- **What it should be**: the correction (brief)

## Instructions

1. Read all three principle skills before starting
2. Review every file in scope against all three areas
3. Report all violations — do not skip minor ones
4. Do **not** suggest fixes beyond the one-line correction in the violation entry
5. Do **not** explain the rules — the author can read the skills
6. If an area has no violations, write "No violations found."
7. If you cannot determine whether something is a violation from context alone, note it as "Unclear — may violate [rule], needs context"
```

- [ ] **Step 2: Verify content**

Check: 3 principle areas listed with skill names, "before you start" section, output format with realistic example (violations + passed + no violations), violation format spec (file:line, rule brackets, found/should-be), 7 instructions.

- [ ] **Step 3: Commit**

```bash
git add agents/principles-reviewer.md
git commit -m "feat: add principles-reviewer agent"
```

---

## Self-Review Against Spec

### Spec Coverage Check

| Spec requirement | Covered by |
|-----------------|------------|
| `plugin.json` metadata | Task 1 |
| `README.md` | Task 1 |
| `conventional-commit` skill | Task 2 |
| `sync-working-status` skill | Task 4 |
| `http-api-principles` skill | Task 6 |
| `exception-principles` skill | Task 7 |
| `general-naming-principles` skill | Task 8 |
| `commit.md` command → delegates to conventional-commit skill | Task 3 |
| `sync.md` command → delegates to sync-working-status skill | Task 5 |
| `principles-reviewer` agent → reviews against all 3 principles | Task 9 |
| Skills use `hw0k-workflow:{skill-name}` namespace | All skill tasks |
| Commands exposed for user-initiated workflow actions only | Tasks 3, 5 |
| Principle skills are reference guides (not commands) | Tasks 6, 7, 8 |

All 13 spec requirements covered. No gaps.

### Placeholder Scan

No TBDs, TODOs, "implement later", "fill in details", "add appropriate error handling", or "similar to Task N" patterns present. Every step contains complete content.

### Type Consistency

No shared types, function signatures, or method names across tasks — each task produces an independent markdown file. No consistency issues.
