# http-api-principles — Examples

Extended examples for the `http-api-principles` skill.

## URL Structure Examples

```
# Single resource
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
DELETE /api/v1/users/{id}

# Collection
GET  /api/v1/users
POST /api/v1/users

# Nested (max 2 levels)
GET  /api/v1/users/{id}/orders
POST /api/v1/users/{id}/orders
GET  /api/v1/users/{id}/orders/{orderId}

# kebab-case multi-word resources
GET  /api/v1/user-profiles
GET  /api/v1/order-items/{id}

# Action on resource (POST + noun path when no REST method fits)
POST /api/v1/users/{id}/password-reset
POST /api/v1/orders/{id}/cancellation
```

## Query Parameter Examples

```
# camelCase, case-sensitive
GET /api/v1/orders?pageSize=20&sortBy=createdAt&includeArchived=false
GET /api/v1/products?categoryId=42&status=ACTIVE
GET /api/v1/users?cursor=eyJpZCI6MTIzfQ==&pageSize=20

# status=ACTIVE and status=active are different values — server is case-sensitive
```

## Enum Examples

```json
// Bad — requires external reference to interpret the integer values
{ "status": 1, "priority": 3 }

// Good — self-documenting
{ "status": "ACTIVE", "priority": "HIGH" }
```

## Error Response Examples (RFC 9457)

**400 Validation Error (multiple fields):**
```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The request contains invalid fields.",
  "errors": [
    { "field": "email", "message": "must not be blank" },
    { "field": "email", "message": "must be a valid email address" },
    { "field": "age", "message": "must be at least 18" }
  ]
}
```

**404 Not Found:**
```json
{
  "type": "https://api.example.com/errors/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "No user exists with the given ID."
}
```

**401 Unauthorized:**
```json
{
  "type": "https://api.example.com/errors/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "The provided authentication token is invalid or has expired."
}
```

**500 Internal Server Error (never expose internals):**
```json
{
  "type": "https://api.example.com/errors/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred. Please try again later."
}
```

## Pagination Examples

**Request:**
```
GET /api/v1/orders?pageSize=20&cursor=eyJpZCI6MTIzfQ==
```

**Response:**
```json
{
  "data": [
    { "id": "ord_124", "status": "SHIPPED", "createdAt": "2026-03-27T10:00:00Z" },
    { "id": "ord_123", "status": "DELIVERED", "createdAt": "2026-03-26T08:30:00Z" }
  ],
  "pagination": {
    "cursor": "eyJpZCI6MTIzfQ==",
    "hasMore": false,
    "limit": 20
  }
}
```

**Reject over-limit:**
```
GET /api/v1/orders?pageSize=500
→ 400 Bad Request

{
  "type": "https://api.example.com/errors/invalid-pagination",
  "title": "Invalid Pagination",
  "status": 400,
  "detail": "pageSize must not exceed 100.",
  "errors": [{ "field": "pageSize", "message": "must be at most 100" }]
}
```

## Versioning and Deprecation Headers

```
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 01 Jan 2028 00:00:00 GMT
Link: <https://api.example.com/api/v2/users>; rel="successor-version"
```

## Status Code Decision Guide

| Situation | Code |
|-----------|------|
| GET success with body | 200 |
| POST created resource | 201 |
| DELETE success / PUT with no body | 204 |
| Missing required field | 400 |
| Invalid format | 400 |
| No auth token | 401 |
| Valid token, wrong permissions | 403 |
| Resource not found | 404 |
| Duplicate resource | 409 |
| Syntactically valid but semantically wrong | 422 |
| Rate limit | 429 |
| Unexpected server failure | 500 |
| Downstream dependency unavailable | 503 |
