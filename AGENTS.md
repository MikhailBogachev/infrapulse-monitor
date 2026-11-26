# Instructions for coding agents

## Project context
Repository documentation is the primary source of project context. Before work, read the [charter](docs/project/charter.md), [roadmap](docs/project/roadmap.md), [risk register](docs/project/risk-register.md) and [glossary](docs/project/glossary.md). Read applicable approved product specifications and ADRs when present.

- Stage 00 — Project Initialization is approved and complete.
- Stage 01 — Product Discovery is in progress.
- Stage 02 — System Design is pending.
- IP-000 — Project Context Initialization is accepted.
- Application implementation has not started. Do not implement application code until the owner authorizes implementation tasks.

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
