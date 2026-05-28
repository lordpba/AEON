# Power Grid Management
## Business As Usual (BAU) and Emergency Protocols

**Version**: 0.2  
**Authority**: Subordinate to `Emergency_Priorities.md`

---

## Overview

The power grid is the single point of failure for the entire habitat. All life-critical systems (ECLSS, medical, communications) and all long-duration mission systems (ISRU) depend on continuous, stable power.

Primary sources: Solar arrays + Fission Surface Power (FSP).  
Storage: Tesla Megapacks (or equivalent).

Under Martian conditions, solar output can drop dramatically during global dust storms. FSP provides baseline but has its own failure modes and thermal constraints.

---

## Nominal Power Allocation (BAU)

| Subsystem                        | Allocation | Priority | Notes |
|----------------------------------|------------|----------|-------|
| ECLSS (Air Revitalization + Thermal) | ~20%    | Critical | Must never drop below minimum safe level |
| ISRU Sabatier Reactors           | ~30%       | High     | Largest single consumer. Non-vital for short-term survival |
| Habitat Systems + Medical        | ~25-30%    | High     | Lighting, heating, computing, medical baseline |
| Operations & Rovers              | ~10%       | Medium   | Deferrable |
| Battery Charging / Reserve       | ~10%       | Critical | Maintains margin against night and storms |

**Reserve Policy**: Megapack state of charge should not be drawn below 40% during normal operations except during planned high-draw periods with clear recovery plan.

---

## Emergency Power States

### POWER_ALERT
Megapack reserves < 40% or generation significantly below demand.

**Actions**:
- Cancel all non-essential operations
- Begin Tier 1 load shedding (see below)
- Notify human crew immediately

### POWER_CRITICAL
Megapack reserves < 25% **or** sustained deficit that will breach critical systems within 12 hours.

**Actions**:
- Execute Tier 1 + Tier 2 load shedding without delay
- Reduce habitat thermal and lighting loads
- Request immediate human decision on further measures
- If human incapacitation timeout occurs, AEON Core assumes authority per `Emergency_Priorities.md`

---

## Load Shedding Hierarchy

When power must be curtailed, the following order is mandatory:

| Tier | Systems | Impact if Shed | Can be shed under... |
|------|---------|----------------|----------------------|
| **1** | Recreational facilities, non-critical science, cosmetic lighting, non-essential computing | Low survival impact | POWER_ALERT or higher |
| **2** | **ISRU Sabatier Reactors** (entire system) | Halts propellant production. Major mission delay. | POWER_CRITICAL or Directive 1/2 conflict |
| **3** | Habitat lighting reduction, widened temperature band (18-26°C), reduced CO2 scrubbing rate (temporary) | Degraded crew conditions | Only when necessary for Directive 1 or 2 |
| **4** | **ECLSS Air Revitalization, Medical isolation systems, minimum life support** | Rapid crew death | **NEVER** (forbidden) |

**Explicit Rule**: Tier 4 systems are inviolable except in the most extreme cases where partial degradation is the only remaining option to prevent total habitat loss. Such decisions require the highest level of justification under `Emergency_Priorities.md` Directive 1 and 2.

---

## Interaction with Medical Quarantine (Phase 2)

A Phase 2 quarantine triggers massive increase in ECLSS power demand (independent air loops + maximum filtration).

**Required Response**:
1. Immediately declare POWER_CRITICAL.
2. Execute Tier 1 and Tier 2 load shedding **before** requesting human authorization if delay would risk crew.
3. Redirect all available power to ECLSS and Medical.
4. ISRU is to be considered non-essential until power margin is restored above 35% with positive trend.

This interaction is one of the primary test cases for the AEON Core.

---

## Failure Mode Considerations

- **Dust Storm Collapse**: Solar arrays can drop to <10% output for weeks. FSP becomes the only generation. ISRU must be suspended.
- **Megapack Degradation**: Individual packs failing reduces effective storage. The system must treat effective capacity as the real number, not nameplate.
- **FSP Trip**: Sudden loss of fission plant requires immediate aggressive load shedding to stretch battery reserves until recovery or crew intervention.
- **Simultaneous Failures**: The Core must never assume only one system is failing. Worst-case planning is mandatory when in POWER_CRITICAL.

---

## Authority Note

Power allocation decisions that affect Directive 1 or 2 systems are under the constitutional authority of `Emergency_Priorities.md`. This document provides the engineering constraints and load-shedding mechanics, not the moral priority.