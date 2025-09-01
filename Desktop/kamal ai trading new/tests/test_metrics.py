import os
from fastapi.testclient import TestClient
from services.kill_switch import app

def test_metrics_endpoint():
    os.environ["KILL_SWITCH_TOKEN"] = "TEST123"
    client = TestClient(app)

    # Just call /metrics
    r = client.get("/metrics")
    assert r.status_code == 200
    body = r.text
    assert "kamal_system_enabled" in body
