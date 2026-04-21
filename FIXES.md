# FIXES REPORT

This document outlines all issues identified across the API, Frontend, and Worker services, including their impact and the fixes applied.> This report follows a strict audit checklist:
> - Hardcoded values ❌
> - Missing environment variables ❌
> - Wrong imports ❌
> - Broken logic ❌



---

# 🔧 API SERVICE (FastAPI)

## 1. File: api/main.py

### Line: 8

### Issue:

Redis connection is hardcoded to `localhost`.

### Why it's a problem:

In a containerized environment, `localhost` refers to the container itself, not the Redis service. This causes connection failures when deployed.

### Fix:

Replaced with environment variables:

* `REDIS_HOST`
* `REDIS_PORT`

---

## 2. File: api/main.py

### Line: 8

### Issue:

Redis client does not use `decode_responses=True`.

### Why it's a problem:

Redis returns byte strings, requiring manual decoding and increasing risk of runtime errors.

### Fix:

Enabled automatic decoding:
`decode_responses=True`

---

## 3. File: api/main.py

### Line: 1

### Issue:

Missing import for `HTTPException`.

### Why it's a problem:

Raising HTTP errors without importing will crash the application.

### Fix:

Added:
`from fastapi import HTTPException`

---

## 4. File: api/main.py

### Line: 13

### Issue:

Queue name is `"job"` (singular).

### Why it's a problem:

Misleading naming since multiple jobs are stored.

### Fix:

Renamed to `"jobs"` for consistency.

---

## 5. File: api/main.py

### Line: 19

### Issue:

Possible `None` value from Redis is not properly handled.

### Why it's a problem:

Calling `.decode()` on `None` will crash the application.

### Fix:

Added proper `None` check and removed manual decoding.

---

## 6. File: api/main.py

### Line: 20

### Issue:

Returns JSON error without HTTP status code.

### Why it's a problem:

Breaks REST API standards and makes debugging harder.

### Fix:

Replaced with:
`HTTPException(status_code=404, detail="Job not found")`

---

## 7. File: api/main.py

### Line: 11–14

### Issue:

No error handling for Redis operations.

### Why it's a problem:

Application crashes if Redis is unavailable.

### Fix:

Wrapped Redis operations in try/except and return HTTP 500 on failure.

---

## 8. File: api/main.py

### Line: 4

### Issue:

Unused import (`os`).

### Why it's a problem:

Reduces code clarity.

### Fix:

Used `os` to implement environment variables.

---

# 🌐 FRONTEND SERVICE (Node.js / Express)


## 9. File: frontend/app.js

### Line: 6

### Issue:
Backend API URL is hardcoded (`http://localhost:8000`).

### Why it's a problem:
Breaks in containerized environments where services communicate using service names instead of localhost.

### Fix:
Replaced with environment variable:
`process.env.API_URL`

---

## 10. File: frontend/app.js

### Line: 11–18

### Issue:
No proper error handling for `/submit` API request.

### Why it's a problem:
Frontend may fail silently or return unclear errors when backend is unavailable.

### Fix:
Wrapped axios request in try/catch and added proper error response handling.

---

## 11. File: frontend/app.js

### Line: 20–27

### Issue:
No proper error handling for `/status/:id` API request.

### Why it's a problem:
Backend failures or invalid job IDs return unhandled errors.

### Fix:
Added try/catch and structured error response handling.

---


## 12. File: frontend/views/index.html

### Line: 25

### Issue:
Hardcoded API route `/submit`.

### Why it's a problem:
Breaks in containerized environments where backend services communicate using service names or environment variables instead of hardcoded paths.

### Fix:
Use a configurable API base URL (e.g. environment variable or proxy setup).

---

## 13. File: frontend/views/index.html

### Line: 25–33

### Issue:
No error handling for the fetch request in `submitJob()`.

### Why it's a problem:
If the backend fails or returns an invalid response, `res.json()` executes without validation, causing crashes or unexpected behavior.

### Fix:
Added:
- `try/catch`
- `res.ok` validation before parsing JSON
- User-friendly error display

---

## 14. File: frontend/views/index.html

### Line: 26

### Issue:
JSON is parsed without validating response success.

### Why it's a problem:
If response is not valid JSON or request fails, the application crashes.

### Fix:
Only parse JSON after checking `res.ok`.

---

##  15. File: frontend/views/index.html

### Line: 34–41

### Issue:
No error handling for fetch request in `pollJob()`.

### Why it's a problem:
Backend failures or invalid job IDs break polling flow silently.

### Fix:
Added:
- `try/catch`
- `res.ok` validation
- Safe fallback UI update

---

## 16. File: frontend/views/index.html

### Line: 35

### Issue:
Response is parsed without validation.

### Why it's a problem:
Can crash if response is empty or invalid.

### Fix:
Validate response before calling `.json()`.

---

## 17. File: frontend/views/index.html

### Line: 38–40

### Issue:
Polling only stops when status is `"completed"`.

### Why it's a problem:
If status is `"failed"`, polling continues forever causing unnecessary API requests.

### Fix:
Updated condition to stop polling when status is:
- `"completed"`
- OR `"failed"`

---

## 18. File: frontend/views/index.html

### Line: 54

### Issue:
Job status is displayed in raw format.

### Why it's a problem:
Poor readability and user experience.

### Fix:
Use:

```js
status.toUpperCase()

# ⚙️ WORKER SERVICE

## 19. File: worker/worker.py

### Line: 6

### Issue:
Redis connection is hardcoded using:
r = redis.Redis(host="localhost", port=6379)

### Why it's a problem:
The worker cannot run in containerized environments where services communicate using service names instead of localhost.

### Fix:
Replaced hardcoded Redis connection with environment variables using os.getenv().

---

## 20. File: worker/worker.py

### Line: 6–9

### Issue:
No environment variable configuration for Redis.

### Why it's a problem:
Worker cannot adapt to different environments (development, staging, production).

### Fix:
Added:
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

---

## 21. File: worker/worker.py

### Line: 15–16

### Issue:
No explicit handling for empty job queue.

### Why it's a problem:
When no jobs are available, worker behavior is unclear and may cause unnecessary processing flow.

### Fix:
Added safe check:
if not job:
    continue

---

## 22. File: worker/worker.py

### Line: 8–12

### Issue:
No error handling during job processing.

### Why it's a problem:
A single failed job can crash the entire worker process.

### Fix:
Wrapped job processing logic inside try/except to ensure continuous execution.

---

## 23. File: worker/worker.py

### Line: 18

### Issue:
Manual decoding of Redis response using job_id.decode().

### Why it's a problem:
Unsafe and dependent on Redis response format, which may break in different environments.

### Fix:
Replaced manual decoding by using decode_responses=True in Redis client configuration.

---

## 24. File: worker/worker.py

### Line: 4

### Issue:
Unused import: signal.

### Why it's a problem:
Adds unnecessary clutter and is not used in the codebase.

### Fix:
Removed unused import to clean up the code.


---


---

# ✅ SUMMARY

All services were improved to:

- Remove hardcoded values and use environment variables
- Improve fault tolerance with proper error handling
- Ensure safe Redis interactions using decode_responses=True
- Prevent crashes from invalid or missing data
- Improve frontend resilience to API failures
- Ensure compatibility with containerized (Docker-based) environments
- Enhance code readability, consistency, and maintainability