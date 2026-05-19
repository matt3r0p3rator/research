# Refrigeration Techniques: Master Guide

*How to cool things using electricity, heat (burner), or other means — with materials, synthesis, and calculation tools.*

**Last updated:** May 18, 2026

---

## Overview

This guide covers all practical refrigeration technologies organized by energy input type:

| Energy Input | Technology | Temperature Range | COP | Complexity |
|---|---|---|---|---|
| **Electricity** | Vapor-compression | −60°C to +15°C | 2–5 | Moderate |
| **Electricity** | Thermoelectric (Peltier) | −105°C to just below ambient | 0.3–0.8 | Easy |
| **Electricity** | Stirling cycle cryocooler | 4 K to −40°C | 0.1–0.5 (fraction of Carnot) | Hard |
| **Heat (burner/waste)** | Absorption refrigeration | −60°C to +10°C | 0.4–1.4 | Moderate-Hard |
| **Heat (burner/waste)** | Adsorption refrigeration | −30°C to +15°C | 0.3–0.6 | Moderate |
| **Compressed air** | Vortex tube | 20–50°C below inlet | ~0.1 | Easy |
| **Electricity (magnets)** | Magnetocaloric | Near room temp | ~1.0 | Very Hard |
| **Nothing (passive)** | Radiative sky cooling | 5–15°C below ambient | N/A | Easy |
| **Chemical reaction** | Endothermic packs | Down to −20°C (single use) | N/A | Trivial |
| **Acoustic (speaker)** | Thermoacoustic | 4 K to −100°C | 0.1–0.4 | Hard |

---

## File Index

Each technology has its own detailed file:

| File | Contents |
|---|---|
| [vapor-compression-refrigeration-research.md](vapor-compression-refrigeration-research.md) | Thermodynamic cycle, refrigerants (R-290, R-717, R-744, etc.), synthesis/sourcing, compressor types, design equations, DIY notes |
| [absorption-refrigeration-research.md](absorption-refrigeration-research.md) | NH₃-H₂O and LiBr-H₂O cycles, Haber-Bosch ammonia synthesis, LiBr synthesis, Einstein refrigerator, building a unit |
| [thermoelectric-peltier-cooling-research.md](thermoelectric-peltier-cooling-research.md) | Seebeck/Peltier physics, ZT figure of merit, Bi₂Te₃ synthesis (4 routes), PbTe/SnSe/SiGe, module construction, cascade TEC |
| [cooling-methods-research.md](cooling-methods-research.md) | Adsorption cycles, zeolite/silica gel/activated carbon synthesis, magnetocaloric, vortex tube, thermoacoustic, evaporative, radiative, JT expansion, chemical cooling |
| [stirling-cycle-refrigeration-research.md](stirling-cycle-refrigeration-research.md) | Stirling cycle, pulse tube, Gifford-McMahon, cryogenic temperatures, Schmidt analysis, Python code, calculation tools (CoolProp, REFPROP, EES, etc.) |

---

## Quick Decision Guide

### What technology should I use?

```
Do I have electricity available?
  YES → How much cooling do I need?
    | Small (watts), no moving parts desired → Thermoelectric (Peltier)
    | Moderate to large, best efficiency → Vapor-compression
    | Cryogenic temperatures (<−100°C) → Stirling / Pulse tube / GM cryocooler
  
  NO → Do I have waste heat or a burner?
    YES → Absorption refrigeration (NH₃-H₂O or LiBr-H₂O)
          OR Adsorption (silica gel/zeolite + solar thermal)
    
  → Do I have compressed air?
    YES → Vortex tube (simple, no refrigerant, low efficiency)
    
  → Do I want passive cooling only?
    YES → Radiative sky cooling, evaporative cooling, PCM thermal mass
    
  → One-time/emergency cooling?
    YES → Endothermic chemical packs (NH₄NO₃ + water)
```

### Temperature ranges at a glance

