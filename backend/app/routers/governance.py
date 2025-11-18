"""
Governance API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.core.simulator import simulator_manager

router = APIRouter()


@router.get("/status")
async def get_governance_status() -> Dict[str, Any]:
    detailed = simulator_manager.get_detailed_status()
    if "error" in detailed:
        raise HTTPException(status_code=500, detail=detailed["error"])
    return detailed.get("governance", {})


@router.post("/proposals")
async def create_proposal(title: str, description: str, proposer: str = "Citizen"):
    module = simulator_manager.get_module("governance")
    if not module:
        raise HTTPException(status_code=503, detail="Simulator not running")
    pid = module.create_proposal(title, description, proposer)
    return {"proposal_id": pid}


@router.post("/proposals/{proposal_id}/vote")
async def vote(proposal_id: str, vote_for: bool = True, votes: int = 1):
    module = simulator_manager.get_module("governance")
    if not module:
        raise HTTPException(status_code=503, detail="Simulator not running")
    module.vote(proposal_id, vote_for, votes)
    return {"ok": True}
