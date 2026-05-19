# Stirling Cycle Refrigeration & Simulation Tools

*Research compiled: May 18, 2026*

---

## Table of Contents

1. [Reversed Stirling Cycle — Fundamentals](#1-reversed-stirling-cycle--fundamentals)
2. [Machine Configurations](#2-machine-configurations)
3. [Working Gases](#3-working-gases)
4. [The Regenerator](#4-the-regenerator)
5. [Schmidt Analysis — Ideal Cycle Calculation](#5-schmidt-analysis--ideal-cycle-calculation)
6. [Pulse Tube Refrigerators](#6-pulse-tube-refrigerators)
7. [Gifford-McMahon (GM) Coolers](#7-gifford-mcmahon-gm-coolers)
8. [Joule-Thomson (JT) Coolers & Ultra-Cold Stages](#8-joule-thomson-jt-coolers--ultra-cold-stages)
9. [Temperature Ranges by Technology](#9-temperature-ranges-by-technology)
10. [DIY Stirling Cooler — Practical Considerations](#10-diy-stirling-cooler--practical-considerations)
11. [Free-Piston Linear Stirling Coolers](#11-free-piston-linear-stirling-coolers)
12. [Drive Methods & Power Input](#12-drive-methods--power-input)
13. [COP Calculation](#13-cop-calculation)
14. [Calculation & Simulation Tools](#14-calculation--simulation-tools)
15. [Key Textbooks & References](#15-key-textbooks--references)

---

## 1. Reversed Stirling Cycle — Fundamentals

The **reversed Stirling cycle** uses mechanical work input to pump heat from a cold reservoir to a hot reservoir — the refrigeration direction. The four ideal processes:

| Process | Description |
|---------|-------------|
| **1 → 2** Isothermal compression | Hot-end piston compresses gas at $T_H$; heat $Q_H$ rejected to hot sink |
| **2 → 3** Constant-volume cooling (regeneration) | Gas displaced through regenerator; heat stored; temperature drops from $T_H$ to $T_C$ |
| **3 → 4** Isothermal expansion | Cold-end piston expands gas at $T_C$; heat $Q_C$ absorbed from cold load |
| **4 → 1** Constant-volume heating (regeneration) | Gas displaced back through regenerator; stored heat returned; temperature rises from $T_C$ to $T_H$ |

**Key physical intuition:** The regenerator makes the constant-volume processes internally reversible. Without a perfect regenerator, the cycle degrades toward a simple (less efficient) gas cycle. With a perfect regenerator, the **ideal reversed Stirling COP equals the Carnot COP**.

```
P
^
|  1----2
|  |    |
|  |    |  ← isotherms (hyperbolas on P-V)
|  4----3
+----------> V
```

*P-V diagram schematic — actual shape is isothermal curves at T_H (top) and T_C (bottom) connected by isochores.*

---

## 2. Machine Configurations

### Alpha Configuration (Two-Piston)
- Two pistons in **separate cylinders** connected by a duct containing the regenerator
- Hot piston and cold piston operate with a **phase angle** (typically ~90°)
- Simplest to analyze; each cylinder is dedicated to one temperature end
- Drawback: both pistons require sliding seals at their respective temperatures

```
[Hot Cylinder] ←→ [Regenerator + Heat Exchangers] ←→ [Cold Cylinder]
     Hot Piston ↕                                          Cold Piston ↕
```

### Beta Configuration (One Piston + Displacer)
- **Single cylinder** containing both a power piston and a displacer (not a sealed piston — it shuttles gas)
- Displacer moves gas between hot and cold ends; power piston changes total volume
- Mechanical advantage: only one seal (on power piston) at near-ambient temperature
- Most common for small Stirling engines/coolers
- Displacer runs approximately **90° ahead** of the power piston

### Gamma Configuration (Separate Expansion Cylinder)
- Displacer in one cylinder, power piston in a **separate cylinder**
- Mechanically simpler linkage than Beta; gas communicates between cylinders
- Cold space is the displacer cylinder (cold end); warm space includes the power cylinder
- Used in some air liquefiers and larger commercial units

### Configuration Comparison

| Feature | Alpha | Beta | Gamma |
|---------|-------|------|-------|
| Cylinders | 2 | 1 | 2 |
| Seals at cold end | Yes | No | No |
| Mechanical complexity | Medium | High | Low |
| Typical use | Lab coolers | Small coolers, engines | Larger industrial |

---

## 3. Working Gases

The choice of working gas significantly impacts performance. Key properties at 300 K, 1 atm:

| Gas | $k$ (W/m·K) | $c_p$ (J/kg·K) | $\mu$ (µPa·s) | $\gamma$ | Notes |
|-----|------------|----------------|---------------|----------|-------|
| **Helium (He)** | 0.152 | 5193 | 20.0 | 1.667 | **Best** — highest $k$, lowest mol. wt., inert |
| **Hydrogen (H₂)** | 0.182 | 14300 | 9.0 | 1.407 | Highest $k$ by mass; flammable; para-H₂ issues |
| **Nitrogen (N₂)** | 0.026 | 1040 | 17.8 | 1.400 | Safe, cheap; poor thermal conductivity |
| **Air** | 0.026 | 1005 | 18.5 | 1.400 | Convenient but moisture/O₂ issues at low T |

**Why Helium dominates cryogenic Stirling/pulse tube:**

1. **Thermal conductivity** — 6× higher than N₂; faster heat exchange in regenerator
2. **Low boiling point** (4.2 K) — stays gaseous all the way to near absolute zero
3. **No liquefaction risk** in cold end at typical operating temperatures
4. **Monatomic** — $\gamma = 5/3$; no vibrational energy modes that complicate analysis
5. **Chemically inert** — no reaction with regenerator materials or seals

**Hydrogen note:** Marginally better thermal conductivity than He by some metrics at room temperature, but the para-H₂/ortho-H₂ conversion releases heat at ~20 K, complicating cryo operation. Flammability is a major practical barrier.

---

## 4. The Regenerator

The regenerator is the **defining component** of the Stirling cycle. It is a porous thermal mass (high heat capacity, low flow resistance) through which the working gas oscillates.

### Function

- During gas flow hot-to-cold: gas deposits heat into matrix → gas cools
- During gas flow cold-to-hot: gas absorbs heat from matrix → gas warms
- Net effect: internal heat exchange that substitutes for two external heat rejection/absorption events per half-cycle

### Regenerator Effectiveness

$$\eta_{reg} = \frac{Q_{actual}}{Q_{ideal}} = \frac{T_{H,in} - T_{H,out}}{T_{H,in} - T_{C,in}}$$

A perfect regenerator has $\eta_{reg} = 1$. Real regenerators achieve **0.95 – 0.999** in well-designed cryocoolers.

### Impact on COP

With regenerator ineffectiveness $\epsilon = 1 - \eta_{reg}$, the additional heat load per cycle is:

$$\Delta Q_{loss} = \dot{m} c_p (T_H - T_C) \cdot \epsilon$$

This directly reduces net cooling capacity.

### Matrix Materials & Geometries

| Material | Temperature Range | Notes |
|----------|------------------|-------|
| **Stainless steel wire mesh** | 77 K – 300 K | Cheap, easy to pack; good from room temp to LN₂ range |
| **Stainless steel sintered spheres** | 77 K – 300 K | More uniform porosity; lower flow resistance |
| **Lead spheres** | 10 K – 77 K | High heat capacity at 20-77 K; toxic; still used in GM coolers |
| **Er₃Ni (Erbium-Nickel)** | 4 K – 20 K | Magnetic specific heat peak near 4 K; essential for 4 K stages |
| **HoCu₂, GdRh** | 1 K – 10 K | Rare-earth intermetallics; used in multi-stage sub-4K coolers |

### Design Parameters

- **Porosity** $\phi$: typically 0.6 – 0.8 for wire mesh; affects void volume and pressure drop
- **Hydraulic diameter** $d_h$: smaller → better heat transfer, higher pressure drop; typical 50–200 µm wire diameter
- **NTU** (Number of Transfer Units): $NTU = \frac{h A_s}{\dot{m} c_p}$ — higher NTU → higher effectiveness
- **Heat capacity ratio**: matrix heat capacity must greatly exceed gas heat capacity per cycle; $C_{matrix}/C_{gas} > 50$ is typical target

---

## 5. Schmidt Analysis — Ideal Cycle Calculation

The **Schmidt analysis** (1871) is the classical closed-form solution for the Stirling cycle assuming:
- Isothermal hot and cold spaces
- Sinusoidal piston motions
- Perfect regenerator
- Ideal gas, no losses

### Geometry Definitions (Alpha configuration)

- $V_{sw,H}$: hot piston swept volume
- $V_{sw,C}$: cold piston swept volume  
- $V_{dH}$: hot dead volume (heat exchanger, regenerator hot side)
- $V_{dC}$: cold dead volume (heat exchanger, regenerator cold side)
- $\alpha$: phase angle of cold piston leading hot piston
- $T_H$, $T_C$: absolute temperatures of hot and cold spaces

### Volume Expressions

$$V_H(\theta) = \frac{V_{sw,H}}{2}(1 - \cos\theta) + V_{dH}$$

$$V_C(\theta) = \frac{V_{sw,C}}{2}(1 - \cos(\theta - \alpha)) + V_{dC}$$

### Total Reduced Volume

Define temperature ratio $\tau = T_C / T_H$ and normalize volumes by $V_{sw,H}$:

$$v_H = V_H / V_{sw,H}, \quad v_C = V_C / V_{sw,H}, \quad v_R = V_R / V_{sw,H}$$

The total reduced volume (accounting for the regenerator at mean temperature $T_m = (T_H + T_C)/2$):

$$V_{total,reduced}(\theta) = v_H + \frac{v_R}{\tau_m} + \frac{v_C}{\tau}$$

where $\tau_m = T_m / T_H = (1 + \tau)/2$.

### Mean Pressure and Pressure Variation

The mean charge pressure:

$$P_{mean} = \frac{m_{total} R}{V_{total,mean}}$$

The instantaneous pressure (ideal gas, perfect regenerator):

$$P(\theta) = \frac{P_{mean} \cdot c}{1 - b\cos(\theta - \phi_{P})}$$

where $b$ and $\phi_P$ are constants derived from the geometry:

$$B = \sqrt{(\kappa \sin\alpha)^2 + (\tau + \kappa \cos\alpha)^2}$$

$$b = B / (S + 1), \quad \kappa = V_{sw,C}/V_{sw,H}$$

$$S = \frac{1}{2}(1 + \tau) \cdot \frac{V_{dR}}{V_{sw,H}} + \frac{V_{dH}}{V_{sw,H}} + \frac{\tau \cdot V_{dC}}{V_{sw,H}} + \frac{1 + \kappa}{2}(1 + \tau)/2$$

### Cooling Power (Cold Space Work)

$$Q_C = \pi P_{mean} V_{sw,C} \frac{b \sin\alpha}{1+b} \cdot \frac{\tau}{?}$$

For the full Schmidt formula (cold work per cycle):

$$W_C = \frac{\pi P_{mean} \kappa \sin\alpha}{\sqrt{1 - b^2}} \cdot V_{sw,H}$$

$$Q_{cold,cycle} = W_C \cdot \tau / (1 - \tau) \quad \text{(for ideal regenerator)}$$

**Reference implementation** (Walker, "Stirling Engines", 1980): the complete Schmidt equations are transcendental but have a closed analytical form. Numerical integration of $\oint P \, dV$ is often more practical.

### Phase Angle Optimization

For equal swept volumes ($\kappa = 1$), maximum cooling power occurs near $\alpha \approx 90°$. For unequal volumes or high dead volumes, the optimum shifts. A sweep over $\alpha$ from 60° to 120° with numerical P-V integration is recommended for actual design.

---

## 6. Pulse Tube Refrigerators

### Operating Principle

Pulse tube refrigerators (PTRs) eliminate **all moving parts at the cold end**, replacing the cold displacer with a gas column (the "pulse tube") and a phase-shifting network at the warm end.

**Thermoacoustic explanation:** An oscillating pressure wave in a tube, combined with an oscillating displacement velocity, creates net enthalpy flow (acoustic streaming of energy). With proper phasing:

- Gas parcels near the cold heat exchanger: expand (cool) → absorb heat from load
- Gas parcels near the warm heat exchanger: compress (warm) → reject heat to sink
- The gas column itself acts as a "thermal buffer" — parcels shuttle without net mass flow

### PTR Types

| Type | Phase Shifter | Notes |
|------|--------------|-------|
| **Basic (BPTR)** | None | Poor phase control; low performance |
| **Orifice (OPTR)** | Orifice + buffer volume | Standard design; good performance |
| **Double-inlet (DIPTR)** | Orifice + bypass valve | Better phase; common in 4 K coolers |
| **Inertance tube** | Long narrow tube replaces orifice | Inductive impedance; best acoustic phase |

### Achieving 4 K

Single-stage PTR reaches ~30–40 K. To reach 4 K:

1. **Two-stage** PTR: first stage at ~70 K, second stage at ~4 K; He-4 working gas
2. **Three-stage** for sub-2K (rare)
3. Key material: **Er₃Ni regenerator fill** in cold stage (magnetic heat capacity peak near 4.2 K)
4. Operating frequency: typically 1–2 Hz (lower frequency → more displacement volume per cycle → more cooling power, but larger compressor)
5. Pulse tube diameter and length set acoustic impedance — tune for $\phi_{phaseangle} \approx 30°$ between pressure and velocity

### Commercial 4 K PTR Performance (representative)

| Manufacturer | Model | Cooling at 4.2 K | First Stage | Input Power |
|---|---|---|---|---|
| Sumitomo | RP-082B | 1.0 W | 40 W @ 45 K | ~6 kW |
| Cryomech | PT415 | 1.5 W | 40 W @ 45 K | ~6 kW |
| Oxford/ICE | Cryodrive | 1.5 W | 45 W @ 50 K | ~5 kW |

### Advantages over GM Coolers

- No cold-end moving parts → no vibration, no wear, effectively infinite lifespan
- Critical for precision instruments (electron microscopes, STM, SQUID sensors)
- Vibration levels: PTR ~1 µm amplitude vs. GM ~5–20 µm

---

## 7. Gifford-McMahon (GM) Coolers

### Mechanism

GM coolers use **valve-actuated pressure switching** instead of a crankshaft-driven piston. The compressor runs continuously at nearly constant pressure; rotary valves switch the cold head between high and low pressure lines.

```
Compressor (HP/LP lines) ──→ Rotary Valve ──→ Displacer Cold Head
                                                     ↓
                                              Regenerator
                                                     ↓
                                              Cold Heat Exchanger
```

**Cycle steps:**
1. High-pressure gas admitted to cold head → gas flows through regenerator, cooling as it goes
2. Displacer pushes gas to cold space
3. Low-pressure line opened → gas expands in cold space → absorbs heat from load
4. Displacer returns, gas flows back through regenerator (regenerator re-cools for next cycle)
5. Low-pressure gas returned to compressor

### Key Differences from Stirling

| Feature | Stirling | GM |
|---------|---------|-----|
| Pressure control | Piston-driven (mechanical) | Valve-switched (pneumatic) |
| Compressor integration | Integral | Separate (flex-line connected) |
| Operating frequency | 25–60 Hz | 1–2 Hz |
| Vibration | Moderate | High (but flex-line isolates cold head) |
| Cold-head placement | Near compressor | Remote, flexible |
| Typical lowest T | 30–40 K (single) | 8–10 K (single), ~4 K (two-stage) |

### Applications

- **MRI machines**: two-stage GM coolers (10 K first stage, ~4 K second stage) re-condense helium boiloff in superconducting magnets → "zero-boiloff" systems
- **Semiconductor fabs**: cryopumps for vacuum chambers (pumps by cryocondensation at ~10 K)
- **NMR spectrometers**: magnet cooling
- **Infrared detector arrays**: imaging sensors in astronomy

### Two-Stage GM to 4 K

- First stage: ~30–50 K (provides pre-cooling and intercepts radiation load)
- Second stage regenerator: **lead spheres** (10–50 K) + **Er₃Ni** (4–20 K)
- Achieves 1–2 W of cooling at 4.2 K
- Requires ~5–7 kW electrical input

---

## 8. Joule-Thomson (JT) Coolers & Ultra-Cold Stages

### JT Principle

Isenthalpic throttling ($h_1 = h_2$) of a real gas through a restriction (needle valve or orifice) produces cooling when the gas is below its **inversion temperature**:

$$\mu_{JT} = \left(\frac{\partial T}{\partial P}\right)_h = \frac{T(\partial v/\partial T)_P - v}{c_p}$$

Positive $\mu_{JT}$ (cooling on expansion) requires $T < T_{inv}$.

| Gas | $T_{inv}$ (K) | Boiling point (K) |
|-----|--------------|-----------------|
| He-4 | 43 | 4.2 |
| H₂ | 202 | 20.3 |
| N₂ | 621 | 77.3 |
| Air | ~650 | ~81 |

**Helium must be pre-cooled below 43 K before JT expansion can liquefy it.** This is why multi-stage systems are required.

### Linde-Hampson + Pre-Cooling Architecture

```
Room Temperature
    │
    ▼
[LN₂ pre-cool, 77 K]   ← cheapest first stage
    │
    ▼
[LHe pre-cool, 4.2 K]  ← or GM/Stirling cooler to 10-40 K
    │
    ▼
[JT expansion valve]   ← drops to 1–2 K with He-3 or He-4
    │
    ▼
[Sub-kelvin stage: dilution refrigerator or adiabatic demagnetization]
```

### He-3 JT for 300 mK

- He-3 (lighter isotope) boils at 3.19 K at 1 atm, but can be pumped to ~0.3 K
- Single-shot or continuous He-3 sorption coolers reach ~250–350 mK
- Requires 4 K base temperature (from PTR or GM)

### Dilution Refrigerator (mK Range)

- Exploits quantum mixing of He-3 and He-4 phases at low temperature
- At $T < 870$ mK, He-3/He-4 mixture separates into concentrated (He-3-rich) and dilute phases
- He-3 crosses the phase boundary → absorbs heat (endothermic mixing)
- Continuous operation possible; achieves **5–20 mK** routinely; record ~2 mK
- Modern "dry" dilution fridges use PTR pre-cooling (no liquid cryogens needed)

---

## 9. Temperature Ranges by Technology

```
300 K ─────────────────────────────────────────── Room temperature
  │
 77 K ─────────────────────────── LN₂ temperature
  │       ↑ Stirling/GM single stage can reach here easily
  │
 40 K ──────────────────────────────────────────── Single-stage Stirling limit
 30 K ──────────────────────────────────────────── Single-stage GM limit
  │
 10 K ──────────────────────────────────────────── Two-stage GM/Stirling
  │
 4.2 K ─────────────────────────────────────────── LHe temperature
        ↑ Two-stage PTR or GM with Er₃Ni regenerator
  │
 1.5 K ─────────────────────────────────────────── Pumped He-4
  │
 0.3 K ─────────────────────────────────────────── He-3 sorption
  │
0.015 K ────────────────────────────────────────── Dilution refrigerator
  │
1 mK ───────────────────────────────────────────── Nuclear adiabatic demagnetization
```

---

## 10. DIY Stirling Cooler — Practical Considerations

### Machining Requirements

Building a functional Stirling cooler (targeting 200–250 K, i.e., -20 to -50°C range) requires:

**Tolerances:**
- Piston-to-cylinder clearance: **5–15 µm** for gas-bearing (non-contacting) operation; 10–25 µm if using piston rings
- Displacer clearance: 50–150 µm acceptable (displacer is not a seal, just a shuttle)
- Surface finish: Ra < 0.4 µm (16 µin) on cylinder bore; honing required

**Recommended materials:**
- **Cylinder:** Hard anodized 6061-T6 aluminum or stainless steel 316
- **Piston:** PEEK or filled PTFE for dry-running; hardened SS for gas-bearing designs
- **Displacer:** Fiberglass/G-10 (low thermal conductivity — reduces conduction loss)
- **Cold heat exchanger:** Copper or aluminum with fins

### Sealing Challenges

The biggest DIY obstacle is sealing at both pressure and low temperature:

| Seal type | Pros | Cons |
|-----------|------|------|
| **O-rings (Buna-N/Viton)** | Easy, cheap | Friction adds heat; limited to ~-40°C |
| **PTFE lip seals** | Low friction, wider temp range | More complex machining |
- **Gas bearing (clearance seal)** | No friction; used in space hardware | Requires < 10 µm clearance; hard to machine |
| **Rotary shaft seal + crankshaft** | Simple | Leakage over time |

**Practical DIY approach:** use a **rhombic drive** mechanism with a rotary shaft seal at room temperature (not at the cold end). Accept some gas leakage; pressurize with N₂ or He as needed.

### Regenerator Materials (DIY)

- **Stainless steel wool** (grade 0000, ~25 µm wire diameter): accessible at hardware stores; pack to ~85% solid fraction; useful to ~-100°C
- **Copper mesh** (100-mesh screen, stacked discs): better thermal conductivity but higher axial conduction loss — actually a disadvantage
- **Stainless mesh screens** (200-mesh, 50 µm): cut to cylinder diameter and stacked; reproducible porosity; recommended

**Regenerator sizing rule of thumb:**
- Length/diameter ratio: 3:1 to 8:1
- Void fraction: 0.6–0.75
- Wire diameter: ~50–150 µm for room temperature Stirling

### Expected Performance (DIY Alpha, 200–300 K range)

- Sweep volume: 10–50 cm³ each end
- Operating pressure: 5–15 bar mean (higher → more power, better heat transfer)
- Phase angle: 90°
- Speed: 300–900 RPM (5–15 Hz)
- Cooling power: 5–50 W (rough estimate; highly dependent on regenerator quality)
- Lowest temperature: **-50 to -100°C** is achievable with careful construction

---

## 11. Free-Piston Linear Stirling Coolers

### Operating Principle

Free-piston Stirling coolers (FPSCs) have **no crankshaft or mechanical linkage**. The piston and displacer are coupled dynamically through:
- Gas spring (compression space acts as spring)
- Mechanical spring (flexure or coil)
- Electromagnetic coupling (linear alternator/motor)

The system oscillates at its **natural resonant frequency**, typically 30–80 Hz.

```
[Linear Motor Coil] ──→ [Piston] ──→ [Gas Spring + Regenerator] ──→ [Displacer] ──→ [Cold End]
     permanent magnet                                                flexure spring
```

### Magnetic Coupling & Sealing

- **Moving-magnet linear motor**: magnet assembly attached to piston; coil is stationary (outside pressure vessel) → **hermetically sealed** — no shaft seal
- Piston supported on **gas bearing** or **flexure bearing** (thin metal diaphragm spring)
- No lubrication required; no wear mechanism → **100,000+ hour lifetime**

### Space Applications

FPSCs dominate space cooling because:
1. **No wear** → no maintenance; critical for 10–15 year missions
2. **No vibration exported** if opposing piston design (dual-opposed) is used
3. Radiation-tolerant (no electronics at cold end)
4. **Examples:**
   - NICMOS cooler on Hubble Space Telescope (Ball Aerospace FPSC, ~60 K)
   - James Webb Space Telescope MIRI instrument cooler (~6 K, using PTR architecture)
   - Earth observation satellite IR detector cooling (RICOR, Sunpower, etc.)

### Performance Characteristics

| Parameter | Typical Range |
|-----------|--------------|
| Cold end temperature | 40–150 K |
| Cooling power | 0.1–10 W |
| Input power | 10–150 W |
| Specific power | 5–20 W input / W cooling |
| Frequency | 30–80 Hz |
| Mass | 0.1–2 kg |

**Commercial suppliers:** Sunpower (now part of Beale International), RICOR, Thales Cryogenics, Infratec

---

## 12. Drive Methods & Power Input

### Electric Motor Drive

Most common. Rotary motor + crank/scotch-yoke converts rotation to linear reciprocation.

$$P_{shaft} = T_{mean} \cdot \omega$$

For a Stirling cooler: $P_{input} = P_{pdV,hot} + P_{friction} + P_{regenerator loss} + P_{HX loss}$

Typical electrical-to-cooling efficiency (actual/Carnot):
- Practical Stirling cooler: 15–30% of Carnot COP
- State-of-the-art (commercial cryocooler): 20–40% of Carnot

### Heat Engine Drive (Compound Stirling)

A Stirling **engine** on the hot side drives a Stirling **cooler** on the cold side. Useful when:
- Waste heat is available (industrial processes)
- Solar thermal is the energy source
- Grid power is unavailable

```
[Heat Source, T_hot] → [Stirling Engine] → [Mechanical shaft] → [Stirling Cooler] → [Cold Load, T_cold]
                              ↓
                    [Heat rejection, T_ambient]
```

Overall COP (heat engine × refrigerator):

$$COP_{compound} = \eta_{engine} \cdot COP_{cooler}$$

$$COP_{compound,Carnot} = \frac{T_{ambient} - T_{cold,engine}}{T_{hot}} \cdot \frac{T_{cold}}{T_{ambient} - T_{cold}}$$

---

## 13. COP Calculation

### Ideal (Carnot) COP

$$COP_{Carnot} = \frac{Q_{cold}}{W_{net}} = \frac{T_C}{T_H - T_C}$$

This is the maximum possible COP for any refrigerator operating between $T_C$ and $T_H$.

### Actual COP with Efficiency Factor

$$COP_{actual} = COP_{Carnot} \cdot \eta_{fraction}$$

$$\boxed{COP = \frac{Q_{cold}}{W_{input}} = \frac{T_C}{T_H - T_C} \cdot \eta_{fraction}}$$

Where $\eta_{fraction}$ accounts for all real losses: regenerator ineffectiveness, pressure drops, seal friction, heat exchanger $\Delta T$, etc.

### COP Examples

| Application | $T_C$ (K) | $T_H$ (K) | $COP_{Carnot}$ | $\eta_{fraction}$ | $COP_{actual}$ |
|---|---|---|---|---|---|
| Food refrigerator | 255 | 308 | 4.8 | 0.35 | 1.7 |
| LN₂ production (77 K) | 77 | 300 | 0.345 | 0.20 | 0.069 |
| GM cooler (4 K) | 4 | 300 | 0.0135 | 0.10 | 0.00135 |
| Dilution refrigerator (15 mK) | 0.015 | 300 | $5 \times 10^{-5}$ | 0.001 | $5 \times 10^{-8}$ |

### Heat Rejection

$$Q_H = Q_C + W_{input}$$

By energy balance, heat rejected to hot sink always exceeds cooling power by the work input.

### Specific Work (Inverse of COP)

Sometimes reported as **specific power** = W/W_cooling:

$$SP = \frac{1}{COP} = \frac{T_H - T_C}{T_C} \cdot \frac{1}{\eta_{fraction}}$$

---

## 14. Calculation & Simulation Tools

### CoolProp (Open Source — Recommended Starting Point)

**Installation:**
```bash
pip install CoolProp
```

**Basic usage:**
```python
from CoolProp.CoolProp import PropsSI

# Get enthalpy of R134a at 300 K, 101325 Pa
h = PropsSI('H', 'T', 300, 'P', 101325, 'R134a')
print(f"Enthalpy: {h:.1f} J/kg")

# Get all properties at a state point
T = 250  # K
P = 500000  # Pa (5 bar)
fluid = 'Helium'

rho  = PropsSI('D', 'T', T, 'P', P, fluid)   # density kg/m³
s    = PropsSI('S', 'T', T, 'P', P, fluid)   # entropy J/kg/K
cp   = PropsSI('CPMASS', 'T', T, 'P', P, fluid)  # cp J/kg/K
k    = PropsSI('CONDUCTIVITY', 'T', T, 'P', P, fluid)  # thermal conductivity W/m/K
mu   = PropsSI('VISCOSITY', 'T', T, 'P', P, fluid)  # dynamic viscosity Pa·s
```

**Vapor compression cycle analysis:**
```python
from CoolProp.CoolProp import PropsSI
import numpy as np

def vapor_compression_cycle(fluid, T_evap, T_cond, eta_comp=0.75):
    """
    Simple vapor compression cycle analysis.
    
    Parameters:
        fluid: CoolProp fluid name (e.g., 'R134a', 'R410A')
        T_evap: evaporating temperature [K]
        T_cond: condensing temperature [K]
        eta_comp: isentropic compressor efficiency
    
    Returns:
        dict with COP, specific work, specific cooling capacity
    """
    # State 1: Evaporator outlet (saturated vapor)
    P_evap = PropsSI('P', 'T', T_evap, 'Q', 1, fluid)
    h1 = PropsSI('H', 'T', T_evap, 'Q', 1, fluid)
    s1 = PropsSI('S', 'T', T_evap, 'Q', 1, fluid)
    
    # State 2s: Isentropic compressor outlet
    P_cond = PropsSI('P', 'T', T_cond, 'Q', 0, fluid)
    h2s = PropsSI('H', 'P', P_cond, 'S', s1, fluid)
    
    # State 2: Actual compressor outlet
    h2 = h1 + (h2s - h1) / eta_comp
    
    # State 3: Condenser outlet (saturated liquid)
    h3 = PropsSI('H', 'T', T_cond, 'Q', 0, fluid)
    
    # State 4: Expansion valve outlet (isenthalpic)
    h4 = h3  # isenthalpic expansion
    
    # Cycle performance
    q_cold = h1 - h4    # specific cooling [J/kg]
    w_comp = h2 - h1    # specific compressor work [J/kg]
    q_hot  = h2 - h3    # specific heat rejected [J/kg]
    COP    = q_cold / w_comp
    
    return {
        'COP': COP,
        'q_cold_kJ_kg': q_cold / 1000,
        'w_comp_kJ_kg': w_comp / 1000,
        'P_evap_bar': P_evap / 1e5,
        'P_cond_bar': P_cond / 1e5,
        'T_evap_K': T_evap,
        'T_cond_K': T_cond,
    }

# Example: R134a, -20°C evaporating, +40°C condensing
result = vapor_compression_cycle('R134a', T_evap=253.15, T_cond=313.15)
for k, v in result.items():
    print(f"  {k}: {v:.3f}")
```

**P-h diagram with cycle overlay:**
```python
import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI

def plot_ph_diagram(fluid, T_evap, T_cond, eta_comp=0.75):
    # Saturation curve
    T_crit = PropsSI('Tcrit', fluid)
    T_trip = PropsSI('Ttriple', fluid)
    T_range = np.linspace(T_trip + 1, T_crit - 0.1, 300)
    
    h_liq = [PropsSI('H','T',T,'Q',0,fluid)/1000 for T in T_range]
    h_vap = [PropsSI('H','T',T,'Q',1,fluid)/1000 for T in T_range]
    P_sat  = [PropsSI('P','T',T,'Q',0,fluid)/1e5  for T in T_range]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(h_liq, P_sat, 'b-', linewidth=2, label='Saturation curve')
    ax.semilogy(h_vap, P_sat, 'b-', linewidth=2)
    
    # Cycle states
    P_e = PropsSI('P','T',T_evap,'Q',1,fluid)
    P_c = PropsSI('P','T',T_cond,'Q',0,fluid)
    h1  = PropsSI('H','T',T_evap,'Q',1,fluid)/1000
    s1  = PropsSI('S','T',T_evap,'Q',1,fluid)
    h2s = PropsSI('H','P',P_c,'S',s1,fluid)/1000
    h2  = h1 + (h2s - h1)/eta_comp
    h3  = PropsSI('H','T',T_cond,'Q',0,fluid)/1000
    h4  = h3
    
    cycle_h = [h1, h2, h3, h4, h1]
    cycle_P = [P_e/1e5, P_c/1e5, P_c/1e5, P_e/1e5, P_e/1e5]
    
    ax.semilogy(cycle_h, cycle_P, 'r-o', linewidth=2, markersize=8, label='Cycle')
    for i, (h, p, label) in enumerate(zip(
        [h1,h2,h3,h4], [P_e/1e5, P_c/1e5, P_c/1e5, P_e/1e5],
        ['1 (evap. out)', '2 (comp. out)', '3 (cond. out)', '4 (exp. out)'])):
        ax.annotate(label, (h, p), textcoords="offset points", xytext=(5,5))
    
    ax.set_xlabel('Specific Enthalpy [kJ/kg]')
    ax.set_ylabel('Pressure [bar]')
    ax.set_title(f'P-h Diagram: {fluid}, T_evap={T_evap-273.15:.0f}°C, T_cond={T_cond-273.15:.0f}°C')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('ph_diagram.png', dpi=150)
    plt.show()

plot_ph_diagram('R134a', T_evap=253.15, T_cond=313.15)
```

**Supported fluids (selection):**

| Category | Fluids |
|----------|--------|
| Natural refrigerants | `Helium`, `Hydrogen`, `Nitrogen`, `Air`, `CO2`, `Ammonia`, `Propane` |
| HFC refrigerants | `R134a`, `R410A`, `R32`, `R125`, `R143a` |
| HFO refrigerants | `R1234yf`, `R1234ze(E)` |
| Cryogenic | `Neon`, `Argon`, `Krypton`, `Oxygen` |

**Documentation:** https://coolprop.org/coolprop/HighLevelAPI.html

---

### Schmidt Analysis — Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

def schmidt_analysis(
    V_sw_H,      # Hot swept volume [m³]
    V_sw_C,      # Cold swept volume [m³]
    V_d_H,       # Hot dead volume [m³]
    V_d_C,       # Cold dead volume [m³]
    V_d_R,       # Regenerator void volume [m³]
    T_H,         # Hot temperature [K]
    T_C,         # Cold temperature [K]
    P_mean,      # Mean charge pressure [Pa]
    alpha_deg,   # Phase angle, cold leads hot [degrees]
    n_points=360
):
    """Schmidt analysis for ideal alpha Stirling cooler."""
    alpha = np.radians(alpha_deg)
    tau = T_C / T_H
    T_R = (T_H + T_C) / 2   # Regenerator mean temperature
    kappa = V_sw_C / V_sw_H
    
    theta = np.linspace(0, 2*np.pi, n_points)
    
    # Volume variation
    V_H = V_d_H + V_sw_H/2 * (1 - np.cos(theta))
    V_C = V_d_C + V_sw_C/2 * (1 - np.cos(theta - alpha))
    
    # Reduced total volume (normalized by T_H)
    V_total_over_T = V_H/T_H + V_d_R/T_R + V_C/T_C
    
    # Ideal gas: P * (V/T_each) = const for each space
    # Total: P * sum(V_i/T_i) = m*R = const
    # So P(theta) = (m*R) / sum(V_i/T_i)
    # With m*R = P_mean * mean(sum(V_i/T_i))
    
    V_tot_T_mean = np.mean(V_total_over_T)
    mR = P_mean * V_tot_T_mean  # mass * specific gas constant [Pa·m³/K]
    
    P = mR / V_total_over_T
    
    # Work done on hot and cold spaces
    dV_H = np.gradient(V_H, theta)
    dV_C = np.gradient(V_C, theta)
    
    # Work per cycle (negative = work done by gas on piston)
    W_H = np.trapz(P * dV_H, theta)   # Work done on hot-space gas
    W_C = np.trapz(P * dV_C, theta)   # Work done on cold-space gas
    
    # Q_cold = work done BY cold gas = -W_C (sign convention)
    Q_cold_cycle = -W_C
    W_net_input  = -(W_H + W_C)  # Net work input per cycle
    
    COP = Q_cold_cycle / W_net_input if W_net_input > 0 else float('inf')
    COP_Carnot = T_C / (T_H - T_C)
    
    return {
        'theta': theta,
        'P': P,
        'V_H': V_H,
        'V_C': V_C,
        'P_min': P.min(),
        'P_max': P.max(),
        'P_ratio': P.max() / P.min(),
        'Q_cold_J': Q_cold_cycle,
        'W_input_J': W_net_input,
        'COP': COP,
        'COP_Carnot': COP_Carnot,
        'eta_fraction': COP / COP_Carnot,
    }

# Example: small Stirling cooler, 300K → 200K
result = schmidt_analysis(
    V_sw_H=20e-6,   # 20 cm³
    V_sw_C=20e-6,   # 20 cm³ (equal swept volumes)
    V_d_H=5e-6,     # 5 cm³ dead volume
    V_d_C=5e-6,
    V_d_R=8e-6,     # 8 cm³ regenerator void
    T_H=300,
    T_C=200,
    P_mean=10e5,    # 10 bar mean pressure
    alpha_deg=90
)
print(f"Cooling per cycle: {result['Q_cold_J']*1000:.2f} mJ")
print(f"Work input/cycle:  {result['W_input_J']*1000:.2f} mJ")
print(f"COP (ideal Schmidt): {result['COP']:.3f}")
print(f"COP Carnot:          {result['COP_Carnot']:.3f}")
print(f"η_fraction (Schmidt/Carnot): {result['eta_fraction']:.3f}")

# Phase angle sweep to find optimum
alphas = range(60, 121, 5)
cops   = []
qcolds = []
for a in alphas:
    r = schmidt_analysis(20e-6, 20e-6, 5e-6, 5e-6, 8e-6, 300, 200, 10e5, a)
    cops.append(r['COP'])
    qcolds.append(r['Q_cold_J'])

plt.figure(figsize=(10, 4))
plt.subplot(1,2,1)
plt.plot(list(alphas), qcolds, 'b-o')
plt.xlabel('Phase angle α [deg]'); plt.ylabel('Q_cold per cycle [J]')
plt.title('Cooling capacity vs. phase angle'); plt.grid(True)

plt.subplot(1,2,2)
plt.plot(list(alphas), cops, 'r-o')
plt.xlabel('Phase angle α [deg]'); plt.ylabel('COP (Schmidt ideal)')
plt.title('COP vs. phase angle'); plt.grid(True)
plt.tight_layout()
plt.savefig('stirling_phase_sweep.png', dpi=150)
plt.show()
```

---

### Thermodynamic Property Libraries

#### thermo (Caleb Bell)

```bash
pip install thermo chemicals
```

```python
from thermo import ChemicalConstantsPackage, CEOSGas, PRMIX
from thermo.interaction_parameters import IPDB

# Peng-Robinson EOS for Helium
constants, correlations = ChemicalConstantsPackage.from_IDs(['helium'])
eos_kwargs = dict(Tcs=constants.Tcs, Pcs=constants.Pcs, omegas=constants.omegas)
gas = CEOSGas(PRMIX, eos_kwargs=eos_kwargs, T=300, P=1e6, zs=[1])
print(f"He at 300K, 10bar: H = {gas.H():.1f} J/mol, S = {gas.S():.3f} J/mol/K")
```

**Documentation:** https://thermo.readthedocs.io

#### iapws (Water/Steam)

```bash
pip install iapws
```

```python
from iapws import IAPWS97

# Superheated steam
steam = IAPWS97(T=500, P=10)  # T in K, P in MPa
print(f"h = {steam.h:.2f} kJ/kg, s = {steam.s:.4f} kJ/kg/K")
```

---

### NIST REFPROP

- **Gold standard** for thermodynamic properties; most accurate equations of state
- **Cost:** ~$300 personal license, ~$2000 professional; https://www.nist.gov/srd/refprop
- **Python wrapper:**
  ```bash
  pip install ctREFPROP  # requires REFPROP DLL to be installed separately
  ```
  ```python
  from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary
  RP = REFPROPFunctionLibrary('/path/to/REFPROP')
  RP.SETPATHdll('/path/to/REFPROP/fluids')
  r = RP.REFPROPdll('Helium','TP','H',0,0,0,300,1000,[1.0])
  print(f"Enthalpy: {r.Output[0]:.2f} J/mol")
  ```
- **Free alternative:** NIST WebBook — https://webbook.nist.gov/chemistry/fluid/

---

### EES (Engineering Equation Solver)

- Integrated thermodynamic property database + equation solver
- **Best for**: cycle analysis, parametric tables, built-in unit handling
- **Pricing**: ~$300 student, ~$900 professional; https://www.fchart.com/ees/
- Built-in functions: `h_('R134a',T=250[K],x=1)` for saturated vapor enthalpy
- Parametric table: sweep operating conditions automatically and plot results

---

### OpenModelica + ThermoSysPro

**Installation:**
```bash
# OpenModelica
wget https://openmodelica.org/download/...  # platform-specific installer
# Or: sudo apt install openmodelica  (Debian/Ubuntu)
```

- **ThermoSysPro library**: https://github.com/EDF-Lab/ThermoSysPro — open source, EDF-developed
- Good for transient simulation of complex cycles (heat exchangers, multi-stage)
- Steeper learning curve than EES but fully free and equation-based

---

### TRNSYS & EnergyPlus

| Tool | Best For | License |
|------|---------|---------|
| **TRNSYS** | Transient solar thermal + absorption cooling; component-based | ~$3000 academic; https://sel.me.wisc.edu/trnsys |
| **EnergyPlus** | Building-level cooling loads + HVAC system simulation | Free (open source); https://energyplus.net |

---

### Hand Calculation Reference Methods

#### LMTD for Heat Exchangers

$$Q = U \cdot A \cdot LMTD$$

$$LMTD = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)}$$

For a counter-flow heat exchanger:
- $\Delta T_1 = T_{hot,in} - T_{cold,out}$
- $\Delta T_2 = T_{hot,out} - T_{cold,in}$

#### NTU-Effectiveness Method

For compact heat exchangers (common in cryocoolers):

$$\varepsilon = \frac{Q_{actual}}{Q_{max}} = \frac{C_{min}(T_{hot,in} - T_{cold,in})}{Q_{actual}} \cdot ...$$

$$NTU = \frac{U \cdot A}{C_{min}}$$

For counter-flow HX with $C_r = C_{min}/C_{max}$:

$$\varepsilon = \frac{1 - \exp[-NTU(1-C_r)]}{1 - C_r \exp[-NTU(1-C_r)]}$$

---

## 15. Key Textbooks & References

### Primary References — Cryogenic/Stirling

| Title | Author(s) | Notes |
|-------|-----------|-------|
| **Stirling Engines** | Walker (1980) | Classic; complete Schmidt analysis derivation |
| **The Stirling Engine Manual** | Organ (1997, 2007) | Two volumes; regenerator theory |
| **Cryogenic Engineering** | Flynn (2nd ed., 2005) | Comprehensive; covers Stirling, GM, PTR, dilution |
| **Refrigeration at Cryogenic Temperatures** | Radebaugh (NIST) | Free NIST monograph; excellent engineering guide |

### Refrigeration & HVAC

| Title | Author(s) | Notes |
|-------|-----------|-------|
| **Industrial Refrigeration Handbook** | Stoecker | Standard reference for industrial systems |
| **Refrigeration and Air Conditioning** | Dossat & Horan | Undergraduate-level; good fundamentals |
| **ASHRAE Fundamentals Handbook** | ASHRAE | Updated annually; authoritative for HVAC |
| **Principles of Heat and Mass Transfer** | Incropera et al. | Heat exchanger design; standard textbook |

### Online Resources

| Resource | URL | Notes |
|----------|-----|-------|
| **NIST WebBook** | https://webbook.nist.gov/chemistry/fluid/ | Free fluid properties; saturation tables, T-s diagrams |
| **NIST REFPROP** | https://www.nist.gov/srd/refprop | Purchase page; most accurate EOS |
| **CoolProp docs** | https://coolprop.org | Installation, API reference, fluid list |
| **ASHRAE online** | https://www.ashrae.org/technical-resources | Standards, calculators (membership required for some) |
| **Engineering Toolbox** | https://www.engineeringtoolbox.com/refrigeration-d_939.html | Quick reference, R-value calculators |
| **Radebaugh NIST review** | https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir5765.pdf | Free; survey of cryocooler technology |
| **ICEAA pulse tube tutorial** | https://www.iceaa.net | Thermoacoustic refrigeration tutorials |

---

*End of document — Stirling Cycle Refrigeration & Simulation Tools*
