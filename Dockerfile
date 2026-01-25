FROM ghcr.io/astral-sh/uv:latest AS uv

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_CACHE_DIR=/var/cache/uv \
    PATH="/app/.venv/bin:/usr/local/bin:${PATH}"

COPY --from=uv /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["sh", "-c", "if [ \"$DEBUG\" = \"1\" ] || [ \"$DEBUG\" = \"true\" ] || [ \"$DEBUG\" = \"True\" ]; then exec uv run uvicorn app:app --host 0.0.0.0 --port 8000 --reload; else exec uv run uvicorn app:app --host 0.0.0.0 --port 8000; fi"]
