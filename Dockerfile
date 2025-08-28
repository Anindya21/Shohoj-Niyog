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
RUN uv venv /app/.venv \
    && uv pip install -e . --no-cache-dir \
    && uv pip install gunicorn --no-cache-dir

# 2nd stage: Runtime
FROM python:3.11.9-slim

WORKDIR /app

# Copy installed venv from builder
COPY --from=builder /app/.venv /app/.venv

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy project files
COPY . .

# Collect Django static files (ignore failure)
RUN python backend/manage.py collectstatic --noinput || true

RUN which gunicorn && gunicorn --version

EXPOSE 8000

# Run Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
