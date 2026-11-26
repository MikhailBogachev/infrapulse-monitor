# Frontend Architecture

IP-005 · Stage 02 COMPLETED AND APPROVED · [AD-011](adr/adr-004-http-identity-and-spa.md)

The React/TypeScript SPA uses React Router, TanStack Query, React Hook Form, Zod and Lucide React. Tailwind CSS and shadcn/ui supply Dark Only primitives and Recharts presents the approved metrics. English copy, WCAG 2.2 AA, keyboard operation, visible focus, contrast and status distinctions beyond color are baseline. Support desktop-first responsive workflows at the approved 360, 768, 1024 and 1440 px reference widths. Stage 03 owns screen layouts, breakpoints, and accessible chart/table presentation.

| Directory | Responsibility |
|---|---|
| `app/` | Router, query client, auth provider, error boundary and application shell |
| `pages/` | Route composition and route-level loading/failure states |
| `features/` | Auth, workspaces, dashboard, monitors, incidents and notifications, each with API hooks and relevant forms |
| `components/` | Shared controls, status, tables and accessible chart wrappers |
| `hooks/` | Reusable cross-feature behavior for freshness and interaction |
| `lib/` | Same-origin API client, Problem Details parser and auth coordination |
| `types/` | Shared API DTOs checked against OpenAPI contracts |

TanStack Query owns server state and invalidation. Use component state and form state for local interaction. No separate global store is required. Parse form input in Zod and retain server authority for validation, including URL policy. React Hook Form maintains existing values on failed patches.

## Routing and API integration

| Browser route | Screen and integration |
|---|---|
| `/sign-in`, `/sign-up` | UI-001/002, credential forms and effective registration availability |
| `/w/:workspaceId` | UI-003, dashboard state, recent observations and incidents |
| `/w/:workspaceId/monitors` | UI-004, monitor list and manual progress |
| `/w/:workspaceId/monitors/new`, `/w/:workspaceId/monitors/:id/edit` | UI-005, monitor forms and configuration precondition |
| `/w/:workspaceId/monitors/:id` | UI-006, configuration, result history, manual progress and metrics |
| `/w/:workspaceId/incidents`, `/w/:workspaceId/incidents/:id` | UI-007/008, active/recovered incident evidence and associated deliveries |
| `/w/:workspaceId/settings/notifications` | UI-009, Telegram configuration and delivery disposition |
| `/account`, `/w/:workspaceId/settings` | UI-010/011, self view/logout and permitted workspace controls |

Use the [API contracts](api-design.md#endpoint-inventory). Resolve workspace membership before loading scoped features. Signed-out navigation may keep a same-origin return path, reauthorized after sign-in. Map field errors to controls, preserve confirmed data on transient errors, and replace views with appropriate access/missing states after an authoritative denial. Invalidate relevant current workspace keys on accepted mutations. On a stale-configuration conflict fetch current configuration and preserve the user's input for reconciliation. Show diagnostic-only manual handling from 202/409/429 and poll until terminal. After an ambiguous mutation response, reload authoritative state before permitting an explicit retry.

## Authentication and cache isolation

Start with an unknown session. On reload, try same-origin refresh before protected queries, then fetch self and owned workspaces. Hold access JWT in memory and send it as Authorization. Credential endpoints use the required same-origin header and JSON payload. Coalesce refresh within a tab and serialize refresh, login and logout across same-origin tabs through Web Locks on supported browsers. Web Locks is a candidate requirement for the supported browser matrix. Stage 04 must verify the matrix or select an equivalent cross-tab coordinator that preserves renewal and reuse protection. Do not share credentials through broadcast or persistent storage. Broadcast logout/session-change signals without token values.

Renew a known-expiring token before protected mutations. After 401, refresh once and replay safe reads once when the session remains current. Mutations with uncertain outcomes are reloaded and explicitly resubmitted by the user when appropriate. A failed renewal ends the local authenticated view. Report server-side logout success only after the API acknowledges revocation. On logout or session change cancel requests, bump the local auth generation, remove prior user queries and navigate after clearing the token. On workspace switch cancel in-flight requests and clear old scoped query state. Late responses from stale generations or workspaces never populate the current view.

Query keys include user/session cache generation, workspace ID, domain, resource ID and normalized filters/window including pagination context. Query functions capture the same scope and pass an AbortSignal. Keep caches in memory. Never show data from a previous workspace as placeholder data during a switch. HTTP responses containing account or workspace data use no-store.

## Data freshness

Per the [MVP polling scope](../product/user-flows.md#mvp-polling-scope), refresh operational data on UI-003, UI-004, UI-006, UI-007, UI-008 and UI-009 every ten seconds while open and executable in the browser. Including delivery queries on UI-008/009 is required. Use one in-flight request per key. Keep query-local last-success time and show a stale indicator after 30 seconds without a successful refresh. Separate initial loading/empty state from a failed refresh of retained data. Run manual refresh and refresh on reconnect, focus or tab resume after timer throttling. Refresh first pages without refreshing loaded archival pages repeatedly. Provide browse controls for history. Drop or reset stale cursors when filters change or retention makes them invalid. Beta SSE and expanded analytics remain later-release designs.

Verify scope-switch races, simultaneous auth refresh, expired tokens, data staleness and recovery, mutation errors, and keyboard/mobile journeys through the [mapped acceptance criteria](system-architecture.md#requirements-and-verification-map).
