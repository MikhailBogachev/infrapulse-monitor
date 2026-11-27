FROM ghcr.io/astral-sh/uv:0.11.19 AS uv
FROM python:3.13.12-slim-bookworm AS base

ENV PYTHONUNBUFFERED=1 UV_PYTHON_DOWNLOADS=never PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY --from=uv /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
COPY backend/src backend/src
RUN groupadd --gid 10001 infrapulse \
    && useradd --uid 10001 --gid 10001 --no-create-home infrapulse \
    && install -d -o infrapulse -g infrapulse /state /locks \
    && touch /state/.initialized /locks/.initialized \
    && chown infrapulse:infrapulse /state/.initialized /locks/.initialized

FROM base AS spike-runner
RUN uv sync --locked --no-editable
ENV PYTHONDONTWRITEBYTECODE=1
USER 10001:10001

FROM base AS runtime
RUN uv sync --locked --no-dev --no-editable
COPY alembic.ini ./
COPY backend/migrations backend/migrations
USER 10001:10001
CMD ["python", "-m", "infrapulse"]
