from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Kamal AI Trading", version="1.0.0")

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    user = req.message.strip().lower()
    if "help" in user or "?" in user:
        reply = "Bhai, aaj ka plan: risk kam, clarity zyada. Symbol bhejo, mai data dekh ke idea dunga."
    else:
        reply = "Samjha! Thoda data share karo (symbol/timeframe). Mai turant plan banata hu."
    return {"reply": reply}
