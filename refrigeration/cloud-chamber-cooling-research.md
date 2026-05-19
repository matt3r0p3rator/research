# DIY Diffusion Cloud Chamber — Cooling Requirements Research

**Date:** May 2026  
**Purpose:** Technical reference for building a Peltier-cooled diffusion (Langsdorf) cloud chamber

---

## 1. Temperature Gradient Required

A diffusion cloud chamber works by maintaining a steep vertical temperature gradient across the chamber volume, creating a layer of **supersaturated alcohol vapor** just above the cold plate. This is the "sensitive zone" where particle tracks form.

| Region | Target Temperature | Notes |
|---|---|---|
| **Cold plate (bottom)** | −25°C to −40°C | Minimum threshold: −25°C (Wikipedia); optimal: −30 to −40°C |
| **Warm top** | +20°C to +40°C | Room temp is the floor; active heating improves quality |
| **Total gradient** | ~50–65°C | Across a chamber height of ~5–10 cm |
| **Sensitive layer height** | ~5–10 mm | Just above cold plate — colder = thicker sensitive layer |

The **colder the plate, the thicker and more visible the sensitive layer**, and the higher the droplet density on each track. Cloudylabs (an expert who has built 13+ thermoelectric chambers) states: *"The colder the surface, the more you have molecules of supersaturated vapour. The tracks have a bigger density and the thickness of the sensible layer increases."*

IPA's freezing point is −89°C, well below any cooling method used here, so it stays liquid throughout.

---

## 2. Standard Cold Plate Temperatures for IPA

- **Absolute minimum for any track visibility:** −25°C to −26°C (confirmed by Wikipedia and Cloudylabs)
- **Typical DIY target (IPA):** −30°C to −35°C — produces clear, regular tracks
- **Optimal / high-quality operation:** −35°C to −40°C — thick sensitive layer, dense droplets, excellent visibility
- **Phase-change (compressor) level:** −40°C — uniform large-area coverage; best track quality

Isopropyl alcohol (IPA / isopropanol) is the standard for DIY chambers:
- Readily available as 99% IPA (pharmacy-grade or hardware store)
- Vapor pressure ~44 mmHg at 20°C — sufficient to saturate the chamber at room temperature
- Lower freezing point (−89°C) than ethanol (−114°C) — both work, IPA is generally preferred for availability
- Typical quantity: 5–15 mL soaked into a felt or sponge pad at the top of the chamber per session

---

## 3. Why Dry Ice (−78°C) Is the Traditional Choice

Dry ice (solid CO₂) sublimes at **−78.5°C at atmospheric pressure**, making it the simplest and most foolproof cooling source for hobbyist cloud chambers.

**Advantages:**
- Delivers far more cold than the minimum needed — generous safety margin
- No electricity, no pumps, no electronics
- Zero setup time: place metal plate on dry ice block, wait 10–15 minutes
- The large ΔT means even poor thermal contact still works
- Copper or aluminum plate resting directly on dry ice achieves −60°C to −70°C plate surface

**Practical specifics:**
- Use 3–5 kg of dry ice pellets or a flat slab per session
- Consumption rate: ~1–2 kg/hour sublimation depending on insulation
- Session duration: typically 1–2 hours per load
- Can extend with styrofoam insulation around sides of the dry ice bath
- Replenishment required for sessions longer than 2 hours

**Disadvantages:**
- Consumable — must be purchased or made
- Not available everywhere; dry ice suppliers often sell in minimum quantities (5–10 kg)
- Cannot run unattended for hours without refilling
- CO₂ sublimation produces gas — must not be used in sealed/unventilated rooms in large quantity

**Why it works so well:** At −78°C, the plate surface is ~100°C colder than the room-temperature top. The very steep gradient over 5–10 cm of chamber height produces an exceptionally thick sensitive zone. The surplus cold also means the alcohol rain (condensed droplets) re-freezes on the plate surface cleanly.

---

## 4. Peltier (TEC) Coolers as an Alternative

### 4.1 Module Specifications

The two most common modules in DIY cloud chamber builds:

| Spec | **TEC1-12706** | **TEC1-12715** |
|---|---|---|
| Rated voltage | 12 V | 12 V |
| Rated current | 6 A | 15 A |
| Max power input | 72 W | 180 W |
| ΔTmax (no load, Th = 27°C) | ~66°C | ~66°C |
| Qmax (max heat pumped, Th = 27°C) | ~50 W | ~130 W |
| Dimensions | 40×40 mm | 40×40 mm |
| Junctions | 127 couples | 127 couples |

