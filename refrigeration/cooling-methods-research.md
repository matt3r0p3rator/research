# Cooling Methods Research
*Compiled: May 18, 2026*

---

## PART 1: ADSORPTION REFRIGERATION

### Overview

Adsorption refrigeration uses solid sorbents driven by a heat source to produce a refrigeration effect — **no liquid pump required**. The cycle is thermal, making it compatible with waste heat, solar energy, or any low-grade heat source.

### 1. Working Principle

1. **Desorption (regeneration):** External heat source drives refrigerant vapor off the saturated sorbent bed.
2. **Condensation:** Refrigerant vapor condenses in the condenser, releasing heat to the environment.
3. **Expansion:** Liquid refrigerant expands through a valve into the evaporator.
4. **Adsorption:** The cooled sorbent bed re-adsorbs refrigerant vapor from the evaporator, lowering evaporator pressure and producing the **cooling effect**.
5. Cycle repeats: sorbent is re-heated to restart desorption.

> The key thermodynamic driver is the affinity of the sorbent for the refrigerant vapor — controlled entirely by temperature.

---

### 2. Working Pairs and Properties

| Working Pair | Drive Temp (°C) | COP | Cooling Temp Range | Notes |
|---|---|---|---|---|
| **Silica gel / Water** | 60–90 | 0.3–0.5 | Above +5°C | Low drive temp; ideal for solar flat-plate collectors |
| **Zeolite 13X / Water** | 150–200 | 0.3–0.6 | Above 0°C | Very robust; long service life; high-temp waste heat |
| **Activated Carbon / Methanol** | 60–120 | 0.3–0.6 | Down to −20°C | Sub-zero capable; methanol is flammable — outdoor/ventilated use |
| **Activated Carbon / Ammonia** | 100–200 | 0.3–0.5 | Sub-zero possible | Ammonia is toxic; requires sealed system; high pressures |
| **MOF-801 (Zr-fumarate) / Water** | 50–80 | TBD (research) | Above 0°C | Very low drive temp possible; not yet commercial (2026) |

**Key insight:** COP is modest (0.3–0.6) compared to vapor-compression (~3–5), but the energy input is **heat** (often free/waste), not electricity.

---

### 3. Synthesis of Adsorbents

#### 3.1 Zeolite 13X

**Procedure:**
1. Mix NaAlO₂ + Na₂SiO₃ in concentrated NaOH solution (target Si/Al molar ratio = 1.0–1.3).
2. Age the gel at room temperature for **6–12 hours** with stirring; this forms the aluminosilicate precursor gel.
3. Transfer to a sealed vessel; crystallize at **80–100°C for 6–48 hours** (autogenous pressure).
4. Filter, wash with deionized water until neutral pH, then dry at 100–120°C.
5. **Activation:** heat to **300–400°C** for 4–8 hours to remove water and open pore structure.

**Quality check:** XRD pattern should show FAU-type framework; BET surface area ~700–900 m²/g.

#### 3.2 Silica Gel

**Procedure:**
1. Prepare sodium silicate solution (Na₂SiO₃·9H₂O in water, ~10–15 wt%).
2. Acidify with dilute HCl or H₂SO₄ dropwise to **pH 4–6** under stirring; silica gel precipitates.
3. Allow gel to age/set for several hours at room temperature.
4. Wash the gel thoroughly with deionized water to remove Na⁺, Cl⁻/SO₄²⁻ ions.
5. Dry at **120°C** until fully dry; then **activate at 150–180°C** to control final pore structure.

**Quality check:** BET surface area ~600–800 m²/g; average pore diameter 4–6 nm for Type A silica gel.

#### 3.3 Activated Carbon

**Two-stage process:**

| Stage | Conditions | Purpose |
|---|---|---|
| **Pyrolysis** | 500–900°C in inert N₂ atmosphere | Carbonize precursor (coconut shell, wood, coal); remove volatiles |
| **Activation** | 800–900°C with CO₂ or steam | Develop micropore structure by selective oxidation of carbon |

**Notes:**
- Coconut shell char produces the highest surface area (1000–1500 m²/g).
- Steam activation: faster but less selective pore development than CO₂.
- **Safety:** all stages require inert/controlled atmosphere to prevent combustion.

