FROM python:3.12.0-alpine

WORKDIR /app
COPY . .
RUN addgroup -g 1000 -S app && adduser -u 1000 -S app -G app \
 && python -m venv venv \
 && source venv/bin/activate \
 && pip install --no-cache-dir .


FROM python:3.12.0-alpine
COPY --from=0 /etc/passwd /etc/group /etc/
COPY --from=0 --chown=1000:1000 /app/venv/ /app/venv/
USER app
WORKDIR /in
WORKDIR /out

LABEL org.opencontainers.image.authors="Calloway https://github.com/callowayproject"
LABEL org.opencontainers.image.base.name="docker.io/library/python:3.12.0-alpine"
LABEL org.opencontainers.image.description="A small command line tool to simplify releasing software by updating all version strings in your source code by the correct increment and optionally commit and tag the changes."
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/callowayproject/bump-my-version"
LABEL org.opencontainers.image.title="bump-my-version"
LABEL org.opencontainers.image.version="0.11.0"

ENTRYPOINT ["/app/venv/bin/bump-my-version"]
