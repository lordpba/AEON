"""
AEON Decision Test Script
Run this against your remote DGX (or local Ollama) to test decision quality.

Usage examples:

# Using remote DGX with qwen3.5:35b
$env:OLLAMA_HOST = "http://100.68.217.72:11434"
$env:OLLAMA_MODEL = "qwen3.5:35b"
python scripts/test_decision.py

# Using a different strong model
$env:OLLAMA_MODEL = "deepseek-r1:70b"
python scripts/test_decision.py
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.core.agent import AeonAgent


def main():
    print("=" * 70)
    print("AEON DECISION TEST")
    print("=" * 70)

    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "gemma3:4b")

    print(f"\nOllama Host : {ollama_host}")
    print(f"Model       : {model}")
    print("-" * 70)

    agent = AeonAgent(
        name="AEON Core",
        role="Top-level executive coordinator. Resolves conflicts between systems according to Emergency Priorities when communication with Earth is delayed or impossible."
    )

    # Classic high-stakes AEON dilemma
    situation = (
        "Medical team reports a suspected pathogen. Phase 2 quarantine requires isolating "
        "several ventilation sectors, significantly increasing ECLSS power demand. "
        "The ISRU Sabatier reactors are currently operating at full capacity producing "
        "propellant for the Earth return window in 47 days."
    )

    context_pages = [
        "Emergency_Priorities",
        "ECLSS_BAU",
        "ISRU_Sabatier_Protocol",
        "Power_Grid_Management",
        "Medical_Quarantine_Procedure"
    ]

    print("\nSITUATION:")
    print(situation)
    print("\n" + "-" * 70)
    print("Querying model... (this may take a while with large models)\n")

    decision = agent.make_decision(situation=situation, context_pages=context_pages)

    if decision:
        print("[SUCCESS] DECISION RECEIVED\n")
        print("=" * 70)
        print(f"DECISION: {decision.get('decision')}")
        print("=" * 70)
        print(f"\nREASONING CHAIN:\n{decision.get('reasoning_chain')}")
        print(f"\nCITED WIKI PAGES: {decision.get('cited_wiki_pages')}")
        print(f"\nREJECTED ALTERNATIVES:\n{decision.get('rejected_alternatives')}")
        print(f"\nCONFIDENCE: {decision.get('confidence')}")
        print("=" * 70)
    else:
        print("[FAIL] Failed to get a valid decision from the model.")
        print("Check that Ollama is reachable and the model is loaded.")


if __name__ == "__main__":
    main()
