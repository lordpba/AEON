# AEON

**Explicit, auditable AI governance for human settlements beyond reliable Earth communication.**

[![Inference](https://img.shields.io/badge/Inference-Ollama%20(Local)-orange)](https://ollama.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## The Problem

When a small crew is on Mars, Earth is 4 to 22 minutes away. In a real crisis — pathogen outbreak, power collapse, life support failure — help from Earth will arrive in hours, not seconds.

Current Mars concepts assume either constant communication or that an opaque AI will "just handle it."

Both assumptions are dangerous. One produces paralysis. The other produces unaccountable power in a system where mistakes are fatal.

**The missing piece is not better models. It is a constitutional decision layer: explicit rules, transparent reasoning, local execution, and hard boundaries on authority.**

See [docs/THE_MARS_GOVERNANCE_PROBLEM.md](docs/THE_MARS_GOVERNANCE_PROBLEM.md) for the full problem statement.

## Core Thesis

The best AI for Mars is not the one that sounds the smartest.  
It is the one whose reasoning can be read, challenged, and corrected by the people whose lives depend on it — especially when those people are injured, exhausted, or unavailable.

AEON is an open attempt to build the minimum viable version of that system.

## Design Principles

| Principle | Requirement |
|-----------|-------------|
| **Local First** | Everything must run on habitat hardware with zero cloud dependency. |
| **Explicit Constitution** | All authority derives from a small set of human-readable, machine-executable documents (the LLMWiki). |
| **Structured Reasoning** | Every decision must output: decision, step-by-step reasoning, exact sources cited, rejected alternatives, and confidence. |
| **Graceful Autonomy** | If humans cannot respond, the system may act — but only within pre-defined limits and with full audit trail. |
| **Physical Grounding** | Decisions are constrained by real engineering limits, not abstract optimization. |

## Current State

**Phase 1** — Minimum viable constitutional engine:

- LLMWiki containing the core operational documents (starting with `Emergency_Priorities.md` as the supreme authority)
- `AEON Core` agent that produces structured, citable decisions using local models (Ollama)
- FastAPI interface for decision requests and wiki inspection
- Basic Mission Control dashboard

The system is deliberately narrow. It is not trying to simulate a colony. It is trying to make decisions that a real crew could trust when the alternative is death.

## Why This Is Different

Most AI-for-space work optimizes for capability or simulation fidelity.

AEON optimizes for **legibility under existential pressure**.

We want the output of the system, five years from now, to be something an exhausted commander on Sol 847 can read in two minutes and either trust or override with clear justification.

## Repository Structure

```
AEON/
├── llmwiki/           # The constitutional knowledge base (Markdown)
│   └── wiki/
│       └── Emergency_Priorities.md   # Supreme authority document
├── backend/           # FastAPI + local decision engine
├── frontend/          # Mission Control interface (React)
├── docs/              # High-signal documents
│   └── THE_MARS_GOVERNANCE_PROBLEM.md
└── scripts/
    └── test_decision.py
```

## Getting Started

### Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally
- A capable model (recommended: `qwen3.5:9b`+, `gemma3:12b`, or stronger)

### Setup

```bash
git clone https://github.com/lordpba/AEON.git
cd AEON

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

**Backend** (recommended with strong model):
```bash
source .venv/bin/activate
PYTHONPATH=backend OLLAMA_MODEL=qwen3.5:latest uvicorn app.main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
npm run dev
```

Open http://localhost:5173

### Test a Decision

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/decide" \
  -H "Content-Type: application/json" \
  -d '{
    "situation": "Medical team reports suspected pathogen. Phase 2 quarantine requires isolating ventilation sectors, increasing ECLSS power demand significantly. ISRU Sabatier reactors are at full capacity for the Earth-return window.",
    "context_pages": ["Emergency_Priorities", "ECLSS_BAU", "ISRU_Sabatier_Protocol", "Power_Grid_Management", "Medical_Quarantine_Procedure"]
  }'
```

## Contributing

AEON is looking for people who want to do rigorous work on one of the hardest unsolved problems in making humanity multi-planetary: **how a small, isolated crew makes life-and-death decisions when Earth cannot help.**

High-value contributions:

- **Exceptional additions to the LLMWiki** — precise, engineering-grade procedures with real constraints and failure modes.
- Major improvements to decision quality and output structure.
- Integration of actual engineering data (power curves, ECLSS performance, ISRU yields).
- Hard evaluation of the agent against realistic crisis scenarios.
- Frontend work that makes the Mission Control interface feel like something operators would actually trust.

Low-value contributions (will likely be rejected):
- Vague "add more features" without understanding the constitutional constraints.
- Simulation work that distracts from decision legibility.

Read the core documents first:
- [docs/THE_MARS_GOVERNANCE_PROBLEM.md](docs/THE_MARS_GOVERNANCE_PROBLEM.md)
- [llmwiki/wiki/Emergency_Priorities.md](llmwiki/wiki/Emergency_Priorities.md)

## Philosophy

> The best AI for space is not the one that sounds the smartest.  
> It is the one whose reasoning can be read, challenged, and corrected by the people whose lives depend on it.

AEON is built in that spirit.

---

**License:** MIT

**Status:** Early but serious. The direction is set. The quality bar will rise rapidly.

*For the first crew that will one day face a real emergency on Mars, with Earth 20 minutes away and no one coming in time.*