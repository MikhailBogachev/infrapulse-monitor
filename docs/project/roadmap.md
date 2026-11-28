# Development Roadmap
ID: IP-DOC-002 | Version: 1.0 | Status: Approved baseline

Eight-week planning estimate for InfraPulse alone, not a delivery guarantee. Weeks are relative to kickoff; gates take precedence over dates.

| Stage | Weeks | Deliverables / exit gate |
|---|---|---|
| 00 Initialization | 1 | Approved charter, roadmap, risks, glossary |
| 01 Product Discovery | 1 | COMPLETED AND APPROVED. IP-003 and IP-004 delivered and finalized the product baseline. |
| 02 System Design | 1–2 | COMPLETED AND APPROVED. IP-005 delivers the approved architecture, ERD, API, queue semantics, threat model and ADRs. |
| 03 UI/UX | 2 | COMPLETED AND APPROVED. The owner accepted the design documentation and local interactive HTML prototype in [IP-006 Final Acceptance](#ip-006-uiux-design). |
| 04 Development Setup | 2 | COMPLETED AND APPROVED. Repository, locked dependencies, [GitHub Actions CI](decision-register.md#d-010), Compose, verified toolchain and [six mandatory technical spikes](../architecture/system-architecture.md#verification-gates) |
| 05 Backend | 3–6 | PENDING. Tested vertical slices, MVP then beta scope |
| 06 Frontend | 4–6 | Usable UI integrated with API |
| 07 QA | 6–7 | Security, integration, end-to-end, load and retention evidence |
| 08 Deployment | 7–8 | Safe demo, operational runbook, recovery verification |
| 09 Release | 8 | Release notes, README, screenshots, architecture, tagged release |

## Product Discovery deliverables

Stage 01 is **COMPLETED AND APPROVED**. IP-002 is approved. IP-003 delivers the [PRD](../product/prd.md), [SRS](../product/srs.md), [personas](../product/user-personas.md), [stories](../product/user-stories.md), [flows and screen catalog](../product/user-flows.md), [business rules](../product/business-rules.md), [acceptance criteria](../product/acceptance-criteria.md), [backlog](../product/product-backlog.md) and [traceability matrix](../product/requirements-traceability-matrix.md).

IP-003 is **COMPLETED AND MERGED**, including its review corrections.

## IP-005 final acceptance

IP-004 is **COMPLETED AND MERGED**. [Q-01–Q-15](decision-register.md#ip-004-product-decisions) form the approved product baseline. IP-005 and Stage 02 are **COMPLETED AND APPROVED**. The owner accepted the [system design](../architecture/system-architecture.md), [AD-013–AD-016](decision-register.md#ad-013) and [PD-016](decision-register.md#pd-016) in IP-005 Final Acceptance. The [verification gates](../architecture/system-architecture.md#verification-gates) track the Stage 04 spikes and Stage 07 load and retention checks.

## IP-006 UI/UX design

IP-006 and Stage 03 are **COMPLETED AND APPROVED**. In IP-006 Final Acceptance, the owner approved [UX-001–UX-012](decision-register.md#approved-stage-03-ux-decisions), the [design system](../design/design-system.md), specifications for all 11 [MVP screens](../design/screen-specifications.md) and the [interactive HTML prototype](../design/prototype/index.html). The design documentation and prototype form the approved design baseline for MVP v0.1.0.

### Owner manual verification

The owner completed visual and functional review and reported that all 15 checklist items passed with no findings. The review covered responsive layouts at 360, 768, 1024 and 1440 px, principal user journeys and manual keyboard navigation.

### Codex automated verification

Codex verified status consistency, ran `git diff HEAD --check` and checked whitespace in all nine new design files. All checks passed.

### Pending verification and next task

Full WCAG 2.2 AA conformance remains unverified. Apply the [accessibility verification checklist](../design/accessibility.md#verification-checklist) to the production frontend, including browser reflow, keyboard interaction and assistive technology checks.

## IP-007 development environment

IP-007 and Stage 04 are **COMPLETED AND APPROVED**. [Final Owner Acceptance](decision-register.md#ip-007-verification) records the 2026-11-28 approval and verification results. The [setup guide](../development/setup.md) documents the development foundation.

Stage 05 is **PENDING** and requires explicit owner authorization. Production egress enforcement and the worker execution guard still require implementation and verification. Load and retention verification remains in Stage 07.

## Release gates

- **v0.1.0 MVP.** F-001–F-012, F-029 and F-033. Demonstrate create monitor → check → incident → notification → recovery, manual checks and basic metrics through the dark, responsive UI. Verify registration, isolation and destination policy.
- **v0.5.0 Beta.** F-013–F-021 and F-030–F-032. Verify integrations, additional check types, team authorization, live updates and expanded analytics.
- **v1.0.0 Release.** F-022–F-028. Publish reproducible measured results and complete documentation. Validate the isolated interactive public demo.

See the [Decision Register](decision-register.md#approved-product-decisions) for the scope sources and the [PRD release gates](../product/prd.md#release-acceptance-gates) for expected evidence.

## Change control
Record scope changes in issues; update affected requirements, risks and roadmap. Obtain owner approval before expanding release scope. Defer optional features rather than compromising security or correctness. Overlapping weeks permit preparation, not bypassing approval gates.
