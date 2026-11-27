# Interaction patterns

IP-006 · MVP v0.1.0 · Stage 03 COMPLETED AND APPROVED

## Forms and feedback

Keep labels, current values, units, persistent help and inline errors within each field. Use text alongside error styling and bind errors through `aria-describedby`. Validate on submit, clear or reevaluate a rejected field as it is corrected, and focus the first invalid control on failure. For server validation, map safe Problem Details field errors and show actionable non-field feedback. Preserve the draft, include the saved configuration on version conflict and require explicit reconciliation. Resolve ambiguous mutations from authoritative reads before asking the user to retry. A local loading/submit state prevents double activation.

Show accepted mutations through polite, transient toasts and persistent state in the affected screen. Keep failure, stale and retry guidance visible until resolved. Confirm irreversible deletion and consequential target changes. A modal has a title, consequence text, safe initial focus, Escape and an explicit cancel action. Restore focus to the trigger, its replacement after a lifecycle change, or the destination heading on navigation. See the [error contract](../architecture/api-design.md#error-contract).

## Monitor actions

| Action | User-facing response |
|---|---|
| Create | PENDING with check schedule and explanatory No data. |
| Ordinary edit | Saved values and same current state. Effective edit increments configuration version and resets streaks. Any retained incident stays open. |
| Change checked URL while active | Confirm the lifecycle consequence. Close any open incident as Configuration changed. Enter PENDING, advance configuration version and reset streaks. Prior committed history stays available. |
| Change checked URL while PAUSED | Confirm that PAUSED is preserved and any open incident closes as Configuration changed. Advance configuration version and reset streaks. Keep future due time absent and start no automatic check. Resume later enters PENDING. |
| Run check now | Accepted 202 shows queued, running and terminal disposition from the returned execution. Manual completion appears in history as Manual. It has no impact on schedule, status, incidents or aggregate metrics. |
| Manual conflict | 409 busy explains ongoing work; 409 paused tells the Owner to resume. 429 uses the server retry interval. Preserve scheduled cadence and report skipped opportunities as diagnostics. |
| Pause / Resume | Pause shows PAUSED, preserves an open incident and stops new checks. Resume enters PENDING and restores scheduling. Confirmed scheduled recovery can close a retained incident after its threshold. |
| Delete | Confirm stopped future checks, removed check history and retained incidents. Any open incident closes as Monitor deleted. Administrative closures create no Incident Resolved delivery. |

[PD-016](../project/decision-register.md#pd-016), [monitor lifecycle](../product/business-rules.md#monitor-lifecycle) and [incident engine](../architecture/backend-design.md#incident-engine) define the transition rules. Platform error, stale evidence, manual check and skipped opportunity leave state and streaks intact. Confirmed target timeout and failure can advance the failure streak.

## Operational states and freshness

| State | Presentation and recovery |
|---|---|
| Loading | Mark the operational region busy and reserve layout space. Initial and scope-change loads show no old scope. |
| Empty | Name the missing collection and offer the relevant primary action. Keep filters on a zero-match result. |
| First-load error | Replace the pending body with safe text and Retry. Keep navigation available. |
| Refresh failure | Retain confirmed authorized data and show an inline failure notice with last success time. |
| Stale | After 30 seconds without a successful update, show “Stale”, warning icon and last successful UTC timestamp. Refresh manually or let recovery update the view. |
| Success | Replace the displayed data and time with current evidence, clear retry/stale feedback and keep the user's focus and context. |
| No data | State the absence of qualifying observations or insufficient samples within the selected window. |

Apply 10-second polling to UI-003, UI-004, UI-006, UI-007, UI-008 and UI-009, including delivery dispositions on UI-008/009. Use per-query last success so one recovered slice cannot hide another stale slice. Revalidate foreground, reconnect and after tab resume. Use one request per key, scope queries by session, owner, resource and filter, and refetch the first page without cycling archival pages. Keep a visible manual Refresh action and a controls-level pause for live updates. On resume request current data. Clear previous scoped data on logout, workspace change or authoritative denial. Keep unsaved form fields independent of delivery polling. [Polling scope](../product/user-flows.md#mvp-polling-scope) · [Frontend freshness](../architecture/frontend-design.md#data-freshness) · [AC-048](../product/acceptance-criteria.md#ac-048)

The local prototype simulates a single snapshot response per screen. Select Loading, Error, Refresh error or Stale under Prototype / Demo Data. Connected requests a fresh snapshot and returns to automatic updates. Refresh data also works while live updates are paused. Prototype fixture observations change simulation state; delivery and check actions stay in memory.

## Data visualization

- Use server window boundaries and UTC for 24h, 7d and 30d. Render per-monitor values and derive summary state counts independently. The chart shows bucket averages of successful, eligible scheduled observations, with an ms axis, UTC time axis, range label and expandable accessible table using identical buckets and sample counts. Render empty buckets as gaps and label them No data in the table. Leave isolated observations visible as points. The prototype displays 12 equal-width buckets and never joins across empty buckets.
- Production KPI values use the exact `Metrics` response. Convert µs to ms for display without recalculating percentiles from chart buckets. The MVP contract exposes metrics and cursor-paginated observations, so chart series come from authorized `/checks` history for the selected range and origin, filtering `metrics_eligible` with successful outcomes. Expose the time coverage of loaded observations and disclose partial history when a cursor remains. A loaded interval with no sample is a gap. Unloaded intervals have unknown coverage. Chart browsing can request older pages without polling the archival pages. An API change for pre-bucketed series would require owner approval.
- Uptime is successful qualifying scheduled results divided by all qualifying scheduled results, including target failure and target timeout. Latency uses only successful qualifying scheduled checks. Exclude manual checks, internal faults, superseded results, skipped work and pause intervals. Surface coverage separately through the known-missed, missing-slot, paused-duration and exclusion fields. No eligible observations yields No data. Show p95 after 20 and p99 after 100 successful samples, using nearest rank. The prototype derives sample metrics directly from its synthetic observation set and demonstrates a window with p95 present and p99 absent.

[Metric conventions](../product/business-rules.md#metric-conventions) · [AC-083–086](../product/acceptance-criteria.md#ac-083)
