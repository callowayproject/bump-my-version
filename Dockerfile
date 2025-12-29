FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.14-slim-bookworm

ARG USERNAME=app
ARG USER_UID=1000
ARG USER_GID=$USER_UID

LABEL com.github.actions.name="Bump My Version" \
    com.github.actions.description="Bump version of a project." \
    com.github.actions.icon="chevrons-up" \
    com.github.actions.color="blue" \
    maintainer="@coordt" \
    org.opencontainers.image.authors="Calloway Project https://github.com/callowayproject" \
    org.opencontainers.image.created=2025-12-29T11:58:47Z \
    org.opencontainers.image.url=https://github.com/callowayproject/bump-my-version \
    org.opencontainers.image.documentation=https://callowayproject.github.io/bump-my-version \
    org.opencontainers.image.source=https://github.com/callowayproject/bump-my-version \
    org.opencontainers.image.version=1.2.6 \
    org.opencontainers.image.licenses=MIT

# Add a non-root user and group
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

COPY --from=builder --chown=$USER_UID:$USER_GID /app /app
USER $USERNAME
WORKDIR /project

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["bump-my-version"]
