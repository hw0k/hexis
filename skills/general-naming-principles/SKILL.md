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

## Extended Examples

For before/after naming comparisons, file naming patterns, class/interface examples, and constants reference, see [examples.md](examples.md).
