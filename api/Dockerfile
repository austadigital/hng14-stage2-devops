# ---- Build Stage ----
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Final Stage ----
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

# Create non-root user
RUN useradd -m appuser

# Copy installed packages
COPY --from=builder /root/.local /home/appuser/.local

# Copy app files
COPY . .

ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

# Healthcheck (you MUST have /health route in FastAPI)
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]