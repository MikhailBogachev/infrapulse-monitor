# Information architecture

IP-006 · MVP v0.1.0 · Stage 03 COMPLETED AND APPROVED

The workspace shell groups Overview, Monitors and Incidents under monitoring and Notifications, Workspace and Account under settings. The workspace name identifies the scope and links to its settings. The topbar exposes context, account and manual data refresh on polling screens. Sign-in and Sign-up use the standalone authentication layout. Use a modal navigation drawer on widths below 1000 px. Production routes inherit the [approved frontend routing](../architecture/frontend-design.md#routing-and-api-integration).

| ID | Screen | Production route | Local prototype fragment |
|---|---|---|---|
| [UI-001](screen-specifications.md#ui-001) | Sign In | `/sign-in` | `#/sign-in` |
| [UI-002](screen-specifications.md#ui-002) | Sign Up | `/sign-up` | `#/sign-up` |
| [UI-003](screen-specifications.md#ui-003) | Overview | `/w/:workspaceId` | `#/overview` |
| [UI-004](screen-specifications.md#ui-004) | Monitors List | `/w/:workspaceId/monitors` | `#/monitors` |
| [UI-005](screen-specifications.md#ui-005) | Create / Edit Monitor | `/w/:workspaceId/monitors/new`, `/w/:workspaceId/monitors/:id/edit` | `#/monitors/new`, `#/monitors/:id/edit` |
| [UI-006](screen-specifications.md#ui-006) | Monitor Details | `/w/:workspaceId/monitors/:id` | `#/monitors/:id` |
| [UI-007](screen-specifications.md#ui-007) | Incidents List | `/w/:workspaceId/incidents` | `#/incidents` |
| [UI-008](screen-specifications.md#ui-008) | Incident Details | `/w/:workspaceId/incidents/:id` | `#/incidents/:id` |
| [UI-009](screen-specifications.md#ui-009) | Notification Settings | `/w/:workspaceId/settings/notifications` | `#/notifications` |
| [UI-010](screen-specifications.md#ui-010) | Account Settings | `/account` | `#/account` |
| [UI-011](screen-specifications.md#ui-011) | Workspace Settings | `/w/:workspaceId/settings` | `#/workspace` |

## Journeys

| Journey | Path | Failure or fallback |
|---|---|---|
| First Owner | Operator provisions first Owner and workspace in a trusted terminal → Sign In → Overview | Setup-required guidance on Sign In when independently known through the operator handoff. Registration availability alone cannot identify setup state. |
| Self-registration | Sign In → Sign Up → successful registration → Sign In → new workspace | Closed by default and during setup. Closed and racing policy changes lead to registration unavailable copy. |
| Session recovery | Protected path → refresh once → current authorized view | If renewal fails, clear prior scoped data, sign in and reauthorize the same-origin return path. |
| Monitor configuration | Overview or Monitors → New monitor → Monitor details → Edit | Preserve typed input on validation or version conflict. Delete returns to Monitors and preserves incident evidence. |
| Incident investigation | Overview or Incidents → Incident details → extant Monitor or delivery disposition | Deleted monitor remains a text label. An unavailable resource uses generic copy without scoped data. |
| Telegram | Notifications, or Workspace → Notifications → Save → Delivery issues | Retain failed/unknown disposition with safe diagnostics. |
| Account and ownership | Account → Sign out → Sign In. Workspace → Rename → updated shell | Verify owned scope before route content. Reauthorize on identity or workspace change. |

## State surfaces

Setup required, registration closed, expired session and access unavailable are states of existing entry points or the current requested route. The [approved operator path](../architecture/security-design.md#identity-and-sessions) covers bootstrap and installation policy. Product behavior follows the [existing journey catalog](../product/user-flows.md#ui-screen-catalog).

In the local prototype, use **Prototype / Demo Data** to change fixture states and reset. On mobile this control is in the navigation drawer. Reload restores the reference workspace. The public demo lifecycle belongs to the later release under [Q-13](../product/prd.md#q-13).
