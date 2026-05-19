# Cloud Chamber Particle Detection: A Comprehensive Research Guide

## Table of Contents
1. [Physics Principles](#1-physics-principles)
2. [Cloud Chamber Types and Construction](#2-cloud-chamber-types-and-construction)
3. [Track Types and Identification](#3-track-types-and-identification)
4. [Radiation Sources](#4-radiation-sources)
5. [Track Physics and Quantitative Analysis](#5-track-physics-and-quantitative-analysis)
6. [Magnetic Field Analysis and Momentum Measurement](#6-magnetic-field-analysis-and-momentum-measurement)
7. [Photography and Imaging Techniques](#7-photography-and-imaging-techniques)
8. [Safety Considerations](#8-safety-considerations)
9. [Historic Discoveries Made in Cloud Chambers](#9-historic-discoveries-made-in-cloud-chambers)
10. [Advanced Experiments](#10-advanced-experiments)
11. [Further Reading](#11-further-reading)

---

## 1. Physics Principles

### How a Cloud Chamber Works

A cloud chamber (Wilson cloud chamber) is a particle detector that makes the paths of ionizing radiation visible. The core mechanism exploits **supersaturation**: a vapor — most commonly isopropanol (IPA) or ethanol — is cooled until it sits in a supersaturated state just above its dew point. When a charged particle passes through this sensitive volume, it ionizes molecules along its path. These ion clusters act as condensation nuclei, and tiny liquid droplets form along the track within milliseconds, producing a white mist trail that can be photographed before it disperses.

### The Sensitive Layer

In a continuous diffusion cloud chamber (the most common DIY design):

- The top of the chamber is at room temperature (~20 °C).
- The bottom rests on dry ice or a Peltier cooler (~−78 °C for dry ice).
- A temperature gradient drives a downward diffusion of saturated vapor.
- A thin band ~1–3 cm above the cold floor sits in the supersaturated "sensitive zone."
- A strong uniform illumination (LED strip or laser) from the side makes tracks visible by scattering.

### Ionization Mechanism

A charged particle traveling through the vapor loses energy continuously by electromagnetic interactions with atomic electrons (described by the **Bethe-Bloch formula**):

$$-\frac{dE}{dx} = \frac{4\pi z^2 e^4 N_A Z \rho}{m_e v^2 A} \left[\ln\frac{2 m_e v^2}{I(1-\beta^2)} - \beta^2\right]$$

Where:
- $z$ = charge of the projectile particle
- $v$ = particle velocity
- $Z$, $A$ = atomic number and mass of the medium
- $\rho$ = density of the medium
- $I$ = mean ionization potential of the medium
- $\beta = v/c$

**Key consequence:** Slow, heavy particles (like alpha particles) deposit energy densely → thick, bright, short tracks. Fast, light particles (like muons) deposit energy sparsely → thin, long, straight tracks.

---

## 2. Cloud Chamber Types and Construction

### 2.1 Expansion (Piston) Cloud Chamber — Original Wilson Type

- Gas + vapor is suddenly **expanded** (cooled adiabatically) by a piston or membrane.
- Supersaturation lasts only ~0.1–1 second per cycle; must be reset between shots.
- Used historically at particle accelerators where it was triggered by coincidence detectors.
- **Not practical for DIY** without precise mechanical control.

### 2.2 Continuous Diffusion Cloud Chamber — Standard DIY Design

**Materials:**
| Component | Specification |
|-----------|--------------|
| Chamber body | Aquarium, acrylic box, or fish tank (20–40 cm wide) |
| Top plate | Black felt glued to underside of lid (holds IPA) |
| Bottom plate | Aluminum or copper (good thermal conductor) |
| Cold source | Dry ice slabs (~−78 °C) or Peltier module stack |
| Working fluid | 99%+ isopropanol (rubbing alcohol is insufficient — 70% IPA won't work) |
| Illumination | High-power LED strip or 5 mW green/red laser pointer at side |
| Sealing | Foam gasket; chamber should be sealed to prevent vapor loss |

**Construction steps (simplified):**
1. Cut black felt to fit the interior top surface; soak with ~5–10 mL of IPA.
2. Place the aluminum bottom plate on the dry ice block.
3. Allow 10–15 minutes for the temperature gradient to stabilize.
4. The sensitive zone will appear as a slight shimmer just above the cold plate.
5. Dim room lights; illuminate from the side at a low angle (~5–10°).

**Optimizing sensitivity:**
- A weak electric field (~50–200 V DC) applied between top and bottom plates prevents positive ions from acting as parasitic condensation nuclei, dramatically improving track clarity. Connect the negative terminal to the bottom plate.
- Ensure the chamber is level; slanted surfaces destroy the diffusion gradient.
- Ambient humidity should be moderate; very dry conditions help.

### 2.3 Peltier-Cooled Cloud Chamber

- Uses thermoelectric (Peltier) modules instead of dry ice.
- Requires a significant heat sink and fan on the hot side.
- Typical two-stage Peltier arrangement reaches −30 to −45 °C; a three-stage setup can reach −60 °C.
- Less cold than dry ice, but continuously controllable and reusable.
- More complex to build but eliminates the need to source dry ice.

---

## 3. Track Types and Identification

### 3.1 Alpha Particle Tracks (α)

**Physical properties:**
- Composition: 2 protons + 2 neutrons (helium-4 nucleus), charge = +2e
- Typical energy from radioactive decay: 4–8 MeV
- Mass: 3,727 MeV/c²
- Air range at 5 MeV: ~3.5 cm at sea level

**Visual appearance:**
- **Thick, dense, straight** tracks with clearly defined length
- Abrupt endpoint (Bragg peak — particle stops nearly dead as all energy is deposited)
- Very dark/bright contrast because ionization density is ~1,000× that of minimum-ionizing particles
- All tracks from a single source have the **same length** (monoenergetic source)
- Slight curvature near the end due to the Bragg peak region

**Identification clues:**
- Uniformly thick from start to finish
- Sharp, defined length
- Minimal scattering (heavy mass, hard to deflect)
- With multiple alpha emitters in the same source, discrete groups of track lengths indicate different isotopes

### 3.2 Beta Particle Tracks (β⁻ and β⁺)

**Physical properties:**
- Composition: electron (β⁻) or positron (β⁺), charge = ±1e
- Typical energy: 0.01–3 MeV (continuous spectrum, not monoenergetic)
- Mass: 0.511 MeV/c²

**Visual appearance:**
- **Thin, wiggly, meandering** tracks
- Much longer range than alpha in air for comparable energy
- Numerous scattering kinks because the electron can deflect significantly off each nucleus (mass ratio near 1:1)
- Tracks fade in and out as the electron's speed varies
- Higher-energy beta particles: longer, straighter; lower-energy: more tortuous

**Key distinction from muons:** Beta tracks scatter much more visibly. A muon track is comparably thin but ruler-straight over long distances.

**Positron tracks (β⁺):** Visually identical to electron tracks; only distinguishable by their curvature in a magnetic field (opposite direction).

### 3.3 Muon Tracks (μ)

**Physical properties:**
- Composition: elementary lepton, charge = ±1e
- Mass: 105.66 MeV/c² (206.7× electron mass)
- Mean lifetime: 2.197 μs
- Cosmic ray muons at sea level: ~10,000 per m² per minute
- Typical energy at sea level: ~3–4 GeV (mean), range ~10 km in air

**Visual appearance:**
- **Thin, perfectly straight, long** tracks crossing the entire chamber
- Often arrive from above (downward-going cosmic ray secondaries), but due to scattering in the atmosphere have a broad angular spread
- Very similar ionization density to electrons, but no scattering kinks
- The defining feature: **ruler-straight over the full chamber length**
- May occasionally show a sharp kink if the muon undergoes a nuclear scatter
- Muon decay: μ⁻ → e⁻ + ν̄ₑ + νμ. Rarely observable, but a sudden track ending with a short spiraling secondary electron track is a textbook muon decay signature

**Cosmic rate:** In a 30×30 cm chamber sensitive zone of ~3 cm thickness, expect roughly 5–15 muon tracks per minute under normal conditions.

### 3.4 Proton Tracks

**Physical properties:**
- Mass: 938.3 MeV/c², charge = +1e
- Can appear from cosmic ray interactions (spallation), nuclear reactions, or in chambers exposed to neutron sources

**Visual appearance:**
- **Shorter and thicker** than muon tracks, thinner than alpha tracks
- More curved and scattered than muon tracks
- Range intermediate between alpha and muon
- In magnetic field: curves opposite to electron (same direction as alpha, positron)

**Identification in magnetic field:**
The radius of curvature $r$ for a relativistic particle:
$$p = qBr$$
where $p$ is momentum, $q$ is charge, $B$ is magnetic field strength. A proton of the same momentum as an electron curves much less (it has greater rigidity per charge at the same kinetic energy due to its higher mass).

### 3.5 Electron-Positron Pair Production

**Requirement:** A high-energy gamma ray (>1.022 MeV) near a nucleus converts into an electron-positron pair:
$$\gamma \rightarrow e^- + e^+$$

**Visual appearance:**
- Two tracks **emerging from a common point** with no incoming track (the photon is invisible)
- The two tracks curve in **opposite directions** in a magnetic field (this is the definitive signature)
- Tracks often asymmetric in energy (the gamma's energy is split unequally between e⁻ and e⁺)
- At low gamma energies (~1 MeV), the tracks are short and heavily curved
- At high energies (>100 MeV), tracks are nearly parallel before diverging

**To observe pair production:** Requires a hard gamma source (e.g., ⁶⁰Co at 1.17 and 1.33 MeV, or ²⁴Na, or cosmic-ray secondaries) and a high-Z converter plate (e.g., a thin lead sheet inside the chamber).

### 3.6 Electron Showers / Cascade Showers

High-energy electrons and photons initiate electromagnetic cascades:
- Electron emits bremsstrahlung photon → photon pair-produces → electrons radiate again
- Produces a **fan of tracks spreading from a single point**
- Visible with lead sheets inside the chamber
- The shower multiplicity grows logarithmically with initial particle energy

### 3.7 Recoil Nuclei from Neutron Scattering

When a fast neutron collides with a nucleus in the vapor, the recoiling nucleus produces a short, fat track:
- Proton recoils (from n + p scattering in hydrogen-rich vapor): short, thick tracks, star-shaped patterns
- Alpha or heavier nucleus recoils: very short (~1 mm), very dense blobs
- Neutrons are invisible; only the recoil nuclei are seen
- Source: neutron generators, Am-Be sources, or high-energy cosmic secondaries

### 3.8 Nuclear Interactions and Stars

Occasionally a cosmic ray (or neutron) undergoes a nuclear disintegration:
- Multiple tracks emerge from a single point — called a **"star"**
- Some tracks are short and fat (heavy fragments), others longer and thinner (protons, alpha particles)
- Rare in diffusion chambers; more common in emulsions or bubble chambers under particle beams

---

## 4. Radiation Sources

### 4.1 Americium-241 from Smoke Detectors

**Properties:**
- Decay mode: alpha (5.486 MeV), plus weak gamma at 59.5 keV
- Half-life: 432.6 years
- Activity in a typical US smoke detector: ~1 μCi (37 kBq) = ~0.29 μg of ²⁴¹Am
- The source is embedded in a gold foil, sealed inside an aluminum holder

**How to obtain:**
- Disassemble an ionization-type smoke detector (contains a small disc labeled with a radioactive symbol)
- The Am-241 source is the small metal button (~5 mm diameter) inside the ionization chamber
- **DO NOT extract the Am-241 from its sealed holder** — the sealed source is safe; loose powder is extremely hazardous
- Use the intact sealed button as your cloud chamber source

**Legal status (USA):**
- Possession for personal, educational, or scientific use is generally permitted under NRC regulations for these small, sealed consumer product sources
- Dismantling the smoke detector is legal; attempting to concentrate or process the americium is not under 10 CFR Part 30
- Many states have their own regulations; verify locally
- Disposal: most municipalities accept smoke detectors in household waste; some manufacturers have take-back programs

**Track appearance in chamber:**
- Uniform alpha tracks, all ~3–4 cm long at this energy in IPA vapor
- Source pointing upward into the sensitive zone produces a bouquet of tracks radiating from one spot
- The ~60 keV gamma from Am-241 is too low-energy to produce visible pair production; betas from decay daughters are weak

### 4.2 Thorium from Gas Mantle Lantern Mantles

**Properties:**
- Old-style camping lantern mantles (pre-1990s) contained ~1% ThO₂ by weight
- ²³²Th (α emitter, 4.083 MeV, half-life 14 billion years) with decay chain daughters:
  - ²²⁸Ra, ²²⁸Ac, ²²⁸Th, ²²⁴Ra, ²²⁰Rn (thoron), ²¹⁶Po, ²¹²Pb, ²¹²Bi, ²¹²Po, ²⁰⁸Pb
- Multiple alpha emitters in the chain = multiple distinct track lengths visible simultaneously

**Modern availability:**
- Most modern mantles use yttrium oxide (non-radioactive)
- Old thoriated mantles still circulate as surplus camping gear
- Identifiable because they glow brighter and with a slightly different color when burned

**Usage:**
- Place the ash of a burned mantle inside a small container inside the chamber
- Radon/thoron gas emitted from the thorium will diffuse into the sensitive zone
- Produces a spectacular display of multiple alpha track lengths from the decay chain

### 4.3 Radon and Thoron as Sources

**Radon-222 (²²²Rn):**
- Decay product of uranium-238 chain
- Half-life: 3.82 days, alpha emitter (5.49 MeV)
- Found naturally in basements and low areas (~48 Bq/m³ average US indoor)
- Simply leaving the cloud chamber open in a basement with elevated radon for 30 minutes can pre-charge the sensitive zone
- Radon daughters (²¹⁸Po, ²¹⁴Pb, ²¹⁴Bi, ²¹⁴Po) plate out on the walls and continue emitting alphas and betas

**Thoron-220 (²²⁰Rn):**
- From thorium-232 decay chain
- Half-life: 55.6 seconds
- Must be generated continuously from thorium source
- Present in air near burning thoriated mantles

### 4.4 Uranium Glass (Vaseline Glass)

- Glass made with 2–25% uranium oxide, fluoresces bright green under UV
- Emits alpha particles from the decay chain, plus very weak betas
- Can be crushed and placed inside the chamber, but alpha range limits visibility
- Primarily alpha tracks; very low activity per surface area compared to Am-241

### 4.5 Potassium-40 (⁴⁰K)

- Present in all living things; ⁴⁰K is 0.012% of natural potassium
- Decays by beta emission (89%, Emax = 1.31 MeV) and electron capture with gamma (10.7%, 1.46 MeV)
- A tablespoon of potassium chloride (NoSalt) contains ~15 Bq of ⁴⁰K
- Activity is low; expect occasional beta tracks rather than a shower

### 4.6 Strontium-90 / Yttrium-90 (⁹⁰Sr/⁹⁰Y)

- **Not legally obtainable** for most individuals without a radioactive material license
- Used in calibration sources for Geiger counters; some old equipment contains small sealed Sr-90 sources
- Beta emitter: Emax(Sr-90) = 0.546 MeV; daughter ⁹⁰Y: Emax = 2.28 MeV
- Would produce beautiful high-energy beta tracks

### 4.7 Background Cosmic Ray Sources (No Source Required)

Even without an artificial source, a cloud chamber will show:
- ~5–15 muon tracks per minute (long, ruler-straight)
- Occasional electron/positron secondaries
- Rare nuclear interactions ("stars")
- Environmental gamma/beta from natural background

This is the cleanest demonstration because tracks arise from deep space rather than a local source.

---

## 5. Track Physics and Quantitative Analysis

### 5.1 Track Length and Particle Energy

For alpha particles in air at standard conditions, the empirical range-energy relation (Bragg-Kleeman):

$$R = 0.31 \cdot E^{3/2} \quad \text{(cm, MeV, in air at STP)}$$

More precise tabulated values:

| Alpha energy (MeV) | Range in air (cm) | Source nuclide |
|---------------------|-------------------|----------------|
| 4.08 | 2.50 | ²³²Th |
| 4.78 | 3.16 | ²³⁸U |
| 5.30 | 3.84 | ²¹⁰Po |
| 5.49 | 4.05 | ²²²Rn |
| 5.486 | 4.03 | ²⁴¹Am |
| 6.00 | 4.69 | ²¹²Bi (part) |
| 7.69 | 7.00 | ²¹²Po |
| 8.78 | 8.57 | ²¹²Po (fast group) |

To correct for non-STP conditions and IPA vapor density differences:
$$R_{\text{medium}} = R_{\text{air}} \cdot \frac{\rho_{\text{air}}}{\rho_{\text{medium}}} \cdot \left(\frac{A_{\text{medium}}}{A_{\text{air}}}\right)^{1/3}$$

In practice, tracks in an IPA-vapor diffusion chamber are ~85–90% the length predicted for pure air, due to the higher stopping power of the IPA molecules.

### 5.2 Ionization Density and Track Width

The linear energy transfer (LET) is proportional to:
$$\text{LET} \propto \frac{z^2}{v^2}$$

Qualitative comparison:

| Particle | Charge z | Typical KE | LET (rel.) | Track appearance |
|----------|----------|------------|------------|-----------------|
| Muon | 1 | 3 GeV | 1× | Ultra-thin line |
| Electron | 1 | 1 MeV | ~5× | Thin, wiggly |
| Proton | 1 | 1 MeV | ~1000× | Thick |
| Alpha | 2 | 5 MeV | ~4000× | Very thick |

### 5.3 Bragg Peak

Near the end of a charged particle's range, $v$ decreases, so LET rises sharply — the **Bragg peak**. In cloud chambers this manifests as a track that is noticeably wider (denser droplets) at its endpoint compared to the beginning. This is especially pronounced in alpha tracks and is absent in muon/electron tracks (which don't stop in the chamber).

### 5.4 Multiple Coulomb Scattering

A particle traversing a thickness $x$ of material of radiation length $X_0$ acquires an angular deflection (RMS):

$$\theta_0 = \frac{13.6 \text{ MeV}}{\beta c p} z \sqrt{x/X_0} \left[1 + 0.038 \ln(x/X_0)\right]$$

- Heavy particles (muons, protons) scatter little → straight tracks
- Electrons scatter enormously → tortuous, kinked tracks
- This formula provides a way to estimate particle momentum from track straightness when $X_0$ is known

---

## 6. Magnetic Field Analysis and Momentum Measurement

### 6.1 Basic Principle

A charged particle in a magnetic field $\vec{B}$ follows a circular arc due to the Lorentz force. The radius of curvature:

$$r = \frac{p}{qB} = \frac{p}{0.3 B} \quad \text{(r in meters, p in GeV/c, B in Tesla)}$$

Or equivalently:
$$p \, [\text{MeV/c}] = 300 \cdot B \, [\text{T}] \cdot r \, [\text{m}]$$

### 6.2 Setting Up a Magnetic Field

**Permanent magnets:**
- Neodymium (NdFeB) magnets can produce ~0.1–0.3 T across a small gap
- Place two large magnets (e.g., 10 × 10 × 2 cm) above and below the chamber with opposite poles facing
- Field uniformity is poor with simple magnets; use a steel yoke to improve it
- At 0.2 T: a 100 MeV/c electron curves with $r \approx 1.7$ m — too straight to see in a small chamber
- A 10 MeV/c electron curves with $r \approx 17$ cm — visible in a 30 cm chamber

**Electromagnet:**
- More controllable; can be reversed to confirm particle charge sign
- Requires a DC power supply capable of high current
- Iron core coil with pole gap ~5 cm can achieve 0.5–1 T

### 6.3 Measuring Curvature from Photographs

**Sagitta method:** For a track of length $L$ (chord) with sagitta $s$ (maximum perpendicular displacement from the chord):

$$r = \frac{L^2}{8s} + \frac{s}{2} \approx \frac{L^2}{8s} \quad \text{for } s \ll L$$

Steps:
1. Photograph the track with a ruler or scale visible in the field of view.
2. Identify two endpoints and the midpoint of a track segment.
3. Measure $L$ (chord length) and $s$ (sagitta, perpendicular from midpoint to chord).
4. Calculate $r = L^2 / (8s)$.
5. Convert to momentum: $p = 300 \cdot B \cdot r$.

**Minimum detectable momentum** is limited by multiple scattering (which mimics curvature). For a track length $L$ in vapor of radiation length $X_0$:

$$\left(\frac{\delta p}{p}\right)_{\text{scatter}} \approx \frac{0.016}{B \cdot L} \sqrt{\frac{L}{X_0}}$$

### 6.4 Charge Sign Identification

In a known magnetic field direction (say $\vec{B}$ pointing up):
- If the particle moves to the right and curves upward → positive charge (by right-hand rule)
- If it curves downward → negative charge
- Pair production is confirmed when two tracks emerge from one point and curve in **opposite** directions

### 6.5 Mass Determination

If you can measure both momentum $p$ (from curvature) and velocity $v$ (from $dE/dx$, i.e., track density), the mass follows:

$$m = \frac{p}{v\gamma} = p \sqrt{\frac{1}{v^2} - \frac{1}{c^2}}$$

In practice, measuring $v$ from track ionization is qualitative, but the combination of track length (related to range, which depends on $m$ and $E$) and curvature can distinguish particles. This was how Anderson identified the positron (1932) and Street & Stevenson identified the muon (1937).

---

## 7. Photography and Imaging Techniques

### 7.1 Camera Settings

| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| Aperture | f/2.8–f/4 | Wide aperture for sensitivity; too wide → shallow depth of field, blurring tracks at edges |
| Shutter speed | 1/30 s – 1/4 s | Longer shutter = more tracks per frame; too long = blurred by airflows |
| ISO | 800–3200 | Higher ISO for dimly lit chambers; adds noise |
| Focus | Manual, set to sensitive zone | Fixed focus; autofocus fails on low-contrast tracks |
| White balance | Custom or daylight | LED illumination is typically warm; cool it digitally |

**Video mode:** Filming at 30–60 fps with a mirrorless camera or high-quality phone camera captures individual track events in motion, including the formation and dispersal of tracks. This is often more instructive than stills.

### 7.2 Lighting

- **Side illumination** at grazing angle is essential: light enters perpendicular to the viewing direction.
- **LED strip** (>1000 lm, 6500K daylight): cheap, effective, runs cool. Cut to length and tape inside the chamber wall.
- **Green laser line** (5–50 mW): extremely efficient, produces the brightest tracks. Caution with eye safety — use appropriate beam stops.
- A **dark background** (black painted walls, black felt on all internal surfaces except the floor) maximizes contrast.
- Avoid direct illumination from below or above — it scatters off the IPA vapor and washes out tracks.

### 7.3 Image Processing

Raw photographs can be enhanced:
- **Increase contrast and mid-tone brightness** in Lightroom / GIMP
- **Flatten the background** using a "dark frame subtraction": take a reference photo with no tracks, subtract it from all track photos to remove fixed illumination gradients
- For curvature measurements, apply grid overlays (draw calibration grid, photograph it with the same setup)
- For track length measurements, include a reference ruler in the field of view

**Software for digitizing tracks:**
- **ImageJ** (free): use the "segmented line" tool to trace tracks and measure length and curvature
- For 3D reconstruction (stereoscopic cameras), specialized physics analysis packages like ROOT can process track coordinates

### 7.4 Video Analysis

- Films taken at 30 fps can be slowed down to examine track development
- **Background frame subtraction** can increase track visibility
- **Python + OpenCV**: basic background subtraction on live webcam feed can automatically detect tracks and record events

---

## 8. Safety Considerations

### 8.1 Dry Ice Safety

- **Cryogenic burns:** Dry ice (solid CO₂, −78.5 °C) causes frostbite within seconds of skin contact. Always use insulated gloves or tongs.
- **Asphyxiation risk:** CO₂ gas sublimes continuously. Never use large quantities of dry ice in a small, unventilated space. Maintain room ventilation. CO₂ is denser than air and accumulates in low areas.
- **Container pressure:** Never store dry ice in a sealed, airtight container — pressure buildup can rupture it. Store in an insulated cooler with a loose lid.
- **Eye protection:** Recommended when handling dry ice.

### 8.2 Isopropanol (IPA) Safety

- **Flammable:** Flash point ~12 °C (54 °F). Keep away from open flames, sparks, and hot surfaces. Never operate the chamber near a gas stove or open flame.
- **Vapor inhalation:** IPA vapor is mildly toxic. Work in a ventilated area. The quantities used in a cloud chamber (5–20 mL) produce low vapor concentrations, but the setup should not be sealed in a breathing space for extended periods.
- **Skin irritant:** Prolonged skin contact causes dehydration of the skin. Wash hands after handling.
- **Disposal:** Small amounts can be allowed to evaporate outdoors; never pour down a drain in large quantities.

### 8.3 Radiation Source Safety

**Americium-241 sealed source (smoke detector):**
- The sealed Am-241 button is **safe to handle** as long as the seal is intact. Alpha particles cannot penetrate skin or the thin metal housing.
- **Do not break the seal, grind, or dissolve the source.** Inhaled or ingested Am-241 is extremely hazardous (biological half-life ~50 years in bone).
- The ~60 keV gamma from Am-241 is very weak; dose rate ~1 cm from the source is <0.1 μSv/h.
- Keep away from children. Store in a labeled container.
- Check local regulations; in most US states possession of intact sealed sources from consumer products is legal.

**Thorium (lantern mantles):**
- The ash is mildly radioactive and should not be inhaled or ingested. Work outdoors or in well-ventilated areas when burning old mantles.
- The main hazard is ingestion or inhalation of thorium dust.

**General radiation hygiene:**
- Never point a radiation source at people, especially the eyes.
- Wash hands after handling any radioactive source.
- Store sources labeled, away from food and living areas.
- Keep a log of your sources for safety accountability.

### 8.4 Electrical Safety

- High-voltage (50–200 V DC) clearing field: lethal if contacted directly. Use insulated wire, secure terminals, and do not touch internal components when powered.
- Electromagnets draw high current; use appropriate wire gauges, fuses, and cooling.

---

## 9. Historic Discoveries Made in Cloud Chambers

### 9.1 C.T.R. Wilson (1911–1912) — Cloud Chamber Invention

C.T.R. Wilson developed the expansion cloud chamber while studying cloud formation on Ben Nevis, Scotland. He observed that mist formed more readily along radiation tracks than in clean air. His 1912 paper showed the first visible alpha and beta particle tracks. He received the 1927 Nobel Prize in Physics.

### 9.2 Proton Discovery (Rutherford, 1919)

While Rutherford's 1919 proton discovery used ionization counters, subsequent cloud chamber observations of nitrogen transmutation (α + ¹⁴N → ¹⁷O + p) made proton tracks directly visible.

### 9.3 Positron Discovery — Carl D. Anderson (1932)

Anderson, using a cloud chamber with a 1.5 T magnetic field and a lead absorber plate, observed a particle with the mass of an electron but **positive charge**. He observed a track curving in the opposite direction to electrons. The particle lost energy passing through the lead plate, confirming it was going upward (the track curvature was greater above the plate after energy loss). This was the positron, the first observed antimatter particle, confirming Dirac's 1928 relativistic quantum theory. Anderson received the 1936 Nobel Prize.

### 9.4 Muon Discovery — Anderson and Neddermeyer (1936)

Also using a magnetic cloud chamber, Anderson noticed particles that were positively charged but curved far less than positrons for the same track density — they were too massive to be positrons. Street and Stevenson (1937) performed a quantitative analysis and determined the muon mass to be approximately 207 electron masses. For two decades it was thought to be Yukawa's nuclear force mediator (pion), but the muon turned out to be a "heavy electron" with no nuclear interactions — leading I.I. Rabi's famous quip: "Who ordered that?"

### 9.5 Pion Discovery (Powell, 1947 — Photographic Emulsions)

While pions were actually discovered in photographic emulsions rather than cloud chambers (emulsions have much higher stopping power), early cloud chamber observations also showed candidate tracks. Cecil Powell received the 1950 Nobel Prize.

### 9.6 Pair Production in Cloud Chambers (Blackett and Occhialini, 1933)

Using a coincidence-controlled cloud chamber triggered by Geiger–Müller tubes, Blackett and Occhialini obtained photographs of cosmic ray showers showing simultaneous electron-positron pair production and electromagnetic cascades in lead. Patrick Blackett received the 1948 Nobel Prize "for his development of the Wilson cloud chamber method, and his discoveries therewith in the fields of nuclear physics and cosmic radiation."

### 9.7 Lambda Baryon and Strange Particles (Rochester and Butler, 1947)

In a cloud chamber at Manchester, Rochester and Butler observed V-shaped track pairs arising from neutral particles decaying into two charged secondaries. One was the kaon (K⁰), the other the Λ baryon — particles with anomalously long lifetimes that suggested a new quantum number: strangeness. This opened the door to the particle zoo and eventually the quark model.

---

## 10. Advanced Experiments

### 10.1 Identifying Multiple Alpha Emitters

**Goal:** Measure the distinct track lengths from different alpha emitters in a thorium decay chain.

**Setup:** Thorium mantle ash as source, or radon from a basement environment.

**Expected tracks from ²³²Th decay chain:**
| Nuclide | Alpha energy (MeV) | Expected range in IPA cloud (cm) |
|---------|-------------------|----------------------------------|
| ²³²Th | 4.08 | ~2.2 |
| ²²⁸Th | 5.42 | ~3.8 |
| ²²⁴Ra | 5.68 | ~4.1 |
| ²²⁰Rn | 6.29 | ~4.8 |
| ²¹⁶Po | 6.78 | ~5.4 |
| ²¹²Po | 8.78 | ~7.5 |

**Analysis:** Photograph many alpha tracks. Measure track lengths. Produce a histogram. The peaks should correspond to the known alpha energies, allowing isotope identification.

### 10.2 Cosmic Ray Muon Rate vs. Altitude / Angle

**Goal:** Measure the directional and energy distribution of cosmic ray muons.

**Method:**
1. Count muon tracks per unit time.
2. Vary the orientation of the chamber (horizontal vs. vertical sensitive zone).
3. Muons predominantly arrive from above (downward-going), so a vertical chamber orientation (tracks mostly crossing the width) will show more muons than a horizontal one (tracks crossing the depth).
4. The flux scales approximately as $\cos^2\theta$ for low-energy muons ($\theta$ = zenith angle).

**Expected rate:** ~1 muon/cm²/minute at sea level.

### 10.3 Pair Production with Lead Converter

**Goal:** Observe electron-positron pair production in a magnetic field.

**Setup:**
1. Position a 1–3 mm thick lead plate horizontally inside the chamber.
2. Use a hard gamma source (⁶⁰Co if accessible under license) or rely on high-energy cosmic-ray photons.
3. Apply a vertical magnetic field (>0.1 T) across the chamber.
4. Photograph or video the region just below the lead plate.

**What to look for:** "V"-shaped events where two thin tracks emerge from the bottom of the lead, curving in opposite directions in the magnetic field.

### 10.4 Muon Decay Observation

**Goal:** Observe a stopped muon decaying to an electron.

**Challenge:** Muons at sea level typically have too much energy to stop in the shallow (~2–3 cm) sensitive zone of a diffusion chamber.

**Method:** Use a thicker sensitive zone (~5–8 cm using Peltier cooling for better gradient control). A fraction of lower-energy muons will stop. The signature:
1. A long straight track that **terminates abruptly** within the sensitive zone (muon stops).
2. After ~2.2 μs (muon mean lifetime), a short spiral track emerges from the stop point (the Michel electron from decay).
3. This requires video recording at high frame rate or triggered photography.

The Michel electron has energy up to $m_\mu/2 \approx 53$ MeV and will curl tightly in a magnetic field.

**Expected rate:** With a 30×30 cm chamber, a stopped muon producing an observable decay is a rare event (~several per week).

### 10.5 Constructing a Differential Cloud Chamber (Bubble-Jet Cooling)

For extreme hobbyists: cool the bottom of the chamber to −60 to −70 °C using a multi-stage Peltier system. This produces a deeper, more stable sensitive zone and allows ethanol (which gives clearer tracks than IPA) as the working fluid. Sensitivity can be improved enough to make cosmic-ray proton tracks occasionally visible, identified by their greater ionization density compared to muons.

---

## 11. Further Reading

### Textbooks

- **Frisch, O.R. (1965)** — *Tracks in Cloud Chambers* — classic visual guide to particle track interpretation
- **Krane, K.S. (1988)** — *Introductory Nuclear Physics* (Wiley) — Chapters 5–6 cover alpha/beta decay and detection
- **Leo, W.R. (1994)** — *Techniques for Nuclear and Particle Physics Experiments* (Springer) — comprehensive treatment of ionization detectors and track analysis
- **Tipler, P. & Llewellyn, R. (2002)** — *Modern Physics*, 4th ed. — accessible introduction

### Papers

- Wilson, C.T.R. (1912). "On an expansion apparatus for making visible the tracks of ionizing particles in gases" — *Proc. Royal Society A*, 87: 277–292
- Anderson, C.D. (1933). "The Positive Electron" — *Physical Review*, 43: 491
- Neddermeyer, S. & Anderson, C.D. (1937). "Note on the Nature of Cosmic-Ray Particles" — *Physical Review*, 51: 884–886
- Street, J. & Stevenson, E.C. (1937). "New Evidence for the Existence of a Particle Intermediate Between the Proton and Electron" — *Physical Review*, 52: 1003
- Blackett, P.M.S. & Occhialini, G. (1933). "Some Photographs of the Tracks of Penetrating Radiation" — *Proc. Royal Society A*, 139: 699

### Online Resources

- **CERN's S'Cool LAB**: Educational resources on cloud chambers used in particle physics outreach
- **DESY Zeuthen Cloud Chamber** educational guide
- **Symmetry Magazine** (Fermilab/SLAC): articles on cosmic ray detection and cloud chambers for outreach
- **HyperPhysics** (Georgia State University): interactive particle physics reference

### DIY Build Resources

- The "Instructables" and "Hack-a-Day" communities maintain many cloud chamber build guides
- MIT OpenCourseWare 8.13–8.14 (Junior Lab): includes quantitative particle identification exercises

---

*This guide is intended for educational and scientific purposes. Always follow applicable regulations regarding radioactive materials in your jurisdiction. Consult with your local radiation safety officer if you are uncertain about any source's regulatory status.*
