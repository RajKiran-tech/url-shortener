
import pytest
from app.main import app

@pytest.fixture
def client():
    return app.test_client()

def test_shorten_url(client):
    res = client.post("/api/shorten", json={"url": "https://google.com"})
    assert res.status_code == 201
    assert "short_code" in res.get_json()

def test_invalid_url(client):
    res = client.post("/api/shorten", json={"url": "not-a-url"})
    assert res.status_code == 400

def test_redirect(client):
    res = client.post("/api/shorten", json={"url": "https://google.com"})
    short_code = res.get_json()["short_code"]
    redirect_res = client.get(f"/{short_code}")
    assert redirect_res.status_code == 302

def test_stats(client):
    res = client.post("/api/shorten", json={"url": "https://google.com"})
    short_code = res.get_json()["short_code"]
    _ = client.get(f"/{short_code}")
    stats_res = client.get(f"/api/stats/{short_code}")
    stats_data = stats_res.get_json()
    assert stats_data["clicks"] == 1
    assert "created_at" in stats_data
