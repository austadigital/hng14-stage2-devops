import redis
import time
import os

# ✅ FIX: Use environment variables instead of hardcoded localhost
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Redis connection (safe for Docker)
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

print("Worker started...")

while True:
    try:
        # ✅ FIX: safely wait for job (handles empty queue automatically)
        job = r.brpop("jobs", timeout=5)

        if not job:
            continue  # No job in queue, keep waiting safely

        _, job_id = job
        print(f"Processing job: {job_id}")

        # ✅ FIX: update status to processing
        r.hset(f"job:{job_id}", "status", "processing")

        try:
            # Simulate work
            time.sleep(3)

            # ✅ FIX: mark job as completed
            r.hset(f"job:{job_id}", "status", "completed")
            print(f"Completed job: {job_id}")

        except Exception as job_error:
            # ✅ FIX: handle job failure safely
            r.hset(f"job:{job_id}", "status", "failed")
            print(f"Job failed: {job_id} - {job_error}")

    except Exception as e:
        # ✅ FIX: prevent worker crash loop
        print(f"Worker error: {e}")
        time.sleep(2)

