"""
Demo scenarios endpoints
"""
from fastapi import APIRouter
from typing import Dict

router = APIRouter()


@router.post("/{scenario_id}/start")
async def start_scenario(scenario_id: str) -> Dict[str, str]:
    # TODO: implement real scenarios logic
    return {"status": "started", "scenario": scenario_id}
