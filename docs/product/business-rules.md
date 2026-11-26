# InfraPulse Business Rules

| Field | Value |
|---|---|
| Document Status | DRAFT — PENDING VALIDATION |
| Version | 0.1 |
| Responsible Role | Product Analyst |
| Related Project Stage | Stage 01 — Product Discovery |
| Project Task | IP-003 |
| Validation | IP-004, pending owner review |

## Rule status

APPROVED identifies an approved core decision in the rule. Explicitly proposed details in the same row remain PROPOSED. DERIVED DRAFT indicates baseline-derived behavior awaiting validation. EXISTING TARGET records the Stage 00 target. Related requirement IDs provide sources and acceptance references.

| Rule | Title | Status | Observed rule | Related requirements |
|---|---|---|---|---|
| <a id="br-001"></a> BR-001 | Registration Policy | APPROVED | Public signup defaults to disabled after setup. Only installation authority can change the setting. Beta workspace invitations use separate workspace authority and do not require public signup to be turned on. | [FR-003](srs.md#fr-003), [FR-004](srs.md#fr-004), [FR-050](srs.md#fr-050) |
| <a id="br-002"></a> BR-002 | Account Bootstrap | DERIVED DRAFT | Initial setup establishes one initial account through an authorized entry path. Initialization prevents subsequent use of bootstrap. The procedure and entry surface are pending [Q-01](prd.md#q-01). | [FR-001](srs.md#fr-001), [FR-002](srs.md#fr-002) |
| <a id="br-003"></a> BR-003 | Authentication | DERIVED DRAFT | Valid sign-in issues a JWT access token and a refresh token. Protected access authenticates a valid JWT. Eligible sessions obtain a new JWT with a valid refresh token. Missing, invalid or expired tokens grant no access or renewal in their respective paths. Sign-out prevents further renewal. Failure feedback omits identity and secret details. Token lifetime and product session policy remain [Q-01](prd.md#q-01). | [FR-005](srs.md#fr-005), [FR-006](srs.md#fr-006), [FR-007](srs.md#fr-007), [FR-008](srs.md#fr-008) |
| <a id="br-004"></a> BR-004 | Workspace Isolation | APPROVED | Scope resources, dependent observations, asynchronous effects and exports to authorized workspaces. Publicly published status exposes only approved selected content. | [FR-009](srs.md#fr-009), [NFR-001](srs.md#nfr-001), [FR-025](srs.md#fr-025), [FR-053](srs.md#fr-053), [FR-056](srs.md#fr-056), [FR-057](srs.md#fr-057), [NFR-018](srs.md#nfr-018) |
| <a id="br-005"></a> BR-005 | Authorization | APPROVED | Installation scope governs registration and network policy. MVP Owners exercise workspace scope. Beta evaluates membership and role. See [Q-07](prd.md#q-07) for the proposed permissions. | [FR-009](srs.md#fr-009), [NFR-001](srs.md#nfr-001), [FR-010](srs.md#fr-010), [FR-025](srs.md#fr-025), [NFR-009](srs.md#nfr-009), [FR-048](srs.md#fr-048), [FR-049](srs.md#fr-049), [FR-050](srs.md#fr-050), [FR-051](srs.md#fr-051), [FR-055](srs.md#fr-055) |
| <a id="br-006"></a> BR-006 | Monitor Configuration | DERIVED DRAFT | Save only valid supported settings. An invalid edit preserves previous values. MVP HTTP methods are GET and HEAD with no arbitrary request body. Apply installation target policy independently of user configuration. Beta JSON assertions use bounded declarative input. Classifying malformed target JSON as a failure is proposed under [Q-09](prd.md#q-09). | [FR-011](srs.md#fr-011), [FR-012](srs.md#fr-012), [FR-013](srs.md#fr-013), [FR-014](srs.md#fr-014), [FR-015](srs.md#fr-015), [FR-016](srs.md#fr-016), [FR-017](srs.md#fr-017), [FR-018](srs.md#fr-018), [FR-031](srs.md#fr-031), [NFR-008](srs.md#nfr-008), [FR-043](srs.md#fr-043), [FR-044](srs.md#fr-044), [FR-045](srs.md#fr-045), [FR-059](srs.md#fr-059), [FR-060](srs.md#fr-060), [NFR-022](srs.md#nfr-022) |
| <a id="br-007"></a> BR-007 | Monitoring Intervals | APPROVED | 30 seconds is the minimum. The proposed default is 60 seconds with a one-second step and a 24-hour inclusive maximum. The 1,000-monitor performance baseline uses 60 seconds. | [FR-020](srs.md#fr-020), [FR-021](srs.md#fr-021), [FR-022](srs.md#fr-022) |
| <a id="br-008"></a> BR-008 | Check Timeouts | DERIVED DRAFT | A healthy execution exceeding its target deadline is a qualifying target timeout. Worker delays and platform failures are separate. The proposed request timeout default is 10 seconds. Bounds and timing details require [Q-02](prd.md#q-02). | [FR-018](srs.md#fr-018), [FR-019](srs.md#fr-019), [FR-035](srs.md#fr-035), [FR-061](srs.md#fr-061) |
| <a id="br-009"></a> BR-009 | Scheduled Execution | DERIVED DRAFT | Configured active monitors have recurring due opportunities. Delayed, missed and completed work have distinguishable dispositions. No recurring target check starts while paused, including when queued work becomes available to a handler. Work that did not execute creates no fabricated target result. Paused manual requests remain [Q-03](prd.md#q-03). | [FR-015](srs.md#fr-015), [FR-022](srs.md#fr-022), [NFR-002](srs.md#nfr-002), [NFR-003](srs.md#nfr-003), [NFR-004](srs.md#nfr-004), [FR-029](srs.md#fr-029), [NFR-032](srs.md#nfr-032) |
| <a id="br-010"></a> BR-010 | Manual Execution | APPROVED | Run Check Now is available asynchronously to authorized users with finite frequency limits. Results appear once in history with their origin. Cadence, measurement and paused behavior remain [Q-03](prd.md#q-03). | [FR-023](srs.md#fr-023), [FR-024](srs.md#fr-024), [FR-025](srs.md#fr-025), [NFR-005](srs.md#nfr-005), [FR-026](srs.md#fr-026), [FR-027](srs.md#fr-027), [FR-028](srs.md#fr-028), [FR-029](srs.md#fr-029) |
| <a id="br-011"></a> BR-011 | Duplicate Execution Handling | DERIVED DRAFT | A repeated delivery has one effective result, transition and notification trigger. The manual and scheduled overlap policy avoids concurrent effective checks of the same monitor. Suggested collision disposition is [Q-03](prd.md#q-03). | [NFR-004](srs.md#nfr-004), [FR-026](srs.md#fr-026), [FR-029](srs.md#fr-029) |
| <a id="br-012"></a> BR-012 | Monitor Lifecycle | PROPOSED | Use the states and transitions below. Check result categories describe individual observations. See [Q-04](prd.md#q-04). | [FR-011](srs.md#fr-011), [FR-014](srs.md#fr-014), [FR-015](srs.md#fr-015), [FR-032](srs.md#fr-032), [FR-033](srs.md#fr-033), [FR-036](srs.md#fr-036) |
| <a id="br-013"></a> BR-013 | Check Result Classification | PROPOSED | Use the classification table below. Exclusion of internal faults from automatic target failure and the qualifying denominator are approved policy. | [FR-019](srs.md#fr-019), [NFR-003](srs.md#nfr-003), [FR-030](srs.md#fr-030), [FR-035](srs.md#fr-035), [FR-037](srs.md#fr-037), [FR-061](srs.md#fr-061), [FR-062](srs.md#fr-062), [FR-063](srs.md#fr-063) |
| <a id="br-014"></a> BR-014 | Incident Opening | APPROVED | The configured consecutive qualifying failure threshold opens the incident. Default is 3. Proposed single-active-incident invariant is enforced by the transition model if approved. | [NFR-004](srs.md#nfr-004), [FR-031](srs.md#fr-031), [FR-032](srs.md#fr-032), [FR-035](srs.md#fr-035), [FR-036](srs.md#fr-036) |
| <a id="br-015"></a> BR-015 | Incident Recovery | APPROVED | The configured consecutive qualifying success threshold closes an active incident as recovered. Default is 2. Proposed lifecycle closures use a distinct disposition and do not imply recovery. | [NFR-004](srs.md#nfr-004), [FR-031](srs.md#fr-031), [FR-033](srs.md#fr-033), [FR-035](srs.md#fr-035), [FR-036](srs.md#fr-036) |
| <a id="br-016"></a> BR-016 | Consecutive Threshold Semantics | PROPOSED | Process eligible observations in logical opportunity order. A qualifying success resets the failure streak and a qualifying failure or timeout resets the recovery streak. Excluded or missed observations do not advance either streak. Counter treatment at gaps and configuration changes is detailed below and remains [Q-04](prd.md#q-04). | [FR-028](srs.md#fr-028), [FR-031](srs.md#fr-031), [FR-032](srs.md#fr-032), [FR-033](srs.md#fr-033), [FR-034](srs.md#fr-034), [FR-035](srs.md#fr-035), [FR-036](srs.md#fr-036), [FR-037](srs.md#fr-037) |
| <a id="br-017"></a> BR-017 | Notification Triggering | DERIVED DRAFT | The product delivers permitted Telegram incident notifications for a correctly configured and enabled channel when the provider is available and can deliver. The opening and recovery defaults remain a separate [Q-05](prd.md#q-05) proposal. Pause, deletion, exclusion and repeated observations while open do not independently trigger recovery notifications. | [FR-032](srs.md#fr-032), [FR-033](srs.md#fr-033), [FR-038](srs.md#fr-038), [FR-039](srs.md#fr-039), [NFR-007](srs.md#nfr-007), [FR-046](srs.md#fr-046), [FR-047](srs.md#fr-047), [FR-065](srs.md#fr-065) |
| <a id="br-018"></a> BR-018 | Notification Deduplication | DERIVED DRAFT | Apply one business notification trigger per effective incident transition and configured destination, including on sequential replay or concurrent processing. With a determinate successful provider outcome the recipient receives one notification from concurrent processing. Replay after confirmed receipt produces no additional notification. A confirmed failure has an observable delivery outcome. Any retry stays associated with the original logical notification event. Retry handling of indeterminate outcomes remains open under [Q-05](prd.md#q-05). | [NFR-004](srs.md#nfr-004), [FR-039](srs.md#fr-039), [NFR-007](srs.md#nfr-007), [FR-065](srs.md#fr-065) |
| <a id="br-019"></a> BR-019 | Pause and Resume | PROPOSED | Pause prevents recurring target checks from starting, including those queued before pause whose target execution has not started. Under the proposed lifecycle in [Q-04](prd.md#q-04), show PAUSED, clear streaks, preserve any active incident, and resume to PENDING with fresh streaks. Eligible in-flight work can remain in history but cannot mutate live state across the pause boundary under that proposal. Rejecting manual checks while paused is conditional on [Q-03](prd.md#q-03). | [FR-015](srs.md#fr-015), [FR-027](srs.md#fr-027), [FR-036](srs.md#fr-036), [FR-063](srs.md#fr-063) |
| <a id="br-020"></a> BR-020 | Monitor Deletion | PROPOSED | Delete prevents new work. Proposed terminally close any active incident as monitor removed without a recovery alert. Treatment of retained history visibility and late results is [Q-04](prd.md#q-04) and [Q-08](prd.md#q-08). | [FR-014](srs.md#fr-014), [FR-036](srs.md#fr-036), [FR-037](srs.md#fr-037) |
| <a id="br-021"></a> BR-021 | Late and Out-of-order Results | PROPOSED | Apply only current-configuration observations newer than the last applied observation to live state. Eligible late results appear once in history. Pending metric eligibility uses the observation window and excludes superseded configuration observations from current-configuration comparisons. | [NFR-004](srs.md#nfr-004), [FR-036](srs.md#fr-036), [FR-037](srs.md#fr-037) |
| <a id="br-022"></a> BR-022 | Network Security | APPROVED | Permit eligible public destinations and deny private destinations by default. Only the Installation Operator may explicitly allowlist eligible internal destinations. Always-denied sensitive destinations remain blocked even with a conflicting allowlist entry, and Workspace Owners cannot override the policy. Validate allowed protocol and effective destination on every connection, including after DNS changes and redirects, for IPv4, IPv6 and mapped addresses. See the destination rules below. | [FR-010](srs.md#fr-010), [FR-035](srs.md#fr-035), [NFR-008](srs.md#nfr-008), [NFR-009](srs.md#nfr-009), [NFR-010](srs.md#nfr-010), [NFR-011](srs.md#nfr-011), [NFR-012](srs.md#nfr-012), [FR-043](srs.md#fr-043), [FR-047](srs.md#fr-047), [NFR-017](srs.md#nfr-017), [NFR-022](srs.md#nfr-022) |
| <a id="br-023"></a> BR-023 | Data Retention | EXISTING TARGET | Keep 30 days of check history under the baseline. [Q-08](prd.md#q-08) covers clock, cleanup window and removal interactions. The demo has its own finite, isolated lifecycle under [Q-13](prd.md#q-13). | [NFR-006](srs.md#nfr-006), [NFR-019](srs.md#nfr-019) |
| <a id="br-024"></a> BR-024 | Availability Calculation | APPROVED | Divide qualifying successes by qualifying completed observations and multiply by 100. Include qualifying failures and target timeouts in the denominator. Distinguish excluded and absent observations. Zero qualifying observations means measured availability is unavailable. Never report 100% uptime for an empty sample. | [FR-028](srs.md#fr-028), [FR-061](srs.md#fr-061), [FR-063](srs.md#fr-063), [FR-064](srs.md#fr-064), [FR-052](srs.md#fr-052), [FR-066](srs.md#fr-066) |
| <a id="br-025"></a> BR-025 | Latency Calculation | APPROVED | Use qualifying successful check durations only. Mean is sum divided by count. p95 and p99 represent upper-tail latency quantiles. Timestamp, percentile estimator, sample policy and rounding remain [Q-06](prd.md#q-06) parameters. Single-monitor conventions apply in MVP. Any combined multi-monitor calculation is a Beta proposal under [Q-06](prd.md#q-06). | [FR-028](srs.md#fr-028), [FR-062](srs.md#fr-062), [FR-063](srs.md#fr-063), [FR-064](srs.md#fr-064), [FR-052](srs.md#fr-052), [FR-066](srs.md#fr-066) |
| <a id="br-026"></a> BR-026 | Demo Isolation | APPROVED | Demo workloads, data, identities and mutable sessions remain isolated from real installations and other sessions. Use controlled synthetic targets, limit activity and storage, and suppress real notification delivery. After the validated trigger, verify actual cleanup under [Q-13](prd.md#q-13), including deletion or another explicitly approved cleanup method. | [FR-058](srs.md#fr-058), [NFR-017](srs.md#nfr-017), [NFR-018](srs.md#nfr-018), [NFR-019](srs.md#nfr-019) |

## Proposed monitor model

The states and transition details are **PROPOSED** under [Q-04](prd.md#q-04). The approved opening and recovery defaults apply to qualifying results. A monitor state describes the current live view. A result describes one execution. An active incident can coexist with PAUSED or PENDING after a lifecycle change, as shown below. Keep at most one active incident per monitor. Opening and closing are idempotent. Track failure and recovery streaks independently. A result advances live state only if it belongs to the current configuration and lifecycle epoch and follows the last applied observation in logical opportunity order. Apply an eligible result when it arrives. A later arrival for an older opportunity cannot retroactively alter the live streak. A target failure or timeout while an incident is active clears the recovery streak. Excluded results neither advance nor break either streak in the proposed model.

| Starting condition | Event | Resulting state and effects |
|---|---|---|
| New monitor | Valid creation | PENDING, zero streaks, no incident. |
| PENDING or UP, no active incident | Qualifying success | UP, failure streak reset. |
| PENDING or UP, no active incident | Qualifying failure or target timeout below threshold | Retain state and increment failure streak. |
| PENDING or UP, no active incident | Failure threshold reached | DOWN, open one incident and reset recovery streak. |
| DOWN or PENDING with active incident | Qualifying success below recovery threshold | Retain state and increment recovery streak. |
| DOWN or PENDING with active incident | Recovery threshold reached | UP, close the incident once as recovered and clear both streaks. |
| DOWN or PENDING with active incident | Qualifying failure or timeout | DOWN, reset recovery streak and keep the existing incident. |
| Any live state | ERROR, SKIPPED, absent observation, replay or late superseded result | Preserve state, counters and incident. Report diagnostics or observation gap as applicable. |
| Active monitor | Authorized pause | PAUSED, clear both streaks, preserve open incident. |
| PAUSED | Resume | PENDING, clear both streaks, preserve open incident and restart scheduled eligibility. |
| PAUSED | In-flight completion or candidate manual request | Keep PAUSED. Eligible in-flight results may be retained outside live evaluation. Reject a new manual request if that behavior is approved under [Q-03](prd.md#q-03). |
| Any live state | Material target or threshold configuration change | Start fresh streaks. Preserve any incident and use PENDING if active or PAUSED if already paused. Older work cannot update live state. |
| Any live state | Accepted manual result | Preserve cadence, counters and incident under [Q-03](prd.md#q-03), including while an incident is open. |
| Any live state | Delete | No further monitor transitions. Proposed retire active incident as removed without recovery notice. |
| Deleted monitor | Late delivery or attempted trigger | No new execution, state change or notification. Historical access and handling of late results remain [Q-04](prd.md#q-04) and [Q-08](prd.md#q-08). |

## Proposed check result classification

| Result | Observable meaning | Qualification |
|---|---|---|
| SUCCESS | Target satisfied the configured condition. | Eligible for uptime and latency if in the selected observation population. |
| FAILURE | Target failed its condition, such as an unexpected status or attributable connection refusal. | Eligible as a failed observation. Ambiguous network and DNS causes require validation under [Q-04](prd.md#q-04) and [Q-10](prd.md#q-10). |
| TIMEOUT | Healthy check execution exhausted its target deadline. | Eligible as a failed observation. Queue delays, worker outages and platform timeouts remain separate. |
| ERROR | Configuration, destination policy, platform, or inconclusive execution failure, with a diagnostic class. | Excluded. Target unavailability remains unestablished. |
| SKIPPED | A known due opportunity was not executed, such as the proposed manual overlap case. | Excluded and separately visible. |
| No observation | A pause or gap with no completed target evidence. | Excluded. Preserve the distinction between missing, paused and known skipped work. |

## Default values

| Parameter | Value | Status |
|---|---|---|
| HTTP method | GET | PROPOSED |
| Monitoring interval | 60 seconds | PROPOSED |
| Minimum interval | 30 seconds | APPROVED |
| Request timeout | 10 seconds | PROPOSED |
| Expected status codes | 200–299 | PROPOSED |
| Follow redirects | Disabled | PROPOSED |
| TLS verification | Enabled | PROPOSED |
| Failure threshold | 3 | APPROVED |
| Recovery threshold | 2 | APPROVED |
| Initial state | PENDING | PROPOSED |
| History retention | 30 days | EXISTING TARGET |
| Incident notification | Enabled when configured | PROPOSED |
| Recovery notification | Enabled when configured | PROPOSED |

Proposed settings cannot override installation destination policy or weaken the treatment of always-denied destinations.

## Destination rules

Validate parseable HTTP or HTTPS target URLs with an eligible host and port and no embedded credentials. Beta typed TCP and certificate destinations use their declared transport and the same administrative destination rules. Evaluate direct IP addresses and resolved DNS answers for both families, including equivalent mapped representations. The address actually contacted must be approved for that connection even when DNS changes between validation and use. Policy applies before outbound redirects, reconnections and retries. Keep rejected attempts distinguishable from service unavailability and redact confidential values. Credential-bearing diagnostics and forwarding credentials to unapproved recipients are prohibited.

Private ranges are denied unless the destination is explicitly eligible and listed by the installation operator. A workspace Owner cannot alter this decision. Cloud metadata services, loopback, link-local and other forbidden sensitive destinations must remain blocked under the installation policy, including when an allowlist entry conflicts. Address class details, port policy and mixed DNS answer handling are [Q-10](prd.md#q-10). Verify with controlled fixtures for direct address inputs, both address families, mixed DNS results, resolution changes, redirects, installation allowlist conflicts and changes, Workspace Owner authority and protected credential values.

## Metric conventions

**MVP single-monitor conventions, PROPOSED under [Q-06](prd.md#q-06).** The exact label `No data` is draft UI copy. BR-024 governs the required absence-of-observations semantics. Select observations by completion timestamp using UTC half-open windows `[start, end)`. Show the timezone alongside personalized display times. An observation exactly at the end belongs to the following adjacent window. A completed qualifying target failure or timeout adds a denominator observation only. Count excluded results separately and show gaps and pauses independently. Under [Q-03](prd.md#q-03) use scheduled observations only. A late eligible observation may update a historical metric for its window under the validated eligibility policy. Never infer an outcome from an expected opportunity.

For mean, divide total qualifying successful duration by count when at least one value exists. Measure duration using the target check elapsed time, excluding scheduling delay. For p95 and p99, propose sorting qualifying successful durations in ascending order and taking the observation at one-based rank `ceil(p × n)`, with `p = 0.95` or `0.99`. Proposed minimums are one duration for mean and 20 each for p95 and p99, with explicit Insufficient data for smaller nonempty percentile samples. Keep full precision in calculations. Propose nearest whole millisecond for displayed latency and one decimal place for uptime, rounding ties up.

Example fixture places one 100 ms success at the start, one 300 ms success strictly inside, an internal error and an in-window failure. A timeout exactly at the end falls in the next window. The first window shows 66.7% uptime, 200 ms mean, insufficient p95 and p99 samples and one excluded platform result. The next window has 0.0% uptime and no successful latency when the timeout is its only eligible observation. In a latency-only fixture of 20 successes from 10 through 200 ms in steps of 10, p95 is 190 ms and p99 is 200 ms. A window with exclusions alone reports availability and latency as unavailable.

**Beta combined metrics, PROPOSED under [Q-06](prd.md#q-06).** The candidate convention pools qualifying observations for selected eligible monitors, computes combined metrics from the pool and exposes sample counts. The proposal excludes averaging per-monitor percentiles. [AC-098](acceptance-criteria.md#ac-098) uses the aggregation, weighting and sample rules if approved.

## References

- [Product Requirements Document](prd.md)
- [Decision Register](../project/decision-register.md)
- [Software Requirements Specification](srs.md)
- [Acceptance Criteria](acceptance-criteria.md)
- [User Flows and Screen Catalog](user-flows.md)
