from fastapi import FastAPI, HTTPException
import redis
import uuid
import os

app = FastAPI()

# =========================
# CONFIGURATION
# =========================
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# =========================
# REDIS CLIENT
# =========================


def get_redis():
    """
    Returns Redis connection.
    Wrapped in a function to make testing easier (can be mocked cleanly).
    """
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True
    )


# =========================
# ROUTES
# =========================

@app.post("/jobs")
def create_job():
    try:
        r = get_redis()

        job_id = str(uuid.uuid4())

        # Add job to queue
        r.lpush("jobs", job_id)

        # Store job status
        r.hset(f"job:{job_id}", mapping={"status": "queued"})

        return {
            "job_id": job_id,
            "status": "queued"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        r = get_redis()

        status = r.hget(f"job:{job_id}", "status")

        if status is None:
            raise HTTPException(status_code=404, detail="Job not found")

        return {
            "job_id": job_id,
            "status": status
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok"}