Both use bismuth telluride (Bi₂Te₃) thermocouple junctions. The `12706` is the standard "CPU cooler" TEC. The `12715` is the high-current version with significantly more pumping capacity and input power.

**Key principle:** ΔTmax is specified at **zero heat load** (Qc = 0). Under real conditions with a heat load from the alcohol environment, achievable ΔT is lower. The hot side temperature is critical — it must be actively managed.

### 4.2 Single-Stage TEC Performance at 25°C Ambient

The cold side temperature you can achieve depends entirely on **how well you cool the hot side**:

| Hot-Side Cooling Method | Typical Hot-Side Temp | Achievable Cold Side | Cloud Chamber Verdict |
|---|---|---|---|
| Passive heatsink (no fan) | 60–80°C | +5°C to −5°C | Useless |
| Air-cooled (CPU fan + heatsink) | 45–60°C | −10°C to −20°C | Marginal; works barely at −20°C |
| Water-cooled (waterblock + radiator) | 30–40°C | −25°C to −35°C | **Works well** |
| Water-cooled (chilled water loop) | 20–25°C | −35°C to −40°C | **Excellent** |

At 25°C ambient with a good water-cooling loop (CPU waterblock + 240 mm radiator), a **single TEC1-12715 can reach −30 to −35°C cold side** — sufficient for good cloud chamber operation.

**Air cooling with a single TEC1-12706 or 12715 alone is marginal at best.** The hot-side temperature climbs to 50–60°C under load, leaving only a cold side of ~−10°C to −15°C. This is below the −25°C threshold.

Cloudylabs confirms this from direct experience: the air-cooled V3 design with 6 Peltiers "was physically stuck." Adding more Peltiers added too much waste heat for the airflow to handle. Switching to water cooling broke through this barrier.

### 4.3 Cascade (Multi-Stage) TEC Configuration

Cascaded TECs stack modules on top of each other, with the hot side of the upper (cold) stage sitting on the cold side of the lower (hot) stage. Each stage provides additional ΔT.

| Configuration | Achievable Cold Side (25°C ambient, water-cooled base) | Power Draw | Complexity |
|---|---|---|---|
| **Single stage TEC1-12715** | −30°C to −35°C | ~200–250 W | Low |
| **2-stage cascade** (12715 bottom + 12706 top) | −45°C to −55°C | ~280–350 W | Moderate |
| **3-stage cascade** | −65°C to −75°C | ~400–500 W | High; rarely worth it |
| **5-stage cascade** (documented on Wikipedia for cloud chambers) | −80°C to −90°C | Very high | Research lab only |

**Recommended for DIY cloud chamber:** A **2-stage cascade with water cooling on the bottom stage** offers the best balance. The bottom stage (TEC1-12715, water-cooled hot side) achieves ~−5°C to −10°C, which becomes the "hot side" for the top TEC1-12706 stage. The top stage then achieves another −35 to −40°C below that — total cold side: ~−45°C to −55°C.

**Practical rules for cascade:**
- Bottom stage must always be the higher-power module (more Qmax to handle both its own heat pump load AND the heat from the stage above)
- Thermal interface between stages: good thermal paste (Arctic MX-4 or Arctic Silver 5, 4–8 W/m·K) is mandatory; press-fit or clamp together, do not rely on weight alone
- Size matching: bottom stage TEC must be physically larger than or equal to the top stage
- Each stage must be independently powered (separate current, separate voltage control)

### 4.4 Heat Sink and Thermal Interface Requirements

**Critical principle:** A TEC pumps heat from cold side to hot side AND adds its electrical power as heat. A TEC1-12715 at 12 V / 15 A inputs 180 W. If it pumps 50 W of cold-side heat, the hot side must dissipate 180 + 50 = **230 W**. This is the sizing requirement for the heat sink.

| Hot-Side Dissipation | Recommended Cooling |
|---|---|
| 1 × TEC1-12706 (72 W in + 30 W pumped ≈ 100 W hot side) | Large CPU air cooler (Noctua NH-D15 class, ≥94 W TDP) — barely adequate |
| 1 × TEC1-12715 (180 W in + 50 W pumped ≈ 230 W hot side) | **Water block + 240 mm radiator minimum** |
| 2 × TEC1-12715 (460 W in + ~100 W pumped ≈ 560 W hot side) | **Water block + 360 mm+ radiator with high-CFM fans** |
| 2-stage cascade | Water block on bottom stage + 240–360 mm radiator |