---

### 4. System Design

#### 4.1 Intermittent (Single-Bed) System

```
[Heat Source] → [Sorbent Bed] ↔ [Condenser] → [Expansion Valve] → [Evaporator]
```

- Simple construction; single bed alternates between heating (desorption) and cooling (adsorption).
- **Limitation:** no cooling during the heating phase; batch output.
- Suitable for ice making in solar applications.

#### 4.2 Continuous (Two-Bed) System

```
Bed A: Desorbing (heated) ──→ Condenser ──→ Evaporator ──→ Bed B: Adsorbing (cooled)
                                                             ↓
                              [Heat Recovery between beds during switchover]
```

- Two beds operate out of phase; switchover every ~15–30 min.
- **Heat recovery** during switching (hot bed pre-heats cool bed) significantly improves COP.
- Continuous cooling output.
- More complex valving and controls.

---

### 5. Thermodynamic Equations

**Coefficient of Performance:**
$$\text{COP} = \frac{Q_\text{evap}}{Q_\text{gen}}$$

Where:
- $Q_\text{evap}$ = heat absorbed at the evaporator (useful cooling effect)
- $Q_\text{gen}$ = heat supplied to the sorbent bed during desorption

**Specific Cooling Power (SCP):**
$$\text{SCP} = \frac{Q_\text{evap}}{m_\text{sorbent} \cdot t_\text{cycle}} \quad [\text{W/kg}]$$

Higher SCP = more compact system for a given cooling capacity.

**Adsorption Isotherms:**

| Model | Equation | Best For |
|---|---|---|
| **Langmuir** | $q = q_m \frac{bP}{1+bP}$ | Monolayer; homogeneous surfaces |
| **Freundlich** | $q = kP^{1/n}$ | Heterogeneous surfaces; empirical |
| **Dubinin-Astakhov (D-A)** | $q = q_0 \exp\left[-\left(\frac{A}{E}\right)^n\right]$ | Activated carbon (micropore filling); most accurate for AC/methanol |

Where $A = RT\ln(P_s/P)$ is the Polanyi adsorption potential.

---

### 6. Solar-Driven Adsorption Systems

- **Flat-plate solar collectors** → suitable for silica gel/water (60–90°C drive temperature)
- **Evacuated tube collectors** → suitable for zeolite/water or AC/methanol (100–200°C)
- **Parabolic trough concentrators** → highest temperatures; useful for zeolite/ammonia pairs

**Ice-making application (solar):**
- Daytime: solar heat drives desorption → refrigerant condenses in condenser
- Night: bed cools → adsorption draws vapor from evaporator → ice forms
- Typical yield: 4–10 kg ice per m² collector per day in sunny climates

**Key challenge:** intermittent solar input matches well with the batch adsorption cycle — no thermal storage required for basic ice-making.

---

### 7. Achievable Temperatures by Working Pair

| Working Pair | Evaporator Temp Range |
|---|---|
| Silica gel / Water | +5°C to +15°C (air conditioning) |
| Zeolite 13X / Water | 0°C to +10°C |
| Activated Carbon / Methanol | −5°C to −20°C |
| Activated Carbon / Ammonia | −20°C to −40°C (possible) |
| MOF-801 / Water | +5°C to +15°C (projected) |

---

## PART 2: EXOTIC AND ALTERNATIVE COOLING METHODS

---

### Method 1: Magnetocaloric / Magnetic Refrigeration

| Parameter | Details |
|---|---|
| **Energy Input** | Magnetic field (permanent magnet + motion, or electromagnet) |
| **Temp Range** | −270°C (mK via adiabatic demagnetization) to room temp (AMR cycle) |
| **COP/Efficiency** | Can approach Carnot theoretically; practical prototypes ~1.5–3 near room temp |
| **DIY Feasibility** | **Not feasible** (requires strong rare-earth magnets + precision materials) |

**How it works:**
- Magnetocaloric materials exhibit an entropy change in their magnetic sublattice when a magnetic field is applied or removed.
- **Apply field (adiabatic):** magnetic moments align → entropy decreases → material heats up.
- **Remove heat to sink**, then **remove field (adiabatic):** material cools below starting temperature.
- Repeat: material absorbs heat from cold reservoir.

