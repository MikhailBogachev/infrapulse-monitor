# InfraPulse Product Requirements Document

| Field | Value |
|---|---|
| Document Status | DRAFT — PENDING VALIDATION |
| Version | 0.1 |
| Responsible Role | Product Analyst |
| Related Project Stage | Stage 01 — Product Discovery |
| Project Task | IP-003 |
| Validation | IP-004, pending owner review |

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

The [Decision Register](../project/decision-register.md#approved-product-decisions) defines PD-001 through PD-015. Approval applies to product decisions and their explicit scope. The derived requirements are draft material for IP-004. The [matrix](requirements-traceability-matrix.md) maps decisions to features and verification.

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
| <a id="f-012"></a> F-012 | Docker Compose, migrations and CI | v0.1.0 MVP | [D-004](../project/decision-register.md#d-004), [D-005](../project/decision-register.md#d-005), [PD-012](../project/decision-register.md#pd-012) | Start, upgrade and verify a self-hosted environment. |
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
| API p95 at most 200 ms | API latency distribution under an approved operation mix. |
| Backend test coverage at least 80% | Coverage report with approved scope and metric. |
| 30-day check history retention | Controlled-clock visibility and expiry checks. |
| Startup using one documented Docker Compose command after prerequisites and configuration | Clean supported installation and a controlled monitoring journey. |
| Safe public demo | Isolation, quota, cleanup, destination and notification evidence from controlled fixtures. |

These are targets. There are no implementation measurements in IP-003.

## Product Constraints

Respect the approved Modular Monolith technical baseline and Stage 00 technology classifications in the [charter](../project/charter.md#approved-architecture-and-technologies). Product requirements describe externally verifiable behavior. Stage 02 owns detailed design and Stage 03 owns concrete breakpoints and layouts. Implementation requires separate owner authorization.

## Dependencies

Self-hosting requires the approved runtime components. Telegram in MVP, email or webhooks in Beta depend on configured and reachable destinations. Beta team flows depend on scoped MVP identity and authorization. Beta analytics needs qualifying retained observations. The release demo depends on validated synthetic targets and isolation controls.

## Assumptions

Workspace owners have authorization for monitored services. Suitable controlled targets can be made available for integration and performance verification. The reference performance environment, browser support and installation prerequisites are pending validation. The project name is a working name pending clearance.

## Risks

See the [risk register](../project/risk-register.md) for network abuse, cross-workspace exposure, false incidents, duplicate work, retention growth, dependency outage, frontend effort and demo abuse. Manual execution and live updates can create bursts. Proposed mitigations require implementation and verification.

## Release Acceptance Gates

- **MVP.** Demonstrate approved authentication, workspace scope, target policy and create → check → incident → configured notification → recovery through the UI. Verify manual execution, dark-only accessibility, mobile usability, retention and the approved baseline measurement protocol.
- **Beta.** Verify integration behavior, new check types, scoped team and API authorization, published data boundaries, maintenance semantics, metric results and update recovery.
- **v1.0.0.** Verify audit and report scope, operational telemetry, published repeatable integration and load evidence, documentation and interactive public demo containment and cleanup.
- **IP-004.** Owner validates the draft requirements, resolves or explicitly defers open questions, and records disposition. Stage 01 remains in progress.

## Open Questions

All product questions require owner validation. Priority uses MoSCoW.

<a id="q-01"></a>
### Q-01 — Bootstrap, sessions and settings

**PENDING** · Must · IP-004 product rules, Stage 02 mechanism. Affected requirements [FR-001](srs.md#fr-001), [FR-002](srs.md#fr-002), [FR-003](srs.md#fr-003), [FR-004](srs.md#fr-004), [FR-005](srs.md#fr-005), [FR-006](srs.md#fr-006), [FR-007](srs.md#fr-007), [FR-008](srs.md#fr-008), [FR-010](srs.md#fr-010).

**Proposal.** Use an operator-authorized one-time setup path and review editable account and workspace fields, account ownership, validation, session expiry and signup feedback as a minimal set.

**Alternatives.** Operator-provisioned first account or one-time setup entry. Read-only settings until editable fields are approved.

**Trade-offs.** Provisioning reduces public surface but adds operator work. A setup entry improves discovery but needs a secure initial access gate.

**Impact if unresolved.** Identity journeys and the operator control surface cannot be verified end to end.

<a id="q-02"></a>
### Q-02 — HTTP defaults and configuration bounds

**PROPOSED** · Must · IP-004. Affected requirements [FR-016](srs.md#fr-016), [FR-017](srs.md#fr-017), [FR-018](srs.md#fr-018), [FR-019](srs.md#fr-019), [FR-020](srs.md#fr-020), [FR-021](srs.md#fr-021).

**Proposal.** Use the listed HTTP defaults, 60-second interval, one-second step and 24-hour maximum. Validate timeout bounds and accepted status input form.

**Alternatives.** Use an interval preset list or a different maximum. Require explicit target options on creation.

**Trade-offs.** Fine-grained intervals suit diverse services but allow more scheduling configurations. Presets simplify validation but reduce flexibility.

**Impact if unresolved.** Defaults and boundary tests remain conditional.

<a id="q-03"></a>
### Q-03 — Manual eligibility, collision and rate policy

**PROPOSED** · Must · IP-004. Affected requirements [FR-023](srs.md#fr-023), [FR-024](srs.md#fr-024), [FR-025](srs.md#fr-025), [NFR-005](srs.md#nfr-005), [FR-026](srs.md#fr-026), [FR-027](srs.md#fr-027), [FR-028](srs.md#fr-028), [FR-029](srs.md#fr-029), [FR-061](srs.md#fr-061), [FR-062](srs.md#fr-062), [FR-063](srs.md#fr-063), [FR-064](srs.md#fr-064).

**Proposal.** Reject paused requests, show existing work on overlap, record a missed scheduled opportunity when a manual check takes its place, keep fixed cadence and exclude manual checks from scheduled metrics and incident evaluation. Define finite rate key, window and cap.

**Alternatives.** Defer overlapping work or let manual checks advance incident and uptime counts. Apply per-monitor, per-user or per-workspace limits.

**Trade-offs.** Keeping manual runs separate preserves scheduled comparability but immediate verification does not resolve an incident. Deferred execution may increase backlog. Scope of throttling affects fairness.

**Impact if unresolved.** Throttling, run eligibility and manual metric and incident acceptance cannot be finalized.

<a id="q-04"></a>
### Q-04 — Incident sequences and monitor lifecycle

**PROPOSED** · Must · IP-004. Affected requirements [FR-014](srs.md#fr-014), [FR-015](srs.md#fr-015), [FR-031](srs.md#fr-031), [FR-032](srs.md#fr-032), [FR-033](srs.md#fr-033), [FR-034](srs.md#fr-034), [FR-035](srs.md#fr-035), [FR-036](srs.md#fr-036), [FR-037](srs.md#fr-037).

**Proposal.** Adopt the proposed transition table. Use positive integer thresholds and validate the upper bounds. Preserve an incident through pause and configuration changes. Archive open incident disposition on deletion and decide historical access.

**Alternatives.** Reset streaks on every gap, close incidents on pause or configuration change, or reconcile late state retroactively.

**Trade-offs.** Ignoring excluded results keeps target evidence separate but spans observation gaps. Preserving incidents avoids false recovery but can keep an incident open longer.

**Impact if unresolved.** Lifecycle, counter ordering, result class edges and configuration transition tests remain conditional.

<a id="q-05"></a>
### Q-05 — Notification defaults and delivery outcome

**PROPOSED** · Must · IP-004 product rules, Stage 02 delivery model. Affected requirements [FR-038](srs.md#fr-038), [FR-039](srs.md#fr-039), [NFR-007](srs.md#nfr-007), [FR-046](srs.md#fr-046), [FR-047](srs.md#fr-047).

**Proposal.** Enable opening and recovery notices when a channel is configured. Distinguish permanent from transient failure with a finite retry policy and surface ambiguous outcomes.

**Alternatives.** Per-event opt-in, or retry fewer ambiguous failures.

**Trade-offs.** Defaults improve visibility but may increase noise. Retrying ambiguous provider outcomes risks recipient duplicates.

**Impact if unresolved.** Notification preferences, retry evidence and ambiguous outcomes remain unsettled.

<a id="q-06"></a>
### Q-06 — Metric windows, latency and aggregation

**PROPOSED** · Must · IP-004. Affected requirements [FR-028](srs.md#fr-028), [FR-052](srs.md#fr-052), [FR-061](srs.md#fr-061), [FR-062](srs.md#fr-062), [FR-063](srs.md#fr-063), [FR-064](srs.md#fr-064).

**Proposal.** Use the proposed UTC observation windows, rounding, nearest-rank percentiles and sample rules. Aggregate qualifying observations across selected eligible monitors in Beta.

**Alternatives.** Use interpolated percentiles, minimum sample thresholds per quantile, or equal weighting per monitor.

**Trade-offs.** Nearest-rank is reproducible but coarse for small samples. Observation weighting can favor frequently checked targets.

**Impact if unresolved.** Exact analytics and cross-window comparisons cannot be validated.

<a id="q-07"></a>
### Q-07 — Beta role matrix and invitations

**PROPOSED** · Must · IP-004. Affected requirements [FR-048](srs.md#fr-048), [FR-049](srs.md#fr-049), [FR-050](srs.md#fr-050), [FR-051](srs.md#fr-051), [FR-055](srs.md#fr-055).

**Proposal.** Use the proposed role matrix, protect last-Owner continuity and validate invitation expiry, cancellation, expiry feedback and current membership enforcement.

**Alternatives.** Use fewer roles or reserve all membership operations to Owner.

**Trade-offs.** Delegation suits teams but raises complexity and the risk of excess access.

**Impact if unresolved.** Permission coverage and invitation abuse controls remain conditional.

<a id="q-08"></a>
### Q-08 — Retention boundaries and removal

**PROPOSED** · Must · IP-004 product rules, Stage 02 implementation. Affected requirements [FR-014](srs.md#fr-014), [NFR-006](srs.md#nfr-006), [FR-037](srs.md#fr-037).

**Proposal.** Anchor retention to UTC observation completion and make data at least 30 days old expire. Validate cleanup lag and deletion interaction.

**Alternatives.** Use receipt time or calendar-day buckets.

**Trade-offs.** Completion aligns with analysis but late results can arrive expired. Calendar-day buckets simplify explanation but vary effective age.

**Impact if unresolved.** Retention boundary, user visibility and cleanup timing remain conditional.

<a id="q-09"></a>
### Q-09 — Additional check input and edge semantics

**PROPOSED** · Must · IP-004. Affected requirements [FR-043](srs.md#fr-043), [FR-044](srs.md#fr-044), [FR-045](srs.md#fr-045), [FR-059](srs.md#fr-059), [FR-060](srs.md#fr-060), [NFR-022](srs.md#nfr-022).

**Proposal.** Adopt the typed check proposals, cap input and response costs, and validate TLS time boundaries, literal matching, JSON assertion operators and timeout classification.

**Alternatives.** Use exact literal-only JSON comparisons or support additional bounded declarative operators. Default TLS port or require it.

**Trade-offs.** Minimal operators are easier to secure but cover fewer API contracts. Explicit ports reduce ambiguity at setup cost.

**Impact if unresolved.** Beta invalid input, equality and response limits cannot be finalized.

<a id="q-10"></a>
### Q-10 — Installation destination policy detail

**PENDING** · Must · IP-004 product rules, Stage 02 threat model. Affected requirements [FR-010](srs.md#fr-010), [NFR-008](srs.md#nfr-008), [NFR-009](srs.md#nfr-009), [NFR-010](srs.md#nfr-010), [NFR-011](srs.md#nfr-011), [NFR-012](srs.md#nfr-012), [FR-047](srs.md#fr-047), [NFR-017](srs.md#nfr-017), [NFR-022](srs.md#nfr-022).

**Proposal.** Adopt deny precedence, classify internal allowlist eligibility and always-denied address classes, and validate port, redirect and general rate policy with controlled fixtures.

**Alternatives.** Limit allowlisting to isolated host entries or permit approved bounded ranges. Reject any mixed DNS answer set or use only still-eligible answers.

**Trade-offs.** Host entries reduce reachability but add maintenance. Mixed-answer rejection simplifies assurance but lowers availability.

**Impact if unresolved.** Security-boundary verification and operator controls need a validated exact policy.

<a id="q-11"></a>
### Q-11 — Performance workload and coverage protocol

**PROPOSED** · Must · IP-004 protocol, Stage 07 execution. Affected requirements [NFR-023](srs.md#nfr-023), [NFR-024](srs.md#nfr-024), [NFR-025](srs.md#nfr-025), [NFR-026](srs.md#nfr-026), [NFR-032](srs.md#nfr-032).

**Proposal.** Use the proposed workload mix, client count and measurement periods. Approve reference environment, failure allowances, scheduling and backlog criteria, and coverage scope.

**Alternatives.** Use multiple representative hardware profiles or a single fixed reference environment. Use line and branch thresholds separately.

**Trade-offs.** Multiple profiles improve capacity context but consume more effort. One fixed profile improves repeatability but limits extrapolation.

**Impact if unresolved.** Targets remain unevaluated and release comparison lacks fixed methodology.

<a id="q-12"></a>
### Q-12 — Update cadence and freshness

**PENDING** · Should · IP-004 product tolerance, Stage 03 UX. Affected requirements [FR-041](srs.md#fr-041), [FR-042](srs.md#fr-042), [NFR-031](srs.md#nfr-031).

**Proposal.** Validate the accepted refresh delay, stale threshold, reconnect expectations and polling behavior for inactive tabs.

**Alternatives.** Use user-triggered refresh during outages or continue bounded automatic refresh.

**Trade-offs.** Faster updates improve freshness but increase background traffic.

**Impact if unresolved.** Timing acceptance and Beta reconnect readiness remain open.

<a id="q-13"></a>
### Q-13 — Demo surfaces, limits and cleanup

**PENDING** · Must · IP-004 policy, Stage 03 UX. Affected requirements [FR-058](srs.md#fr-058), [NFR-017](srs.md#nfr-017), [NFR-018](srs.md#nfr-018), [NFR-019](srs.md#nfr-019).

**Proposal.** Reuse existing monitoring screens for synthetic workflows and propose an entry and reset surface or automatic expiry. Validate quotas, session duration, cleanup bound and allowed simulated notifications.

**Alternatives.** Use a shared read-only tour plus isolated interactive sessions, or isolated sessions alone.

**Trade-offs.** Reuse limits UI effort. Visible reset improves clarity. Automatic cleanup limits exposure but may interrupt a visitor.

**Impact if unresolved.** Demo screen coverage and isolation acceptance cannot be closed.

<a id="q-14"></a>
### Q-14 — Responsive and accessibility verification

**PENDING** · Must · IP-004 verification baseline, Stage 03 layouts. Affected requirements [NFR-027](srs.md#nfr-027), [NFR-028](srs.md#nfr-028), [NFR-029](srs.md#nfr-029).

**Proposal.** Validate a contrast and keyboard verification baseline and representative mobile and desktop test viewports. Define concrete layout and breakpoints in Stage 03.

**Alternatives.** Test a broader device matrix or a minimal supported set.

**Trade-offs.** More devices improve confidence but increase review cost. A minimal set leaves more rendering uncertainty.

**Impact if unresolved.** Dark-only behavior is testable now as a specification. Exact contrast and responsive evidence remains undefined.

<a id="q-15"></a>
### Q-15 — Baseline Beta and release feature details

**PENDING** · Should · IP-004 product behavior, Stage 02 contracts. Affected requirements [FR-053](srs.md#fr-053), [FR-054](srs.md#fr-054), [FR-055](srs.md#fr-055), [FR-056](srs.md#fr-056), [NFR-016](srs.md#nfr-016), [FR-057](srs.md#fr-057).

**Proposal.** Validate public status fields, API key scopes and expiry, maintenance boundaries and effects, auditable events, operational signal set and export formats.

**Alternatives.** Adopt a minimal field set and expand after release, or broaden supported fields after owner review.

**Trade-offs.** Minimal exposure protects sensitive data and reduces validation effort but limits reporting and automation flexibility.

**Impact if unresolved.** Detailed gates remain conditional for these approved baseline features.

## References

- [Project Charter](../project/charter.md)
- [Decision Register](../project/decision-register.md)
- [Software Requirements Specification](srs.md)
- [User Flows and Screen Catalog](user-flows.md)
- [Requirements Traceability Matrix](requirements-traceability-matrix.md)
- [Project Roadmap](../project/roadmap.md)
- [Risk Register](../project/risk-register.md)
