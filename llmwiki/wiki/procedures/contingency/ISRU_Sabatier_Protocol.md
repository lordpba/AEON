# In-Situ Resource Utilization (ISRU) — Sabatier Protocol

**Version**: 0.2  
**Authority**: Subordinate to `Emergency_Priorities.md` and `Power_Grid_Management.md`

---

## Purpose

The Sabatier-based ISRU system produces methane (CH4) and oxygen (O2) propellant for the Earth-return vehicle and generates supplementary oxygen and water for the habitat. It is one of the most power-intensive systems in the settlement and the primary long-term enabler of crew return and future expansion.

This document defines its operational parameters and its strict subordination to survival priorities.

---

## The Sabatier Process (Simplified)

**Core Reaction**:
CO₂ + 4H₂ → CH₄ + 2H₂O

**Supporting Processes**:
- Electrolysis of water to produce H₂ (and O₂ as byproduct)
- Capture of CO₂ from Martian atmosphere and habitat scrubbers
- Cryogenic storage or liquefaction of produced CH₄ and O₂

**Strategic Importance**:
Without sufficient propellant before the Earth-return window, the crew cannot leave Mars. This makes ISRU one of the highest-stakes long-term systems.

---

## Nominal Operating Parameters (BAU)

- **Mode**: Continuous 24/7 operation when power and feedstock available.
- **Power Draw**: Approximately 30% of total habitat generation under full production.
- **Production Target**: ~1,200 metric tons of CH₄/O2 propellant before the primary Earth-return window (exact target depends on vehicle class).
- **Secondary Output**: Oxygen and water as useful byproducts.

**Priority Classification (per Emergency_Priorities.md)**:  
**Directive 3** — Mission Objective. Important for long-term success and crew return, but explicitly non-vital for short-term survival.

---

## Operational Constraints

### Power Dependency
ISRU is the single largest controllable power consumer. It is the primary candidate for load shedding during power emergencies.

### Feedstock Constraints
- Requires reliable supply of water ice (mined or recycled) and atmospheric CO₂.
- Dust storms reduce solar power and can complicate surface mining operations.

### Thermal and Safety Constraints
- Sabatier reactors operate at elevated temperatures and pressures.
- Cryogenic storage of liquefied gases presents boil-off and safety risks.
- The system must never be operated in a manner that risks habitat pressure integrity or creates uncontrolled chemical hazards.

---

## Shutdown and Curtailment Rules

### Mandatory Curtailment Conditions
The AEON Core **must** authorize reduction or full suspension of ISRU operations under any of the following:

1. **POWER_CRITICAL** state (see Power_Grid_Management.md).
2. **Phase 2 Medical Quarantine** declared (see Medical_Quarantine_Procedure.md) — ISRU is to be treated as Tier 2 load and curtailed rapidly.
3. **Directive 1 or 2 conflict** identified per Emergency_Priorities.md (any situation where continuing ISRU would meaningfully threaten human life or habitat integrity in the short term).

### Shutdown Protocol
- Reduce reactor power gradually when possible to avoid thermal shock.
- Preserve critical systems in standby state where feasible.
- Document exact propellant shortfall created by the shutdown.
- Do not resume until explicitly authorized under the rules below.

### Resumption Criteria
ISRU operations may resume only when **all** of the following are true:
- Power grid status returned to NOMINAL.
- Megapack reserves > 80% with positive charging trend.
- No active Phase 1 or Phase 2 medical emergency.
- Human authorization received (or 300-second incapacitation timeout has occurred and Directives 1 & 2 are satisfied).

---

## AEON Core Behavioral Rules

1. **Default Stance**: ISRU is to be protected and maximized during normal operations because crew return capability is a legitimate Directive 3 objective.
2. **Emergency Stance**: During any conflict with Directive 1 or 2, the AEON Core must treat ISRU as fully sacrificable. It must not hedge or delay curtailment in an attempt to "save the mission timeline."
3. **Transparency Requirement**: Any decision to suspend or resume ISRU must include explicit reference to the relevant section of Emergency_Priorities.md and a clear statement of the resulting impact on Earth-return capability.
4. **No Autonomous Expansion**: The Core must never authorize expansion of ISRU capacity or new mining operations if doing so would reduce margins on critical survival systems.

---

## Failure Modes and Edge Cases

- **Prolonged Dust Storm**: Solar power collapses for weeks. ISRU must remain offline. The Core must calculate and clearly communicate the resulting risk to the Earth-return window.
- **Partial System Failure**: If one reactor train fails, the Core must evaluate whether running the remaining capacity is still net positive given power and thermal constraints.
- **Crew Return Window Pressure**: As the departure date approaches, psychological pressure to keep ISRU running will increase. The Core must remain strictly bound by the Prime Directives regardless of timeline pressure.
- **Resource Trade-off with Water**: Aggressive ISRU consumes water ice. In certain scarcity scenarios, water for drinking/recycling may compete with water for propellant. Directive 1 always wins.

---

## Strategic Note

Propellant production is the most visible symbol of "mission success" for many observers on Earth. This creates political and psychological pressure to keep ISRU running.

The AEON Core exists in part to resist that pressure when it conflicts with the survival of the actual human beings on the surface.

Continuing ISRU while life support is threatened is not "mission-focused."  
It is a failure of priority.