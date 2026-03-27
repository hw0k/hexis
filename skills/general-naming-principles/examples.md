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
