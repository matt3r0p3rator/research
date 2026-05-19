# Absorption Refrigeration: Comprehensive Research Guide

*Heat-powered refrigeration using chemical working pairs — no compressor required.*

---

## Table of Contents

1. [Thermodynamic Principles](#thermodynamic-principles)
2. [Ammonia-Water (NH₃-H₂O) Systems](#ammonia-water-systems)
3. [Lithium Bromide-Water (LiBr-H₂O) Systems](#libr-water-systems)
4. [Synthesis of Key Materials](#synthesis-of-key-materials)
5. [The Einstein Refrigerator (No Moving Parts)](#the-einstein-refrigerator)
6. [Building an Absorption Refrigerator](#building-an-absorption-refrigerator)
7. [Adsorption Refrigeration (Solid Sorbent)](#adsorption-refrigeration)
8. [Surprising Findings and Open Questions](#surprising-findings)

---

## 1. Thermodynamic Principles

### Vapor-Compression vs. Absorption

| Feature | Vapor-Compression | Absorption |
|---|---|---|
| Primary energy input | Electrical work (shaft) | Heat (thermal) |
| Moving parts | Compressor (many) | Pump (small liquid pump only) |
| COP basis | COP = Q_e / W_comp | COP = Q_e / Q_gen |
| Noise/vibration | Significant | Very low |
| Best heat source temp | N/A | 80–200°C (single-effect); 130–180°C (double-effect) |
| Refrigerants | HFCs, HFOs, CO₂, NH₃ | NH₃ (w/ H₂O absorbent); H₂O (w/ LiBr absorbent) |

The key insight: a small pump raises liquid pressure from absorber to generator. Since liquids are nearly incompressible, this pump work is tiny (~1–3% of heat input). The system converts low-grade heat into refrigeration with minimal electricity.

### Component Descriptions

**Generator (Desorber):** Heat Q_gen drives refrigerant vapor out of "rich solution." High temperature/pressure. Remaining liquid is the "weak solution."

**Condenser:** High-pressure refrigerant vapor condenses, rejecting heat Q_cond to ambient.

**Evaporator:** Low-pressure refrigerant evaporates, absorbing heat Q_evap from refrigerated space (the useful cooling output).

**Absorber:** Refrigerant vapor from evaporator is absorbed into weak solution (exothermic — heat Q_abs rejected to ambient). Now-rich solution pumped back to generator.

**Solution Heat Exchanger (SHX):** Hot weak solution preheats cold rich solution — critical for COP (10–20% improvement).

### Energy Balance and COP

First Law balance:
$$Q_{gen} + Q_{evap} + W_{pump} = Q_{cond} + Q_{abs}$$

Since W_pump is small (~1–3% of Q_gen):
$$\text{COP} = \frac{Q_{evap}}{Q_{gen} + W_{pump}} \approx \frac{Q_{evap}}{Q_{gen}}$$

**Theoretical maximum COP (Carnot limit):**
$$\text{COP}_{max} = \left(1 - \frac{T_a}{T_g}\right) \cdot \frac{T_e}{T_a - T_e}$$

Where all temperatures are in Kelvin: T_g = generator, T_a = ambient (absorber/condenser), T_e = evaporator.

**Example:** T_g = 393 K (120°C), T_a = 308 K (35°C), T_e = 275 K (2°C):
$$\text{COP}_{max} = \left(1 - \frac{308}{393}\right) \times \frac{275}{308-275} = 0.216 \times 8.33 = 1.80$$

Real single-effect systems achieve ~30–50% of this Carnot limit.

### Typical COP Values

| System Type | COP Range | Notes |
|---|---|---|
| Single-effect LiBr-H₂O | 0.65–0.80 | Most common commercial type |
| Single-effect NH₃-H₂O | 0.50–0.70 | Rectifier losses reduce COP |
| Double-effect LiBr-H₂O | 1.00–1.40 | Two-stage heat input |
| Triple-effect LiBr-H₂O | 1.50–1.80 | Requires high-grade heat >160°C |
| GAX (Gen-Absorber eXchange) NH₃-H₂O | 0.70–1.00 | Internal heat recovery |
| Einstein/Platen-Munters (no pump) | 0.10–0.40 | No electricity needed |
| Vapor-compression (reference) | 2.50–5.00 | For comparison |

---

## 2. Ammonia-Water (NH₃-H₂O) Systems

### Why NH₃-H₂O for Sub-Zero Applications

Ammonia boiling point = −33.4°C at atmospheric pressure → evaporator temperatures possible down to −60°C. This is the system of choice for ice-making, food freezing, and industrial refrigeration. LiBr systems cannot go below 0°C.

Trade-off: water is semi-volatile, co-evaporates with NH₃ in generator, requiring rectification.

### Complete Cycle State Points (Typical 0°C Evaporator System)

| Point | Location | Temp | Pressure | NH₃ wt% | Phase |
|---|---|---|---|---|---|
| 1 | Generator exit (vapor) | 100–130°C | 14–18 bar | ~99.5% (after rectifier) | Superheated vapor |
| 2 | Condenser exit | 35–40°C | 14–18 bar | 100% NH₃ | Saturated liquid |
| 3 | Evaporator inlet | -5 to 5°C | 4–5 bar | 100% NH₃ | Two-phase |
| 4 | Evaporator exit | 0–10°C | 4–5 bar | 100% NH₃ | Saturated vapor |
| 5 | Absorber exit / pump inlet | 30–45°C | 4–5 bar | 35–40% (strong) | Saturated liquid |
| 6 | SHX cold side exit | 65–80°C | 14–18 bar | 35–40% | Liquid |
| 7 | Generator exit (weak) | 95–130°C | 14–18 bar | 22–28% (weak) | Near-saturated liquid |
| 8 | Absorber inlet (throttled) | 35–50°C | 4–5 bar | 22–28% | Partially flashed |

**High-side pressure** set by condenser temp: NH₃ saturation at 40°C ≈ 15–16 bar.  
**Low-side pressure** set by evaporator temp: NH₃ saturation at 0°C ≈ 4.3 bar, at −10°C ≈ 2.9 bar, at −30°C ≈ 1.2 bar.

### Solution Concentration

- **Strong solution (rich in NH₃):** 35–42 wt% NH₃ — enters generator
- **Weak solution (poor in NH₃):** 22–30 wt% NH₃ — exits generator

**Circulation ratio:**
$$f = \frac{x_{strong} - x_{weak}}{x_{strong} - x_{vapor}}$$

Typical f = 5–15. Higher f = more pump work and generator heat per unit cooling.

### The Rectifier and Analyzer

**Problem:** Water co-evaporates in generator. At 130°C / 15 bar, generator vapor may be only 90–95% NH₃. Water in evaporator elevates evaporation temperature and can cause ice blockages.

**Analyzer:** Trays/packing above generator where rising vapor contacts descending liquid — enriches vapor to ~95% NH₃ through partial condensation.

**Rectifier (dephlegmator):** Condenser cooled by water or incoming rich solution. Condenses remaining water vapor, which drains back to generator. Achieves >99.5% NH₃ purity.

Heat removed in rectifier (Q_rect) reduces effective COP — this is why NH₃-H₂O COP is lower than LiBr-H₂O.

### Operating Conditions Summary

| Component | Temperature | Pressure | NH₃ Fraction |
|---|---|---|---|
| Generator | 80–170°C | High (10–25 bar) | Weak (22–30 wt%) |
| Rectifier | 50–80°C | High | Enriching to >99% |
| Condenser | 30–40°C | High (10–18 bar) | ~100% NH₃ liquid |
| Evaporator | -20 to +10°C | Low (1.5–6 bar) | ~100% NH₃ |
| Absorber | 30–40°C | Low | Strong (35–42 wt%) |

---

## 3. Lithium Bromide-Water (LiBr-H₂O) Systems

### Overview

In LiBr-H₂O, **water is the refrigerant** and **LiBr is the absorbent**. LiBr solution has vapor pressure far below pure water — this vapor pressure depression drives absorption. Cannot cool below 0°C (water freezes). Used exclusively for air conditioning and chilled water (5–12°C typical output).

### Vacuum Operation

Water must evaporate at 6–10°C for air conditioning. Saturation pressure of water:

| Temperature | Saturation Pressure |
|---|---|
| 5°C | 0.87 kPa |
| 10°C | 1.23 kPa |
| 40°C (condenser) | 7.38 kPa |
| 85°C (generator) | 57.8 kPa |

**Entire system operates under deep vacuum** (0.6–8 kPa). This means no high-pressure containment, but air infiltration is a persistent problem — even microscopic leaks allow non-condensable gases to accumulate in the condenser/evaporator, degrading performance. **Purge systems** must periodically remove accumulated air.

### Single-Effect Cycle Operating Conditions

| Component | Temperature | Pressure | LiBr Concentration |
|---|---|---|---|
| Evaporator | 5–10°C | 0.87–1.23 kPa | N/A (pure water) |
| Absorber | 30–40°C | 0.87–1.23 kPa | 58–62% LiBr |
| Generator | 75–95°C | 6–10 kPa | 62–65% LiBr |
| Condenser | 38–43°C | 6–10 kPa | N/A (pure water) |

**Double-effect cycle:** High-pressure generator at 140–165°C drives a second low-pressure generator. COP improves to 1.0–1.4.

### Crystallization Hazard — Critical Operational Issue

| LiBr wt% | State at 25°C |
|---|---|
| < 50% | Safe |
| 50–60% | Typical operating range |
| ~62% | Upper safe operating limit |
| ~65% at 20°C | Crystallization begins |
| ~70% | Rapidly crystallizing paste |

**Crystallization line equation (approximate):**
$$T_{cr} \approx -130.6 + 567.5x + 8.9x^2 \quad (x = \text{mass fraction, not }\%)$$

At x = 0.65 (65 wt%): T_cr ≈ 36°C — solution will solidify if cooled below 36°C.

**Prevention:** Dilution control valve, concentration monitoring, minimum cooling water temp interlock (~18–20°C), Dühring chart monitoring.

### Corrosion Inhibitors for LiBr Systems

| Inhibitor | Concentration | Notes |
|---|---|---|
| Lithium molybdate (Li₂MoO₄) | 0.1–0.5 wt% | Preferred modern inhibitor (non-toxic) |
| Lithium chromate (Li₂CrO₄) | 0.1–0.3 wt% | Most effective but Cr(VI) is toxic/regulated |
| Lithium nitrate (LiNO₃) | 0.2–0.5 wt% | Supplementary passivation |
| 2-Ethyl-1-hexanol | 50–100 ppm | Wetting agent for absorber |
| Octyl alcohol | 50–200 ppm | Reduces surface tension at absorber |

Use 316L or 304 stainless steel for all wetted parts.

---

## 4. Synthesis of Key Materials

### 4.1 Ammonia (NH₃)

#### Haber-Bosch Process (Industrial Standard)

$$\text{N}_2 + 3\text{H}_2 \rightleftharpoons 2\text{NH}_3 \quad \Delta H_{rxn} = -92.4 \text{ kJ/mol}$$

| Parameter | Value | Rationale |
|---|---|---|
| Temperature | 400–500°C | Balance kinetics vs. equilibrium (exothermic → lower T favors product) |
| Pressure | 150–300 atm (15–30 MPa) | Volume decrease (4→2 mol) → high P favors NH₃ |
| Conversion per pass | 15–25% | Equilibrium limited; remainder recycled |
| Catalyst | Fe₃O₄ reduced to α-Fe, K₂O (~1%) + Al₂O₃ (~2–3%) promoters | K₂O = electronic promoter; Al₂O₃ = structural promoter |

**Catalyst mechanism on iron:**
1. N₂ dissociative chemisorption (rate-determining): N₂ + 2Fe* → 2N*
2. H₂ dissociative adsorption: H₂ + 2Fe* → 2H*
3. Sequential hydrogenation: N* + H* → NH*, NH* + H* → NH₂*, etc.
4. Desorption: NH₃* → NH₃ + Fe*

**Catalyst poisons:** Even ppm levels of sulfur, oxygen, or water vapor permanently deactivate the catalyst. Must use purified H₂ and N₂.

**H₂ sources:**
- Steam methane reforming (SMR): CH₄ + H₂O → CO + 3H₂ (700–900°C, Ni/Al₂O₃ catalyst) → water-gas shift → CO₂ removal → H₂
- Water electrolysis (green H₂): 2H₂O → 2H₂ + O₂ (75–85% efficiency in PEM systems)

**N₂ sources:**
- Cryogenic air separation (fractional distillation of liquid air): N₂ bp −196°C vs O₂ bp −183°C
- Pressure swing adsorption (PSA): zeolites adsorb O₂, N₂ passes through; 95–99.999% purity

**Small-scale alternatives:**
- Electrochemical synthesis (ambient conditions): N₂ + 6H⁺ + 6e⁻ → 2NH₃; historically <1% Faradaic efficiency, but Li-mediated methods achieved 30–80% Faradaic efficiency as of 2024–2025 — still pre-commercial
- Plasma-assisted synthesis: non-thermal plasma activates N₂ at ambient; low energy efficiency (~20% of Haber-Bosch)

#### Purchasing Aqueous Ammonia (Practical for DIY)

| Product | Concentration | Source |
|---|---|---|
| Household ammonia | 5–10% NH₃ | Grocery/hardware store — too dilute |
| Janitorial/industrial ammonia | 26–29% NH₃ | Chemical supply, janitorial distributors — suitable |
| Anhydrous liquid ammonia | ~100% | Agricultural suppliers — requires pressure vessel |
| 26° Baumé ammonia | ~26% | Chemical distributors (Brenntag, Univar) |

**Safety:** NH₃ IDLH = 300 ppm. Work outdoors or with ventilation. Vapor lighter than air. NH₃ attacks copper — use steel/stainless steel only.

### 4.2 Lithium Bromide (LiBr)

#### Industrial Synthesis Routes

**Route 1 (preferred — high purity):**
$$\text{LiOH} + \text{HBr} \rightarrow \text{LiBr} + \text{H}_2\text{O}$$

**Route 2 (common — lower cost):**
$$\text{Li}_2\text{CO}_3 + 2\text{HBr} \rightarrow 2\text{LiBr} + \text{H}_2\text{O} + \text{CO}_2\uparrow$$

#### Lithium Sources
- **Spodumene ore** (LiAlSi₂O₆): roast at 1050°C, acid leach with H₂SO₄, precipitate as Li₂CO₃ with Na₂CO₃
- **Brine extraction** (Atacama, Chile; Qinghai, China): solar evaporation then lithium extraction

Li₂CO₃ → LiOH by: Li₂CO₃ + Ca(OH)₂ → 2LiOH + CaCO₃

#### Hydrobromic Acid (HBr) Production

**Method 1 (clean, pure HBr):**
$$\text{H}_2 + \text{Br}_2 \rightarrow 2\text{HBr} \quad \Delta H = -103.7 \text{ kJ/mol}$$
Dissolve HBr gas in water → up to 48% hydrobromic acid.

**Method 2 (simpler lab method):**
$$\text{NaBr} + \text{H}_2\text{SO}_4 \rightarrow \text{HBr}\uparrow + \text{NaHSO}_4$$
Moderate heating with concentrated H₂SO₄; dissolve HBr gas in water.

#### Preparing LiBr-H₂O Working Solution

For 62 wt% LiBr solution (100 kg total):
- 62 kg LiBr (anhydrous) + 38 kg distilled water

**Inhibitor addition:**
- 0.15–0.30 kg lithium molybdate (Li₂MoO₄)
- 0.05–0.10 kg lithium nitrate (LiNO₃)
- 50–100 mL 2-ethyl-1-hexanol
- Adjust pH to 9.5–10.5 with small LiOH addition

Commercial LiBr available as 45–55% aqueous solution (lower shipping hazard than solid). Concentrate under vacuum to desired 62–65% operating concentration.

---

## 5. The Einstein Refrigerator (No Moving Parts)

### Historical Background

Albert Einstein and Leó Szilárd patented (US Patent 1,781,541, 1930) an absorption refrigerator with **no moving parts whatsoever** — motivated by fatal household refrigerator leaks. Uses three fluids: **ammonia, butane, and water**.

Key insight: raise total gas pressure in evaporator by adding inert butane gas → ammonia partial pressure remains low at same total pressure → ammonia evaporates at low temperature without mechanical pressure difference.

### Single-Pressure Operating Principle

**Circuit 1 (NH₃-Butane, evaporator side):**
- Liquid NH₃ enters evaporator vessel containing butane gas
- NH₃ evaporates at low partial pressure → absorbs heat from refrigerated space
- NH₃ + butane vapor mixture moves to absorber by gravity/buoyancy

**Circuit 2 (NH₃-Water, absorber-generator):**
- NH₃ vapor absorbed into water in absorber (exothermic — reject heat)
- Aqueous ammonia flows to generator by gravity
- Heat drives off NH₃ vapor → rectifier → condenser → liquid NH₃ → back to evaporator

**Circuit 3 (Butane pump):**
- Bubble pump: heat applied to bottom of narrow riser tube causes vapor bubbles, pushing liquid upward — no moving parts
- Optimal L/D ratio for riser tube: ~100–200; typical ID 2–5 mm, length 0.3–1 m

### Practical Considerations

- **COP:** Only ~0.1–0.2 (inert gas approach inherently less efficient)
- **Three-fluid balance is critical** — ratio of NH₃:H₂O:butane must be precisely calculated
- System must be **precisely leveled** (all flow driven by gravity/thermal gradients)
- **Modern research:** Peter Delano (Georgia Tech 1998 PhD), Malcolm McCulloch (Oxford) — improved bubble pump understanding
- **Commercial history:** AEG produced ~2,000 units in early 1930s before Freon made them uneconomical
- **Dometic/Norcold RV fridges** use a variant (Platen-Munters design, 1922) with H₂ as inert gas instead of butane — same principle, completely silent operation

---

## 6. Building an Absorption Refrigerator

### Reference Commercial Systems

**Dometic/Norcold RV fridges (NH₃-H₂-H₂O, Platen-Munters):**
- No moving parts, completely silent
- Heat input: 150–300 W (propane burner or AC heater)
- COP: 0.2–0.4
- Temperatures: 0–8°C fridge, −12 to −18°C freezer

### Component List (1 kW Cooling, Pumped NH₃-H₂O System)

| Component | Material | Specification |
|---|---|---|
| Generator/boiler | Steel tube | 50–100 mm OD, 200–400 mm long, must withstand 20–25 bar |
| Rectifier | Steel tube with wire mesh packing | Removes water from NH₃ vapor |
| Condenser | Steel coil in water bath or finned steel in air | High-side pressure rated |
| Expansion valve | Stainless needle valve OR capillary tube 0.5–1 mm ID × 1–3 m | Refrigerant metering |
| Evaporator | Steel coil in insulated box | Low-side, refrigerated space contact |
| Absorber | Steel coil in water bath or finned air exchanger | Low-side, rejects absorber heat |
| Solution HX | Shell-and-tube or plate HX | Critical for COP |
| Solution pump | Diaphragm or gear pump (NH₃ compatible) | ~0.1–0.3 bar differential |
| Safety relief valve | Steel, set at 25 bar | **Critical safety device** |
| Pressure gauges | Bourdon tube (NH₃ rated) | High side 0–30 bar; low side 0–10 bar |

### Fabrication Requirements

- **All welding:** TIG (GTAW) or silver-brazing (≤30 bar). **No copper solder — NH₃ attacks copper.**
- **Pressure test:** Nitrogen to 1.5× max operating pressure (25 bar → 37.5 bar test). Check with soap solution.
- **Leak test:** Evacuate to <1 mbar, charge with small NH₃, check with NH₃ detector.
- **Wall thickness:** For 25 bar in steel (yield 250 MPa), t = PD/(2S). 2–3 mm practical minimum for small tubes → safety factor >>10.
- **Fittings:** Swagelok or Parker rated for NH₃ service. No brass or copper alloy.

### Typical Small System Parameters (1 kW Cooling)

| Parameter | Value |
|---|---|
| Cooling capacity | 1 kW |
| COP | ~0.55 |
| Generator heat input | ~1.8 kW |
| NH₃ charge | 1–2 kg |
| Solution charge | 8–15 kg (25–35% NH₃) |
| Operating pressures | ~15 bar high / ~4 bar low (0°C evap, 40°C cond) |
| Solution pump power | ~20–50 W electric |

### Heat Source Sizing

For 1 kW cooling at COP = 0.55: Q_gen = 1.82 kW

**Propane burner consumption:**
$$\dot{m}_{fuel} = \frac{2000 \text{ W}}{46{,}300 \text{ J/g}} = 0.043 \text{ g/s} = 155 \text{ g/hour}$$

A 1 lb (454 g) propane cylinder lasts ~3 hours at 2 kW input.

---

## 7. Adsorption Refrigeration (Solid Sorbent)

### Absorption vs. Adsorption

| Property | Absorption | Adsorption |
|---|---|---|
| Sorbent phase | Liquid | Solid |
| Process | Bulk dissolution | Surface adhesion/pore condensation |
| Regeneration | Continuous | Batch (heat-cool cycles of solid bed) |
| Moving parts | Solution pump | None (valves only) |
| COP range | 0.5–1.4 | 0.3–0.6 |

### Working Pairs

| Pair | Drive Temp | Evap Temp | COP | Notes |
|---|---|---|---|---|
| Silica gel / water | 60–90°C | +5 to +15°C | 0.3–0.5 | Solar compatible, system under vacuum |
| Zeolite 13X / water | 120–200°C | +5 to +15°C | 0.3–0.6 | Long life, thermochemical energy storage |
| Activated carbon / methanol | 70–120°C | -10 to -30°C | 0.3–0.5 | Flammable! Sub-zero possible |
| Activated carbon / ammonia | 100–200°C | -20 to -40°C | 0.3–0.4 | Deep freeze possible |
| MOF-801 / water | 40–70°C | +5 to +15°C | 0.4–0.7 | Research stage, very low drive temp |

### Adsorption Cycle Operation (2-Bed System)

- **Bed A (adsorbing):** Connected to evaporator; refrigerant vapor adsorbs → cooling; bed heats up
- **Bed B (desorbing):** Connected to condenser; heat applied → refrigerant desorbs; condensed liquid flows to evaporator
- After half-cycle: beds swap roles
- **Heat recovery phase** between half-cycles: hot desorbing bed preheats cold adsorbing bed → improves COP by ~20–30%

### COP Analysis

For silica gel-water:
$$\text{COP}_{ads} = \frac{\Delta q \cdot L_{ev}}{Q_{des} + \Delta q \cdot L_{ev}}$$

Where:
- Δq = net uptake change per cycle ≈ 0.05–0.15 kg water / kg silica gel
- L_ev = latent heat at evaporator temperature (~2450 kJ/kg water at 10°C)
- Q_des = heat of desorption (includes heat of adsorption + sensible heat of bed)

### Adsorbent Synthesis

**Zeolite 13X:**
1. Dissolve NaAlO₂ and Na₂SiO₃ in NaOH solution (Si/Al = 1.0–1.3)
2. Age at room temperature 6–12 hours
3. Crystallize at 80–100°C for 6–48 hours in sealed vessel
4. Filter, wash with distilled water, dry
5. Activate at 300–400°C for 4–8 hours

**Silica Gel:**
1. Acidify Na₂SiO₃ (sodium silicate) with HCl or H₂SO₄ to pH 4–6
2. Allow gel to form at room temperature (30 min – 2 hours)
3. Wash with distilled water to remove salt ions
4. Dry at 120°C, then activate at 150–180°C
5. Surface area ~600–800 m²/g

**Activated Carbon:**
1. Pyrolyze coconut shells, wood, or coal at 500–900°C under N₂ atmosphere
2. Activate with CO₂ or steam at 800–900°C (creates micropores)
3. Wash with dilute HCl to remove ash, then with water
4. Dry and activate at 200°C

---

## 8. Surprising Findings and Open Questions

### Surprising Facts

1. **Absorption predates vapor compression:** Ferdinand Carré's 1858 NH₃-H₂O absorption cycle predates reliable electric compressors by decades. Commercial ice-making by absorption was running before most cities had electricity.

2. **NH₃ absorption fridges "banned" in US homes:** A series of fatal NH₃ leaks in 1920s–30s domestic absorption fridges led to regulatory pressure, directly causing Einstein and Szilárd to invent the no-moving-parts design in 1930.

3. **Absorption heat pumps can have COP > 1 for heating:** COP_heat = COP_cool + 1. Gas absorption heat pumps (Robur, Vaillant) achieve 130–170% nominal efficiency vs. direct-fired boiler.

4. **The theoretical COP ceiling for cooling absorption is much higher than 1:** At T_g = 473 K (200°C), T_a = 308 K (35°C), T_e = 280 K (7°C), COP_max = 3.49. Real systems achieve ~5–15% of Carnot.

5. **Double-effect COP improvement:** In double-effect LiBr, vapor from high-pressure stage heats low-pressure stage — internal heat cascading equivalent to running two cycles in series. Triple-effect (COP ~1.7) and quadruple-effect (COP ~2.2) are theoretically possible but limited by LiBr solution stability above ~175°C.

6. **Einstein refrigerators were commercially produced:** ~2,000 AEG units in early 1930s before Freon ended production. Electrolux acquired the patent portfolio.

7. **Electrochemical compressor hybrid:** An electrochemical cell pumps NH₃ vapor across a membrane (NH₃ dissolves as ammonium ion, migrates under electric potential, reforms on other side). No moving parts, less electricity than mechanical compression, can be driven by PV. Companies like Xergy have demonstrated this.

8. **SrCl₂-NH₃ chemisorption for seasonal solar energy storage:** SrCl₂ + 8NH₃ ⇌ SrCl₂·8NH₃ (ΔH = −40 kJ/mol NH₃). Can store solar energy for months without insulation losses. Village-scale solar ice making demonstrated at CNRS.

9. **GAX cycle breaks single-effect COP barrier:** Generator-Absorber eXchange cycle uses internal heat recovery to achieve COP > 0.9 from single-effect NH₃-H₂O — rivaling double-effect systems.

10. **LiBr chillers were used for early electric grid peak shaving:** 1970s–1990s, chilled water produced overnight (off-peak electricity) stored in tanks for daytime cooling.

### Key Numbers Reference Card

| Quantity | Value |
|---|---|
| NH₃ normal boiling point | −33.4°C |
| NH₃ critical point | 132.3°C, 113.5 bar |
| NH₃ heat of vaporization at 0°C | 1262 kJ/kg |
| H₂O heat of vaporization at 10°C | 2478 kJ/kg |
| LiBr crystallization onset (65 wt%) | ~36°C |
| LiBr molar mass | 86.84 g/mol |
| NH₃ molar mass | 17.03 g/mol |
| Haber-Bosch ΔH | −92.4 kJ/mol NH₃ |
| Haber-Bosch pressure | 150–300 atm |
| Haber-Bosch temperature | 400–500°C |
| NH₃ IDLH | 300 ppm |
| Propane heat of combustion (lower) | 46.3 MJ/kg |
| Single-effect LiBr COP | 0.65–0.80 |
| Double-effect LiBr COP | 1.0–1.4 |
| Single-effect NH₃-H₂O COP | 0.45–0.65 |
| Einstein refrigerator COP | 0.1–0.2 |

### Key References

- *Absorption Chillers and Heat Pumps* — Keith Herold, Reinhard Radermacher, Sanford Klein (CRC Press, 2016) — **authoritative reference**
- *Industrial Refrigeration Handbook* — Wilbert Stoecker (McGraw-Hill, 1998)
- ASHRAE Handbooks — Fundamentals and HVAC Systems chapters on absorption
- Patek-Klomfar correlation for NH₃-H₂O thermodynamic properties (standard reference)
