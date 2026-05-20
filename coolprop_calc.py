"""
CoolProp Thermodynamic Calculator
----------------------------------
Interactive tool for fluid property lookups, refrigeration cycle analysis,
and general thermodynamic calculations.
"""

import sys
import math
import numpy as np
from CoolProp.CoolProp import PropsSI, get_fluid_param_string, FluidsList
import CoolProp.CoolProp as CP

# ── Property metadata ─────────────────────────────────────────────────────────

PROPS = {
    "T":    ("Temperature",            "K",       lambda v: f"{v:.4f} K  /  {v - 273.15:.4f} °C"),
    "P":    ("Pressure",               "Pa",      lambda v: f"{v:.2f} Pa  /  {v/1000:.4f} kPa  /  {v/1e5:.6f} bar"),
    "D":    ("Density",                "kg/m³",   lambda v: f"{v:.6f} kg/m³"),
    "H":    ("Specific enthalpy",      "J/kg",    lambda v: f"{v:.4f} J/kg  /  {v/1000:.6f} kJ/kg"),
    "S":    ("Specific entropy",       "J/kg·K",  lambda v: f"{v:.6f} J/kg·K  /  {v/1000:.8f} kJ/kg·K"),
    "U":    ("Specific internal energy","J/kg",   lambda v: f"{v:.4f} J/kg"),
    "C":    ("Specific heat (const P)", "J/kg·K", lambda v: f"{v:.4f} J/kg·K"),
    "O":    ("Specific heat (const V)", "J/kg·K", lambda v: f"{v:.4f} J/kg·K"),
    "L":    ("Thermal conductivity",   "W/m·K",   lambda v: f"{v:.6f} W/m·K"),
    "V":    ("Dynamic viscosity",      "Pa·s",    lambda v: f"{v:.4e} Pa·s"),
    "Q":    ("Vapor quality",          "-",       lambda v: f"{v:.6f}  (0=liquid, 1=vapor)"),
    "A":    ("Speed of sound",         "m/s",     lambda v: f"{v:.4f} m/s"),
}

INPUT_PAIRS = {
    "PT": ("P", "T"),
    "PH": ("P", "H"),
    "PS": ("P", "S"),
    "PQ": ("P", "Q"),
    "TQ": ("T", "Q"),
    "TP": ("T", "P"),
    "HS": ("H", "S"),
    "TD": ("T", "D"),
}

