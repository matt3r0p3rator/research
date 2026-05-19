# DIY Cloud Chamber: Complete Builder's Guide
*Research date: May 19, 2026*

---

## Table of Contents
1. [How a Cloud Chamber Works](#1-how-a-cloud-chamber-works)
2. [Design A — Dry Ice Diffusion Chamber](#2-design-a--dry-ice-diffusion-chamber)
3. [Design B — Peltier-Cooled Diffusion Chamber](#3-design-b--peltier-cooled-diffusion-chamber)
4. [Critical Dimensions](#4-critical-dimensions)
5. [Lighting: Angle, Type, and Placement](#5-lighting-angle-type-and-placement)
6. [The Electric Field ("Ion Scrubber") Trick](#6-the-electric-field-ion-scrubber-trick)
7. [Common Mistakes and Troubleshooting](#7-common-mistakes-and-troubleshooting)
8. [Where to Buy Dry Ice and Typical Cost](#8-where-to-buy-dry-ice-and-typical-cost)
9. [Radiation Sources to Use](#9-radiation-sources-to-use)
10. [Total Cost Estimates](#10-total-cost-estimates)

---

## 1. How a Cloud Chamber Works

A **diffusion cloud chamber** exploits a steep temperature gradient to create a thin layer of *supersaturated* alcohol vapor just above a very cold plate. When an ionizing particle (alpha, beta, muon, proton) passes through this layer, it strips electrons from air molecules, leaving a trail of ion pairs. These ions act as condensation nuclei — tiny alcohol droplets form around them, making the particle's path visible as a white, misty track that persists for 1–5 seconds before settling.

### What You Can See
| Track Type | Particle | Appearance |
|---|---|---|
| Short, thick, straight | Alpha (α) | 2–5 cm, like a fat white rope |
| Long, thin, wispy, curling | Beta (β / electron) | May spiral from magnetic deflection |
| Long, nearly straight | Muon (cosmic ray) | Crosses entire chamber |
| Short, branched | Proton recoils | Uncommon without a strong source |

**Minimum cold plate temperature:** −26 °C (−15 °F). In practice, aim for −30 °C to −50 °C for reliable tracks.

---

## 2. Design A — Dry Ice Diffusion Chamber

### Overview
The simplest and cheapest approach. Dry ice (solid CO₂, −78.5 °C) directly chills the bottom aluminum plate. The whole build can be done in 1–2 hours. Major limitation: dry ice sublimes in ~1–3 hours per session, so there is a recurring consumable cost.

### Bill of Materials

| # | Item | Specification | Where to Buy | Approx. Cost |
|---|---|---|---|---|
| 1 | **Clear chamber enclosure** | 10-gallon glass aquarium (50 × 25 × 30 cm) **or** clear acrylic box (30 × 25 × 15 cm interior, 3–6 mm walls) | Pet/hardware store, Amazon | $15–40 |
| 2 | **Aluminum cold plate** | 6061 alloy, 3–6 mm thick, sized to fit bottom of aquarium (e.g., 45 × 20 cm); edges filed smooth | Metal supplier, Amazon, hardware store | $10–20 |
| 3 | **Black felt or velvet** | Dense, short-pile; cut to line the interior bottom and optionally walls | Fabric/craft store | $5–10 |
| 4 | **Felt wicking strip** | 1.5–2.5 cm wide strip to line the top interior perimeter | Fabric/craft store | included above |
| 5 | **Isopropyl alcohol, 99%** | Must be ≥99% purity — 70% and 91% do NOT work reliably | Hardware store, Amazon, pharmacy | $10–18 (500 mL) |
| 6 | **Dry ice** | 3–8 lbs per session (blocks, not pellets if possible) | Grocery stores, see §8 | $5–20/session |
| 7 | **Styrofoam cooler or dry ice tray** | To hold dry ice beneath the plate; 6-qt camping cooler works well | Grocery / hardware store | $5–15 |
| 8 | **LED strip light or flashlight** | Bright, cool-white (5000–6500 K); LED strip preferred (even illumination) | Amazon, hardware | $8–20 |
| 9 | **Black matte spray paint** | If not using felt on bottom plate | Hardware store | $5 |
| 10 | **Rubber or foam gasket** *(optional)* | Closed-cell foam weatherstripping; seals lid to reduce air currents inside | Hardware store | $5–8 |
| 11 | **Cryogenic/insulating gloves** | For safe dry ice handling | Amazon, safety supply | $10–20 |
| 12 | **Thermal conductive pad or paste** *(optional)* | Placed between dry ice and aluminum plate to improve contact | Amazon | $5–10 |

**Total one-time cost: ~$68–156** (not counting dry ice, which is recurring)

---

### Step-by-Step Construction: Dry Ice Version

#### Step 1 — Prepare the Chamber

1. **Aquarium version:** Use a standard rectangular 10-gallon aquarium laid on its side so the opening faces you (i.e., one long glass wall becomes the bottom). The aluminum plate slides in to rest on the glass "floor" (now a wall).  
   **Acrylic box version:** Purchase or fabricate a box with an open top or removable lid, at minimum 30 × 20 cm interior footprint and 12–15 cm tall.

2. **Paint or line the bottom.** The cold plate and the floor you'll view through must be **matte black**. Options:
   - Glue black velvet to the top face of the aluminum plate (the side facing into the chamber).
   - Or spray the plate with 2–3 coats of matte black paint and let cure completely.
   - The walls can remain clear or be left uncoated.

3. **Apply the felt strip wicking source.** Cut felt into 2 cm wide strips. Glue (contact cement or silicone RTV) these strips around the **upper interior perimeter** of the chamber walls, approximately 1–2 cm from the top edge. This is the alcohol reservoir — alcohol evaporates from here and falls downward.

#### Step 2 — Seal and Prep the Lid

If using an aquarium, cut a piece of plywood or plexiglass for the lid. Apply a strip of closed-cell foam weatherstripping around the perimeter so the lid seals moderately well (not airtight, but reducing drafts). Leave a small vent hole (~3 mm) to prevent pressure buildup.

#### Step 3 — Saturate the Felt Wicking Strip

Using a syringe or small squeeze bottle, apply **99% isopropyl alcohol** to the felt strip until saturated. Then blot lightly — the felt should be damp and holding liquid, but not dripping. A good starting amount is **15–25 mL** total for a 30 × 20 cm strip. Excess alcohol causes a "rainstorm" that obscures tracks; too little and no vapor is produced.

#### Step 4 — Add Dry Ice

1. Place 3–5 lbs of dry ice into the styrofoam cooler. Break it into flat slabs rather than chunks if possible — better thermal contact.
2. **Lay the aluminum cold plate on top of the dry ice.** It will rapidly cool. Wait 2–3 minutes for it to equalize.
3. If the plate doesn't sit flat (chunks vs. slabs), use a thin layer of isopropyl alcohol or sand to flatten contact; the IPA freezes and improves contact.
4. Lower the chamber assembly onto the cold plate so the plate forms the floor.

#### Step 5 — Establish the Temperature Gradient

Put the lid on. Wait **5–10 minutes** for the gradient to develop. You need:
- Top (felt level): ~20–25 °C (room temperature)
- Bottom (plate): ~ −30 °C to −50 °C
- Sensitive zone: 5–25 mm above the plate, where vapor is supersaturated

During this time, set up your light source.

#### Step 6 — Illuminate and Observe

See §5 for lighting details. Once the gradient is established, darken the room, shine the light, and watch for tracks. The first tracks usually appear after 5–10 minutes of cooling; the chamber is "at its best" from roughly 10–60 minutes after placing on dry ice.

---

## 3. Design B — Peltier-Cooled Diffusion Chamber

### Overview
A Peltier (thermoelectric cooler, TEC) chamber runs continuously on wall power, no dry ice needed. The challenge: a single TEC module (ΔT_max ≈ 68 °C at zero load) will only cool a plate to about −25 °C to −35 °C in practice, right at the minimum threshold. For reliable, impressive tracks, a **two-stage (cascaded) TEC system** reaching −45 °C to −65 °C is recommended.

### How Many TECs and Which Models

#### Option 1 — Single-Stage (Budget, Marginal Performance)
- **2× TEC1-12706** (6 A, 12 V, 57 W) or **2× TEC1-12710** (10 A, 12 V, 92 W) wired in parallel, sandwiched between the cold aluminum plate (top) and a large heat sink (bottom).
- Cold side can reach −25 °C to −35 °C if the heat sink is adequate.
- Expect faint tracks; works at altitude (thinner air = more cosmic rays) or with a strong radioactive source.

#### Option 2 — Two-Stage Cascade (Recommended)
Stage arrangement from bottom to top:
1. **Heat sink + fan** (removes all heat to ambient)
2. **Stage 1 TEC (hot):** 2× **TEC1-12710** in parallel (10 A each, run at 12 V)
3. **Intermediate copper/aluminum spreader plate** (8–10 mm thick)
4. **Stage 2 TEC (cold):** 1× **TEC1-12706** or **TEC1-12705** run at reduced voltage (8–10 V) to optimize COP
5. **Cold plate** (aluminum, 6061, 6–10 mm thick, polished surface)

This stack reaches approximately **−45 °C to −65 °C** on the cold plate with good heat sinking, comfortably in the "excellent track visibility" range.

### Bill of Materials — Peltier Version

| # | Item | Specification / Model | Approx. Cost |
|---|---|---|---|
| 1 | **TEC modules (Stage 1)** | 2× TEC1-12710 (10 A, 12 V, 92 W, 40×40 mm) | $10–18 (pair) |
| 2 | **TEC module (Stage 2)** | 1× TEC1-12706 (6 A, 12 V, 57 W, 40×40 mm) or TEC1-12705 | $5–10 |
| 3 | **CPU heat sink** | Large tower-style; e.g., Noctua NH-D15 or equivalent (~0.10 °C/W); minimum 140 mm fan | $30–80 |
| 4 | **Heat sink fan** | 120–140 mm, 12 V DC, ≥1500 RPM; already included if using CPU heat sink | $0–15 |
| 5 | **Aluminum cold plate** | 6061-T6, ~80×80×10 mm, lapped flat; sized to match TEC footprint | $10–20 |
| 6 | **Thermal paste** | Arctic Silver 5 or Kryonaut; ~3 g tube | $6–12 |
| 7 | **Power supply** | ATX desktop PC PSU (12 V rail: ≥20 A, 5 V rail for fan) **or** dedicated 12 V/20 A DC supply | $15–40 |
| 8 | **Chamber enclosure** | Same as Design A: clear acrylic box or aquarium, 30×25×15 cm | $15–40 |
| 9 | **Black felt/velvet liner** | Same as Design A | $5–10 |
| 10 | **Felt wicking strip** | Same as Design A | included |
| 11 | **Isopropyl alcohol, 99%** | Same as Design A | $10–18 |
| 12 | **LED strip light** | Bright white LED strip, 5000–6500 K | $8–20 |
| 13 | **Temperature controller** *(optional)* | STC-1000 or similar; monitors cold plate temp, adjusts fan speed | $10–20 |
| 14 | **Thermistor or thermocouple** | To monitor cold plate temperature in real time | $5–10 |
| 15 | **Rubber gasket/weatherstripping** | Same as Design A | $5–8 |
| 16 | **Mounting hardware, wiring, zip ties** | 16 AWG wire, spade connectors, small screws | $5–10 |

**Total one-time cost: ~$144–331** (no recurring costs once built)

---

### Step-by-Step Construction: Peltier Version

#### Step 1 — Assemble the TEC Stack

1. **Clean all mating surfaces.** Polish or lap the heat sink base, both faces of the intermediate plate, both TEC modules, and the cold plate with 400–600 grit sandpaper, then 1500 grit. All surfaces should be as flat as possible.
2. **Apply Arctic Silver or Kryonaut sparingly.** Spread a thin uniform film on each mating surface (not pea-sized blobs — spread flat).
3. **Layer the stack (bottom to top):**
   - Heat sink (fins facing down, fan attached)
   - 2× Stage 1 TEC (cold sides up)
   - Intermediate copper spreader plate (10 mm thick, same footprint as TECs or slightly larger)
   - 1× Stage 2 TEC (cold side up)
   - Cold aluminum plate (10 mm thick, polished top surface)
4. **Clamp or bolt the stack.** Use M3 or M4 stainless bolts through all layers. Torque evenly; 2–3 N·m is typical. Do not overtighten — TEC ceramics are brittle.
5. **Insulate the cold plate edges.** Wrap sides of the cold plate and Stage 2 TEC with 10–15 mm of closed-cell foam or neoprene. This prevents condensation and reduces heat leakback from the sides.

#### Step 2 — Wiring

Wire for 2-stage operation:
- Stage 1 TECs (in parallel): connect both red (+) wires together to the 12 V rail; both black (−) wires to ground. They draw ~18–20 A combined — ensure wiring is 14 AWG minimum for this run.
- Stage 2 TEC: connect to a separate DC-DC buck converter set to 8–10 V (or a separate 12 V source at reduced duty cycle via PWM). Running Stage 2 at full 12 V reduces its COP and can actually deliver less cooling at the cold plate.
- Heat sink fan: 12 V from the power supply.
- All grounds common.

#### Step 3 — Test the Thermal Stack (Dry Run)

Before installing the chamber, power the stack and measure the cold plate temperature every 2 minutes with a thermocouple. You should see:
- After 5 min: ~0 to −10 °C
- After 15 min: −25 to −40 °C (two-stage, good heat sink)
- After 30 min (steady state): −40 to −65 °C

If the heat sink is warm to the touch (not hot) and the cold plate is below −30 °C, you're ready. If the heat sink is too hot to touch, you need more thermal dissipation (bigger heat sink, more fan, or water cooling).

#### Step 4 — Install Chamber on Cold Plate

1. **Line the chamber bottom.** Glue black velvet to the top (inside-facing) surface of the cold plate. It should be flush with the interior floor.
2. **Seal the chamber base.** Apply a bead of silicone RTV or closed-cell foam weatherstripping around the cold plate perimeter. Set the chamber enclosure on top. Allow to cure if using RTV.
3. **Apply felt wicking strip and saturate with 99% IPA** (same as Design A, Step 3).
4. **Place lid with small vent hole.**

#### Step 5 — Power Up and Wait

Power on the TEC stack. The chamber will cool toward operating temperature over 15–30 minutes. Monitor cold plate temp with the thermocouple. Do not add alcohol until the plate is below −25 °C. Optimal tracks appear when the plate is −35 °C or colder.

#### Step 6 — Illuminate and Observe

Same as Design A, Step 6. Since the Peltier chamber can run all day, you have unlimited observation time.

---

## 4. Critical Dimensions

### Chamber Size
- **Minimum viable interior:** 20 × 15 cm footprint, 10 cm tall
- **Recommended:** 30 × 25 cm footprint, 12–15 cm tall
- **Large/display:** 45 × 30 cm footprint, 15–20 cm tall
- Larger chambers produce more visible tracks simultaneously (more cosmic ray muons per second) and allow the sensitive zone to extend further.

### Felt Strip (Alcohol Wicking Strip)
- **Width:** 1.5–2.5 cm (1 cm is too thin; 3+ cm can deliver too much vapor)
- **Position:** At the **top interior wall**, around the full perimeter or just the two long walls
- **Distance from cold plate:** As much as possible — full interior height. A 12–15 cm gradient height works well.
- **Material:** Dense felt (craft felt, not thin fashion felt). Some builders prefer 3–5 mm open-cell foam as it holds more alcohol.

### Alcohol Saturation
- **Amount per session:** 15–30 mL for a 30 × 20 cm chamber
- **Criterion:** Felt should be fully saturated but **not dripping**. After applying, wait 30 seconds; if large drops fall from the felt, blot with a paper towel until droplets stop.
- **Replenish:** If running for more than ~45 minutes (Peltier version), re-apply 5–10 mL when tracks become faint. The felt dries out over time.

### Cold Plate Temperature Targets
| Cold Plate Temp | Track Visibility |
|---|---|
| −20 °C to −26 °C | Marginal; faint tracks only with strong sources |
| −27 °C to −35 °C | Acceptable; cosmic ray muons visible |
| −36 °C to −50 °C | Good; alpha and beta tracks clearly visible |
| −51 °C to −78 °C | Excellent; highly active; dry ice range |

---

## 5. Lighting: Angle, Type, and Placement

Lighting is just as critical as temperature. The wrong lighting makes tracks invisible even in a perfectly functioning chamber.

### Geometry
- **Angle:** The light must be **nearly horizontal** — 5–15° above the plane of the cold plate. This is called **grazing-angle illumination** or side lighting. Overhead lighting does not work.
- **Direction:** From one side of the chamber, aimed at the **sensitive zone** (the 1–3 cm layer just above the cold plate).
- **Distance:** 10–30 cm from the side wall works well. Closer = brighter illumination.

### Light Source Options
| Source | Pros | Cons |
|---|---|---|
| **LED strip (cool white, 6000 K)** | Even, continuous illumination; easy to position along one wall | Need to aim precisely at sensitive zone |
| **High-brightness LED flashlight** (Convoy S2+, Fenix, etc.) | Very concentrated beam; can tune the angle precisely | Must hold or clamp in position |
| **Halogen spotlight/flashlight** | Strong output, good spectral range | Heats up; limited battery life |
| **Laser pointer (green, 532 nm)** | Extremely high contrast; very cool effect | Can damage eyes; need diffusion to spread beam |

### Practical Setup
1. Use a **bright LED strip** (e.g., 5630 SMD, 12 V) or a flashlight rated ≥500 lumens.
2. Mount it **outside** the chamber, pressed against one side wall (the glass/acrylic transmits light well).
3. Tilt it **downward 5–10°** so the beam sweeps across the cold plate surface and sensitive zone.
4. Completely darken the room; ambient light kills contrast.
5. Allow your eyes to dark-adapt for ~2 minutes before looking. Tracks are white/gray against the black background.
6. Photographing: use a camera set to ISO 800–3200, f/2.8–f/4, 1/60–1/30 s. A dark room and the chamber lit only by the side light gives excellent results.

---

## 6. The Electric Field ("Ion Scrubber") Trick

### What It Is
A high-voltage electrode suspended above the cold plate creates a moderate electric field (typically 1–5 kV at the electrode, corresponding to field strengths of 100–500 V/cm across the chamber). This field serves two roles:

1. **Ion clearing:** In the absence of an electric field, residual ion pairs created by previous particle tracks linger in the chamber. These cause "background" condensation rain that fills the chamber with haze. The field sweeps these ions away quickly, clearing the sensitive zone between tracks.

2. **Background rain suppression:** Alcohol droplets falling from the supersaturated upper zone carry charge. The field pushes them to the walls, keeping the field of view clean.

The net effect: **tracks appear sharper, last longer, and are easier to distinguish from noise.**

### Is It Necessary?
- **No** — you will see tracks without it. Many successful beginner chambers have no electric field.
- **Yes, if you want clean images or video** — it dramatically improves visual clarity, especially with a strong source producing many tracks.
- It is particularly helpful for the Peltier version, where the temperature gradient is shallower and background fog more persistent.

### How to Implement It

**Materials:**
- Aluminum foil plate or screen (~80% of interior footprint), cut to fit 8–10 cm above the cold plate
- High-voltage DC source: 1,000–5,000 V
  - Budget option: negative ion generator module (sells for $5–15 on AliExpress/eBay; outputs ~3–5 kV)
  - Better option: ZVS flyback driver + Cockcroft-Walton multiplier (adjustable; well-documented online)
  - Proper option: Benchtop HV supply
- **Safety resistor:** 10–50 MΩ, 2 W, in series. This limits fault current to under 100 µA even if you touch the electrode — uncomfortable but non-lethal.
- Insulated standoffs (nylon or acrylic) to support the plate inside the chamber

**Wiring:**
- Connect the **positive** terminal of the HV source to the electrode plate (positive ions are swept down toward the grounded cold plate).
- Connect the **negative** terminal and cold plate to earth ground.
- The series resistor goes between the HV supply positive and the electrode.

**Typical settings:**
- Electrode voltage: +1 kV to +4.6 kV (experimentally documented cloud chamber images use ~4.6 kV)
- If using an ion generator module, output is typically fixed at 3–6 kV negative; in that case, reverse polarity (negative electrode, positive plate) — still works for ion clearing.

**Safety notes:**
- Always use the series safety resistor. Without it, the electrode can store significant energy (E = ½CV²).
- Discharge the electrode before opening the chamber (touch a grounded wire to the electrode through the access port).
- Never omit the resistor if children are present.

---

## 7. Common Mistakes and Troubleshooting

### No Tracks Visible at All

| Symptom | Likely Cause | Fix |
|---|---|---|
| No tracks after 20+ minutes | Cold plate not cold enough | Check temp with thermocouple; add more dry ice or improve TEC stack |
| No tracks, plate is cold | 70% or 91% IPA used | Replace with 99% IPA; anything below 95% is unreliable |
| No tracks, everything correct | Felt is dry | Re-saturate with alcohol |
| No tracks, alcohol rain falling | Too much alcohol | Blot felt; reduce to damp-not-dripping |
| Faint fog but no tracks | Room is too bright | Darken the room completely |
| Can't see anything | Light angle wrong | Move light to horizontal, grazing angle |

### Poor or Smeared Tracks

| Symptom | Likely Cause | Fix |
|---|---|---|
| Tracks blur and disappear instantly | Air currents inside chamber | Seal lid better; move away from HVAC vents |
| Whole chamber fills with fog | Plate too warm, or too much IPA | Wait longer; reduce IPA |
| Tracks curve strangely | Uneven cold plate (not flat) | Replace or lap the plate flat |
| "Streamers" from one spot | Radioactive source producing alphas | That's correct — point the source elsewhere for varied tracks |

### Dry Ice Specific

| Symptom | Fix |
|---|---|
| Dry ice sublimes in < 30 min | Use larger pieces; insulate with styrofoam; use more |
| Plate doesn't get cold enough | Ensure direct dry-ice-to-plate contact; flatten the dry ice surface with a small mallet |
| Condensation frost on plate bottom | Adds insulation; wipe surface before placing plate; work quickly |
| Tracks only at edges | Aluminum plate not sitting flush; warped plate |

### Peltier Specific

| Symptom | Fix |
|---|---|
| Cold plate won't go below −20 °C | Heat sink inadequate; add a second fan; clean thermal paste joints |
| TEC module gets very hot and fails | Thermal paste applied incorrectly; hot side not sinking heat; reduce Stage 2 voltage |
| Cold plate has frost but no tracks | Temperature gradient not steep enough; increase Stage 1 power |
| TEC modules fail repeatedly | Thermal cycling stress; use slow ramp-up; ensure clamping is even |

### Safety Notes
- Dry ice: **never** handle with bare skin; always use insulating gloves. **Never** seal dry ice in a fully airtight container (CO₂ buildup, pressure risk). Work in a ventilated room.
- 99% IPA: flammable. Keep away from open flames. Have ventilation.
- Electric field: treat the ion scrubber with caution; always use the series safety resistor.

---

## 8. Where to Buy Dry Ice and Typical Cost

### Retail Locations (USA)
Dry ice is sold by weight at many grocery chains. Call ahead to confirm availability, as not all stores carry it and supply can be inconsistent.

| Retailer | Typical Form | Typical Price (2025–2026) |
|---|---|---|
| **Walmart** (Marketside Dry Ice) | 1–5 lb bags | ~$1.50–$2.00/lb |
| **Kroger / King Soopers / Smith's** | Blocks or bags | ~$1.50–$2.50/lb |
| **Safeway / Albertsons** | 1 lb and 5 lb bags | ~$2.00–$3.00/lb |
| **Publix** | Blocks | ~$2.00–$3.00/lb |
| **Meijer** | Blocks | ~$1.50–$2.00/lb |
| **Restaurant supply stores** (Gordon Food, US Foods) | 50 lb blocks | ~$0.75–$1.25/lb |
| **Dry ice delivery services** (Airgas, Continental Carbonic) | 50–100 lb blocks | ~$0.60–$1.00/lb (delivery fee) |

### How Much You Need
- **One 1–2 hour cloud chamber session:** 3–6 lbs is sufficient.
- Buy a 5 lb bag and you'll have a margin for setup time.
- At $2/lb × 5 lb = **~$10 per session** at retail.

### Tips for Purchasing
- Always purchase dry ice **on the day** of your experiment. It sublimates at ~5–10 lbs per 24 hours in a typical styrofoam cooler.
- In the USA, Walmart's freezer aisle near customer service is the most reliable source nationwide.
- Carry it in a styrofoam cooler; do not seal the cooler lid completely in a car (CO₂ buildup).

---

## 9. Radiation Sources to Use

You don't need a special source — cosmic rays are everywhere.

| Source | What You See | Acquisition |
|---|---|---|
| **Cosmic ray muons** (ambient) | Long, straight tracks crossing the full chamber; ~1 per cm²/min at sea level; more at altitude | No purchase needed |
| **Americium-241** (from smoke detectors) | Short, thick, straight alpha tracks; very reliable; ~3 cm range | Old ionization smoke detectors (check local regulations on disassembly) |
| **Thorite mineral / thoriated lantern mantles** | Alpha, beta, and occasional gamma tracks | Online mineral suppliers; old camping lantern mantles (thoriated type) |
| **Uranium glass** | Multiple track types | Antique stores, eBay |
| **Radium watch dial** | Multiple types, very active | Antique dealers; handle with care; check local regulations |
| **Potassium-40** (salt substitute) | Faint beta tracks | Any grocery (NoSalt, Nu-Salt); very weak, needs excellent chamber |

> **Legal note:** Americium-241 in smoke detectors is legal to own in the USA; intentionally releasing the source material is prohibited. Most DIY builders carefully crack open the ionization chamber to expose the tiny 0.9 µCi Am-241 disk.

---

## 10. Total Cost Estimates

### Design A — Dry Ice Version

| Category | Budget Build | Full Build |
|---|---|---|
| 10-gal aquarium or acrylic box | $20 | $40 |
| Aluminum cold plate (6061) | $12 | $20 |
| Black felt / velvet | $6 | $10 |
| 99% IPA (500 mL) | $10 | $15 |
| LED flashlight (500+ lm) or LED strip | $10 | $20 |
| Styrofoam cooler | $5 | $12 |
| Insulating gloves, misc hardware | $8 | $15 |
| Rubber gasket | — | $8 |
| Black matte spray paint | $5 | $5 |
| **One-time subtotal** | **~$76** | **~$145** |
| Dry ice per session (5 lbs @ $2/lb) | $10 | $10 |
| **First session total** | **~$86** | **~$155** |

### Design B — Peltier Version (Two-Stage Cascade)

| Category | Budget Build | Full Build |
|---|---|---|
| 2× TEC1-12710 (Stage 1) | $12 | $18 |
| 1× TEC1-12706 (Stage 2) | $6 | $10 |
| CPU heat sink + 120mm fan | $20 | $60 |
| Aluminum cold plate + intermediate plate | $15 | $30 |
| Arctic Silver / Kryonaut paste | $6 | $12 |
| Power supply (ATX salvage or 12V/20A) | $15 | $45 |
| Chamber enclosure | $20 | $40 |
| Black felt / velvet | $6 | $10 |
| 99% IPA (500 mL) | $10 | $15 |
| LED strip light | $8 | $20 |
| DC-DC buck converter (Stage 2 voltage) | $5 | $10 |
| Thermocouple + thermometer | $8 | $15 |
| Misc (wiring, hardware, gasket) | $10 | $20 |
| **One-time total** | **~$141** | **~$305** |
| Recurring costs | **$0** | **$0** |

### Head-to-Head Comparison

| Criterion | Dry Ice | Peltier (2-stage) |
|---|---|---|
| **First-session total** | $86–155 | $141–305 |
| **Long-term cost** | +$10–20 per session | None (electricity only) |
| **Cold plate temp** | −50 to −78 °C | −35 to −65 °C |
| **Track visibility** | Excellent | Good to excellent |
| **Session duration** | 1–3 hours (dry ice limited) | Unlimited |
| **Setup time** | 10–15 min | 20–40 min (first time); 5 min thereafter |
| **Portability** | High (no mains power) | Low (requires AC power) |
| **Complexity** | Very low | Moderate |
| **Best for** | Occasional demos, beginners | Permanent display, frequent use |

---

## Quick-Start Checklist (Dry Ice Version)

- [ ] 10-gal aquarium or acrylic box with black-velvet bottom
- [ ] Aluminum plate matching interior footprint, velvet on top
- [ ] Felt strip glued at top interior, saturated with 99% IPA
- [ ] 5 lbs dry ice in styrofoam cooler, plate resting on dry ice
- [ ] Chamber placed on plate; lid on with small vent hole
- [ ] Bright LED flashlight clamped to side, aimed nearly horizontally at plate surface
- [ ] Room lights off; wait 8–10 minutes
- [ ] Watch for white, misty tracks drifting downward — cosmic ray muons cross the whole chamber in a fraction of a second, leaving straight persistent trails

---

*Note: All costs are approximate 2025–2026 US retail prices. Always handle dry ice with insulating gloves, work in ventilated spaces, and use the safety resistor with any high-voltage ion scrubber circuit.*
