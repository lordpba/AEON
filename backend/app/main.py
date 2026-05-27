from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
from typing import List, Dict, Any

from app.core.agent import AeonAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AEON: Autonomous Extraterrestrial Operations Network",
    description="PhD-level MAS Framework for Space Colony Governance using Ollama.",
    version="1.0.0"
)

# Allow React Frontend (Vite runs on 5173 by default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the AEON Core Agent
core_agent = AeonAgent(
    name="AEON Core", 
    role="Top-level executive coordinator. Resolves conflicts between lower-tier agents according to Emergency Priorities.",
    model="gemma4:e4b"  # Ensure gemma4:e4b is pulled in Ollama locally
)

class SituationRequest(BaseModel):
    situation: str
    context_pages: List[str]

@app.get("/")
def read_root():
    return {"status": "AEON MAS Backend is running (Offline Mode - Ollama)."}

@app.get("/api/v1/wiki")
def list_wiki_pages():
    """Returns a list of available markdown pages in the LLMWiki."""
    try:
        files = os.listdir(core_agent.wiki_dir)
        pages = [f.replace(".md", "") for f in files if f.endswith(".md")]
        return {"pages": pages}
    except Exception as e:
        logger.error(f"Error reading wiki directory: {e}")
        return {"pages": []}

@app.get("/api/v1/wiki/{page_name}")
def get_wiki_page(page_name: str):
    """Returns the markdown content of a specific wiki page."""
    content = core_agent.read_wiki(page_name)
    if "not found" in content:
        raise HTTPException(status_code=404, detail="Wiki page not found")
    return {"content": content}

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