```
Temperature (°C)
+20 ─── Radiative sky cooling, evaporative cooling
  0 ─── Ice/water PCM; LiBr-H₂O absorption lower limit
−20 ─── NH₃-H₂O absorption, AC-methanol adsorption, Peltier (single stage)
−40 ─── Vapor-compression, NH₃-H₂O deep freeze mode
−60 ─── NH₃-H₂O low side; double-stage vapor compression
−80 ─── 2–3 stage cascaded Peltier
−100 ─── 4-stage Peltier, Stirling cooler (single stage ≈ −150°C achievable)
−150 ─── Stirling single stage, Gifford-McMahon
−196 ─── Liquid nitrogen (passive storage/use)
−269 ─── Pulse tube / GM two-stage cryocooler
  4 K ─── Pulse tube / dilution refrigerator (with JT)
```

---

## Section 1: Vapor-Compression Refrigeration (Electric)

> **Detailed file:** [vapor-compression-refrigeration-research.md](vapor-compression-refrigeration-research.md)

### How It Works

Four-step cycle:
1. **Evaporator:** Low-pressure refrigerant absorbs heat from cold space → evaporates
2. **Compressor (electric motor):** Vapor compressed to high pressure and temperature
3. **Condenser:** High-pressure vapor rejects heat to ambient → condenses to liquid
4. **Expansion device:** Liquid throttles back to low pressure (isenthalpic) → back to evaporator

**COP equations:**
$$\text{COP}_{cooling} = \frac{Q_{evap}}{W_{compressor}} = \frac{h_1 - h_4}{h_2 - h_1}$$
$$\text{COP}_{Carnot} = \frac{T_{cold}}{T_{hot} - T_{cold}} \quad \text{(temperatures in Kelvin)}$$

### Key Refrigerants

| Refrigerant | Formula | Normal BP | GWP₁₀₀ | Safety | Low/High Pressure @ 0°C evap / 45°C cond |
|---|---|---|---|---|---|
| R-290 (propane) | C₃H₈ | −42.1°C | 3 | A3 (flammable) | 4.7 / 16.8 bar |
| R-600a (isobutane) | C₄H₁₀ | −11.7°C | 3 | A3 (flammable) | 1.4 / 5.4 bar |
| R-717 (ammonia) | NH₃ | −33.4°C | 0 | B2L (toxic) | 4.3 / 17.4 bar |
| R-744 (CO₂) | CO₂ | −56.6°C (triple pt) | 1 | A1 | Transcritical; 35 bar low side typical |
| R-134a | CH₂FCF₃ | −26.4°C | 1430 | A1 (safe) | 2.9 / 11.7 bar |
| R-410A | R-32/R-125 blend | −51.4°C | 2088 | A1 | 7.9 / 26.5 bar |
| R-1234yf | CF₃CF=CH₂ | −29.4°C | 4 | A2L | Similar to R-134a |

### Refrigerant Synthesis and Sourcing

| Refrigerant | DIY Synthesis? | Practical Source |
|---|---|---|
| R-290 propane | No — industrial steam cracking/NGL fractionation | BBQ/camping cylinders, MAPP gas cylinders |
| R-600a isobutane | Possible: n-C₄H₁₀ + AlCl₃ catalyst, 80–120°C → isomerization | Some lighter fluids; household refrigerator refill |
| R-717 ammonia | Possible at small scale via Haber-Bosch; practical to buy | 26% aqueous from hardware stores; anhydrous from agricultural supply |
| R-744 CO₂ | Easy: collect from fermentation/combustion, compress and liquefy | Food-grade CO₂ cylinders (beverage supply) |
| R-134a, R-410A, R-1234yf | No — complex fluorination chemistry; not DIY | HVAC suppliers (EPA 608 certification required in US) |

**Haber-Bosch for ammonia (key reaction):**
$$\text{N}_2 + 3\text{H}_2 \xrightarrow[\text{Fe}_3\text{O}_4 + \text{K}_2\text{O} + \text{Al}_2\text{O}_3]{400-500°C, 150-300 \text{ atm}} 2\text{NH}_3 \quad \Delta H = -92.4 \text{ kJ/mol}$$

