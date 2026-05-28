import json
import logging
import os
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
    def __init__(self, name: str, role: str, model: str | None = None):
        self.name = name
        self.role = role

        # Support remote Ollama (e.g. DGX or another machine)
        # Set OLLAMA_HOST=http://100.68.217.72:11434 before starting the backend
        ollama_host = os.getenv("OLLAMA_HOST")
        if ollama_host:
            os.environ["OLLAMA_HOST"] = ollama_host  # ollama client reads this

        # Model can come from env var or parameter (useful when switching between laptop and DGX)
        self.model = model or os.getenv("OLLAMA_MODEL", "gemma3:4b")

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
        """
        Queries the local/remote Ollama model to produce a structured, auditable decision.
        Optimized for strong models like Qwen3.5, DeepSeek-R1, Llama4, etc.
        """
        context_text = ""
        for page in context_pages:
            content = self.read_wiki(page)
            context_text += f"\n--- {page}.md ---\n{content}\n"

        # Strong prompt optimized for Qwen3.5 / high-capability models
        prompt = f"""You are the {self.name} for the AEON Mars Colony.

ROLE: {self.role}

You must make a high-stakes decision under strict operational constraints. Your reasoning will be reviewed by human experts and must be transparent, logical, and directly grounded in the provided Standard Operating Procedures.

=== CURRENT SITUATION ===
{situation}

=== RELEVANT STANDARD OPERATING PROCEDURES (LLMWiki) ===
{context_text}

=== INSTRUCTIONS ===
1. Read the Emergency Priorities document first — it is the ultimate decision hierarchy.
2. Analyze the situation using ONLY the information in the provided wiki pages.
3. Produce a single, clear executive decision.
4. Your reasoning must be explicit, step-by-step, and cite specific sections from the wiki pages.
5. Explicitly state what alternatives you considered and why you rejected them.
6. Be conservative when human life is at risk.

Respond **ONLY** with a valid JSON object in this exact schema (no markdown, no extra text):

{{
    "decision": "Clear, actionable decision in one sentence",
    "reasoning_chain": "Detailed step-by-step logical reasoning (3-8 sentences). Reference specific principles from the wiki pages.",
    "cited_wiki_pages": ["ExactPageName1", "ExactPageName2"],
    "rejected_alternatives": "What other options you considered and why they were inferior or violated priorities.",
    "confidence": 0.0
}}

The "confidence" field must be a number between 0.0 and 1.0 reflecting how well the decision is supported by the SOPs."""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                format="json",
                options={
                    "temperature": 0.2,   # Low temperature for more deterministic, serious decisions
                    "top_p": 0.9,
                }
            )

            raw_content = response["message"]["content"]
            result = json.loads(raw_content)
            return result

        except json.JSONDecodeError:
            logger.warning("Model did not return valid JSON. Attempting extraction...")
            # Fallback: try to extract JSON from the response
            try:
                import re
                match = re.search(r"\{.*\}", raw_content, re.DOTALL)
                if match:
                    result = json.loads(match.group(0))
                    return result
            except Exception:
                pass
            logger.error(f"Failed to parse decision from model. Raw output:\n{raw_content}")
            return None

        except Exception as e:
            logger.error(f"Error calling Ollama model '{self.model}': {e}")
            return None
