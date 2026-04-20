import pytest
from fastapi.testclient import TestClient
from nexustask.interfaces.api.main import app
import uuid

from nexustask.config import settings
settings.TESTING = True

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "10.4.2"}

def test_create_task():
    with TestClient(app) as client:
        payload = {
            "title": "My first enterprise task",
            "project_id": str(uuid.uuid4())
        }
        response = client.post("/api/v1/tasks", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "accepted"
