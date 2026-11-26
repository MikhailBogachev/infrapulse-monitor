# InfraPulse Product Requirements Document

| Field | Value |
|---|---|
| Document Status | READY FOR OWNER APPROVAL |
| Version | 0.2 |
| Responsible Role | Product Analyst |
| Related Project Stage | Stage 01 — Product Discovery |
| Project Task | IP-004 |
| Validation | IP-004, final owner acceptance pending |

## Executive Summary

InfraPulse is an intended MIT-licensed, self-hosted infrastructure and API availability monitor with a full web interface. It records recurring observations, detects incidents and recoveries, and sends notifications. The software is in Product Discovery.

## Product Vision

Give small engineering teams an independently operated view of service health from one console. Demonstrate production-oriented Python backend engineering with a complete monitoring workflow.

## Problem Statement

Teams need a reliable record of intermittent failures and recovery across services without manually checking endpoints or depending on hosted monitoring. Without a shared timeline, responders cannot easily distinguish a transient check failure, a persistent outage and missing monitoring evidence.

## Target Audience

Backend Developers, DevOps Engineers, Independent Developers and Small Engineering Teams. The [personas](user-personas.md) are assumptions to validate in IP-004.

## User Needs

- Know which targets were checked, when they were checked and what evidence supports their reported state.
- Detect sustained failures, confirm recovery and notify the expected recipients.
- Investigate latency and availability without misreading collection gaps as outages or success.
- Operate a self-hosted instance with scoped access and controllable target policy.

## Value Proposition

One self-hosted web application provides monitoring setup, background checks, workspace-scoped history, investigation and notifications. An installation can operate without mandatory hosted monitoring services. Optional notification integrations depend on the selected providers.

## Product Goals

Deliver a usable monitoring-to-recovery journey in MVP, extend monitoring and collaboration in Beta, and publish evidence, operational documentation and a safe interactive demo for v1.0.0.

## Non-goals

**OUT OF SCOPE.** Kubernetes, distributed monitoring agents, microservices, billing, AI features, native mobile apps, full server metrics, arbitrary scripts or executable expressions, DNS/ICMP/heartbeat monitoring, localization and multilingual UI. The UI supports Dark Only. MVP excludes arbitrary HTTP request bodies and methods other than GET and HEAD.

## Approved Product Decisions

