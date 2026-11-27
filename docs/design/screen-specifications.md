# MVP screen specifications

IP-006 · MVP v0.1.0 · Stage 03 COMPLETED AND APPROVED

Routes and navigation come from the [information architecture](information-architecture.md). API paths below are relative to `/api/v1`. The [endpoint inventory](../architecture/api-design.md#endpoint-inventory), [schemas and conventions](../architecture/api-design.md#schemas-and-conventions) and [error contract](../architecture/api-design.md#error-contract) are authoritative. All screens inherit the [responsive layout](responsive-design.md), [accessibility checks](accessibility.md) and shared trace to [NFR-027–030](../product/srs.md#nfr-027) and [AC-091–094](../product/acceptance-criteria.md#ac-091). All workspace data inherits [NFR-001](../product/srs.md#nfr-001) and [AC-010](../product/acceptance-criteria.md#ac-010).

## UI-001

**Sign In ·** `/sign-in` · Sign-out, protected deep link, or post-registration entry.

- Center a single card with brand, email, password, Sign in and registration availability. Show setup-required guidance when the operator context establishes an uninitialized installation. Bootstrap executes through the approved trusted terminal and ends at Sign In.
- Read effective policy with `GET /auth/registration`. Submit `POST /auth/login`. On eligible recovery use `POST /auth/refresh`, then `GET /users/me` and `GET /workspaces` before opening the authorized destination. The API supplies no public bootstrap status or mutation.
- Require email and password, preserve the email on failure, show a generic credential error on 401 and show retry timing on 429. Announce expired session and provide explicit sign-in. While initial session resolution runs, withhold protected content.
- Keep a single fluid column with persistent labels, email and password autocomplete, paste and password-manager support, and error focus. Give the card room to scroll on short screens.

## UI-002

**Sign Up ·** `/sign-up` · From the registration entry on Sign In.

- Display a single credential card when eligible. A closed policy presents “Registration is closed” and a return to Sign In.
- `GET /auth/registration` determines eligibility. Use `POST /auth/register` to create the account and first owned workspace. A 201 hands off to Sign In. A 403 updates the state if the policy changed. Show a generic 409 conflict and 429 retry guidance.
- Use labeled, required email and password inputs and consistent validation. Preserve the email on known invalid input and keep the return action visible within the authentication card at mobile widths.

## UI-003

**Overview ·** `/w/:workspaceId` · Default authorized landing page and sidebar entry.

- Show total monitors, UP and DOWN counts, active incident count and a breakdown for all four states. Provide a current monitor overview, bounded active incident summaries, freshness and New monitor. Preserve the API boundary of recent summaries; link to Incidents for the full open list when the bounded dashboard response cannot provide every open item. Use the authorized open incident collection for this count. When a continuation remains, label the count as a lower bound, such as “50+”, and link to the open list.
- Show selected-monitor response time and uptime for 24h, 7d and 30d. Use `GET /dashboard`, `GET /monitors`, `GET /incidents?status=OPEN`, and selected-monitor `GET /monitors/{id}/metrics` and `GET /monitors/{id}/checks`. Use the scope and range conventions from [data visualization](interaction-patterns.md#data-visualization).
- Show first-load, empty workspace, first-load error, retained error/stale and per-chart No data. A failed or missing metrics series leaves monitor and incident statuses independent.
- Use four KPI cards across where space permits, plus a chart and status/incident rail. On phones stack panels in reading order and keep text totals and a chart data disclosure.

## UI-004

**Monitors List ·** `/w/:workspaceId/monitors` · Sidebar or Overview → All monitors.

- Show name, current state, next check in UTC, latest manual status and row actions. Provide New monitor, name search, status filter, detail, edit, pause/resume and manual request. Delete confirmation lives on Monitor Details.
- `GET /monitors?workspace_id=…&state=…` supports state and cursor pagination. Search matches loaded monitor names locally; the MVP API has no name search parameter. Clearly scope search results to loaded records and allow loading more within the current status filter. Actions use `POST /monitors/{id}/pause`, `/resume` and `/checks`, with execution detail read when needed.
- Distinguish empty workspace from zero matches. Keep cleared filters recoverable and announce result changes during text search. Handle 409 busy/paused and 429 rate limit. Refresh against the selected filters and preserve search input.
- Keep keyboard-accessible table headers, action names and a named scroll region on narrow screens. Keep New monitor and filters outside the horizontal region.

## UI-005

**Create / Edit Monitor ·** `/w/:workspaceId/monitors/new` and `/w/:workspaceId/monitors/:id/edit` · From Overview, Monitors or Monitor Details.

- Use separate pages with Target, Check schedule and Incident thresholds. Fields are name, HTTP(S) URL, GET/HEAD, interval, timeout and consecutive failure/recovery thresholds. The default values are GET, 60 s, 10 s, 3 and 2. HTTP 2xx indicates success. Describe TLS verification and disabled redirects in static help.
- Create through `POST /monitors` with workspace scope; the resulting monitor starts PENDING. Edit uses `GET /monitors/{id}` and `PATCH /monitors/{id}` with `expected_configuration_version`. Render the authorized response and route to details. Cancel returns to the source list or detail.
- Require name and a valid HTTP(S) URL without embedded credentials or fragment. Apply interval 30–86,400 s, timeout 1–30 s and at most the interval, and positive whole-number thresholds. The API remains authoritative for URL policy and merged values. On 422 preserve the draft and mark affected controls. On stale version 409 load the current configuration alongside the draft for explicit reconciliation. Show the URL confirmation and lifecycle consequences before saving.
- Put labels and errors next to each input. Use two columns for paired numbers, stack on phones, and keep actions after the form in focus order.

## UI-006

**Monitor Details ·** `/w/:workspaceId/monitors/:id` · From Overview, monitor list, incident detail or form success.

- Show current state, target, method, configuration, schedule, uptime, average latency, p95 and p99, chart, manual progress, check history and incident history. Offer Run check now, Pause/Resume, Edit and Delete.
- Use `GET /monitors/{id}`, `GET /monitors/{id}/metrics?window=…`, `GET /monitors/{id}/checks`, `GET /monitors/{id}/checks/{execution_id}` and `GET /incidents?workspace_id=…&monitor_id=…`. Mutations use the monitor DELETE and the pause, resume and manual POST routes. Follow the returned execution location and expose safe progress until terminal.
- Use separate no-observation, manual ineligible/busy/rate-limited, canceled/stale observation and retained snapshot states. Give the confirmed consequences in deletion and pause dialogs. Display platform errors as internal faults and preserve last confirmed monitor state.
- Keep context and actions before metrics in DOM order. Actions wrap; KPI cards become two columns, and history tables use labeled scroll regions. Supply explicit text for null metrics and gaps.

## UI-007

**Incidents List ·** `/w/:workspaceId/incidents` · Sidebar or Overview → View all.

- List incident monitor snapshot, open/closed status, UTC times and close reason. Order by opening time descending and link each row to details. Keep recovered, configuration-changed and deleted-monitor dispositions distinct.
- Use `GET /incidents?workspace_id=…`, with supported status and cursor parameters; scope monitor-based links through `monitor_id`. A filtered empty result keeps the filter controls available. A transient refresh failure retains confirmed rows.
- Keep Status and Incident history above a named scroll region. Convey state and close reason in readable text with a status icon.

## UI-008

**Incident Details ·** `/w/:workspaceId/incidents/:id` · From the dashboard, incidents, monitor history or delivery issues.

- Show affected origin and monitor snapshot, UTC opening and closing times, open/closed state and close reason. Link only to a current authorized monitor. Present associated delivery event, disposition, attempts, timestamps and safe diagnostics where returned.
- Use `GET /incidents/{id}` and `GET /notifications/deliveries?workspace_id=…&incident_id=…`. Poll disposition and deliveries, each with its own freshness in production. Missing or foreign incident returns the shared access state. Mark a removed monitor as deleted while retaining historical context.
- Keep timeline before deliveries at every width and show a labeled empty state if no delivery exists. Label UNKNOWN as “Unknown” and explain that provider acceptance could not be confirmed.

## UI-009

**Notification Settings ·** `/w/:workspaceId/settings/notifications` · Sidebar or Workspace settings.

- Show configured/enabled status, write-only bot token and chat ID, enabled action, and Incident opened/resolved preferences. Defaults are enabled for both events on initial setup. Delivery issues show FAILED and UNKNOWN dispositions with safe event and attempt details.
- `GET/PATCH /notifications/telegram?workspace_id=…` reads and replaces supplied settings. Blank replacement fields omit those keys. Require a complete destination before enabling. Use scoped `GET /notifications/deliveries` with FAILED and UNKNOWN filtering. There is no provider test action or manual resend.
- Keep draft fields untouched when delivery polling, confirm disabling and report the saved status after the accepted patch. On error retain the settings draft without reflecting secret values in messages. Link delivery issues to Incident Details.
- Settings and activity stack on a narrow screen. Use labels and a fieldset for event preferences. Provide “configured” presence in text and never render stored secret material.

## UI-010

**Account Settings ·** `/account` · Avatar or sidebar Account.

- Show the currently authorized email and account creation timestamp through `GET /users/me`. Sign out through `POST /auth/logout`. Clear session and cached scope and hand off to Sign In. Only acknowledge revocation after the API confirms it.
- Show a loading or failure state when self data is unresolved. On session expiry use the shared recovery path. Display account values as readable text and keep Sign out accessible on phones. Editable account fields remain deferred.

## UI-011

**Workspace Settings ·** `/w/:workspaceId/settings` · Sidebar Workspace or the workspace card.

- Show current workspace name and the Notifications entry. Edit only the workspace name through scoped `GET/PATCH /workspaces/{id}`. Update the workspace name in the shell after a successful save.
- Require a nonblank name, preserve the draft on error and show a success message. Apply generic access feedback on an authoritative denial. Installation registration and destination policy remain operator procedures.
- Use a single column and a labeled input with adjacent field help and validation. Keep Save changes and the Notification settings entry available on phones.

## Requirements by screen

The common requirements above apply in addition to this MVP-specific mapping. Request timing, authentication security and egress controls require integrated acceptance evidence.

| Screen | Requirements | Acceptance | Flows |
|---|---|---|---|
| [UI-001](#ui-001) | [FR-001–007](../product/srs.md#fr-001), [FR-009](../product/srs.md#fr-009) | [AC-001–007](../product/acceptance-criteria.md#ac-001), [AC-009](../product/acceptance-criteria.md#ac-009) | [UF-001–006](../product/user-flows.md#uf-001) |
| [UI-002](#ui-002) | [FR-003–005](../product/srs.md#fr-003) | [AC-003–005](../product/acceptance-criteria.md#ac-003), [AC-054](../product/acceptance-criteria.md#ac-054) | [UF-002](../product/user-flows.md#uf-002) |
| [UI-003](#ui-003) | [FR-040–041](../product/srs.md#fr-040), [FR-061–064](../product/srs.md#fr-061), [NFR-031](../product/srs.md#nfr-031) | [AC-047–048](../product/acceptance-criteria.md#ac-047), [AC-083–086](../product/acceptance-criteria.md#ac-083), [AC-095](../product/acceptance-criteria.md#ac-095) | [UF-018](../product/user-flows.md#uf-018) |
| [UI-004](#ui-004) | [FR-011–012](../product/srs.md#fr-011), [FR-015](../product/srs.md#fr-015), [FR-023](../product/srs.md#fr-023), [FR-025](../product/srs.md#fr-025), [FR-027](../product/srs.md#fr-027), [FR-041](../product/srs.md#fr-041), [NFR-005](../product/srs.md#nfr-005), [NFR-031](../product/srs.md#nfr-031) | [AC-013](../product/acceptance-criteria.md#ac-013), [AC-016](../product/acceptance-criteria.md#ac-016), [AC-027](../product/acceptance-criteria.md#ac-027), [AC-029–032](../product/acceptance-criteria.md#ac-029), [AC-048](../product/acceptance-criteria.md#ac-048) | [UF-007](../product/user-flows.md#uf-007), [UF-010](../product/user-flows.md#uf-010), [UF-012](../product/user-flows.md#uf-012), [UF-018](../product/user-flows.md#uf-018) |
| [UI-005](#ui-005) | [FR-011](../product/srs.md#fr-011), [FR-013](../product/srs.md#fr-013), [FR-016–022](../product/srs.md#fr-016), [FR-031](../product/srs.md#fr-031), [FR-036](../product/srs.md#fr-036), [NFR-008–010](../product/srs.md#nfr-008), [NFR-031](../product/srs.md#nfr-031) | [AC-012](../product/acceptance-criteria.md#ac-012), [AC-014](../product/acceptance-criteria.md#ac-014), [AC-017–023](../product/acceptance-criteria.md#ac-017), [AC-037](../product/acceptance-criteria.md#ac-037), [AC-042](../product/acceptance-criteria.md#ac-042), [AC-050–052](../product/acceptance-criteria.md#ac-050), [AC-095](../product/acceptance-criteria.md#ac-095) | [UF-007–008](../product/user-flows.md#uf-007) |
| [UI-006](#ui-006) | [FR-012–015](../product/srs.md#fr-012), [FR-023–030](../product/srs.md#fr-023), [FR-035–036](../product/srs.md#fr-035), [FR-041](../product/srs.md#fr-041), [FR-061–064](../product/srs.md#fr-061), [NFR-005–006](../product/srs.md#nfr-005), [NFR-031](../product/srs.md#nfr-031) | [AC-013–016](../product/acceptance-criteria.md#ac-013), [AC-027–036](../product/acceptance-criteria.md#ac-027), [AC-041–043](../product/acceptance-criteria.md#ac-041), [AC-048](../product/acceptance-criteria.md#ac-048), [AC-083–086](../product/acceptance-criteria.md#ac-083) | [UF-009–015](../product/user-flows.md#uf-009) |
| [UI-007](#ui-007) | [FR-034](../product/srs.md#fr-034), [FR-041](../product/srs.md#fr-041), [NFR-031](../product/srs.md#nfr-031) | [AC-040](../product/acceptance-criteria.md#ac-040), [AC-048](../product/acceptance-criteria.md#ac-048) | [UF-014–015](../product/user-flows.md#uf-014) |
| [UI-008](#ui-008) | [FR-032–034](../product/srs.md#fr-032), [FR-039](../product/srs.md#fr-039), [FR-041](../product/srs.md#fr-041), [NFR-007](../product/srs.md#nfr-007), [NFR-031](../product/srs.md#nfr-031) | [AC-038–040](../product/acceptance-criteria.md#ac-038), [AC-045–046](../product/acceptance-criteria.md#ac-045), [AC-048](../product/acceptance-criteria.md#ac-048) | [UF-014–015](../product/user-flows.md#uf-014), [UF-017](../product/user-flows.md#uf-017) |
| [UI-009](#ui-009) | [FR-038–039](../product/srs.md#fr-038), [FR-041](../product/srs.md#fr-041), [FR-065](../product/srs.md#fr-065), [NFR-007](../product/srs.md#nfr-007), [NFR-011](../product/srs.md#nfr-011), [NFR-031](../product/srs.md#nfr-031) | [AC-044–046](../product/acceptance-criteria.md#ac-044), [AC-048](../product/acceptance-criteria.md#ac-048), [AC-053](../product/acceptance-criteria.md#ac-053), [AC-097](../product/acceptance-criteria.md#ac-097) | [UF-016–017](../product/user-flows.md#uf-016) |
| [UI-010](#ui-010) | [FR-007–008](../product/srs.md#fr-007) | [AC-007–008](../product/acceptance-criteria.md#ac-007) | [UF-005](../product/user-flows.md#uf-005), [UF-019](../product/user-flows.md#uf-019) |
| [UI-011](#ui-011) | [FR-009–010](../product/srs.md#fr-009), [NFR-001](../product/srs.md#nfr-001) | [AC-009–011](../product/acceptance-criteria.md#ac-009) | [UF-006](../product/user-flows.md#uf-006), [UF-020](../product/user-flows.md#uf-020) |

[PD-016](../project/decision-register.md#pd-016) applies where UI-005 changes the checked URL and UI-006 displays the resulting state. [FR-008 and AC-008](../product/requirements-traceability-matrix.md#deferred-coverage-and-exceptions) track deferred editable account settings.
