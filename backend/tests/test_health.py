from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_ok():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_consultations_rejects_missing_token():
    client = TestClient(app)
    response = client.post(
        "/api/consultations",
        json={"notes": "Patient presents with persistent cough for 5 days."},
    )
    assert response.status_code in (401, 403)
