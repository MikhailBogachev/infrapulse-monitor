# InfraPulse Software Requirements Specification

| Field | Value |
|---|---|
| Document Status | READY FOR OWNER APPROVAL |
| Version | 0.2 |
| Responsible Role | Requirements Engineer |
| Related Project Stage | Stage 01 — Product Discovery |
| Project Task | IP-004 |
| Validation | IP-004, final owner acceptance pending |

## Purpose and Scope

This specification describes verifiable InfraPulse behavior from MVP through v1.0.0. It inherits approved release boundaries and does not define API contracts, data schemas or deployment architecture.

## Definitions and References

Words use the [glossary](../project/glossary.md) and [business rules](business-rules.md). MUST denotes mandatory intent, SHOULD denotes recommended behavior requiring documented deviation if accepted, and MAY denotes permission. Normative intent in this document is subject to its status. Approval status records whether the underlying behavior has explicit owner approval or awaits acceptance as a derived specification.

## Product Overview

A self-hosted Modular Monolith exposes workspace-scoped web workflows, runs checks in the background and stores observation history. Runtime technology classifications come from the charter.

## User Classes

- Installation Operator controls installation policy and operation.
- Workspace Owner configures and investigates authorized resources.
- Account holder or signup visitor uses identity workflows.
- Beta workspace participants act within validated membership and roles.
- Public visitors see intentionally published status or isolated demo data in the applicable release.

## Operating Environment

Supported self-hosted environments use the baseline Docker and Docker Compose setup. Specific host prerequisites and supported browser versions are pending. The product provides a desktop-first responsive browser interface.

## Functional Requirements

The tables group functional requirements by user capability. Priority uses MoSCoW, followed by the requirement validation status.

