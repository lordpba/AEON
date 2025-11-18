"""
Citizens API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.core.simulator import simulator_manager

router = APIRouter()


@router.get("/status")
async def get_citizen_wellbeing() -> Dict[str, Any]:
    detailed = simulator_manager.get_detailed_status()
    if "error" in detailed:
        raise HTTPException(status_code=500, detail=detailed["error"])
    return detailed.get("citizen_wellbeing", {})
