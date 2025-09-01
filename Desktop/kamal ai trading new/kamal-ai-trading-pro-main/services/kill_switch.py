
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import os

app = FastAPI(title="Kamal AI Trading - Control Service")

# simple in-memory state
_enabled = True

# metrics
ORDERS_PUBLISHED = Counter("kamal_orders_published_total", "Total orders published")
AGENT_DECISIONS = Counter("kamal_agent_decisions_total", "Total decisions made")
SYSTEM_ENABLED = Gauge("kamal_system_enabled", "System is enabled (1) or disabled (0)")

@app.on_event("startup")
def startup():
    SYSTEM_ENABLED.set(1 if _enabled else 0)

@app.get("/health", response_class=PlainTextResponse)
def health():
    return "ok"

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

def _auth(token: str | None):
    expected = os.getenv("KILL_SWITCH_TOKEN", "")
    return expected and token == expected

@app.post("/kill")
def kill(x_token: str | None = Header(None)):
    global _enabled
    if not _auth(x_token):
        raise HTTPException(status_code=403, detail="invalid token")
    _enabled = False
    SYSTEM_ENABLED.set(0)
    return {"status": "killed"}

@app.post("/revive")
def revive(x_token: str | None = Header(None)):
    global _enabled
    if not _auth(x_token):
        raise HTTPException(status_code=403, detail="invalid token")
    _enabled = True
    SYSTEM_ENABLED.set(1)
    return {"status": "revived"}
