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

## Extended Examples

For full JSON error response examples, pagination request/response examples, URL structure patterns, and status code decision guide, see [examples.md](examples.md).