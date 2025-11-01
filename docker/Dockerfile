FROM python:3.13-slim-bookworm AS builder

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    tzdata \
    redis-server \
    ca-certificates \
    build-essential \
    binutils \
    libproj-dev \
    gdal-bin \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | tee /etc/apt/trusted.gpg.d/pgdg.asc \
    && apt-get update

RUN apt-get install -y postgresql-client libpq5 mariadb-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /app/
COPY --from=ghcr.io/astral-sh/uv:0.5.4 /uv /uvx /bin/
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app/src

COPY ./pyproject.toml .
COPY ./uv.lock .

COPY ./src /app/src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]