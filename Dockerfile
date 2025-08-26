FROM python:3.11.9-slim AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

WORKDIR /app

# Copy dependency files
COPY uv.lock pyproject.toml ./

# Install dependencies in a venv
RUN uv sync

# 2nd stage: Runtime
FROM python:3.11.9-slim

WORKDIR /app

# Copy installed venv from builder
COPY --from=builder /app/.venv .venv

ENV PATH="/app/.venv/bin:$PATH"

# Copy project files
COPY . .

# Collect Django static files (optional, skip if it fails)
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]