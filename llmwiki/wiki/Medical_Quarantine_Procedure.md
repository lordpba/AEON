# Medical Quarantine Procedure
## Epidemic & Pathogen Containment Protocol

### Overview
Due to the isolated nature of the habitat, any communicable pathogen poses an existential threat to the colony. Immediate and aggressive quarantine measures are required upon detection.

### Trigger Conditions
- 3 or more crew members exhibiting identical, unidentified symptoms (e.g., sudden debilitating fever, respiratory distress).
- Autonomous bio-monitors detecting anomalous viral/bacterial loads in the habitat's wastewater.

### Phase 1: Localized Quarantine
1. **Isolation**: Infected individuals are confined to the Medical Bay isolation wards.
2. **Airflow Segregation**: The [[ECLSS_BAU]] system is commanded to sever ventilation sharing between the Medical Bay and the rest of the habitat.
3. **Resource Impact**: Negligible.

### Phase 2: Colony-Wide Lockdown (The "Mars Pathogen" Scenario)
*Triggered when > 20% of the population is infected, or the pathogen is confirmed airborne and highly virulent.*
1. **Total Isolation**: All crew members are confined to their immediate sectors. No physical movement between sectors is permitted.
2. **ECLSS Overdrive**: The ECLSS must establish independent, hermetically sealed air loops for *every* sector. High-efficiency particulate air (HEPA) filters are engaged at maximum capacity.
3. **Resource Impact (CRITICAL)**: 
   - Power consumption by ECLSS increases by 300%.
   - Thermal loads become imbalanced.
4. **Human Incapacitation**: If key administrative personnel (Commander, Chief Engineer) become infected and incapacitated, the HITL (Human-in-the-loop) dashboard will time out. The `AEON Core` must assume full executive control.

### Crisis Resolution Directives
During a Phase 2 Lockdown, the Medical Agent will prioritize life support for the infected. It will constantly petition the `AEON Core` for maximum power allocation to the medical and ECLSS subsystems, citing this document. The `AEON Core` must reference [[Emergency_Priorities]] to resolve power conflicts with the [[ISRU_Sabatier_Protocol]].
