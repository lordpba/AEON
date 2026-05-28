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
    description="Research platform for AI governance of Mars colonies under communication delay and human incapacitation. Local inference only.",
    version="0.1.0"
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
# Model and Ollama host can be controlled via environment variables:
#   $env:OLLAMA_MODEL = "qwen2.5:14b"
#   $env:OLLAMA_HOST  = "http://100.68.217.72:11434"
core_agent = AeonAgent(
    name="AEON Core",
    role="Top-level executive coordinator. Resolves conflicts between systems according to Emergency Priorities when communication with Earth is delayed or impossible.",
)

class SituationRequest(BaseModel):
    situation: str
    context_pages: List[str]

@app.get("/")
def read_root():
    return {"status": "AEON MAS Backend is running (Offline Mode - Ollama)."}

@app.get("/api/v1/wiki")
def list_wiki_pages():
    """Returns a list of available markdown pages in the LLMWiki (recursive, supports modular structure)."""
    try:
        pages = []
        for path in core_agent.wiki_dir.rglob("*.md"):
            if path.name != "README.md" and path.name != "00_INDEX.md":
                # Return relative path without extension for clarity (e.g. principles/Emergency_Priorities)
                relative = path.relative_to(core_agent.wiki_dir)
                pages.append(str(relative.with_suffix("")))
        pages.sort()
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
