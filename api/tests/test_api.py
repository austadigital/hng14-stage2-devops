from api.main import app
from unittest.mock import patch
from fastapi.testclient import TestClient
import sys
import os

# Ensure Python can find api module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = TestClient(app)


# ✅ FIX: patch get_redis (NOT r)
@patch("api.main.get_redis")
def test_create_job(mock_get_redis):
    mock_redis = mock_get_redis.return_value

    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = True

    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"


@patch("api.main.get_redis")
def test_redis_called(mock_get_redis):
    mock_redis = mock_get_redis.return_value

    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = True

    response = client.post("/jobs")

    assert response.status_code == 200

    # Optional: verify Redis calls
    mock_redis.lpush.assert_called_once()
    mock_redis.hset.assert_called_once()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
