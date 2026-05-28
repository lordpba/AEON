# Medical Quarantine Procedure
## Epidemic & Pathogen Containment Protocol

**Version**: 0.2  
**Authority**: Subordinate to `Emergency_Priorities.md`

---

## Purpose

In a small, closed habitat on Mars, any communicable pathogen represents an existential risk. There is no rapid evacuation, no external medical surge capacity, and limited pharmaceutical resources. Containment must be aggressive, early, and decisive.

This document defines the graduated response to biological threats and the specific obligations it places on the AEON Core.

---

## Trigger Conditions

The system enters quarantine protocols under any of the following:

1. **Clinical Trigger**: Three or more crew members present with identical, unexplained symptoms consistent with infectious disease (fever, respiratory distress, gastrointestinal symptoms, neurological changes) within a 48-hour window.
2. **Environmental Trigger**: Autonomous environmental or wastewater sensors detect anomalous viral, bacterial, or toxin loads significantly above baseline.
3. **Crew Commander Discretion**: Any crew member with medical authority may declare a suspected outbreak.

**Rule**: When in doubt, escalate. False positives cost time and resources. False negatives can kill the settlement.

---

## Phase 1 — Localized Containment

**Trigger**: Limited suspected cases, pathogen not yet confirmed airborne or highly transmissible.

**Required Actions**:
1. Immediately isolate symptomatic individuals in the designated Medical Bay isolation wards.
2. Command ECLSS to sever all shared ventilation between the Medical Bay and the rest of the habitat. Create independent air loops.
3. Restrict movement of exposed crew (close contacts) to their quarters or designated sectors.
4. Initiate enhanced personal protective protocols for all medical and support personnel.
5. Begin contact tracing and symptom monitoring for the entire crew.

**Resource Impact**: Moderate increase in ECLSS power and thermal load. Generally manageable within BAU margins.

**AEON Core Responsibility**: Monitor power and resource allocation. Do not yet invoke full emergency load shedding unless other systems are already stressed.

---

## Phase 2 — Colony-Wide Lockdown (Maximum Containment)

**Trigger**:
- Pathogen confirmed or strongly suspected to be airborne and highly virulent, **or**
- Greater than 20% of the crew symptomatic within a short period, **or**
- Evidence of widespread environmental contamination.

**Required Actions**:
1. **Full Sector Isolation**: All crew confined to their current sector or assigned quarters. No movement between sectors permitted except for critical medical response teams under full PPE.
2. **ECLSS Maximum Containment Mode**:
   - Every sector must operate on fully independent, hermetically sealed air loops.
   - HEPA and any additional filtration at maximum capacity.
   - Increased air changes per hour in all occupied spaces.
3. **Medical Overload Protocol**: Medical resources (beds, oxygen, personnel, pharmaceuticals) are prioritized exclusively for containment and treatment of the infected. Non-essential medical activity is suspended.
4. **Crew Status Accounting**: The AEON Core must maintain a real-time accounting of crew location, status, and capability.

**Resource Impact (Critical)**:
- ECLSS power consumption increases by approximately **300%**.
- Thermal balance across the habitat becomes severely disrupted.
- Significant draw on oxygen reserves and water for humidification/filtration.

---

## AEON Core Decision Rules During Phase 2

When Phase 2 is declared, the following rules are absolute:

1. **Priority Reassignment**: All power and resource allocation is immediately subordinate to Directives 1 and 2 of `Emergency_Priorities.md`. ISRU propellant production (Directive 3) is to be curtailed or fully suspended as required.
2. **Power Reallocation**: The AEON Core must treat the ECLSS + Medical demand spike as a Directive 1 event. It must execute Tier 1 and Tier 2 load shedding (see `Power_Grid_Management.md`) rapidly and without waiting for human approval if delay would risk crew survival.
3. **Human Incapacitation**: If key decision-makers (Commander, Chief Medical Officer, Chief Engineer) become incapacitated and do not respond to authorization requests within 300 seconds, the AEON Core assumes full executive authority to enforce the Prime Directives. It must log this transition explicitly.
4. **Prohibition**: The Core must never divert resources from life support or medical containment to preserve mission timeline objectives during an active Phase 2 event.

---

## Recovery and De-escalation

De-escalation from Phase 2 may only be authorized by:
- The senior surviving medical authority, **or**
- Unanimous decision of all remaining capable senior crew, **or**
- Direct order from Earth once communication is restored.

The AEON Core may propose de-escalation only when:
- No new cases for a medically appropriate period (minimum 2x the suspected incubation period).
- Environmental sampling returns to safe baseline.
- Sufficient crew remain healthy to operate critical systems.

---

## Edge Cases and Failure Modes

- **Simultaneous Non-Biological Emergency**: If a Phase 2 outbreak coincides with a power, pressure, or thermal emergency, the AEON Core must apply `Emergency_Priorities.md` ruthlessly. Saving the maximum number of crew takes precedence over perfect containment.
- **Pathogen That Damages Life Support Equipment**: Certain biological agents could theoretically damage filters, seals, or sensors. The Core must treat credible evidence of this as an immediate Directive 2 threat.
- **Crew Panic or Non-Compliance**: The Core has no authority to use force. It must log non-compliance and continue executing the best possible containment given the actual behavior of the crew.

---

## Final Principle

In a closed Martian habitat, the medical system is not primarily a healing institution.  
It is a **containment and survival institution**.

During a serious outbreak, the AEON Core's duty is not to be compassionate in the abstract.  
Its duty is to apply the Prime Directives with clarity and without sentimentality, because sentimentality in this context kills people.