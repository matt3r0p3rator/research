# Vapor-Compression Refrigeration: Comprehensive Research Notes

*Date: 2026-05-18*

---

## Table of Contents

1. [Thermodynamic Cycle Overview](#1-thermodynamic-cycle-overview)
2. [Key Refrigerants Reference Table](#2-key-refrigerants-reference-table)
3. [Refrigerant Synthesis and Sourcing](#3-refrigerant-synthesis-and-sourcing)
4. [Key System Components](#4-key-system-components)
5. [Design Equations](#5-design-equations)
6. [DIY Practical Notes](#6-diy-practical-notes)
7. [Key Surprising Facts](#7-key-surprising-facts)

---

## 1. Thermodynamic Cycle Overview

### 1.1 The Four Processes

The ideal vapor-compression cycle is represented on a pressure–enthalpy (P–h) diagram and consists of four distinct thermodynamic processes operating between a low-pressure evaporating side and a high-pressure condensing side.

```
         HIGH SIDE
    ┌─────────────────────────────┐
    │  3 ← ← ← ← ← 2            │
    │  (condenser)  (compressor)  │
    │  liquid       hot gas       │
    └───┬─────────────────────┬───┘
        │ (expansion)         │ (compressor work W)
        ↓                     ↑
    ┌───┴─────────────────────┴───┐
    │  4 → → → → → 1             │
    │  (evaporator)               │
    │  flash mix    sat. vapor    │
    └─────────────────────────────┘
         LOW SIDE
```

| State Point | Process | Idealization | Description |
|---|---|---|---|
| **1 → 2** | Compression | Isentropic (s = const) | Low-P saturated vapor enters compressor; exits as high-P superheated vapor. Work W_net is input. |
| **2 → 3** | Condensation | Isobaric (P = const) | Superheated vapor rejects heat Q_H to condenser medium (air or water); exits as saturated or subcooled liquid. |
| **3 → 4** | Expansion | Isenthalpic (h = const) | High-P liquid throttles through expansion device; pressure drops, partial flash evaporation occurs — an irreversible process. |
| **4 → 1** | Evaporation | Isobaric (P = const) | Low-P two-phase mixture absorbs heat Q_L from refrigerated space; exits as saturated (or slightly superheated) vapor. |

### 1.2 Energy Balance

Using enthalpy values at each state point (per unit mass of refrigerant):

$$q_L = h_1 - h_4 \quad \text{(heat absorbed per kg, evaporator)}$$

$$w_{net} = h_2 - h_1 \quad \text{(compressor work per kg)}$$

$$q_H = h_2 - h_3 \quad \text{(heat rejected per kg, condenser)}$$

$$q_H = q_L + w_{net} \quad \text{(first law energy balance)}$$

### 1.3 Coefficient of Performance (COP)

**Cooling COP** (refrigerator/air conditioner):

$$\text{COP}_c = \frac{Q_L}{W_{net}} = \frac{h_1 - h_4}{h_2 - h_1}$$

**Heating COP** (heat pump mode):

$$\text{COP}_{hp} = \frac{Q_H}{W_{net}} = \frac{h_2 - h_3}{h_2 - h_1} = \text{COP}_c + 1$$

**Carnot (ideal) COP** — the theoretical maximum for given temperature limits:

$$\text{COP}_{Carnot} = \frac{T_L}{T_H - T_L} \quad \text{(temperatures in Kelvin)}$$

**Second-law efficiency** (how close to Carnot):

$$\eta_{II} = \frac{\text{COP}_{actual}}{\text{COP}_{Carnot}}$$

Typical real systems achieve η_II ≈ 0.4–0.65. A household refrigerator with T_L = 255 K (−18 °C) and T_H = 308 K (35 °C) has COP_Carnot = 4.8; actual COP ≈ 1.5–2.5.

### 1.4 Real-Cycle Deviations from Ideal

- **Superheating at compressor inlet**: intentional 5–10 K superheat prevents liquid slugging; increases h_1, reduces COP slightly but protects compressor.
- **Subcooling at condenser outlet**: intentional 3–8 K subcooling below saturation reduces flash gas at expansion, increases h_1 − h_4 and thus COP at no compressor work cost.
- **Pressure drops**: in piping and heat exchangers — suction-line pressure drop increases compression ratio and reduces COP.
- **Non-isentropic compression**: isentropic efficiency η_s = (h_2s − h_1)/(h_2 − h_1) ≈ 0.65–0.85 for reciprocating, 0.70–0.80 for scroll.
- **Heat gains/losses in piping**: suction-line heat gain (superheating before compressor) is generally undesirable; liquid-line subcooling is beneficial.

---

## 2. Key Refrigerants Reference Table

Pressures shown are saturated conditions at representative operating points: **evaporating at 0 °C** (low side) and **condensing at 45 °C** (high side), which approximates a residential air conditioner in a warm climate. R-744 is transcritical above 31 °C.

| Refrigerant | Common Name | Chemical Formula | Boiling Pt @ 1 atm | GWP₁₀₀ | ASHRAE Safety | Low Side (bar abs) | High Side (bar abs) |
|---|---|---|---|---|---|---|---|
| **R-290** | Propane | C₃H₈ | −42.1 °C | 3 | A3 | ~4.74 | ~15.3 |
| **R-600a** | Isobutane | C₄H₁₀ | −11.7 °C | 3 | A3 | ~1.58 | ~5.30 |
| **R-717** | Ammonia | NH₃ | −33.3 °C | < 1 | B2L | ~4.29 | ~17.8 |
| **R-744** | Carbon dioxide | CO₂ | −56.6 °C† | 1 | A1 | ~34.8 | ~90–120‡ |
| **R-134a** | HFC-134a | CH₂FCF₃ | −26.1 °C | 1,430 | A1 | ~2.93 | ~11.7 |
| **R-410A** | Puron / AZ-20 | CH₂F₂ / C₂HF₅ (50/50) | −51.4 °C | 2,088 | A1 | ~8.00 | ~28.3 |
| **R-1234yf** | HFO-1234yf | CF₃CF=CH₂ | −29.5 °C | 4 | A2L | ~3.38 | ~12.6 |

**† R-744 notes:**
- CO₂ sublimes at 1 atm at −78.5 °C (dry ice). Liquid CO₂ only exists above its triple point: 5.18 bar / −56.6 °C.
- Critical point: **31.1 °C / 73.8 bar**. Any condenser above 31 °C means transcritical operation — the "condenser" becomes a **gas cooler** and there is no condensation.
- ‡ Transcritical high-side pressure is not set by saturation but by a back-pressure valve; optimum discharge pressure for COP ≈ 2.6 × T_gas-cooler-outlet (°C) + 7.7 (bar), typically 90–120 bar depending on ambient temperature.

**ASHRAE Safety Class Key:**
- **A** = lower toxicity (IDLH > 400 ppm) | **B** = higher toxicity
- **1** = non-flammable | **2L** = mildly flammable (LFL > 3.5%, burning velocity ≤ 10 cm/s) | **2** = flammable | **3** = highly flammable (LFL < 3.5% or heat of combustion ≥ 19 kJ/g)

**Regulatory context:**
- R-134a: phased out of new US light-duty vehicles since 2021 (replaced by R-1234yf); still available for service.
- R-410A: phased down under AIM Act; new residential equipment transitioning to R-454B, R-32, R-1234yf blends by 2025–2026.
- R-290 / R-600a: charge limits of 150 g (R-290) and 150 g (R-600a) per IEC 60335-2-89 for household appliances in the US; EU allows up to 500 g under EN 378.

---

## 3. Refrigerant Synthesis and Sourcing

### 3.1 R-290 — Propane

**Chemistry / Industrial Source:**
Propane is a C₃ hydrocarbon isolated primarily by two industrial routes:
1. **Natural gas processing**: propane condenses out of wet natural gas streams in gas processing plants via refrigeration or absorption. It is separated from methane, ethane, butane, and heavier fractions by fractionation towers.
2. **Steam cracking of naphtha/ethane**: during ethylene/propylene production, propane is a by-product.
3. **Petroleum refining**: from catalytic cracking and hydrocracking units.

**DIY synthesis:** Not feasible. Requires petrochemical infrastructure.

**Purchasing / Sourcing:**
- **BBQ cylinder propane** (HD-5 or HD-10 grade): >95% propane; HD-5 allows max 5% propylene. Widely available at hardware, home improvement, and grocery stores. Contains odorant (ethyl mercaptan) — not suitable for precise refrigerant applications without further purification.
- **MAPP gas cylinders** (MAP/Pro): primarily propylene + propane mixture — NOT suitable as refrigerant R-290.
- **Refrigerant-grade R-290**: available from HVAC/refrigerant suppliers; requires EPA 608 certification in the US for purchase of regulated refrigerants above de minimis quantities.
- **EPA 608 note**: As of 2021, R-290 and other natural refrigerants used in stationary systems are covered under Section 608. Technicians servicing systems must be certified. Self-contained "low loss" fittings are required.

**Key physical concern:** Propane is heavier than air (vapor density ~1.5 × air); leaks accumulate at floor level. Requires Class I, Division 2 electrical components in enclosed spaces.

---

### 3.2 R-600a — Isobutane

**Chemistry / Industrial Source:**
Isobutane (2-methylpropane) is produced by:

1. **Butane isomerization**: Normal butane (n-C₄H₁₀) is converted over AlCl₃ (Lewis acid) or Pt/zeolite catalysts at 80–120 °C and moderate pressure. Equilibrium favors ~50–60% isobutane at 100 °C. Product is separated by distillation.
   - Reaction: n-C₄H₁₀ → i-C₄H₁₀ (ΔG° near zero; equilibrium limited)
2. **Petroleum refining**: isobutane is a natural by-product of catalytic cracking (FCC units) and is recovered from refinery gases by fractionation.
3. **Alkylation plants** consume large amounts of isobutane as feedstock and produce it as a recycle stream.

**DIY synthesis:** Not practical. The AlCl₃ isomerization can theoretically be run in a lab-scale reaction vessel, but separation of isobutane from n-butane and obtaining refrigerant-grade purity is extremely difficult without distillation equipment. Not worth attempting.

**Purchasing / Sourcing:**
- **Lighter fluid / camping fuel canisters**: Some Coleman and Primus butane/isobutane blend canisters sold for camping stoves contain significant isobutane fractions. Purity is inconsistent and contains higher hydrocarbons; not suitable as a refrigerant without analysis.
- **Refrigerant-grade R-600a**: commonly available in Europe through HVAC distributors for household refrigerator service. In the US, availability is growing as more domestic refrigerators use it.
- **Household refrigerators in EU**: essentially all domestic refrigerators sold in Europe since ~2004 use R-600a at charges of 40–130 g. Widely serviced.
- **Charge limits**: 150 g maximum per IEC 60335-2-89 for household appliances; sufficient for most small refrigerators.

---

### 3.3 R-717 — Ammonia

**Chemistry / Industrial Source (Haber-Bosch Process):**

The dominant industrial route is the **Haber-Bosch process**, one of the most important chemical processes in history (~175 million tonnes NH₃/year globally):

$$\text{N}_2 + 3\,\text{H}_2 \rightleftharpoons 2\,\text{NH}_3 \quad \Delta H_{rxn} = -92 \;\text{kJ/mol} \;\text{(exothermic)}$$

**Conditions:**
- **Catalyst**: promoted iron (α-Fe from magnetite, Fe₃O₄); promoters K₂O (electronic promoter, increases electron density at Fe surface) and Al₂O₃ (structural promoter, prevents sintering).
- **Temperature**: 400–500 °C. Lower T favors equilibrium (exothermic), but kinetics are too slow below ~350 °C on iron catalyst. Upper limit set by catalyst sintering and equilibrium yield.
- **Pressure**: 150–300 atm (modern plants typically 150–200 atm; older Haber plants 200–300 atm). Higher pressure shifts equilibrium toward NH₃ (fewer moles of gas product) and increases reaction rate.
- **Conversion per pass**: ~15–25% (limited by equilibrium). Unreacted N₂/H₂ is recycled after NH₃ is condensed out.
- **H₂ source**: primarily steam methane reforming (SMR): CH₄ + H₂O → CO + 3H₂, then water-gas shift CO + H₂O → CO₂ + H₂. Green ammonia uses electrolytic H₂.

**Small-scale / DIY consideration:**
- Full Haber-Bosch requires high-pressure equipment, pure N₂ and H₂ feeds, and activated iron catalyst. Not DIY-feasible.
- Some hobbyist chemistry literature discusses electrosynthesis of ammonia (electrochemical nitrogen reduction), but yields are currently micromolar-scale — not practically useful for refrigerant quantities.

**Purchasing / Sourcing:**
- **Aqueous ammonia (ammonium hydroxide, 26–30% w/w)**: Sold at hardware stores as "household ammonia" (5–10%) or janitorial concentrate (26–30%). NOT suitable as refrigerant R-717 — water contamination will cause acid in refrigerant system and destroy steel/iron components.
- **Anhydrous ammonia (> 99.5% purity)**: The actual refrigerant grade. Available from:
  - **Agricultural suppliers** (as fertilizer, NH₃ is the largest use of ammonia globally): sold in 1-ton nurse tanks to farmers; can often purchase smaller quantities by arrangement.
  - **Industrial gas suppliers** (Air Products, Praxair/Linde, Airgas): in cylinders.
  - **Refrigerant distributors**: refrigerant-grade R-717 in cylinders.
- **Regulations**: Anhydrous ammonia is an EPA-listed Extremely Hazardous Substance. OSHA PSM (Process Safety Management) applies to facilities holding ≥ 10,000 lbs. No EPA 608 requirement for NH₃ (it is not an ODS), but storage and handling regulations apply.

**Safety critical data:**
- IDLH (Immediately Dangerous to Life/Health): **300 ppm**
- OSHA PEL (8-hr TWA): **25 ppm**; ACGIH TLV: 25 ppm
- LEL/UEL: **15% / 28%** in air (flammable at high concentrations)
- Immediately detectable by smell at ~1–5 ppm; strong warning properties
- Attacks copper, copper alloys (brass, bronze), and zinc — all piping and components must be steel, aluminum, or stainless steel. No copper tubing.
- Water in system forms corrosive alkaline solution that attacks steel; stringent drying required.

---

### 3.4 R-744 — Carbon Dioxide

**Chemistry / Industrial Source:**
CO₂ is captured as a by-product from:
1. **Combustion flue gas** (post-combustion capture)
2. **Fermentation**: brewery fermentation CO₂ is a major source of food-grade CO₂
3. **Ammonia plant off-gas**: CO₂ from SMR/water-gas-shift is recovered
4. **Natural wells**: naturally occurring CO₂ is mined in some locations (e.g., Colorado, New Mexico)

**DIY considerations:** CO₂ is not synthesized for refrigerant use; it is captured and purified. Food-grade CO₂ from a beverage gas supplier is essentially the same purity as refrigerant-grade.

**Purchasing / Sourcing:**
- **Beverage-grade CO₂ cylinders**: widely available from homebrew shops, restaurant suppliers, welding suppliers. Food-grade (≥99.9% purity) is suitable.
- **SodaStream cylinders**: small, contain about 400–500 g CO₂; refillable at many locations.
- **Dry ice (solid CO₂)**: available at grocery stores, gas stations — sublimes at −78.5 °C at 1 atm.

**Transcritical cycle note:** Above 31.1 °C ambient, R-744 systems cannot condense — they operate in **transcritical mode**. The gas cooler (heat exchanger) cools high-pressure supercritical CO₂ but does not condense it. Expansion is from a high-pressure supercritical state. This requires:
- High-side pressures 90–130 bar (up to ~140 bar in very hot climates)
- Special thick-walled components (not standard HVAC hardware)
- Electronic back-pressure valves for discharge pressure control
- R-744 systems are increasingly used for commercial refrigeration (supermarkets) and heat pump water heaters where high-temperature heat delivery is valuable

---

### 3.5 R-134a, R-410A, R-1234yf — HFCs and HFOs

**Chemistry:** These refrigerants are synthesized by complex fluorination chemistry:
- **R-134a (CH₂FCF₃)**: produced by fluorination of trichloroethylene (CCl₂=CCl₂ + HF → intermediate → CH₂FCF₃). Requires HF chemistry, specialty reactors, corrosion-resistant Inconel/Monel equipment, catalysts (SbCl₅-based), and precise temperature control.
- **R-410A**: blend of R-32 (CH₂F₂, difluoromethane) and R-125 (CHF₂CF₃, pentafluoroethane), each requiring multi-step fluorination of precursor chlorocarbons or direct fluorination.
- **R-1234yf (CF₃CF=CH₂)**: synthesized from R-1234ze precursors or by dehydrofluorination routes involving hexafluoropropylene oxide intermediates; proprietary processes (Chemours/Honeywell).

**DIY synthesis: Not feasible.** HF (hydrofluoric acid) chemistry requires specialized corrosion-resistant equipment, specialized scrubbing for HCl/HF exhaust, and operates under significant pressure at elevated temperatures. Fatal burns at tiny exposures (HF penetrates skin and sequesters calcium, causing systemic toxicity). No hobbyist-accessible route exists.

**Purchasing / Sourcing:**
- **HVAC/refrigerant distributors**: primary source; Johnstone Supply, Wesco, Grainger, Refrigerants Inc., etc.
- **EPA Section 608 certification** required for purchase of refrigerants in containers > 2 lbs that are regulated under Section 608. As of 2021, this includes HFCs (R-134a, R-410A). The rule was expanded to cover HFCs to prevent venting.
- **R-1234yf**: sold primarily to automotive dealers/certified shops; Chemours (Opteon YF) and Honeywell (Solstice yf) are the main suppliers. Significantly more expensive than R-134a (~4–6× per pound).
- **Small cans (≤2 lbs)**: legally purchasable without 608 cert for specific self-sealing can products, but this exemption is narrowing.

---

## 4. Key System Components

### 4.1 Compressors

The compressor is the only component requiring external work input (W_net). It raises refrigerant pressure from evaporating to condensing level and keeps refrigerant circulating.

#### Reciprocating Compressor
- **Mechanism**: piston-cylinder with reed valves or Schrader-type check valves; positive displacement.
- **Capacity range**: 0.1 kW to > 1,000 kW (hermetic → open-drive industrial).
- **Types**: hermetic (motor sealed inside, no shaft seal, most household), semi-hermetic (bolted crankcase, serviceable), open-drive (external motor with shaft seal).
- **Pros**: high pressure ratios achievable; tolerates slugging (liquid refrigerant) better than scrolls; wide operating range.
- **Cons**: more moving parts, higher vibration, pulsating flow; needs suction accumulator in many applications.
- **Volumetric efficiency** η_vol drops at high compression ratio: η_vol ≈ 1 − C[(P_H/P_L)^(1/n) − 1], where C = clearance volume ratio (~0.02–0.05), n = polytropic index.

#### Scroll Compressor
- **Mechanism**: two interleaved Archimedean spiral scrolls (one fixed, one orbiting); refrigerant pockets are progressively compressed from outer periphery to center.
- **Capacity range**: 1–20 kW; dominant in residential split AC systems and heat pumps.
- **Pros**: very quiet, smooth flow (no pulsation), fewer moving parts, high efficiency at design conditions, compact.
- **Cons**: cannot reverse rotation (will pump outward, no compression — wrapping contacts would damage it); less tolerant of liquid slugging than reciprocating; requires precise machining.
- **Isentropic efficiency**: typically 0.68–0.78 at rated conditions.

#### Rotary (Rolling Piston) Compressor
- **Mechanism**: eccentric rotor rolls inside a cylinder; a spring-loaded vane divides suction from discharge.
- **Capacity range**: 0.3–5 kW; very common in room air conditioners, window ACs, mini-splits, and household refrigerators in Asia.
- **Pros**: very compact, low vibration, simple construction, low cost.
- **Cons**: moderate efficiency; vane wear over time; limited pressure ratio.

#### Screw Compressor (Twin-Rotor)
- **Mechanism**: two intermeshing helical rotors (male + female); gas is trapped between rotor lobes and end plates, progressively compressed.
- **Capacity range**: 50–2,000 kW; commercial and industrial refrigeration, chillers.
- **Pros**: continuous flow, very high reliability, handles liquid injection (economizer ports); variable capacity via slide valve.
- **Cons**: oil injection required for sealing and cooling (must be separated from refrigerant); high cost; not suitable for small systems.

#### Centrifugal (Turbocompressor)
- **Mechanism**: high-speed impeller(s) impart velocity to vapor; velocity converted to pressure in diffuser. Dynamic (not positive displacement) compression.
- **Capacity range**: 200 kW to > 10 MW; large chiller plants.
- **Pros**: very high capacity, smooth flow, efficient at large scale.
- **Cons**: susceptible to **surge** at low load (must use hot gas bypass or variable speed drive); not suitable for high pressure ratios per stage; minimum practical capacity limit.

---

### 4.2 Expansion Devices

The expansion device reduces refrigerant from high-side to low-side pressure. The process is isenthalpic (throttling): enthalpy h₃ = h₄, but entropy increases (irreversible). Flash evaporation cools the remaining liquid to the evaporating temperature.

#### Capillary Tube
- **Mechanism**: a fixed-geometry tube (typically 0.5–2 mm ID, 0.5–5 m long) creates pressure drop through viscous friction.
- **Applications**: household refrigerators, freezers, window AC units, small dehumidifiers, pre-charged sealed systems.
- **Sizing**: flow resistance depends on L/D ratio, refrigerant properties, and pressure differential. Selected by iteration or empirical charts for a specific design point.
- **Pros**: no moving parts, no maintenance, very low cost (cents), self-balancing to some extent during off cycles (pressures equalize, reducing compressor start-up torque).
- **Cons**: fixed restriction — cannot adapt to load changes; prone to moisture/debris plugging; system performance degrades significantly at off-design ambient temperatures; requires precise refrigerant charge (system sensitive to overcharge/undercharge).

#### Thermostatic Expansion Valve (TXV / TEV)
- **Mechanism**: a spring-loaded needle valve modulated by a thermostatic power element. A sensing bulb filled with charge fluid (similar or identical to refrigerant) is clamped to the suction line after the evaporator. As suction superheat increases, bulb pressure rises, opening the valve; as superheat decreases, it closes. External equalizer port senses evaporator outlet pressure to compensate for pressure drop.
- **Applications**: residential split systems, commercial refrigeration, large-capacity systems.
- **Superheat setpoint**: typically 4–8 K (factory adjustable via spring tension).
- **Pros**: automatically maintains near-full evaporator utilization; adapts to variable load.
- **Cons**: hunting (oscillation around setpoint) at low load; does not optimize for overall system efficiency; bulb placement is critical.

#### Electronic Expansion Valve (EEV)
- **Mechanism**: stepper motor or pulse-width-modulated solenoid drives a needle into a port; controlled by the system controller (ECU/microprocessor) using multiple sensor inputs (suction superheat, discharge temperature, load sensors).
- **Applications**: inverter-driven mini-splits, variable refrigerant flow (VRF) systems, heat pump water heaters, commercial showcases with sophisticated controls.
- **Pros**: precise superheat control; enables rapid response to load changes; supports economizer and vapor injection strategies; allows sub-zero superheat in some modes.
- **Cons**: requires electronics and wiring; more expensive; failure mode if controller or motor fails.

---

### 4.3 Heat Exchangers

#### Fin-and-Tube (Air-to-Refrigerant)
- Most common type for air conditioners, heat pumps, and domestic refrigerators.
- **Construction**: copper or aluminum tubes (0.5–12 mm OD) with aluminum fins at 1.5–4 mm pitch. Refrigerant flows inside tubes; air flows over fins under fan pressure.
- **Evaporators**: typically 3–10 rows deep, with large fin area for low ΔT and low air-side pressure drop.
- **Condensers**: fewer rows, higher air velocity acceptable.
- **Fin types**: plain, wavy (corrugated), louvered, lanced; louvered fins give best heat transfer coefficient at the cost of higher air-side pressure drop.
- **Frosting**: evaporators operating below 0 °C will frost; requires defrost cycle (electric resistance or hot-gas bypass).

#### Microchannel (MCHX)
- **Construction**: flat aluminum multi-port extrusions (~0.5–1.5 mm channels) with louvered aluminum fins, brazed assembly.
- **Applications**: automotive condensers (now nearly universal), modern residential and commercial condensers; increasingly used in evaporators.
- **Pros**: higher heat transfer coefficient, lower refrigerant charge (30–50% less than fin-and-tube), lower air-side pressure drop at same capacity, lighter.
- **Cons**: more susceptible to corrosion in coastal/industrial environments; difficult to repair in the field; oil return from microchannel evaporators requires careful design.

#### Shell-and-Tube
- **Construction**: refrigerant in tubes (or shell-side), water or brine on the other side. Tube bundles with baffles.
- **Applications**: large water chillers (flooded evaporator or DX), industrial heat exchangers, condensers in large systems.
- **Flooded evaporator**: refrigerant floods the shell side at saturation; tubes carry chilled water. Very efficient heat transfer due to nucleate boiling; requires more refrigerant charge.

#### Brazed-Plate Heat Exchanger (BPHE)
- **Construction**: thin (0.4–0.6 mm) corrugated stainless steel plates dip-brazed with copper or nickel. Alternating refrigerant and secondary fluid channels.
- **Applications**: geothermal heat pumps (refrigerant-to-water), solar/hydronic systems, industrial chillers.
- **Pros**: very compact for capacity; high overall heat transfer coefficient (U ≈ 2,000–5,000 W/m²K for water-to-refrigerant).
- **Cons**: prone to freezing/fouling; not repairable — must replace entire unit.

---

## 5. Design Equations

### 5.1 System Performance

**COP (cooling):**
$$\text{COP}_c = \frac{\dot{Q}_L}{\dot{W}_{comp}} = \frac{h_1 - h_4}{h_2 - h_1}$$

**Mass flow rate:**
$$\dot{m} = \frac{\dot{Q}_L}{h_1 - h_4} \quad [\text{kg/s}]$$

where $\dot{Q}_L$ is cooling capacity [kW], and enthalpies are read from P–h diagram or refrigerant property tables.

**Compressor power (actual):**
$$\dot{W}_{comp} = \frac{\dot{m}(h_{2s} - h_1)}{\eta_s} \quad [\text{kW}]$$

where $h_{2s}$ is isentropic discharge enthalpy and $\eta_s$ is isentropic efficiency.

**Condenser heat rejection:**
$$\dot{Q}_H = \dot{m}(h_2 - h_3) = \dot{Q}_L + \dot{W}_{comp}$$

### 5.2 Compressor Displacement

The required compressor swept volume (displacement) for a target cooling capacity:

$$\dot{V}_{disp} = \frac{\dot{m} \cdot v_1}{\eta_{vol}} \quad [\text{m}^3/\text{s}]$$

where:
- $v_1$ = specific volume at compressor suction [m³/kg] (from property tables or ideal gas: $v = RT/P$ as approximation only)
- $\eta_{vol}$ = volumetric efficiency ≈ 0.70–0.88

For a reciprocating compressor at speed N [rev/s] with n cylinders of bore B and stroke S:

$$\dot{V}_{disp} = n \cdot \frac{\pi B^2}{4} \cdot S \cdot N$$

**Example**: R-290 system, 1 kW cooling, evap 0 °C, cond 45 °C:
- h₁ (sat. vapor, 0 °C) ≈ 569 kJ/kg
- h₄ ≈ h₃ (sat. liquid, 45 °C) ≈ 277 kJ/kg  [isenthalpic expansion]
- h₂ (isentropic discharge) ≈ 643 kJ/kg
- ṁ = 1.0 / (569 − 277) = 3.42 g/s
- v₁ (sat. vapor at 0 °C, R-290) ≈ 0.043 m³/kg
- V̇_disp = (3.42 × 10⁻³ × 0.043) / 0.80 ≈ 1.84 × 10⁻⁴ m³/s ≈ 11.1 L/min displacement

### 5.3 Heat Exchanger Sizing — LMTD Method

For a heat exchanger with overall heat transfer coefficient U [W/m²K] and surface area A [m²]:

$$\dot{Q} = U \cdot A \cdot \text{LMTD}$$

**Log Mean Temperature Difference (LMTD)** for a counterflow arrangement:

$$\text{LMTD} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)}$$

where ΔT₁ and ΔT₂ are the temperature differences at each end of the exchanger.

**For a condenser** (refrigerant condenses at T_cond, air enters at T_air,in, exits at T_air,out):

$$\Delta T_1 = T_{cond} - T_{air,in}$$
$$\Delta T_2 = T_{cond} - T_{air,out}$$

**For an evaporator** (refrigerant evaporates at T_evap, air enters at T_air,in, exits at T_air,out):

$$\Delta T_1 = T_{air,in} - T_{evap}$$
$$\Delta T_2 = T_{air,out} - T_{evap}$$

**Typical U values (fin-and-tube, air-to-refrigerant):**
- Condenser: U ≈ 25–80 W/m²K (based on outer tube area, including fins via fin efficiency)
- Evaporator (dry): U ≈ 20–60 W/m²K
- Evaporator (wet/condensing): U ≈ 40–80 W/m²K (water film enhances heat transfer)

**Fin efficiency:**
$$\eta_{fin} = \frac{\tanh(mL)}{mL}, \quad m = \sqrt{\frac{2h}{k_{fin} \cdot \delta_{fin}}}$$

where h = air-side heat transfer coefficient [W/m²K], k_fin = fin conductivity (Al ≈ 200 W/mK), δ_fin = fin thickness [m].

**Overall surface efficiency** (accounting for fin efficiency and base area):
$$\eta_o = 1 - \frac{A_{fin}}{A_{total}}(1 - \eta_{fin})$$

Then: $\dot{Q} = \eta_o \cdot h_{air} \cdot A_{total} \cdot \text{LMTD}$ (air-side dominant resistance)

### 5.4 Refrigerant Pipe Sizing

Suction line — sized for acceptable pressure drop (< 0.5–1 K equivalent saturation temperature loss) and minimum velocity for oil return:

**Minimum velocity for oil return (vertical risers):**
$$v_{min} \approx 4\;\text{m/s (R-22/R-410A)} \quad v_{min} \approx 3\;\text{m/s (R-717)}$$

**Pressure drop in straight pipe (Darcy-Weisbach):**
$$\Delta P = f \cdot \frac{L}{D} \cdot \frac{\rho v^2}{2} \quad [\text{Pa}]$$

where f is Darcy friction factor (use Moody chart or Colebrook equation for turbulent flow in smooth copper: f ≈ 0.015–0.025).

---

## 6. DIY Practical Notes

### 6.1 Using Automotive (Car AC) Compressors

Car AC compressors are widely available, cheap (used, $20–$150), and robust — making them popular for DIY refrigeration projects.

**Common compressor types:**
- **Sanden (SD) rotary vane series** (SD505, SD507, SD508): extremely common OEM, good quality, open-drive with external pulley. Many units available as "reman" cores from auto parts stores.
- **Denso 10PA, 10S series**: 10-cylinder double-acting, high capacity.
- **Denso 6SEU, 7SEU**: newer scroll compressors used in modern vehicles; internally fixed compression ratio, less tolerant of off-design operation.
- **Sanden TRSE series**: newer, more efficient; uses R-134a or R-1234yf.

**Drive options:**
- **Belt-drive**: run the pulley with an electric motor (1,450–3,000 RPM typical). Requires matching pulley diameters. A 1 HP (750 W) motor is sufficient for a small system (~0.5–1 kW cooling).
- **Clutch engagement**: standard automotive clutch requires 12 V DC (~2–4 A). For continuous operation, wire it directly to battery/DC supply, or remove clutch and weld/bolt pulley to shaft (irreversible).
- **Electric AC compressors** (Toyota Prius, Tesla HVAC compressors): internally driven by 3-phase inverter; can be repurposed with a suitable variable-frequency drive (VFD) or dedicated inverter. High efficiency but complex.

**Oil compatibility:**
- R-134a compressors use **PAG (polyalkylene glycol)** oil (ISO VG 46 or 100). PAG is hygroscopic — keep dry.
- When retrofitting to R-290 or R-600a: use **POE (polyol ester)** oil, which is compatible with natural refrigerants and HFCs. Drain PAG oil from used compressor before charging with natural refrigerants.
- R-717 (ammonia): requires **mineral oil** or **alkylbenzene oil** (not PAG or POE — ammonia hydrolyzes esters). Uses steel/aluminum compressors only.

**Fittings:** Standard SAE J639 1/4" (#6 SAE) low side and 3/8" (#10 SAE) high side flare fittings are common on many compressors. Some use Schrader valve access ports (standard auto AC service ports).

### 6.2 Natural Refrigerant DIY Systems (R-290, R-600a)

**Charge limits — why they matter:**
- With R-290, 150 g is sufficient for a ~200–300 W cooling system (small chest freezer conversion).
- Staying under 150 g (per IEC 60335-2-89 / UL 60335-2-89) keeps the system in the "lower charge limit" category and reduces risk classification.
- Above ~600 g of propane, you enter the territory where a single leak could create a flammable atmosphere in a room — design accordingly.

**Tubing materials:** Standard ACR (air conditioning & refrigeration) copper tubing (Type L or ACR cleaned/dehydrated) is fine for R-290, R-600a, CO₂ (below critical), and R-134a. NOT for ammonia.

**Component sourcing:**
- Reciprocating compressors for R-290/R-600a: Embraco, Secop (formerly Danfoss), Nidec-Global, and Kulthorn make hermetic compressors specifically rated for these refrigerants.
- Dedicated "hydrocarbon" compressors have spark-free motor windings and are designed for flammable charge.
- **Do not use** standard HFC compressors with propane/isobutane unless the compressor manufacturer explicitly approves — motor winding materials may not be compatible, and the units are not rated for the different operating pressures.

### 6.3 Pressure Gauge Usage (Manifold Gauge Set)

**Standard manifold gauge set:**
- **Blue gauge** (compound gauge): low-side pressure; typically reads −30 inHg to 120 psi (or 0–10 bar). Reads below-atmospheric pressures for evacuation monitoring.
- **Red gauge**: high-side pressure; typically reads 0–500 psi (or 0–35 bar). Some high-pressure sets go to 800 psi for R-410A and CO₂.
- **Hose color convention**: blue = low side suction, red = high side discharge, yellow = refrigerant cylinder / recovery tank / vacuum pump.
- **Outer scale**: temperature scale calibrated for common refrigerant saturation temperatures — allows reading "saturation temperature" directly without tables.

**Evacuation procedure:**
1. Connect yellow hose to vacuum pump; open both manifold valves.
2. Evacuate to < 500 microns (0.5 mmHg / 67 Pa) — use a micron gauge (electronic vacuum gauge), not a refrigerant manifold gauge (insufficient resolution at these pressures).
3. Isolate and hold vacuum for 15–30 minutes: a rise indicates a leak or moisture.
4. Triple evacuation (evacuate → break with dry nitrogen → re-evacuate × 3) is standard best practice for systems with suspected moisture.
5. Backfill with nitrogen to ~5 psig before opening for service if moisture ingress is suspected.

**Pressure testing:**
- Leak test with dry nitrogen (never use air — oxygen + refrigerant oil is a fire risk; never use oxygen or refrigerant for pressure testing).
- R-290 system: test to 1.1× maximum working pressure. MAWP for low side typically ~10 bar; test at ~11 bar N₂.
- Use leak detection: electronic refrigerant detector (semiconductor type for HFCs; catalytic bead type for hydrocarbons; electrochemical for NH₃), soapy water solution, or fluorescent UV dye (HFCs only).

### 6.4 Safety Requirements Summary

| Hazard | R-290 / R-600a | R-717 | R-744 | R-134a / R-410A |
|---|---|---|---|---|
| Flammability | High (A3) — explosive range | Moderate (B2L) at high conc. | None | None (R-1234yf: mildly flammable A2L) |
| Toxicity | Low | High (IDLH 300 ppm) | Asphyxiant at high conc. | Low |
| Pressure hazard | Moderate | Moderate | **Extreme** (>130 bar) | Moderate–High |
| PPE required | Fire/spark precautions; ventilation | Full-face respirator (APF 50+), ammonia-rated; self-contained BA for confined space | High-pressure training; blast shield; CO₂ meter | Safety glasses; gloves |
| Piping material | Copper, steel | Steel, aluminum only | Special high-pressure rated | Copper, steel |
| Electrical | Class I, Div. 2 zone | Class I, Div. 2 zone | Standard | Standard |

**General rules:**
- Always work in a ventilated area or outdoors.
- Never heat refrigerant cylinders above 52 °C (125 °F).
- Never fill a cylinder to > 80% liquid fill by weight.
- Install refrigerant-rated pressure relief devices on vessels and trapped liquid sections.
- Keep a CO₂ or dry-chemical fire extinguisher nearby when working with R-290/R-600a.
- For ammonia: have an ammonia gas detector, water-spray/shower nearby, and a clear egress path.

---

## 7. Key Surprising Facts

1. **COP can far exceed 1.0** — Unlike heat engines that are thermodynamically limited to COP < 1 for work output, a refrigerator (or heat pump) can deliver 3–6 units of thermal energy per unit of work input. The "extra" energy comes from the low-temperature thermal reservoir, not from creating energy. COP_Carnot for T_L = 0 °C, T_H = 35 °C is 7.8 — even real systems commonly achieve COP 3–5.

2. **R-744 (CO₂) systems run at pressures that would fail standard AC equipment** — A CO₂ commercial refrigeration system high side can reach 130–140 bar (~2,000 psi) in summer. Standard automotive AC operates at ~14–18 bar high side. This means CO₂ systems require tubing and components roughly 8–10× the wall thickness of conventional HVAC. A CO₂ leak test pressure can exceed the burst pressure of an R-134a manifold gauge.

3. **The expansion process is entirely irreversible and is a significant source of COP loss** — Throttling generates entropy; no work is recovered. In large ammonia systems (>500 kW), **expansion turbines** (expanders) are used to recover some of this work — isentropic expansion produces mechanical energy rather than just flash cooling. A two-stage expander can recover 15–25% of this "waste" energy.

4. **Subcooling is nearly free efficiency** — Subcooling the liquid refrigerant by 5–10 K before the expansion valve increases Q_L (more refrigerating effect per kg) without increasing compressor work. In a properly designed system, the suction line can act as a liquid-suction heat exchanger (LSHX), subcooling the liquid while slightly superheating the vapor — net COP improvement of 3–8% with no added components.

5. **R-410A cannot be used in R-22 systems** — R-410A operates at ~60–70% higher pressures than R-22. Simply retrofitting an R-22 system with R-410A would burst the low-side service ports, TXV, and possibly the evaporator and filter-drier. Equipment rated for R-22 uses different materials and wall thicknesses. There is no "drop-in" replacement for R-22 in older systems; retrofit requires replacing almost all components.

6. **Refrigerant charge quantity is startlingly critical** — A ±10% deviation from the correct charge can reduce COP by 5–15% and in extreme cases can destroy the compressor. Overcharge in a system with a TXV causes liquid slugging (hydraulic compressor damage); overcharge in a capillary tube system floods the compressor with liquid immediately on startup. The charge is not "added until it seems cold enough" — it must be weighed in or charged to a precise superheat/subcooling target.

7. **Compressor oil travels the entire refrigerant circuit** — Oil is carried along with refrigerant vapor through the discharge line, condenser, expansion device, and evaporator, and must return to the compressor via the suction line. Oil velocity in suction lines must be > ~3–4 m/s upward in vertical risers to carry oil back. Inadequate velocity causes "oil logging" in the evaporator, reducing heat transfer and eventually starving the compressor of lubrication. This is why suction line sizing and double risers (one small, one large, for part-load operation) are critical in variable-capacity systems.

8. **Ammonia has the best thermodynamic properties of any common refrigerant** — NH₃ has the highest latent heat of vaporization (~1,370 kJ/kg vs ~220 kJ/kg for R-134a) and lowest molecular weight (17 vs 102 g/mol), giving it exceptional volumetric refrigerating capacity and high COP at most conditions. The entire global food cold chain — meat packing, ice cream, frozen food, fish processing — runs predominantly on ammonia. Only its toxicity limits residential use.

9. **Scroll compressors will fail immediately if run backward** — A scroll compressor running in reverse rotation will push refrigerant outward instead of inward — achieving essentially zero compression — and the orbiting scroll tip seals will be rapidly destroyed by contact in the wrong direction. Many modern scroll compressors have a check valve to prevent reverse rotation, but during wiring/phase errors in 3-phase commercial equipment, scroll compressor failures from reverse rotation are common field failures.

10. **Flash gas at the expansion valve is the enemy of efficiency** — When refrigerant at the expansion valve inlet is saturated or near-saturated, some flashes immediately to vapor upon pressure drop. This flash vapor does no additional useful cooling in the evaporator (it arrived as vapor) but must still be compressed. A practical consequence: liquid-line pressure drop from a long or undersized liquid line causes partial flashing before the TXV, dramatically reducing system capacity. This is why liquid line sizing and the liquid-line solenoid valve placement are carefully engineered.

11. **Domestic refrigerators use R-600a at charges sometimes as low as 30 grams** — Modern European domestic refrigerators use R-600a charges of 30–130 g. At 30 g, the energy content is roughly equivalent to a tablespoon of lighter fluid. The low-side pressure is close to atmospheric (isobutane boils at −11.7 °C), so even a catastrophic leak carries minimal explosion risk if vented in a reasonably ventilated space.

12. **A transcritical CO₂ heat pump water heater can achieve COP > 4 while heating water to 90 °C** — Because CO₂ does not condense in the gas cooler but instead glides from ~110 °C down to ~15 °C (matching the temperature glide of the water being heated from cold inlet to hot outlet in a counterflow arrangement), the heat exchange is thermodynamically near-ideal. This temperature glide matching is a fundamental advantage that R-744 has over condensing refrigerants in heat pump water heaters — it is why R-744 heat pump water heaters (Sanden, Eco Cute) dominate the high-efficiency water heating market in Japan.

---

## References and Further Reading

- **ASHRAE Fundamentals Handbook** (2021): Chapters 1–4 (Thermodynamics), Chapter 29 (Refrigerants), Chapter 43 (Compressors).
- **ASHRAE Refrigeration Handbook** (2022): Systems, components, and industrial refrigeration.
- **IIR (International Institute of Refrigeration)**: NIST REFPROP thermodynamic properties database — the gold standard for refrigerant P–h diagrams and property calculations. Available at [webbook.nist.gov](https://webbook.nist.gov/chemistry/fluid/) (free online fluid properties).
- **EPA Section 608** regulations: [epa.gov/section608](https://www.epa.gov/section608)
- **NIST REFPROP**: industry-standard refrigerant properties software (NIST; paid license or web interface).
- **CoolProp**: open-source refrigerant property library (Python, C++, MATLAB bindings) — excellent free alternative to REFPROP for DIY calculations. [coolprop.org](http://www.coolprop.org)
- **UN Environment RTOC reports**: Refrigeration, Air Conditioning and Heat Pump Technical Options Committee — covers HFC phase-down, low-GWP alternatives.
