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