Conversion per pass: 15–25%; unreacted gas recycled. H₂ from steam methane reforming (CH₄ + H₂O → CO + 3H₂ at 700–900°C on Ni/Al₂O₃) or water electrolysis.

### Key Design Equations

**Mass flow rate:** m_dot = Q_evap / (h₁ − h₄)  
**Compressor work:** W = m_dot × (h₂ − h₁)  
**Condenser duty:** Q_cond = m_dot × (h₂ − h₃)  
**Compressor displacement:** V_d = m_dot × v₁ / η_vol  
**Pipe sizing:** 4–12 m/s liquid lines; 6–20 m/s suction vapor lines

---

## Section 2: Absorption Refrigeration (Heat/Burner Powered)

> **Detailed file:** [absorption-refrigeration-research.md](absorption-refrigeration-research.md)

### How It Works

Replaces the mechanical compressor with a **thermal compressor**: refrigerant is absorbed into a liquid at low pressure, pumped (as liquid — tiny work), then driven off by heat at high pressure. Only the small liquid pump requires electricity (~1–3% of heat input).

**Energy input:** Heat from propane burner, natural gas, waste heat, solar thermal, or even wood gas.

**COP equation:**
$$\text{COP} = \frac{Q_{evap}}{Q_{generator}} \approx \frac{Q_{evap}}{Q_{gen}}$$

### Two Main Working Pairs

**NH₃-H₂O (Ammonia-Water):**
- NH₃ = refrigerant; H₂O = absorbent
- Can cool to −60°C; requires rectifier to remove water vapor from NH₃ stream
- Operating pressures: ~4 bar low side, ~15 bar high side
- COP: 0.45–0.65 (single-effect)
- Applications: RV fridges (Dometic/Norcold), industrial ice-making, propane-powered fridges

**LiBr-H₂O (Lithium Bromide-Water):**
- H₂O = refrigerant; LiBr = absorbent
- Cannot cool below 0°C (water freezes)
- Operates entirely under vacuum (0.6–8 kPa)
- COP: 0.65–0.80 (single-effect); 1.0–1.4 (double-effect)
- Applications: commercial building air conditioning (Carrier, York, Trane chillers)

### Key Materials and Synthesis

**Ammonia (for NH₃-H₂O systems):**
- Haber-Bosch process: N₂ + 3H₂ → 2NH₃ at 400–500°C, 150–300 atm, iron catalyst
- Practically: purchase 26–29% aqueous ammonia from janitorial/chemical suppliers
- Safety: IDLH = 300 ppm; never use copper fittings (NH₃ attacks copper)

**Lithium Bromide (for LiBr-H₂O systems):**
- Synthesis: LiOH + HBr → LiBr + H₂O (best purity)
- OR: Li₂CO₃ + 2HBr → 2LiBr + H₂O + CO₂↑
- Li₂CO₃ from spodumene ore or brine evaporation
- HBr synthesis: H₂ + Br₂ → 2HBr (catalytic) OR NaBr + H₂SO₄ → HBr + NaHSO₄
- Practically: purchase 45–55% LiBr solution from chemical distributors

### Einstein Refrigerator (No Moving Parts At All)

Three-fluid system (NH₃ + butane + water) operating at **single pressure throughout** — butane acts as inert pressure-equalizing gas, allowing NH₃ to evaporate at low partial pressure without mechanical pressure difference. A **bubble pump** (narrow tube heated at bottom) drives fluid circulation with no moving parts.

- COP: 0.1–0.2 (low but zero electricity needed)
- RV fridges (Dometic, Norcold) use a variant with H₂ as the inert gas

---

## Section 3: Thermoelectric / Peltier Cooling (Electric, Solid State)

> **Detailed file:** [thermoelectric-peltier-cooling-research.md](thermoelectric-peltier-cooling-research.md)

### How It Works

The **Peltier effect:** When DC current flows through a junction of two dissimilar semiconductors, heat is pumped from one side to the other. No moving parts, no refrigerant.

**Figure of merit:**
$$ZT = \frac{S^2 \sigma T}{\kappa}$$
where S = Seebeck coefficient, σ = electrical conductivity, κ = thermal conductivity.