**Thermal Interface Materials (TIM):**
- Between TEC hot side and water block: Arctic MX-4, Thermal Grizzly Kryonaut, or similar (4–12 W/m·K)
- Between TEC cold side and cold plate: same thermal paste, ensure flat surfaces — any air gap dramatically degrades performance
- Cold plate material: **copper** preferred (401 W/m·K) over aluminum (237 W/m·K) for cloud chamber use; a 3–5 mm thick copper plate distributes temperature uniformly
- Clamp pressure: 30–60 psi is typical recommended range for TEC modules; use M3/M4 screws with measured torque or spring washers, not just hand-tight

**Condensation management:** The cold side will frost/ice up in open air. The cold plate must be inside the sealed chamber. The TEC module itself should be surrounded by insulating foam (extruded polystyrene or polyurethane foam) to prevent condensation forming on the sides of the module and shorting it.

---

## 5. Why Liquid Nitrogen (−196°C) Is Overkill

Liquid nitrogen (LN₂) boils at **−196°C at atmospheric pressure** — nearly 170°C colder than needed for IPA cloud chambers.

**Occasional uses:**
- Research-grade cloud chambers requiring extremely thick sensitive layers
- Very large-area chambers (>50 × 50 cm) where the extra cold compensates for massive heat load
- Extreme-resolution photography of rare cosmic ray events

**Why it's impractical for DIY:**
- LN₂ is expensive and must be stored in a Dewar flask
- Boils off very quickly (especially in a warm chamber environment)
- Achieves temperatures far below what IPA can use (IPA freezes at −89°C, so the plate would freeze the alcohol before it evaporates)
- Safety hazard: asphyxiation risk in enclosed spaces, cryogenic burns
- No practical benefit over dry ice for standard IPA operation

**If someone wants even colder than dry ice:** Dry ice/acetone slurry reaches −78°C (same as dry ice alone), and dry ice/ethanol slurry also reaches −72°C. For the chamber itself, dry ice is the practical ceiling before phase-change compressors take over.

---

## 6. The Warm Top: Active Heating or Room Temperature?

**Short answer:** Room temperature (~20–25°C) is technically sufficient for basic operation. Active heating significantly improves quality and stability.

**Why the top needs to be warm:**
- IPA must evaporate from the top surface to create the downward vapor flow
- If the top is too cold, evaporation rate drops and the sensitive zone thins
- The gradient must be steep enough for supersaturation to form

**Room temperature (passive):**
- Works for basic operation in a 20–25°C room
- Simple setup: alcohol-soaked felt pad at top, chamber left open at top or sealed with a transparent lid
- Cloud chambers at physics departments typically rely on room temperature for the top

**Active top heating benefits:**
- **Felt heater/resistive heater:** 5–10 W applied to the top felt pad raises evaporation rate; improves sensitive zone thickness
- **Infrared (IR) lamp:** Cloudylabs uses this in the phase-change design — *"without the IR light, the machine will work with no change during a dozen of minutes, then some mist will form on the top and will deteriorate the equilibrium."*
- **Warm top target:** 30–40°C at the top felt/alcohol source gives a ~65–80°C gradient (with −35 to −40°C cold plate)

**Practical recommendation:** For a first build, room temperature top is fine. If tracks are sparse or disappear after 10–15 minutes, add a 5–10 W resistive heater or a small IR lamp to keep the top warm and maintain the evaporation rate.

---

## 7. Alcohol Evaporation Rate and Replenishment

**How it works:**
- Alcohol-soaked felt or foam pad at the top of the chamber is the vapor source
- IPA evaporates naturally at room temperature (vapor pressure 44 mmHg at 20°C)
- Vapor descends through the chamber, cooled by proximity to the cold plate
- Most vapor condenses on the cold plate; a thin layer just above remains supersaturated

**Evaporation rate factors:**
- Chamber volume and height (taller chambers consume more per hour)
- Temperature of the top surface (warmer = faster evaporation)
- Air drafts (should be zero — seal the chamber)

**Typical consumption:** A standard 20 × 20 cm chamber consumes ~2–5 mL of IPA per hour of operation.

**Replenishment approaches:**
| Method | Pros | Cons |
|---|---|---|
| Pipette/dropper through a port | Simple, controlled | Must briefly disturb chamber seal |
| Pre-soaked foam reservoir (large) | Runs 2–4 hours unattended | Must reload between sessions |
| Wick from an external reservoir | Continuous, no intervention | More complex construction |
| Peristaltic micro-pump | Fully automated | Adds complexity/cost |

**Practical rule:** A 3–5 mm thick felt pad (~10 cm²) loaded with ~5 mL of IPA provides ~1 hour of operation. A fresh application every session (recharged with a pipette between runs) is the simplest approach.

