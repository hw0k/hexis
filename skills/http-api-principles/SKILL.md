---
name: http-api-principles
description: Opinionated HTTP API design standards — Richardson Level 2, /api/{version}/{resource} URL signature, JSON camelCase, RFC 9457 errors, and resource-centric modeling
type: reference
---

# HTTP API Design Principles

## Maturity Target

Target **Richardson Maturity Model Level 2** — HTTP verbs and resources. Level 3 (HATEOAS) is explicitly out of scope; complexity overhead exceeds practical benefit for most production APIs.

## URL Structure

**Required signature:** `/api/{version}/{resource}`

- The URL must identify itself as an API:
  - ✅ `api.example.com/v1/users`
  - ✅ `booking-api.example.com/v1/orders`
  - ✅ `example.com/api/v1/users`
  - ❌ `example.com/users` — not identifiable as an API from the URL alone
- **Ordering principle:** segments go from least-to-most frequently changing — `api` → `version` → `resource`. This is the rationale for the structure, not arbitrary convention.
- URI segments: **kebab-case**
- Nest to show ownership, max 2 levels deep: `/api/v1/orders/{id}/items`
- Use **plural nouns** for collections: `/users`, `/orders`, `/products`
- **Never use verbs in URLs:**
  - ❌ `/api/v1/getUser`, `/api/v1/createOrder`
  - ✅ `GET /api/v1/users/{id}`, `POST /api/v1/orders`
- IDs belong in the path, not the query: `/api/v1/users/{userId}` not `/api/v1/users?id={userId}`

## Query Parameters

- Use **camelCase**: `?pageSize=20`, `?sortBy=createdAt`, `?includeArchived=true`
- API server must be **case-sensitive**: `?status=READY` and `?status=ready` are distinct values
- Boolean params: `true` / `false` strings

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

## Request/Response Body

- `Content-Type: application/json` required on all requests and responses with a body
- JSON field names: **camelCase** (`userId`, `createdAt`, `orderItems`)
- If the backend language uses `snake_case`, convert at the serialization layer:
  - Python/Django: `djangorestframework-camel-case`
  - Go: `json:"fieldName"` struct tags
  - Spring Boot: `spring.jackson.property-naming-strategy=LOWER_CAMEL_CASE`
- Dates in ISO 8601 UTC: `"2026-03-27T10:00:00Z"`
- Never expose internal database IDs as the primary public identifier — use UUIDs or opaque IDs

## Enum Values

Represent enums as **strings**, not integers.

- ❌ `"status": 1` — requires external reference to interpret
- ✅ `"status": "READY"` — self-documenting

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

Follow **RFC 9457 (Problem Details for HTTP APIs)**. Minimum required fields:

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The request contains invalid fields.",
  "errors": [
    { "field": "email", "message": "must not be blank" }
  ]
}
```

- `type`: URI identifying the error class (absolute URL or relative path)
- `title`: human-readable summary, same for all instances of this error type
- `status`: HTTP status code as integer
- `detail`: human-readable explanation of this specific occurrence
- Additional members allowed (e.g., `errors` for field-level details)

Never expose stack traces, internal error codes, or database error messages.

## Resource-Centric Mapping

APIs represent **domain resources**, not database tables. Internal implementation details (table structure, JOIN strategy, column names) must not leak into the API surface.

- ✅ `GET /api/v1/orders/{id}/items` — `items` is a sub-resource of `Order`
- ❌ Exposing an `order_items` table directly with DB column names as field names

Design the API around the domain model. The database is an implementation detail.

## Consistency

The same concept must use the same name across the entire API. Align with the `general-naming-principles` consistency rule.

```
# Bad — same concept, inconsistent names
GET /api/v1/orders?userId=123
GET /api/v1/products?user_id=123   ← inconsistent field name AND casing

# Good
GET /api/v1/orders?userId=123
GET /api/v1/products?userId=123
```

## Versioning

- Version in the URL path as part of the required signature: `/api/v1/...`
- Increment major version only for **breaking changes** (removed fields, changed semantics)
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

## Reference

[Microsoft REST API Design Guidelines](https://learn.microsoft.com/ko-kr/azure/architecture/best-practices/api-design)

## Extended Examples

For URL structure examples, error response variations, enum and query parameter examples, pagination examples, and status code decision guide, see [examples.md](examples.md).