**Key Materials:**

| Material | Curie Temp | ΔT_ad (max) | Notes |
|---|---|---|---|
| Gadolinium (Gd) | ~294 K (21°C) | ~14 K at 7 T | Benchmark material; expensive |
| Gd₅Si₂Ge₂ | Tunable | Large | Giant magnetocaloric effect; first-order transition |
| La(Fe,Si)₁₃ | ~195 K (tunable) | ~6–10 K at 2 T | More practical field strengths |
| MnFePAs | ~300 K (tunable) | ~6–8 K at 2 T | Contains toxic As; being replaced with MnFePSi |

**AMR (Active Magnetic Regenerator) Cycle:**
- Magnetocaloric bed acts simultaneously as refrigerant AND thermal regenerator.
- Heat transfer fluid flows through the bed; enables temperature spans much larger than single-material ΔT.
- Near-room-temperature refrigeration becomes viable.

**Adiabatic Demagnetization:**
- Used in cryogenic labs to reach millikelvin temperatures.
- Paramagnetic salts (e.g., cerium magnesium nitrate) or nuclear demagnetization stages.

**Commercial status (2026):** Cooltech Applications (France), Camfridge (UK), BASF (Germany) have working prototypes; no mass-market products yet. Primary barriers: cost of magnetocaloric materials, achieving large temperature spans with permanent magnets.

---

### Method 2: Vortex Tube (Ranque-Hilsch Tube)

| Parameter | Details |
|---|---|
| **Energy Input** | Compressed air (5–10 bar) |
| **Temp Range** | −50°C to +100°C (cold end 20–50°C below inlet; hot end 20–80°C above) |
| **COP** | ~0.1–0.5 (thermodynamically inefficient) |
| **DIY Feasibility** | **Easy–Moderate** (machinable from aluminum; commercial units available cheaply) |

**Operating principle:**
1. Compressed air enters **tangentially** through one or more nozzles, creating a high-speed vortex.
2. The outer (fast) layer migrates to the hot end and exits through a **cone valve**.
3. The inner (slow) layer transfers kinetic energy to the outer layer, cools, and exits the **cold orifice** at the inlet end.
4. Energy separation mechanism: angular momentum transfer + thermodynamic work exchange between layers.

**Construction (DIY):**
```
[Air inlet, tangential nozzle]
      ↓
[Cylindrical tube, ~20mm ID, L/D ≈ 30–50]
      ↓ vortex
[Cold orifice (small, ~40% tube ID)] ←cold air out
[Hot end: adjustable cone valve] → hot air out
```
- Tube material: aluminum, stainless steel, or brass.
- Cold fraction (μ): typically 0.3–0.7 (fraction of inlet air exiting cold end); optimum for max cooling ~0.3–0.4.
- No lubrication, no refrigerants, no electricity. Drawback: wastes compressed air energy.

**Applications:** spot cooling in CNC machines/electronics, pneumatic cooling vests, emergency breathing air cooling, rapid chilling small components.

---

### Method 3: Thermoacoustic Refrigeration

| Parameter | Details |
|---|---|
| **Energy Input** | Acoustic/mechanical (loudspeaker or linear motor driver) |
| **Temp Range** | Room temp down to −100°C and below (cryogenic demonstrated) |
| **COP** | Standing wave: 10–20% of Carnot; Traveling wave: up to 40–50% of Carnot |
| **DIY Feasibility** | **Moderate** (standing wave prototypes buildable; traveling wave requires precision) |

**Operating principle:**
- Acoustic waves at resonance frequency create oscillating pressure and displacement of the working gas.
- Gas parcels undergo compression (heating) and expansion (cooling) as they oscillate through the **stack** (ceramic plates or mesh screens).
- Heat is pumped from cold end to hot end of the stack.

**Standing wave vs. traveling wave:**

| Type | Phase relationship | Efficiency | Complexity |
|---|---|---|---|
| **Standing wave** | Pressure and velocity 90° out of phase | Low–moderate | Simple (just a resonator + stack) |
| **Traveling wave** | Pressure and velocity in phase | High (Stirling-like) | Complex (looped resonator, careful acoustic matching) |