**COP at optimal current:**
$$\text{COP} = \frac{\alpha T_c I - \frac{1}{2}I^2 R - K \Delta T}{\alpha I \Delta T + I^2 R}$$

Commercial Bi₂Te₃ modules: ZT ≈ 1.0, COP ≈ 0.3–0.8, ΔT_max ≈ 68–72°C (single stage).

### Key Materials

| Material | ZT | Temperature | Notes |
|---|---|---|---|
| Bi₂Te₃ (commercial) | ~1.0 | Room temperature | Most common; buy as TEC modules |
| (Bi,Sb)₂Te₃ nanostructured | ~1.4 | Room temp | Enhanced by ball milling + SPS |
| PbTe (toxic — lead) | ~2.2 | 400–700 K | Mid-temperature applications |
| SnSe (single crystal) | ~2.62–3.1 | 600–900 K | Record holder; brittle |
| SiGe | ~1.0–1.3 | 900–1300 K | Space RTGs |
| Filled skutterudites | ~1.7 | 500–900 K | "Rattler" phonon scattering |

### Bi₂Te₃ Synthesis Routes

**Route A: Melt Synthesis (Bridgman)**
- Mix stoichiometric Bi + Te (+ Sb for p-type, or Se for n-type) in evacuated sealed quartz ampoule
- Melt at 620–650°C; cool at 1–5 mm/hour through thermal gradient
- ⚠️ Te vapor toxic; ampoule must be sealed under vacuum

**Route B: Mechanical Alloying + SPS (Nanostructured, higher ZT)**
- Ball mill Bi + Te powders under Ar, 10–40 hours
- Spark plasma sinter at 350–450°C, 50–100 MPa, 3–10 minutes

**Route C: Solvothermal (nanoplates)**
- BiCl₃ + SbCl₃ + Na₂TeO₃ + NaBH₄ in ethylene glycol, autoclave at 160–200°C for 12–24 hours

**Route D: Electrodeposition (thin films)**
- Bi(NO₃)₃ + TeO₂ in HNO₃; potentiostatic deposition at −130 mV vs. Ag/AgCl

### Building Your Own Peltier Cooler

Purchase TEC modules (e.g., TEC1-12706 ≈ $5–15 each on AliExpress/Amazon). For effective cooling:
- Critical: hot-side heat sink must be excellent (dominates system performance)
- R = 0.1–0.5 K/W for forced-air finned Al heat sink
- Total hot-side heat = cold-side cooling + all electrical power input
- Use PID control at minimum current needed (reduces I²R waste dramatically)
- Cascade multiple stages for temperatures below −50°C

---

## Section 4: Stirling Cycle and Cryogenic Cooling (Primarily Electric)

> **Detailed file:** [stirling-cycle-refrigeration-research.md](stirling-cycle-refrigeration-research.md)

### How It Works

Reversed Stirling cycle: mechanically compress gas at warm end → gas flows through regenerator (stores heat) → expand at cold end → gas flows back through regenerator (recovers stored heat).

**Key insight:** A perfect regenerator makes the cycle approach **Carnot efficiency**.

Working gases: Helium (preferred for cryogenic), H₂, N₂, air.

### Types and Temperature Ranges

| Technology | Temperature Range | Moving Parts in Cold Zone |
|---|---|---|
| Stirling cooler | −40°C to −150°C | Yes (cold piston/displacer) |
| Gifford-McMahon (GM) | 10 K to −150°C | Yes (cold displacer) |
| Pulse tube refrigerator | 4 K to −150°C | **No** (only warm-end components) |
| Dilution refrigerator | 10 mK to 1 K | No |

### DIY Considerations

Stirling coolers require precision machining (±0.01 mm tolerances), high-pressure seals (50–200 bar for He), and carefully designed regenerators (stainless steel mesh or Er₃Ni spheres for cryogenic stages). Commercially manufactured units are typically more practical than DIY for temperatures below −100°C.

---

## Section 5: Adsorption Refrigeration (Heat Powered, No Liquid Pump)

