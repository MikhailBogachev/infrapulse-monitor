# InfraPulse Software Requirements Specification

| Field | Value |
|---|---|
| Document Status | DRAFT — PENDING VALIDATION |
| Version | 0.1 |
| Responsible Role | Requirements Engineer |
| Related Project Stage | Stage 01 — Product Discovery |
| Project Task | IP-003 |
| Validation | IP-004, pending owner review |

## Purpose and Scope

This specification describes verifiable InfraPulse behavior from MVP through v1.0.0. It inherits approved release boundaries and does not define API contracts, data schemas or deployment architecture.

## Definitions and References

Words use the [glossary](../project/glossary.md) and [business rules](business-rules.md). MUST denotes mandatory intent, SHOULD denotes recommended behavior requiring documented deviation if accepted, and MAY denotes permission. Normative intent in this document is subject to its status. DERIVED DRAFT indicates a requirement derived from approved scope and awaiting validation. PROPOSED indicates specific unresolved behavior. PENDING indicates a missing decision or input. APPROVED is reserved for the explicitly approved rules and source decisions.

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
| <a id="fr-001"></a> FR-001 | Bootstrap first account | The installation MUST provide an operator-authorized path to establish the first account while public registration is disabled. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001) | Controlled integration test | [AC-001](acceptance-criteria.md#ac-001) | DERIVED DRAFT · [Q-01](prd.md#q-01) |
| <a id="fr-002"></a> FR-002 | Close bootstrap | The installation MUST prevent unauthorized bootstrap and reuse after initial setup. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001) | Controlled integration test | [AC-002](acceptance-criteria.md#ac-002) | DERIVED DRAFT · [Q-01](prd.md#q-01) |
| <a id="fr-003"></a> FR-003 | Default registration policy | The installation MUST disable public registration by default after initial setup. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001) | Controlled integration test | [AC-003](acceptance-criteria.md#ac-003) | DERIVED DRAFT |
| <a id="fr-004"></a> FR-004 | Operator registration control | The installation MUST enforce the operator's current public registration setting. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001) | Controlled integration test | [AC-004](acceptance-criteria.md#ac-004) | DERIVED DRAFT |
| <a id="fr-005"></a> FR-005 | Issue and validate JWT access tokens | The product MUST issue a JWT access token and a refresh token after valid sign-in, authenticate protected access using a valid JWT, and reject invalid account credentials and missing, invalid or expired access tokens. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-005](acceptance-criteria.md#ac-005) | DERIVED DRAFT · [Q-01](prd.md#q-01) |
| <a id="fr-006"></a> FR-006 | Renew JWT access | The product MUST issue a new JWT access token on presentation of a valid refresh token for an eligible session, including after access token expiry. Missing, invalid or expired refresh tokens MUST be rejected without renewing access. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-006](acceptance-criteria.md#ac-006) | DERIVED DRAFT · [Q-01](prd.md#q-01) |
| <a id="fr-007"></a> FR-007 | Sign out | The product MUST end the active session on sign-out and reject subsequent renewal with its previously valid refresh token. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-007](acceptance-criteria.md#ac-007) | DERIVED DRAFT · [Q-01](prd.md#q-01) |
| <a id="fr-008"></a> FR-008 | Account settings | The product SHOULD let an authenticated user view and manage their own approved account settings. | v0.1.0 MVP | Should | [F-001](prd.md#f-001), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-008](acceptance-criteria.md#ac-008) | PROPOSED · [Q-01](prd.md#q-01) |


## Authorization Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-009"></a> FR-009 | MVP ownership | The product MUST authorize the Owner to manage resources within their own workspace. | v0.1.0 MVP | Must | [F-002](prd.md#f-002), [PD-007](../project/decision-register.md#pd-007) | Security verification with controlled fixtures | [AC-009](acceptance-criteria.md#ac-009) | DERIVED DRAFT |
| <a id="nfr-001"></a> NFR-001 | Workspace isolation | Every protected workspace operation MUST enforce current workspace authorization, including access to background effects, live updates and exports where applicable. | v0.1.0 MVP | Must | [F-002](prd.md#f-002), [PD-007](../project/decision-register.md#pd-007) | Security verification with controlled fixtures | [AC-010](acceptance-criteria.md#ac-010) | DERIVED DRAFT |
| <a id="fr-010"></a> FR-010 | Workspace settings | The product MUST limit workspace settings to permitted workspace-level controls and deny installation policy changes through workspace authority. | v0.1.0 MVP | Must | [F-002](prd.md#f-002), [PD-006](../project/decision-register.md#pd-006), [PD-007](../project/decision-register.md#pd-007), [PD-001](../project/decision-register.md#pd-001) | Security verification with controlled fixtures | [AC-011](acceptance-criteria.md#ac-011) | DERIVED DRAFT · [Q-01](prd.md#q-01) |
| <a id="fr-048"></a> FR-048 | Team authorization | Beta MUST enforce workspace membership and role-based authorization for covered operations. | v0.5.0 Beta | Must | [F-017](prd.md#f-017), [PD-007](../project/decision-register.md#pd-007) | Security verification with controlled fixtures | [AC-063](acceptance-criteria.md#ac-063) | DERIVED DRAFT · [Q-07](prd.md#q-07) |
| <a id="fr-049"></a> FR-049 | Candidate Beta roles | Beta SHOULD apply the proposed Owner, Admin, Member and Viewer permissions including Owner continuity. | v0.5.0 Beta | Should | [F-017](prd.md#f-017), [F-032](prd.md#f-032), [PD-007](../project/decision-register.md#pd-007) | Security verification with controlled fixtures | [AC-064](acceptance-criteria.md#ac-064) | PROPOSED · [Q-07](prd.md#q-07) |
| <a id="fr-050"></a> FR-050 | Invite workspace participants | An authorized actor MUST be able to invite a participant to the actor's workspace. | v0.5.0 Beta | Must | [F-032](prd.md#f-032), [PD-001](../project/decision-register.md#pd-001), [PD-007](../project/decision-register.md#pd-007) | Security verification with controlled fixtures | [AC-065](acceptance-criteria.md#ac-065) | DERIVED DRAFT · [Q-07](prd.md#q-07) |
| <a id="fr-051"></a> FR-051 | Manage workspace membership | An authorized actor MUST be able to manage memberships within their own workspace. | v0.5.0 Beta | Must | [F-032](prd.md#f-032), [PD-007](../project/decision-register.md#pd-007) | Security verification with controlled fixtures | [AC-066](acceptance-criteria.md#ac-066) | DERIVED DRAFT · [Q-07](prd.md#q-07) |


## Monitor management and check execution

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-011"></a> FR-011 | Create monitor | The Owner MUST be able to create a valid monitor and see its configuration in their workspace. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-012](acceptance-criteria.md#ac-012) | DERIVED DRAFT |
| <a id="fr-012"></a> FR-012 | Read monitor | The Owner MUST be able to list and inspect their workspace monitors. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-013](acceptance-criteria.md#ac-013) | DERIVED DRAFT |
| <a id="fr-013"></a> FR-013 | Edit monitor | The Owner MUST be able to save a valid configuration change to their monitor. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-014](acceptance-criteria.md#ac-014) | DERIVED DRAFT |
| <a id="fr-014"></a> FR-014 | Delete monitor | The Owner MUST be able to delete a monitor and thereby stop new executions for it. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-015](acceptance-criteria.md#ac-015) | DERIVED DRAFT |
| <a id="fr-015"></a> FR-015 | Pause and resume recurring checks | The Owner MUST be able to suspend and resume recurring checks. The product MUST prevent new recurring target checks from starting while paused, including checks whose jobs were queued before pause but had not started. The product MUST NOT fabricate observations for work that did not execute. Paused manual execution is a separate open decision under [Q-03](prd.md#q-03). | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [F-005](prd.md#f-005), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-016](acceptance-criteria.md#ac-016) | DERIVED DRAFT |
| <a id="fr-016"></a> FR-016 | HTTP methods | HTTP monitors MUST support GET and HEAD and reject other methods and arbitrary request bodies. | v0.1.0 MVP | Must | [F-004](prd.md#f-004), [PD-002](../project/decision-register.md#pd-002) | Controlled integration test | [AC-017](acceptance-criteria.md#ac-017) | DERIVED DRAFT |
| <a id="fr-017"></a> FR-017 | HTTP success condition | The product MUST evaluate an HTTP response against the monitor's expected status condition. | v0.1.0 MVP | Must | [F-004](prd.md#f-004), [PD-002](../project/decision-register.md#pd-002) | Controlled integration test | [AC-018](acceptance-criteria.md#ac-018) | DERIVED DRAFT · [Q-02](prd.md#q-02) |
| <a id="fr-018"></a> FR-018 | HTTP defaults | New HTTP monitors SHOULD default to GET, a 10-second timeout, accepted statuses 200–299, redirects disabled and TLS verification enabled. | v0.1.0 MVP | Should | [F-004](prd.md#f-004), [PD-002](../project/decision-register.md#pd-002) | Controlled integration test | [AC-019](acceptance-criteria.md#ac-019) | PROPOSED · [Q-02](prd.md#q-02) |
| <a id="fr-019"></a> FR-019 | Timeout classification | A check that reaches its configured target request deadline MUST yield a target timeout when execution was healthy up to that deadline. | v0.1.0 MVP | Must | [F-004](prd.md#f-004), [PD-003](../project/decision-register.md#pd-003), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-020](acceptance-criteria.md#ac-020) | DERIVED DRAFT |
| <a id="fr-020"></a> FR-020 | Minimum interval | The product MUST reject monitoring intervals below 30 seconds and allow a 30-second configuration. | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [PD-003](../project/decision-register.md#pd-003) | Controlled integration test | [AC-021](acceptance-criteria.md#ac-021) | DERIVED DRAFT |
| <a id="fr-021"></a> FR-021 | Interval defaults and range | The interval SHOULD default to 60 seconds and allow integer-second values through 24 hours inclusive. | v0.1.0 MVP | Should | [F-005](prd.md#f-005), [PD-003](../project/decision-register.md#pd-003) | Controlled integration test | [AC-022](acceptance-criteria.md#ac-022) | PROPOSED · [Q-02](prd.md#q-02) |
| <a id="fr-022"></a> FR-022 | Recurring execution | Active monitors MUST receive recurring background checks according to their configured interval, subject to visible execution delays and failures. | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-023](acceptance-criteria.md#ac-023) | DERIVED DRAFT |
| <a id="fr-023"></a> FR-023 | Request immediate check | The product MUST let an authorized user request an asynchronous Run Check Now execution and inspect its progress and outcome. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [PD-005](../project/decision-register.md#pd-005) | Controlled integration test | [AC-027](acceptance-criteria.md#ac-027) | DERIVED DRAFT |
| <a id="fr-024"></a> FR-024 | Persist manual result | The product MUST save completed manual check results in the monitor history with their manual origin. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [F-007](prd.md#f-007), [PD-005](../project/decision-register.md#pd-005) | Controlled integration test | [AC-028](acceptance-criteria.md#ac-028) | DERIVED DRAFT |
| <a id="fr-025"></a> FR-025 | Authorize manual execution | The product MUST authorize manual execution against the monitor's workspace before accepting work. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [PD-005](../project/decision-register.md#pd-005), [PD-007](../project/decision-register.md#pd-007) | Controlled integration test | [AC-029](acceptance-criteria.md#ac-029) | DERIVED DRAFT |
| <a id="fr-026"></a> FR-026 | Prevent overlapping execution | The product MUST prevent duplicate effective executions when concurrent manual requests or a manual and scheduled opportunity collide. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [F-005](prd.md#f-005), [PD-005](../project/decision-register.md#pd-005) | Controlled integration test | [AC-031](acceptance-criteria.md#ac-031) | DERIVED DRAFT |
| <a id="fr-027"></a> FR-027 | Manual check on paused monitor | If the paused behavior proposed in [Q-03](prd.md#q-03) is approved, the product SHOULD reject manual execution on a paused monitor and explain how to resume. | v0.1.0 MVP | Should | [F-029](prd.md#f-029), [F-003](prd.md#f-003), [PD-005](../project/decision-register.md#pd-005) | Controlled integration test | [AC-032](acceptance-criteria.md#ac-032) | PROPOSED · [Q-03](prd.md#q-03) |
| <a id="fr-028"></a> FR-028 | Manual observation effects | Manual execution SHOULD preserve scheduled cadence and remain outside scheduled availability, latency and incident calculations. | v0.1.0 MVP | Should | [F-029](prd.md#f-029), [F-005](prd.md#f-005), [F-008](prd.md#f-008), [F-033](prd.md#f-033), [PD-005](../project/decision-register.md#pd-005), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-033](acceptance-criteria.md#ac-033) | PROPOSED · [Q-03](prd.md#q-03) |
| <a id="fr-029"></a> FR-029 | Collision disposition | A manual request SHOULD point the Owner to any already accepted execution. A due scheduled opportunity overlapping a manual execution SHOULD remain a skipped opportunity. | v0.1.0 MVP | Should | [F-029](prd.md#f-029), [F-005](prd.md#f-005), [PD-005](../project/decision-register.md#pd-005) | Controlled integration test | [AC-034](acceptance-criteria.md#ac-034) | PROPOSED · [Q-03](prd.md#q-03) |
| <a id="fr-043"></a> FR-043 | TCP check | An authorized workspace user MUST be able to verify connection establishment to a configured host and valid TCP port under installation policy. | v0.5.0 Beta | Must | [F-013](prd.md#f-013), [PD-009](../project/decision-register.md#pd-009) | Controlled integration test | [AC-058](acceptance-criteria.md#ac-058) | DERIVED DRAFT · [Q-09](prd.md#q-09) |
| <a id="fr-044"></a> FR-044 | Certificate check | An authorized workspace user MUST be able to check the TLS certificate expiry of a configured host and port against a validated expiry threshold. | v0.5.0 Beta | Must | [F-014](prd.md#f-014), [PD-009](../project/decision-register.md#pd-009) | Controlled-clock test | [AC-059](acceptance-criteria.md#ac-059) | DERIVED DRAFT · [Q-09](prd.md#q-09) |
| <a id="fr-045"></a> FR-045 | Certificate boundary policy | The certificate check SHOULD succeed at or above a nonnegative minimum remaining lifetime while a certificate at or past its expiry instant SHOULD fail. | v0.5.0 Beta | Should | [F-014](prd.md#f-014), [PD-009](../project/decision-register.md#pd-009) | Controlled-clock test | [AC-060](acceptance-criteria.md#ac-060) | PROPOSED · [Q-09](prd.md#q-09) |
| <a id="fr-059"></a> FR-059 | HTTP keyword check | An authorized workspace user MUST be able to require a literal keyword in an eligible HTTP response body. | v0.5.0 Beta | Must | [F-030](prd.md#f-030), [PD-009](../project/decision-register.md#pd-009) | Controlled integration test | [AC-080](acceptance-criteria.md#ac-080) | DERIVED DRAFT · [Q-09](prd.md#q-09) |
| <a id="fr-060"></a> FR-060 | JSON assertion check | An authorized workspace user MUST be able to verify a bounded declarative assertion against an eligible well-formed JSON response. Executable configuration input MUST be rejected. Malformed JSON classification is conditional on [Q-09](prd.md#q-09). | v0.5.0 Beta | Must | [F-031](prd.md#f-031), [PD-009](../project/decision-register.md#pd-009) | Controlled integration test | [AC-081](acceptance-criteria.md#ac-081), [AC-099](acceptance-criteria.md#ac-099) | DERIVED DRAFT · [Q-09](prd.md#q-09) |


## History and incidents

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-030"></a> FR-030 | Inspect check history | The Owner MUST be able to inspect authorized check outcomes, times, origin and diagnostic class, including empty history. | v0.1.0 MVP | Must | [F-007](prd.md#f-007), [D-005](../project/decision-register.md#d-005), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-035](acceptance-criteria.md#ac-035) | DERIVED DRAFT |
| <a id="fr-031"></a> FR-031 | Configure thresholds | The Owner MUST be able to configure both incident thresholds, whose defaults are three failures and two successes. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-037](acceptance-criteria.md#ac-037) | DERIVED DRAFT · [Q-04](prd.md#q-04) |
| <a id="fr-032"></a> FR-032 | Open at failure threshold | The product MUST open an incident upon reaching the configured consecutive qualifying failure threshold. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-038](acceptance-criteria.md#ac-038) | DERIVED DRAFT |
| <a id="fr-033"></a> FR-033 | Recover at success threshold | The product MUST close the active incident upon reaching the configured consecutive qualifying success threshold. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-039](acceptance-criteria.md#ac-039) | DERIVED DRAFT |
| <a id="fr-034"></a> FR-034 | Inspect incidents | The Owner MUST be able to list and inspect incidents with their current disposition and available time evidence. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-040](acceptance-criteria.md#ac-040) | DERIVED DRAFT |
| <a id="fr-035"></a> FR-035 | Exclude platform faults | The product MUST classify an internal or policy-blocked execution distinctly from a qualifying target failure. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [F-007](prd.md#f-007), [PD-004](../project/decision-register.md#pd-004), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-041](acceptance-criteria.md#ac-041) | DERIVED DRAFT |
| <a id="fr-036"></a> FR-036 | State and streak transitions | The state and counter rules SHOULD follow the proposed transition table, including streak isolation across lifecycle and configuration changes. | v0.1.0 MVP | Should | [F-008](prd.md#f-008), [F-003](prd.md#f-003), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-042](acceptance-criteria.md#ac-042) | PROPOSED · [Q-04](prd.md#q-04) |
| <a id="fr-037"></a> FR-037 | Late observations | The product SHOULD retain eligible late results while excluding superseded or out-of-order observations from live state transitions. | v0.1.0 MVP | Should | [F-008](prd.md#f-008), [F-007](prd.md#f-007), [PD-004](../project/decision-register.md#pd-004), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-043](acceptance-criteria.md#ac-043) | PROPOSED · [Q-04](prd.md#q-04) · [Q-08](prd.md#q-08) |


## External Integration Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-038"></a> FR-038 | Configure Telegram | The Owner MUST be able to configure and disable Telegram delivery for their workspace. The product MUST protect destination credentials and suppress new deliveries while the channel is disabled. | v0.1.0 MVP | Must | [F-009](prd.md#f-009), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-044](acceptance-criteria.md#ac-044) | DERIVED DRAFT |
| <a id="fr-039"></a> FR-039 | Deliver permitted Telegram notifications | Given a correctly configured and enabled Telegram channel, a permitted incident transition and a provider able to confirm successful delivery, the product MUST deliver the notification to the configured recipient. Sequential replay and concurrent processing of one logical notification event for the same destination MUST preserve one business effect. With a determinate successful provider outcome, concurrent processing MUST yield one received notification, and replay after confirmed delivery MUST yield no additional notification. Confirmed delivery failure is covered by [NFR-007](srs.md#nfr-007). Default event preferences and retry handling when receipt cannot be confirmed or ruled out remain open under [Q-05](prd.md#q-05). | v0.1.0 MVP | Must | [F-009](prd.md#f-009), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-045](acceptance-criteria.md#ac-045) | DERIVED DRAFT · [Q-05](prd.md#q-05) |
| <a id="fr-065"></a> FR-065 | Default Telegram event preferences | If approved under [Q-05](prd.md#q-05), configured Telegram delivery SHOULD enable incident opening and confirmed recovery by default. | v0.1.0 MVP | Should | [F-009](prd.md#f-009), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-097](acceptance-criteria.md#ac-097) | PROPOSED · [Q-05](prd.md#q-05) |
| <a id="fr-046"></a> FR-046 | Email notifications | The product MUST let an authorized user configure email notifications for incident transitions. | v0.5.0 Beta | Must | [F-015](prd.md#f-015), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-061](acceptance-criteria.md#ac-061) | DERIVED DRAFT |
| <a id="fr-047"></a> FR-047 | Webhook notifications | The product MUST let an authorized user configure a policy-eligible webhook for incident transitions. | v0.5.0 Beta | Must | [F-016](prd.md#f-016), [D-005](../project/decision-register.md#d-005), [PD-006](../project/decision-register.md#pd-006) | Controlled integration test | [AC-062](acceptance-criteria.md#ac-062) | DERIVED DRAFT · [Q-10](prd.md#q-10) |


## User Interface Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-040"></a> FR-040 | Dashboard summary | The Owner MUST be able to inspect workspace monitor states, recent observations and incidents and navigate to their details. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-047](acceptance-criteria.md#ac-047) | DERIVED DRAFT |
| <a id="fr-041"></a> FR-041 | Polling and stale data | Browser-initiated polling MUST refresh changing operational data on [UI-003](user-flows.md#ui-003), [UI-004](user-flows.md#ui-004), [UI-006](user-flows.md#ui-006), [UI-007](user-flows.md#ui-007), [UI-008](user-flows.md#ui-008), [UI-009](user-flows.md#ui-009) while the view is open, as defined in the [MVP polling scope](user-flows.md#mvp-polling-scope). Each view MUST distinguish initial loading, stale retained data and refresh failure, and show current authorized data after recovery without manual reload. Cadence and freshness tolerances remain open under [Q-12](prd.md#q-12). | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [PD-008](../project/decision-register.md#pd-008) | Controlled integration test | [AC-048](acceptance-criteria.md#ac-048) | DERIVED DRAFT · [Q-12](prd.md#q-12) |
| <a id="fr-042"></a> FR-042 | Beta live updates | Beta MUST deliver live operational updates through Server-Sent Events and reconcile displayed authorized data after reconnecting. Reconnect behavior and timing tolerances remain under [Q-12](prd.md#q-12). | v0.5.0 Beta | Must | [F-010](prd.md#f-010), [F-018](prd.md#f-018), [PD-008](../project/decision-register.md#pd-008) | Controlled integration test | [AC-049](acceptance-criteria.md#ac-049) | DERIVED DRAFT · [Q-12](prd.md#q-12) |
| <a id="nfr-027"></a> NFR-027 | Dark-only presentation | All product views MUST use the dark theme across release scopes and host theme preferences. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [PD-013](../project/decision-register.md#pd-013) | Browser walkthrough and inspection | [AC-091](acceptance-criteria.md#ac-091) | DERIVED DRAFT |
| <a id="nfr-029"></a> NFR-029 | Desktop-first responsive interface | The web interface MUST preserve the principal navigation, dashboard, monitor management, incident and account settings journeys on mobile viewports. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [F-008](prd.md#f-008), [F-010](prd.md#f-010), [F-001](prd.md#f-001), [PD-014](../project/decision-register.md#pd-014) | Browser walkthrough and inspection | [AC-093](acceptance-criteria.md#ac-093) | DERIVED DRAFT · [Q-14](prd.md#q-14) |
| <a id="nfr-030"></a> NFR-030 | English product surfaces | UI text, technical messages, repository documentation and source identifiers and comments MUST be in English. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [PD-015](../project/decision-register.md#pd-015), [D-006](../project/decision-register.md#d-006) | Browser walkthrough and inspection | [AC-094](acceptance-criteria.md#ac-094) | DERIVED DRAFT |


## Analytics and publishing

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-052"></a> FR-052 | Extended analytics | Beta MUST let authorized users compare availability and successful check latency across supported windows and eligible monitors. Combined multi-monitor analytics remain a separate proposal under [Q-06](prd.md#q-06). | v0.5.0 Beta | Must | [F-018](prd.md#f-018), [F-033](prd.md#f-033), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-067](acceptance-criteria.md#ac-067) | DERIVED DRAFT · [Q-06](prd.md#q-06) |
| <a id="fr-066"></a> FR-066 | Combined multi-monitor analytics | If approved under [Q-06](prd.md#q-06), Beta SHOULD show combined availability and successful-check latency for the selected eligible monitors using the policy approved for the combined sample. | v0.5.0 Beta | Should | [F-018](prd.md#f-018), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-098](acceptance-criteria.md#ac-098) | PROPOSED · [Q-06](prd.md#q-06) |
| <a id="fr-053"></a> FR-053 | Publish status page | An authorized user MUST be able to publish a public status view restricted to intentionally selected monitors. | v0.5.0 Beta | Must | [F-019](prd.md#f-019), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-068](acceptance-criteria.md#ac-068) | DERIVED DRAFT · [Q-15](prd.md#q-15) |
| <a id="fr-054"></a> FR-054 | Schedule maintenance | An authorized user MUST be able to schedule and inspect a maintenance window for authorized monitors. Maintenance effects on availability and latency remain open under [Q-15](prd.md#q-15). | v0.5.0 Beta | Must | [F-020](prd.md#f-020), [D-005](../project/decision-register.md#d-005) | Controlled-clock test | [AC-069](acceptance-criteria.md#ac-069) | DERIVED DRAFT · [Q-15](prd.md#q-15) |
| <a id="fr-055"></a> FR-055 | Manage API keys | Beta MUST let an authorized user create and revoke workspace-scoped API keys. | v0.5.0 Beta | Must | [F-021](prd.md#f-021), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-070](acceptance-criteria.md#ac-070) | DERIVED DRAFT · [Q-07](prd.md#q-07) · [Q-15](prd.md#q-15) |
| <a id="fr-056"></a> FR-056 | Inspect audit log | An authorized user MUST be able to inspect an audit trail of defined workspace actions. | v1.0.0 Release | Must | [F-022](prd.md#f-022), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-071](acceptance-criteria.md#ac-071) | DERIVED DRAFT · [Q-15](prd.md#q-15) |
| <a id="fr-057"></a> FR-057 | Export reports | An authorized user MUST be able to export an authorized monitoring report within the supported selection. | v1.0.0 Release | Must | [F-024](prd.md#f-024), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-073](acceptance-criteria.md#ac-073) | DERIVED DRAFT · [Q-15](prd.md#q-15) |
| <a id="fr-061"></a> FR-061 | Calculate uptime | The product MUST show per-monitor uptime as qualifying successes divided by all qualifying completed observations, expressed as a percentage over the selected window. | v0.1.0 MVP | Must | [F-033](prd.md#f-033), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-083](acceptance-criteria.md#ac-083) | DERIVED DRAFT · [Q-03](prd.md#q-03) · [Q-06](prd.md#q-06) |
| <a id="fr-062"></a> FR-062 | Calculate successful latency | The product MUST use only qualifying successful checks when calculating average latency and supported latency percentiles. | v0.1.0 MVP | Must | [F-033](prd.md#f-033), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-084](acceptance-criteria.md#ac-084) | DERIVED DRAFT · [Q-03](prd.md#q-03) · [Q-06](prd.md#q-06) |
| <a id="fr-063"></a> FR-063 | Show incomplete observations | The product MUST distinguish empty samples, excluded observations, pauses and missing observations from measured availability. A window without qualifying observations MUST show availability as unavailable and MUST NOT report 100% uptime. Exact window and sample conventions require [Q-06](prd.md#q-06). | v0.1.0 MVP | Must | [F-033](prd.md#f-033), [F-010](prd.md#f-010), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-085](acceptance-criteria.md#ac-085) | DERIVED DRAFT · [Q-06](prd.md#q-06) |
| <a id="fr-064"></a> FR-064 | Single-monitor metric conventions | MVP SHOULD apply the proposed window boundaries, rounding, sample minimums and percentile rules to one monitor at a time. | v0.1.0 MVP | Should | [F-033](prd.md#f-033), [PD-011](../project/decision-register.md#pd-011) | Controlled-clock test | [AC-086](acceptance-criteria.md#ac-086) | PROPOSED · [Q-06](prd.md#q-06) · [Q-03](prd.md#q-03) |


## Interactive demo

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-058"></a> FR-058 | Interactive demo journey | Public demo visitors MUST receive an isolated session and be able to take at least one permitted interactive action within the approved monitor and incident scope. The action MUST cause a controlled synthetic monitoring scenario to execute or change and MUST expose the resulting outcome through an existing product surface. The specific scenario and permitted action set remain open under [Q-13](prd.md#q-13). | v1.0.0 Release | Must | [F-025](prd.md#f-025), [PD-010](../project/decision-register.md#pd-010) | Security verification with controlled fixtures | [AC-074](acceptance-criteria.md#ac-074) | DERIVED DRAFT · [Q-13](prd.md#q-13) |
| <a id="nfr-017"></a> NFR-017 | Demo network containment | Demo sessions MUST be restricted to controlled synthetic destinations and deny arbitrary scanning and notifications to external recipients. | v1.0.0 Release | Must | [F-025](prd.md#f-025), [F-027](prd.md#f-027), [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006), [PD-010](../project/decision-register.md#pd-010) | Security verification with controlled fixtures | [AC-075](acceptance-criteria.md#ac-075) | DERIVED DRAFT |
| <a id="nfr-018"></a> NFR-018 | Public deployment isolation | The public demo MUST isolate real deployments and data and prevent visitor sessions from reading or mutating each other's mutable data. | v1.0.0 Release | Must | [F-027](prd.md#f-027), [PD-010](../project/decision-register.md#pd-010) | Security verification with controlled fixtures | [AC-076](acceptance-criteria.md#ac-076) | DERIVED DRAFT |
| <a id="nfr-019"></a> NFR-019 | Demo resource and data lifecycle | The public demo MUST enforce finite resource limits and complete data cleanup after the validated lifecycle trigger. Verify deletion of in-scope data or completion of another cleanup method explicitly approved under [Q-13](prd.md#q-13). Access denial alone does not satisfy cleanup. | v1.0.0 Release | Must | [F-027](prd.md#f-027), [PD-010](../project/decision-register.md#pd-010) | Security verification with controlled fixtures | [AC-077](acceptance-criteria.md#ac-077) | DERIVED DRAFT · [Q-13](prd.md#q-13) |


## Non-functional Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-013"></a> NFR-013 | Local operation | The project MUST support documented self-hosted startup using one Docker Compose command after documented prerequisites and configuration. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [D-004](../project/decision-register.md#d-004), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-055](acceptance-criteria.md#ac-055) | DERIVED DRAFT |
| <a id="nfr-014"></a> NFR-014 | Migration readiness | The supported setup and upgrade procedure MUST apply required data migrations while preserving supported existing data. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-056](acceptance-criteria.md#ac-056) | DERIVED DRAFT |
| <a id="nfr-015"></a> NFR-015 | CI assurance | For each eligible change, repository CI MUST execute the required MVP automated tests and quality checks in GitHub Actions and report their actual outcomes under [D-010](../project/decision-register.md#d-010). Measurement inputs and scope remain open under [Q-11](prd.md#q-11). | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [D-005](../project/decision-register.md#d-005), [D-010](../project/decision-register.md#d-010) | GitHub Actions run evidence for controlled passing and failing changes | [AC-057](acceptance-criteria.md#ac-057) | DERIVED DRAFT |
| <a id="nfr-020"></a> NFR-020 | Release integration and load evidence | The project MUST record integration and load verification results for the release under the documented repeatable profiles. | v1.0.0 Release | Must | [F-026](prd.md#f-026), [D-005](../project/decision-register.md#d-005), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-078](acceptance-criteria.md#ac-078) | DERIVED DRAFT |
| <a id="nfr-021"></a> NFR-021 | Release documentation | The release MUST provide English installation, operation, usage and safe demo documentation for supported features. | v1.0.0 Release | Must | [F-028](prd.md#f-028), [D-005](../project/decision-register.md#d-005), [PD-015](../project/decision-register.md#pd-015) | Measurement and evidence review | [AC-079](acceptance-criteria.md#ac-079) | DERIVED DRAFT |
| <a id="nfr-025"></a> NFR-025 | Backend test coverage | Backend test coverage MUST reach at least 80% using the approved measurement scope and metric under [Q-11](prd.md#q-11). | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-089](acceptance-criteria.md#ac-089) | DERIVED DRAFT · [Q-11](prd.md#q-11) |


## Security Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-005"></a> NFR-005 | Manual rate limit | The product MUST enforce a finite rate limit on manual requests and surface rejected requests without starting work. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [F-029](prd.md#f-029), [PD-005](../project/decision-register.md#pd-005) | Security verification with controlled fixtures | [AC-030](acceptance-criteria.md#ac-030) | DERIVED DRAFT · [Q-03](prd.md#q-03) |
| <a id="nfr-008"></a> NFR-008 | URL and protocol validation | The product MUST reject invalid target URL syntax, embedded credentials and unsupported scheme or port configuration before connection. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006) | Security verification with controlled fixtures | [AC-050](acceptance-criteria.md#ac-050) | DERIVED DRAFT · [Q-10](prd.md#q-10) |
| <a id="nfr-009"></a> NFR-009 | Restricted destination policy | The installation MUST permit eligible public destinations and deny private IPv4 and IPv6 destinations by default. Only the Installation Operator MAY explicitly allowlist eligible internal destinations. Always-denied sensitive destinations MUST remain blocked even if an allowlist entry conflicts. Workspace Owners MUST NOT override installation policy. Enforce the policy on actual connections and after DNS resolution and redirects, as verified by [NFR-010](srs.md#nfr-010). | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006) | Security verification with controlled fixtures | [AC-051](acceptance-criteria.md#ac-051) | DERIVED DRAFT · [Q-10](prd.md#q-10) |
| <a id="nfr-010"></a> NFR-010 | Resolve and validate every connection | Every actual outbound target connection MUST use a destination validated against current policy, including direct IPs, DNS answers, DNS changes and each redirect hop. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006) | Security verification with controlled fixtures | [AC-052](acceptance-criteria.md#ac-052) | DERIVED DRAFT · [Q-10](prd.md#q-10) |
| <a id="nfr-011"></a> NFR-011 | Protect confidential values | The platform MUST protect credentials and secrets from unauthorized views, diagnostics and unapproved outbound disclosure. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006), [PD-015](../project/decision-register.md#pd-015) | Security verification with controlled fixtures | [AC-053](acceptance-criteria.md#ac-053) | DERIVED DRAFT |
| <a id="nfr-012"></a> NFR-012 | Rate limiting | The installation MUST limit abusive eligible product requests and preserve service for ordinary authorized traffic. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [D-005](../project/decision-register.md#d-005) | Security verification with controlled fixtures | [AC-054](acceptance-criteria.md#ac-054) | DERIVED DRAFT · [Q-10](prd.md#q-10) |
| <a id="nfr-022"></a> NFR-022 | Beta check safety | Additional monitor types MUST use the installation destination policy and bounded target interaction, including response inspection where applicable. | v0.5.0 Beta | Must | [F-011](prd.md#f-011), [F-013](prd.md#f-013), [F-014](prd.md#f-014), [F-030](prd.md#f-030), [F-031](prd.md#f-031), [PD-006](../project/decision-register.md#pd-006), [PD-009](../project/decision-register.md#pd-009) | Security verification with controlled fixtures | [AC-082](acceptance-criteria.md#ac-082) | DERIVED DRAFT · [Q-09](prd.md#q-09) · [Q-10](prd.md#q-10) |


## Data and Retention Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-006"></a> NFR-006 | History retention | Check results MUST remain available within the 30-day retention target, subject to authorized data removal, and expire according to the approved retention rule. | v0.1.0 MVP | Must | [F-007](prd.md#f-007), [PD-012](../project/decision-register.md#pd-012) | Controlled-clock test | [AC-036](acceptance-criteria.md#ac-036) | DERIVED DRAFT · [Q-08](prd.md#q-08) |


## Error Handling Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-007"></a> NFR-007 | Notification failure isolation | A confirmed failure MUST be observable as a delivery outcome independent of incident state. Reattempts for confirmed transient failures eligible under the validated policy MUST be bounded. Retry treatment of an indeterminate provider outcome remains open under [Q-05](prd.md#q-05). | v0.1.0 MVP | Must | [F-009](prd.md#f-009), [F-006](prd.md#f-006), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-046](acceptance-criteria.md#ac-046) | DERIVED DRAFT · [Q-05](prd.md#q-05) |
| <a id="nfr-031"></a> NFR-031 | Actionable errors | Product errors MUST identify the failed action or affected field in English and preserve previously confirmed data. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [F-004](prd.md#f-004), [F-010](prd.md#f-010), [PD-008](../project/decision-register.md#pd-008) | Controlled integration test | [AC-095](acceptance-criteria.md#ac-095) | DERIVED DRAFT |


## Reliability Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-002"></a> NFR-002 | Background execution | Scheduled checks and notification work MUST run in the approved background task system while interactive views remain usable. | v0.1.0 MVP | Must | [F-006](prd.md#f-006), [D-003](../project/decision-register.md#d-003), [D-004](../project/decision-register.md#d-004) | Controlled integration test | [AC-024](acceptance-criteria.md#ac-024) | DERIVED DRAFT |
| <a id="nfr-003"></a> NFR-003 | Worker interruption | The product MUST distinguish delayed, missed or internally failed work during worker unavailability from an observed service failure. | v0.1.0 MVP | Must | [F-006](prd.md#f-006), [F-007](prd.md#f-007), [D-005](../project/decision-register.md#d-005), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-025](acceptance-criteria.md#ac-025) | DERIVED DRAFT |
| <a id="nfr-004"></a> NFR-004 | Application idempotency | Sequential replay and concurrent processing of one logical execution MUST preserve a single effective result, incident transition and business notification trigger per destination. Recipient delivery follows [FR-039](srs.md#fr-039). | v0.1.0 MVP | Must | [F-006](prd.md#f-006), [F-008](prd.md#f-008), [F-009](prd.md#f-009), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-026](acceptance-criteria.md#ac-026) | DERIVED DRAFT |


## Performance Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-023"></a> NFR-023 | Baseline performance target | The platform MUST meet API p95 latency of at most 200 ms under the approved baseline workload with 1,000 active monitors at 60-second intervals. The workload, reference environment and workload-validity checks remain under [Q-11](prd.md#q-11). | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-087](acceptance-criteria.md#ac-087) | DERIVED DRAFT · [Q-11](prd.md#q-11) |
| <a id="nfr-024"></a> NFR-024 | Stress characterization | The performance report MUST characterize the 30-second stress profile as capacity evidence. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-088](acceptance-criteria.md#ac-088) | DERIVED DRAFT · [Q-11](prd.md#q-11) |
| <a id="nfr-026"></a> NFR-026 | Proposed workload protocol | Performance measurement SHOULD follow the proposed warm-up, operation mix, client count, duration and outcome reporting profile. | v0.1.0 MVP | Should | [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-090](acceptance-criteria.md#ac-090) | PROPOSED · [Q-11](prd.md#q-11) |
| <a id="nfr-033"></a> NFR-033 | Repeatable baseline and coverage evidence | The project MUST document a reproducible protocol for baseline performance and backend coverage under [Q-11](prd.md#q-11). The protocol MUST identify reference conditions, eligibility of measurements, run inputs, evidence to retain and how to determine target pass or fail. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-100](acceptance-criteria.md#ac-100) | DERIVED DRAFT · [Q-11](prd.md#q-11) |


## Observability Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-016"></a> NFR-016 | Operational telemetry | The release MUST expose approved operational signals for Prometheus and provide a Grafana view of system health. | v1.0.0 Release | Must | [F-023](prd.md#f-023), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-072](acceptance-criteria.md#ac-072) | DERIVED DRAFT · [Q-15](prd.md#q-15) |
| <a id="nfr-032"></a> NFR-032 | Execution diagnostics | Operators MUST be able to distinguish execution delays, backlog, internal failure and notification failure without exposing secrets. | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [F-006](prd.md#f-006), [F-009](prd.md#f-009), [D-005](../project/decision-register.md#d-005), [PD-012](../project/decision-register.md#pd-012) | Controlled integration test | [AC-096](acceptance-criteria.md#ac-096) | DERIVED DRAFT |


## Accessibility Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-028"></a> NFR-028 | Accessible controls and status | Interactive product surfaces MUST provide readable contrast, keyboard access, visible focus and a perceptible status distinction beyond color. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [PD-013](../project/decision-register.md#pd-013) | Browser walkthrough and inspection | [AC-092](acceptance-criteria.md#ac-092) | DERIVED DRAFT · [Q-14](prd.md#q-14) |

## Verification Approach

Use controlled functional and security integration tests, browser walkthroughs, deterministic clocks and performance measurement. Check the given conditions, observed result and any prohibited side effects. See [Acceptance Criteria](acceptance-criteria.md) for cases and [traceability](requirements-traceability-matrix.md) for coverage. Test execution awaits implementation and approved environments.

## Constraints and Assumptions

The product inherits the approved architecture and documented release boundaries. Detailed storage, contracts, dependency versions, worker model and provider or deployment choices belong to later gates. Use authorized synthetic targets in verification. Proposed timing and sample parameters require approval as listed below.

## Open Requirements

The [open questions](prd.md#open-questions) are the authoritative validation agenda. A question link on an SRS row identifies a parameter or conditional behavior relevant to that requirement. DERIVED DRAFT remains appropriate when the base capability is established. A draft criterion can specify the evidence before the owner approves exact parameters. Contextual links in the PRD identify related scope that can be verified independently of that question.

The table records the disposition of the 59 PRD affected-requirement links that lacked a reciprocal SRS reference in the IP-003 baseline. Existing question references and newly added requirements are outside that count.

| Question | Direct dependencies added to SRS | Contextual links retained in PRD | Verification rationale |
|---|---|---|---|
| [Q-01](prd.md#q-01) | [FR-001](srs.md#fr-001), [FR-002](srs.md#fr-002), [FR-005](srs.md#fr-005), [FR-006](srs.md#fr-006), [FR-007](srs.md#fr-007) | [FR-003](srs.md#fr-003), [FR-004](srs.md#fr-004) | Bootstrap eligibility and verified token lifecycle depend on approved parameters. Default registration and operator control are specified independently. |
| [Q-02](prd.md#q-02) | [FR-017](srs.md#fr-017) | [FR-016](srs.md#fr-016), [FR-019](srs.md#fr-019), [FR-020](srs.md#fr-020) | Status-condition input form affects full verification. Supported methods, timeout classification for a configured deadline and the 30-second floor stand independently. |
| [Q-03](prd.md#q-03) | [FR-061](srs.md#fr-061), [FR-062](srs.md#fr-062), [FR-064](srs.md#fr-064) | [FR-023](srs.md#fr-023), [FR-024](srs.md#fr-024), [FR-025](srs.md#fr-025), [FR-026](srs.md#fr-026), [FR-063](srs.md#fr-063) | Manual-result eligibility affects metric samples. The basic request, storage, authorization, nonduplication and display of missing observations have independent acceptance; disposition and timing have separate cases. |
| [Q-04](prd.md#q-04) | [FR-031](srs.md#fr-031) | [FR-014](srs.md#fr-014), [FR-015](srs.md#fr-015), [FR-032](srs.md#fr-032), [FR-033](srs.md#fr-033), [FR-034](srs.md#fr-034), [FR-035](srs.md#fr-035) | Threshold bounds remain open. Core deletion, scheduled pause, incident thresholds, incident inspection and platform-fault separation are verifiable independently of lifecycle and ordering proposals. |
| [Q-05](prd.md#q-05) | — | [FR-038](srs.md#fr-038), [FR-046](srs.md#fr-046), [FR-047](srs.md#fr-047) | Configured-channel behavior can be tested with an explicitly permitted event. Channel configuration does not require default preferences or a retry model. |
| [Q-06](prd.md#q-06) | [FR-061](srs.md#fr-061), [FR-062](srs.md#fr-062), [FR-063](srs.md#fr-063) | [FR-028](srs.md#fr-028) | Window membership and sample rules affect full metric verification. Manual-result eligibility is governed by Q-03; exact metric conventions are context for that requirement. |
| [Q-07](prd.md#q-07) | [FR-051](srs.md#fr-051), [FR-055](srs.md#fr-055) | — | Role permissions determine who can manage memberships or API keys. |
| [Q-08](prd.md#q-08) | [FR-037](srs.md#fr-037) | [FR-014](srs.md#fr-014) | Retention affects eligible late results. Stopping new executions on monitor deletion is independent of history removal. |
| [Q-09](prd.md#q-09) | [FR-043](srs.md#fr-043), [FR-059](srs.md#fr-059), [FR-060](srs.md#fr-060) | — | Supported input and response limits, matching and edge classification affect full typed-check verification. Basic well-formed JSON matching has a separate mandatory case. |
| [Q-10](prd.md#q-10) | [NFR-008](srs.md#nfr-008), [NFR-010](srs.md#nfr-010), [FR-047](srs.md#fr-047), [NFR-022](srs.md#nfr-022) | [FR-010](srs.md#fr-010), [NFR-011](srs.md#nfr-011), [NFR-017](srs.md#nfr-017) | Exact port and destination policy affects these cases. Installation authority, protection from unauthorized secret disclosure and demo containment remain independently testable. |
| [Q-11](prd.md#q-11) | [NFR-024](srs.md#nfr-024) | [NFR-032](srs.md#nfr-032) | The stress report uses the reference protocol. Basic execution diagnostics can be verified without reference workload targets. |
| [Q-12](prd.md#q-12) | [FR-041](srs.md#fr-041), [FR-042](srs.md#fr-042) | [NFR-031](srs.md#nfr-031) | Timing and recovery details affect full polling and SSE verification. Basic actionable error feedback is independent of approved timing. |
| [Q-13](prd.md#q-13) | [FR-058](srs.md#fr-058) | [NFR-017](srs.md#nfr-017), [NFR-018](srs.md#nfr-018) | The approved demo journey defines full coverage. Synthetic-only containment and session isolation can be verified independently of the final journey and cleanup parameters. |
| [Q-14](prd.md#q-14) | — | [NFR-027](srs.md#nfr-027) | Dark-only appearance is independently verifiable; contrast and responsive evidence have separate criteria. |
| [Q-15](prd.md#q-15) | [FR-053](srs.md#fr-053), [FR-055](srs.md#fr-055), [FR-057](srs.md#fr-057) | — | Published status fields, key scopes and expiry, and export formats affect complete verification. Maintenance effects on metrics remain a gap tied to FR-054; FR-064 covers single-monitor conventions only. |

## Performance measurement protocol

The following targets are approved through PD-012. Measurements are pending implementation and reference profile approval.

| Profile | Active monitors | Interval | Calculated checks/s | Calculated daily results | Calculated 30-day results |
|---|---:|---:|---:|---:|---:|
| Baseline | 1,000 | 60 seconds | 16.67 | 1.44 million | 43.2 million |
| Capacity stress | 1,000 | 30 seconds | 33.33 | 2.88 million | 86.4 million |

Volumes assume one result per due opportunity and a continuous workload. Report actual attempted, completed, excluded and missing observations separately. Apply the 200 ms API p95 target to the approved baseline workload. Stress results are capacity evidence.

| Measurement input | Proposed or pending value |
|---|---|
| Host and environment | PENDING reference environment. Capture CPU model and cores, RAM, storage, OS and architecture, runtime and dependency versions, CPU/memory limits, deployment topology, component configuration and controlled target network characteristics. |
| Dataset | PROPOSED seed an equivalent 30-day result corpus of about 43.2 million rows, 1,000 active monitors and 10 synthetic workspaces, with a stable seed and documented age and outcome distribution. Use a separate stress corpus approaching 86.4 million results if feasible and report the actual size and any differences. |
| Profile | PROPOSED stagger due times evenly and exercise only controlled local targets with documented success, failure and latency fixtures. Hold candidate and settings constant between comparable runs. |
| API operation mix | PROPOSED 40% overview reads, 30% monitor/history reads, 20% incident list and detail reads and 10% monitor settings writes that preserve active monitor count. Document filtering, pagination, auth state, selection and offered rate. |
| Parallel clients | PROPOSED 20 concurrent authenticated clients in a closed-loop workload with fixed pacing. PENDING precise pacing and rate. |
| Timing | PROPOSED 10-minute warm-up followed by 30 minutes measured in three independently reset baseline and stress runs. Document stop criteria for unsafe resource saturation and incomplete runs. |
| API metrics | Report request count, throughput, p50/p95/p99 elapsed latency for the mixed baseline and each operation group, with timeout and error rate. Document whether failed responses enter latency statistics and disclose their separate latency counts. PENDING acceptable error rate. |
| Scheduling delay | Report due time to actual check start as p50/p95/p99, plus missed opportunities. PENDING acceptance bounds and reporting for unstarted work. |
| Queue backlog | Report initial, peak and final number of pending checks and notifications separately, sampling cadence, oldest work age and recovery time. PENDING acceptable sustained backlog and drain bounds. |
| Coverage | PROPOSED backend line coverage over production application modules and API, scheduler and worker paths. Publish exclusions including generated artifacts and test code, and expose uncovered critical paths. PENDING branch-coverage policy. |
| Retention | With a controlled clock, seed results just newer, exactly at and older than the 30-day boundary. Verify visible query results and eventual expiration separately, measuring actual cleanup lag. PENDING boundary and lag policy under Q-08. |
| Reproduction and results | Publish run identifier, candidate revision, fixture seed, dataset counts, settings, commands, tool versions, timestamps, environment, raw sanitized time series and a summary table per run. Include results versus target, deviations, errors and incomplete evidence. |

[AC-100](acceptance-criteria.md#ac-100) checks reproducibility of the protocol. [AC-087](acceptance-criteria.md#ac-087) and [AC-089](acceptance-criteria.md#ac-089) evaluate actual target attainment using the approved inputs. Unapproved inputs or invalid evidence leave attainment incomplete. No load or coverage measurements have been performed in Product Discovery.

## Proposed additional check semantics

Beta capabilities are approved. Input bounds and edge semantics are **PROPOSED** under Q-09. All checks use identical installation destination and secret policies, reject forbidden destinations prior to connection, and bound target interaction in time and resource use. A platform fault or policy rejection remains separate from target failure.

| Type | Purpose and inputs | Validation | Success | Failure and edge cases |
|---|---|---|---|---|
| TCP | Test whether a service accepts a TCP connection. Host, port and configured deadline. | Valid host or permitted IP literal, integer port 1–65535, valid deadline and eligible destination. | TCP connection established within the deadline. | Refusal is target failure. Time limit on healthy execution is TIMEOUT. No user payload is sent. |
| SSL certificate | Warn before the certificate presented by a TLS endpoint expires. Host, port, deadline and required minimum remaining validity. | Valid host and port, nonnegative lifetime within approved bounds and normal TLS policy. | Valid peer identity and unexpired certificate with remaining lifetime at or above threshold. | Expired at equality with expiry, too little time, or failed TLS identity means failure if attributable to target. Unavailable certificate, clock uncertainty and timeout require distinct diagnostics. |
| HTTP keyword | Check for a literal token in an eligible response. HTTP target, expected status, deadline and a nonempty literal. | Eligible body-bearing request, supported content encoding, bounded literal, bounded decoded body and approved destination. | Accepted status and case-sensitive literal present in decoded body. | False status or missing token fails. Empty body has no match. Oversize, unsupported encoding and timeout follow validated diagnostics. No regex or executable expression is accepted. |
| JSON assertion | Validate an API payload. HTTP target, expected status, deadline, bounded declarative path and expected JSON value or presence rule. | Enforce bounded path, depth, response size and supported operations. Reject executable input. | Accepted status and approved path resolves with matching typed value or required presence. | Missing path, wrong type or mismatched value fails under the proposed semantics. Treating malformed target JSON as a failure is conditional on [Q-09](prd.md#q-09) and verified by [AC-099](acceptance-criteria.md#ac-099) if approved. Distinguish missing from explicit null. Oversize and ambiguous JSON require validated diagnostics. |

## Proposed Beta authorization matrix

**PROPOSED under Q-07.** These are workspace roles only. Installation policy changes are reserved to installation authority. All cells also require membership and scope. Public published status has separate authorized publication rules and anonymous read access.

| Operation | Owner | Admin | Member | Viewer |
|---|---|---|---|---|
| Read workspace operational views | Yes | Yes | Yes | Yes |
| Configure monitors and maintenance | Yes | Yes | Yes | No |
| Run an eligible manual check | Yes | Yes | Yes | No |
| Manage notifications and status page publishing | Yes | Yes | No | No |
| Manage workspace settings and API keys | Yes | Yes | No | No |
| Invite, remove or assign Member and Viewer | Yes | Yes | No | No |
| Assign Admin or change Owner membership | Yes, preserve a last Owner | No | No | No |
| Change installation registration or destination policy | No through role | No through role | No through role | No through role |

## References

- [Product Requirements Document](prd.md)
- [Project Charter](../project/charter.md)
- [Decision Register](../project/decision-register.md)
- [Business Rules](business-rules.md)
- [Acceptance Criteria](acceptance-criteria.md)
- [Requirements Traceability Matrix](requirements-traceability-matrix.md)
- [Glossary](../project/glossary.md)
