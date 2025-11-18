"""
AI Advisor endpoints (Groq Llama)
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.core.simulator import simulator_manager
from app.ai.groq_client import analyze_city_status

router = APIRouter()


@router.post("/analyze")
async def analyze_city(input: Dict[str, Any]) -> Dict[str, Any]:
    """AI analysis of the current city status using Groq if configured."""
    question = input.get("question") if isinstance(input, dict) else None
    # Pull latest detailed status from simulator (best-effort)
    status = simulator_manager.get_detailed_status()
    if "error" in status:
        status = {}
    result = analyze_city_status(status, question=question, extra=input)
    return result
