# ---- Build Stage ----
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies in isolated user directory
COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt


# ---- Final Stage ----
FROM python:3.11-slim

WORKDIR /app

# Create non-root user (security requirement)
RUN useradd -m appuser

# Copy installed Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application source code
COPY . .

# Ensure installed packages are found
ENV PATH=/home/appuser/.local/bin:$PATH

# Switch to non-root user
USER appuser

# Healthcheck (uses wget so no extra packages needed)
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD wget -qO- http://localhost:8000/health || exit 1

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]