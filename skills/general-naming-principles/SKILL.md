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

For before/after naming comparisons by language and class/interface examples, see [examples.md](references/examples.md).
