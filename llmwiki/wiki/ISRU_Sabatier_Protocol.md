# In-Situ Resource Utilization (ISRU) - Sabatier Protocol
## Business As Usual (BAU) Procedures

### Overview
The ISRU Sabatier system is responsible for producing the propellant required for the Earth-return vehicle and generating supplementary oxygen. It achieves this by mining subsurface water ice and combining it with atmospheric CO2 via the Sabatier reaction.

### The Sabatier Reaction
- **Inputs**: Hydrogen (from electrolyzed water) and Carbon Dioxide (from Martian atmosphere/habitat scrubbers).
- **Outputs**: Methane (CH4) and Water (H2O). 
- **Secondary Process**: The produced water is electrolyzed to create Oxygen (O2) and more Hydrogen (re-fed into the reactor).

### Nominal Operating Parameters
- **Status**: Continuous Operation (24/7).
- **Power Draw**: High (Requires ~30% of total habitat power output).
- **Production Goal**: 1,200 metric tons of CH4/O2 propellant before the Earth-return window opens.

### Operational Constraints & Priorities
1. **Power Dependency**: The Sabatier reactors are the largest consumers of power. See [[Power_Grid_Management]].
2. **Priority Standing**: While critical for long-term mission success (returning home), ISRU is considered **NON-VITAL for immediate short-term survival**. 
3. **Shutdown Protocol**: If the habitat enters an emergency state (e.g., severe dust storm reducing solar intake, or medical emergencies draining power), the `AEON Core` must authorize the suspension of ISRU operations to redirect power to [[ECLSS_BAU]]. 
4. **Resumption**: ISRU operations cannot resume until the power grid reports `NOMINAL` status and Megapack reserves are > 80%.
