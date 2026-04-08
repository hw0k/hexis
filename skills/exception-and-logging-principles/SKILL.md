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

For annotated multi-layer re-throw chains, retry/circuit-breaker patterns, correlation ID flow, and before/after comparisons, see [examples.md](references/examples.md).
