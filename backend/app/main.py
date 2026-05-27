from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from typing import List, Dict, Any

from app.core.agent import AeonAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AEON: Autonomous Extraterrestrial Operations Network",
    description="PhD-level MAS Framework for Space Colony Governance using Ollama.",
    version="1.0.0"
)

# Initialize the AEON Core Agent
core_agent = AeonAgent(
    name="AEON Core", 
    role="Top-level executive coordinator. Resolves conflicts between lower-tier agents according to Emergency Priorities.",
    model="llama3"  # Ensure llama3 is pulled in Ollama locally
)

class SituationRequest(BaseModel):
    situation: str
    context_pages: List[str]

@app.get("/")
def read_root():
    return {"status": "AEON MAS Backend is running (Offline Mode - Ollama)."}

@app.post("/api/v1/decide")
def make_agent_decision(request: SituationRequest):
    """
    Endpoint for testing the Agent's decision-making capabilities using the LLMWiki.
    """
    decision = core_agent.make_decision(
        situation=request.situation,
        context_pages=request.context_pages
    )
    
    if not decision:
        raise HTTPException(status_code=500, detail="Agent failed to formulate a decision. Check Ollama connection.")
        
    return {"agent": core_agent.name, "response": decision}

# Placeholder for WebSocket Dashboard connection
@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket):
    await websocket.accept()
    await websocket.send_text("AEON Telemetry Stream Initialized.")
    # Implementation of real-time telemetry push goes here
