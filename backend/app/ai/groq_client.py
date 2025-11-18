"""
Groq AI client wrapper for AEON
"""
from typing import Dict, Any, Optional
import json
from loguru import logger

try:
    from groq import Groq  # type: ignore
except Exception:
    Groq = None  # type: ignore

from app.core.config import settings


def ai_available() -> bool:
    return bool(Groq) and bool(settings.GROQ_API_KEY)


def _build_prompt(city_status: Dict[str, Any], question: Optional[str] = None, extra: Optional[Dict[str, Any]] = None) -> str:
    summary = {
        "time": city_status.get("time", {}),
        "infrastructure": city_status.get("infrastructure", {}),
        "public_services": city_status.get("public_services", {}),
        "citizen_wellbeing": city_status.get("citizen_wellbeing", {}),
        "governance": city_status.get("governance", {}),
        "events": city_status.get("events", [])[:10],
    }
    q = question or "Provide prioritized operational recommendations for the next day."
    instructions = (
        "You are an AI advisor for a municipal operations center. "
        "Analyze the city status and return a concise JSON with keys: "
        "analysis (string) and recommendations (array of {action, priority}). "
        "Priorities: high, medium, low. Keep it practical and specific."
    )
    return (
        f"{instructions}\nCityStatus:\n{json.dumps(summary)}\nQuestion: {q}\n"
        "Return ONLY JSON matching schema: {\"analysis\": str, \"recommendations\": [{\"action\": str, \"priority\": str}]}"
    )


def analyze_city_status(city_status: Dict[str, Any], question: Optional[str] = None, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not ai_available():
        logger.warning("Groq not configured; returning placeholder analysis.")
        return {
            "analysis": "Groq not configured. This is a placeholder analysis.",
            "recommendations": [
                {"action": "Schedule preventive maintenance on critical bridges", "priority": "high"},
                {"action": "Boost waste collection routes in hotspots", "priority": "medium"},
            ],
            "provider": "placeholder",
        }

    client = Groq(api_key=settings.GROQ_API_KEY)
    prompt = _build_prompt(city_status, question, extra)

    try:
        completion = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a concise municipal operations AI."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=600,
        )
        text = completion.choices[0].message.content if completion.choices else "{}"
        try:
            data = json.loads(text)
        except Exception:
            logger.debug("Non-JSON response from Groq; wrapping as analysis text.")
            data = {"analysis": text, "recommendations": []}
        data["provider"] = "groq"
        return data
    except Exception as e:
        logger.error(f"Groq analyze error: {e}")
        return {
            "analysis": f"Groq error: {e}",
            "recommendations": [],
            "provider": "groq",
            "error": str(e),
        }
