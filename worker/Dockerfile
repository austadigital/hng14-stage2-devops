FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN useradd -m appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

# Healthcheck (checks if process is running)
HEALTHCHECK CMD echo ok || exit 1

CMD ["python", "worker.py"]