# Cloud Chamber — Quick Reference Summary

*Full guide: [cloud-chamber-master-guide.md](cloud-chamber-master-guide.md)*

---

## What It Is

A **diffusion cloud chamber** creates a continuously supersaturated layer of isopropyl alcohol vapor between a warm top (~25 °C) and a cold bottom plate (−26 °C minimum, −35 to −78 °C optimal). Ionizing particles leave visible white mist trails in this layer.

---

## Cooling — The Critical Constraint

**You need the cold plate below −26 °C.** See [refrigeration/master-refrigeration-guide.md](../refrigeration/master-refrigeration-guide.md) for full method details.

| Method | Cold Plate | Go/No-go |
|---|---|---|
| Dry ice (−78.5 °C) | −50 to −70 °C | ✅ Best; easiest |
| 2-stage Peltier + water cooling | −45 to −55 °C | ✅ Best Peltier option |
| Mini fridge compressor | −35 to −45 °C | ✅ Best permanent |
| Single Peltier + air cooling | −10 to −20 °C | ❌ Too warm |
| Liquid nitrogen | −190 °C | ❌ IPA freezes at −89 °C |

**IPA freezes at −89 °C** — never use LN₂. Dry ice at −78.5 °C is the practical lower limit.

---

## Fastest Build (Dry Ice, ~$86, 1 hour)

1. 10-gal glass aquarium + aluminum plate (matte black velvet on top face)
2. **99% IPA** — not 70%, not 91% — on felt strips at the top interior perimeter (15–25 mL)
3. Aluminum plate on dry ice slabs in a styrofoam cooler; chamber sits on plate
4. Lid with small vent hole; wait 10 min
5. Bright LED at 5–15° above horizontal from one side; darken room completely

**Session length:** 1–3 hr per 5 lb of dry ice (~$10)

---

## Permanent Build (Peltier, ~$144–306, no recurring costs)

TEC stack: **2× TEC1-12710** (Stage 1, hot side) → copper spreader → **1× TEC1-12706 at 8–10 V** (Stage 2, cold side) → copper cold plate

- Air-cooled alone won't work — need a large CPU tower heat sink at minimum; water loop preferred
- Reaches −40 to −55 °C with good heat sinking
- See [refrigeration/thermoelectric-peltier-cooling-research.md](../refrigeration/thermoelectric-peltier-cooling-research.md) for TEC details

---

## What You'll See

| Track | Particle | Looks Like |
|---|---|---|
| Short, thick, straight, defined end | Alpha (α) | Fat white rope, 2–5 cm |
| Thin, wispy, curling | Beta (e⁻/e⁺) | Wiggly thread |
| Long, ruler-straight | Cosmic muon | Crosses full chamber |
| Two tracks from one invisible point | Pair production (γ → e⁻e⁺) | Needs Pb plate + strong γ source |

**Without any source:** 5–15 cosmic muon tracks/min — free, always on.

---

## Best Starter Radioactive Source

**Am-241 from an old ionization-type smoke detector** — produces beautiful thick alpha tracks (~3 cm). Keep the source sealed in its original gold foil holder. Legal for personal use in the USA.

---

## Top 3 Mistakes

1. **Using 70% or 91% IPA instead of 99%** — chamber will not work
2. **Single Peltier with air cooling** — too warm; won't reach minimum threshold
3. **Wrong light angle** — light must be nearly horizontal (5–15°), not overhead

---

## Research Files

| Topic | File |
|---|---|
| **Master guide (this topic)** | [cloud-chamber-master-guide.md](cloud-chamber-master-guide.md) |
| Cooling methods overview | [../refrigeration/master-refrigeration-guide.md](../refrigeration/master-refrigeration-guide.md) |
| Peltier/TEC deep dive | [../refrigeration/thermoelectric-peltier-cooling-research.md](../refrigeration/thermoelectric-peltier-cooling-research.md) |
| Cooling analysis for cloud chambers | [../refrigeration/cloud-chamber-cooling-research.md](../refrigeration/cloud-chamber-cooling-research.md) |
| Particle detection guide | [cloud-chamber-particle-detection-guide.md](cloud-chamber-particle-detection-guide.md) |
| Physics & history | [../chem/cloud-chamber-research.md](../chem/cloud-chamber-research.md) |
| DIY construction detail | [../diy-cloud-chamber-complete-guide.md](../diy-cloud-chamber-complete-guide.md) |