## Identity

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-001"></a> FR-001 | Bootstrap first account | The installation MUST establish the first Owner through a protected, operator-authorized one-time setup while public registration is unavailable. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001), [Q-01](prd.md#q-01) | Controlled integration test | [AC-001](acceptance-criteria.md#ac-001) | APPROVED |
| <a id="fr-002"></a> FR-002 | Close bootstrap | The installation MUST prevent unauthorized bootstrap and reuse after initial setup. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001), [Q-01](prd.md#q-01) | Controlled integration test | [AC-002](acceptance-criteria.md#ac-002) | APPROVED |
| <a id="fr-003"></a> FR-003 | Default registration policy | The installation MUST disable public registration by default after initial setup. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001), [Q-01](prd.md#q-01) | Controlled integration test | [AC-003](acceptance-criteria.md#ac-003) | APPROVED |
| <a id="fr-004"></a> FR-004 | Operator registration control | The installation MUST enforce the operator's current public registration setting. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001), [Q-01](prd.md#q-01) | Controlled integration test | [AC-004](acceptance-criteria.md#ac-004) | APPROVED |
| <a id="fr-005"></a> FR-005 | Issue and validate JWT access tokens | The product MUST issue a 15-minute access JWT and a 7-day refresh token after valid email and password sign-in. Protected operations MUST validate the access JWT. Reject invalid credentials and missing, invalid or expired access tokens. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [D-005](../project/decision-register.md#d-005), [Q-01](prd.md#q-01) | Controlled integration test | [AC-005](acceptance-criteria.md#ac-005) | APPROVED |
| <a id="fr-006"></a> FR-006 | Renew JWT access | The product MUST renew JWT access for an eligible session with a valid refresh token, including after access token expiry. Each renewal MUST rotate the refresh token and invalidate its predecessor. Reject missing, invalid, expired or rotated-out refresh tokens. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [D-005](../project/decision-register.md#d-005), [Q-01](prd.md#q-01) | Controlled integration test | [AC-006](acceptance-criteria.md#ac-006) | APPROVED |
| <a id="fr-007"></a> FR-007 | Sign out | Logout MUST return the user to sign-in, revoke the corresponding refresh session and prevent further renewal through that session. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [D-005](../project/decision-register.md#d-005), [Q-01](prd.md#q-01) | Controlled integration test | [AC-007](acceptance-criteria.md#ac-007) | APPROVED |
| <a id="fr-008"></a> FR-008 | Account settings | Editable account settings require separate owner approval. Preserve workspace and account isolation for any approved settings. | v0.1.0 MVP | Should | [F-001](prd.md#f-001), [D-005](../project/decision-register.md#d-005), [Q-01](prd.md#q-01) | Controlled integration test | [AC-008](acceptance-criteria.md#ac-008) | DEFERRED |


## Authorization Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-009"></a> FR-009 | MVP ownership | MVP MUST use the Owner as its only workspace role. Owners may manage resources within their authorized workspace. | v0.1.0 MVP | Must | [F-002](prd.md#f-002), [PD-007](../project/decision-register.md#pd-007), [Q-07](prd.md#q-07) | Security verification with controlled fixtures | [AC-009](acceptance-criteria.md#ac-009) | APPROVED |
| <a id="nfr-001"></a> NFR-001 | Workspace isolation | Every release MUST enforce current workspace authorization for all protected operations, including background effects, live updates and exports where applicable. | v0.1.0 MVP | Must | [F-002](prd.md#f-002), [PD-007](../project/decision-register.md#pd-007), [Q-07](prd.md#q-07) | Security verification with controlled fixtures | [AC-010](acceptance-criteria.md#ac-010) | APPROVED |
| <a id="fr-010"></a> FR-010 | Workspace settings | The product MUST limit workspace settings to permitted workspace-level controls and deny installation policy changes through workspace authority. | v0.1.0 MVP | Must | [F-002](prd.md#f-002), [PD-006](../project/decision-register.md#pd-006), [PD-007](../project/decision-register.md#pd-007), [PD-001](../project/decision-register.md#pd-001), [Q-01](prd.md#q-01), [Q-10](prd.md#q-10) | Security verification with controlled fixtures | [AC-011](acceptance-criteria.md#ac-011) | READY FOR OWNER APPROVAL |
| <a id="fr-048"></a> FR-048 | Team authorization | Beta MUST enforce workspace membership and role-based authorization for covered operations. | v0.5.0 Beta | Must | [F-017](prd.md#f-017), [PD-007](../project/decision-register.md#pd-007), [Q-07](prd.md#q-07) | Security verification with controlled fixtures | [AC-063](acceptance-criteria.md#ac-063) | READY FOR OWNER APPROVAL |
| <a id="fr-049"></a> FR-049 | Beta role permissions | Beta MUST apply the approved [role matrix](srs.md#beta-authorization-matrix) and protect Owner authority and last-Owner continuity. | v0.5.0 Beta | Must | [F-017](prd.md#f-017), [F-032](prd.md#f-032), [PD-007](../project/decision-register.md#pd-007), [Q-07](prd.md#q-07) | Security verification with controlled fixtures | [AC-064](acceptance-criteria.md#ac-064) | APPROVED |
| <a id="fr-050"></a> FR-050 | Invite workspace participants | Authorized actors MUST be able to invite participants to their workspace. Invitations MUST be single-use, expire after 7 days, and be revocable. | v0.5.0 Beta | Must | [F-032](prd.md#f-032), [PD-001](../project/decision-register.md#pd-001), [PD-007](../project/decision-register.md#pd-007), [Q-07](prd.md#q-07) | Security verification with controlled fixtures | [AC-065](acceptance-criteria.md#ac-065) | APPROVED |
| <a id="fr-051"></a> FR-051 | Manage workspace membership | An authorized actor MUST be able to manage memberships within their own workspace. | v0.5.0 Beta | Must | [F-032](prd.md#f-032), [PD-007](../project/decision-register.md#pd-007), [Q-07](prd.md#q-07) | Security verification with controlled fixtures | [AC-066](acceptance-criteria.md#ac-066) | READY FOR OWNER APPROVAL |


## Monitor management and check execution

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-011"></a> FR-011 | Create monitor | The Owner MUST be able to create a valid monitor in their workspace and view its configuration. A new monitor starts in PENDING. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005), [Q-04](prd.md#q-04) | Controlled integration test | [AC-012](acceptance-criteria.md#ac-012) | APPROVED |
| <a id="fr-012"></a> FR-012 | Read monitor | The Owner MUST be able to list and inspect their workspace monitors. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-013](acceptance-criteria.md#ac-013) | READY FOR OWNER APPROVAL |
| <a id="fr-013"></a> FR-013 | Edit monitor | The Owner MUST be able to save a valid configuration change to their monitor. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-014](acceptance-criteria.md#ac-014) | READY FOR OWNER APPROVAL |
| <a id="fr-014"></a> FR-014 | Delete monitor | The Owner MUST be able to delete a monitor, stop new executions and remove its check history while preserving incident history. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005), [Q-04](prd.md#q-04), [Q-08](prd.md#q-08) | Controlled integration test | [AC-015](acceptance-criteria.md#ac-015) | APPROVED |
| <a id="fr-015"></a> FR-015 | Pause and resume recurring checks | The Owner MUST be able to suspend and resume recurring checks. The product MUST prevent new recurring target checks from starting while paused, including checks whose jobs were queued before pause but had not started. The product MUST NOT fabricate observations for work that did not execute. See [Q-03](prd.md#q-03). | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [F-005](prd.md#f-005), [PD-011](../project/decision-register.md#pd-011), [Q-03](prd.md#q-03), [Q-04](prd.md#q-04) | Controlled integration test | [AC-016](acceptance-criteria.md#ac-016) | APPROVED |
| <a id="fr-016"></a> FR-016 | HTTP methods | HTTP monitors MUST support GET and HEAD and reject other methods and arbitrary request bodies. | v0.1.0 MVP | Must | [F-004](prd.md#f-004), [PD-002](../project/decision-register.md#pd-002), [Q-02](prd.md#q-02) | Controlled integration test | [AC-017](acceptance-criteria.md#ac-017) | APPROVED |
| <a id="fr-017"></a> FR-017 | HTTP success condition | MVP HTTP monitors MUST treat only status codes 200–299 as successful. | v0.1.0 MVP | Must | [F-004](prd.md#f-004), [PD-002](../project/decision-register.md#pd-002), [Q-02](prd.md#q-02) | Controlled integration test | [AC-018](acceptance-criteria.md#ac-018) | APPROVED |
| <a id="fr-018"></a> FR-018 | HTTP defaults | MVP HTTP monitors MUST default to GET and a 10-second timeout. Timeouts MUST be within 1–30 seconds inclusive and MUST NOT exceed the interval. Redirect following MUST be disabled and TLS certificate verification MUST be enforced. | v0.1.0 MVP | Must | [F-004](prd.md#f-004), [PD-002](../project/decision-register.md#pd-002), [Q-02](prd.md#q-02) | Controlled integration test | [AC-019](acceptance-criteria.md#ac-019) | APPROVED |
| <a id="fr-019"></a> FR-019 | Timeout classification | A check that reaches its configured target request deadline MUST yield a target timeout when execution was healthy up to that deadline. | v0.1.0 MVP | Must | [F-004](prd.md#f-004), [PD-003](../project/decision-register.md#pd-003), [PD-011](../project/decision-register.md#pd-011), [Q-02](prd.md#q-02) | Controlled integration test | [AC-020](acceptance-criteria.md#ac-020) | APPROVED |
| <a id="fr-020"></a> FR-020 | Minimum interval | The product MUST reject monitoring intervals below 30 seconds and allow a 30-second configuration. | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [PD-003](../project/decision-register.md#pd-003), [Q-02](prd.md#q-02) | Controlled integration test | [AC-021](acceptance-criteria.md#ac-021) | APPROVED |
| <a id="fr-021"></a> FR-021 | Interval defaults and range | The interval MUST default to 60 seconds and MUST be at most 24 hours. | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [PD-003](../project/decision-register.md#pd-003), [Q-02](prd.md#q-02) | Controlled integration test | [AC-022](acceptance-criteria.md#ac-022) | APPROVED |
| <a id="fr-022"></a> FR-022 | Recurring execution | Active monitors MUST receive recurring background checks according to their configured interval, subject to visible execution delays and failures. | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-023](acceptance-criteria.md#ac-023) | READY FOR OWNER APPROVAL |
| <a id="fr-023"></a> FR-023 | Request immediate check | The product MUST let an authorized user request an asynchronous Run Check Now execution and inspect its progress and outcome. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [PD-005](../project/decision-register.md#pd-005), [Q-03](prd.md#q-03) | Controlled integration test | [AC-027](acceptance-criteria.md#ac-027) | READY FOR OWNER APPROVAL |
| <a id="fr-024"></a> FR-024 | Persist manual result | The product MUST save completed manual check results in monitor history with the Manual origin. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [F-007](prd.md#f-007), [PD-005](../project/decision-register.md#pd-005), [Q-03](prd.md#q-03) | Controlled integration test | [AC-028](acceptance-criteria.md#ac-028) | APPROVED |
| <a id="fr-025"></a> FR-025 | Authorize manual execution | The product MUST authorize manual execution against the monitor's workspace before accepting work. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [PD-005](../project/decision-register.md#pd-005), [PD-007](../project/decision-register.md#pd-007), [Q-03](prd.md#q-03) | Controlled integration test | [AC-029](acceptance-criteria.md#ac-029) | READY FOR OWNER APPROVAL |
| <a id="fr-026"></a> FR-026 | Prevent overlapping execution | Manual execution MUST NOT run concurrently with any other check of the same monitor, including another manual or scheduled check. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [F-005](prd.md#f-005), [PD-005](../project/decision-register.md#pd-005), [Q-03](prd.md#q-03) | Controlled integration test | [AC-031](acceptance-criteria.md#ac-031) | APPROVED |
| <a id="fr-027"></a> FR-027 | Manual check on paused monitor | The product MUST reject manual execution on PAUSED monitors. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [F-003](prd.md#f-003), [PD-005](../project/decision-register.md#pd-005), [Q-03](prd.md#q-03) | Controlled integration test | [AC-032](acceptance-criteria.md#ac-032) | APPROVED |
| <a id="fr-028"></a> FR-028 | Manual observation effects | Manual checks MUST preserve the schedule and MUST NOT affect uptime, aggregated latency, monitor state or automated incidents. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [F-005](prd.md#f-005), [F-008](prd.md#f-008), [F-033](prd.md#f-033), [PD-005](../project/decision-register.md#pd-005), [PD-011](../project/decision-register.md#pd-011), [Q-03](prd.md#q-03), [Q-06](prd.md#q-06) | Controlled integration test | [AC-033](acceptance-criteria.md#ac-033) | APPROVED |
| <a id="fr-029"></a> FR-029 | Collision disposition and cadence | The product MUST preserve scheduled cadence when manual and scheduled checks collide. Disposition of overlapping requests and scheduled opportunities is deferred to Stage 02. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [F-005](prd.md#f-005), [PD-005](../project/decision-register.md#pd-005), [Q-03](prd.md#q-03) | Controlled integration test | [AC-034](acceptance-criteria.md#ac-034) | APPROVED |
| <a id="fr-043"></a> FR-043 | TCP check | An authorized workspace user MUST be able to verify connection establishment to a configured host and valid TCP port under installation policy. | v0.5.0 Beta | Must | [F-013](prd.md#f-013), [PD-009](../project/decision-register.md#pd-009), [Q-09](prd.md#q-09) | Controlled integration test | [AC-058](acceptance-criteria.md#ac-058) | APPROVED |
| <a id="fr-044"></a> FR-044 | Certificate check | An authorized workspace user MUST be able to check TLS certificate validity and remaining lifetime for a configured target. | v0.5.0 Beta | Must | [F-014](prd.md#f-014), [PD-009](../project/decision-register.md#pd-009), [Q-09](prd.md#q-09) | Controlled-clock test | [AC-059](acceptance-criteria.md#ac-059) | APPROVED |
| <a id="fr-045"></a> FR-045 | Certificate boundary policy | Exact Beta certificate timing and threshold boundaries require approval before implementation. | v0.5.0 Beta | Should | [F-014](prd.md#f-014), [PD-009](../project/decision-register.md#pd-009), [Q-09](prd.md#q-09) | Controlled-clock test | [AC-060](acceptance-criteria.md#ac-060) | DEFERRED |
| <a id="fr-059"></a> FR-059 | HTTP keyword check | An authorized workspace user MUST be able to require a literal keyword in an eligible HTTP response body. | v0.5.0 Beta | Must | [F-030](prd.md#f-030), [PD-009](../project/decision-register.md#pd-009), [Q-09](prd.md#q-09) | Controlled integration test | [AC-080](acceptance-criteria.md#ac-080) | APPROVED |
| <a id="fr-060"></a> FR-060 | JSON assertion check | An authorized workspace user MUST be able to verify a bounded declarative assertion against a JSON response. Executable input MUST be rejected. Malformed target JSON MUST fail the check. | v0.5.0 Beta | Must | [F-031](prd.md#f-031), [PD-009](../project/decision-register.md#pd-009), [Q-09](prd.md#q-09) | Controlled integration test | [AC-081](acceptance-criteria.md#ac-081), [AC-099](acceptance-criteria.md#ac-099) | APPROVED |


## History and incidents

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-030"></a> FR-030 | Inspect check history | The Owner MUST be able to inspect authorized check outcomes, times, origin and diagnostic class, including empty history. | v0.1.0 MVP | Must | [F-007](prd.md#f-007), [D-005](../project/decision-register.md#d-005), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-035](acceptance-criteria.md#ac-035) | READY FOR OWNER APPROVAL |
| <a id="fr-031"></a> FR-031 | Configure thresholds | The Owner MUST be able to configure both incident thresholds, whose defaults are three failures and two successes. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [PD-004](../project/decision-register.md#pd-004), [Q-04](prd.md#q-04) | Controlled integration test | [AC-037](acceptance-criteria.md#ac-037) | APPROVED |
| <a id="fr-032"></a> FR-032 | Open at failure threshold | At the configured consecutive qualifying failure threshold, the monitor MUST transition to DOWN and open an incident. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [PD-004](../project/decision-register.md#pd-004), [Q-04](prd.md#q-04) | Controlled integration test | [AC-038](acceptance-criteria.md#ac-038) | APPROVED |
| <a id="fr-033"></a> FR-033 | Recover at success threshold | At the configured consecutive qualifying recovery threshold, the monitor MUST transition to UP and close the active incident as recovered, including an incident retained across pause and resume. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [PD-004](../project/decision-register.md#pd-004), [Q-04](prd.md#q-04) | Controlled integration test | [AC-039](acceptance-criteria.md#ac-039) | APPROVED |
| <a id="fr-034"></a> FR-034 | Inspect incidents | The Owner MUST be able to list and inspect incidents with their current disposition and available time evidence. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [D-005](../project/decision-register.md#d-005), [Q-04](prd.md#q-04) | Controlled integration test | [AC-040](acceptance-criteria.md#ac-040) | READY FOR OWNER APPROVAL |
| <a id="fr-035"></a> FR-035 | Exclude platform faults | The product MUST classify an internal or policy-blocked execution distinctly from a qualifying target failure. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [F-007](prd.md#f-007), [PD-004](../project/decision-register.md#pd-004), [PD-011](../project/decision-register.md#pd-011), [Q-04](prd.md#q-04), [Q-10](prd.md#q-10) | Controlled integration test | [AC-041](acceptance-criteria.md#ac-041) | APPROVED |
| <a id="fr-036"></a> FR-036 | State and streak transitions | The product MUST apply the approved [monitor lifecycle](business-rules.md#monitor-lifecycle). Pause and configuration changes reset streaks. An address change sets PENDING and closes any open incident for configuration change. Deletion closes an open incident as Monitor Deleted. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [F-003](prd.md#f-003), [PD-004](../project/decision-register.md#pd-004), [Q-04](prd.md#q-04) | Controlled integration test | [AC-042](acceptance-criteria.md#ac-042) | APPROVED |
| <a id="fr-037"></a> FR-037 | Late observations | Stale results MUST NOT change current monitor state or contribute to live incident thresholds or transitions. Retention applies to eligible history. Result ordering and processing details are deferred to Stage 02. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [F-007](prd.md#f-007), [PD-004](../project/decision-register.md#pd-004), [PD-011](../project/decision-register.md#pd-011), [Q-04](prd.md#q-04), [Q-08](prd.md#q-08) | Controlled integration test | [AC-043](acceptance-criteria.md#ac-043) | APPROVED |


## External Integration Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-038"></a> FR-038 | Configure Telegram | The Owner MUST be able to configure, enable and disable Telegram delivery for their workspace. The product MUST protect destination credentials and send only through a configured and enabled channel. | v0.1.0 MVP | Must | [F-009](prd.md#f-009), [D-005](../project/decision-register.md#d-005), [Q-05](prd.md#q-05) | Controlled integration test | [AC-044](acceptance-criteria.md#ac-044) | APPROVED |
| <a id="fr-039"></a> FR-039 | Deliver permitted Telegram notifications | Given a correctly configured and enabled Telegram channel, a permitted incident transition and a provider able to confirm successful delivery, the product MUST deliver the notification to the configured recipient. Sequential replay and concurrent processing of one logical notification event for the same destination MUST preserve one business effect. With a determinate successful provider outcome, concurrent processing MUST yield one received notification, and replay after confirmed delivery MUST yield no additional notification. Confirmed delivery failure is covered by [NFR-007](srs.md#nfr-007). An indeterminate provider result does not permit blind retry. | v0.1.0 MVP | Must | [F-009](prd.md#f-009), [PD-004](../project/decision-register.md#pd-004), [Q-05](prd.md#q-05) | Controlled integration test | [AC-045](acceptance-criteria.md#ac-045) | APPROVED |
| <a id="fr-065"></a> FR-065 | Default Telegram event preferences | MVP Telegram event preferences MUST enable Incident Opened and Incident Resolved by default. Manual Check Completed, Monitor Paused and Internal System Error notifications are outside MVP. | v0.1.0 MVP | Must | [F-009](prd.md#f-009), [PD-004](../project/decision-register.md#pd-004), [Q-05](prd.md#q-05) | Controlled integration test | [AC-097](acceptance-criteria.md#ac-097) | APPROVED |
| <a id="fr-046"></a> FR-046 | Email notifications | The product MUST let an authorized user configure email notifications for incident transitions. | v0.5.0 Beta | Must | [F-015](prd.md#f-015), [D-005](../project/decision-register.md#d-005), [Q-05](prd.md#q-05) | Controlled integration test | [AC-061](acceptance-criteria.md#ac-061) | READY FOR OWNER APPROVAL |
| <a id="fr-047"></a> FR-047 | Webhook notifications | The product MUST let an authorized user configure a policy-eligible webhook for incident transitions. | v0.5.0 Beta | Must | [F-016](prd.md#f-016), [D-005](../project/decision-register.md#d-005), [PD-006](../project/decision-register.md#pd-006), [Q-05](prd.md#q-05), [Q-10](prd.md#q-10) | Controlled integration test | [AC-062](acceptance-criteria.md#ac-062) | READY FOR OWNER APPROVAL |


## User Interface Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-040"></a> FR-040 | Dashboard summary | The Owner MUST be able to inspect workspace monitor states, recent observations and incidents and navigate to their details. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-047](acceptance-criteria.md#ac-047) | READY FOR OWNER APPROVAL |
| <a id="fr-041"></a> FR-041 | Polling and stale data | Browser-initiated polling MUST refresh changing operational data on [UI-003](user-flows.md#ui-003), [UI-004](user-flows.md#ui-004), [UI-006](user-flows.md#ui-006), [UI-007](user-flows.md#ui-007), [UI-008](user-flows.md#ui-008), [UI-009](user-flows.md#ui-009) while the view is open, as defined in the [MVP polling scope](user-flows.md#mvp-polling-scope). Each view MUST distinguish initial loading, stale retained data and refresh failure, and show current authorized data after recovery without manual reload. Poll over HTTP every 10 seconds. Indicate staleness after 30 seconds without a successful refresh and support manual refresh. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [PD-008](../project/decision-register.md#pd-008), [Q-12](prd.md#q-12) | Controlled integration test | [AC-048](acceptance-criteria.md#ac-048) | APPROVED |
| <a id="fr-042"></a> FR-042 | Beta live updates | Beta MUST deliver live operational updates through Server-Sent Events and reconcile displayed authorized data after reconnecting. Transport and reconnect details are deferred to Beta design. | v0.5.0 Beta | Must | [F-010](prd.md#f-010), [F-018](prd.md#f-018), [PD-008](../project/decision-register.md#pd-008), [Q-12](prd.md#q-12) | Controlled integration test | [AC-049](acceptance-criteria.md#ac-049) | APPROVED |
| <a id="nfr-027"></a> NFR-027 | Dark-only presentation | All product views MUST use the dark theme across release scopes and host theme preferences. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [PD-013](../project/decision-register.md#pd-013), [Q-14](prd.md#q-14) | Browser walkthrough and inspection | [AC-091](acceptance-criteria.md#ac-091) | APPROVED |
| <a id="nfr-029"></a> NFR-029 | Desktop-first responsive interface | The desktop-first interface MUST preserve principal navigation, dashboard, monitor, incident and account journeys on mobile. Verify representative widths of 360, 768, 1024 and 1440 px. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [F-008](prd.md#f-008), [F-010](prd.md#f-010), [F-001](prd.md#f-001), [PD-014](../project/decision-register.md#pd-014), [Q-14](prd.md#q-14) | Browser walkthrough and inspection | [AC-093](acceptance-criteria.md#ac-093) | APPROVED |
| <a id="nfr-030"></a> NFR-030 | English product surfaces | UI text, technical messages, repository documentation and source identifiers and comments MUST be in English. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [PD-015](../project/decision-register.md#pd-015), [D-006](../project/decision-register.md#d-006) | Browser walkthrough and inspection | [AC-094](acceptance-criteria.md#ac-094) | APPROVED |


## Analytics and publishing

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-052"></a> FR-052 | Extended analytics | Beta MUST let authorized users compare availability and successful-check latency across supported windows and eligible monitors. | v0.5.0 Beta | Must | [F-018](prd.md#f-018), [F-033](prd.md#f-033), [PD-011](../project/decision-register.md#pd-011), [Q-06](prd.md#q-06) | Controlled integration test | [AC-067](acceptance-criteria.md#ac-067) | APPROVED |
| <a id="fr-066"></a> FR-066 | Combined multi-monitor analytics | Beta MUST calculate combined uptime and latency for selected eligible monitors from the pooled valid observations, applying the same eligibility and sample rules as single-monitor metrics. | v0.5.0 Beta | Must | [F-018](prd.md#f-018), [PD-011](../project/decision-register.md#pd-011), [Q-06](prd.md#q-06) | Controlled integration test | [AC-098](acceptance-criteria.md#ac-098) | APPROVED |
| <a id="fr-053"></a> FR-053 | Publish status page | An authorized user MUST be able to publish statuses, uptime and public incidents for intentionally selected monitors only. | v0.5.0 Beta | Must | [F-019](prd.md#f-019), [D-005](../project/decision-register.md#d-005), [Q-15](prd.md#q-15) | Controlled integration test | [AC-068](acceptance-criteria.md#ac-068) | APPROVED |
| <a id="fr-054"></a> FR-054 | Schedule maintenance | An authorized user MUST be able to schedule and inspect a maintenance window for authorized monitors. Scheduled checks MUST continue, notifications MUST be suppressed and maintenance results MUST be excluded from uptime. Incident and latency effects require approval before Beta implementation. | v0.5.0 Beta | Must | [F-020](prd.md#f-020), [D-005](../project/decision-register.md#d-005), [Q-15](prd.md#q-15) | Controlled-clock test | [AC-069](acceptance-criteria.md#ac-069) | APPROVED |
| <a id="fr-055"></a> FR-055 | Manage API keys | Beta MUST let authorized users create, expire and revoke workspace-scoped API keys with limited permissions. Expired and revoked keys MUST be rejected. | v0.5.0 Beta | Must | [F-021](prd.md#f-021), [D-005](../project/decision-register.md#d-005), [Q-07](prd.md#q-07), [Q-15](prd.md#q-15) | Controlled integration test | [AC-070](acceptance-criteria.md#ac-070) | APPROVED |
| <a id="fr-056"></a> FR-056 | Inspect audit log | An authorized user MUST be able to inspect an audit trail of defined workspace actions. Each entry MUST record actor, action, resource, timestamp and outcome. | v1.0.0 Release | Must | [F-022](prd.md#f-022), [D-005](../project/decision-register.md#d-005), [Q-15](prd.md#q-15) | Controlled integration test | [AC-071](acceptance-criteria.md#ac-071) | APPROVED |
| <a id="fr-057"></a> FR-057 | Export reports | An authorized user MUST be able to export authorized monitoring reports as CSV within the supported selection. | v1.0.0 Release | Must | [F-024](prd.md#f-024), [D-005](../project/decision-register.md#d-005), [Q-15](prd.md#q-15) | Controlled integration test | [AC-073](acceptance-criteria.md#ac-073) | APPROVED |
| <a id="fr-061"></a> FR-061 | Calculate uptime | The product MUST calculate uptime as Successful / (Successful + Failed) × 100% over valid scheduled results. Target TIMEOUT counts as failed. Exclude internal errors, skipped checks, paused periods and manual checks. | v0.1.0 MVP | Must | [F-033](prd.md#f-033), [PD-011](../project/decision-register.md#pd-011), [Q-03](prd.md#q-03), [Q-06](prd.md#q-06) | Controlled integration test | [AC-083](acceptance-criteria.md#ac-083) | APPROVED |
| <a id="fr-062"></a> FR-062 | Calculate successful latency | Average latency, p95 and p99 MUST use successful scheduled checks only. | v0.1.0 MVP | Must | [F-033](prd.md#f-033), [PD-011](../project/decision-register.md#pd-011), [Q-03](prd.md#q-03), [Q-06](prd.md#q-06) | Controlled integration test | [AC-084](acceptance-criteria.md#ac-084) | APPROVED |
| <a id="fr-063"></a> FR-063 | Show incomplete observations | The product MUST distinguish excluded results, pauses and gaps from measured availability. An empty eligible sample MUST show No data and MUST NOT report 100% uptime. | v0.1.0 MVP | Must | [F-033](prd.md#f-033), [F-010](prd.md#f-010), [PD-011](../project/decision-register.md#pd-011), [Q-03](prd.md#q-03), [Q-06](prd.md#q-06) | Controlled integration test | [AC-085](acceptance-criteria.md#ac-085) | APPROVED |
| <a id="fr-064"></a> FR-064 | Single-monitor metric conventions | MVP MUST use UTC reporting periods of 24h, 7d and 30d for single-monitor metrics. Use nearest-rank p95 and p99 and require at least 20 and 100 eligible latency samples respectively. | v0.1.0 MVP | Must | [F-033](prd.md#f-033), [PD-011](../project/decision-register.md#pd-011), [Q-03](prd.md#q-03), [Q-06](prd.md#q-06) | Controlled-clock test | [AC-086](acceptance-criteria.md#ac-086) | APPROVED |


## Interactive demo

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-058"></a> FR-058 | Interactive demo journey | Public demo visitors MUST be able to enter without registration, receive an isolated temporary workspace, create a monitor for a controlled synthetic HTTP service and observe incidents open and resolve through the product. | v1.0.0 Release | Must | [F-025](prd.md#f-025), [PD-010](../project/decision-register.md#pd-010), [Q-13](prd.md#q-13) | Security verification with controlled fixtures | [AC-074](acceptance-criteria.md#ac-074) | APPROVED |
| <a id="nfr-017"></a> NFR-017 | Demo network containment | Demo sessions MUST be restricted to controlled synthetic destinations and deny arbitrary scanning and notifications to external recipients. | v1.0.0 Release | Must | [F-025](prd.md#f-025), [F-027](prd.md#f-027), [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006), [PD-010](../project/decision-register.md#pd-010), [Q-10](prd.md#q-10), [Q-13](prd.md#q-13) | Security verification with controlled fixtures | [AC-075](acceptance-criteria.md#ac-075) | APPROVED |
| <a id="nfr-018"></a> NFR-018 | Public deployment isolation | The public demo MUST isolate real deployments and data and prevent visitor sessions from reading or mutating each other's mutable data. | v1.0.0 Release | Must | [F-027](prd.md#f-027), [PD-010](../project/decision-register.md#pd-010), [Q-13](prd.md#q-13) | Security verification with controlled fixtures | [AC-076](acceptance-criteria.md#ac-076) | APPROVED |
| <a id="nfr-019"></a> NFR-019 | Demo resource and data lifecycle | The public demo MUST enforce at most 5 monitors per session and a 60-minute session lifetime. In-scope temporary data MUST be cleaned up within 15 minutes after termination. Access denial alone does not constitute cleanup. | v1.0.0 Release | Must | [F-027](prd.md#f-027), [PD-010](../project/decision-register.md#pd-010), [Q-13](prd.md#q-13) | Security verification with controlled fixtures | [AC-077](acceptance-criteria.md#ac-077) | APPROVED |


## Non-functional Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-013"></a> NFR-013 | Local operation | The project MUST support documented self-hosted startup using one Docker Compose command after documented prerequisites and configuration. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [D-004](../project/decision-register.md#d-004), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-055](acceptance-criteria.md#ac-055) | READY FOR OWNER APPROVAL |
| <a id="nfr-014"></a> NFR-014 | Migration readiness | The supported setup and upgrade procedure MUST apply required data migrations while preserving supported existing data. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-056](acceptance-criteria.md#ac-056) | READY FOR OWNER APPROVAL |
| <a id="nfr-015"></a> NFR-015 | CI assurance | For each eligible change, repository CI MUST execute the required MVP automated tests and quality checks in GitHub Actions and report their actual outcomes under [D-010](../project/decision-register.md#d-010). Stage 04 defines pipeline details. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [D-005](../project/decision-register.md#d-005), [D-010](../project/decision-register.md#d-010) | GitHub Actions run evidence for controlled passing and failing changes | [AC-057](acceptance-criteria.md#ac-057) | APPROVED |
| <a id="nfr-020"></a> NFR-020 | Release integration and load evidence | The project MUST record integration and load verification results for the release under the documented repeatable profiles. | v1.0.0 Release | Must | [F-026](prd.md#f-026), [D-005](../project/decision-register.md#d-005), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-078](acceptance-criteria.md#ac-078) | READY FOR OWNER APPROVAL |
| <a id="nfr-021"></a> NFR-021 | Release documentation | The release MUST provide English installation, operation, usage and safe demo documentation for supported features. | v1.0.0 Release | Must | [F-028](prd.md#f-028), [D-005](../project/decision-register.md#d-005), [PD-015](../project/decision-register.md#pd-015) | Measurement and evidence review | [AC-079](acceptance-criteria.md#ac-079) | READY FOR OWNER APPROVAL |
| <a id="nfr-025"></a> NFR-025 | Backend test coverage | Backend line coverage MUST reach at least 80%. Stage 07 defines the measurement scope. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012), [Q-11](prd.md#q-11) | Measurement and evidence review | [AC-089](acceptance-criteria.md#ac-089) | APPROVED |


## Security Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-005"></a> NFR-005 | Manual rate limit | The product MUST accept at most one manual run per monitor per 30 seconds and surface throttling without starting rejected work. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [F-029](prd.md#f-029), [PD-005](../project/decision-register.md#pd-005), [Q-03](prd.md#q-03) | Security verification with controlled fixtures | [AC-030](acceptance-criteria.md#ac-030) | APPROVED |
| <a id="nfr-008"></a> NFR-008 | URL and protocol validation | MVP MUST accept HTTP and HTTPS only. Ports 80 and 443 are allowed by default and additional ports require administrative configuration. Reject invalid URLs, embedded credentials and unsupported schemes or ports before connection. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006), [Q-10](prd.md#q-10) | Security verification with controlled fixtures | [AC-050](acceptance-criteria.md#ac-050) | APPROVED |
| <a id="nfr-009"></a> NFR-009 | Restricted destination policy | The installation MUST permit eligible public destinations and deny private IPv4 and IPv6 destinations by default. Only the Installation Operator MAY explicitly allowlist eligible internal destinations. Always-denied sensitive destinations MUST remain blocked even if an allowlist entry conflicts. Workspace Owners MUST NOT override installation policy. Enforce the policy on actual connections after DNS resolution and on redirect hops where supported, as verified by [NFR-010](srs.md#nfr-010). | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006), [Q-10](prd.md#q-10) | Security verification with controlled fixtures | [AC-051](acceptance-criteria.md#ac-051) | APPROVED |
| <a id="nfr-010"></a> NFR-010 | Resolve and validate every connection | Every actual outbound target connection MUST use a destination validated against current policy, including direct IP, DNS, supported retries and reconnections, and redirect hops where supported. Normalize IPv4-mapped IPv6 before applying policy. Reject the entire check when DNS answers mix eligible and denied destinations. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006), [Q-10](prd.md#q-10) | Security verification with controlled fixtures | [AC-052](acceptance-criteria.md#ac-052) | APPROVED |
| <a id="nfr-011"></a> NFR-011 | Protect confidential values | The platform MUST protect credentials and secrets from unauthorized views, diagnostics and unapproved outbound disclosure. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006), [PD-015](../project/decision-register.md#pd-015), [Q-10](prd.md#q-10) | Security verification with controlled fixtures | [AC-053](acceptance-criteria.md#ac-053) | READY FOR OWNER APPROVAL |
| <a id="nfr-012"></a> NFR-012 | Rate limiting | The installation MUST limit abusive requests and preserve service for ordinary authorized traffic. Stage 02 defines the general rate policy. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [D-005](../project/decision-register.md#d-005), [Q-10](prd.md#q-10) | Security verification with controlled fixtures | [AC-054](acceptance-criteria.md#ac-054) | READY FOR OWNER APPROVAL |
| <a id="nfr-022"></a> NFR-022 | Beta check safety | Additional monitor types MUST enforce installation destination policy and bound target interaction, including response size and computational cost where applicable. | v0.5.0 Beta | Must | [F-011](prd.md#f-011), [F-013](prd.md#f-013), [F-014](prd.md#f-014), [F-030](prd.md#f-030), [F-031](prd.md#f-031), [PD-006](../project/decision-register.md#pd-006), [PD-009](../project/decision-register.md#pd-009), [Q-09](prd.md#q-09), [Q-10](prd.md#q-10) | Security verification with controlled fixtures | [AC-082](acceptance-criteria.md#ac-082) | APPROVED |


## Data and Retention Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-006"></a> NFR-006 | History retention | Check results MUST remain available for 30 days after completion in UTC, subject to authorized removal. At expiry, complete cleanup within 24 hours. Authorized monitor deletion removes its check history. Incident history MUST be retained until workspace deletion. | v0.1.0 MVP | Must | [F-007](prd.md#f-007), [PD-012](../project/decision-register.md#pd-012), [Q-08](prd.md#q-08), [Q-11](prd.md#q-11) | Controlled-clock test | [AC-036](acceptance-criteria.md#ac-036) | APPROVED |


## Error Handling Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-007"></a> NFR-007 | Notification failure isolation | Confirmed delivery failures MUST be observable independently of incident state. Retries of eligible confirmed failures MUST be bounded. Indeterminate outcomes MUST NOT trigger blind retries. Stage 02 defines the retry policy. | v0.1.0 MVP | Must | [F-009](prd.md#f-009), [F-006](prd.md#f-006), [D-005](../project/decision-register.md#d-005), [Q-05](prd.md#q-05) | Controlled integration test | [AC-046](acceptance-criteria.md#ac-046) | APPROVED |
| <a id="nfr-031"></a> NFR-031 | Actionable errors | Product errors MUST identify the failed action or affected field in English and preserve previously confirmed data. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [F-004](prd.md#f-004), [F-010](prd.md#f-010), [PD-008](../project/decision-register.md#pd-008), [Q-12](prd.md#q-12) | Controlled integration test | [AC-095](acceptance-criteria.md#ac-095) | READY FOR OWNER APPROVAL |


## Reliability Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-002"></a> NFR-002 | Background execution | Scheduled checks and notification work MUST run in the approved background task system while interactive views remain usable. | v0.1.0 MVP | Must | [F-006](prd.md#f-006), [D-003](../project/decision-register.md#d-003), [D-004](../project/decision-register.md#d-004) | Controlled integration test | [AC-024](acceptance-criteria.md#ac-024) | READY FOR OWNER APPROVAL |
| <a id="nfr-003"></a> NFR-003 | Worker interruption | The product MUST distinguish delayed, missed or internally failed work during worker unavailability from an observed service failure. | v0.1.0 MVP | Must | [F-006](prd.md#f-006), [F-007](prd.md#f-007), [D-005](../project/decision-register.md#d-005), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-025](acceptance-criteria.md#ac-025) | READY FOR OWNER APPROVAL |
| <a id="nfr-004"></a> NFR-004 | Application idempotency | Sequential replay and concurrent processing of one logical execution MUST preserve a single effective result, incident transition and business notification trigger per destination. Recipient delivery follows [FR-039](srs.md#fr-039). | v0.1.0 MVP | Must | [F-006](prd.md#f-006), [F-008](prd.md#f-008), [F-009](prd.md#f-009), [PD-004](../project/decision-register.md#pd-004), [Q-05](prd.md#q-05) | Controlled integration test | [AC-026](acceptance-criteria.md#ac-026) | APPROVED |


## Performance Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-023"></a> NFR-023 | Baseline performance target | With 1,000 active monitors at 60-second intervals under the approved baseline, API p95 MUST be at most 200 ms excluding external check duration, API server errors MUST be below 1%, and scheduled start delay p95 MUST be at most 5 seconds. | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012), [Q-11](prd.md#q-11) | Measurement and evidence review | [AC-087](acceptance-criteria.md#ac-087) | APPROVED |
| <a id="nfr-024"></a> NFR-024 | Stress characterization | The performance report MUST characterize the 30-second stress profile as capacity evidence. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012), [Q-11](prd.md#q-11) | Measurement and evidence review | [AC-088](acceptance-criteria.md#ac-088) | APPROVED |
| <a id="nfr-026"></a> NFR-026 | Reference workload protocol | Performance measurement MUST use the approved reference environment, concurrency and timing in the [performance measurement protocol](srs.md#performance-measurement-protocol). Stage 07 defines the complete reproducible protocol. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012), [Q-11](prd.md#q-11) | Measurement and evidence review | [AC-090](acceptance-criteria.md#ac-090) | APPROVED |
| <a id="nfr-033"></a> NFR-033 | Repeatable baseline and coverage evidence | The project MUST document a reproducible protocol for baseline performance and backend coverage under [Q-11](prd.md#q-11). The protocol MUST identify reference conditions, eligibility of measurements, run inputs, evidence to retain and how to determine target pass or fail. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012), [Q-11](prd.md#q-11) | Measurement and evidence review | [AC-100](acceptance-criteria.md#ac-100) | APPROVED |


## Observability Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-016"></a> NFR-016 | Operational telemetry | The release MUST expose approved operational signals for Prometheus and provide a Grafana view of system health. | v1.0.0 Release | Must | [F-023](prd.md#f-023), [D-005](../project/decision-register.md#d-005), [Q-15](prd.md#q-15) | Controlled integration test | [AC-072](acceptance-criteria.md#ac-072) | READY FOR OWNER APPROVAL |
| <a id="nfr-032"></a> NFR-032 | Execution diagnostics | Operators MUST be able to distinguish execution delays, backlog, internal failure and notification failure without exposing secrets. | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [F-006](prd.md#f-006), [F-009](prd.md#f-009), [D-005](../project/decision-register.md#d-005), [PD-012](../project/decision-register.md#pd-012), [Q-11](prd.md#q-11) | Controlled integration test | [AC-096](acceptance-criteria.md#ac-096) | READY FOR OWNER APPROVAL |


## Accessibility Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-028"></a> NFR-028 | Accessible controls and status | Interactive product surfaces MUST target WCAG 2.2 AA, with keyboard access, visible focus, readable contrast and status distinctions beyond color. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [PD-013](../project/decision-register.md#pd-013), [Q-14](prd.md#q-14) | Browser walkthrough and inspection | [AC-092](acceptance-criteria.md#ac-092) | APPROVED |

## Verification Approach

Use controlled functional and security integration tests, browser walkthroughs, deterministic clocks and performance measurement. Check the given conditions, observed result and any prohibited side effects. See [Acceptance Criteria](acceptance-criteria.md) for cases and [traceability](requirements-traceability-matrix.md) for coverage. Test execution awaits implementation and approved environments.

## Constraints and Assumptions

The product inherits the approved architecture and documented release boundaries. Detailed storage, contracts, dependency versions, worker model and provider or deployment choices belong to later gates. Use authorized synthetic targets in verification. Measurement and implementation dependencies are recorded in the applicable decision.

## Approved decisions and deferred design

The [IP-004 decisions](prd.md#ip-004-product-decisions) record approved parameters and design deferrals. Requirement rows link back to the applicable decisions as sources. APPROVED denotes an explicitly approved product obligation. READY FOR OWNER APPROVAL denotes derived specification text. DEFERRED denotes an existing identifier retained for an obligation whose details need further approval.

## Performance measurement protocol

The approved reference environment is 4 vCPU, 8 GB RAM and SSD, with 20 concurrent API users, a 5-minute warm-up and 30 minutes of measurement. Use controlled targets. Apply the baseline gates to 1,000 active monitors at 60 seconds. Run the 1,000-monitor 30-second profile separately as capacity stress evidence.

| Profile | Interval | Calculated checks/s | Calculated 30-day results |
|---|---:|---:|---:|
| Baseline | 60 seconds | 16.67 | 43.2 million |
| Capacity stress | 30 seconds | 33.33 | 86.4 million |

Volumes assume continuous workload and one result per due opportunity. Record actual attempted, completed, excluded and missing observations. Report API latency excluding external check duration, API server error rate, scheduled due-to-start delay and backlog. Retain reproduction inputs, commands, run identifiers, fixture seeds, candidate revision, settings and sanitized measurements. Stage 07 approves the precise dataset, endpoints, request profile, workload validity rules and backend line coverage scope.

[AC-100](acceptance-criteria.md#ac-100) checks protocol reproducibility. [AC-087](acceptance-criteria.md#ac-087) and [AC-089](acceptance-criteria.md#ac-089) evaluate attainment. PASS requires valid evidence meeting all applicable targets. A candidate missing an approved gate in a valid test is FAIL. Missing approved inputs or unusable evidence is INCOMPLETE. Stress characterization follows [AC-088](acceptance-criteria.md#ac-088). These are targets and no Product Discovery measurements exist.

## Beta check contracts

All Beta checks inherit installation destination and secret policies. Enforce bounded execution, response size and computation where applicable.

| Type | Approved behavior |
|---|---|
| TCP | Check TCP port reachability within the configured deadline. |
| SSL | Check certificate validity and remaining lifetime. |
| HTTP keyword | Find a configured literal string in the HTTP response. |
| JSON assertion | Verify a bounded declarative assertion on JSON values without executing user code. Malformed JSON fails. |

Define exact limits, comparison operators, certificate timing boundaries and detailed input and diagnostics contracts before Beta implementation.

## Beta authorization matrix

Approved under [Q-07](prd.md#q-07). All permissions require current membership and workspace scope. Installation policy requires installation authority. Public access is limited to intentionally published status content.

| Permission | Owner | Admin | Member | Viewer |
|---|---|---|---|---|
| View monitors | Yes | Yes | Yes | Yes |
| View incidents | Yes | Yes | Yes | Yes |
| Create/edit monitors | Yes | Yes | Yes | No |
| Delete monitors | Yes | Yes | No | No |
| Run manual checks | Yes | Yes | Yes | No |
| Manage notifications | Yes | Yes | No | No |
| Manage team | Yes | Yes | No | No |
| Manage API keys | Yes | Yes | No | No |
| Transfer ownership | Yes | No | No | No |
| Delete workspace | Yes | No | No | No |

Admin cannot change Owner permissions or appoint an Owner. The last Owner cannot leave without transferring ownership. Permissions for operations outside this matrix require approval before Beta implementation.

## References

- [Product Requirements Document](prd.md)
- [Project Charter](../project/charter.md)
- [Decision Register](../project/decision-register.md)
- [Business Rules](business-rules.md)
- [Acceptance Criteria](acceptance-criteria.md)
- [Requirements Traceability Matrix](requirements-traceability-matrix.md)
- [Glossary](../project/glossary.md)
