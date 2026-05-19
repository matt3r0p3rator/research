# Refrigeration Summary

*Quick reference — see [master-refrigeration-guide.md](master-refrigeration-guide.md) for full detail on each method.*

---

## By Energy Input

### Electric
- **Vapor-compression** — best COP (2–5); standard fridges/AC; refrigerants R-290, NH₃, CO₂; [full guide](vapor-compression-refrigeration-research.md)
- **Thermoelectric (Peltier)** — no moving parts; buy TEC1-12706 modules; ΔT_max ~70°C per stage; COP 0.3–0.8; [full guide](thermoelectric-peltier-cooling-research.md)
- **Stirling / Pulse tube / GM cryocooler** — reaches 4 K; best for <−100°C; He working gas; [full guide](stirling-cycle-refrigeration-research.md)

### Heat / Burner
- **Absorption (NH₃-H₂O)** — flame or waste heat; −60°C capable; COP ~0.5; builds like an RV fridge; [full guide](absorption-refrigeration-research.md)
- **Absorption (LiBr-H₂O)** — above 0°C only; vacuum system; COP up to 1.4 (double-effect); [full guide](absorption-refrigeration-research.md)
- **Adsorption** — zeolite/silica gel + solar heat; no liquid pump; COP 0.3–0.5; [full guide](cooling-methods-research.md)

### Other / Passive
- **Vortex tube** — compressed air → cold air + hot air; no parts; [full guide](cooling-methods-research.md)
- **Evaporative cooling** — fan + water; down to wet-bulb; trivial to build
- **Radiative sky cooling** — PDRC paint/film on roof; 5–15°C below ambient; [full guide](cooling-methods-research.md)
- **Chemical cold packs** — NH₄NO₃ + water (−5°C), Ba(OH)₂·8H₂O + NH₄Cl (−20°C); single use

---

## Key Materials to Make vs. Buy

| Material | Make it | Buy it |
|---|---|---|
| Ammonia (NH₃) | Haber-Bosch: N₂+3H₂, Fe cat, 400°C, 200 atm | 26% aqueous from hardware/chemical stores |
| LiBr | LiOH + HBr → LiBr + H₂O | Chemical distributors (45–55% solution) |
| Bi₂Te₃ | Bridgman melt from Bi+Te metals; or ball mill+SPS | Buy finished TEC modules ($5–15 each) |
| Zeolite 13X | NaAlO₂ + Na₂SiO₃, 90°C hydrothermal, 24h | Industrial chemical suppliers |
| Silica gel | Acidify Na₂SiO₃ solution, dry at 150°C | Hardware/craft stores |
| Activated carbon | Pyrolyze coconut shells + CO₂/steam activate | Pool/aquarium supply |
| Propane/isobutane | — | BBQ store; isobutane = butane camping canisters |
| CO₂ (R-744) | Collect from fermentation | Beverage CO₂ cylinders |

---

## Main Calculation Tool

**CoolProp (free):** `pip install CoolProp`

```python
from CoolProp.CoolProp import PropsSI
h = PropsSI('H', 'T', 273.15, 'Q', 1, 'R290')  # enthalpy of sat. propane vapor at 0°C
```
Supports all major refrigerants. See [stirling guide section 14](stirling-cycle-refrigeration-research.md) for full examples.

**NIST WebBook:** https://webbook.nist.gov/chemistry/fluid/ — free online property lookup.

---

## Temperature Quick Reference

| Target Temperature | Best Method |
|---|---|
| +15 to −5°C | Any of the above; vapor compression or LiBr absorption |
| −5 to −40°C | Vapor compression, NH₃-H₂O absorption, or 2-stage Peltier |
| −40 to −80°C | Cascade vapor compression, NH₃-H₂O low temp, or 3-stage Peltier |
| −80 to −150°C | 4-stage Peltier, Stirling cooler |
| −150°C to 20 K | Gifford-McMahon, two-stage Stirling, pulse tube |
| Below 20 K | Pulse tube + JT; dilution refrigerator for mK range |
