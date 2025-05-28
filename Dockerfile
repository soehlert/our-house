FROM python:3.13-slim AS builder

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install uv

# Copy UV files first (better caching)
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

FROM python:3.13-slim

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

RUN pip install --upgrade pip && pip install uv

COPY --from=builder /app/.venv /app/.venv

WORKDIR /app

COPY --chown=appuser:appuser . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir -p /app/media /app/staticfiles && \
    chown -R appuser:appuser /app/media /app/staticfiles

RUN uv run python manage.py collectstatic --noinput

USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "housetracker.wsgi:application"]
