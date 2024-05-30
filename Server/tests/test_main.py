from fastapi.testclient import TestClient
from ..APP.APIs import app

client = TestClient(app)


def test_create_line():
    response = client.post("/lines/", json={"name": "Line 1"})
    assert response.status_code == 200
    assert response.json()["name"] == "Line 1"


def test_read_line():
    response = client.get("/lines/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
