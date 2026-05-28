import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

import ollama
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentResponse(BaseModel):
    decision: str
    reasoning_chain: str
    cited_wiki_pages: List[str]
    rejected_alternatives: str
    confidence: float


class AeonAgent:
    def __init__(self, name: str, role: str, model: str = "gemma3:4b"):
        self.name = name
        self.role = role
        self.model = model

        # Robust path resolution: from backend/app/core/agent.py → repo root / llmwiki/wiki
        self.wiki_dir = Path(__file__).resolve().parents[4] / "llmwiki" / "wiki"
        
    def read_wiki(self, page_name: str) -> str:
        """Reads a markdown file from the LLMWiki."""
        file_path = self.wiki_dir / f"{page_name}.md"
        try:
            return file_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return f"Wiki page {page_name} not found."

    def make_decision(self, situation: str, context_pages: List[str]) -> Optional[Dict[str, Any]]:
        """Queries Ollama to make a decision based on the situation and wiki context."""
        context_text = ""
        for page in context_pages:
            content = self.read_wiki(page)
            context_text += f"\n--- {page}.md ---\n{content}\n"
            
        prompt = f"""
You are the {self.name} Agent for the AEON Space Colony. Your role is: {self.role}.
You must make a critical decision based on the following situation and Standard Operating Procedures (SOPs).

SITUATION:
{situation}

RELEVANT WIKI PAGES (SOPs):
{context_text}

Respond ONLY with a valid JSON object matching this schema:
{{
    "decision": "Action to take",
    "reasoning_chain": "Step-by-step logic",
    "cited_wiki_pages": ["Page1", "Page2"],
    "rejected_alternatives": "What you considered but didn't do",
    "confidence": 0.95
}}
"""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format='json'
            )
            # Parse the JSON response
            result = json.loads(response['message']['content'])
            return result
        except Exception as e:
            logger.error(f"Error in {self.name} decision making: {e}")
            return None
