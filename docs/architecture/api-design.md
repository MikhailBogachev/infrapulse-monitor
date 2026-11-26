# REST API Design

IP-005 · Stage 02 COMPLETED AND APPROVED · [AD-004](adr/adr-004-http-identity-and-spa.md)

All paths below use `/api/v1` except probes. Publish FastAPI OpenAPI with Pydantic request, response and error models. JSON field names use snake_case, identifiers are UUIDs, instants are RFC 3339 UTC and durations use explicit units. Verify input shape and field constraints before mutation. Responses use `application/json`, except empty 204s and errors. Use HTTPS at Nginx and same-origin requests. The [frontend design](frontend-design.md) maps these contracts to screens.

## Endpoint inventory

| Method and path | Access | Contract and success status |
|---|---|---|
| GET `/auth/registration` | Public | `200 {enabled}` reflects initialized installation and effective signup policy. |
| POST `/auth/register` | Public, operator-enabled, CSRF guard | `Credentials → 201 Account`. Creates initial workspace atomically and hands off to sign-in. Closed policy gives 403; unavailable email gives a generic 409. |
| POST `/auth/login` | Public, CSRF guard | `Credentials → 200 Access` and refresh cookie. Invalid credentials give 401. |
| POST `/auth/refresh` | Refresh credential, CSRF guard | `{} → 200 Access` and replacement cookie. Invalid, expired or spent token gives 401. |
| POST `/auth/logout` | Refresh cookie when present, CSRF guard | `{} → 204`. Revoke recognized session and clear cookie. |
| GET `/users/me` | Bearer | `200 Account`. Read-only account fields. |
| GET `/workspaces` | Bearer | `200 Page<Workspace>` with owned workspaces. |
| GET, PATCH `/workspaces/{id}` | Owner | `200 Workspace`. PATCH accepts `{name}` only. Bootstrap/signup provisions workspaces. Authorized workspace destruction is an offline operator procedure for retention. |
| GET `/monitors?workspace_id=…` | Owner | `200 Page<MonitorSummary>`. Optional `state` filter. |
| POST `/monitors` | Owner | `{workspace_id, ...MonitorInput} → 201 Monitor`, with Location. |
| GET, PATCH, DELETE `/monitors/{id}` | Owner | `200 Monitor` for read or partial configuration edit. DELETE gives 204 after scoped removal. |
| POST `/monitors/{id}/pause`, `/monitors/{id}/resume` | Owner | `{} → 200 Monitor`. Repeating an already applied action returns current state without a new lifecycle transition. |
| POST `/monitors/{id}/checks` | Owner | `{} → 202 Execution`, with Location to execution detail. Paused or busy gives 409 and an acceptance limit gives 429. |
| GET `/monitors/{id}/checks` | Owner | `200 Page<Observation>` for completed history. Filters `from`, `to`, `origin` and `outcome`. |
| GET `/monitors/{id}/checks/{execution_id}` | Owner | `200 Execution` with progress and retained committed result when present. |
| GET `/monitors/{id}/metrics?window=24h\|7d\|30d` | Owner | `200 Metrics`, default window 24h. |
| GET `/incidents?workspace_id=…` | Owner | `200 Page<Incident>`. Filters `status=OPEN\|CLOSED`, `monitor_id`, `close_reason`, `from` and `to` by opening time. A retained deleted monitor ID may be used within its workspace. |
| GET `/incidents/{id}` | Owner | `200 Incident`. Associated deliveries are fetched through the scoped listing. |
| GET, PATCH `/notifications/telegram?workspace_id=…` | Owner | `200 Channel` including an unconfigured state. PATCH creates or updates explicitly supplied fields. Disabling sets `enabled=false`. |
| GET `/notifications/deliveries?workspace_id=…` | Owner | `200 Page<Delivery>`. Optional `incident_id`, `status`, `from` and `to` by creation time. Settings can select FAILED and UNKNOWN dispositions. |
| GET `/dashboard?workspace_id=…` | Owner | `200 Dashboard` with state counts and bounded recent observation and incident summaries. |
| GET `/health/live` | Infrastructure | `200 {status:"live"}` when the API event loop serves requests. |
| GET `/health/ready` | Infrastructure | `200 {status:"ready"}` or `503`. Checks required API dependencies per [deployment design](deployment-design.md#startup-shutdown-and-health). |

Resource paths derive workspace from the scoped database join. Collection and create routes apply the explicit workspace ID against current ownership. No workspace mutation can set ownership or installation policy. The operator procedures and CSRF rules appear in [security design](security-design.md#identity-and-sessions).

## Schemas and conventions

| Shape | Fields and invariants |
|---|---|
| Credentials / Account / Access | Credentials `{email, password}`. Account `{id,email,created_at}`. Access `{access_token,token_type:"bearer",expires_in:900}`. Cookie is set separately. |
| Workspace | `{id,name,created_at,updated_at}`. |
| MonitorInput | `{name,url,method,interval_seconds,timeout_seconds,failure_threshold,recovery_threshold}`. Name and URL required on create. GET/HEAD default GET, interval 30–86400 default 60, timeout 1–30 default 10 and capped by interval, positive thresholds default 3/2. PATCH validates the complete merged object. Read-only state, diagnostics and ownership are forbidden in update input. |
| MonitorSummary / Monitor | Summary `{id,workspace_id,name,state,next_check_at,latest_manual_execution}` with nullable schedule and execution summary. Detail adds MonitorInput values, `configuration_version,created_at,updated_at`. PAUSED returns null next due. The detail GET supports polling of progress alongside metrics/history. |
| Execution / Observation | Execution `{id,monitor_id,origin,status,accepted_at,due_at,started_at,ended_at,diagnostic_code,result}`. Result nullable, with `{execution_id,monitor_id,origin,completed_at,outcome,duration_us,http_status,diagnostic_code,metrics_eligible,stale_reason}`. Origin is SCHEDULED or MANUAL, outcome is SUCCESS/FAILURE/TIMEOUT/ERROR. Execution-only SKIPPED and INTERRUPTED remain observable as dispositions. |
| Incident | `{id,workspace_id,monitor_id,monitor_name,monitor_deleted,affected_origin,opened_at,closed_at,close_reason}`. Closed reasons RECOVERED, MONITOR_DELETED or CONFIGURATION_CHANGED. Open status is derived from null `closed_at`. |
| Channel | `{configured,enabled,incident_opened,incident_resolved,updated_at}`. PATCH additionally accepts write-only `bot_token,chat_id` when configuring/replacing. Omitted values preserve stored fields. Enabling requires a complete channel. Responses show only configuration presence. |
| Delivery | `{id,incident_id,event,status,attempt_count,created_at,settled_at,diagnostic_code}`. Status follows the [delivery state machine](backend-design.md#notification-engine). |
| Metrics | `{window,from,to,uptime_percent,successful,failed,timeout,excluded_by_reason,latency_sample_count,average_latency_us,p95_latency_us,p99_latency_us,known_missed_slots,missing_slot_count,paused_seconds}`. Failed and timeout counts are disjoint, and both enter the uptime denominator. Null values carry no-data or insufficient-sample semantics. |
| Dashboard | `{as_of,state_counts,recent_observations,recent_incidents}`. Initial limit ten items per recent collection. Use detail and list routes for exploration. |

Verify settings errors without changing accepted configuration. Apply PATCH under the monitor row lock using the current values. Require `expected_configuration_version` on configuration PATCH and give 409 with code `stale_configuration` if the version has changed. Validate MonitorInput exactly as [Q-02](../product/prd.md#q-02) and the destination policy prescribe. Apply the [approved lifecycle](../product/business-rules.md#monitor-lifecycle) to URL changes. An accepted URL edit while PAUSED returns the updated configuration version and PAUSED state, closes any open incident as CONFIGURATION_CHANGED and starts no automatic check. Resume later returns PENDING.

## Filtering and cursor pagination

List envelopes are `{items,next_cursor}`. Default page size 50, maximum 100, and empty collections return an empty array with null cursor. Order observations by `(completed_at, execution_id)`, incidents by `(opened_at, id)`, deliveries by `(created_at,id)`, all descending. Workspaces and monitors use ascending ID order. Apply exclusive keyset continuation across equal timestamps with the UUID tie-breaker. Time filters use inclusive lower and exclusive upper bounds. History is clipped to the current retention window. A cursor binds its version, endpoint, subject, tenant, resource, filter fingerprint, first-page time bound, expiry and sort tuple with a MAC. Reject malformed, expired or mismatched cursors and reauthorize on every page. New polling starts from the first page. Continuations exclude newer observations by time fence and can reflect concurrent deletion, expiry, or changes in mutable filter values. No DB snapshot spans HTTP requests.

## Error contract

Use RFC 9457 Problem Details with media type `application/problem+json`, stable local `type` URI, `title`, HTTP `status`, safe English `detail`, opaque `instance` request reference, `code` and optional `errors: [{field,code,message}]`. Provide the code/field extensions in OpenAPI. Never reflect raw exception text, input secrets or foreign resource existence.

| HTTP status | Examples |
|---|---|
| 400 | Invalid or mismatched cursor. |
| 401 | Missing/invalid bearer (with Bearer challenge for protected operations), invalid credentials or unusable refresh token. |
| 403 | Closed signup, origin/CSRF violation or an operation explicitly forbidden to an authenticated principal in scope. |
| 404 | Absent, tombstoned or foreign resource, or expired execution record. |
| 409 | Monitor busy/paused for manual run, stale configuration precondition, conflicting settings state or generic account conflict. |
| 422 | Invalid body, field relation, filter or rejected deterministic URL policy. No changes saved. |
| 429 | Rate policy reached, with actionable `Retry-After`. |
| 503 | Dependency or lifecycle guard unavailable within budget. Retry safety depends on operation and authoritative outcome. |

[Product flows UF-001–UF-020](../product/user-flows.md#uf-001) specify the user journeys. Workspace isolation, refresh and outbox-backed manual acceptance are verified through the corresponding [architecture mapping](system-architecture.md#requirements-and-verification-map).
