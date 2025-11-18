"""
Infrastructure API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.core.simulator import simulator_manager

router = APIRouter()


@router.get("/status")
async def get_infrastructure_status() -> Dict[str, Any]:
    detailed = simulator_manager.get_detailed_status()
    if "error" in detailed:
        raise HTTPException(status_code=500, detail=detailed["error"])
    return detailed.get("infrastructure", {})


@router.post("/{component_key}/maintain")
async def perform_maintenance(component_key: str) -> Dict[str, Any]:
    module = simulator_manager.get_module("infrastructure")
    if not module:
        raise HTTPException(status_code=503, detail="Simulator not running")
    try:
        # prioritize and perform maintenance for the specific component
        current_day = 0.0
        if simulator_manager.simulator:
            current_day = simulator_manager.simulator.engine.clock.get_current_day()
        success = module.perform_maintenance(component_key, current_day=current_day)
        return {"success": success, "component": component_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
