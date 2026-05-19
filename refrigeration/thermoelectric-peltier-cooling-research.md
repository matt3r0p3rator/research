# Thermoelectric (Peltier Effect) Cooling: Comprehensive Research Guide

*Electric-powered solid-state cooling with no moving parts — via the Peltier effect.*

---

## Table of Contents

1. [Physics of Thermoelectric Effects](#physics-of-thermoelectric-effects)
2. [Thermoelectric Module Operation](#thermoelectric-module-operation)
3. [Bismuth Telluride — Primary Material](#bismuth-telluride)
4. [Other Thermoelectric Materials](#other-thermoelectric-materials)
5. [Module Construction](#module-construction)
6. [Cascade Multi-Stage TEC Systems](#cascade-systems)
7. [Practical Applications and Limitations](#practical-applications)
8. [Heat Sink Design](#heat-sink-design)
9. [Raw Material Sourcing](#raw-material-sourcing)
10. [Surprising Findings and Emerging Research](#surprising-findings)

---

## 1. Physics of Thermoelectric Effects

### 1.1 The Seebeck Effect (1821)

When a temperature gradient exists across a conductor, an EMF is generated:
$$\mathbf{E}_{EMF} = -S \nabla T$$

Where S is the **Seebeck coefficient** (thermopower, units V/K). For two dissimilar materials A and B:
$$V = (S_A - S_B) \cdot \Delta T$$

Typical values: metals ±1–10 μV/K; semiconductors ±100–1000 μV/K. Sign indicates carrier type: n-type materials have negative S (electrons accumulate at cold end), p-type have positive S (holes accumulate at cold end).

### 1.2 The Peltier Effect (1834)

When current I flows through a junction of two dissimilar conductors, heat is generated or absorbed:
$$\dot{Q} = (\Pi_A - \Pi_B) \cdot I$$

Where Π is the **Peltier coefficient** (W/A). Related to Seebeck coefficient by the **second Thomson relation:**
$$\Pi = T \cdot S$$

For a typical Bi₂Te₃ module: S ≈ 400 μV/K (total n+p pair); at T = 300 K: Π = 300 × 400×10⁻⁶ = 0.12 W/A. So a module passing 5A pumps ~0.6 W at each junction. Commercial modules achieve ~10 W/A.

### 1.3 The Thomson Effect (1851)

In a current-carrying conductor with temperature gradient:
$$\dot{q} = -K \mathbf{J} \cdot \nabla T$$

Where K = Thomson coefficient = T · (dS/dT). Typically 1–5% of total thermoelectric effect; often neglected in first-order analysis.

### 1.4 Figure of Merit ZT

The efficiency of a thermoelectric material is characterized by the **dimensionless figure of merit:**
$$ZT = \frac{S^2 \sigma T}{\kappa} = \frac{S^2 T}{\rho \kappa}$$

Where:
- S = Seebeck coefficient (V/K)
- σ = electrical conductivity (S/m); ρ = 1/σ = resistivity
- T = absolute temperature (K)
- κ = total thermal conductivity (W/m·K) = κ_electron + κ_phonon

The numerator S²σ is the **power factor** (W/m·K²).

**Maximum COP as fraction of Carnot COP:**
$$\frac{\text{COP}_{max}}{\text{COP}_{Carnot}} = \frac{\sqrt{1 + ZT_{avg}} - T_h/T_c}{\sqrt{1 + ZT_{avg}} + 1}$$

**Practical implications:**
- ZT = 1 → ~10–15% of Carnot efficiency
- ZT = 2 → ~22% of Carnot efficiency
- ZT = 3+ → ~30%+ of Carnot efficiency

Current commercial Bi₂Te₃ modules (ZT ~0.8–1.0) → COP of 0.3–0.6, versus COP ~2–3 for vapor compression.

### 1.5 The Core Challenge: Decoupling κ from σ

The **Wiedemann–Franz law** couples electrical and thermal conductivity:
$$\frac{\kappa_e}{\sigma T} = L_0 = 2.44 \times 10^{-8} \text{ W·Ω/K}^2$$

Increasing σ inevitably increases κ_e. Strategy: reduce **lattice thermal conductivity** κ_L (via nanostructuring, complex crystal structures, "rattler" atoms) while preserving electronic transport.

G.A. Slack's **"phonon glass, electron crystal" (PGEC)** concept: ideal thermoelectric behaves as a glass to phonons (high phonon scattering) but as a perfect crystal to electrons (high mobility, low scattering).

### 1.6 Best ZT Values (2025–2026)

| Material | Peak ZT | Temperature | Notes |
|---|---|---|---|
| SnSe single crystal | ~2.62 | 923 K | b-axis; anisotropic |
| SnSe polycrystalline (Na-doped) | ~3.1 | ~783 K | 2021 breakthrough |
| PbTe/SrTe nanocomposite | ~2.2–2.5 | 800–900 K | All-scale hierarchical |
| GeTe (doped) | ~2.4 | ~750 K | Mid-temperature |
| Bi₂Te₃/Sb₂Te₃ superlattice | ~2.4 | 300 K | p-type thin film; Intel validation |
| Bulk (Bi,Sb)₂Te₃ nanocomposite | ~1.4–1.5 | 373 K | Practical bulk material |
| Filled skutterudites (Ce/La-CoSb₃) | ~1.7 | 600–800 K | Rattler atoms |
| Heusler thin film (metastable) | ~5–6 | — | Hinterleitner 2019 — contested, not bulk-reproducible |

---

## 2. Thermoelectric Module Operation

### 2.1 Module Architecture

A TEC module consists of:
- Multiple thermocouple pairs (typically 127 in a standard 40×40 mm module; range: 6 to 254)
- Each pair: one n-type and one p-type semiconductor leg, ~1–2 mm tall
- Legs are **electrically in series** (current flows through all legs sequentially)
- Legs are **thermally in parallel** (heat flows through all legs simultaneously)
- Metal interconnects: typically copper (~0.1 mm), plated with Ni or Ag
- Substrates: aluminum oxide (Al₂O₃) or aluminum nitride (AlN) ceramic

### 2.2 Commercial Bi₂Te₃ Module Specifications

Example: TEC1-12706 (TEC = thermoelectric cooler, 1 = single stage, 127 = couple count, 06 = max current in A)

| Parameter | Typical Range | Notes |
|---|---|---|
| ΔT_max (no heat load) | 68–72°C | At T_h = 25°C; decreases at higher T_h |
| Q_max (max heat pumped) | 50–100 W | At ΔT = 0, maximum current |
| I_max | 5–15 A | TEC1-12706: 6A; TEC1-12710: 10A |
| V_max | 14.4–16.0 V | At T_h = 25°C |
| Module resistance (ACR) | 1.6–3.0 Ω | AC resistance |
| Dimensions | 30×30 to 62×62 mm | — |
| MTBF | >100,000 hours | At rated conditions |

### 2.3 COP and Performance Equations

Heat pumped from cold side (Q_c), rejected at hot side (Q_h), electrical input (P):
$$Q_c = \alpha I T_c - \frac{1}{2}I^2 R - K \Delta T$$
$$Q_h = \alpha I T_h + \frac{1}{2}I^2 R - K \Delta T$$
$$P = Q_h - Q_c = \alpha I \Delta T + I^2 R$$

Where:
- α = total module Seebeck coefficient (0.02–0.05 V/K)
- I = current (A)
- T_c, T_h = cold-side and hot-side temperatures (K)
- ΔT = T_h - T_c
- R = module electrical resistance (Ω)
- K = module thermal conductance (W/K)

The three terms in Q_c:
1. **αIT_c** — Peltier cooling (desired effect, linear with I)
2. **-½I²R** — half the Joule heat conducted back to cold side (scales as I²)
3. **-KΔT** — thermal leakback through legs (grows with ΔT)

**COP:**
$$\text{COP} = \frac{Q_c}{P} = \frac{\alpha T_c I - \frac{1}{2}I^2 R - K \Delta T}{\alpha I \Delta T + I^2 R}$$

**Optimal current for maximum COP:**
$$I_{opt,COP} = \frac{\alpha \Delta T}{R(\sqrt{1+ZT} - 1)}$$

This is lower than I_max — running at partial current maximizes efficiency.

**Operating line (for given I):**
$$\Delta T = \Delta T_{max}\left(1 - \frac{Q_c}{Q_{max}}\right)$$

---

## 3. Bismuth Telluride (Bi₂Te₃) — Primary Material

### 3.1 Crystal Structure and Properties

| Property | Value |
|---|---|
| Crystal structure | Trigonal (rhombohedral), tetradymite-type layered |
| Space group | R3̄m (#166) |
| Lattice parameters | a = 0.4395 nm, c = 3.044 nm |
| Density | 7.74 g/cm³ |
| Melting point | 585°C |
| Bandgap | ~0.16 eV (direct) |
| Seebeck coefficient | +200 to +300 μV/K (p-type); −200 to −250 μV/K (n-type) |
| Electrical conductivity | ~1.1×10⁵ S/m |
| Thermal conductivity | 1.2–1.5 W/m·K total; κ_L ≈ 0.7 W/m·K |
| ZT at 300 K | ~0.8–1.0 (bulk); ~1.5 (optimized nanostructured) |

Bi₂Te₃ is **strongly anisotropic**: best ZT measured in-plane (perpendicular to c-axis). Directional solidification aligns grains for optimal performance.

**Why Bi₂Te₃ dominates room-temperature use:** Bandgap of ~0.16 eV suppresses bipolar conduction (requires E_g > 6k_BT ≈ 0.16 eV). Heavy atoms (Bi: 209 u, Te: 128 u) provide intrinsically low lattice κ via slow phonon group velocities and high anharmonicity.

### 3.2 Doping Strategy

**P-type: (Bi_xSb_{1-x})₂Te₃, typically Bi₀.₅Sb₁.₅Te₃**
- ~75% Sb substitution for Bi → ZT ~1.0–1.3 at 300 K
- Alternatively: excess Te (Te antisite defects) or Cu₂Te doping

**N-type: Bi₂(Te_xSe_{1-x})₃, typically Bi₂Te₂.₇Se₀.₃**
- ~5–10% Se substitution for Te → ZT ~0.9–1.1 at 300 K
- Also doped with SbI₃ (I on Te site = donor), CuBr, or HgBr₂

### 3.3 Synthesis Route A: Melt Synthesis (Bridgman / Zone Melting)

**Industrial standard for bulk ingots.** Produces directionally solidified crystal with grain alignment.

**Materials needed (n-type Bi₂Te₂.₇Se₀.₃ example):**
- Bismuth metal: 99.999% (5N), 417.96 g
- Tellurium metal: 99.999% (5N), 344.52 g
- Selenium metal: 99.999% (5N), 23.69 g

**Procedure:**
1. Weigh and combine stoichiometric quantities in glovebox (Ar atmosphere)
2. Place in quartz ampoule (~12–25 mm inner diameter)
3. **Evacuate to <10⁻⁴ torr** (preferably <10⁻⁶ torr); backfill with 50–100 torr Ar/He; seal by torch
   - ⚠️ **SAFETY:** Te vapor pressure at 620°C is ~0.1 atm; failure to properly seal before heating can cause explosive ampoule rupture and toxic Te vapor. Use fume hood and blast shield.
4. Place in vertical Bridgman furnace: upper zone 620–650°C, lower zone 450–500°C
5. Hold at temperature ~2–4 hours until uniform melt
6. Translate ampoule downward at **1–5 mm/hour** through thermal gradient (directional solidification)
7. Cool to room temperature at ≤50°C/hour (prevent thermal shock cracking)
8. **Anneal** at 250–350°C for 24–72 hours in Te/Se atmosphere to homogenize composition
9. Cut ingot into ~1.5 mm wafers by wire saw; lap and dice into legs (~1.5×1.5×1.5 mm)

**Zone melting (alternative):** Narrow RF induction coil traverses charge at ~2 mm/hour, producing single-crystal-like material with zone purification.

**Quality metrics:** ZEM-3 for Seebeck/resistivity, laser flash for κ. Target: S > 220 μV/K, ρ < 1.0×10⁻⁵ Ω·m, κ < 1.5 W/m·K.

### 3.4 Synthesis Route B: Mechanical Alloying + Spark Plasma Sintering (MA+SPS)

Produces **nanostructured** Bi₂Te₃ with 20–500 nm grain sizes. Poudel et al. (Science, 2008) demonstrated ZT ~1.4 at 100°C for p-type (Bi,Sb)₂Te₃ via this route.

**Ball milling:**
1. Weigh stoichiometric quantities (can use 4N purity)
2. Place in WC/Co planetary ball mill jar with 10–15 mm balls (ball-to-powder ratio 10:1 to 20:1)
3. Mill under **argon atmosphere** for **10–40 hours at 300–400 RPM**
   - Check by XRD: Bi₂Te₃ phase with broadened peaks (Scherrer: crystallite size 20–100 nm)

**Spark Plasma Sintering:**
1. Load milled powder (5–10 g) into graphite die (12–20 mm diameter) with graphite foil liner
2. Apply uniaxial pressure: **50–100 MPa**
3. Apply pulsed DC current to heat sample by Joule heating
4. Heat to **350–450°C at 100°C/min**; hold **3–10 minutes**
5. Release pressure while hot; cool; extract pellet
6. Measure density by Archimedes method (target: >95% theoretical density)

**Result:** ZT ~1.2–1.5 at 300–400 K for optimized compositions; some reports of ~1.8 with triple-hierarchical nanostructures.

### 3.5 Synthesis Route C: Solvothermal (Nanomaterials)

**P-type Bi₀.₅Sb₁.₅Te₃ nanoplates:**
1. Dissolve BiCl₃ (0.5 mmol) and SbCl₃ (1.5 mmol) in ethylene glycol (50 mL)
2. Add Na₂TeO₃ (3 mmol) as Te source
3. Add NaBH₄ (10 mmol) as reducing agent; stir vigorously
4. Transfer to 100 mL Teflon-lined stainless steel autoclave
5. Heat at **160–200°C for 12–24 hours**
6. Cool; centrifuge at 8000 RPM; wash with ethanol and water
7. Dry under vacuum at 60°C; optional anneal at 300°C in H₂/Ar forming gas

**N-type Bi₂Te₂.₇Se₀.₃:** Replace Na₂TeO₃ with Na₂TeO₃/Na₂SeO₃ mixture (2.7:0.3 ratio).

### 3.6 Synthesis Route D: Electrodeposition (Thin Films)

Used for MEMS-scale coolers and thin-film devices.

**Electrolyte:**
- 0.01–0.05 M Bi(NO₃)₃ in dilute HNO₃ (pH 0.5–1.5)
- 0.005–0.02 M TeO₂ dissolved in HNO₃ (forms HTeO₂⁺ ions)
- pH control critical: at pH > 3, Te precipitates; at pH < 0, Bi deposits preferentially

**Deposition:**
1. Substrate: Au/Ti on Si wafer or Cu foil
2. Three-electrode cell: working (substrate), Pt counter, Ag/AgCl reference
3. **Potentiostatic deposition at −100 to −180 mV vs. Ag/AgCl** (optimal: −130 mV)
4. Deposition rate: ~0.5–2 μm/hour at 5 mA/cm²
5. Post-anneal at 250–350°C in N₂ for 30–60 min

Venkatasubramanian et al. (Nature, 2001) achieved ZT ~2.4 using MOCVD-grown superlattices of alternating 10 Å Bi₂Te₃ / 50 Å Sb₂Te₃ layers.

---

## 4. Other Thermoelectric Materials

### 4.1 Lead Telluride (PbTe) — Mid-Temperature

| Property | Value |
|---|---|
| Temperature range | 400–700 K (127–427°C) |
| Bandgap | ~0.32 eV at 300 K |
| Best ZT | ~2.2 (Na-doped PbTe/SrTe nanocomposite, 915 K) |
| Toxicity | HIGH — Pb is cumulative neurotoxin; EU RoHS restricted |
| Melting point | 924°C |

**Synthesis:** Identical to Bi₂Te₃ melt method but at higher temperature (~1000°C melt). Mix Pb and Te (1:1 molar), seal in evacuated quartz ampoule, melt, Bridgman-cool at 1–5 mm/hour. Dope Na (p-type) or Bi/I (n-type).

**Key strategy:** "All-scale hierarchical architecture" (Biswas et al., Nature 2012): atomic-scale doping + nanoscale SrTe precipitates (2–10 nm) + mesoscale grain boundaries (1–5 μm) → κ_L reduced to ~0.5 W/m·K.

### 4.2 Silicon-Germanium (SiGe) — High Temperature / Space

| Property | Value |
|---|---|
| Temperature range | 900–1300 K |
| Best ZT | ~1.0–1.3 at 1000°C (n-type Si₈₀Ge₂₀) |
| Applications | RTGs on Voyager, Cassini, Curiosity rover |

**Synthesis:** Ball mill Si and Ge powders, melt together (or SPS). Dope with P (n-type) or B (p-type). Alloying scatters phonons (mass contrast Si=28 vs Ge=73) reducing κ from ~150 W/m·K (pure Si) to ~5–8 W/m·K.

### 4.3 Filled Skutterudites (CoSb₃ + rare earth "rattlers")

| Property | Value |
|---|---|
| Formula | LM₄X₁₂ (L = rare earth cage-filling atom, e.g. La, Ce, Yb) |
| Temperature range | 500–900 K |
| Best ZT | ~1.7–2.0 |
| Applications | NASA Multi-Mission RTG (planned SiGe replacement) |

**Why they work:** Rare earth atoms in oversized cages vibrate with large amplitude, scattering phonons over broad frequency range (PGEC principle in action).

**Synthesis:** Ball mill elemental Co, Sb, and rare-earth powders in Ar; SPS at 600–700°C, 65 MPa, 5–8 min.

### 4.4 Half-Heusler Alloys — Robust Mid-Temperature

| Property | Value |
|---|---|
| Formula | XYZ cubic (e.g., TiNiSn, ZrNiSn, NbFeSb) |
| Temperature range | 700–1000 K |
| Best ZT | ~1.5 (NbFeSb-based, p-type) |
| Advantages | Earth-abundant, no Pb/Te/Se, mechanically robust |

**Synthesis:** Ball mill elemental powders; SPS at 900–1100°C. Hf/Ti substitution on X site most effective at reducing κ.

### 4.5 Tin Selenide (SnSe) — Current Record Holder

| Property | Value |
|---|---|
| Crystal structure | Orthorhombic (Pnma), layers held by weak van der Waals |
| Bandgap | 0.9 eV (indirect) |
| Melting point | 861°C |
| Best ZT | 2.62 at 923 K (b-axis, single crystal; Zhao et al., Nature 2014) |
| Polycrystalline ZT | 3.1 at 783 K (Na-doped, 2021) |
| Lattice κ | 0.23 W/m·K at 923 K (extraordinarily low) |

**Why SnSe is exceptional:** Sn²⁺ stereochemically active lone pair creates extreme bond anharmonicity (Grüneisen parameter γ > 3). Layered structure blocks cross-plane phonon transport. Multiple valence band valleys provide high carrier mobility above ~750 K (Pnma→Cmcm transition).

**Synthesis of SnSe single crystal:**
1. Mix Sn (99.999%) and Se (99.999%) in 1:1 molar ratio in evacuated quartz ampoule
2. Heat to 950–1000°C; hold 12 hours
3. **Slow cool at 1–2°C/hour to 700°C** (must traverse Cmcm→Pnma transition at ~750 K very slowly to avoid cracking)
4. Continue cooling at 5°C/hour to room temperature
5. Measure crystal orientation by Laue diffraction (b-axis shows highest ZT)

### 4.6 Organic Thermoelectrics: PEDOT:PSS

| Property | Value |
|---|---|
| Best ZT (p-type) | ~0.42–0.7 |
| Seebeck coefficient | +15–30 μV/K |
| Advantages | Flexible, lightweight, solution-processable, non-toxic |
| Challenges | Low ZT; n-type unstable in air; poor thermal stability >150°C |

**Processing:** Commercial PEDOT:PSS (Heraeus Clevios PH-1000) spin-coated or inkjet-printed onto substrates. Post-treatment with H₂SO₄, DMSO, or ethylene glycol removes excess PSS, raises σ by 2–3 orders of magnitude.

### 4.7 ZT Summary Table

| Material | Temperature (K) | ZT | Type |
|---|---|---|---|
| Bi₂Te₃ (bulk commercial) | 300 | 1.0 | p/n |
| (Bi,Sb)₂Te₃ nanocomposite | 373 | 1.4 | p |
| PbTe:Na/SrTe hierarchical | 915 | 2.2 | p |
| GeTe (Bi-doped) | 773 | 2.4 | p |
| SnSe single crystal (b-axis) | 923 | 2.62 | p |
| SnSe polycrystalline (Na-doped) | 783 | 3.1 | p |
| Filled skutterudite CoSb₃ | 800 | 1.7 | n |
| NbFeSb Half-Heusler | 1100 | 1.5 | p |
| Si₈₀Ge₂₀ (RTG) | 1173 | 1.0–1.3 | n |
| PEDOT:PSS (organic) | 300–350 | 0.42 | p |

---

## 5. Module Construction

### 5.1 Assembly Process

1. **Ingot preparation:** Bridgman-grown ingots → cut into ~1.5 mm wafers by wire saw → lap and dice into legs (~1.5×1.5×1.5 mm)

2. **Leg metallization:** Both ends metallized with:
   - Nickel barrier layer (1–3 μm by electroplating or sputtering) — prevents solder diffusion into Bi₂Te₃
   - Gold or silver flash over Ni for solderability

3. **Substrate preparation:** Al₂O₃ or AlN ceramic tiles with **DBC (direct bond copper)** coating — copper foil bonded to ceramic at ~1065°C, then photolithographically etched to form interdigitated conductor pattern

4. **Module assembly:**
   - Dispense solder paste (typically Bi₅₈Sn₄₂ mp 138°C; or Au₂₀Sn₈₀ mp 280°C for high-reliability) by stencil printing
   - Place n-type and p-type legs alternately by pick-and-place (±0.1 mm precision); legs must connect n→copper→p→copper in series
   - Place top ceramic substrate
   - Reflow solder at 160–200°C peak, 30–90 s dwell, in N₂ atmosphere

5. **Encapsulation:** Silicone elastomer perimeter bead; leads (28–22 AWG tinned Cu wire) soldered to terminals

### 5.2 Substrate Comparison

| Property | Al₂O₃ | AlN |
|---|---|---|
| Thermal conductivity (W/m·K) | 24–30 | 150–180 |
| CTE (ppm/K) | 6.7 | 4.5 |
| Cost | Low (baseline) | 3–5× Al₂O₃ |
| Use case | Standard commercial | High-performance |

---

## 6. Cascade (Multi-Stage) TEC Systems

### 6.1 Principles

Multiple stages stacked — each stage acts as heat load for the stage below. The temperature achievable with N stages is **not** simply N × 68°C because each lower stage adds Joule heat that must be pumped by the stage below.

### 6.2 Practical ΔT Limits (at no heat load, 25°C ambient)

| Stages | ΔT_max (practical) | Min temp from +25°C |
|---|---|---|
| 1 | ~68–72°C | ~−43 to −47°C |
| 2 | ~90–100°C | ~−65 to −75°C |
| 3 | ~105–120°C | ~−80 to −95°C |
| 4 | ~115–130°C | ~−90 to −105°C |

Under actual heat load, achievable ΔT drops significantly.

### 6.3 Heat Flow Management in 2-Stage Cascade

- **Stage 1 (cold stage):** Pumps Q_c,1 from the object being cooled
- **Stage 2 (hot stage):** Must pump Q_c,1 + P_1 plus its own electrical power
- Area ratio: stage 2 typically 3–5× the area of stage 1

Three-stage TEC cooling a CCD to −90°C may consume 50–100 W to maintain a few milliwatts of cooling.

### 6.4 Segmented Legs for Multi-Stage

Different materials along the leg height:
- Near hot side (300–500 K): Bi₂Te₃ optimal
- Mid range (500–700 K): PbTe or GeTe
- Near cold side (<250 K): Bi-Sb alloys (Bi₉₅Sb₅)

---

## 7. Practical Applications and Limitations

### 7.1 Major Applications

**DNA Thermal Cyclers (PCR):** Most widespread precision TEC application. Rapid cycling between 95°C / 55°C / 72°C at 5–10°C/s; PID control to ±0.1°C. The TEC both heats and cools.

**Laser diode temperature stabilization:** DWDM telecom lasers require wavelength stability within ±12.5 GHz of ITU grid (~±0.1 nm/°C drift). TEC maintains junction to ±0.01°C in feedback loop. Typical: 6×6 mm module, 1–3 W, integrated in butterfly package.

**CCD/CMOS sensor cooling (astronomy):** Dark current halves every 6–8°C. Astronomical cameras cool CCDs to −100°C via 3–4 stage cascade TECs — eliminating liquid nitrogen dewars.

**Portable vehicle coolers:** 12V DC operation. Typical: TEC1-12706 module, finned Al heat sinks, 12V fan. Can maintain contents ~20°C below ambient. COP ~0.3–0.5.

**Cloud chambers for radiation visualization:** 2-stage TEC can cool vapor below −26°C, enabling continuous visualization of ionizing radiation — popular in physics education.

**Wearable cooling (emerging):** Thin-film Bi₂Te₃ on polyimide for stretchable patches. Embr Labs Wave 2 wristband (commercial): cools wrist's pulse point by 1–2°C for perceived whole-body cooling. Intel Cryo Cooling Technology: TEC + water cooling for CPU junction cooling below ambient.

### 7.2 Why TEC Efficiency is ~10% That of Vapor Compression

At ZT ≈ 1.0, 40°C temperature lift:
- Carnot COP = 6.65
- TEC COP ≈ 0.12 × 6.65 ≈ 0.8
- Vapor compression achieves COP ~2.7–4.0 (40–60% of Carnot)

**Root cause:** The Joule heating term (I²R) is always present and grows faster than Peltier cooling as current increases. To pump more heat, you increase I, but I²R waste grows quadratically.

**The threshold for competitiveness:** ZT > 3–4 would make TEC competitive with vapor compression. At ZT = 4, COP approaches ~40% of Carnot (~2.7 for 40°C lift). This is the materials science target.

### 7.3 Advantages of TEC Despite Low Efficiency

- No moving parts: MTBF >100,000 hours vs. compressor ~10,000–50,000 hours
- No refrigerant: no CFC/HFC leakage risk, no pressure vessels
- Precise temperature control: PID to ±0.001°C; bidirectional (can heat or cool)
- Compact: from 2×2 mm to 60×60 mm; any orientation
- Low vibration and noise: critical for precision instruments
- Rapid response: no thermal mass in fluid loops

---

## 8. Heat Sink Design

### 8.1 Why Hot-Side Thermal Management Dominates

Every watt pumped from cold side exits through hot side PLUS all electrical power input.

For a module cooling 30 W (Q_c) with COP = 0.5:
$$Q_h = Q_c + P = 30 + 60 = 90 \text{ W}$$

If hot-side heat sink has R = 0.5 K/W:
$$T_h = 25°C + 90 \times 0.5 = 70°C$$

But the module's ΔT_max assumes T_h = 25°C! At T_h = 70°C, ΔT_max drops to ~55–60°C, so minimum cold-side = 70 − 55 = **+15°C** instead of −47°C. This is why hot-side heat sink quality dominates system performance.

### 8.2 Thermal Resistance Model

$$\Delta T_{total} = Q_c \cdot (R_{cs} + R_{module}) + Q_h \cdot (R_{TIM,hot} + R_{heatsink})$$

**Thermal interface materials (TIM):**
- Arctic Silver 5 thermal grease: κ ≈ 8–9 W/m·K; contact resistance ~0.01–0.05 K/W·cm²
- Indium foil: κ = 82 W/m·K; excellent conformance; best for high performance
- Phase-change TIM: melts at operating temperature for better conformance

### 8.3 Heat Sink Types

**Finned aluminum + forced convection (most common):**
- Al 6061/6063, anodized
- Fin spacing: 2–4 mm forced air; 8–15 mm natural convection
- Thermal resistance: R = 0.1–0.5 K/W (forced air), 0.5–2.0 K/W (natural convection) per 40×40 mm module

**Required airflow:**
$$\text{CFM} = \frac{Q_h \times 1.76}{\Delta T_{allowable}}$$

For Q_h = 90 W, ΔT_allowable = 15°C: ~10.6 CFM minimum.

**Water/liquid cooling:** Water block with copper microchannels: R ≈ 0.02–0.05 K/W. Used in Intel Cryo cooling technology.

### 8.4 System Design Rules

1. Maximize heat sink area on hot side (dominates system performance)
2. Use thermal grease or indium foil — never leave air gaps
3. Account for Q_h (not Q_c) when sizing heat sink
4. Use PID control — minimum current needed to maintain set temperature; lower current = much lower I²R waste
5. Insulate cold side from ambient to prevent condensation and parasitic heat load
6. Use desiccant or dry nitrogen purge in sealed cold-side enclosures

---

## 9. Raw Material Sourcing

### Tellurium (for Bi₂Te₃)

**Critical material** — ~500 metric tonnes produced globally per year.

**Primary source:** Byproduct of copper electrolytic refining. Copper anode slimes (2–10% Te) are processed:
1. Oxidative leach with H₂SO₄ + HNO₃
2. Neutralization → TeO₂ precipitate
3. Reduction of TeO₂:
   - Carbon reduction: TeO₂ + 2C → Te + 2CO at 500–600°C
   - Hydrogen reduction: TeO₂ + 2H₂ → Te + 2H₂O at 450°C
   - Electrolytic refining in NaOH: deposit at −0.9 V vs. SHE
4. Zone refining to 6N purity

**Price:** Fluctuates $10–100/kg depending on Cu production rates and competition with CdTe solar panels (First Solar consumes most global Te supply).

### Bismuth (for Bi₂Te₃)

Byproduct of **lead smelting** (~20,000 tonnes/year globally, mainly China).

**Production route:**
1. Pb-Bi alloy → liquation at ~330°C (Pb-Bi eutectic separation)
2. Betterton-Krohl process: add Ca and Mg → scavenge Bi as Ca₂Bi₂ and Mg₃Bi₂ intermetallics
3. Remove dross; chlorinate to BiCl₃; reduce to metal

**Alternative:** Roast bismuthinite ore: 2Bi₂S₃ + 9O₂ → 2Bi₂O₃ + 6SO₂; then Bi₂O₃ + 3C → 2Bi + 3CO at ~800°C.

**Relatively non-toxic** compared to Pb or Te. Used medicinally (Pepto-Bismol).

### Antimony (for p-type Bi₂Te₃)

From stibnite ore (Sb₂S₃) or byproduct of Pb smelting. Roast Sb₂S₃ → Sb₂O₃; reduce Sb₂O₃ + 3C → 2Sb + 3CO at ~800°C. China: >80% of global supply.

### Selenium (for n-type Bi₂Te₃)

Coproduced with tellurium from copper anode slimes. Reduction of SeO₂ by SO₂ or carbon. ~2000 metric tonnes/year globally.

---

## 10. Surprising Findings and Emerging Research (2023–2026)

### Bi₂Te₃ is a Topological Insulator

Bi₂Te₃ — the primary commercial thermoelectric — is simultaneously a **topological insulator (TI)**: insulating bulk but conducting surface states protected by time-reversal symmetry, immune to backscattering from non-magnetic impurities. These surface states might enable higher Seebeck coefficients at the nanoscale. Research at ETH Zurich and Stanford is exploring TI surface states for enhanced thermoelectric performance in thin exfoliated flakes and MBE-grown films.

### Ionic Thermoelectrics

Ionic Seebeck coefficients can be **1–2 mV/K** — orders of magnitude larger than electronic Seebeck (~200 μV/K for Bi₂Te₃). Mechanism: thermal diffusion of ions (Soret effect). Key examples: hydrogel polymer electrolytes, thermogalvanic cells.

Ionic-electronic hybrid thermoelectrics ("ambipolar" materials) combine fast electronic transport with slow ionic drift for large Seebeck coefficient. MIT and ETH Zurich demonstrated **ionic thermoelectric supercapacitors (i-TESCs)** achieving energy density ~10× conventional thermoelectrics for pulsed applications (2024–2026).

### Machine Learning for Thermoelectric Discovery

Materials Project database: >100,000 inorganic compounds with DFT-computed properties. ML models trained on known ZT values predict new high-ZT compositions. Notable verified predictions (2023–2025):
- Pb-free, Bi-free mid-temperature chalcogenides (AgSbTe₂-based)
- Layered van der Waals materials (SnSe₂, In₂Se₃, GeSe)
- Antiperovskite thermoelectrics

### Cu₂Se "Liquid-Like" Thermoelectrics

Above ~400 K, Cu sublattice in Cu₂Se becomes liquid-like — Cu ions diffuse rapidly, scattering phonons like a liquid while Se provides a rigid crystalline framework for electron transport. ZT ~1.6 at 1000 K. **Challenge:** Cu electromigration under current flow causes composition instability (major reliability issue).

### Flexible and Wearable TEC Cooling

- **Stretchable TEC patches:** Thin-film Bi₂Te₃ on polyimide substrates, serpentine interconnects for strain tolerance. Can cool ~5°C below skin temperature.
- **Intel Cryo Cooling Technology (10th gen Core):** TEC + water cooling loop reduces CPU junction temperature below ambient, enabling sustained boost frequencies without throttling.

### Transverse Thermoelectric Devices

Traditional TECs use longitudinal geometry (current/heat parallel). **Transverse devices** use heat flow perpendicular to current, enabled by anisotropic materials or tilted multilayer composites. No P-N leg pairs needed — monolithic device. Research into pure Bi, NbSe₂, and Bi/Bi₂Te₃ multilayers shows promise.

---

## Key Numbers Summary

| Quantity | Value |
|---|---|
| Bi₂Te₃ melting point | 585°C |
| Commercial module ΔT_max | 68–72°C (single stage) |
| Commercial module ZT | ~1.0 |
| TEC COP at ZT=1, ΔT=40°C | ~0.8 (vs. Carnot COP 6.65) |
| TEC efficiency vs. vapor compression | ~10–25% |
| ZT needed to match vapor compression | ~3–4 |
| SnSe record ZT | 2.62 (single crystal) / 3.1 (polycrystalline 2021) |
| Seebeck coefficient (Bi₂Te₃ module pair) | ~400–450 μV/K |
| Wiedemann-Franz constant L₀ | 2.44×10⁻⁸ W·Ω/K² |
| Ball milling conditions (MA+SPS) | 10–40 h, 300–400 RPM, Ar atmosphere |
| SPS sintering conditions (Bi₂Te₃) | 350–450°C, 50–100 MPa, 3–10 min |
| Electrodeposition potential (Bi₂Te₃) | −130 mV vs. Ag/AgCl |
| Bridgman growth rate | 1–5 mm/hour |
| Quartz ampoule vacuum | <10⁻⁴ torr |
| Global Te production | ~500 metric tonnes/year |
| Thomson relation | Π = T · S |

### Key References

- Goldsmid, H.J. (2016) *Introduction to Thermoelectricity*. Springer.
- Snyder, G.J. & Toberer, E.S. (2008) "Complex thermoelectric materials." *Nature Materials* 7, 105–114.
- Poudel, B. et al. (2008) "High-Thermoelectric Performance of Nanostructured Bismuth Antimony Telluride Bulk Alloys." *Science* 320, 634.
- Zhao, L.-D. et al. (2014) "Ultralow thermal conductivity and high thermoelectric figure of merit in SnSe crystals." *Nature* 508, 373–377.
- Venkatasubramanian, R. et al. (2001) "Thin-film thermoelectric devices with high room-temperature figures of merit." *Nature* 413, 597–602.
- Biswas, K. et al. (2012) "High-performance bulk thermoelectrics with all-scale hierarchical architectures." *Nature* 489, 414–418.
