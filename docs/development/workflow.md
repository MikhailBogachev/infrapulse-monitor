# Development Workflow
ID: IP-DOC-005 | Version: 1.0 | Status: Approved principles

For tasks that change the repository, use GitHub Flow with an issue, a focused branch, task-specific checks, a pull request and human review. Main must remain releasable. Use Conventional Commits such as `feat(auth): implement JWT authentication`.

Board: Backlog → Ready → In Progress → Review → Testing → Done. An issue is Ready when scope, dependencies and acceptance criteria are clear.

## Lean Development workflow

Task → Implementation → Self-validation → Owner Review → Commit → Pull Request → Merge.

1. Define one complete outcome, its scope and its acceptance criteria in the task.
2. Codex implements and self-validates the outcome in one session, including correction and rechecking of in-scope defects. Group small corrections within the task. Reopen previously accepted areas when there is evidence of regression.
3. Report concise evidence and unresolved findings for owner review. Use independent review as needed for material architectural, security-sensitive or release-critical changes. Obtain owner approval for material product or architecture decisions.
4. Commit after owner review using Conventional Commits. Present the reviewed change through a pull request. Merge requires the applicable automated tests and CI checks to pass, plus human review and explicit authorization.

CRITICAL and material HIGH defects block acceptance. Fix MEDIUM defects within the task when scope permits and document those requiring material expansion for owner review. LOW defects and optional improvements do not block acceptance. Use [AGENTS.md](../../AGENTS.md) for standing instructions and keep task prompts focused on the outcome.

## Main branch protection

Changes to `main` must go through a pull request. Resolve review threads, bring the PR branch up to date with `main` and pass all required CI checks before merging. Force pushes and deletion of `main` are prohibited. GitHub requires zero approving reviews by design for solo development. Manual Owner Approval remains required by the project workflow.

**Branch Protection — PASS.** On 2026-11-28 the owner verified the configuration and effective rules for `main` using the GitHub REST API.

| Field | Verified value |
|---|---|
| Repository | `MikhailBogachev/infrapulse-monitor` |
| Ruleset | [main-protection (28282585)](https://github.com/MikhailBogachev/infrapulse-monitor/settings/rules/28282585) |
| Enforcement | `active` |
| Target | `~DEFAULT_BRANCH` |
| Effective protected branch | `main` |
| Bypass actors | None |
| Active rules | `non_fast_forward`, `pull_request`, `required_status_checks`, `deletion` |
| Required approving review count | `0` |
| Required review thread resolution | `true` |
| Require code owner review | `false` |
| Require last push approval | `false` |
| Dismiss stale reviews on push | `false` |
| Require extra approval for unattributed changes | `true` |
| Allowed merge methods | `merge`, `squash`, `rebase` |
| Required status checks | `backend`, `frontend`, `integration`, `linux-compose-topology`, `linux-egress-fixture` |
| Required status check source | `integration_id` `15368` for all five checks |
| Strict required status checks policy | `true` |

The owner used these API endpoints.

- `GET /repos/MikhailBogachev/infrapulse-monitor/rulesets/28282585`
- `GET /repos/MikhailBogachev/infrapulse-monitor/rules/branches/main`

## Codex CLI workflow

- Codex CLI is the current development assistant interface. Repository documentation is the primary source of project context.
- Use the read-only sandbox for analysis tasks and the workspace-write sandbox for approved editing tasks.
- Obtain human approval before expanding task scope.
- Obtain human review before committing or merging changes.
- Never push automatically to remote repositories.

## Task template
Task ID; title; context; objective; functional requirements; technical requirements; scope; out of scope; acceptance criteria; testing; documentation; deliverables; verification commands.

## Definition of Done

### Analysis and read-only tasks

- The report addresses the task and its acceptance criteria, cites evidence and records unresolved findings.
- A human reviews and accepts the report. Acceptance may occur without repository changes, commits or a pull request.

### Documentation tasks

- The documentation meets the acceptance criteria and passes relevant consistency checks and local link validation.
- Owner review precedes the commit. The pull request records the reviewed change and the applicable verification evidence.

### Implementation tasks

- Requirements and acceptance criteria satisfied.
- Relevant unit and integration tests written and passed.
- Ruff and mypy checks passed when configured.
- Authorization and security reviewed.
- Documentation updated.
- CI passed; human review completed; PR merged into main.

## Review discipline
Record material decisions as ADRs with context, options, decision and consequences. Do not treat a proposed ADR as approved. Report test evidence and unresolved issues. [D-010](../project/decision-register.md#d-010) requires GitHub Actions for MVP CI. The [setup guide](setup.md) documents the Stage 04 pipeline and verification commands.
