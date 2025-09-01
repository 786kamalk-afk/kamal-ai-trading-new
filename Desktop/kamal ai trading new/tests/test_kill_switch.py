import os
from fastapi.testclient import TestClient
from services.kill_switch import app

def test_kill_switch_toggle():
    os.environ["KILL_SWITCH_TOKEN"] = "TEST123"
    client = TestClient(app)

    # Enable system
    r = client.post("/enable", headers={"Authorization": "Bearer TEST123"})
    assert r.status_code == 200
    assert r.json()["enabled"] is True

    # Kill system
    r = client.post("/kill", headers={"Authorization": "Bearer TEST123"})
    assert r.status_code == 200
    assert r.json()["enabled"] is False
