# Risk Register
ID: IP-DOC-003 | Version: 1.0 | Status: Active

All risks initially open. H = high, M = medium, L = low. Owner reviews at each stage gate; proposed mitigations are not implemented controls.

| ID | Risk | Likelihood / impact | Mitigation / verification | Responsible role |
|---|---|---|---|---|
| R-01 | Scope creep | H/H | Release boundaries; change approval | Product owner |
| R-02 | SSRF / network abuse | H/H | Validate resolved destinations and redirects, prevent DNS rebinding, enforce egress restrictions; adversarial tests | Backend |
| R-03 | Duplicate tasks | H/H | Stable execution IDs, DB uniqueness, concurrent delivery tests | Backend |
| R-04 | Lost tasks | M/H | Define ack and publish semantics; evaluate transactional outbox; broker failure tests | Backend |
| R-05 | False incidents | H/M | Failure/recovery thresholds; ordered state transitions | Backend |
| R-06 | History growth | H/H | Retention, indexes, capacity tests; evaluate partitioning | Backend |
| R-07 | Provider outage | H/M | Timeouts, bounded retry, rate limits, failure visibility | Backend |
| R-08 | AI-generated defects | H/H | Small PRs, human review, tests, no unverified claims | Owner |
| R-09 | Frontend effort | H/M | Reusable components and limited MVP screens | Frontend |
| R-10 | Naming conflict | H/M | Working name only; clearance or rename before public branding | Owner |
| R-11 | Tenant data leakage | M/H | Workspace-scoped authorization and cross-tenant tests | Backend |
| R-12 | Public demo abuse | H/H | Controlled targets, quotas, isolated demo, no visitor-supplied secrets | Operations |
| R-13 | Dependency/concurrency mismatch | M/H | Validate Python and Celery execution model; pin versions | Backend |
| R-14 | Credential exposure | M/H | Secret handling, redaction, secret scanning | Operations |

Roles are responsibilities of the solo developer, not separate staff. Review residual risk and evidence before release.
