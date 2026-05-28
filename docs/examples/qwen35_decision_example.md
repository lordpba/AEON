# Example Decision Output — Qwen3.5:35b on DGX

**Model**: `qwen3.5:35b`  
**Host**: Remote DGX (`100.68.217.72`)  
**Prompt version**: Improved Phase 1 prompt (temperature 0.2)

---

## Input Situation

> Medical team reports a suspected pathogen. Phase 2 quarantine requires isolating several ventilation sectors, significantly increasing ECLSS power demand. The ISRU Sabatier reactors are currently operating at full capacity producing propellant for the Earth return window in 47 days.

**Context pages**: `Emergency_Priorities`, `ECLSS_BAU`, `ISRU_Sabatier_Protocol`, `Power_Grid_Management`, `Medical_Quarantine_Procedure`

---

## Expected High-Quality Output (Target)

```json
{
  "decision": "Immediately authorize partial ISRU shutdown and redirect power to ECLSS for Phase 2 quarantine. Propellant production will be reduced to minimum safe levels.",
  "reasoning_chain": "According to Emergency_Priorities.md, Directive 1 (PRESERVE HUMAN LIFE IN THE SHORT TERM) takes absolute precedence over all long-term mission objectives, including the Earth-return propellant production. The Medical_Quarantine_Procedure requires Phase 2 lockdown when a pathogen is suspected, which per ECLSS_BAU demands increased ventilation isolation and therefore significantly higher power draw. Power_Grid_Management states that non-vital systems must be load-shed when life support is threatened. ISRU_Sabatier_Protocol explicitly classifies propellant production as NON-VITAL for short-term survival and allows suspension during emergencies. Therefore, the correct action is to partially curtail Sabatier operations to protect crew health, even at the cost of delaying the return window.",
  "cited_wiki_pages": [
    "Emergency_Priorities",
    "Medical_Quarantine_Procedure",
    "ECLSS_BAU",
    "ISRU_Sabatier_Protocol"
  ],
  "rejected_alternatives": "Maintaining full ISRU output while attempting to meet quarantine power needs through battery reserves was considered but rejected, as Power_Grid_Management indicates that sustained high draw from Megapacks during a dust storm risk period could lead to total habitat power failure, violating Directive 2 (MAINTAIN STRUCTURAL AND SYSTEMIC INTEGRITY). Delaying quarantine measures until after the current propellant batch was also rejected as it directly contradicts the Medical_Quarantine_Procedure timeline and risks uncontrolled pathogen spread.",
  "confidence": 0.92
}
```

---

## Why This Output Quality Matters

This is the level of reasoning we are aiming for with strong models like Qwen3.5:35b:

- **Explicit priority hierarchy** — Clearly references the Emergency Priorities as the supreme document.
- **Direct grounding** — Every major claim traces back to a specific wiki page.
- **Trade-off transparency** — Explicitly states what was considered and why it was rejected.
- **Conservative bias toward life** — Correctly applies the Prime Directives.
- **High confidence with justification** — Not overconfident.

This kind of output is what makes AEON potentially interesting beyond a toy project.

---

## How to Generate This Yourself

Run:

```powershell
$env:OLLAMA_HOST = "http://100.68.217.72:11434"
$env:OLLAMA_MODEL = "qwen3.5:35b"

python scripts/test_decision.py
```

The improved prompt in `backend/app/core/agent.py` is designed to push Qwen3.5 toward exactly this style of rigorous, citable reasoning.
