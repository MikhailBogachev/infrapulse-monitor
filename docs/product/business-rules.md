# InfraPulse Business Rules

| Field | Value |
|---|---|
| Document Status | READY FOR OWNER APPROVAL |
| Version | 0.2 |
| Responsible Role | Product Analyst |
| Related Project Stage | Stage 01 — Product Discovery |
| Project Task | IP-004 |
| Validation | IP-004, final owner acceptance pending |

## Rule status

APPROVED identifies explicit product decisions. READY FOR OWNER APPROVAL identifies derived specification text. Linked requirements provide sources and verification references.

| Rule | Title | Status | Observed rule | Related requirements |
|---|---|---|---|---|
| <a id="br-001"></a> BR-001 | Registration Policy | APPROVED | Public signup defaults to disabled after setup. Only installation authority can change the setting. Beta workspace invitations use separate workspace authority and do not require public signup to be turned on. | [FR-003](srs.md#fr-003), [FR-004](srs.md#fr-004), [FR-050](srs.md#fr-050) |
| <a id="br-002"></a> BR-002 | Account Bootstrap | APPROVED | A protected, operator-authorized one-time procedure creates the first Owner. It is unavailable after initial setup. | [FR-001](srs.md#fr-001), [FR-002](srs.md#fr-002) |
| <a id="br-003"></a> BR-003 | Authentication | APPROVED | Email and password sign-in issues a 15-minute access JWT and a 7-day refresh token. Protected access requires a valid JWT. Renewal requires an eligible session and valid refresh token and invalidates the previous refresh token. Logout revokes the corresponding refresh session. Failure feedback omits identity and secret details. | [FR-005](srs.md#fr-005), [FR-006](srs.md#fr-006), [FR-007](srs.md#fr-007), [FR-008](srs.md#fr-008) |
| <a id="br-004"></a> BR-004 | Workspace Isolation | APPROVED | Scope resources, dependent observations, asynchronous effects and exports to authorized workspaces. Publicly published status exposes only approved selected content. | [FR-009](srs.md#fr-009), [NFR-001](srs.md#nfr-001), [FR-025](srs.md#fr-025), [FR-053](srs.md#fr-053), [FR-056](srs.md#fr-056), [FR-057](srs.md#fr-057), [NFR-018](srs.md#nfr-018) |
| <a id="br-005"></a> BR-005 | Authorization | APPROVED | Installation authority governs registration and network policy. MVP has only the Owner role. Beta uses the [approved permission matrix](srs.md#beta-authorization-matrix). Invitations are single-use, expire after 7 days and are revocable. | [FR-009](srs.md#fr-009), [NFR-001](srs.md#nfr-001), [FR-010](srs.md#fr-010), [FR-025](srs.md#fr-025), [NFR-009](srs.md#nfr-009), [FR-048](srs.md#fr-048), [FR-049](srs.md#fr-049), [FR-050](srs.md#fr-050), [FR-051](srs.md#fr-051), [FR-055](srs.md#fr-055) |
| <a id="br-006"></a> BR-006 | Monitor Configuration | APPROVED | Save only supported settings. Invalid edits preserve previous values. MVP allows GET and HEAD with no arbitrary body. Status 200–299 is successful. Redirect following is disabled and TLS certificate verification is mandatory. Installation policy applies independently of monitor configuration. Beta JSON assertions are bounded and declarative. Malformed target JSON fails the check. | [FR-011](srs.md#fr-011), [FR-012](srs.md#fr-012), [FR-013](srs.md#fr-013), [FR-014](srs.md#fr-014), [FR-015](srs.md#fr-015), [FR-016](srs.md#fr-016), [FR-017](srs.md#fr-017), [FR-018](srs.md#fr-018), [FR-031](srs.md#fr-031), [NFR-008](srs.md#nfr-008), [FR-043](srs.md#fr-043), [FR-044](srs.md#fr-044), [FR-045](srs.md#fr-045), [FR-059](srs.md#fr-059), [FR-060](srs.md#fr-060), [NFR-022](srs.md#nfr-022) |
| <a id="br-007"></a> BR-007 | Monitoring Intervals | APPROVED | Intervals default to 60 seconds and range from 30 seconds to 24 hours inclusive. The performance baseline uses 60 seconds. | [FR-020](srs.md#fr-020), [FR-021](srs.md#fr-021), [FR-022](srs.md#fr-022) |
| <a id="br-008"></a> BR-008 | Check Timeouts | APPROVED | Timeouts default to 10 seconds and range from 1 to 30 seconds inclusive, capped by the interval. A healthy execution exceeding its target deadline produces a target TIMEOUT. Worker delay and platform faults are separate. | [FR-018](srs.md#fr-018), [FR-019](srs.md#fr-019), [FR-035](srs.md#fr-035), [FR-061](srs.md#fr-061) |
| <a id="br-009"></a> BR-009 | Scheduled Execution | READY FOR OWNER APPROVAL | Active monitors have recurring due opportunities. Delayed, missed and completed work have distinguishable dispositions. No recurring target check starts while PAUSED, including a job queued before pause. Work that did not execute creates no fabricated result. | [FR-015](srs.md#fr-015), [FR-022](srs.md#fr-022), [NFR-002](srs.md#nfr-002), [NFR-003](srs.md#nfr-003), [NFR-004](srs.md#nfr-004), [FR-029](srs.md#fr-029), [NFR-032](srs.md#nfr-032) |
| <a id="br-010"></a> BR-010 | Manual Execution | APPROVED | Run Check Now provides authorized asynchronous diagnostics. Accept at most one manual run per monitor in 30 seconds. PAUSED monitors are ineligible. Record the result as Manual in history and exclude it from scheduled cadence, uptime, aggregated latency, live state and automated incidents. | [FR-023](srs.md#fr-023), [FR-024](srs.md#fr-024), [FR-025](srs.md#fr-025), [NFR-005](srs.md#nfr-005), [FR-026](srs.md#fr-026), [FR-027](srs.md#fr-027), [FR-028](srs.md#fr-028), [FR-029](srs.md#fr-029) |
| <a id="br-011"></a> BR-011 | Duplicate Execution Handling | READY FOR OWNER APPROVAL | Replay or concurrent processing of one logical execution preserves one effective result, transition and notification trigger per destination. A manual check cannot run alongside another check for the same monitor. Collision disposition is deferred to Stage 02. | [NFR-004](srs.md#nfr-004), [FR-026](srs.md#fr-026), [FR-029](srs.md#fr-029) |
| <a id="br-012"></a> BR-012 | Monitor Lifecycle | APPROVED | Apply the approved [monitor lifecycle](#monitor-lifecycle). Execution result categories describe individual observations. | [FR-011](srs.md#fr-011), [FR-014](srs.md#fr-014), [FR-015](srs.md#fr-015), [FR-032](srs.md#fr-032), [FR-033](srs.md#fr-033), [FR-036](srs.md#fr-036) |
| <a id="br-013"></a> BR-013 | Check Result Classification | READY FOR OWNER APPROVAL | Classify observations as described below. Internal faults do not establish target unavailability. | [FR-019](srs.md#fr-019), [NFR-003](srs.md#nfr-003), [FR-030](srs.md#fr-030), [FR-035](srs.md#fr-035), [FR-037](srs.md#fr-037), [FR-061](srs.md#fr-061), [FR-062](srs.md#fr-062), [FR-063](srs.md#fr-063) |
| <a id="br-014"></a> BR-014 | Incident Opening | APPROVED | Reaching the configurable consecutive qualifying failure threshold sets DOWN and opens an incident. Default is 3. | [NFR-004](srs.md#nfr-004), [FR-031](srs.md#fr-031), [FR-032](srs.md#fr-032), [FR-035](srs.md#fr-035), [FR-036](srs.md#fr-036) |
| <a id="br-015"></a> BR-015 | Incident Recovery | APPROVED | Confirmed recovery at the configurable consecutive qualifying success threshold sets UP and closes the incident as recovered. Default is 2. Deletion and address-change closures have their own reasons. | [NFR-004](srs.md#nfr-004), [FR-031](srs.md#fr-031), [FR-033](srs.md#fr-033), [FR-035](srs.md#fr-035), [FR-036](srs.md#fr-036) |
| <a id="br-016"></a> BR-016 | Consecutive Threshold Semantics | APPROVED | Only qualifying scheduled results contribute to failure and recovery thresholds. Pause and configuration changes reset streaks. Ordering and other eligibility boundaries are deferred to Stage 02. | [FR-028](srs.md#fr-028), [FR-031](srs.md#fr-031), [FR-032](srs.md#fr-032), [FR-033](srs.md#fr-033), [FR-034](srs.md#fr-034), [FR-035](srs.md#fr-035), [FR-036](srs.md#fr-036), [FR-037](srs.md#fr-037) |
| <a id="br-017"></a> BR-017 | Notification Triggering | APPROVED | Telegram Incident Opened and Incident Resolved are enabled by default and require a configured, enabled channel. Manual Check Completed, Monitor Paused and Internal System Error notifications are outside MVP. Deletion and address changes do not establish recovery. | [FR-032](srs.md#fr-032), [FR-033](srs.md#fr-033), [FR-038](srs.md#fr-038), [FR-039](srs.md#fr-039), [NFR-007](srs.md#nfr-007), [FR-046](srs.md#fr-046), [FR-047](srs.md#fr-047), [FR-065](srs.md#fr-065) |
| <a id="br-018"></a> BR-018 | Notification Deduplication | APPROVED | Preserve one business notification trigger per effective transition and destination across sequential replay and concurrent processing. For a determinate successful provider outcome, concurrent processing yields one receipt and replay after confirmed receipt yields no additional notification. Observe confirmed failures independently of incident state. Eligible confirmed failures may be retried within a bounded budget for the original logical event. Indeterminate outcomes must not be blindly resent. | [NFR-004](srs.md#nfr-004), [FR-039](srs.md#fr-039), [NFR-007](srs.md#nfr-007), [FR-065](srs.md#fr-065) |
| <a id="br-019"></a> BR-019 | Pause and Resume | APPROVED | Pause enters PAUSED, resets streaks and preserves any open incident. No recurring target check starts while paused, including a pre-queued check, and manual execution is unavailable. Resume enters PENDING, and an incident retained across pause closes only on confirmed recovery. | [FR-015](srs.md#fr-015), [FR-027](srs.md#fr-027), [FR-036](srs.md#fr-036), [FR-063](srs.md#fr-063) |
| <a id="br-020"></a> BR-020 | Monitor Deletion | APPROVED | Deletion prevents new work, removes check history and closes any open incident as Monitor Deleted. Incident history remains until workspace deletion. | [FR-014](srs.md#fr-014), [FR-036](srs.md#fr-036), [FR-037](srs.md#fr-037) |
| <a id="br-021"></a> BR-021 | Late and Out-of-order Results | APPROVED | Stale results cannot change live state or incident decisions. Eligible history remains subject to retention and authorized removal. Classifying and ordering stale or concurrent work belongs to Stage 02. | [NFR-004](srs.md#nfr-004), [FR-036](srs.md#fr-036), [FR-037](srs.md#fr-037) |
| <a id="br-022"></a> BR-022 | Network Security | APPROVED | Use eligible public IPv4 and IPv6, deny private networks by default and allow installation operators to allowlist eligible internal destinations. Always-denied classes take precedence. Reject mixed eligible and denied DNS answers. Normalize IPv4-mapped IPv6. Apply the destination rules below to every supported outbound path. | [FR-010](srs.md#fr-010), [FR-035](srs.md#fr-035), [NFR-008](srs.md#nfr-008), [NFR-009](srs.md#nfr-009), [NFR-010](srs.md#nfr-010), [NFR-011](srs.md#nfr-011), [NFR-012](srs.md#nfr-012), [FR-043](srs.md#fr-043), [FR-047](srs.md#fr-047), [NFR-017](srs.md#nfr-017), [NFR-022](srs.md#nfr-022) |
| <a id="br-023"></a> BR-023 | Data Retention | APPROVED | Check results expire 30 days after completion in UTC. Complete cleanup within 24 hours of expiry. Monitor deletion removes check history and incident history is retained until workspace deletion. Demo data follows its own cleanup deadline. | [NFR-006](srs.md#nfr-006), [NFR-019](srs.md#nfr-019) |
| <a id="br-024"></a> BR-024 | Availability Calculation | APPROVED | Use Successful / (Successful + Failed) × 100% over valid scheduled observations. Target TIMEOUT is a failure. Exclude manual checks, platform errors, skipped checks and paused periods. Beta maintenance results are also excluded from uptime. No eligible observations means No data. | [FR-028](srs.md#fr-028), [FR-061](srs.md#fr-061), [FR-063](srs.md#fr-063), [FR-064](srs.md#fr-064), [FR-052](srs.md#fr-052), [FR-066](srs.md#fr-066), [FR-054](srs.md#fr-054) |
| <a id="br-025"></a> BR-025 | Latency Calculation | APPROVED | Use only qualifying successful scheduled observations. Compute average and nearest-rank p95 and p99, requiring 20 and 100 samples for the respective percentiles. Use UTC reporting periods of 24h, 7d and 30d. Beta combines valid observations into one pool. | [FR-028](srs.md#fr-028), [FR-062](srs.md#fr-062), [FR-063](srs.md#fr-063), [FR-064](srs.md#fr-064), [FR-052](srs.md#fr-052), [FR-066](srs.md#fr-066) |
| <a id="br-026"></a> BR-026 | Demo Isolation | APPROVED | The v1.0.0 public demo isolates temporary workspaces from other sessions and real deployments. Registration is unnecessary. Visitors can create monitors for controlled HTTP services and observe incident opening and recovery. Suppress real notifications. Limit sessions to 5 monitors and 60 minutes and complete temporary data cleanup within 15 minutes of termination. | [FR-058](srs.md#fr-058), [NFR-017](srs.md#nfr-017), [NFR-018](srs.md#nfr-018), [NFR-019](srs.md#nfr-019) |

## Monitor lifecycle

The table specifies the transitions approved in [Q-04](prd.md#q-04). Scheduled target checks cannot start while PAUSED, including jobs queued before the pause. An internal fault or stale result cannot establish a state transition. Manual results are diagnostic only.

| Event | State and effects |
|---|---|
| Create a monitor | PENDING. |
| First qualifying success of a new monitor | UP. |
| Configured consecutive failure threshold reached | DOWN, open an incident. |
| Configured consecutive recovery threshold reached after DOWN, including recovery following resume with a retained incident | UP, close the incident as recovered. |
| Pause | PAUSED, reset streaks and keep the open incident. |
| Resume | PENDING, preserve the open incident until confirmed recovery. |
| Change the checked address | PENDING, reset streaks and close the previous incident for configuration change. |
| Change configuration | Reset streaks. |
| Delete | Stop new executions and close any open incident as Monitor Deleted. |

Stage 02 specifies ordering, stale-result eligibility and concurrent processing. Additional state transitions require owner approval.

## Check result classification

| Result | Observable meaning | Qualification |
|---|---|---|
| SUCCESS | Target satisfied the configured condition. | Eligible for uptime and latency if in the selected observation population. |
| FAILURE | Target failed its condition, such as an unexpected status or attributable connection refusal. | Eligible as a failed observation. Stage 02 defines diagnostic treatment of inconclusive network and DNS outcomes. |
| TIMEOUT | Healthy check execution exhausted its target deadline. | Eligible as a failed observation. Queue delays, worker outages and platform timeouts remain separate. |
| ERROR | Configuration, destination policy, platform, or inconclusive execution failure, with a diagnostic class. | Excluded. Target unavailability remains unestablished. |
| SKIPPED | A known due opportunity was not executed, for example, work omitted by the scheduler. | Excluded and separately visible. |
| No observation | A pause or gap with no completed target evidence. | Excluded. Preserve the distinction between missing, paused and known skipped work. |

## Default values

| Parameter | Approved value |
|---|---|
| HTTP method | GET |
| Monitoring interval | 60 seconds, within 30 seconds to 24 hours |
| Request timeout | 10 seconds, within 1–30 seconds and bounded by the interval |
| Successful HTTP status codes | 200–299 |
| MVP redirect following | Disabled |
| TLS certificate verification | Mandatory |
| Failure threshold | 3 |
| Recovery threshold | 2 |
| Initial state | PENDING |
| History retention | 30 days from check completion in UTC |
| Incident Opened and Incident Resolved | Enabled by default, delivery requires a configured and enabled channel |

## Destination rules

Validate parseable HTTP or HTTPS target URLs without embedded credentials. MVP defaults to ports 80 and 443. Additional ports require administrative configuration. Beta typed TCP and certificate destinations use their declared transport under the same installation policy. Evaluate direct IP addresses and resolved DNS answers in both families. Normalize IPv4-mapped IPv6 before evaluation. Reject a check in its entirety if DNS answers mix eligible and denied destinations. The actual destination must be eligible for every connection, including after DNS changes and on supported retries, reconnections and redirect hops. MVP never follows redirects.

Private networks are denied unless explicitly eligible and allowlisted by the Installation Operator. Loopback, link-local, cloud metadata and other always-denied sensitive destinations remain blocked even when an allowlist entry conflicts. Workspace Owners cannot bypass the policy. Keep policy rejections distinct from target failures, redact diagnostics and prevent credential disclosure to unapproved destinations. Verify applicable paths and address classes with controlled fixtures under [AC-051](acceptance-criteria.md#ac-051) and [AC-052](acceptance-criteria.md#ac-052).

## Metric conventions

Use UTC reporting periods of 24h, 7d and 30d. Count valid scheduled observations only. Provide No data when there are no valid results and keep exclusions and observation gaps distinguishable. If there are failures but no successes, uptime is 0% and there is no latency sample.

For a qualifying successful latency sample of size n, average is the sum divided by n. For a percentile p, sort values and take one-based rank `ceil(p × n)`. Show p95 only at n ≥ 20 and p99 only at n ≥ 100. A fixture with 20 durations from 10 to 200 ms in steps of 10 yields p95 of 190 ms and no p99. A fixture with 100 durations from 10 to 1,000 ms in steps of 10 yields p95 of 950 ms and p99 of 990 ms. Beta pools eligible observations across selected monitors before calculating the same metrics.

Stage 02 specifies exact timing and window boundary conventions. Stage 03 specifies rounding and presentation of nonempty samples below percentile minimums.

## References

- [Product Requirements Document](prd.md)
- [Decision Register](../project/decision-register.md)
- [Software Requirements Specification](srs.md)
- [Acceptance Criteria](acceptance-criteria.md)
- [User Flows and Screen Catalog](user-flows.md)