COMMON_FLUIDS = [
    "Water", "Air", "Nitrogen", "Oxygen", "CO2", "Argon", "Hydrogen", "Helium",
    "R134a", "R410A", "R404A", "R22", "R32", "R1234yf", "R1234ze(E)",
    "Ammonia", "Propane", "IsoButane", "n-Butane", "Ethanol", "Methanol",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def separator(char="─", width=60):
    print(char * width)


def header(title):
    separator("═")
    print(f"  {title}")
    separator("═")


def section(title):
    print()
    separator()
    print(f"  {title}")
    separator()


def ask(prompt, default=None):
    suffix = f" [{default}]" if default is not None else ""
    raw = input(f"  {prompt}{suffix}: ").strip()
    return raw if raw else (str(default) if default is not None else "")


def parse_float(s, label="value"):
    try:
        return float(s)
    except ValueError:
        print(f"  ✗ Invalid {label}: '{s}'")
        return None


def get_critical_props(fluid):
    Tc = PropsSI("Tcrit", fluid)
    Pc = PropsSI("Pcrit", fluid)
    Tt = PropsSI("Ttriple", fluid)
    Pt = PropsSI("ptriple", fluid)
    M  = PropsSI("M", fluid) * 1000  # g/mol
    return Tc, Pc, Tt, Pt, M


# ── Feature 1: Single state point ─────────────────────────────────────────────

def calc_state_point():
    section("Single State Point")
    fluid = ask("Fluid (e.g. Water, R134a, CO2)", "Water")

    print()
    print("  Input pairs available:")
    for key, (p1, p2) in INPUT_PAIRS.items():
        print(f"    {key:4s}  ({p1}, {p2})")
    pair = ask("Input pair", "PT").upper()
    if pair not in INPUT_PAIRS:
        print(f"  ✗ Unknown pair '{pair}'")
        return

    p1, p2 = INPUT_PAIRS[pair]

    unit1 = PROPS[p1][1] if p1 in PROPS else "—"
    unit2 = PROPS[p2][1] if p2 in PROPS else "—"

    v1 = parse_float(ask(f"{p1} ({unit1})"), p1)
    v2 = parse_float(ask(f"{p2} ({unit2})"), p2)
    if v1 is None or v2 is None:
        return

    print()
    print(f"  Results for {fluid}  [{pair}: {v1}, {v2}]")
    separator()

    for key, (name, unit, fmt) in PROPS.items():
        try:
            val = PropsSI(key, p1, v1, p2, v2, fluid)
            print(f"  {name:<28s} {fmt(val)}")
        except Exception:
            pass


# ── Feature 2: Saturation curve ───────────────────────────────────────────────

def calc_saturation():
    section("Saturation Properties at a Given Temperature or Pressure")
    fluid = ask("Fluid", "R134a")

    mode = ask("Fix by  T (temperature) or P (pressure)?", "T").upper()

    if mode == "T":
        T = parse_float(ask("Temperature [K]"), None)
        if T is None:
            return
        Tc, Pc, *_ = get_critical_props(fluid)
        if T >= Tc:
            print(f"  ✗ T={T} K exceeds critical temperature Tc={Tc:.2f} K")
            return

        def get(output, quality):
            return PropsSI(output, "T", T, "Q", quality, fluid)

        label = f"T = {T} K  ({T - 273.15:.2f} °C)"

    elif mode == "P":
        P = parse_float(ask("Pressure [Pa]"), None)
        if P is None:
            return
        Pc = PropsSI("Pcrit", fluid)
        if P >= Pc:
            print(f"  ✗ P={P} Pa exceeds critical pressure Pc={Pc:.2f} Pa")
            return

        def get(output, quality):
            return PropsSI(output, "P", P, "Q", quality, fluid)

        T_sat = PropsSI("T", "P", P, "Q", 0, fluid)
        label = f"P = {P} Pa ({P/1000:.2f} kPa)  →  T_sat = {T_sat:.2f} K ({T_sat-273.15:.2f} °C)"

    else:
        print("  ✗ Choose T or P")
        return

    print()
    print(f"  Saturation properties for {fluid}  at  {label}")
    separator()
    print(f"  {'Property':<28s} {'Liquid (Q=0)':<28s} {'Vapor (Q=1)'}")
    separator()

    for key, (name, unit, fmt) in PROPS.items():
        if key == "Q":
            continue
        try:
            liq = get(key, 0)
            vap = get(key, 1)
            print(f"  {name:<28s} {fmt(liq):<40s} {fmt(vap)}")
        except Exception:
            pass


# ── Feature 3: Ideal vapor-compression refrigeration cycle ────────────────────

def calc_refrigeration_cycle():
    section("Ideal Vapor-Compression Refrigeration Cycle")
    fluid = ask("Refrigerant", "R134a")

    T_evap = parse_float(ask("Evaporator temperature [°C]", "-10"))
    T_cond = parse_float(ask("Condenser temperature [°C]", "40"))
    if T_evap is None or T_cond is None:
        return

    T_evap_K = T_evap + 273.15
    T_cond_K = T_cond + 273.15

    superheat   = parse_float(ask("Superheat at compressor inlet [K]", "5"))
    subcooling  = parse_float(ask("Subcooling at condenser exit [K]", "5"))
    eta_comp    = parse_float(ask("Isentropic compressor efficiency [0-1]", "0.75"))
    if any(v is None for v in [superheat, subcooling, eta_comp]):
        return

    Tc, Pc, *_ = get_critical_props(fluid)
    if T_evap_K >= Tc or T_cond_K >= Tc:
        print(f"  ✗ Temperature exceeds critical point ({Tc-273.15:.1f} °C)")
        return

    # State 1: compressor inlet (superheated vapor)
    P_evap = PropsSI("P", "T", T_evap_K, "Q", 1, fluid)
    T1 = T_evap_K + superheat
    H1 = PropsSI("H", "T", T1, "P", P_evap, fluid)
    S1 = PropsSI("S", "T", T1, "P", P_evap, fluid)

    # State 2s: isentropic compression exit
    P_cond = PropsSI("P", "T", T_cond_K, "Q", 1, fluid)
    H2s = PropsSI("H", "P", P_cond, "S", S1, fluid)

    # State 2: actual compression exit
    H2 = H1 + (H2s - H1) / eta_comp
    T2 = PropsSI("T", "P", P_cond, "H", H2, fluid)

    # State 3: condenser exit (subcooled liquid)
    T3 = T_cond_K - subcooling
    H3 = PropsSI("H", "T", T3, "P", P_cond, fluid)

    # State 4: expansion valve exit (isenthalpic)
    H4 = H3  # isenthalpic flash
    Q4 = PropsSI("Q", "P", P_evap, "H", H4, fluid)

    # COP & capacity per kg of refrigerant
    q_evap = H1 - H4        # evaporator heat absorption [J/kg]
    w_comp = H2 - H1        # compressor work [J/kg]
    q_cond = H2 - H3        # condenser heat rejection [J/kg]
    COP    = q_evap / w_comp

    print()
    print(f"  Cycle Results — {fluid}")
    separator()
    print(f"  {'State':<8} {'T (°C)':<12} {'P (kPa)':<12} {'H (kJ/kg)':<14} {'Q'}")
    separator()

    def st(label, T_K, P_Pa, H_Jkg, Q_val=None):
        Q_str = f"{Q_val:.3f}" if Q_val is not None else "  —"
        print(f"  {label:<8} {T_K-273.15:<12.2f} {P_Pa/1000:<12.2f} {H_Jkg/1000:<14.4f} {Q_str}")

    st("1 (comp in)",   T1,   P_evap, H1)
    st("2s (ideal)",    T2,   P_cond, H2s)
    st("2 (actual)",    T2,   P_cond, H2)
    st("3 (cond out)",  T3,   P_cond, H3)
    st("4 (exp out)",   T_evap_K, P_evap, H4, Q4)

    separator()
    print(f"  Evaporator pressure   {P_evap/1000:>10.3f} kPa")
    print(f"  Condenser pressure    {P_cond/1000:>10.3f} kPa")
    print(f"  Pressure ratio        {P_cond/P_evap:>10.3f}")
    separator()
    print(f"  Refrigeration effect  {q_evap/1000:>10.4f} kJ/kg")
    print(f"  Compressor work       {w_comp/1000:>10.4f} kJ/kg")
    print(f"  Heat rejection        {q_cond/1000:>10.4f} kJ/kg")
    print(f"  COP (cooling)         {COP:>10.4f}")
    print(f"  COP (heat pump)       {(q_cond/w_comp):>10.4f}")
    print(f"  Flash quality at exp. {Q4:>10.4f}")


# ── Feature 4: Fluid critical & triple point info ─────────────────────────────

def fluid_info():
    section("Fluid Critical & Reference Data")
    fluid = ask("Fluid", "Water")

    try:
        Tc, Pc, Tt, Pt, M = get_critical_props(fluid)
    except Exception as e:
        print(f"  ✗ Could not retrieve data: {e}")
        return

    T_nbp = PropsSI("T", "P", 101325, "Q", 0, fluid)

    print()
    print(f"  Fluid: {fluid}")
    separator()
    print(f"  Molar mass            {M:.4f} g/mol")
    print(f"  Critical temperature  {Tc:.4f} K  /  {Tc-273.15:.4f} °C")
    print(f"  Critical pressure     {Pc:.2f} Pa  /  {Pc/1e5:.4f} bar")
    print(f"  Triple point T        {Tt:.4f} K  /  {Tt-273.15:.4f} °C")
    print(f"  Triple point P        {Pt:.4f} Pa")
    print(f"  Normal boiling point  {T_nbp:.4f} K  /  {T_nbp-273.15:.4f} °C")


# ── Feature 5: Unit conversion helpers ────────────────────────────────────────

def unit_conversions():
    section("Unit Conversions")
    conversions = [
        ("Temperature: °C → K",   lambda x: x + 273.15,   "°C", "K"),
        ("Temperature: K → °C",   lambda x: x - 273.15,   "K",  "°C"),
        ("Temperature: °F → K",   lambda x: (x - 32)*5/9 + 273.15, "°F", "K"),
        ("Pressure: bar → Pa",    lambda x: x * 1e5,      "bar", "Pa"),
        ("Pressure: psi → Pa",    lambda x: x * 6894.76,  "psi", "Pa"),
        ("Pressure: kPa → Pa",    lambda x: x * 1000,     "kPa", "Pa"),
        ("Energy: kJ/kg → J/kg",  lambda x: x * 1000,     "kJ/kg", "J/kg"),
        ("Power: kW → W",         lambda x: x * 1000,     "kW", "W"),
    ]
    print()
    for i, (label, *_) in enumerate(conversions, 1):
        print(f"  {i:2d}. {label}")
    print()
    choice = ask("Choose conversion number")
    try:
        idx = int(choice) - 1
        _, fn, unit_in, unit_out = conversions[idx]
    except (ValueError, IndexError):
        print("  ✗ Invalid choice")
        return
    val = parse_float(ask(f"Value [{unit_in}]"))
    if val is None:
        return
    result = fn(val)
    print(f"  {val} {unit_in}  =  {result:.6g} {unit_out}")


# ── Feature 6: List available fluids ──────────────────────────────────────────

def list_fluids():
    section("Available Fluids")
    fluids = FluidsList()
    print(f"  CoolProp has {len(fluids)} fluids. Common fluids:\n")
    for i, f in enumerate(COMMON_FLUIDS, 1):
        print(f"  {i:3d}. {f}")
    print()
    show_all = ask("Show all fluids? (y/n)", "n").lower()
    if show_all == "y":
        print()
        for i, f in enumerate(fluids, 1):
            print(f"  {i:4d}. {f}")


# ── Capillary tube helpers ───────────────────────────────────────────────────

def _churchill_f(Re, eps_D):
    """Darcy friction factor, Churchill (1977) — valid for all Re."""
    Re = max(Re, 1.0)
    A = (-2.457 * math.log((7 / Re) ** 0.9 + 0.27 * eps_D)) ** 16
    B = (37530 / Re) ** 16
    return 8 * ((8 / Re) ** 12 + (A + B) ** (-1.5)) ** (1 / 12)


def _rho_h(fluid, P, h):
    """Density at (P, h) — returns None on error."""
    try:
        return PropsSI("D", "P", P, "H", h, fluid)
    except Exception:
        return None


def _mu_h(fluid, P, h):
    """Dynamic viscosity at (P, h) — returns None on error."""
    try:
        return PropsSI("V", "P", P, "H", h, fluid)
    except Exception:
        return None


# ── Feature 7: Capillary tube sizing ─────────────────────────────────────────

def calc_capillary_tube():
    """
    Size an adiabatic capillary tube using the homogeneous equilibrium model.

    Governing momentum equation (horizontal, constant area, isenthalpic h=const):

        dP/dz = -(f G² / 2Dρ) / [1 + G² d(1/ρ)/dP|_h]

    Denominator → 0  =>  choked (critical) flow.
    """
    section("Capillary Tube Sizing  (adiabatic, homogeneous EQ model)")
    fluid = ask("Refrigerant", "R134a")

    T_cond  = parse_float(ask("Condensing temperature [°C]", "40"))
    subcool = parse_float(ask("Subcooling at tube inlet [K]", "5"))
    T_evap  = parse_float(ask("Evaporating temperature [°C]", "-10"))
    if any(v is None for v in [T_cond, subcool, T_evap]):
        return

    P_in  = PropsSI("P", "T", T_cond + 273.15, "Q", 0, fluid)
    P_out = PropsSI("P", "T", T_evap + 273.15, "Q", 1, fluid)

    print(f"\n  P_in  (cond) = {P_in/1000:.2f} kPa")
    print(f"  P_out (evap) = {P_out/1000:.2f} kPa")
    print(f"  Pressure ratio = {P_in/P_out:.3f}")

    mode = ask("\n  Find (L)ength for given diameter, or (D)iameter for given length?", "L").upper()

    if mode == "L":
        D_mm   = parse_float(ask("Tube inner diameter [mm]", "0.8"))
        m_dot  = parse_float(ask("Mass flow rate [kg/s]", "0.005"))
        if D_mm is None or m_dot is None:
            return
        D = D_mm / 1000
        diameters = [D]
        flows     = [m_dot]
    else:
        L_m    = parse_float(ask("Tube length [m]", "2.0"))
        m_dot  = parse_float(ask("Mass flow rate [kg/s]", "0.005"))
        if L_m is None or m_dot is None:
            return
        # Iterate on D from 0.5 mm to 3.0 mm, find which gives L_m
        # We'll compute L for a range of D values and print the table
        diameters = np.linspace(0.5e-3, 3.0e-3, 26)
        flows     = [m_dot] * len(diameters)

    roughness = 1.5e-6   # copper tube roughness [m]
    N_steps   = 1000

    # Inlet enthalpy (subcooled liquid)
    T_in_K = PropsSI("T", "P", P_in, "Q", 0, fluid) - subcool
    try:
        h_in = PropsSI("H", "T", T_in_K, "P", P_in, fluid)
    except Exception as e:
        print(f"  ✗ Cannot compute inlet state: {e}")
        return

    def calc_length(D_val, mdot_val):
        A = math.pi * D_val ** 2 / 4
        G = mdot_val / A
        eps_D = roughness / D_val
        P_arr = np.linspace(P_in, P_out, N_steps + 1)
        L_tube = 0.0
        choked = False
        P_choke = None
        dP_num = (P_in - P_out) * 1e-4   # small perturbation for d(1/ρ)/dP

        for i in range(N_steps):
            P     = P_arr[i]
            delta = abs(P_arr[i + 1] - P_arr[i])

            rho = _rho_h(fluid, P, h_in)
            mu  = _mu_h(fluid, P, h_in)
            if rho is None or mu is None or rho <= 0:
                break

            # Numerical d(1/ρ)/dP at constant h
            rho_p = _rho_h(fluid, P + dP_num, h_in)
            rho_m = _rho_h(fluid, P - dP_num, h_in)
            if rho_p and rho_m and rho_p > 0 and rho_m > 0:
                d_inv_rho_dP = (1 / rho_m - 1 / rho_p) / (2 * dP_num)
            else:
                d_inv_rho_dP = 0.0

            denom = 1.0 + G ** 2 * d_inv_rho_dP
            if denom <= 1e-6:
                choked = True
                P_choke = P
                break

            Re = G * D_val / mu
            f  = _churchill_f(Re, eps_D)

            # dz from: delta = (f*G²/(2Dρ)/denom) * dz
            dz_fric = (f * G ** 2) / (2 * D_val * rho)
            if dz_fric <= 0:
                break
            dz = delta * denom / dz_fric
            L_tube += dz

        return L_tube, choked, P_choke, G

    if mode == "L":
        L_val, choked, P_choke, G = calc_length(diameters[0], flows[0])
        A_val = math.pi * diameters[0] ** 2 / 4
        v_in  = G / (_rho_h(fluid, P_in, h_in) or 1)

        print()
        print(f"  ── Results ──")
        print(f"  Tube inner diameter   {diameters[0]*1000:.2f} mm")
        print(f"  Mass flux G           {G:.2f} kg/m²s")
        print(f"  Inlet velocity        {v_in:.4f} m/s")
        print(f"  Required tube length  {L_val:.4f} m  ({L_val*100:.2f} cm)")
        if choked:
            print(f"  ⚠  Choked flow detected at P = {P_choke/1000:.2f} kPa  — reduce flow or enlarge tube")
        else:
            print(f"  Flow: subcritical (not choked)")
    else:
        # Table of D vs computed length
        print()
        print(f"  For desired length L = {L_m:.2f} m  (mass flow = {m_dot*1000:.4f} g/s)")
        separator()
        print(f"  {'D (mm)':<10} {'G (kg/m²s)':<14} {'Computed L (m)':<18} {'Note'}")
        separator()
        for D_val, md in zip(diameters, flows):
            L_val, choked, P_choke, G = calc_length(D_val, md)
            note = "CHOKED" if choked else ("← close" if abs(L_val - L_m) / L_m < 0.05 else "")
            print(f"  {D_val*1000:<10.2f} {G:<14.1f} {L_val:<18.4f} {note}")
        print()
        print("  Tip: choose the diameter whose computed length is closest to your target.")


# ── Feature 8: System power sizing ───────────────────────────────────────────

def calc_system_sizing():
    """
    Given a desired cooling capacity, compute:
      - Refrigerant mass flow rate
      - Compressor shaft power & electrical input
      - Condenser heat rejection
      - COP (cooling & heat-pump)
      - Secondary (chilled water / brine) loop pump power
    """
    section("System Power & Flow Sizing")
    fluid = ask("Refrigerant", "R134a")

    Q_cool_kW = parse_float(ask("Desired cooling capacity [kW]", "5"))
    T_evap    = parse_float(ask("Evaporator temperature [°C]", "-10"))
    T_cond    = parse_float(ask("Condenser temperature [°C]", "40"))
    superheat = parse_float(ask("Superheat at compressor inlet [K]", "5"))
    subcool   = parse_float(ask("Subcooling at condenser exit [K]", "5"))
    eta_comp  = parse_float(ask("Isentropic compressor efficiency [0-1]", "0.75"))
    eta_motor = parse_float(ask("Motor efficiency [0-1]", "0.92"))
    if any(v is None for v in [Q_cool_kW, T_evap, T_cond, superheat, subcool, eta_comp, eta_motor]):
        return

    Q_cool = Q_cool_kW * 1000
    T_evap_K = T_evap + 273.15
    T_cond_K = T_cond + 273.15

    Tc = PropsSI("Tcrit", fluid)
    if T_evap_K >= Tc or T_cond_K >= Tc:
        print(f"  ✗ Temperature exceeds critical point ({Tc-273.15:.1f} °C)")
        return

    # ── Refrigeration cycle state points ─────────────────────────────────────
    P_evap = PropsSI("P", "T", T_evap_K, "Q", 1, fluid)
    P_cond = PropsSI("P", "T", T_cond_K, "Q", 1, fluid)

    # State 1: compressor inlet (superheated)
    T1 = T_evap_K + superheat
    H1 = PropsSI("H", "T", T1, "P", P_evap, fluid)
    S1 = PropsSI("S", "T", T1, "P", P_evap, fluid)

    # State 2: actual compressor exit
    H2s = PropsSI("H", "P", P_cond, "S", S1, fluid)
    H2  = H1 + (H2s - H1) / eta_comp

    # State 3: subcooled liquid
    T3 = T_cond_K - subcool
    H3 = PropsSI("H", "T", T3, "P", P_cond, fluid)

    # State 4: after expansion (isenthalpic)
    H4 = H3

    q_evap = H1 - H4         # specific refrigeration effect [J/kg]
    w_comp = H2 - H1         # specific compressor work [J/kg]
    q_cond = H2 - H3         # specific condenser duty [J/kg]

    if q_evap <= 0:
        print("  ✗ Negative refrigeration effect — check temperatures")
        return

    m_dot       = Q_cool / q_evap
    W_comp_sh   = m_dot * w_comp          # shaft power [W]
    W_comp_el   = W_comp_sh / eta_motor   # electrical input [W]
    Q_cond      = m_dot * q_cond          # condenser duty [W]
    COP_cool    = Q_cool / W_comp_sh
    COP_hp      = Q_cond / W_comp_sh
    PR          = P_cond / P_evap

    print()
    separator()
    print(f"  ── Refrigerant Side  ({fluid}) ──")
    separator()
    print(f"  Cooling capacity          {Q_cool/1000:>10.4f} kW")
    print(f"  Mass flow rate            {m_dot*1000:>10.4f} g/s  ({m_dot:>10.6f} kg/s)")
    print(f"  Refrigeration effect      {q_evap/1000:>10.4f} kJ/kg")
    print(f"  Compressor work           {w_comp/1000:>10.4f} kJ/kg")
    separator()
    print(f"  Compressor shaft power    {W_comp_sh/1000:>10.4f} kW")
    print(f"  Compressor electrical in  {W_comp_el/1000:>10.4f} kW")
    print(f"  Condenser heat rejection  {Q_cond/1000:>10.4f} kW")
    print(f"  COP (cooling)             {COP_cool:>10.4f}")
    print(f"  COP (heat pump)           {COP_hp:>10.4f}")
    print(f"  Pressure ratio            {PR:>10.4f}")
    print(f"  Evap pressure             {P_evap/1000:>10.3f} kPa")
    print(f"  Cond pressure             {P_cond/1000:>10.3f} kPa")

    # ── Secondary loop pump ───────────────────────────────────────────────────
    print()
    do_pump = ask("Size secondary loop pump? (y/n)", "y").lower()
    if do_pump != "y":
        return

    sec_fluid   = ask("Secondary fluid (Water, MEG, Brine)", "Water")
    dT_sec      = parse_float(ask("Temperature rise across evaporator [K]", "5"))
    head_m      = parse_float(ask("System pressure head [m of fluid]", "10"))
    eta_pump    = parse_float(ask("Pump efficiency [0-1]", "0.65"))
    if any(v is None for v in [dT_sec, head_m, eta_pump]):
        return

    # Secondary fluid properties (approximate at mean evap temperature)
    T_sec_mean_K = T_evap_K + dT_sec / 2 + 5   # a few degrees above evap temp
    T_sec_mean_K = max(T_sec_mean_K, 274.0)      # keep above freezing
    P_ref = 101325.0

    if sec_fluid.lower() == "water":
        try:
            rho_sec = PropsSI("D", "T", T_sec_mean_K, "P", P_ref, "Water")
            cp_sec  = PropsSI("C", "T", T_sec_mean_K, "P", P_ref, "Water")
        except Exception:
            rho_sec, cp_sec = 999.0, 4182.0
    else:
        # Generic estimate for brines/glycol
        rho_sec = float(ask(f"  Density of {sec_fluid} at operating temp [kg/m³]", "1040")) or 1040
        cp_sec  = float(ask(f"  Specific heat of {sec_fluid} [J/kg·K]", "3800")) or 3800

    m_dot_sec  = Q_cool / (cp_sec * dT_sec)
    V_dot_sec  = m_dot_sec / rho_sec
    W_pump_sh  = rho_sec * 9.81 * V_dot_sec * head_m
    W_pump_el  = W_pump_sh / eta_pump

    print()
    separator()
    print(f"  ── Secondary Loop  ({sec_fluid}) ──")
    separator()
    print(f"  Fluid density             {rho_sec:>10.2f} kg/m³")
    print(f"  Fluid specific heat       {cp_sec:>10.2f} J/kg·K")
    print(f"  Mass flow rate (sec)      {m_dot_sec*1000:>10.4f} g/s  ({m_dot_sec:>10.6f} kg/s)")
    print(f"  Volumetric flow rate      {V_dot_sec*1000:>10.4f} L/s  ({V_dot_sec*3600:>8.4f} m³/h)")
    print(f"  Pump head                 {head_m:>10.2f} m")
    print(f"  Pump shaft power          {W_pump_sh:>10.4f} W  ({W_pump_sh/1000:.4f} kW)")
    print(f"  Pump electrical input     {W_pump_el:>10.4f} W  ({W_pump_el/1000:.4f} kW)")
    separator()
    print(f"  Total electrical input    {(W_comp_el + W_pump_el)/1000:>10.4f} kW")
    print(f"  System EER (kW_cool/kW_el) {Q_cool/(W_comp_el+W_pump_el):>9.4f}")


# ── Main menu ─────────────────────────────────────────────────────────────────

MENU = [
    ("State point properties",                    calc_state_point),
    ("Saturation properties",                     calc_saturation),
    ("Vapor-compression refrigeration cycle",     calc_refrigeration_cycle),
    ("System power & flow sizing",                calc_system_sizing),
    ("Capillary tube sizing",                     calc_capillary_tube),
    ("Fluid critical & reference data",           fluid_info),
    ("Unit conversions",                          unit_conversions),
    ("List available fluids",                     list_fluids),
]


def main():
    header("CoolProp Thermodynamic Calculator")
    print(f"  CoolProp version: {CP.__version__ if hasattr(CP, '__version__') else 'unknown'}")

    while True:
        print()
        separator()
        print("  MENU")
        separator()
        for i, (label, _) in enumerate(MENU, 1):
            print(f"  {i}. {label}")
        print("  0. Exit")
        separator()

        choice = ask("Select").strip()
        if choice == "0":
            print("  Goodbye.")
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(MENU):
                MENU[idx][1]()
            else:
                print("  ✗ Choice out of range")
        except ValueError:
            print("  ✗ Enter a number")
        except KeyboardInterrupt:
            print("\n  (interrupted — returning to menu)")
        except Exception as e:
            print(f"  ✗ CoolProp error: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  Exited.")
        sys.exit(0)