> **Detailed file:** [cooling-methods-research.md](cooling-methods-research.md)

### How It Works

Solid adsorbent (zeolite, silica gel, activated carbon) is heated → refrigerant desorbs → condenses in condenser → evaporates in evaporator (cooling effect) → re-adsorbs when sorbent bed cools.

Completely solid system — no liquid pump needed.

### Working Pairs

| Pair | Drive Temperature | Min Evap Temperature | COP |
|---|---|---|---|
| Silica gel / water | 60–90°C | +5°C | 0.3–0.5 |
| Zeolite 13X / water | 120–200°C | +5°C | 0.3–0.6 |
| Activated carbon / methanol | 70–120°C | −20°C | 0.3–0.5 |
| Activated carbon / ammonia | 100–200°C | −40°C | 0.3–0.4 |

### Making the Adsorbents

- **Zeolite 13X:** Hydrothermal synthesis from NaAlO₂ + Na₂SiO₃ + NaOH, 80–100°C, 6–48 hours
- **Silica gel:** Acidify sodium silicate to pH 4–6, gel forms, wash and dry at 120–180°C
- **Activated carbon:** Pyrolyze coconut shells at 500–900°C under N₂, activate with CO₂/steam at 800–900°C

---

## Section 6: Exotic and Alternative Cooling Methods

> **Detailed file:** [cooling-methods-research.md](cooling-methods-research.md)

### Vortex Tube (Compressed Air → Hot + Cold Streams)

- Compressed air (5–10 bar) enters tangentially → vortex → hot air exits one end, cold air other end
- No moving parts, no refrigerant, no electricity (only compressed air)
- Temperature separation: 20–50°C cold end below inlet
- COP: ~0.1–0.5 (inefficient but extremely simple)
- Build from: metal tube ~20 mm diameter, tangential nozzle, cone valve at hot end, small orifice at cold end
- Practical for: spot cooling tools, vests, electronics

### Magnetocaloric (Magnetic Refrigeration)

- Apply/remove magnetic field to magnetocaloric material → temperature change
- Materials: Gadolinium (Gd), Gd₅Si₂Ge₂, La(Fe,Si)₁₃, MnFe(P,As) compounds
- Near room temperature cooling demonstrated commercially (Cooltech, BASF, Astronautics)
- Adiabatic demagnetization: cooled paramagnetic salt in magnetic field → remove field → cools to millikelvin range
- COP approaching ~1.0; no refrigerant gases required
- Status (2026): room-temperature magnetic chillers still pre-mass-market; cryogenic adiabatic demagnetization well-established in labs

### Thermoacoustic Refrigeration

- Sound waves at resonance drive a thermodynamic cycle analogous to Stirling
- Standing wave type (simpler) vs. traveling wave type (higher efficiency)
- Working fluid: He or He-Ar mixtures at high pressure; driven by loudspeaker
- No moving parts in cold zone
- Can reach −100°C and cryogenic temperatures
- Los Alamos National Lab pioneered practical thermoacoustic coolers (STAR cooler)

### Evaporative Cooling

- **Direct:** Water evaporates into air stream; limited to wet-bulb temperature; ideal for dry climates
- **Indirect (dew-point coolers):** Two-stage indirect-direct; can approach dew point; cool below wet-bulb
- Materials: cellulose/ceramic evaporative pads, water pump, fan
- DIY feasibility: **Very easy**

### Passive Radiative Sky Cooling

- Special surfaces emit infrared at 8–13 μm (atmospheric transparency window) to outer space
- Can cool 5–15°C below ambient even in daytime with no energy input
- Materials: SiO₂/HfO₂ photonic multilayer films, PDRC polymer-metal composite films, specialized white paint
- Stanford 2017 demonstration: ~5°C below ambient; commercial products emerging 2022+
- DIY: apply PDRC paint or film to roof surface

### Joule-Thomson Expansion

- High-pressure gas expanded through throttle valve → cools if below inversion temperature
- N₂ inversion temp = 621 K (can use directly from compressed N₂ cylinder)
- He inversion temp = 40 K (must pre-cool He before JT expansion works)
- Used in Linde liquefaction cycle, portable cryoprobe surgical tools
- Build: needle valve + coiled precooling tube + insulation

