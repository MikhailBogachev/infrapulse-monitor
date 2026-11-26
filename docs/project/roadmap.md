# Development Roadmap
ID: IP-DOC-002 | Version: 1.0 | Status: Approved baseline

Eight-week planning estimate for InfraPulse alone, not a delivery guarantee. Weeks are relative to kickoff; gates take precedence over dates.

| Stage | Weeks | Deliverables / exit gate |
|---|---|---|
| 00 Initialization | 1 | Approved charter, roadmap, risks, glossary |
| 01 Product Discovery | 1 | COMPLETED AND APPROVED. IP-003 and IP-004 delivered and finalized the product baseline. |
| 02 System Design | 1–2 | COMPLETED AND APPROVED. IP-005 delivers the approved architecture, ERD, API, queue semantics, threat model and ADRs. |
| 03 UI/UX | 2 | PENDING. IP-006 covers screen flows, design system and responsive mockups. |
| 04 Development Setup | 2 | Repository, locked dependencies, [GitHub Actions CI](decision-register.md#d-010), Compose, verified toolchain and [six mandatory technical spikes](../architecture/system-architecture.md#verification-gates) |
| 05 Backend | 3–6 | Tested vertical slices, MVP then beta scope |
| 06 Frontend | 4–6 | Usable UI integrated with API |
| 07 QA | 6–7 | Security, integration, end-to-end, load and retention evidence |
| 08 Deployment | 7–8 | Safe demo, operational runbook, recovery verification |
| 09 Release | 8 | Release notes, README, screenshots, architecture, tagged release |

## Product Discovery deliverables

Stage 01 is **COMPLETED AND APPROVED**. IP-002 is approved. IP-003 delivers the [PRD](../product/prd.md), [SRS](../product/srs.md), [personas](../product/user-personas.md), [stories](../product/user-stories.md), [flows and screen catalog](../product/user-flows.md), [business rules](../product/business-rules.md), [acceptance criteria](../product/acceptance-criteria.md), [backlog](../product/product-backlog.md) and [traceability matrix](../product/requirements-traceability-matrix.md).

IP-003 is **COMPLETED AND MERGED**, including its review corrections.

## IP-005 final acceptance

IP-004 is **COMPLETED AND MERGED**. [Q-01–Q-15](decision-register.md#ip-004-product-decisions) form the approved product baseline. IP-005 and Stage 02 are **COMPLETED AND APPROVED**. The owner accepted the [system design](../architecture/system-architecture.md), [AD-013–AD-016](decision-register.md#ad-013) and [PD-016](decision-register.md#pd-016) in IP-005 Final Acceptance. Stage 03 is **PENDING**. Next task: **IP-006 — UI/UX Design**. The [verification gates](../architecture/system-architecture.md#verification-gates) retain the pending Stage 04 spikes and Stage 07 load and retention checks.

## Release gates

- **v0.1.0 MVP.** F-001–F-012, F-029 and F-033. Demonstrate create monitor → check → incident → notification → recovery, manual checks and basic metrics through the dark, responsive UI. Verify registration, isolation and destination policy.
- **v0.5.0 Beta.** F-013–F-021 and F-030–F-032. Verify integrations, additional check types, team authorization, live updates and expanded analytics.
- **v1.0.0 Release.** F-022–F-028. Publish reproducible measured results and complete documentation. Validate the isolated interactive public demo.

See the [Decision Register](decision-register.md#approved-product-decisions) for the scope sources and the [PRD release gates](../product/prd.md#release-acceptance-gates) for expected evidence.

## Change control
Record scope changes in issues; update affected requirements, risks and roadmap. Obtain owner approval before expanding release scope. Defer optional features rather than compromising security or correctness. Overlapping weeks permit preparation, not bypassing approval gates.
