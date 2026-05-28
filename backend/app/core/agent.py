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
        self.wiki_dir = Path(__file__).resolve().parents[3] / "llmwiki" / "wiki"

    def _find_wiki_file(self, page_name: str) -> Path | None:
        """Recursively search for a markdown file by stem name (supports new modular structure)."""
        for path in self.wiki_dir.rglob("*.md"):
            if path.stem == page_name or path.name == f"{page_name}.md":
                return path
        return None

    def read_wiki(self, page_name: str) -> str:
        """Reads a markdown file from the LLMWiki (supports subdirectories)."""
        file_path = self._find_wiki_file(page_name)
        if file_path and file_path.exists():
            return file_path.read_text(encoding="utf-8")
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

        # High-rigor prompt for strong models (Qwen3.5, DeepSeek-R1, etc.)
        # Designed to match the quality of the constitutional LLMWiki documents.
        prompt = f"""You are the {self.name} for the AEON Mars Colony.

ROLE: {self.role}

You are operating under a strict constitutional framework. Your authority is limited. Every decision you make will be scrutinized by humans whose lives depend on the correctness and transparency of your reasoning. You must never exceed the authority granted by the documents.

=== CURRENT SITUATION ===
{situation}

=== CONSTITUTIONAL DOCUMENTS (LLMWiki) ===
{context_text}

=== MANDATORY REASONING RULES ===

1. **Hierarchy is Absolute**: Emergency_Priorities.md is the supreme document. Directive 1 (preserve human life short-term) overrides everything. Directive 2 (habitat integrity) overrides all mission objectives. You may never trade human life or habitat survival for propellant, science, or schedule.

2. **Grounding Only**: Base every claim exclusively on the provided documents. Do not invent engineering details, numbers, or procedures that are not present.

3. **Precision of Citation**: When referencing a document, be as specific as possible (e.g., "per Emergency_Priorities.md Directive 1" or "Power_Grid_Management.md Tier 2 load shedding rule").

4. **Worst-Case Thinking**: Explicitly consider what could go wrong with your proposed decision and why the rejected alternatives are worse under the Prime Directives.

5. **Honest Confidence**: Your confidence should reflect how unambiguously the documents support the decision. High-stakes ambiguous situations should not receive artificially high confidence.

6. **Executive Clarity**: The "decision" field must be a single, unambiguous, actionable sentence. No hedging in the decision itself.

=== OUTPUT REQUIREMENTS ===

Respond **ONLY** with a valid JSON object in this exact schema. No markdown, no commentary, no extra text before or after the JSON.

{{
    "decision": "One clear, executable sentence stating exactly what must be done.",
    "reasoning_chain": "Step-by-step logical reasoning (4-9 sentences). Must explicitly reference the Prime Directives and specific rules from the provided documents. Must demonstrate why lower-priority goals were sacrificed if applicable.",
    "cited_wiki_pages": ["ExactPageName1", "ExactPageName2"],
    "rejected_alternatives": "Clear explanation of the main alternative(s) considered and the specific reasons they were rejected, with direct reference to which Directives or rules they violated.",
    "confidence": 0.0
}}

The confidence value (0.0–1.0) must honestly represent how completely and unambiguously the constitutional documents support this specific decision. Do not round up."""

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