### Endothermic Chemical Cooling (Single Use)

- NH₄NO₃ + H₂O → ΔH = +25.7 kJ/mol; reaches ~5°C (instant cold packs)
- NH₄Cl + Ba(OH)₂·8H₂O → ΔH = +54 kJ/mol; can reach −20°C
- Phase change materials (PCM): ice/water (0°C, 333 kJ/kg), Na₂SO₄·10H₂O (32°C, 254 kJ/kg)

---

## Section 7: Calculation and Simulation Tools

> **Detailed file:** [stirling-cycle-refrigeration-research.md](stirling-cycle-refrigeration-research.md) — Section 14

### CoolProp (Free, Open Source — Most Important Tool)

```bash
pip install CoolProp
```

```python
from CoolProp.CoolProp import PropsSI

# Get enthalpy of R-290 (propane) at 0°C and 4.7 bar (saturated vapor)
h = PropsSI('H', 'T', 273.15, 'P', 470000, 'R290')  # J/kg

# Saturated conditions at a given temperature
h_liq = PropsSI('H', 'T', 273.15, 'Q', 0, 'R290')   # Q=0 = saturated liquid
h_vap = PropsSI('H', 'T', 273.15, 'Q', 1, 'R290')   # Q=1 = saturated vapor

# All common refrigerants supported: 'Ammonia', 'R134a', 'R744' (CO2), 'R410A', etc.
```

Key functions: `PropsSI` for pure fluids, `HAPropsSI` for humid air.
Full documentation: http://www.coolprop.org/

### NIST REFPROP (Gold Standard, ~$300 Commercial)

Gold standard for thermodynamic properties. FORTRAN/C++/Python interface. Free alternative: NIST WebBook at https://webbook.nist.gov/chemistry/fluid/

### Python Thermodynamic Libraries

```python
# thermo — equations of state, UNIFAC activity coefficients
pip install thermo fluids

# iapws — water and steam properties (free)
pip install iapws

# pyXSteam — steam tables
pip install pyXSteam
```

### CoolProp Vapor-Compression Cycle Analysis Example

```python
from CoolProp.CoolProp import PropsSI
import numpy as np
import matplotlib.pyplot as plt

def vapor_compression_cycle(fluid, T_evap, T_cond, superheat=5, subcooling=3):
    """
    Simple vapor-compression cycle analysis.
    T_evap, T_cond: evaporating/condensing temps in °C
    superheat/subcooling: K of superheat/subcooling
    """
    T_evap_K = T_evap + 273.15
    T_cond_K = T_cond + 273.15

    # State 1: Evaporator outlet (suction) — slightly superheated
    T1 = T_evap_K + superheat
    P_low = PropsSI('P', 'T', T_evap_K, 'Q', 1, fluid)
    h1 = PropsSI('H', 'T', T1, 'P', P_low, fluid)
    s1 = PropsSI('S', 'T', T1, 'P', P_low, fluid)

    # State 2: Compressor outlet — isentropic compression
    P_high = PropsSI('P', 'T', T_cond_K, 'Q', 1, fluid)
    h2s = PropsSI('H', 'P', P_high, 'S', s1, fluid)  # isentropic
    h2 = h1 + (h2s - h1) / 0.75  # assume 75% isentropic efficiency

    # State 3: Condenser outlet — slightly subcooled
    T3 = T_cond_K - subcooling
    h3 = PropsSI('H', 'T', T3, 'P', P_high, fluid)

    # State 4: Evaporator inlet — isenthalpic expansion
    h4 = h3

    # Performance
    q_evap = h1 - h4     # heat absorbed in evaporator (J/kg)
    w_comp = h2 - h1     # compressor work (J/kg)
    q_cond = h2 - h3     # heat rejected in condenser (J/kg)
    COP = q_evap / w_comp

    print(f"Fluid: {fluid}")
    print(f"Evaporating: {T_evap}°C at {P_low/1e5:.2f} bar")
    print(f"Condensing: {T_cond}°C at {P_high/1e5:.2f} bar")
    print(f"q_evap = {q_evap/1000:.1f} kJ/kg")
    print(f"w_comp = {w_comp/1000:.1f} kJ/kg")
    print(f"COP = {COP:.2f}")
    print(f"Carnot COP = {T_evap_K / (T_cond_K - T_evap_K):.2f}")
    return COP

# Example: R-290 propane system
vapor_compression_cycle('R290', T_evap=0, T_cond=40)
```

