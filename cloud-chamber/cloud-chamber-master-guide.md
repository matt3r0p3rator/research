# How to Build a Cloud Chamber: Complete Research Guide

*Compiled May 19, 2026 — Cross-referenced with [refrigeration research](../refrigeration/master-refrigeration-guide.md)*

---

## Table of Contents

1. [What Is a Cloud Chamber?](#1-what-is-a-cloud-chamber)
2. [The Physics](#2-the-physics)
3. [Choosing a Design](#3-choosing-a-design)
4. [Cooling Requirements & Method Selection](#4-cooling-requirements--method-selection)
5. [Design A — Dry Ice Chamber (Best for Beginners)](#5-design-a--dry-ice-chamber-best-for-beginners)
6. [Design B — Peltier-Cooled Chamber (Permanent Build)](#6-design-b--peltier-cooled-chamber-permanent-build)
7. [Design C — Vapor-Compression Chamber (Museum-Quality)](#7-design-c--vapor-compression-chamber-museum-quality)
8. [Lighting Setup](#8-lighting-setup)
9. [The Ion Scrubber (Electric Field Trick)](#9-the-ion-scrubber-electric-field-trick)
10. [Radiation Sources](#10-radiation-sources)
11. [Reading the Tracks](#11-reading-the-tracks)
12. [Photography](#12-photography)
13. [Troubleshooting](#13-troubleshooting)
14. [Safety](#14-safety)
15. [Cost Summary](#15-cost-summary)
16. [Advanced Experiments](#16-advanced-experiments)

---

## 1. What Is a Cloud Chamber?

A **cloud chamber** is a particle detector that renders the paths of individual subatomic particles visible as white mist trails. When a charged particle (alpha, beta, muon, proton) passes through a layer of supersaturated alcohol vapor, it ionizes gas molecules along its path. Each ion acts as a condensation nucleus, and tiny alcohol droplets grow around them within milliseconds — producing a visible white track that persists for 1–5 seconds.

### Two Types

| Type | Invented | How It Works | DIY Suitability |
|---|---|---|---|
| **Wilson Expansion Chamber** | 1911 (C.T.R. Wilson) | Rapid adiabatic expansion creates momentary supersaturation | Poor — requires precise mechanical piston, ~1 Hz pulsed operation |
| **Diffusion Cloud Chamber** | 1936 (Alexander Langsdorf) | Steady temperature gradient creates continuous supersaturated layer | Excellent — no moving parts, simple construction |

All DIY builds use the **diffusion** type. It is continuously sensitive (no dead time) and requires no mechanical cycling.

### Historical Milestones

| Year | Discovery | Physicist | Cloud Chamber Role |
|---|---|---|---|
| 1911 | Cloud chamber invented | C.T.R. Wilson | Direct invention; Nobel Prize 1927 |
| 1932 | Positron discovered | Carl Anderson | Track curving opposite to electrons in magnetic field |
| 1936 | Muon discovered | Anderson & Neddermeyer | Track too light for proton, too heavy for electron |
| 1947 | Kaon (strange particles) | Rochester & Butler | V-shaped decay tracks from a neutral particle |

---

## 2. The Physics

### Supersaturation

A vapor is **supersaturated** when its partial pressure exceeds the equilibrium vapor pressure at that temperature:

$$S = \frac{p}{p_\text{sat}(T)} > 1$$

The system is metastable — it will remain vapor until a nucleation event triggers condensation. The **Kelvin equation** shows that very small droplets require higher $S$ to grow because surface tension raises their effective vapor pressure:

$$\ln S = \frac{2\gamma V_m}{rRT}$$

where $\gamma$ = surface tension, $V_m$ = molar volume, $r$ = droplet radius, $R$ = gas constant, $T$ = temperature.

### Why Ions Create Tracks

When a charged particle passes through the vapor, it strips electrons from air molecules via Coulomb interactions — the **ionization** described by the Bethe-Bloch formula:

$$-\frac{dE}{dx} = \frac{4\pi z^2 e^4 N_A Z \rho}{m_e v^2 A} \left[\ln\frac{2 m_e v^2}{I(1-\beta^2)} - \beta^2\right]$$

Key consequences:
- **High charge** ($z$) → high ionization density → **thick tracks** (alpha: $z=2$ → 4× ionization of a proton at same speed)
- **Low speed** ($v \to 0$) → high ionization → tracks get brighter near the end (Bragg peak)
- **High speed** (relativistic $\beta \to 1$) → minimum ionization → thinnest tracks (muons)

Each ion pair created acts as a condensation nucleus. Droplets (~10–100 µm) grow around each ion within milliseconds, making the track visible.

### The Diffusion Chamber's Sensitive Layer

In a diffusion cloud chamber:
- The **warm top** (~20–40 °C) holds a felt pad soaked in 99% isopropyl alcohol (IPA); it evaporates continuously.
- Vapor diffuses downward toward the **cold plate** (−26 °C minimum; −35 to −78 °C optimal).
- In a narrow zone ~1–3 cm above the cold plate, the vapor concentration exceeds $p_\text{sat}(T)$ — this is the **sensitive zone**.
- This layer is *continuously* supersaturated; tracks appear at any moment.

---

## 3. Choosing a Design

```
Do you want to build once and not buy consumables?
  YES → Do you want a permanent display or museum quality?
    YES → Design C (vapor compression, ~$500–800)
    NO  → Design B (Peltier cascade, ~$141–305, no recurring costs)
  NO  → Design A (dry ice, ~$76–155 + ~$10/session)

Are you just experimenting for the first time?
  → Design A — fastest to build, cheapest, excellent performance
  
Do you want best track quality regardless of complexity?
  → Design A (dry ice at −78°C gives thicker sensitive layer than Peltier)
  
Do you want it to run all day unattended?
  → Design B or C
```

---

## 4. Cooling Requirements & Method Selection

> **Full cooling method details are in:** [refrigeration/master-refrigeration-guide.md](../refrigeration/master-refrigeration-guide.md)

### Temperature Targets

| Region | Temperature | Notes |
|---|---|---|
| Cold plate (bottom) — minimum | −26 °C | Absolute floor; only faint tracks possible |
| Cold plate — practical | −30 to −35 °C | Acceptable; cosmic muons visible |
| Cold plate — good | −35 to −50 °C | Clear alpha and beta tracks |
| Cold plate — excellent | −50 to −78 °C | Thick sensitive layer; dry ice range |
| Warm top | 20–40 °C | Room temperature works; active heating (IR lamp, 5–15 W) improves quality |
| Total gradient | 50–65 °C across 5–10 cm height | More gradient = thicker sensitive layer |

### Cooling Method Comparison for Cloud Chambers

| Method | Cold Plate Achievable | Session Length | Complexity | Cost | Recommended? |
|---|---|---|---|---|---|
| **Dry ice (−78.5 °C)** | −50 to −70 °C (plate) | 1–3 hr/load | Very low | ~$10/session | ✅ Best for beginners |
| **Single-stage Peltier + air cooling** | −10 to −20 °C | Indefinite | Low | ~$60 | ❌ Below minimum threshold |
| **Single-stage Peltier + water cooling** | −28 to −35 °C | Indefinite | Medium | ~$150 | ⚠️ Marginal; works with good source |
| **2-stage cascade Peltier + water cooling** | −45 to −55 °C | Indefinite | Medium-high | ~$200–250 | ✅ Best Peltier option |
| **Vapor compression (mini fridge compressor)** | −35 to −45 °C | Indefinite | High (brazing) | ~$300–500 | ✅ Best permanent build |
| **Liquid nitrogen** | −170 to −190 °C | 30 min/L | Medium | Variable | ❌ Overkill; IPA freezes at −89 °C |

> **Critical warning:** IPA freezes at **−89 °C**. Using LN₂ would freeze the alcohol solid on the plate, destroying chamber operation. Dry ice at −78.5 °C is the practical lower limit for IPA chambers.

### Why Air-Cooled Single Peltier Fails

A single TEC1-12706 or TEC1-12715 has $\Delta T_\text{max} \approx 66$ °C with no heat load. At 25 °C ambient with air cooling, the hot side reaches 55–60 °C, leaving only 55–60 °C of $\Delta T$ — giving a cold side of only **−10 to −20 °C**, below the −26 °C minimum. Air cooling alone is not sufficient for a single-stage Peltier cloud chamber.

### Cross-Reference: Peltier (TEC) Details

From [thermoelectric-peltier-cooling-research.md](../refrigeration/thermoelectric-peltier-cooling-research.md):
- **TEC1-12706:** 12 V / 6 A, 72 W input, 40×40 mm
- **TEC1-12715:** 12 V / 15 A, 180 W input, 40×40 mm
- For a 2-stage cascade, use **2× TEC1-12710** (Stage 1, hot-side) + **1× TEC1-12706** (Stage 2, cold plate)
- Thermal interface material: Arctic MX-4 or Kryonaut (4–12 W/m·K) at every interface
- Cold plate material: 3–5 mm copper (401 W/m·K) or 6061 aluminum

### Cross-Reference: Vapor Compression Details

From [vapor-compression-refrigeration-research.md](../refrigeration/vapor-compression-refrigeration-research.md):
- Use a Danfoss/Secop BD35F or BD50F hermetic compressor, or a repurposed chest-freezer compressor
- Refrigerant: R134a, R290 (propane), or R600a
- Achieved cold plate: −35 to −45 °C (indefinite runtime)
- Requires brazing skills or pre-sealed refrigerant loop
- Weight: ~20 kg for the compressor unit alone

---

## 5. Design A — Dry Ice Chamber (Best for Beginners)

### Bill of Materials

| # | Item | Specification | Approx. Cost |
|---|---|---|---|
| 1 | Clear chamber enclosure | 10-gal glass aquarium (50×25×30 cm) or clear acrylic box (30×25×15 cm interior) | $15–40 |
| 2 | Aluminum cold plate | 6061 alloy, 3–6 mm thick, sized to fit aquarium bottom | $10–20 |
| 3 | Black velvet or dense felt | Lines the top face of the cold plate (interior floor) | $5–10 |
| 4 | Felt wicking strip | 1.5–2.5 cm wide, lines upper interior perimeter | Included above |
| 5 | **99% Isopropyl alcohol** | MUST be ≥99% — 70% and 91% do not work | $10–18 (500 mL) |
| 6 | Dry ice | 3–8 lbs per 2-hour session (blocks preferred over pellets) | $5–20/session |
| 7 | Styrofoam cooler | Holds dry ice beneath the plate; 6-qt camping cooler | $5–15 |
| 8 | LED strip or bright flashlight | Cool-white (5000–6500 K), ≥500 lumens | $8–20 |
| 9 | Black matte spray paint | If not using velvet on cold plate | $5 |
| 10 | Rubber/foam gasket (optional) | Closed-cell foam weatherstripping; seals lid | $5–8 |
| 11 | Cryogenic gloves | For dry ice handling | $10–20 |
| 12 | Thermal conductive pad (optional) | Between dry ice and aluminum plate | $5–10 |

**One-time cost: ~$76–156** | **Per session (dry ice): ~$10**

### Step-by-Step Construction

#### Step 1 — Prepare the Chamber
1. If using an aquarium, lay it on its side so one long glass wall is the floor and the opening faces you.
2. **Line or paint the cold plate matte black.** Glue black velvet to the top face of the aluminum plate (the interior-facing side). Alternatively, spray 2–3 coats of matte black paint.
3. **Attach the felt wicking strip.** Cut felt into 2 cm wide strips. Glue them around the **upper interior perimeter** of the chamber walls, 1–2 cm from the top edge. This is the alcohol vapor source.

#### Step 2 — Prepare the Lid
Cut plywood or plexiglass for the lid. Apply closed-cell foam weatherstripping around the perimeter. Leave a ~3 mm vent hole to prevent pressure buildup (never seal completely airtight).

#### Step 3 — Saturate the Felt
Apply **99% IPA** to the felt wicking strip with a syringe or squeeze bottle. Amount: **15–25 mL** for a 30×20 cm chamber. The felt should be damp but not dripping. Excess causes a "rainstorm" that obscures tracks.

#### Step 4 — Add Dry Ice
1. Place 3–5 lbs of dry ice into the styrofoam cooler. Break into flat slabs for better contact.
2. **Set the aluminum cold plate directly on the dry ice.** Wait 2–3 minutes to equilibrate.
3. Lower the chamber enclosure onto the cold plate. The plate becomes the chamber floor.

#### Step 5 — Wait for Gradient (5–10 min)
Put the lid on. The temperature gradient takes 5–10 minutes to develop:
- Top (felt level): ~20–25 °C (room temperature)
- Bottom (plate): −50 to −70 °C
- Sensitive zone: 5–25 mm above the plate

#### Step 6 — Illuminate and Observe
- Set up grazing-angle lighting (see §8)
- Darken the room completely
- Wait 2 minutes for your eyes to dark-adapt
- First tracks typically appear 5–10 minutes after placing on dry ice
- Best performance: 10–60 minutes into the session

#### Operating Notes
- **Session length:** ~1–3 hours per load; replenish dry ice to extend
- **IPA replenishment:** Add 5–10 mL to the felt if tracks fade after ~45 min
- **Equilibrium indicator:** A thin (~1 mm) pool of condensed IPA forming on the cold plate means the vapor cycle is balanced — best track visibility is 5–10 min after this appears

---

## 6. Design B — Peltier-Cooled Chamber (Permanent Build)

> See [cloud-chamber-cooling-research.md](../refrigeration/cloud-chamber-cooling-research.md) for detailed TEC specifications.

### Why Two Stages Are Required
A single-stage TEC with air cooling only reaches −10 to −20 °C — below the −26 °C minimum. A **two-stage cascade** with water cooling reliably reaches **−45 to −55 °C**, well into the "excellent" range.

### TEC Stack Configuration (Bottom to Top)
```
[Heat sink fins + 2× 120mm fans — removes all heat to ambient]
         ↓
[2× TEC1-12710 in parallel @ 12 V / 10 A each] ← Stage 1 (hot side)
         ↓
[10 mm copper intermediate spreader plate]
         ↓
[1× TEC1-12706 @ 8–10 V / 6 A via buck converter] ← Stage 2 (cold side)
         ↓
[3–5 mm copper cold plate — polished top surface]
         ↓
[Black velvet or felt on top face]
         ↓
[Chamber sits here]
```

For best results, replace the air-cooled heat sink with a **CPU water block → pump → 240 mm radiator + 2× 120mm fans**, which brings the hot-side temperature to 30–40 °C and pushes the cold plate to −45 to −50 °C no-load, −38 to −45 °C operating.

### Bill of Materials

| # | Item | Model / Spec | Approx. Cost |
|---|---|---|---|
| 1 | Stage 1 TECs | 2× TEC1-12710 (10 A, 12 V, 40×40 mm) | $10–18 |
| 2 | Stage 2 TEC | 1× TEC1-12706 (6 A, 12 V, 40×40 mm) | $5–10 |
| 3 | CPU heat sink | Tower style, ≥120 mm fan (e.g., Noctua NH-D15) | $30–80 |
| 4 | Copper cold plate | 5 mm thick, 6 cm × 6 cm minimum, lapped flat | $10–20 |
| 5 | Copper intermediate plate | 10 mm thick, same footprint as TECs | $10–15 |
| 6 | Thermal paste | Arctic MX-4 or Kryonaut | $6–12 |
| 7 | Power supply | ATX PSU (≥20 A on 12 V rail) or dedicated 12 V/20 A supply | $15–40 |
| 8 | DC-DC buck converter | For running Stage 2 TEC at 8–10 V | $5–10 |
| 9 | Chamber enclosure | Same as Design A | $15–40 |
| 10 | Black felt/velvet | Same as Design A | $5–10 |
| 11 | Felt wicking strip | Same as Design A | Included |
| 12 | 99% IPA | Same as Design A | $10–18 |
| 13 | LED strip light | Cool-white 5000–6500 K | $8–20 |
| 14 | K-type thermocouple + meter | Monitor cold plate temp (±1–2 °C) | $5–15 |
| 15 | Closed-cell foam insulation | 20–25 mm XPS around TEC stack sides | $5–10 |
| 16 | Rubber gasket | Weatherstripping for lid | $5–8 |

**One-time total: ~$144–326** | **No recurring costs**

### Step-by-Step Construction

#### Step 1 — Assemble TEC Stack
1. Sand all mating surfaces with 400–600 grit, then 1500 grit. Surfaces must be as flat as possible.
2. Apply thermal paste in a thin uniform film on every interface (not a pea-sized blob).
3. Stack (bottom to top): heat sink → 2× Stage 1 TECs → copper intermediate plate → Stage 2 TEC → cold plate.
4. Clamp with M3/M4 stainless bolts. Torque evenly to ~2–3 N·m. TEC ceramics are brittle — do not overtighten.
5. Wrap the TEC stack sides in 20 mm closed-cell foam to prevent frost on the ceramics and reduce heat leakback.

#### Step 2 — Wiring
- **Stage 1 TECs (parallel):** Both red (+) → 12 V rail; both black (−) → ground. Combined draw: ~18–20 A. Use 14 AWG wire minimum.
- **Stage 2 TEC:** Connect to buck converter set to 8–10 V (running at full 12 V reduces COP and can overheat Stage 2).
- **Fan:** 12 V from PSU.
- **All grounds common.**

#### Step 3 — Dry Run Test
Power the stack, monitor cold plate temperature every 2 minutes:
- 5 min: 0 to −10 °C
- 15 min: −25 to −40 °C
- 30 min (steady-state): −40 to −65 °C

If heat sink is too hot to touch, thermal dissipation is inadequate — add more fan, bigger heat sink, or switch to water cooling.

#### Step 4 — Install the Chamber
1. Glue black velvet to the top (interior) face of the cold plate.
2. Apply silicone RTV or weatherstripping around the cold plate perimeter; set the chamber enclosure on top.
3. Install felt wicking strip and saturate with 99% IPA (same as Design A, Step 3).
4. Install lid with small vent hole.

#### Step 5 — Power Up
- Power the TEC stack. Monitor cold plate temperature.
- Do not add alcohol until plate reaches −25 °C.
- Best track visibility at −35 °C and colder.
- Equilibration time: 15–30 minutes. Tracks appear ~5 min after plate stabilizes.

---

## 7. Design C — Vapor-Compression Chamber (Museum-Quality)

> Full refrigerant cycle details: [vapor-compression-refrigeration-research.md](../refrigeration/vapor-compression-refrigeration-research.md)

### Overview
The "phase-change" design used by professional/museum cloud chamber manufacturers (e.g., Cloudylabs). Uses a hermetic compressor — essentially a mini fridge — to cool the plate to −35 to −45 °C indefinitely.

### Key Components
- **Compressor:** Danfoss/Secop BD35F or BD50F hermetic compressor; or repurposed chest-freezer compressor
- **Refrigerant:** R134a, R290 (propane — flammable, but more environmentally friendly), or R600a
- **Evaporator plate:** Custom copper/aluminum plate soldered or brazed to the refrigerant loop; this becomes the cloud chamber cold plate
- **Condenser:** Air-cooled (fan + fins) or water-cooled
- Achieves **−35 to −45 °C** cold plate with indefinite runtime; no consumables

### Why Choose This
- Best for large chambers (40×40 cm+) where multiple TECs would be needed
- Uniform temperature across large surfaces
- Silent operation if compressor is isolated
- Powers a display that runs 24/7

### Why Not Start Here
- Requires brazing or silver-soldering skills for refrigerant loop
- Pre-sealed compressor loops (~$100–200) available but need modification
- Total weight ~15–25 kg
- Cost: ~$300–800 depending on compressor source and whether you braze or buy a loop

---

## 8. Lighting Setup

Lighting is as critical as temperature. The wrong lighting makes tracks invisible even in a perfect chamber.

### Geometry
- **Angle:** 5–15° above horizontal — nearly horizontal **grazing-angle** illumination. Overhead lighting does not work.
- **Direction:** From one side of the chamber, aimed at the sensitive zone (1–3 cm above cold plate).
- **Distance:** 10–30 cm from the side wall.

### Light Sources

| Source | Pros | Cons |
|---|---|---|
| **LED strip (cool-white 6000 K)** | Even, continuous illumination along full wall | Must aim precisely at sensitive zone |
| **Bright LED flashlight** (≥500 lm) | Concentrated, tuneable angle | Needs clamping |
| **Green laser (532 nm)** | Extremely high contrast, looks spectacular | Eye hazard; must diffuse the beam |

### Practical Setup
1. Mount a bright LED strip outside the chamber, pressed against one side wall.
2. Tilt the strip or flashlight so the beam sweeps across the sensitive zone at ~5–10° below horizontal.
3. **Completely darken the room.** Ambient light kills contrast.
4. Dark-adapt your eyes for ~2 minutes before observing.

---

## 9. The Ion Scrubber (Electric Field Trick)

### What It Does
A high-voltage electrode (~1–5 kV) suspended above the cold plate sweeps lingering ion pairs away between tracks, clearing the sensitive zone and sharpening track contrast. Also suppresses background condensation "rain."

### Is It Required?
**No.** Tracks are visible without it. But it dramatically improves clarity for photography or with a strong radioactive source.

### Implementation
- **Electrode:** Aluminum foil plate or screen, ~80% of interior footprint, suspended 8–10 cm above the cold plate on nylon standoffs
- **HV source options:**
  - Budget: Negative ion generator module (~$10 on AliExpress), outputs ~3–5 kV
  - Better: ZVS flyback driver + Cockcroft-Walton voltage multiplier (adjustable, well-documented online)
  - Best: Benchtop HV supply (adjustable 0–10 kV)
- **Safety resistor:** **MANDATORY** — 10–50 MΩ, 2 W, in series. Limits fault current to <100 µA even if touched directly.
- **Wiring:** Positive terminal of HV supply → safety resistor → electrode plate. Cold plate and HV supply negative → earth ground.
- **Voltage setting:** +1 to +5 kV. Experimentally documented optimum ~4.6 kV.

> **Safety:** Always include the series resistor. Discharge the electrode before opening the chamber. Never omit the resistor if children are present.

---

## 10. Radiation Sources

### No Source Required — Just Watch Cosmic Rays

Even with no artificial source, a cloud chamber shows **5–15 muon tracks per minute** from cosmic rays, plus occasional electron secondaries and rare nuclear interactions.

### Common Sources

| Source | Track Type | Activity / Notes | Acquisition |
|---|---|---|---|
| **Cosmic ray muons** | Long, straight, thin | ~10,000/m²/min at sea level; more at altitude | Free — always present |
| **Americium-241** (smoke detector) | Short (3–4 cm), thick, straight alpha tracks | ~1 µCi per detector; most reliable alpha source | Old ionization smoke detectors; do not extract from sealed holder |
| **Thoriated lantern mantles** (old, pre-1990) | Multiple alpha lengths (thorium decay chain) + betas | ~1% ThO₂; burn the mantle, use the ash | Old camping supply; online surplus |
| **Uranium glass (Vaseline glass)** | Alpha tracks, low intensity | 2–25% UO₂; fluoresces green under UV | Antique stores, eBay |
| **Radon gas** | Alpha tracks from Rn daughters | 3.82-day half-life; diffuses into chamber from basement air | Leave chamber open in a radon-elevated basement |
| **Potassium chloride (NoSalt)** | Faint beta tracks (⁴⁰K) | ~15 Bq per tablespoon; very weak | Grocery store; works only in excellent chambers |

### Am-241 Legal Note (USA)
Possession of the sealed Am-241 source from an ionization smoke detector is legal for personal/educational use under NRC exemptions. Do not extract the Am-241 from its gold-foil sealed holder — use the intact sealed button as your source. Intentionally releasing or concentrating the material is prohibited under 10 CFR Part 30.

---

## 11. Reading the Tracks

### Quick Identification Table

| Track Appearance | Particle | Why |
|---|---|---|
| **Thick, straight, defined length, abrupt end** | Alpha (α) | Heavy ($m \approx 3727$ MeV/$c^2$), charge $z=2$ → 4× ionization; Bragg peak at range end |
| **Thin, wispy, curling, variable length** | Beta/electron (β) | Light ($m = 0.511$ MeV/$c^2$) → large Coulomb scattering deflections |
| **Thin, ruler-straight, full chamber length** | Muon (cosmic) | $m = 106$ MeV/$c^2$, minimum-ionizing at GeV energies, almost no scattering |
| **Two tracks from one invisible point, curving opposite ways** | Electron-positron pair (γ conversion) | Requires high-Z converter plate inside chamber + $E_\gamma > 1.022$ MeV |
| **Multiple tracks exploding from one point** | Nuclear star | Cosmic ray or neutron disintegration of a nucleus |
| **Short, fat, slightly curved** | Proton (recoil) | Intermediate between alpha and muon |

### The Bethe-Bloch Insight

The key ratio: alpha tracks are **~16× thicker** than muon tracks because the ionization scales as $z^2 / \beta^2$ — alpha has $z=2$ (giving $z^2 = 4$) and is much slower than a GeV muon (giving higher $1/\beta^2$), so combined the effect is roughly $4 \times 4 = 16$.

### Magnetic Field Analysis

If you add a magnetic field $B$ perpendicular to the sensitive layer (e.g., strong neodymium magnets above and below the chamber), tracks curve. The radius of curvature directly gives momentum:

$$p \, [\text{GeV}/c] = 0.3 \cdot B \, [\text{T}] \cdot r \, [\text{m}]$$

- **Positive** vs. **negative** charge → curves in opposite directions
- Anderson's discovery of the positron (1932): a track that curved the "wrong" way for an electron in a vertical magnetic field — same mass as an electron, but positive charge

---

## 12. Photography

| Parameter | Recommendation |
|---|---|
| ISO | 800–3200 (higher if tracks are faint) |
| Aperture | f/2.8–f/4 |
| Shutter speed | 1/60–1/30 s (catch tracks before they disperse) |
| Focus | Manual, focused on the sensitive zone (~1–3 cm above cold plate) |
| White balance | Auto or daylight |
| Room | Fully darkened; only the side-lighting active |
| Tripod | Essential — no hand-holding at these exposures |

**Video:** Use 60 fps if available; tracks at 1/60 s frames are often not captured at 30 fps. DSLR or mirrorless outperforms phone cameras significantly in low light.

**Post-processing:** Boost contrast and apply a mild unsharp mask. ImageJ (free) can stack frames to show track statistics over time.

---

## 13. Troubleshooting

### No Tracks

| Symptom | Most Likely Cause | Fix |
|---|---|---|
| No tracks after 20+ min | Cold plate not cold enough | Measure with thermocouple; must be <−26 °C |
| No tracks, plate is cold | IPA below 99% purity | Replace with 99% IPA — 70% or 91% will not work |
| No tracks, IPA is correct | Felt is dry | Re-saturate the wicking strip |
| Fog everywhere, no discrete tracks | Too much IPA | Blot felt; reduce to damp, not dripping |
| Nothing visible | Room not dark enough | Eliminate all ambient light |
| Nothing visible | Light angle wrong | Move light to nearly horizontal (5–15°) |

### Poor Tracks

| Symptom | Cause | Fix |
|---|---|---|
| Tracks blur instantly | Air currents inside chamber | Seal lid better; move away from HVAC vents |
| Whole chamber fills with fog | Plate not cold enough or too much IPA | Wait longer; reduce IPA amount |
| Tracks curve strangely | Cold plate not flat | Replace or lap the plate flat |
| Background haze won't clear | No ion scrubber | Add HV electrode (§9) or wait for natural clearing |

### Peltier-Specific

| Symptom | Fix |
|---|---|
| Cold plate won't go below −20 °C | Heat sink inadequate; add fan or switch to water cooling |
| TEC module gets very hot and fails | Thermal paste incorrectly applied; hot side not dissipating; reduce Stage 2 voltage |
| TEC modules fail repeatedly | Thermal cycling stress; use slow power ramp; ensure even clamping |
| Cold plate below target but no tracks | Temperature gradient too shallow — check that top is at room temperature or warmer |

---

## 14. Safety

### Dry Ice
- **Never** handle with bare skin — cryogenic burns at contact. Use insulating gloves.
- **Never** seal dry ice in a fully airtight container — CO₂ pressure buildup risk.
- In enclosed spaces (car, small room), subliming dry ice displaces oxygen. Ventilate.

### Isopropyl Alcohol (99% IPA)
- Flash point 11.7 °C — extremely flammable. Keep away from all ignition sources (flames, sparks).
- Vapor is denser than air and will pool at low points. Operate with ventilation.

### Electric Field (Ion Scrubber)
- Always install the 10–50 MΩ series safety resistor.
- Discharge the electrode before opening the chamber.
- Treat as a shock hazard; do not allow unsupervised children near the HV components.

### Radiation Sources
- **Cosmic rays:** No precautions needed.
- **Am-241 (smoke detector):** Keep the source sealed. Do not grind, crush, or extract the Am-241 foil. Wash hands after handling.
- **Thoriated mantles:** Handle ash with gloves; do not inhale. Ash is an insoluble solid — internal contamination risk if ingested/inhaled.
- **General:** Exposure from these small, sealed, low-activity sources is minuscule — comparable to or less than normal background. The main hazards are accidental ingestion or inhalation of loose radioactive material, not external exposure.

---

## 15. Cost Summary

### Design A — Dry Ice

| Category | Budget | Full |
|---|---|---|
| Aquarium or acrylic box | $20 | $40 |
| Aluminum cold plate | $12 | $20 |
| Black felt/velvet | $6 | $10 |
| 99% IPA (500 mL) | $10 | $15 |
| LED flashlight or strip | $10 | $20 |
| Styrofoam cooler | $5 | $12 |
| Gloves, misc hardware | $8 | $15 |
| Rubber gasket (optional) | — | $8 |
| Black matte paint | $5 | $5 |
| **One-time total** | **~$76** | **~$145** |
| Dry ice per session (5 lbs) | $10 | $10 |
| **First session total** | **~$86** | **~$155** |

### Design B — 2-Stage Peltier Cascade

| Category | Budget | Full |
|---|---|---|
| 2× TEC1-12710 Stage 1 | $12 | $18 |
| 1× TEC1-12706 Stage 2 | $6 | $10 |
| CPU heat sink + fan | $20 | $60 |
| Copper cold + intermediate plates | $15 | $30 |
| Thermal paste | $6 | $12 |
| Power supply | $15 | $45 |
| Buck converter | $5 | $10 |
| Chamber enclosure | $20 | $40 |
| Black felt/velvet + IPA | $16 | $28 |
| LED strip | $8 | $20 |
| Thermocouple + meter | $8 | $15 |
| Insulation foam + wiring | $13 | $18 |
| **One-time total** | **~$144** | **~$306** |
| Recurring costs | **$0** | **$0** |

### Head-to-Head

| Criterion | Dry Ice | Peltier 2-Stage |
|---|---|---|
| First-session cost | $86–155 | $144–306 |
| Long-term per-session cost | +$10–20 | ~$0 (electricity only) |
| Cold plate temp | −50 to −70 °C | −35 to −65 °C |
| Track visibility | Excellent | Good to Excellent |
| Session length | 1–3 hr/load | Unlimited |
| Setup time | 10–15 min | 20–40 min (cold soak) |
| Portability | High (no mains power) | Low (AC required) |
| Complexity | Very low | Moderate |
| Best for | Beginners, demos | Permanent display |

---

## 16. Advanced Experiments

### Multi-Isotope Alpha Histogram
Use multiple alpha sources (Am-241, thoriated mantle ash, uranium glass). Each isotope produces tracks of a specific length proportional to $E_\alpha^{3/2}$. Photograph and measure track lengths — plot a histogram to identify isotopes by energy.

### Muon Angular Distribution
Photograph the chamber for 30–60 minutes. Measure the zenith angle of each muon track. Cosmic muon flux follows an $\approx \cos^2\theta$ distribution — verify this experimentally.

### Pair Production with Lead Converter
Insert a 1–3 mm lead sheet inside the chamber. Hard gamma rays (≥1.022 MeV) interact with lead nuclei to produce electron-positron pairs. In a magnetic field, the two tracks curve in opposite directions — directly demonstrating antiparticles.

### Muon Decay Signature
Extremely rare but observable in a well-optimized chamber: a muon stops in the sensitive layer, then decays ($\mu^- \rightarrow e^- + \bar{\nu}_e + \nu_\mu$), and the resulting electron track begins at the muon's stopping point with a short spiral.

### Magnetic Field Momentum Measurement
Mount strong neodymium magnets above and below the chamber. Photograph tracks and measure their radius of curvature using the **sagitta method** (measure the perpendicular distance from the chord midpoint to the arc). Apply $p = 0.3Br$ to calculate momentum. Compare measured muon momenta to the known sea-level spectrum (~3–4 GeV mean).

---

## Related Files in This Workspace

| File | Contents |
|---|---|
| [refrigeration/master-refrigeration-guide.md](../refrigeration/master-refrigeration-guide.md) | All cooling methods, decision guide, temperature ranges |
| [refrigeration/thermoelectric-peltier-cooling-research.md](../refrigeration/thermoelectric-peltier-cooling-research.md) | TEC physics, module specs, cascade design, Bi₂Te₃ synthesis |
| [refrigeration/vapor-compression-refrigeration-research.md](../refrigeration/vapor-compression-refrigeration-research.md) | Compressor cycles, refrigerant choices, DIY compressor notes |
| [refrigeration/cloud-chamber-cooling-research.md](../refrigeration/cloud-chamber-cooling-research.md) | Detailed cooling analysis specific to cloud chambers |
| [cloud-chamber/cloud-chamber-particle-detection-guide.md](cloud-chamber-particle-detection-guide.md) | Full particle detection guide, quantitative track analysis |
| [chem/cloud-chamber-research.md](../chem/cloud-chamber-research.md) | Physics history, Bethe-Bloch, discoveries, supersaturation theory |
| [diy-cloud-chamber-complete-guide.md](../diy-cloud-chamber-complete-guide.md) | Full construction guide with detailed step-by-step instructions |
