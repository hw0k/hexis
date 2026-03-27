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
