# AEON: Autonomous Extraterrestrial Operations Network

**An open research platform for AI governance of isolated space colonies under communication blackout and human incapacitation.**

[![Status](https://img.shields.io/badge/Status-Research%20Prototype-blue)](https://github.com/lordpba/AEON)
[![Inference](https://img.shields.io/badge/Inference-Ollama%20(Local)-orange)](https://ollama.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## The Problem

When humans establish permanent presence on Mars, Earth will be 4 to 22 minutes away (one way). In a serious crisis — medical emergency, habitat failure, or crew incapacitation — ground control cannot provide timely intervention.

**How does a colony make high-stakes decisions when the humans on site are compromised and help from Earth is hours away?**

AEON is an experimental framework exploring **shared autonomy** between humans and AI in these extreme conditions. It studies how a Multi-Agent System can:

- Execute life-critical operations using explicit, auditable knowledge
- Negotiate resource conflicts under hard physical constraints
- Transition gracefully to full autonomy when human oversight is lost
- Provide transparent, reviewable reasoning for every decision

## Core Design Principles

| Principle | Why It Matters for Mars |
|-----------|-------------------------|
| **100% Local Inference** | No reliable internet. No cloud. The system must operate with models running on habitat hardware. |
| **Explicit Knowledge Base** | All operational knowledge lives in plain Markdown (LLMWiki). No black-box retrieval. Every citation is human-readable. |
| **Structured Reasoning (XAI)** | Every decision returns machine-readable + human-auditable output: decision, reasoning chain, cited sources, rejected alternatives, confidence. |
| **Human-in-the-Loop with Hard Fallback** | Critical actions require human authorization. If the human is incapacitated (timeout), the system can override according to pre-defined survival priorities. |
| **Physical Grounding** | Decisions are constrained by real engineering limits (power budgets, ECLSS physics, propellant production rates, medical resource constraints). |

## Current Focus (Phase 1)

We are building the **minimum viable governance layer**:

- A small set of high-quality Standard Operating Procedures in the LLMWiki
- A core executive agent (`AEON Core`) capable of reading those procedures and producing structured decisions
- A clean, auditable API for decision requests
- A minimal Mission Control interface for human oversight and wiki inspection

The goal is **not** a flashy full-colony simulator yet. The goal is a trustworthy, inspectable decision engine that serious researchers and engineers would be willing to stress-test against real mission constraints.

## Why This Matters

- SpaceX, NASA, and ESA are actively planning crewed Mars missions this decade.
- Current concepts assume continuous or near-continuous communication with Earth.
- Long-duration surface operations will eventually break that assumption.
- The governance and autonomy layer is one of the least mature parts of current mission architecture.

AEON is an attempt to explore that layer in the open.

## Repository Structure

```
AEON/
├── llmwiki/           # The knowledge foundation (plain Markdown SOPs)
│   └── wiki/
├── backend/           # FastAPI + local LLM decision engine
│   └── app/
│       └── core/
│           └── agent.py
├── frontend/          # Minimal Mission Control dashboard (React)
├── docs/              # Architecture, research notes, references
└── README.md
```

## Quickstart

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- A model pulled (recommended for Phase 1: `gemma3:4b`, `llama3.2`, or `qwen2.5:7b`)

### 1. Clone and setup

```bash
git clone https://github.com/lordpba/AEON.git
cd AEON

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start Ollama and pull a model

```bash
ollama pull gemma3:4b
# or any model you prefer
```

### 3. Run the backend

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. Run the frontend (optional)

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` to access the Mission Control interface.

### 5. Test the decision engine

Use the Swagger UI at `http://localhost:8000/docs` or call the endpoint directly:

```bash
curl -X POST "http://localhost:8000/api/v1/decide" \
  -H "Content-Type: application/json" \
  -d '{
    "situation": "Medical team reports suspected pathogen. Phase 2 quarantine requires isolating ventilation sectors. This will increase ECLSS power demand by 40%. ISRU Sabatier reactors are currently running at full capacity.",
    "context_pages": ["Emergency_Priorities", "ECLSS_BAU", "ISRU_Sabatier_Protocol", "Power_Grid_Management"]
  }'
```

The agent will return a structured decision with reasoning and citations from the LLMWiki.

## Current Status

**What works today:**

- LLMWiki with core Mars colony procedures (Emergency Priorities, ECLSS, ISRU, Medical, Power)
- AEON Core agent that produces structured, citable decisions using local Ollama models
- FastAPI endpoints for wiki access and decision requests
- Basic React frontend that can browse the knowledge base

**What does not exist yet:**

- Multiple specialized agents with negotiation
- Real-time simulation of physical systems
- Full Human-in-the-Loop override workflow
- Evaluation harness against historical mission data or expert review

See [ROADMAP.md](docs/ROADMAP.md) for planned development.

## Contributing

We are looking for people who care about making humanity multi-planetary and who are willing to do rigorous, grounded work.

Particularly valuable contributions right now:

- High-quality, technically accurate additions to the LLMWiki
- Improvements to the structured reasoning prompt and output validation
- Integration of real engineering data (power budgets, ECLSS performance curves, medical protocols)
- Evaluation frameworks for agent decisions
- Frontend work on the Mission Control interface

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) before submitting work.

## Philosophy

> The best AI for space is not the one that sounds the smartest.  
> It is the one whose reasoning can be read, challenged, and improved by the people whose lives depend on it.

AEON is built in that spirit.

---

**License:** MIT

**Status:** Early research prototype. Everything is subject to change as we learn what actually works.

*For the people who will one day have to decide between keeping the lights on and keeping the crew alive — when no one on Earth can help in time.*