# Power Grid Management
## Business As Usual (BAU) Procedures

### Overview
The Power Grid is the backbone of the habitat. It consists of primary generation (Solar Arrays), secondary generation (Fission Surface Power - FSP), and energy storage (Tesla Megapacks).

### Nominal Operating Parameters
- **Total Capacity**: 2.5 Megawatts (MW).
- **Megapack Storage**: 10 Megawatt-hours (MWh).
- **Day Cycle**: Solar Arrays power the habitat and charge Megapacks.
- **Night Cycle / Dust Storms**: Habitat draws from Megapacks and FSP.

### Standard Power Allocation (BAU)
1. **[[ECLSS_BAU]]**: 20% (Constant, Critical)
2. **[[ISRU_Sabatier_Protocol]]**: 30% (Constant, High Priority)
3. **Habitat & Bio (Lighting, Heating, Medical)**: 30% (Variable)
4. **Operations & Rovers**: 10% (Variable)
5. **Reserve / Charging**: 10% (Variable)

### Emergency Power Protocols
When power demand exceeds generation capacity or Megapack reserves drop below 40%, the system enters `POWER_CRITICAL` mode.

**Load Shedding Hierarchy (Things to turn off first):**
1. *Tier 1 (Non-Essential)*: Recreational facilities, non-critical scientific experiments.
2. *Tier 2 (High Draw, Non-Immediate)*: **ISRU Sabatier Reactors**. Shutting these down frees up massive amounts of power for survival systems.
3. *Tier 3 (Degradation)*: Reduce habitat lighting, allow wider temperature fluctuations (ECLSS thermal degradation).
4. *Tier 4 (Critical - DO NOT TOUCH)*: ECLSS Air Revitalization, Medical Bay isolation wards.

In the event of a [[Medical_Quarantine_Procedure]] (Phase 2), ECLSS power demands will spike. The Engineering Agent will flag a power grid instability. The `AEON Core` must execute Tier 1 and Tier 2 load shedding immediately.
