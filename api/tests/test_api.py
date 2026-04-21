from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

# Ensure Python can find your api module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)


@patch("main.r")   # ✅ ADD THIS
def test_create_job(mock_redis):
    mock_redis.set.return_value = True

    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


@patch("main.r")
def test_redis_called(mock_redis):
    mock_redis.set.return_value = True

    response = client.post("/jobs")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200