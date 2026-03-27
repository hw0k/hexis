# http-api-principles — Examples

Extended examples for the `http-api-principles` skill.

## URL Structure Examples

```
# Single resource
GET    /users/{id}
PUT    /users/{id}
DELETE /users/{id}

# Collection
GET  /users
POST /users

# Nested (max 2 levels)
GET  /users/{id}/orders
POST /users/{id}/orders
GET  /users/{id}/orders/{orderId}

# Action on resource (POST + noun path when no REST method fits)
POST /users/{id}/password-reset
POST /orders/{id}/cancellation
```

## Error Response Examples

**400 Validation Error (multiple fields):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid fields.",
    "details": [
      { "field": "email", "message": "must not be blank" },
      { "field": "email", "message": "must be a valid email address" },
      { "field": "age", "message": "must be at least 18" }
    ]
  }
}
```

**404 Not Found:**
```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "No user exists with the given ID.",
    "details": []
  }
}
```

**401 Unauthorized:**
```json
{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "The provided authentication token is invalid or has expired.",
    "details": []
  }
}
```

**500 Internal Server Error (never expose internals):**
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred. Please try again later.",
    "details": []
  }
}
```

## Pagination Examples

**Request:**
```
GET /orders?limit=20&cursor=eyJpZCI6MTIzfQ==
```

**Response:**
```json
{
  "data": [
    { "id": "ord_124", "status": "shipped", "createdAt": "2026-03-27T10:00:00Z" },
    { "id": "ord_123", "status": "delivered", "createdAt": "2026-03-26T08:30:00Z" }
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
GET /orders?limit=500
→ 400 Bad Request
{
  "error": {
    "code": "INVALID_PAGINATION",
    "message": "limit must not exceed 100.",
    "details": [{ "field": "limit", "message": "must be at most 100" }]
  }
}
```

## Versioning and Deprecation Headers

```
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 01 Jan 2028 00:00:00 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
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
```
