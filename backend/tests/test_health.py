from fastapi.testclient import TestClient

from src.main import app


def test_health_endpoint_returns_expected_shape(monkeypatch):
    monkeypatch.setattr("src.use_cases.health_check.check_postgres_connection", lambda: True)

    class FakeMongoAdapter:
        def ping(self):
            return True

        def close(self):
            return None

    monkeypatch.setattr("src.use_cases.health_check.MongoAdapter", FakeMongoAdapter)

    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "postgres": "ok", "mongodb": "ok"}
