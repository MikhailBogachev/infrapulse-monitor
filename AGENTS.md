# Instructions for coding agents

## Project context
Repository documentation is the primary source of project context. Before work, read the [charter](docs/project/charter.md), [roadmap](docs/project/roadmap.md), [risk register](docs/project/risk-register.md) and [glossary](docs/project/glossary.md). Read applicable approved product specifications and ADRs when present.

- Stage 00 — Project Initialization is approved and complete.
- Stage 01 — Product Discovery is in progress.
- Stage 02 — System Design is pending.
- IP-000 — Project Context Initialization is accepted.
- IP-001 — Project Initialization Baseline Corrections is complete and merged.
- IP-002 — Product Discovery Decision Review is approved.
- IP-003 — Product Requirements Documentation was merged in PR #2 with unresolved findings. Final Reviews R1 and R2 required corrections.
- IP-003-R1 — Review corrections are complete in the working tree.
- IP-003-R2 — Targeted review corrections are complete. Independent Final Review R3 failed.
- IP-003-R3 — Targeted acceptance criteria corrections were reviewed in Final Review R4, which identified REV-010 as the remaining blocker.
- IP-003-R4 — REV-010 correction is complete in the working tree, pending owner review. The nine product documents remain draft pending validation.
- IP-004 — Product Requirements Validation is pending owner review.
- Application implementation has not started. Explicit owner authorization is required before implementation.

## Product requirements

- Read [approved product decisions PD-001–PD-015](docs/project/decision-register.md#approved-product-decisions) for Stage 01 scope.
- Use the [PRD](docs/product/prd.md) for scope and catalog, the [SRS](docs/product/srs.md) for normative requirements and the [Acceptance Criteria](docs/product/acceptance-criteria.md) for expected evidence. The product documents are DRAFT — PENDING VALIDATION.
- Preserve feature IDs and release assignments. Trace requirements to their sources, verification methods and acceptance criteria in the [Requirements Traceability Matrix](docs/product/requirements-traceability-matrix.md). Link applicable stories, rules, flows and screens. Record exceptions and gaps.
- Keep proposals and pending questions distinct from approved scope. Owner validation in IP-004 is pending.

## Codex CLI
- Use Codex CLI as the current development assistant interface.
- Use the read-only sandbox for analysis tasks and the workspace-write sandbox for approved editing tasks.
- Obtain human approval before expanding task scope and human review before committing or merging changes.
- Never push automatically to remote repositories.

## Working rules
- Follow the current issue, acceptance criteria and approved scope. Ask about contradictions or missing requirements; do not silently invent product behavior.
- Prefer a modular monolith, explicit boundaries, simple solutions and typed Python. Do not introduce dependencies or architectural changes without justification and approval where material.
- Never commit secrets, tokens, real credentials or sensitive logs. Use synthetic fixtures. Do not probe external networks without authorization; test with controlled targets.
- Preserve workspace isolation, bounded retries, idempotency and SSRF defenses. Do not weaken security or tests to make a task pass.
- Inspect existing files before editing; preserve unrelated changes. Keep diffs focused. Do not push, merge, deploy or perform destructive operations without explicit authorization.
- Write code, comments and repository documentation in English. Discuss work with the owner in Russian unless requested otherwise.
- Run relevant checks once tooling exists. Report exact commands, outcomes, skipped checks and blockers. Never claim unrun tests passed.
- Do not assume dependency versions or verification commands exist before setup. Update docs with behavioral changes.

## Task completion report
Summarize changes, affected files, requirement IDs, tests run and results, remaining risks and suggested next step. Follow the [development workflow](docs/development/workflow.md).