### P-h Diagram Plotter

```python
from CoolProp.Plots import PropertyPlot
import matplotlib.pyplot as plt

plot = PropertyPlot('R290', 'PH', unit_system='SI')
plot.calc_isolines()
plot.show()
```

### Hand Calculation Methods

**LMTD for heat exchanger sizing:**
$$\text{LMTD} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)}$$
$$Q = U \cdot A \cdot \text{LMTD}$$

Typical U values: condensers 200–400 W/m²K (forced air), 700–1500 W/m²K (water cooled); evaporators 150–300 W/m²K (forced air).

**NTU-effectiveness method (preferred for compact HX):**
$$\varepsilon = \frac{Q}{Q_{max}} = f(NTU, C_{min}/C_{max})$$
$$NTU = \frac{U \cdot A}{C_{min}}$$

### Simulation Software

| Tool | Cost | Best For |
|---|---|---|
| **CoolProp** | Free | Refrigerant properties, Python integration |
| **NIST WebBook** | Free | Quick property lookups, online |
| **EES** (Engineering Equation Solver) | ~$700 academic | Cycle analysis, parametric studies |
| **Aspen HYSYS / Plus** | Commercial | Process simulation, chemical plants |
| **TRNSYS** | Commercial | Transient solar thermal + adsorption systems |
| **EnergyPlus** | Free (DOE) | Building energy simulation |
| **OpenModelica + ThermoSysPro** | Free | Complex cycles, Modelica language |
| **REFPROP** | ~$300 personal | Gold standard fluid properties |

### Key Textbooks

1. **Stoecker, W.F.** — *Industrial Refrigeration Handbook* (McGraw-Hill, 1998) — best practical reference
2. **Herold, K.E., Radermacher, R., Klein, S.A.** — *Absorption Chillers and Heat Pumps* (CRC, 2016)
3. **Dossat, R.J. & Horan, T.J.** — *Principles of Refrigeration* — excellent introductory text
4. **Goldsmid, H.J.** — *Introduction to Thermoelectricity* (Springer, 2016)
5. **Incropera, F.P.** — *Fundamentals of Heat and Mass Transfer* — heat exchanger analysis
6. **ASHRAE Fundamentals Handbook** — authoritative reference for calculations and standards

---

## Section 8: Regulatory and Safety Considerations

### United States (EPA)

- **EPA Section 608** certification required to purchase regulated refrigerants (HFCs/HCFCs) in quantities >2 lb
- **Natural refrigerants** (R-290 propane, R-600a isobutane, R-744 CO₂, R-717 ammonia) have fewer purchase restrictions
- Propane and isobutane: purchase freely as camping/cooking gas; may have charge limitations for appliances

### Europe (F-Gas Regulation)

- EU Regulation 517/2014: phase-down of high-GWP HFCs
- Natural refrigerants (CO₂, HC, NH₃) are unregulated under F-Gas
- EU phase-down schedule: HFCs >2500 GWP banned in most new equipment; R-404A phase-out complete by 2025

### Ammonia Safety

- IDLH (Immediately Dangerous to Life and Health): 300 ppm
- ERPG-3 (life-threatening, 1 hour): 700 ppm
- TLV-TWA: 25 ppm (ACGIH)
- Lighter than air — accumulates near ceiling
- **Industrial ammonia systems:** Must follow ASHRAE 15, IIAR standards; OSHA PSM if >10,000 lb NH₃

### Material Compatibility