**Working fluids:**
- Helium (He): low viscosity, high speed of sound; preferred
- He-Ar mixtures: tunable acoustic properties
- Operating pressure: typically 10–30 bar for reasonable power density

**Key components:**
1. **Driver:** electrodynamic loudspeaker or linear motor (outside cold space)
2. **Resonator tube:** sets acoustic resonance; length ≈ λ/2 or λ/4
3. **Stack/regenerator:** fine-pore ceramic honeycomb or wire mesh; thermal contact with gas
4. **Heat exchangers:** ambient (hot) and cold heat exchangers at stack ends

**Notable demonstrations:**
- Los Alamos National Lab (LANL): demonstrated cryogenic thermoacoustic cooling for natural gas liquefaction and space applications.
- Ben & Jerry's (Swift/Garrett): thermoacoustic freezer prototype using propane acoustic driver.

---

### Method 4: Electrocaloric Cooling

| Parameter | Details |
|---|---|
| **Energy Input** | Electric field (high voltage, low current) |
| **Temp Range** | Near ambient; ΔT ~12–15°C demonstrated in thin films |
| **COP** | Theoretical ~Carnot; practical limited by dielectric losses |
| **DIY Feasibility** | **Not feasible** (high electric fields in thin films; nanofabrication required) |

**How it works:**
- Apply electric field to ferroelectric/electrocaloric material → dipoles align → entropy decreases → material heats.
- Remove field → dipoles randomize → material cools below starting temperature.
- Thermodynamically analogous to magnetocaloric effect but driven by electric rather than magnetic field.

**Key materials:**

| Material | Form | ΔT achieved | Notes |
|---|---|---|---|
| BaTiO₃ | Ceramic | ~1–2 K (bulk) | Classic ferroelectric; limited bulk ΔT |
| PbZr₀.₉₅Ti₀.₀₅O₃ (PZT) | Thin film | ~12 K at ~480 kV/cm | Best demonstrated ΔT (Mischenko 2006) |
| PVDF-TrFE | Polymer film | ~12–15 K | Flexible; lower operating voltages than ceramics |

**Key challenge:** ΔT is large in thin films (GV/m fields over nm distances = practical voltages), but scaling to bulk/macroscale while maintaining field strength is unsolved. Current focus: stacked multilayer devices for microelectronics cooling (chips, LEDs).

---

### Method 5: Evaporative Cooling

| Parameter | Details |
|---|---|
| **Energy Input** | Low electricity (fan + pump); water |
| **Temp Range** | Wet-bulb limit for direct; sub-wet-bulb possible with indirect/dew-point systems |
| **COP** | Very high (~10–50+); cheap to run |
| **DIY Feasibility** | **Easy** (direct evaporative coolers are simple; dew-point systems moderately complex) |

**Three tiers:**

#### Direct Evaporative Cooling (DEC)
- Water evaporates directly into supply airstream.
- Outlet temperature approaches **wet-bulb temperature** of ambient air.
- Effective in hot, dry climates (RH < 40%).
- Adds humidity — unsuitable in already-humid environments.
- Components: cellulose/ceramic pad, water pump, fan.

#### Indirect Evaporative Cooling (IEC)
- Secondary airstream is evaporatively cooled; primary airstream is cooled through a heat exchanger without gaining humidity.
- Can approach but not reach wet-bulb temperature of ambient.
- More complex; requires plate heat exchanger or heat pipe.

#### Dew-Point Cooler (Two-Stage IEC)
- Working air (exhaust) is split: part is used as the evaporating stream.
- Can cool **below the wet-bulb temperature** of the inlet air, approaching the **dew-point temperature**.
- Effectiveness: 80–120% of wet-bulb depression.
- Commercial products: Coolerado, dais analytic, Maisotsenko cycle (M-Cycle) coolers.

**Climate suitability:**

| Climate | Direct | Indirect | Dew-Point |
|---|---|---|---|
| Hot dry (desert) | Excellent | Good | Good |
| Hot humid | Poor | Marginal | Fair |
| Temperate | Good | Good | Good |

---

### Method 6: Passive Radiative Sky Cooling

