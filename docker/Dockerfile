# Stage 1: Build the application environment
FROM python:3.13-slim-bookworm AS builder

# Install system packages and Redis
RUN apt-get update && apt-get install -y \
    redis-server \
    ca-certificates \
    build-essential \
    binutils \
    libproj-dev \
    gdal-bin \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add PostgreSQL APT repository
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | tee /etc/apt/trusted.gpg.d/pgdg.asc \
    && apt-get update

# Install PostgreSQL client (latest available version, likely 16.x)
RUN apt-get install -y postgresql-client libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure the dynamic linker for libpq
RUN echo "/usr/lib/x86_64-linux-gnu" | tee /etc/ld.so.conf.d/libpq.conf && \
    ldconfig && \
    ldconfig -p | grep libpq


ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.5.4 /uv /uvx /bin/

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"

# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Install dependencies
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app/src

COPY ./pyproject.toml .
COPY ./uv.lock .

COPY ./src /app/src

# Sync the project
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]