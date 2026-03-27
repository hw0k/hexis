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
