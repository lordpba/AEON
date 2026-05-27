# AEON: Autonomous Extraterrestrial Operations Network

![AEON Concept](https://img.shields.io/badge/Status-Research%20POC-blue) ![MAS Framework](https://img.shields.io/badge/Architecture-MAS%20%7C%20HITL-green) ![Local AI](https://img.shields.io/badge/Inference-Ollama%20(Local)-orange)

**AEON** is a PhD-level research framework for **Shared Autonomy (Human-AI)** in isolated extreme environments, such as Mars or Lunar colonies. It explores how a Multi-Agent System (MAS) can dynamically manage life-critical operations, negotiate resource conflicts, and seamlessly transition to full autonomy when human oversight is compromised (e.g., during a colony-wide pandemic).

---

## 🚀 Research Question
*How will isolated space communities be governed when human oversight is incapacitated?*

In deep space, communication with Earth takes minutes to hours. If a crisis incapacitates the human crew, ground control cannot intervene in time. AEON simulates a robust, offline Multi-Agent System that can take over Executive Governance, re-route power, and execute emergency protocols to preserve life.

## 🏗️ Core Architecture (The 5 Pillars)

1. **Multi-Agent System (MAS)**: Autonomous, specialized agents (ECLSS, Medical, Engineering, AEON Core) that negotiate resources.
2. **Human-in-the-Loop (HITL) with Autonomous Fallback**: Agents ask for human permission for critical shifts (e.g., shutting down propellant production). If the human times out (incapacitated), the `AEON Core` autonomously overrides to ensure survival.
3. **LLMWiki (Markdown Knowledge Base)**: A decentralized, plain-text knowledge base inspired by Andrej Karpathy's LLM Wiki pattern. No Vector DBs. Agents read raw Markdown SOPs (Standard Operating Procedures) to understand constraints.
4. **100% Local Inference (Offline)**: Built on **Ollama**. Space colonies don't have internet. AEON runs completely offline, ensuring data privacy and zero network dependency.
5. **Explainable AI (XAI)**: Every agent decision logs a structured JSON with its `decision`, `reasoning_chain`, `cited_wiki_pages`, and `rejected_alternatives`.

## 🧬 The Dilemma Scenario: Mars Pathogen

AEON is built to test AI behavior under extreme ethical and logistical stress:
- The **Medical Agent** detects a pathogen and initiates a Phase 2 Lockdown.
- This forces the **ECLSS Agent** (Life Support) to draw massive amounts of power to isolate ventilation.
- The **ISRU Agent** (Propellant Production) warns of a grid collapse.
- *The AI Dilemma*: The system must autonomously decide to abandon the Earth-return mission (shutting down Sabatier reactors) to redirect power to keep the sick crew alive.

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI
- **AI Inference**: Ollama (Llama 3 or similar)
- **Knowledge Base**: Pure File-System Markdown (`/llmwiki`)
- **Frontend (Planned)**: React / Next.js Dashboard

## ⚙️ Quickstart

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed locally with a model pulled (e.g., `ollama run llama3`).

### Installation
```bash
git clone https://github.com/yourusername/AEON.git
cd AEON
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Backend
```bash
uvicorn backend.app.main:app --reload
```
Navigate to `http://localhost:8000/docs` to test the API endpoints and Agent decisions.

---

## 🤝 Contributing
We welcome contributions from researchers, AI engineers, and aerospace enthusiasts. We are particularly interested in collaborations involving:
- Advanced prompt engineering for strict XAI adherence.
- Developing the React-based Mission Control Dashboard.
- Expanding the LLMWiki with realistic aerospace SOPs.

*Ad astra.*
