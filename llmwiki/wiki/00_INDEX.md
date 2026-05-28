# LLMWiki — Structure & Guidelines

This is the foundational knowledge base for AEON.

The goal of this wiki is to serve as the explicit, auditable "constitution + operating manual" for small human crews operating in isolated, high-risk environments (Mars and beyond).

## Core Philosophy

- All high-stakes knowledge must be **human-readable** and **machine-executable**.
- The wiki is the single source of truth for both daily operations (BAU) and emergency fallback.
- AEON must be able to explain every decision by citing specific documents and sections.
- The structure must remain **modular and extensible** so that future missions can easily add new systems, procedures, or domains.

## Directory Structure

```
llmwiki/wiki/
├── 00_INDEX.md                 # This file — explains the overall structure
│
├── principles/                 # Fundamental, high-level rules and hierarchies (very stable)
│
├── procedures/
│   ├── bau/                    # Business As Usual procedures (normal operations)
│   └── contingency/            # Emergency, degraded, and fallback procedures
│
├── systems/                    # Descriptive knowledge about physical systems and equipment
│
├── crew/                       # Human Factors, crew state, performance, and wellbeing
│
├── resources/                  # Inventories, stocks, capacities, and logistics
│
├── monitoring/                 # Integrated indicators, cross-system awareness, early warnings
│
└── interfaces/                 # How different systems and humans interact with each other
```

### Guidelines for Each Category

- **principles/**  
  Contains the supreme decision hierarchy (e.g. Emergency_Priorities). Changes here should be rare and deliberate.

- **procedures/**  
  - `bau/`: How to operate under normal conditions.
  - `contingency/`: What to do when things go wrong or when operating in degraded states.

- **systems/**  
  Technical descriptions of hardware, capabilities, limitations, performance curves, failure modes, etc.  
  Focus on *what the system is*, not only *what to do* with it.

- **crew/**  
  Knowledge related to human performance, fatigue, team dynamics, behavioral indicators, and factors that affect crew reliability in isolated environments.

- **resources/**  
  Current or nominal inventories, consumption rates, resupply logic, and critical resource constraints.

- **monitoring/**  
  Documents that describe how to combine information from multiple domains (e.g. how power state + crew fatigue + ECLSS performance should be interpreted together).

- **interfaces/**  
  Documents describing interactions between systems or between systems and crew.

## How to Add New Content

1. Identify the correct top-level category.
2. If adding a new system, create a folder inside `systems/` (example: `systems/greenhouse/`).
3. If adding new human factors knowledge, add it under `crew/`.
4. Use clear, descriptive filenames.
5. Include a small header in every document with:
   - Version
   - Last updated
   - Related documents (if relevant)

Example header:
```markdown
# Document Title
**Version**: 0.3  
**Category**: Systems / ECLSS  
**Last Updated**: 2026-05-28
```

## Notes for Contributors

- Write for both humans and strong language models.
- Be precise. Avoid vague language.
- When a document has implications for crew state or safety, cross-reference the relevant files in `crew/` and `principles/`.
- The more the wiki grows, the more important it becomes to keep this structure clean.

This structure is designed to scale from a small early Mars habitat to larger, more complex settlements over time.