| Parameter | Details |
|---|---|
| **Energy Input** | None (passive); optional fan/pump for active systems |
| **Temp Range** | 5–15°C below ambient air, even in direct sunlight |
| **COP** | N/A (passive); effective cooling power ~40–100 W/m² |
| **DIY Feasibility** | **Moderate** (polymer films/paints available; photonic multilayers not DIY) |

**Physics:**
- Earth's atmosphere is transparent in the **8–13 μm** mid-infrared window (matches blackbody emission at ~300 K).
- A surface that emits strongly in this band radiates heat directly to outer space (~3 K).
- Net radiative cooling flux: $P_\text{cool} = P_\text{rad}(T_s) - P_\text{atm}(T_\text{amb}) - P_\text{solar}$
- Challenge: sunlight (~0.3–2.5 μm) must be reflected to avoid solar heating during daytime.

**Materials:**

| Material | Type | Performance | Status |
|---|---|---|---|
| SiO₂/HfO₂ photonic multilayer | Thin film on Ag | ~40–100 W/m² sub-ambient | Stanford 2017 landmark demo; 5°C below ambient in full sun |
| PDRC (polymer-metal composite) | Polymer + Al film | ~50–100 W/m² | Commercial products emerging 2022–2026 |
| White/ultrawhite paints | Paint coating | ~80–100 W/m² | Purdue "whitest paint" (BaSO₄); commercial versions available |
| Selective emitter films | Polymer (PE, PVDF) | Varies | Lower-cost; research stage |

**Applications:**
- Passive building cooling (roof coatings, wall panels)
- Cool water systems: circulate water through radiative panels at night (cooled water stored for daytime use)
- Food preservation in off-grid settings
- Combined with PV cells: dual solar harvesting + passive cooling

---

### Method 7: Joule-Thomson Expansion

| Parameter | Details |
|---|---|
| **Energy Input** | Mechanical (compressor to pressurize gas) |
| **Temp Range** | Depends on gas: N₂ → LN₂ (−196°C); He → LHe (−269°C) |
| **COP** | Low for simple J-T; improved with regenerative heat exchange (Linde cycle) |
| **DIY Feasibility** | **Moderate** (basic J-T probes buildable; liquefaction plants are industrial) |

**Physics:**
$$\mu_{JT} = \left(\frac{\partial T}{\partial P}\right)_H = \frac{1}{C_p}\left[T\left(\frac{\partial V}{\partial T}\right)_P - V\right]$$

- Gas cools on expansion only if temperature is **below its inversion temperature**.
- Above inversion temperature: gas warms on expansion (e.g., H₂ and He at room temperature must be pre-cooled first).

**Inversion temperatures:**

| Gas | Inversion Temp | Pre-cooling needed? |
|---|---|---|
| N₂ | 621 K (348°C) | No |
| O₂ | 764 K (491°C) | No |
| Ar | 794 K (521°C) | No |
| H₂ | 202 K (−71°C) | Yes (pre-cool with LN₂) |
| He | 40 K (−233°C) | Yes (pre-cool to below 40 K) |

**Linde liquefaction cycle:** Adds counterflow heat exchanger between high-pressure feed and low-pressure return streams. The expanded cold gas pre-cools the incoming feed, progressively reducing temperature until liquefaction begins.

**Simple J-T probe construction:**
```
[High-pressure gas] → [Coiled Cu tube (counterflow heat exchanger)] → [Needle valve] → [Cold tip]
                              ↑ cold expanded gas flows back to pre-cool incoming stream
```
Used in: cryosurgical probes, portable LN₂ generators, closed-cycle refrigerators (combined with Joule-Thomson stage).

---

### Method 8: Chemical / Endothermic Cooling

| Parameter | Details |
|---|---|
| **Energy Input** | Chemical energy (consumed; not regenerated) |
| **Temp Range** | 0°C to −20°C depending on reagents |
| **COP** | N/A (single-use energy release) |
| **DIY Feasibility** | **Easy** (common lab/hardware store chemicals) |

#### 8.1 Dissolution-Based Cold Packs

