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
| <a id="fr-001"></a> FR-001 | Bootstrap first account | The installation MUST provide an operator-authorized path to establish the first account while public registration is disabled. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001) | Controlled integration test | [AC-001](acceptance-criteria.md#ac-001) | DERIVED DRAFT |
| <a id="fr-002"></a> FR-002 | Close bootstrap | The installation MUST prevent unauthorized bootstrap and reuse after initial setup. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001) | Controlled integration test | [AC-002](acceptance-criteria.md#ac-002) | DERIVED DRAFT |
| <a id="fr-003"></a> FR-003 | Default registration policy | The installation MUST disable public registration by default after initial setup. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001) | Controlled integration test | [AC-003](acceptance-criteria.md#ac-003) | DERIVED DRAFT |
| <a id="fr-004"></a> FR-004 | Operator registration control | The installation MUST enforce the operator's current public registration setting. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [PD-001](../project/decision-register.md#pd-001) | Controlled integration test | [AC-004](acceptance-criteria.md#ac-004) | DERIVED DRAFT |
| <a id="fr-005"></a> FR-005 | Sign in | The product MUST establish an authenticated session for valid account credentials and reject invalid credentials. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-005](acceptance-criteria.md#ac-005) | DERIVED DRAFT |
| <a id="fr-006"></a> FR-006 | Refresh session | The product MUST renew an eligible session using its valid refresh credential. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-006](acceptance-criteria.md#ac-006) | DERIVED DRAFT |
| <a id="fr-007"></a> FR-007 | Sign out | The product MUST end the active session on sign-out and prevent its further renewal. | v0.1.0 MVP | Must | [F-001](prd.md#f-001), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-007](acceptance-criteria.md#ac-007) | DERIVED DRAFT |
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
| <a id="fr-051"></a> FR-051 | Manage workspace membership | An authorized actor MUST be able to manage memberships within their own workspace. | v0.5.0 Beta | Must | [F-032](prd.md#f-032), [PD-007](../project/decision-register.md#pd-007) | Security verification with controlled fixtures | [AC-066](acceptance-criteria.md#ac-066) | DERIVED DRAFT |


## Monitor management and check execution

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-011"></a> FR-011 | Create monitor | The Owner MUST be able to create a valid monitor and see its configuration in their workspace. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-012](acceptance-criteria.md#ac-012) | DERIVED DRAFT |
| <a id="fr-012"></a> FR-012 | Read monitor | The Owner MUST be able to list and inspect their workspace monitors. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-013](acceptance-criteria.md#ac-013) | DERIVED DRAFT |
| <a id="fr-013"></a> FR-013 | Edit monitor | The Owner MUST be able to save a valid configuration change to their monitor. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-014](acceptance-criteria.md#ac-014) | DERIVED DRAFT |
| <a id="fr-014"></a> FR-014 | Delete monitor | The Owner MUST be able to delete a monitor and thereby stop new executions for it. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-015](acceptance-criteria.md#ac-015) | DERIVED DRAFT |
| <a id="fr-015"></a> FR-015 | Pause and resume | The Owner MUST be able to suspend and resume recurring checks without creating observations for the suspended period. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [F-005](prd.md#f-005), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-016](acceptance-criteria.md#ac-016) | DERIVED DRAFT |
| <a id="fr-016"></a> FR-016 | HTTP methods | HTTP monitors MUST support GET and HEAD and reject other methods and arbitrary request bodies. | v0.1.0 MVP | Must | [F-004](prd.md#f-004), [PD-002](../project/decision-register.md#pd-002) | Controlled integration test | [AC-017](acceptance-criteria.md#ac-017) | DERIVED DRAFT |
| <a id="fr-017"></a> FR-017 | HTTP success condition | The product MUST evaluate an HTTP response against the monitor's expected status condition. | v0.1.0 MVP | Must | [F-004](prd.md#f-004), [PD-002](../project/decision-register.md#pd-002) | Controlled integration test | [AC-018](acceptance-criteria.md#ac-018) | DERIVED DRAFT |
| <a id="fr-018"></a> FR-018 | HTTP defaults | New HTTP monitors SHOULD default to GET, a 10-second timeout, accepted statuses 200–299, redirects disabled and TLS verification enabled. | v0.1.0 MVP | Should | [F-004](prd.md#f-004), [PD-002](../project/decision-register.md#pd-002) | Controlled integration test | [AC-019](acceptance-criteria.md#ac-019) | PROPOSED · [Q-02](prd.md#q-02) |
| <a id="fr-019"></a> FR-019 | Timeout classification | A check that reaches its configured target request deadline MUST yield a target timeout when execution was healthy up to that deadline. | v0.1.0 MVP | Must | [F-004](prd.md#f-004), [PD-003](../project/decision-register.md#pd-003), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-020](acceptance-criteria.md#ac-020) | DERIVED DRAFT |
| <a id="fr-020"></a> FR-020 | Minimum interval | The product MUST reject monitoring intervals below 30 seconds and allow a 30-second configuration. | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [PD-003](../project/decision-register.md#pd-003) | Controlled integration test | [AC-021](acceptance-criteria.md#ac-021) | DERIVED DRAFT |
| <a id="fr-021"></a> FR-021 | Interval defaults and range | The interval SHOULD default to 60 seconds and allow integer-second values through 24 hours inclusive. | v0.1.0 MVP | Should | [F-005](prd.md#f-005), [PD-003](../project/decision-register.md#pd-003) | Controlled integration test | [AC-022](acceptance-criteria.md#ac-022) | PROPOSED · [Q-02](prd.md#q-02) |
| <a id="fr-022"></a> FR-022 | Recurring execution | Active monitors MUST receive recurring background checks according to their configured interval, subject to visible execution delays and failures. | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-023](acceptance-criteria.md#ac-023) | DERIVED DRAFT |
| <a id="fr-023"></a> FR-023 | Request immediate check | The product MUST let an authorized user request an asynchronous Run Check Now execution and inspect its progress and outcome. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [PD-005](../project/decision-register.md#pd-005) | Controlled integration test | [AC-027](acceptance-criteria.md#ac-027) | DERIVED DRAFT |
| <a id="fr-024"></a> FR-024 | Persist manual result | The product MUST save completed manual check results in the monitor history with their manual origin. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [F-007](prd.md#f-007), [PD-005](../project/decision-register.md#pd-005) | Controlled integration test | [AC-028](acceptance-criteria.md#ac-028) | DERIVED DRAFT |
| <a id="fr-025"></a> FR-025 | Authorize manual execution | The product MUST authorize manual execution against the monitor's workspace before accepting work. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [PD-005](../project/decision-register.md#pd-005), [PD-007](../project/decision-register.md#pd-007) | Controlled integration test | [AC-029](acceptance-criteria.md#ac-029) | DERIVED DRAFT |
| <a id="fr-026"></a> FR-026 | Prevent overlapping execution | The product MUST prevent duplicate effective executions when concurrent manual requests or a manual and scheduled opportunity collide. | v0.1.0 MVP | Must | [F-029](prd.md#f-029), [F-005](prd.md#f-005), [PD-005](../project/decision-register.md#pd-005) | Controlled integration test | [AC-031](acceptance-criteria.md#ac-031) | DERIVED DRAFT |
| <a id="fr-027"></a> FR-027 | Manual check on paused monitor | The product SHOULD reject manual execution on a paused monitor and explain how to resume. | v0.1.0 MVP | Should | [F-029](prd.md#f-029), [F-003](prd.md#f-003), [PD-005](../project/decision-register.md#pd-005) | Controlled integration test | [AC-032](acceptance-criteria.md#ac-032) | PROPOSED · [Q-03](prd.md#q-03) |
| <a id="fr-028"></a> FR-028 | Manual observation effects | Manual execution SHOULD preserve scheduled cadence and remain outside scheduled availability, latency and incident calculations. | v0.1.0 MVP | Should | [F-029](prd.md#f-029), [F-005](prd.md#f-005), [F-008](prd.md#f-008), [F-033](prd.md#f-033), [PD-005](../project/decision-register.md#pd-005), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-033](acceptance-criteria.md#ac-033) | PROPOSED · [Q-03](prd.md#q-03) |
| <a id="fr-029"></a> FR-029 | Collision disposition | A manual request SHOULD point the Owner to any already accepted execution. A due scheduled opportunity overlapping a manual execution SHOULD remain a skipped opportunity. | v0.1.0 MVP | Should | [F-029](prd.md#f-029), [F-005](prd.md#f-005), [PD-005](../project/decision-register.md#pd-005) | Controlled integration test | [AC-034](acceptance-criteria.md#ac-034) | PROPOSED · [Q-03](prd.md#q-03) |
| <a id="fr-043"></a> FR-043 | TCP check | An authorized workspace user MUST be able to verify connection establishment to a configured host and valid TCP port under installation policy. | v0.5.0 Beta | Must | [F-013](prd.md#f-013), [PD-009](../project/decision-register.md#pd-009) | Controlled integration test | [AC-058](acceptance-criteria.md#ac-058) | DERIVED DRAFT |
| <a id="fr-044"></a> FR-044 | Certificate check | An authorized workspace user MUST be able to check the TLS certificate expiry of a configured host and port against a validated expiry threshold. | v0.5.0 Beta | Must | [F-014](prd.md#f-014), [PD-009](../project/decision-register.md#pd-009) | Controlled-clock test | [AC-059](acceptance-criteria.md#ac-059) | DERIVED DRAFT · [Q-09](prd.md#q-09) |
| <a id="fr-045"></a> FR-045 | Certificate boundary policy | The certificate check SHOULD succeed at or above a nonnegative minimum remaining lifetime while a certificate at or past its expiry instant SHOULD fail. | v0.5.0 Beta | Should | [F-014](prd.md#f-014), [PD-009](../project/decision-register.md#pd-009) | Controlled-clock test | [AC-060](acceptance-criteria.md#ac-060) | PROPOSED · [Q-09](prd.md#q-09) |
| <a id="fr-059"></a> FR-059 | HTTP keyword check | An authorized workspace user MUST be able to require a literal keyword in an eligible HTTP response body. | v0.5.0 Beta | Must | [F-030](prd.md#f-030), [PD-009](../project/decision-register.md#pd-009) | Controlled integration test | [AC-080](acceptance-criteria.md#ac-080) | DERIVED DRAFT |
| <a id="fr-060"></a> FR-060 | JSON assertion check | An authorized workspace user MUST be able to verify a bounded declarative assertion against an eligible JSON response. | v0.5.0 Beta | Must | [F-031](prd.md#f-031), [PD-009](../project/decision-register.md#pd-009) | Controlled integration test | [AC-081](acceptance-criteria.md#ac-081) | DERIVED DRAFT |


## History and incidents

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-030"></a> FR-030 | Inspect check history | The Owner MUST be able to inspect authorized check outcomes, times, origin and diagnostic class, including empty history. | v0.1.0 MVP | Must | [F-007](prd.md#f-007), [D-005](../project/decision-register.md#d-005), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-035](acceptance-criteria.md#ac-035) | DERIVED DRAFT |
| <a id="fr-031"></a> FR-031 | Configure thresholds | The Owner MUST be able to configure both incident thresholds, whose defaults are three failures and two successes. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-037](acceptance-criteria.md#ac-037) | DERIVED DRAFT |
| <a id="fr-032"></a> FR-032 | Open at failure threshold | The product MUST open an incident upon reaching the configured consecutive qualifying failure threshold. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-038](acceptance-criteria.md#ac-038) | DERIVED DRAFT |
| <a id="fr-033"></a> FR-033 | Recover at success threshold | The product MUST close the active incident upon reaching the configured consecutive qualifying success threshold. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-039](acceptance-criteria.md#ac-039) | DERIVED DRAFT |
| <a id="fr-034"></a> FR-034 | Inspect incidents | The Owner MUST be able to list and inspect incidents with their current disposition and available time evidence. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-040](acceptance-criteria.md#ac-040) | DERIVED DRAFT |
| <a id="fr-035"></a> FR-035 | Exclude platform faults | The product MUST classify an internal or policy-blocked execution distinctly from a qualifying target failure. | v0.1.0 MVP | Must | [F-008](prd.md#f-008), [F-007](prd.md#f-007), [PD-004](../project/decision-register.md#pd-004), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-041](acceptance-criteria.md#ac-041) | DERIVED DRAFT |
| <a id="fr-036"></a> FR-036 | State and streak transitions | The state and counter rules SHOULD follow the proposed transition table, including streak isolation across lifecycle and configuration changes. | v0.1.0 MVP | Should | [F-008](prd.md#f-008), [F-003](prd.md#f-003), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-042](acceptance-criteria.md#ac-042) | PROPOSED · [Q-04](prd.md#q-04) |
| <a id="fr-037"></a> FR-037 | Late observations | The product SHOULD retain eligible late results while excluding superseded or out-of-order observations from live state transitions. | v0.1.0 MVP | Should | [F-008](prd.md#f-008), [F-007](prd.md#f-007), [PD-004](../project/decision-register.md#pd-004), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-043](acceptance-criteria.md#ac-043) | PROPOSED · [Q-04](prd.md#q-04) |


## External Integration Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-038"></a> FR-038 | Configure Telegram | The Owner MUST be able to configure and disable Telegram delivery for their workspace with protected destination credentials. | v0.1.0 MVP | Must | [F-009](prd.md#f-009), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-044](acceptance-criteria.md#ac-044) | DERIVED DRAFT |
| <a id="fr-039"></a> FR-039 | Notify on incident transitions | Configured Telegram delivery SHOULD notify on incident opening and confirmed recovery by default. | v0.1.0 MVP | Should | [F-009](prd.md#f-009), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-045](acceptance-criteria.md#ac-045) | PROPOSED · [Q-05](prd.md#q-05) |
| <a id="fr-046"></a> FR-046 | Email notifications | The product MUST let an authorized user configure email notifications for incident transitions. | v0.5.0 Beta | Must | [F-015](prd.md#f-015), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-061](acceptance-criteria.md#ac-061) | DERIVED DRAFT |
| <a id="fr-047"></a> FR-047 | Webhook notifications | The product MUST let an authorized user configure a policy-eligible webhook for incident transitions. | v0.5.0 Beta | Must | [F-016](prd.md#f-016), [D-005](../project/decision-register.md#d-005), [PD-006](../project/decision-register.md#pd-006) | Controlled integration test | [AC-062](acceptance-criteria.md#ac-062) | DERIVED DRAFT |


## User Interface Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-040"></a> FR-040 | Dashboard summary | The Owner MUST be able to inspect workspace monitor states, recent observations and incidents and navigate to their details. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-047](acceptance-criteria.md#ac-047) | DERIVED DRAFT |
| <a id="fr-041"></a> FR-041 | Polling and stale data | MVP views with changing operational data MUST refresh through polling and visibly distinguish initial loading, stale retained data and update failures. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [PD-008](../project/decision-register.md#pd-008) | Controlled integration test | [AC-048](acceptance-criteria.md#ac-048) | DERIVED DRAFT |
| <a id="fr-042"></a> FR-042 | Beta live updates | Beta MUST deliver live operational updates through Server-Sent Events and reconcile displayed authorized data after reconnecting. | v0.5.0 Beta | Must | [F-010](prd.md#f-010), [F-018](prd.md#f-018), [PD-008](../project/decision-register.md#pd-008) | Controlled integration test | [AC-049](acceptance-criteria.md#ac-049) | DERIVED DRAFT |
| <a id="nfr-027"></a> NFR-027 | Dark-only presentation | All product views MUST use the dark theme across release scopes and host theme preferences. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [PD-013](../project/decision-register.md#pd-013) | Browser walkthrough and inspection | [AC-091](acceptance-criteria.md#ac-091) | DERIVED DRAFT |
| <a id="nfr-029"></a> NFR-029 | Desktop-first responsive interface | The web interface MUST preserve the principal navigation, dashboard, monitor management, incident and account settings journeys on mobile viewports. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [F-008](prd.md#f-008), [F-010](prd.md#f-010), [F-001](prd.md#f-001), [PD-014](../project/decision-register.md#pd-014) | Browser walkthrough and inspection | [AC-093](acceptance-criteria.md#ac-093) | DERIVED DRAFT · [Q-14](prd.md#q-14) |
| <a id="nfr-030"></a> NFR-030 | English product surfaces | UI text, technical messages, repository documentation and source identifiers and comments MUST be in English. | v0.1.0 MVP | Must | [F-010](prd.md#f-010), [PD-015](../project/decision-register.md#pd-015), [D-006](../project/decision-register.md#d-006) | Browser walkthrough and inspection | [AC-094](acceptance-criteria.md#ac-094) | DERIVED DRAFT |


## Analytics and publishing

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-052"></a> FR-052 | Extended analytics | Beta MUST let authorized users compare availability and successful check latency across supported windows and eligible monitors. | v0.5.0 Beta | Must | [F-018](prd.md#f-018), [F-033](prd.md#f-033), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-067](acceptance-criteria.md#ac-067) | DERIVED DRAFT · [Q-06](prd.md#q-06) |
| <a id="fr-053"></a> FR-053 | Publish status page | An authorized user MUST be able to publish a public status view restricted to intentionally selected monitors. | v0.5.0 Beta | Must | [F-019](prd.md#f-019), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-068](acceptance-criteria.md#ac-068) | DERIVED DRAFT |
| <a id="fr-054"></a> FR-054 | Schedule maintenance | An authorized user MUST be able to schedule and inspect a maintenance window for authorized monitors. | v0.5.0 Beta | Must | [F-020](prd.md#f-020), [D-005](../project/decision-register.md#d-005) | Controlled-clock test | [AC-069](acceptance-criteria.md#ac-069) | DERIVED DRAFT · [Q-15](prd.md#q-15) |
| <a id="fr-055"></a> FR-055 | Manage API keys | Beta MUST let an authorized user create and revoke workspace-scoped API keys. | v0.5.0 Beta | Must | [F-021](prd.md#f-021), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-070](acceptance-criteria.md#ac-070) | DERIVED DRAFT |
| <a id="fr-056"></a> FR-056 | Inspect audit log | An authorized user MUST be able to inspect an audit trail of defined workspace actions. | v1.0.0 Release | Must | [F-022](prd.md#f-022), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-071](acceptance-criteria.md#ac-071) | DERIVED DRAFT · [Q-15](prd.md#q-15) |
| <a id="fr-057"></a> FR-057 | Export reports | An authorized user MUST be able to export an authorized monitoring report within the supported selection. | v1.0.0 Release | Must | [F-024](prd.md#f-024), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-073](acceptance-criteria.md#ac-073) | DERIVED DRAFT |
| <a id="fr-061"></a> FR-061 | Calculate uptime | The product MUST show per-monitor uptime as qualifying successes divided by all qualifying completed observations, expressed as a percentage over the selected window. | v0.1.0 MVP | Must | [F-033](prd.md#f-033), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-083](acceptance-criteria.md#ac-083) | DERIVED DRAFT |
| <a id="fr-062"></a> FR-062 | Calculate successful latency | The product MUST use only qualifying successful checks when calculating average latency and supported latency percentiles. | v0.1.0 MVP | Must | [F-033](prd.md#f-033), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-084](acceptance-criteria.md#ac-084) | DERIVED DRAFT |
| <a id="fr-063"></a> FR-063 | Show incomplete observations | The product MUST distinguish empty samples, excluded observations, pauses and missing observations from measured availability. | v0.1.0 MVP | Must | [F-033](prd.md#f-033), [F-010](prd.md#f-010), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-085](acceptance-criteria.md#ac-085) | DERIVED DRAFT |
| <a id="fr-064"></a> FR-064 | Metric calculation conventions | The product SHOULD apply the proposed time boundaries, rounding, sample minimums, percentile and aggregation rules in the metric conventions. | v0.1.0 MVP | Should | [F-033](prd.md#f-033), [F-018](prd.md#f-018), [PD-011](../project/decision-register.md#pd-011) | Controlled-clock test | [AC-086](acceptance-criteria.md#ac-086) | PROPOSED · [Q-06](prd.md#q-06) |


## Interactive demo

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="fr-058"></a> FR-058 | Interactive demo journey | Public demo visitors MUST be able to exercise approved monitor and incident journeys against controlled synthetic targets. | v1.0.0 Release | Must | [F-025](prd.md#f-025), [PD-010](../project/decision-register.md#pd-010) | Security verification with controlled fixtures | [AC-074](acceptance-criteria.md#ac-074) | DERIVED DRAFT |
| <a id="nfr-017"></a> NFR-017 | Demo network containment | Demo sessions MUST be restricted to controlled synthetic destinations and deny arbitrary scanning and notifications to external recipients. | v1.0.0 Release | Must | [F-025](prd.md#f-025), [F-027](prd.md#f-027), [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006), [PD-010](../project/decision-register.md#pd-010) | Security verification with controlled fixtures | [AC-075](acceptance-criteria.md#ac-075) | DERIVED DRAFT |
| <a id="nfr-018"></a> NFR-018 | Public deployment isolation | The public demo MUST isolate real deployments and data and prevent visitor sessions from reading or mutating each other's mutable data. | v1.0.0 Release | Must | [F-027](prd.md#f-027), [PD-010](../project/decision-register.md#pd-010) | Security verification with controlled fixtures | [AC-076](acceptance-criteria.md#ac-076) | DERIVED DRAFT |
| <a id="nfr-019"></a> NFR-019 | Demo resource and data lifecycle | The public demo MUST enforce finite resource limits and remove visitor-created data per its validated reset and cleanup policy. | v1.0.0 Release | Must | [F-027](prd.md#f-027), [PD-010](../project/decision-register.md#pd-010) | Security verification with controlled fixtures | [AC-077](acceptance-criteria.md#ac-077) | DERIVED DRAFT · [Q-13](prd.md#q-13) |


## Non-functional Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-013"></a> NFR-013 | Local operation | The project MUST support documented self-hosted startup using one Docker Compose command after documented prerequisites and configuration. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [D-004](../project/decision-register.md#d-004), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-055](acceptance-criteria.md#ac-055) | DERIVED DRAFT |
| <a id="nfr-014"></a> NFR-014 | Migration readiness | The supported setup and upgrade procedure MUST apply required data migrations while preserving supported existing data. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-056](acceptance-criteria.md#ac-056) | DERIVED DRAFT |
| <a id="nfr-015"></a> NFR-015 | CI assurance | Repository CI MUST report the outcome of required project checks for each eligible change. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-057](acceptance-criteria.md#ac-057) | DERIVED DRAFT |
| <a id="nfr-020"></a> NFR-020 | Release integration and load evidence | The project MUST record integration and load verification results for the release under the documented repeatable profiles. | v1.0.0 Release | Must | [F-026](prd.md#f-026), [D-005](../project/decision-register.md#d-005), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-078](acceptance-criteria.md#ac-078) | DERIVED DRAFT |
| <a id="nfr-021"></a> NFR-021 | Release documentation | The release MUST provide English installation, operation, usage and safe demo documentation for supported features. | v1.0.0 Release | Must | [F-028](prd.md#f-028), [D-005](../project/decision-register.md#d-005), [PD-015](../project/decision-register.md#pd-015) | Measurement and evidence review | [AC-079](acceptance-criteria.md#ac-079) | DERIVED DRAFT |
| <a id="nfr-025"></a> NFR-025 | Backend test coverage | Backend test coverage MUST reach at least 80% using the approved measurement scope and metric. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-089](acceptance-criteria.md#ac-089) | DERIVED DRAFT · [Q-11](prd.md#q-11) |


## Security Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-005"></a> NFR-005 | Manual rate limit | The product MUST enforce a finite rate limit on manual requests and surface rejected requests without starting work. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [F-029](prd.md#f-029), [PD-005](../project/decision-register.md#pd-005) | Security verification with controlled fixtures | [AC-030](acceptance-criteria.md#ac-030) | DERIVED DRAFT · [Q-03](prd.md#q-03) |
| <a id="nfr-008"></a> NFR-008 | URL and protocol validation | The product MUST reject invalid target URL syntax, embedded credentials and unsupported scheme or port configuration before connection. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006) | Security verification with controlled fixtures | [AC-050](acceptance-criteria.md#ac-050) | DERIVED DRAFT |
| <a id="nfr-009"></a> NFR-009 | Restricted destination policy | The installation MUST allow eligible public destinations, deny private IPv4 and IPv6 by default and allow only explicitly selected eligible internal destinations through operator policy. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006) | Security verification with controlled fixtures | [AC-051](acceptance-criteria.md#ac-051) | DERIVED DRAFT · [Q-10](prd.md#q-10) |
| <a id="nfr-010"></a> NFR-010 | Resolve and validate every connection | Every actual outbound target connection MUST use a destination validated against current policy, including direct IPs, DNS answers, DNS changes and each redirect hop. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006) | Security verification with controlled fixtures | [AC-052](acceptance-criteria.md#ac-052) | DERIVED DRAFT |
| <a id="nfr-011"></a> NFR-011 | Protect confidential values | The platform MUST protect credentials and secrets from unauthorized views, diagnostics and unapproved outbound disclosure. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [PD-006](../project/decision-register.md#pd-006), [PD-015](../project/decision-register.md#pd-015) | Security verification with controlled fixtures | [AC-053](acceptance-criteria.md#ac-053) | DERIVED DRAFT |
| <a id="nfr-012"></a> NFR-012 | Rate limiting | The installation MUST limit abusive eligible product requests and preserve service for ordinary authorized traffic. | v0.1.0 MVP | Must | [F-011](prd.md#f-011), [D-005](../project/decision-register.md#d-005) | Security verification with controlled fixtures | [AC-054](acceptance-criteria.md#ac-054) | DERIVED DRAFT · [Q-10](prd.md#q-10) |
| <a id="nfr-022"></a> NFR-022 | Beta check safety | Additional monitor types MUST use the installation destination policy and bounded target interaction, including response inspection where applicable. | v0.5.0 Beta | Must | [F-011](prd.md#f-011), [F-013](prd.md#f-013), [F-014](prd.md#f-014), [F-030](prd.md#f-030), [F-031](prd.md#f-031), [PD-006](../project/decision-register.md#pd-006), [PD-009](../project/decision-register.md#pd-009) | Security verification with controlled fixtures | [AC-082](acceptance-criteria.md#ac-082) | DERIVED DRAFT · [Q-09](prd.md#q-09) |


## Data and Retention Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-006"></a> NFR-006 | History retention | Check results MUST remain available within the 30-day retention target, subject to authorized data removal, and expire according to the approved retention rule. | v0.1.0 MVP | Must | [F-007](prd.md#f-007), [PD-012](../project/decision-register.md#pd-012) | Controlled-clock test | [AC-036](acceptance-criteria.md#ac-036) | DERIVED DRAFT · [Q-08](prd.md#q-08) |


## Error Handling Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-007"></a> NFR-007 | Notification failure isolation | Delivery failure MUST be visible as a notification outcome independent of the incident state, with bounded reattempts for eligible transient failures. | v0.1.0 MVP | Must | [F-009](prd.md#f-009), [F-006](prd.md#f-006), [D-005](../project/decision-register.md#d-005) | Controlled integration test | [AC-046](acceptance-criteria.md#ac-046) | DERIVED DRAFT · [Q-05](prd.md#q-05) |
| <a id="nfr-031"></a> NFR-031 | Actionable errors | Product errors MUST identify the failed action or affected field in English and preserve previously confirmed data. | v0.1.0 MVP | Must | [F-003](prd.md#f-003), [F-004](prd.md#f-004), [F-010](prd.md#f-010), [PD-008](../project/decision-register.md#pd-008) | Controlled integration test | [AC-095](acceptance-criteria.md#ac-095) | DERIVED DRAFT |


## Reliability Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-002"></a> NFR-002 | Background execution | Scheduled checks and notification work MUST run in the approved background task system while interactive views remain usable. | v0.1.0 MVP | Must | [F-006](prd.md#f-006), [D-003](../project/decision-register.md#d-003), [D-004](../project/decision-register.md#d-004) | Controlled integration test | [AC-024](acceptance-criteria.md#ac-024) | DERIVED DRAFT |
| <a id="nfr-003"></a> NFR-003 | Worker interruption | The product MUST distinguish delayed, missed or internally failed work during worker unavailability from an observed service failure. | v0.1.0 MVP | Must | [F-006](prd.md#f-006), [F-007](prd.md#f-007), [D-005](../project/decision-register.md#d-005), [PD-011](../project/decision-register.md#pd-011) | Controlled integration test | [AC-025](acceptance-criteria.md#ac-025) | DERIVED DRAFT |
| <a id="nfr-004"></a> NFR-004 | Application idempotency | Repeated processing of one logical execution MUST preserve a single effective result and transition, with no repeated transition notification caused by that replay. | v0.1.0 MVP | Must | [F-006](prd.md#f-006), [F-008](prd.md#f-008), [F-009](prd.md#f-009), [PD-004](../project/decision-register.md#pd-004) | Controlled integration test | [AC-026](acceptance-criteria.md#ac-026) | DERIVED DRAFT |


## Performance Requirements

| ID | Title | Requirement | Release | Priority | Source | Verification | Criterion | Status |
|---|---|---|---|---|---|---|---|---|
| <a id="nfr-023"></a> NFR-023 | Baseline performance target | The platform MUST be evaluated against 1,000 active monitors at 60-second intervals and API p95 at most 200 ms under the approved workload. | v0.1.0 MVP | Must | [F-005](prd.md#f-005), [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-087](acceptance-criteria.md#ac-087) | DERIVED DRAFT · [Q-11](prd.md#q-11) |
| <a id="nfr-024"></a> NFR-024 | Stress characterization | The performance report MUST characterize the 30-second stress profile as capacity evidence. | v0.1.0 MVP | Must | [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-088](acceptance-criteria.md#ac-088) | DERIVED DRAFT |
| <a id="nfr-026"></a> NFR-026 | Proposed workload protocol | Performance measurement SHOULD follow the proposed warm-up, operation mix, client count, duration and outcome reporting profile. | v0.1.0 MVP | Should | [F-012](prd.md#f-012), [PD-012](../project/decision-register.md#pd-012) | Measurement and evidence review | [AC-090](acceptance-criteria.md#ac-090) | PROPOSED · [Q-11](prd.md#q-11) |


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

The [open questions](prd.md#open-questions) are the authoritative validation agenda. Each requirement that depends directly on an unsettled input links to its question. A draft criterion can establish the expected evidence before approving its parameter values.

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

No load or coverage measurements have been performed in Product Discovery.

## Proposed additional check semantics

Beta capabilities are approved. Input bounds and edge semantics are **PROPOSED** under Q-09. All checks use identical installation destination and secret policies, reject forbidden destinations prior to connection, and bound target interaction in time and resource use. A platform fault or policy rejection remains separate from target failure.

| Type | Purpose and inputs | Validation | Success | Failure and edge cases |
|---|---|---|---|---|
| TCP | Test whether a service accepts a TCP connection. Host, port and configured deadline. | Valid host or permitted IP literal, integer port 1–65535, valid deadline and eligible destination. | TCP connection established within the deadline. | Refusal is target failure. Time limit on healthy execution is TIMEOUT. No user payload is sent. |
| SSL certificate | Warn before the certificate presented by a TLS endpoint expires. Host, port, deadline and required minimum remaining validity. | Valid host and port, nonnegative lifetime within approved bounds and normal TLS policy. | Valid peer identity and unexpired certificate with remaining lifetime at or above threshold. | Expired at equality with expiry, too little time, or failed TLS identity means failure if attributable to target. Unavailable certificate, clock uncertainty and timeout require distinct diagnostics. |
| HTTP keyword | Check for a literal token in an eligible response. HTTP target, expected status, deadline and a nonempty literal. | Eligible body-bearing request, supported content encoding, bounded literal, bounded decoded body and approved destination. | Accepted status and case-sensitive literal present in decoded body. | False status or missing token fails. Empty body has no match. Oversize, unsupported encoding and timeout follow validated diagnostics. No regex or executable expression is accepted. |
| JSON assertion | Validate an API payload. HTTP target, expected status, deadline, bounded declarative path and expected JSON value or presence rule. | Enforce bounded path, depth, response size and supported operations. Reject executable input. | Accepted status and approved path resolves with matching typed value or required presence. | Missing path, wrong type, mismatched value or malformed target JSON fails. Distinguish missing from explicit null. Oversize and ambiguous JSON require validated diagnostics. |

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