The [Decision Register](../project/decision-register.md#approved-product-decisions) defines PD-001 through PD-016. Q-01–Q-15 finalize the approved Stage 01 parameters. [PD-016](../project/decision-register.md#pd-016) refines monitor lifecycle behavior for a paused URL edit and was approved in IP-005 Final Acceptance. The [matrix](requirements-traceability-matrix.md) maps decisions to features and verification.

## Feature Catalog

| Feature | Title | Release | Scope source | Outcome |
|---|---|---|---|---|
| <a id="f-001"></a> F-001 | Authentication (JWT and refresh tokens) | v0.1.0 MVP | [D-005](../project/decision-register.md#d-005), [PD-001](../project/decision-register.md#pd-001), [PD-014](../project/decision-register.md#pd-014) | Bootstrap, controlled signup, sign in, renew sessions and sign out. |
| <a id="f-002"></a> F-002 | Workspace isolation | v0.1.0 MVP | [D-005](../project/decision-register.md#d-005), [PD-006](../project/decision-register.md#pd-006), [PD-007](../project/decision-register.md#pd-007) | Operate within authorized workspace resources and settings. |
| <a id="f-003"></a> F-003 | Monitor CRUD | v0.1.0 MVP | [D-005](../project/decision-register.md#d-005), [PD-014](../project/decision-register.md#pd-014) | Create, inspect, edit, delete, pause and resume monitors. |
| <a id="f-004"></a> F-004 | HTTP/HTTPS checks | v0.1.0 MVP | [D-005](../project/decision-register.md#d-005), [PD-002](../project/decision-register.md#pd-002), [PD-006](../project/decision-register.md#pd-006) | Check HTTP targets using approved methods and status conditions. |
| <a id="f-005"></a> F-005 | Scheduler | v0.1.0 MVP | [D-005](../project/decision-register.md#d-005), [PD-003](../project/decision-register.md#pd-003), [PD-012](../project/decision-register.md#pd-012) | Run recurring checks at configured intervals. |
| <a id="f-006"></a> F-006 | RabbitMQ/Celery tasks | v0.1.0 MVP | [D-003](../project/decision-register.md#d-003), [D-004](../project/decision-register.md#d-004), [D-005](../project/decision-register.md#d-005) | Operate the approved background task system. |
| <a id="f-007"></a> F-007 | Check history | v0.1.0 MVP | [D-005](../project/decision-register.md#d-005), [PD-005](../project/decision-register.md#pd-005), [PD-011](../project/decision-register.md#pd-011), [PD-012](../project/decision-register.md#pd-012) | Inspect historical observations and recognized gaps. |
| <a id="f-008"></a> F-008 | Incidents | v0.1.0 MVP | [D-005](../project/decision-register.md#d-005), [PD-004](../project/decision-register.md#pd-004), [PD-005](../project/decision-register.md#pd-005), [PD-014](../project/decision-register.md#pd-014) | Detect, inspect and recover incidents using qualifying observations. |
| <a id="f-009"></a> F-009 | Telegram notifications | v0.1.0 MVP | [D-005](../project/decision-register.md#d-005), [PD-004](../project/decision-register.md#pd-004) | Set up Telegram and receive incident transition notifications. |
| <a id="f-010"></a> F-010 | Dashboard | v0.1.0 MVP | [D-005](../project/decision-register.md#d-005), [PD-008](../project/decision-register.md#pd-008), [PD-013](../project/decision-register.md#pd-013), [PD-014](../project/decision-register.md#pd-014), [PD-015](../project/decision-register.md#pd-015) | Inspect current status and navigate to workspace operational details. |
| <a id="f-011"></a> F-011 | SSRF protection and rate limiting | v0.1.0 MVP | [D-005](../project/decision-register.md#d-005), [PD-005](../project/decision-register.md#pd-005), [PD-006](../project/decision-register.md#pd-006), [PD-009](../project/decision-register.md#pd-009) | Restrict destinations, protect credentials and bound abusive requests. |
| <a id="f-012"></a> F-012 | Docker Compose, migrations and GitHub Actions CI | v0.1.0 MVP | [D-004](../project/decision-register.md#d-004), [D-005](../project/decision-register.md#d-005), [PD-012](../project/decision-register.md#pd-012), [D-010](../project/decision-register.md#d-010) | Start and upgrade a self-hosted environment and verify eligible changes through the required GitHub Actions checks. |
| <a id="f-013"></a> F-013 | TCP checks | v0.5.0 Beta | [D-005](../project/decision-register.md#d-005), [PD-009](../project/decision-register.md#pd-009) | Check TCP connection availability. |
| <a id="f-014"></a> F-014 | SSL expiry | v0.5.0 Beta | [D-005](../project/decision-register.md#d-005), [PD-009](../project/decision-register.md#pd-009) | Check remaining TLS certificate validity. |
| <a id="f-015"></a> F-015 | Email | v0.5.0 Beta | [D-005](../project/decision-register.md#d-005) | Receive incident notifications by email. |
| <a id="f-016"></a> F-016 | Webhooks | v0.5.0 Beta | [D-005](../project/decision-register.md#d-005), [PD-006](../project/decision-register.md#pd-006) | Receive incident events at approved webhook destinations. |
| <a id="f-017"></a> F-017 | RBAC | v0.5.0 Beta | [D-005](../project/decision-register.md#d-005), [PD-007](../project/decision-register.md#pd-007) | Restrict operations using workspace roles. |
| <a id="f-018"></a> F-018 | Uptime and latency analytics | v0.5.0 Beta | [D-005](../project/decision-register.md#d-005), [PD-008](../project/decision-register.md#pd-008), [PD-011](../project/decision-register.md#pd-011) | Compare monitoring metrics across Beta filters and selections. |
| <a id="f-019"></a> F-019 | Public status pages | v0.5.0 Beta | [D-005](../project/decision-register.md#d-005) | Publish status for selected monitors. |
| <a id="f-020"></a> F-020 | Maintenance windows | v0.5.0 Beta | [D-005](../project/decision-register.md#d-005) | Schedule and track maintenance windows. |
| <a id="f-021"></a> F-021 | API keys | v0.5.0 Beta | [D-005](../project/decision-register.md#d-005) | Create and revoke workspace-scoped credentials. |
| <a id="f-022"></a> F-022 | Audit log | v1.0.0 Release | [D-005](../project/decision-register.md#d-005) | Inspect a history of approved auditable workspace actions. |
| <a id="f-023"></a> F-023 | Prometheus/Grafana | v1.0.0 Release | [D-005](../project/decision-register.md#d-005) | Inspect operational signals through Prometheus and Grafana. |
| <a id="f-024"></a> F-024 | Report export | v1.0.0 Release | [D-005](../project/decision-register.md#d-005) | Export monitoring information within authorized scope. |
| <a id="f-025"></a> F-025 | Demo mode | v1.0.0 Release | [D-005](../project/decision-register.md#d-005), [PD-010](../project/decision-register.md#pd-010) | Exercise monitoring workflows with controlled synthetic data. |
| <a id="f-026"></a> F-026 | Integration and load testing | v1.0.0 Release | [D-005](../project/decision-register.md#d-005), [PD-012](../project/decision-register.md#pd-012) | Produce repeatable verification evidence. |
| <a id="f-027"></a> F-027 | Public demo deployment | v1.0.0 Release | [D-005](../project/decision-register.md#d-005), [PD-006](../project/decision-register.md#pd-006), [PD-010](../project/decision-register.md#pd-010) | Expose the interactive demo with isolated data and limited resources. |
| <a id="f-028"></a> F-028 | Documentation | v1.0.0 Release | [D-005](../project/decision-register.md#d-005), [PD-015](../project/decision-register.md#pd-015) | Operate and use supported product features with English guidance. |
| <a id="f-029"></a> F-029 | Run Check Now | v0.1.0 MVP | [PD-005](../project/decision-register.md#pd-005) | Request and inspect an asynchronous manual check. |
| <a id="f-030"></a> F-030 | HTTP keyword monitoring | v0.5.0 Beta | [PD-009](../project/decision-register.md#pd-009) | Check for a literal keyword in an HTTP response. |
| <a id="f-031"></a> F-031 | JSON assertion monitoring | v0.5.0 Beta | [PD-009](../project/decision-register.md#pd-009) | Evaluate a declarative JSON condition on a response. |
| <a id="f-032"></a> F-032 | Workspace invitations and membership | v0.5.0 Beta | [PD-007](../project/decision-register.md#pd-007), [PD-001](../project/decision-register.md#pd-001) | Invite participants and manage workspace membership. |
| <a id="f-033"></a> F-033 | Basic uptime and latency metrics | v0.1.0 MVP | [PD-011](../project/decision-register.md#pd-011) | Inspect per-monitor availability and successful check latency in MVP. |

## Release Scope

| Release | Usable increment | Scope assignments |
|---|---|---|
| v0.1.0 MVP | One Owner monitors HTTP/HTTPS endpoints and investigates incidents from the dark responsive web interface. | Baseline F-001–F-012, plus F-029 (PD-005) and F-033 (PD-011). |
| v0.5.0 Beta | Team collaboration, more check types and channels, live updates, analytics, status pages, maintenance and API access. | Baseline F-013–F-021, plus F-030 and F-031 (PD-009), F-032 (PD-007 and PD-001), and SSE (PD-008). |
| v1.0.0 Release | Operational evidence, audit and reports, documentation and an isolated interactive public demo. | Baseline F-022–F-028 with the approved demo extension (PD-010 and PD-006). |

PD-001 refines authentication. PD-002 through PD-004 refine HTTP configuration, cadence and incident behavior. PD-006 and PD-007 refine security and workspace authority. PD-008 refines presentation updates by release. PD-011 and PD-012 define measurement and evidence. PD-013 through PD-015 apply dark-only presentation, responsiveness and language rules from MVP onward. Baseline feature release assignments remain in effect. Later extensions inherit relevant earlier controls.

## Core User Journeys

1. Operator establishes an initial account, chooses whether to allow public signup, and applies installation destination policy.
2. An Owner signs in, creates a valid HTTP monitor, reviews history, and requests a manual check when an immediate observation is needed.
3. A target experiences consecutive qualifying failures. The Owner views the opened incident, receives configured notification and inspects confirmed recovery.
4. In Beta a workspace Owner invites a participant, controls role-based access and publishes selected service status.
5. A v1.0.0 demo visitor exercises a synthetic monitoring journey without access to real installation data or arbitrary destinations.

See [User Flows](user-flows.md) for alternate and failure paths.

## Success Metrics

| Target | Evidence |
|---|---|
| 1,000 active monitors at 60 seconds | Reproducible baseline workload with measured scheduling and result completion. |
| API p95 at most 200 ms | Valid baseline evidence with external check duration excluded. |
| Backend line coverage at least 80% | Coverage report with approved scope and metric. |
| API server error rate below 1% and scheduling delay p95 at most 5 seconds | Valid baseline API and scheduling evidence under Q-11. |
| 30-day check history retention | Controlled-clock visibility and expiry checks. |
| Startup using one documented Docker Compose command after prerequisites and configuration | Clean supported installation and a controlled monitoring journey. |
| Safe public demo | Isolation, quota, cleanup, destination and notification evidence from controlled fixtures. |

These are targets. Implementation measurements are pending.

## Product Constraints

Respect the approved Modular Monolith technical baseline and current technology classifications in the [charter](../project/charter.md#approved-architecture-and-technologies). Product requirements describe externally verifiable behavior. Stage 02 owns detailed design and Stage 03 owns concrete breakpoints and layouts. Implementation requires separate owner authorization.

## Dependencies

Self-hosting requires the approved runtime components. Telegram in MVP, email or webhooks in Beta depend on configured and reachable destinations. Beta team flows depend on scoped MVP identity and authorization. Beta analytics needs qualifying retained observations. The release demo depends on validated synthetic targets and isolation controls.

## Assumptions

Workspace owners have authorization for monitored services. Suitable controlled targets can be made available for integration and performance verification. Browser support and installation prerequisites will be defined in later stages. The project name is a working name pending clearance.

## Risks

See the [risk register](../project/risk-register.md) for network abuse, cross-workspace exposure, false incidents, duplicate work, retention growth, dependency outage, frontend effort and demo abuse. Manual execution and live updates can create bursts. Proposed mitigations require implementation and verification.

## Release Acceptance Gates

- **MVP.** Demonstrate approved authentication, workspace scope, target policy and create → check → incident → configured notification → recovery through the UI. Verify JWT use and refresh, manual execution, polling, single-monitor metrics, dark-only accessibility, mobile usability and retention. Verify required checks through executed GitHub Actions runs under [AC-057](acceptance-criteria.md#ac-057). Reproduce the approved measurement protocol and assess the baseline performance and coverage targets separately.
- **Beta.** Verify integration behavior, new check types, scoped team and API authorization, published data boundaries, maintenance semantics, cross-window and cross-monitor comparisons, observable SSE and update recovery. Verify combined multi-monitor metrics under [Q-06](prd.md#q-06).
- **v1.0.0.** Verify audit and report scope, operational telemetry, published repeatable integration and load evidence, documentation and interactive public demo containment and verified cleanup under the approved lifecycle policy.
- **IP-004.** Owner reviews the finalized requirements and records acceptance before Stage 01 can close.

## IP-004 Product Decisions

The owner approved Q-01–Q-15 in IP-004. The [Decision Register](../project/decision-register.md#ip-004-product-decisions) records their disposition. Final acceptance of the documentation remains with the owner.

<a id="q-01"></a>
### Q-01 — Registration and authentication

**APPROVED.** A protected one-time setup establishes the first Owner. Public registration is closed by default afterward and the Installation Operator can enable it. Sign-in uses email and password. Access JWTs last 15 minutes and refresh tokens last 7 days. Refresh rotates the token. Logout revokes the corresponding refresh session.

**Deferred.** Stage 02 defines the bootstrap mechanism, token storage and session implementation. Stage 03 defines the entry and approved settings surfaces. Stage 03 can propose editable account fields for separate owner approval before implementation.

**Related requirements.** [FR-001](srs.md#fr-001), [FR-002](srs.md#fr-002), [FR-003](srs.md#fr-003), [FR-004](srs.md#fr-004), [FR-005](srs.md#fr-005), [FR-006](srs.md#fr-006), [FR-007](srs.md#fr-007), [FR-008](srs.md#fr-008), [FR-010](srs.md#fr-010)

<a id="q-02"></a>
### Q-02 — HTTP monitor configuration

**APPROVED.** MVP supports GET and HEAD, default GET. The interval defaults to 60 seconds and ranges from 30 seconds to 24 hours. The timeout defaults to 10 seconds and ranges from 1 to 30 seconds, capped by the interval. Only 200–299 is successful. Redirect following is disabled and TLS certificate verification is mandatory. Destination policy applies to every supported connection path.

**Deferred.** Configurable redirects are deferred to future releases. Stage 02 specifies connection handling within these constraints.

**Related requirements.** [FR-016](srs.md#fr-016), [FR-017](srs.md#fr-017), [FR-018](srs.md#fr-018), [FR-019](srs.md#fr-019), [FR-020](srs.md#fr-020), [FR-021](srs.md#fr-021)

<a id="q-03"></a>
### Q-03 — Manual checks

**APPROVED.** Manual checks are diagnostic and unavailable while PAUSED. They do not overlap with another check of the same monitor or change the schedule. Completed results appear in history as Manual and do not affect uptime, aggregated latency, monitor state or automated incidents. Accept at most one manual run per monitor in 30 seconds.

**Deferred.** Stage 02 defines overlap handling and enforcement. Stage 03 defines feedback for ineligible or overlapping requests.

**Related requirements.** [FR-023](srs.md#fr-023), [FR-024](srs.md#fr-024), [FR-025](srs.md#fr-025), [NFR-005](srs.md#nfr-005), [FR-026](srs.md#fr-026), [FR-027](srs.md#fr-027), [FR-028](srs.md#fr-028), [FR-029](srs.md#fr-029), [FR-061](srs.md#fr-061), [FR-062](srs.md#fr-062), [FR-063](srs.md#fr-063), [FR-064](srs.md#fr-064), [FR-015](srs.md#fr-015)

<a id="q-04"></a>
### Q-04 — Monitor lifecycle and incidents

**APPROVED.** States are PENDING, UP, DOWN and PAUSED. Creation starts in PENDING and the first qualifying success of a new monitor sets UP. Configurable consecutive failure and recovery thresholds default to 3 and 2. Crossing the failure threshold sets DOWN and opens an incident. Confirmed recovery sets UP and closes it. Pause sets PAUSED and preserves an open incident. Resume sets PENDING and a retained incident closes only after confirmed recovery. Deletion closes an open incident as Monitor Deleted. Changing the checked address of an active monitor sets PENDING and closes any open incident as Configuration Changed. Under [PD-016](../project/decision-register.md#pd-016), changing the checked URL of a PAUSED monitor keeps it PAUSED, closes any open incident as Configuration Changed, resets both result streaks and advances the configuration version. The edit starts no automatic check. A later Resume sets PENDING. Pause and configuration edits reset streaks. Internal faults do not establish unavailability. Stale results cannot alter live state. A scheduled check cannot start while PAUSED, including one queued before pause.

**Design.** The approved [incident engine](../architecture/backend-design.md#incident-engine) defines ordering, concurrency and stale-result handling. Additional lifecycle rules or threshold bounds require owner approval before becoming normative.

**Related requirements.** [FR-014](srs.md#fr-014), [FR-015](srs.md#fr-015), [FR-031](srs.md#fr-031), [FR-032](srs.md#fr-032), [FR-033](srs.md#fr-033), [FR-034](srs.md#fr-034), [FR-035](srs.md#fr-035), [FR-036](srs.md#fr-036), [FR-037](srs.md#fr-037), [FR-011](srs.md#fr-011)

<a id="q-05"></a>
### Q-05 — Notifications

**APPROVED.** Telegram is the MVP channel. Incident Opened and Incident Resolved are enabled by default and delivery requires a configured, enabled channel. Manual Check Completed, Monitor Paused and Internal System Error notifications are outside MVP. Confirmed eligible delivery failures may have bounded retries. An indeterminate outcome must not trigger blind resending. Sequential replay and concurrent handling preserve one business effect for the same logical event and destination.

**Deferred.** Stage 02 defines the retry policy and deduplication mechanism. Confirmed-success receipt evidence is required under controlled conditions. Unconditional exactly-once delivery through the provider is outside the contract.

**Related requirements.** [FR-038](srs.md#fr-038), [FR-039](srs.md#fr-039), [NFR-007](srs.md#nfr-007), [FR-046](srs.md#fr-046), [FR-047](srs.md#fr-047), [FR-065](srs.md#fr-065), [NFR-004](srs.md#nfr-004)

<a id="q-06"></a>
### Q-06 — Uptime and latency

**APPROVED.** Use UTC windows of 24h, 7d and 30d. Uptime is Successful / (Successful + Failed) × 100%, using valid scheduled checks. Target TIMEOUT counts as failed. Exclude internal errors, skipped checks, pauses and manual checks. Latency uses successful scheduled checks only, with average, nearest-rank p95 and nearest-rank p99. The minimum samples are 20 and 100 for p95 and p99 respectively. Show No data for an empty eligible sample. Beta aggregation pools valid observations across selected monitors.

**Deferred.** Stage 02 defines exact window and measurement boundaries. Stage 03 defines presentation and rounding without changing eligibility or sample minimums.

**Related requirements.** [FR-028](srs.md#fr-028), [FR-052](srs.md#fr-052), [FR-061](srs.md#fr-061), [FR-062](srs.md#fr-062), [FR-063](srs.md#fr-063), [FR-064](srs.md#fr-064), [FR-066](srs.md#fr-066)

<a id="q-07"></a>
### Q-07 — RBAC, workspaces and invitations

**APPROVED.** MVP uses Owner only. Beta uses Owner, Admin, Member and Viewer with the [approved permission matrix](srs.md#beta-authorization-matrix). Admin cannot alter Owner authority or appoint a new Owner. The last Owner cannot leave without transferring ownership. Invitations are single-use, last 7 days and can be revoked. Workspace isolation is mandatory in all releases.

**Deferred.** Beta design specifies invitation and membership contracts and authorization for operations outside the approved matrix before implementation.

**Related requirements.** [FR-048](srs.md#fr-048), [FR-049](srs.md#fr-049), [FR-050](srs.md#fr-050), [FR-051](srs.md#fr-051), [FR-055](srs.md#fr-055), [FR-009](srs.md#fr-009), [NFR-001](srs.md#nfr-001)

<a id="q-08"></a>
### Q-08 — Data retention

**APPROVED.** Check results expire 30 days from UTC check completion. Cleanup must finish within 24 hours of expiry. Deleting a monitor deletes its check history and preserves incident history. Incident history is retained until workspace deletion.

**Deferred.** Stage 02 defines the storage model, indexes, partitioning and cleanup mechanism.

**Related requirements.** [FR-014](srs.md#fr-014), [NFR-006](srs.md#nfr-006), [FR-037](srs.md#fr-037)

<a id="q-09"></a>
### Q-09 — Additional monitor types

**APPROVED.** Beta adds TCP port reachability, TLS certificate validity and expiry, literal HTTP response keyword matching, and bounded declarative JSON assertions without user code. Malformed target JSON fails the check. Response size and computation are bounded.

**Deferred.** Before Beta implementation, define exact limits, input rules, certificate threshold semantics and JSON comparison operators.

**Related requirements.** [FR-043](srs.md#fr-043), [FR-044](srs.md#fr-044), [FR-045](srs.md#fr-045), [FR-059](srs.md#fr-059), [FR-060](srs.md#fr-060), [NFR-022](srs.md#nfr-022)

<a id="q-10"></a>
### Q-10 — Network security and SSRF

**APPROVED.** Eligible public IPv4 and IPv6 are allowed. Private access is denied by default and the Installation Operator may allow eligible internal networks. Always-denied destinations, including loopback, link-local and cloud metadata, take precedence. Normalize IPv4-mapped IPv6 and reject the entire check for mixed eligible and denied DNS answers. Workspace Owners cannot bypass installation policy. MVP supports HTTP and HTTPS with ports 80 and 443 allowed by default. Additional ports require administrative configuration. The [destination rules](business-rules.md#destination-rules) and [AC-051](acceptance-criteria.md#ac-051) / [AC-052](acceptance-criteria.md#ac-052) apply.

**Deferred.** Stage 02 defines DNS resolution, rebinding protection, egress enforcement, allowlist representation and installation-wide rate policy.

**Related requirements.** [FR-010](srs.md#fr-010), [NFR-008](srs.md#nfr-008), [NFR-009](srs.md#nfr-009), [NFR-010](srs.md#nfr-010), [NFR-011](srs.md#nfr-011), [NFR-012](srs.md#nfr-012), [FR-047](srs.md#fr-047), [NFR-017](srs.md#nfr-017), [NFR-022](srs.md#nfr-022), [FR-035](srs.md#fr-035)

<a id="q-11"></a>
### Q-11 — Performance and quality

**APPROVED.** Baseline targets are 1,000 active monitors at 60 seconds, API p95 ≤ 200 ms excluding external check duration, API server error rate < 1%, scheduling delay p95 ≤ 5 seconds, backend line coverage ≥ 80% and 30 days of check-result retention. Reference workload uses 4 vCPU, 8 GB RAM, SSD, 20 concurrent API users, 5 minutes of warm-up and 30 minutes of measurement. The 1,000-monitor 30-second run is stress characterization. These are targets.

**Deferred.** Stage 07 defines the reproducible protocol, endpoint list, request profile and coverage scope. Baseline and coverage attainment are reported as PASS, FAIL or INCOMPLETE using actual evidence.

**Related requirements.** [NFR-023](srs.md#nfr-023), [NFR-024](srs.md#nfr-024), [NFR-025](srs.md#nfr-025), [NFR-026](srs.md#nfr-026), [NFR-032](srs.md#nfr-032), [NFR-033](srs.md#nfr-033), [NFR-006](srs.md#nfr-006)

<a id="q-12"></a>
### Q-12 — Data freshness

**APPROVED.** MVP uses HTTP polling every 10 seconds on the [mandatory screens](user-flows.md#mvp-polling-scope). Indicate stale data after 30 seconds without a successful refresh, support manual refresh and resume automatically when connectivity returns. Beta uses SSE.

**Deferred.** Stage 02 and Stage 03 define transport and display details, including Beta reconnect policy and freshness presentation.

**Related requirements.** [FR-041](srs.md#fr-041), [FR-042](srs.md#fr-042), [NFR-031](srs.md#nfr-031)

<a id="q-13"></a>
### Q-13 — Interactive demo

**APPROVED.** v1.0.0 provides registration-free isolated temporary workspaces with controlled HTTP services. Visitors can create monitors and observe incidents open and resolve. Limit sessions to 5 monitors and 60 minutes. Complete actual cleanup within 15 minutes after session termination. Arbitrary external destinations and real notification delivery are prohibited.

**Deferred.** v1.0.0 design defines session isolation and cleanup implementation before development. Stage 03 defines entry, expiry and reset UX.

**Related requirements.** [FR-058](srs.md#fr-058), [NFR-017](srs.md#nfr-017), [NFR-018](srs.md#nfr-018), [NFR-019](srs.md#nfr-019)

<a id="q-14"></a>
### Q-14 — Accessibility and responsive design

**APPROVED.** Use Dark Only, English UI and desktop-first responsive design supporting principal operations on mobile. Target WCAG 2.2 AA. Provide keyboard navigation, visible focus and non-color status cues. Representative widths are 360, 768, 1024 and 1440 px.

**Deferred.** Stage 03 defines layouts, breakpoints, supported browser coverage and implementation details.

**Related requirements.** [NFR-027](srs.md#nfr-027), [NFR-028](srs.md#nfr-028), [NFR-029](srs.md#nfr-029)

<a id="q-15"></a>
### Q-15 — Beta and release contracts

**APPROVED.** Beta public status pages expose status, uptime and public incidents for selected monitors. Beta API keys have limited permissions, expiry and revocation. During Beta maintenance windows, scheduled checks continue, notifications are suppressed and maintenance observations are excluded from uptime. v1.0.0 audit records contain actor, action, resource, timestamp and outcome. Reports export CSV. Operational visibility uses Prometheus and Grafana.

**Deferred.** Before implementation of the applicable release, define detailed API and event contracts, storage rules and data models. Maintenance effects on latency and incident processing require separate owner validation.

**Related requirements.** [FR-053](srs.md#fr-053), [FR-054](srs.md#fr-054), [FR-055](srs.md#fr-055), [FR-056](srs.md#fr-056), [NFR-016](srs.md#nfr-016), [FR-057](srs.md#fr-057)

## References

- [Project Charter](../project/charter.md)
- [Decision Register](../project/decision-register.md)
- [Software Requirements Specification](srs.md)
- [User Flows and Screen Catalog](user-flows.md)
- [Requirements Traceability Matrix](requirements-traceability-matrix.md)
- [Project Roadmap](../project/roadmap.md)
- [Risk Register](../project/risk-register.md)