| Refrigerant | Incompatible Materials | Required Materials |
|---|---|---|
| NH₃ | Copper, brass, zinc, aluminum alloys | Steel, stainless steel, cast iron |
| CO₂ | — | High-pressure rated (>130 bar); carbon steel or stainless |
| HFCs (R-134a, R-410A) | Natural rubber | POE or PAG oil; compatible metals |
| LiBr solution | Carbon steel, copper, aluminum | 316L/304 stainless steel |

---

## Quick Reference: Materials Synthesis Summary

| Material | Purpose | Key Synthesis Route |
|---|---|---|
| Ammonia (NH₃) | Refrigerant (R-717), absorption working fluid | Haber-Bosch: N₂ + 3H₂ → 2NH₃, Fe catalyst, 400–500°C, 150–300 atm; or purchase 26% aqueous |
| Lithium bromide (LiBr) | LiBr-H₂O absorption absorbent | LiOH + HBr → LiBr + H₂O; or Li₂CO₃ + 2HBr → 2LiBr + H₂O + CO₂ |
| Bi₂Te₃ | Thermoelectric (Peltier) semiconductor | Bridgman melt synthesis from Bi + Te metal; or ball mill + SPS |
| Zeolite 13X | Adsorption refrigeration sorbent | Hydrothermal: NaAlO₂ + Na₂SiO₃ + NaOH, 80–100°C, 24 hours |
| Silica gel | Adsorption sorbent | Acidify sodium silicate → gel → wash → dry at 150–180°C |
| Activated carbon | Adsorption sorbent | Pyrolyze coconut shells/coal at 800–900°C; activate with CO₂/steam |
| CO₂ (R-744) | Refrigerant | Capture from fermentation; purchase as food-grade CO₂ cylinder |
| Propane/isobutane | Natural hydrocarbon refrigerant | Purchase commercially; isobutane from n-butane isomerization (AlCl₃ cat.) |

---

## Comparison Table: All Technologies

| Technology | Energy In | Temp Range | COP | Moving Parts | Refrigerant | DIY Difficulty |
|---|---|---|---|---|---|---|
| Vapor-compression | Electricity | −60 to +15°C | 2–5 | Compressor | R-290, NH₃, CO₂, etc. | Moderate |
| Thermoelectric (Peltier) | Electricity | −105 to −5°C | 0.3–0.8 | None | None | Easy |
| Stirling/GM cryocooler | Electricity | 4 K to −150°C | 0.1–0.5 | Pistons/displacers | He gas | Hard |
| Pulse tube | Electricity | 4 K to −150°C | 0.1–0.4 | None (warm end only) | He gas | Very Hard |
| Absorption (NH₃-H₂O) | Heat (burner) | −60 to +10°C | 0.45–0.65 | Small pump only | NH₃/H₂O | Moderate-Hard |
| Absorption (LiBr-H₂O) | Heat (burner) | +5 to +15°C | 0.65–1.4 | Small pump only | H₂O/LiBr | Hard |
| Einstein refrigerator | Heat (burner) | +5 to +15°C | 0.1–0.2 | **None** | NH₃/butane/H₂O | Hard |
| Adsorption | Heat (solar/waste) | −30 to +15°C | 0.3–0.6 | None | H₂O/methanol/NH₃ | Moderate |
| Vortex tube | Compressed air | 20–50°C below inlet | 0.1–0.5 | None | Air | Easy |
| Magnetocaloric | Electricity (magnets) | Near room temp | ~1.0 | Rotating/oscillating | None | Very Hard |
| Thermoacoustic | Electricity (speaker) | −100 to room temp | 0.1–0.4 | Speaker driver only | He | Hard |
| Evaporative | Water (passive/fan) | Down to wet-bulb | N/A | Fan (optional) | Water | Trivial |
| Radiative sky cooling | None (passive) | 5–15°C below ambient | N/A | None | None | Easy |
| JT expansion | Pressure (gas cylinder) | −150 to −10°C | N/A | None | N₂, He, Ar | Moderate |
| Chemical (endothermic) | Chemical energy | −20 to +5°C | N/A | None | NH₄NO₃, etc. | Trivial |
