UV ?= uv
COMPOSE ?= docker compose
SPIKE_COMPOSE = $(COMPOSE) -f compose.yaml -f spikes/compose.yaml --profile spike
PY = $(UV) run --locked
WEB = npm --prefix frontend
SECRETS_DIR ?= $(if $(INFRAPULSE_SECRETS_DIR),$(INFRAPULSE_SECRETS_DIR),.secrets)

.PHONY: install secrets config up down build format lint typecheck test test-integration migrate smoke browser spike-stack spike-postgres spike-rabbit spike-httpx spike-egress spike-guard spike-runner

install:
	$(UV) sync --locked
	$(WEB) ci

secrets:
	python3 scripts/setup_secrets.py "$(SECRETS_DIR)"

config:
	$(COMPOSE) config -q

up: secrets
	$(COMPOSE) up --build --wait --wait-timeout 150

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build api nginx
	$(WEB) run build

format:
	$(PY) ruff check --fix .
	$(PY) ruff format .

lint:
	$(PY) ruff check .
	$(PY) ruff format --check .
	$(WEB) run lint

typecheck:
	$(PY) mypy
	$(WEB) run typecheck

test:
	$(PY) pytest -m "not integration"
	$(WEB) test

test-integration:
	$(PY) pytest -m integration

migrate:
	$(COMPOSE) run --rm migrate

smoke:
	bash scripts/smoke.sh

browser:
	$(WEB) run e2e

spike-runner: secrets
	$(SPIKE_COMPOSE) build spike

spike-stack: test-integration smoke browser-container
	$(SPIKE_COMPOSE) run --rm --no-deps -T spike python /spikes/stack.py

spike-postgres:
	$(COMPOSE) exec -T postgres psql -X -v ON_ERROR_STOP=1 -U infrapulse_admin -d infrapulse < spikes/postgres.sql
	$(COMPOSE) exec -T postgres sh -s < spikes/postgres_locks.sh

spike-rabbit:
	$(COMPOSE) exec -T postgres psql -X -v ON_ERROR_STOP=1 -U infrapulse_admin -d infrapulse < spikes/rabbit_setup.sql
	$(SPIKE_COMPOSE) run --rm --no-deps -T spike python /spikes/rabbit.py

spike-httpx:
	$(SPIKE_COMPOSE) run --rm --no-deps -T spike pytest -q -s -p no:cacheprovider /spikes/test_transport.py

spike-guard:
	bash spikes/lock_identity.sh
	$(COMPOSE) exec -T postgres psql -X -v ON_ERROR_STOP=1 -U infrapulse_admin -d infrapulse < spikes/guard_setup.sql
	$(SPIKE_COMPOSE) run --rm --no-deps -T spike pytest -q -s -p no:cacheprovider /spikes/test_guard.py
	bash spikes/guard_lifecycle.sh $(SPIKE_COMPOSE)

spike-egress:
	unshare --mount --net -- bash spikes/egress.sh "$$(readlink /proc/self/ns/net)"

.PHONY: browser-container
browser-container:
	$(SPIKE_COMPOSE) build browser
	$(SPIKE_COMPOSE) run --rm --no-deps -T browser

.PHONY: spike-topology
spike-topology:
	bash spikes/topology.sh
