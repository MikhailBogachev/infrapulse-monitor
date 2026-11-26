# ADR-004 · REST, Session Security and SPA Integration

**Status:** APPROVED baseline · AD-004, AD-005 and AD-011 · owner approval in IP-005.

## Context

The SPA needs predictable contracts, scoped history and secure continuity across access expiry and concurrent browser requests.

## Decision

Use same-origin REST under `/api/v1`, OpenAPI, RFC 9457 errors and signed keyset cursors. Keep a 15-minute access JWT in memory and rotate a seven-day opaque refresh credential through an HttpOnly cookie. Revoke session families on logout or recognized reuse, require CSRF protection, and enforce current workspace ownership. Use React Router and TanStack Query for navigation and polled server state. See [API](../api-design.md), [Security](../security-design.md) and [Frontend](../frontend-design.md).

## Alternatives

Persistent browser token storage exposes secrets to a larger script and storage surface. Offset pagination grows cost and shifts under inserts. A global client store would duplicate existing server-state responsibilities. RLS could add defense in depth with additional session and policy operational complexity.

## Consequences

Cookie renewal needs cross-tab coordination. Access validation consults PostgreSQL. Cursor continuations reauthorize and observe retention. Visual design and responsive layout details remain with Stage 03.