**Visible indicator:** When the cold plate has a thin pooled film of condensed IPA (~1 mm deep), the evaporation/condensation cycle is in equilibrium. Tracks become most visible 5–10 minutes after this pool forms.

---

## 8. Vapor Compression (Mini Compressor from a Fridge) as an Alternative

**Yes — this works and is the best permanent solution.** This is exactly what Cloudylabs' "phase-change" cloud chambers use.

**How it works:** A small hermetic refrigeration compressor (the same type in a mini-fridge or car cooler) drives a refrigeration cycle using R134a or R290 refrigerant. The evaporator plate is the cloud chamber's cold plate. Achieves:
- Cold plate temperature: **−35°C to −45°C** (typical), up to **−55°C** with optimized design
- Uniform temperature distribution across large plates (32 × 32 cm demonstrated by Cloudylabs)
- Runs continuously for hours without any consumable
- Stable equilibrium reached in 20–30 minutes after startup

**Practical compressor options:**
- Small chest freezer compressor (surplus/salvage): ~200–400 W, −30°C to −40°C evaporator
- Danfoss BD35F or BD50F variable-speed hermetic compressors: purpose-designed for low-temperature cooling
- Repurposed car fridge compressor (Secop/Danfoss ACC series): 12 V operation possible
- Purpose-built thermoelectric cooler compressor module from China: available ~$80–200 USD

**Cloudylabs experience with phase-change:**
> *"As we can build big surface cooled uniformly at about −40°C with phase change system... It is easy to obtain particles in a cloud chamber. All you need is the right negative temperature (−25°C threshold), a sealed chamber of moderate height and some electrical field."*

**Drawbacks vs. Peltier:**
- Mechanical complexity — requires refrigerant brazing/soldering skills or prefabricated sealed loop
- Weight: 20–30 kg for the compressor assembly alone
- Noise: compressor runs intermittently
- Cannot easily vary cold plate temperature (unlike Peltier via PWM)

**Drawbacks vs. Dry Ice:**
- Cost and complexity of construction (hundreds of dollars, weeks of work)
- Not portable without significant effort

**Verdict:** Vapor compression is overkill for a first build but is the gold standard for a permanent, high-quality, always-ready cloud chamber that can run unattended. It achieves larger surface areas and better track quality than Peltier setups, and beats dry ice for long-term/continuous use.

---

## 9. Temperature Monitoring on the Cold Plate

**Yes — a thermometer is essentially mandatory for reliable operation.**

**Why you need it:**
- You need to confirm the plate is below −25°C before expecting tracks
- Allows detection of thermal equilibrium (when temperature stabilizes = ready)
- Helps diagnose problems (hot side not cooling, poor thermal contact, frost insulation buildup)
- Lets you optimize: colder is better up to the limits of your cooling system

**Sensor types for cold plate monitoring:**

| Sensor | Range | Accuracy | Interface | Notes |
|---|---|---|---|---|
| **K-type thermocouple + digital meter** | −200 to +1350°C | ±1–2°C | Analog display | **Best choice** — cheap, fast response, no calibration needed |
| K-type + Arduino/MAX31855 | −200 to +1350°C | ±2°C | Digital/SPI | Good for logging or display |
| **NTC 10kΩ thermistor** | −50 to +125°C | ±1°C | Analog/ADC | Cheap, works well in range; needs calibration curve |
| DS18B20 digital | −55 to +125°C | ±0.5°C | 1-Wire/digital | Clean digital output; rated to −55°C (marginal) |
| PT100/PT1000 RTD | −200 to +600°C | ±0.5°C | Analog bridge/ADC | More expensive, more accurate |

**Placement:**
- Thermistor or thermocouple tip should be pressed flat against the cold plate surface under a thin layer of thermal paste
- Tape it down with Kapton (polyimide) tape — does not become brittle at −40°C unlike regular tape
- Route the wire out through the foam insulation without creating a thermal bridge

**What to watch for:**
- Cold plate should reach −25°C within 5–10 minutes of startup (TEC) or 15–20 minutes (compressor)
- Tracks appear 5–10 minutes after cold plate stabilizes
- If temperature plateaus above −20°C: hot-side cooling is insufficient; check radiator, pump flow, or thermal paste

---

## 10. Focused Analysis: Peltier Design at 25°C Ambient

### Minimum Achievable Cold-Side Temperature

With **25°C ambient** room temperature:

