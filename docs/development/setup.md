# Development environment

IP-007 implements the executable Stage 04 foundation for F-012 and exercises AC-055–AC-057. See the [approved deployment design](../architecture/deployment-design.md) and [technical spike results](technical-spikes.md).

## Prerequisites

| Tool | Reference version |
|---|---|
| Python | CPython 3.13.12. The package requires Python 3.13. |
| uv | 0.11.19 |
| Node and npm | Node 22.22.2 and npm 10.9.7 in the build image. Local Node 20.20.2 and npm 10.8.2 also run the locked frontend toolchain. |
| Docker | Docker Engine 28.4.0 and Compose v2.39.4 were used through Docker Desktop 4.47.0 on Apple Silicon. |
| Shell tools | Make, Bash, curl and Python 3 for development scripts. |

Use Docker Desktop on macOS for development. Use native Linux Docker Engine for production verification under AD-013. The default Compose project is a loopback-bound development foundation. Its workers have an internal control network and no outbound check or notification transports. Production Linux namespace and host policy provisioning, provider policy, secret rotation, TLS and supported deployment evidence remain acceptance work. The [deployment design](../architecture/deployment-design.md#restricted-egress) specifies their requirements.

The manifests pin direct dependencies and the lockfiles pin their resolved trees. Python development uses the root `.venv`. npm uses the frontend-local `node_modules`. Build and infrastructure images use exact release tags.

| Image | Version tag |
|---|---|
| Python | `python:3.13.12-slim-bookworm` |
| uv | `ghcr.io/astral-sh/uv:0.11.19` |
| Node | `node:22.22.2-bookworm-slim` |
| Nginx | `nginx:1.28.3-alpine` |
| PostgreSQL | `postgres:17.9-bookworm` |
| RabbitMQ | `rabbitmq:4.2.5` |
| Redis | `redis:8.6.2-alpine` |
| Browser fixture | Node build image with the Playwright 1.58.2 locked Chromium binary and its Debian runtime dependencies. |

## Start and stop

Run from the repository root.

```sh
cp .env.example .env
make install
make up
make smoke
make down
```

Open <http://127.0.0.1:8080/>. The placeholder fetches `/health/live` through Nginx. `/health/ready` requires PostgreSQL at the Alembic head and authenticated Redis. Only Nginx publishes a port. It returns the static SPA fallback for client routes and keeps API and health responses intact.

`make up` creates missing local credentials with `make secrets`, builds the two images and starts Compose. The one-shot `migrate` service locks migrations, upgrades the database using its own database role and declares the smoke queue topology. API and workers use the restricted runtime database role. RabbitMQ uses one generated credential for the local smoke stack. PostgreSQL, RabbitMQ, Beat and execution-lock files each use dedicated local volumes. Beat and the control worker run in one scheduler service under process supervision. The check worker uses two prefork children in one container. Shutdown signals let workers finish in-flight work within the Compose grace period. The host-local execution-lock volume is mounted in the API and check worker for future guarded execution.

Use a dedicated project and credential directory for experiments. Keep both the port and the base URL aligned when overriding them.

```sh
export COMPOSE_PROJECT_NAME=infrapulse-ip007
export INFRAPULSE_PORT=18087
export INFRAPULSE_BASE_URL=http://127.0.0.1:18087
export INFRAPULSE_SECRETS_DIR=./.secrets/ip007
make up
```

`make down` retains volumes. Retain the associated secret files while retaining these volumes. The secret directory is private on the host. Generated files are readable by the specific unprivileged services that receive each read-only mount. Initial role provisioning runs only on an empty PostgreSQL volume.

## Developer commands

| Command | Purpose |
|---|---|
| `make install` | Install from `uv.lock` and `frontend/package-lock.json`. |
| `make build` | Build the backend and Nginx images and produce the local frontend bundle. |
| `make format` | Apply Ruff lint fixes and Python formatting. |
| `make lint typecheck` | Check Ruff, ESLint, mypy and TypeScript. |
| `make test test-integration` | Run backend and frontend unit tests and a disposable PostgreSQL Testcontainers test. |
| `make migrate` | Re-run the one-shot migration and queue declaration against the selected Compose project. |
| `make smoke browser-container` | Verify Nginx, health, each Celery lane's database access and the compiled SPA in Chromium. The browser image installs its dependencies from the lockfile. |
| `make browser` | Run Playwright on the host after `npm --prefix frontend exec -- playwright install chromium`. |
| `make spike-runner` | Build the image with isolated experiment dependencies. |
| `npm --prefix frontend run dev` | Serve the Vite client with an API proxy to Nginx on local port 8080. |

## CI

[GitHub Actions](../../.github/workflows/ci.yml) runs on pull requests and pushes to main with read-only repository permissions and SHA-pinned actions. The backend and frontend jobs verify locked installations, lint, types and tests. Integration validates Compose, builds and starts the stack, runs migrations, checks browser and broker integration and runs the disposable PostgreSQL, RabbitMQ, HTTPX and execution-guard experiments. The Linux egress job runs the synthetic host-routing harness twice in fresh private namespaces. The separate Linux Compose topology job exercises the approved bridge layout and prefork worker with controlled targets. All five jobs passed in the [approved CI run](technical-spikes.md#approved-ci-evidence). The owner verified [main branch protection](workflow.md#main-branch-protection).

## Troubleshooting

| Symptom | Check |
|---|---|
| Docker SDK cannot find Docker Desktop | Set `DOCKER_HOST="$(docker context inspect desktop-linux --format '{{.Endpoints.docker.Host}}')"` for the Testcontainers command. |
| Buildx cannot write its activity file in a restricted shell | Point `BUILDX_CONFIG` at a writable workspace directory. uv, npm and Playwright caches can likewise use workspace-local directories. |
| Nginx responds but readiness is 503 | Check `docker compose ps -a` and the migration status. Verify PostgreSQL and Redis before restarting the API. Inspect individual service logs with care because infrastructure images have their own log configuration. |
| New database roles are missing | Confirm the selected volume was initialized with the current project and matching secret files. Use a fresh project name to verify empty-volume initialization. |
| Chromium launch fails due to host permissions | Use `make browser-container` with the running Compose project. It reaches Nginx through the private ingress bridge. |
| Compose cannot allocate the local port | Choose an unused `INFRAPULSE_PORT` and set `INFRAPULSE_BASE_URL` for the host smoke check. |