| Reaction | ΔH | Final Temp (approx.) | Safety |
|---|---|---|---|
| NH₄NO₃ + H₂O | +25.7 kJ/mol (endothermic) | ~5°C from 20°C | Mild; standard cold pack |
| NH₄Cl + H₂O | +14.8 kJ/mol | ~10°C from 20°C | Safe; common salt |
| NH₄Cl + Ba(OH)₂·8H₂O | Large endotherm | ~−20°C | Ba(OH)₂ is toxic; ventilated use |
| Urea + H₂O | +15.4 kJ/mol | ~10–12°C from 20°C | Very safe; fertilizer |

#### 8.2 Phase Change Materials (PCM)

PCMs store/release large amounts of latent heat at a fixed temperature — useful for thermal buffering and passive cooling.

| PCM | Phase Change Temp | Latent Heat | Notes |
|---|---|---|---|
| Water → Ice | 0°C | 333 kJ/kg | Best volumetric capacity; cheap |
| n-Tetradecane | 5.5°C | 227 kJ/kg | Refrigeration applications |
| n-Octadecane | 28°C | 242 kJ/kg | Building comfort cooling |
| Paraffin wax (mixed) | 18–55°C | 150–250 kJ/kg | Cheap; variable melting point |
| Na₂SO₄·10H₂O (Glauber's salt) | 32.4°C | 254 kJ/kg | Inorganic; high capacity; supercooling issues |
| CaCl₂·6H₂O | 29.8°C | 190 kJ/kg | Inorganic; moderate supercooling |

**PCM applications:** thermal storage in buildings, solar cooling buffer tanks, cold-chain packaging, electronics thermal management.

---

## COMPARATIVE SUMMARY

| Method | Energy Input | Temp Range | COP / Efficiency | DIY Feasibility |
|---|---|---|---|---|
| **Adsorption refrigeration** | Heat (waste/solar) | −20°C to +15°C | 0.3–0.6 (thermal COP) | Moderate–Hard |
| **Magnetocaloric** | Magnetic field | mK to room temp | ~1.5–3 (near RT) | Not feasible |
| **Vortex tube** | Compressed air | −50°C to +100°C (relative) | 0.1–0.5 | Easy–Moderate |
| **Thermoacoustic** | Acoustic/electrical | −100°C to room temp | 10–50% of Carnot | Moderate |
| **Electrocaloric** | Electric field | ΔT ~12–15°C | ~Carnot (theoretical) | Not feasible |
| **Direct evaporative** | Electricity (fan/pump) + water | Down to wet-bulb | 10–50+ | Easy |
| **Dew-point evaporative** | Electricity + water | Below wet-bulb | 5–20 | Moderate |
| **Passive radiative** | None (passive) | 5–15°C below ambient | N/A (passive) | Moderate |
| **Joule-Thomson** | Mechanical (compression) | Down to −270°C | Low (simple J-T) | Moderate |
| **Chemical cold packs** | Chemical energy | 0°C to −20°C | N/A (single-use) | Easy |
| **Phase change materials** | Stored latent heat | Fixed temp (PCM dependent) | N/A (passive buffer) | Easy |

---

## KEY DESIGN SELECTION GUIDE

```
Need sub-zero cooling?
├── YES → Activated carbon/methanol or AC/ammonia adsorption
│         OR Joule-Thomson (N₂)
│         OR Thermoacoustic (traveling wave)
└── NO (comfort/food cooling) →
    ├── Have waste heat / solar? → Adsorption refrigeration (silica gel or zeolite)
    ├── Dry climate? → Evaporative / dew-point cooling (cheapest)
    ├── Need zero energy? → Passive radiative sky cooling
    ├── Need spot cooling with just air? → Vortex tube
    └── Off-grid emergency? → Chemical cold packs + PCM buffer

Research / future:
├── Electrocaloric → electronics cooling (chip-scale, 2030+ timeline)
└── Magnetocaloric → efficient near-RT refrigeration (commercial 2028–2035 projection)
```

---

*Sources: synthesized from thermodynamics literature, ASHRAE fundamentals, adsorption refrigeration research (Wang et al., Critoph et al.), magnetocaloric reviews (Gutfleisch et al.), Los Alamos thermoacoustic work (Swift), Stanford photonic cooling (Raman et al. 2017).*