| Configuration | Hot Side Cooling | Cold Side Achievable | Cloud Chamber Use |
|---|---|---|---|
| Single TEC1-12706, air-cooled | 55°C | ~−11°C | **No — too warm** |
| Single TEC1-12706, water-cooled | 35°C | ~−31°C | **Yes — marginal** |
| Single TEC1-12715, water-cooled | 35–40°C | ~−28°C to −35°C | **Yes — good** |
| TEC1-12715 + TEC1-12706 (2-stage cascade), water-cooled base | 35°C | ~−45°C to −55°C | **Excellent** |
| TEC1-12715 + TEC1-12706 (air-cooled base only) | 55°C | ~−25°C to −30°C | **Marginal** |

The formula for cold-side estimation under zero heat load:
$$T_{cold} \approx T_{hot} - \Delta T_{max} \times \left(1 - \frac{V_{op}}{V_{max}}\right)$$

Under load (real-world), expect 10–20°C less ΔT than the datasheet maximum.

### Best Practical TEC Configuration for a DIY Cloud Chamber

**Recommended: 2-stage cascade, water-cooled**

```
[Cold Plate — aluminum or copper, 3 mm thick]
         |
[TEC1-12706 (top stage, 6A @ 8-10V for temperature control)]
         |
[Small copper spreader plate, 3 mm]
         |  
[TEC1-12715 (bottom stage, 15A @ 12V)]
         |
[CPU Water Block (copper base)]
         |
[Water loop: pump → 240 mm radiator with 2 × 120 mm fans]
```

**Power supply requirements:**
- Bottom TEC1-12715: 12 V / 15 A = 180 W → use a dedicated 12 V / 20 A PSU or ATX 12 V rail
- Top TEC1-12706: 12 V / 6 A = 72 W, but run at reduced voltage (8–10 V) to prevent overcooling and module stress → use a separate 12 V / 6 A supply or buck converter
- Water pump: 12 V / 0.5–1 A (standard PC pump)
- Radiator fans: 12 V / 0.5 A each

**Thermal paste layers:**
- Cold plate → TEC top stage: Arctic MX-4 or Kryonaut
- TEC top stage → copper spreader: Arctic MX-4
- Copper spreader → TEC bottom stage: Arctic MX-4
- TEC bottom stage → water block: Arctic MX-4

**Insulation:** Surround the TEC stack and cold plate bottom/sides with 20–25 mm of extruded polystyrene (XPS) foam. Use silicone RTV or closed-cell foam tape to seal gaps and prevent frost buildup on the TEC ceramic faces (which would eventually crack the module due to ice expansion).

**Expected performance at 25°C ambient:**
- Cold plate: −45°C to −50°C (no heat load)
- Cold plate under operating load (chamber assembled): −38°C to −45°C
- Sensitive layer: 10–15 mm thick
- Time to reach operating temperature: 10–15 minutes
- Track visibility: very clear alpha and beta tracks; cosmic muon tracks visible with patience

---

## 11. Comparison Summary: All Cooling Methods

| Method | Cold Temp | Cost | Session Duration | Portability | Complexity | Best For |
|---|---|---|---|---|---|---|
| **Dry ice** | −60 to −70°C (plate) | Low (consumable) | 1–2 hours/load | Moderate | Very low | **First builds, demos, events** |
| **Air-cooled TEC** | −10 to −20°C | Low | Indefinite | High | Low | Marginal — not recommended |
| **Water-cooled TEC** | −30 to −40°C | Medium | Indefinite | Medium | Medium | **Good permanent builds** |
| **2-stage cascade TEC + water** | −45 to −55°C | Medium-high | Indefinite | Low-medium | Medium-high | **Best TEC option** |
| **Vapor compression (mini compressor)** | −35 to −45°C | High | Indefinite | Low | High | **Best permanent, large-area builds** |
| **Liquid nitrogen** | −170 to −190°C (plate) | High | 30 min/liter | Low | Medium | Overkill; research only |

---

## References / Sources

1. Wikipedia — "Cloud chamber" (consulted May 2026): −26°C minimum threshold, TEC and dry ice as standard methods
2. Cloudylabs (cloudylabs.fr) — first-hand builder documentation for 13+ chambers: temperature targets, multi-stage TEC experience, phase-change compressor details, hot-side cooling requirements
3. Harvard Natural Sciences Lecture Demonstrations — cloud chamber setup notes: dry ice/ethanol bath, 15-minute equilibration time
4. Ferrotec Thermoelectric Reference Guide — TEC performance theory, cascade module design principles
5. TEC1-12706 / TEC1-12715 standard datasheets (Heliios/generic Chinese manufacturers): ΔTmax ≈ 66°C @ Th = 27°C, ratings above
