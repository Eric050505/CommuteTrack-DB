from fastapi.testclient import TestClient
from ..app.main import app

client = TestClient(app)


def test_create_line():
    response = client.post("/lines/", json={"name": "Line 1"})
    assert response.status_code == 200
    assert response.json()["name"] == "Line 1"


def test_read_line():
    response = client.get("/lines/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

# 添加站点和乘车的测试
