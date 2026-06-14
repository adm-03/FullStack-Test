FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-editable


FROM python:3.12-slim

WORKDIR /app

RUN groupadd --system app && useradd --system --gid app --home-dir /app app

ENV PYTHONPATH=src \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=builder --chown=app:app /app/.venv /app/.venv

COPY --chown=app:app ./src ./src

#USER app

EXPOSE 8000

#CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]
CMD ["/app/.venv/bin/gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--chdir", "src"]
