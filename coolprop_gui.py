"""
CoolProp Thermodynamic Calculator  ─  GUI Edition
Requires: customtkinter, CoolProp, numpy
"""

# ── Auto-install customtkinter if needed ──────────────────────────────────────
try:
    import customtkinter as ctk
except ImportError:
    import subprocess, sys as _sys
    print("Installing customtkinter …")
    subprocess.check_call([_sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk

import math, sys
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from CoolProp.CoolProp import PropsSI, FluidsList
import CoolProp.CoolProp as CP

# ── Matplotlib (optional – charts disabled if not installed) ──────────────────
try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MPLOK = True
except ImportError:
    MPLOK = False

# ── Theme ─────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ── Fluid lists ───────────────────────────────────────────────────────────────
_COMMON = [
    "R134a", "R410A", "R32", "R1234yf", "R22", "Ammonia", "CO2",
    "Water",  "Air",   "Propane", "IsoButane", "n-Butane",
    "Nitrogen", "Oxygen", "Argon", "Hydrogen", "Helium",
]
ALL_FLUIDS = _COMMON + [f for f in sorted(FluidsList()) if f not in _COMMON]

# ── Input variable definitions ────────────────────────────────────────────────
# key → (label, SI_unit, [(display_unit, to_SI_fn)])
IVARS = {
    "T": ("Temperature",   "K",      [("K",  lambda x: x),
                                       ("°C", lambda x: x + 273.15),
                                       ("°F", lambda x: (x - 32)*5/9 + 273.15)]),
    "P": ("Pressure",      "Pa",     [("Pa",  lambda x: x),
                                       ("kPa", lambda x: x * 1e3),
                                       ("MPa", lambda x: x * 1e6),
                                       ("bar", lambda x: x * 1e5),
                                       ("psi", lambda x: x * 6894.76)]),
    "H": ("Enthalpy",      "J/kg",   [("J/kg",  lambda x: x),
                                       ("kJ/kg", lambda x: x * 1e3)]),
    "S": ("Entropy",       "J/kg·K", [("J/kg·K",  lambda x: x),
                                       ("kJ/kg·K", lambda x: x * 1e3)]),
    "D": ("Density",       "kg/m³",  [("kg/m³", lambda x: x)]),
    "Q": ("Vapor Quality", "—",      [("—", lambda x: x)]),
    "U": ("Int. Energy",   "J/kg",   [("J/kg",  lambda x: x),
                                       ("kJ/kg", lambda x: x * 1e3)]),
}

# ── Output variable definitions ───────────────────────────────────────────────
# (cp_key, display_name, format_fn)
OVARS = [
    ("T", "Temperature",        lambda v: f"{v:.4f} K   ({v - 273.15:.4f} °C)"),
    ("P", "Pressure",           lambda v: f"{v/1000:.4f} kPa   ({v/1e5:.6f} bar)"),
    ("D", "Density",            lambda v: f"{v:.6f} kg/m³"),
    ("H", "Enthalpy",           lambda v: f"{v/1000:.5f} kJ/kg"),
    ("S", "Entropy",            lambda v: f"{v/1000:.7f} kJ/kg·K"),
    ("U", "Internal Energy",    lambda v: f"{v/1000:.5f} kJ/kg"),
    ("C", "Cp",                 lambda v: f"{v:.4f} J/kg·K"),
    ("O", "Cv",                 lambda v: f"{v:.4f} J/kg·K"),
    ("Q", "Vapor Quality",      lambda v: f"{v:.6f}"),
    ("A", "Speed of Sound",     lambda v: f"{v:.4f} m/s"),
    ("L", "Thermal Cond.",      lambda v: f"{v:.6f} W/m·K"),
    ("V", "Dyn. Viscosity",     lambda v: f"{v:.4e} Pa·s"),
]

SAT_TABLE_COLUMNS = [
    "T (°C)",
    "P_sat (kPa)",
    "ρ_liq (kg/m³)",
    "ρ_vap (kg/m³)",
    "h_liq (kJ/kg)",
    "h_vap (kJ/kg)",
    "ΔH_vap (kJ/kg)",
]

# ── Variable descriptions ─────────────────────────────────────────────────────
# VAR_DESC: key → (short name, multi-line tooltip text)
VAR_DESC = {
    "T": ("Temperature",
          "Absolute temperature of the fluid.\n"
          "• SI unit: K (Kelvin)\n"
          "• Also accepts: °C, °F\n"
          "• 0 K = absolute zero  |  273.15 K = 0 °C  |  373.15 K = 100 °C"),
    "P": ("Pressure",
          "Force per unit area exerted by the fluid.\n"
          "• SI unit: Pa (Pascal = N/m²)\n"
          "• Also accepts: kPa, MPa, bar, psi\n"
          "• 1 atm ≈ 101.325 kPa ≈ 1.01325 bar ≈ 14.696 psi"),
    "H": ("Specific Enthalpy",
          "Thermodynamic potential  h = u + Pv\n"
          "• Combines internal energy + flow work (P·v)\n"
          "• SI unit: J/kg  (kJ/kg common in engineering)\n"
          "• Key quantity in the steady-flow energy equation\n"
          "• Reference state varies by fluid (ASHRAE / NBP convention)"),
    "S": ("Specific Entropy",
          "Measure of molecular disorder and irreversibility.\n"
          "• SI unit: J/kg·K\n"
          "• Increases in all irreversible processes (2nd Law: ds ≥ δq/T)\n"
          "• Isentropic = reversible adiabatic (ds = 0)\n"
          "• Used to define isentropic compressor efficiency"),
    "D": ("Density",
          "ρ = m/V  (mass per unit volume).\n"
          "• SI unit: kg/m³\n"
          "• Inverse of specific volume: v = 1/ρ  [m³/kg]\n"
          "• Determines pipe velocities, pressure drops, and equipment sizing"),
    "Q": ("Vapor Quality",
          "Mass fraction of vapor in a two-phase liquid–vapor mixture.\n"
          "• Q = 0  →  saturated liquid  (bubble point)\n"
          "• Q = 1  →  saturated vapor   (dew point)\n"
          "• Only defined inside the two-phase dome\n"
          "• Dimensionless (0 – 1)"),
    "U": ("Specific Internal Energy",
          "Energy stored in molecular motion and intermolecular forces.\n"
          "• SI unit: J/kg\n"
          "• h = u + Pv  (enthalpy = internal energy + flow work)\n"
          "• Closed-system energy balance: ΔU = Q − W"),
    "C": ("Cp — Specific Heat at Constant Pressure",
          "Heat needed to raise 1 kg of fluid by 1 K at constant pressure.\n"
          "• SI unit: J/kg·K\n"
          "• Always Cp > Cv for real fluids\n"
          "• Diverges near the critical point\n"
          "• Sensible heat equation: Q = ṁ·Cp·ΔT"),
    "O": ("Cv — Specific Heat at Constant Volume",
          "Heat needed to raise 1 kg of fluid by 1 K at constant volume.\n"
          "• SI unit: J/kg·K\n"
          "• Heat ratio γ = Cp/Cv  (isentropic exponent)\n"
          "• Ideal gas: Cp − Cv = R/M"),
    "A": ("Speed of Sound",
          "Velocity of small pressure waves in the fluid.\n"
          "• SI unit: m/s\n"
          "• a = √(∂P/∂ρ)ₛ  (isentropic derivative)\n"
          "• Critical for capillary tube choked-flow analysis\n"
          "• Air at 20 °C ≈ 343 m/s  |  Water ≈ 1480 m/s"),
    "L": ("Thermal Conductivity",
          "Ability of the fluid to conduct heat.\n"
          "• SI unit: W/m·K\n"
          "• Fourier’s law: q = −k ∇T\n"
          "• Key parameter for heat exchanger sizing\n"
          "• Liquids generally have higher k than vapors"),
    "V": ("Dynamic Viscosity",
          "Internal resistance of the fluid to shear flow.\n"
          "• SI unit: Pa·s  (= kg/m·s)\n"
          "• Kinematic viscosity: ν = μ/ρ  [m²/s]\n"
          "• Reynolds number: Re = ρ·v·D/μ\n"
          "• Liquids: viscosity ↓ with T  |  Gases: viscosity ↑ with T"),
}

# FIELD_DESC: input field key → tooltip shown on hover over the label
FIELD_DESC = {
    "fluid":  "Working fluid / refrigerant.\n"
              "124 fluids available; common refrigerants listed first.\n"
              "Examples: R134a (HFC), R410A (blend), CO2 (natural), NH₃ (Ammonia)",
    "T_evap": "Evaporator saturation temperature  [°C].\n"
              "The refrigerant boils at this temperature, absorbing heat from the cooled space.\n"
              "• Sets the low-side (suction) pressure via the saturation curve\n"
              "• Typical refrigeration: −40 °C to +10 °C",
    "T_cond": "Condenser saturation temperature  [°C].\n"
              "The refrigerant condenses here, rejecting heat to air or water.\n"
              "• Sets the high-side (discharge) pressure\n"
              "• Typical air-cooled: 30 °C to 55 °C",
    "SH":     "Superheat at the compressor inlet  [K above saturation].\n"
              "Extra temperature above saturation protects the compressor from liquid slugging.\n"
              "• Typical: 5 – 15 K\n"
              "• Too much superheat → higher discharge temperature, lower COP",
    "SC":     "Subcooling at the condenser exit  [K below saturation].\n"
              "Extra cooling below saturation increases refrigeration effect\n"
              "and prevents flash gas in the liquid line.\n"
              "• Typical: 3 – 10 K",
    "eta_c":  "Isentropic (adiabatic) compressor efficiency.\n"
              "η_is = (h₂s − h₁) / (h₂_actual − h₁)\n"
              "Accounts for friction, heat transfer, and gas leakage.\n"
              "• Typical hermetic compressor: 0.60 – 0.80",
    "eta_m":  "Electric motor efficiency: shaft power out / electrical power in.\n"
              "Includes copper losses, iron losses, and windage.\n"
              "• Typical EC / BLDC motor: 0.88 – 0.96",
    "Q_kw":   "Desired cooling capacity (refrigeration effect)  [kW].\n"
              "Heat removed from the cooled space per unit time.\n"
              "• 1 ton of refrigeration = 3.517 kW = 12,000 BTU/h",
    "m_dot":  "Refrigerant mass flow rate  [kg/s].\n"
              "Determined by compressor displacement × volumetric efficiency × suction density.\n"
              "• Typical small household systems: 1 – 10 g/s",
    "dT":     "Temperature rise of the secondary fluid across the evaporator  [K].\n"
              "Smaller ΔT → higher mass flow rate, larger pump.\n"
              "• Typical chilled water systems: 5 – 8 K",
    "head":   "Total pump head  [m of fluid]  the pump must overcome.\n"
              "Includes pipe friction, fittings, control valves, and HX pressure drop.\n"
              "• Typical small systems: 5 – 20 m\n"
              "• Use Darcy–Weisbach for accurate pipe sizing",
    "eta_p":  "Overall pump efficiency: hydraulic + mechanical + motor losses.\n"
              "W_hydraulic / W_electrical.\n"
              "• Typical small centrifugal pump: 0.50 – 0.70",
}

# ── Tooltip ───────────────────────────────────────────────────────────────────
class Tooltip:
    """Lightweight hover tooltip for any tkinter / customtkinter widget."""

    def __init__(self, widget, text: str):
        self._widget = widget
        self._text   = text
        self._tw     = None
        widget.bind("<Enter>",       self._show, add="+")
        widget.bind("<Leave>",       self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _show(self, event=None):
        if self._tw or not self._text:
            return
        x = self._widget.winfo_rootx() + 20
        y = self._widget.winfo_rooty() + self._widget.winfo_height() + 4
        self._tw = tw = tk.Toplevel(self._widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.wm_attributes("-topmost", True)
        frame = tk.Frame(tw, background="#252526", relief="flat",
                         highlightbackground="#3c3c3c", highlightthickness=1)
        frame.pack(ipadx=6, ipady=4)
        tk.Label(frame, text=self._text, background="#252526",
                 foreground="#cccccc", font=("Segoe UI", 9),
                 wraplength=340, justify="left").pack()

    def _hide(self, event=None):
        if self._tw:
            self._tw.destroy()
            self._tw = None


# ── Fonts  (initialized in App.__init__ after the root window exists) ────────
F_TITLE   = None
F_SECTION = None
F_BODY    = None
F_SMALL   = None
F_CALC    = None
F_MONO    = None


def _init_fonts():
    global F_TITLE, F_SECTION, F_BODY, F_SMALL, F_CALC, F_MONO
    F_TITLE   = ctk.CTkFont(size=20, weight="bold")
    F_SECTION = ctk.CTkFont(size=13, weight="bold")
    F_BODY    = ctk.CTkFont(size=12)
    F_SMALL   = ctk.CTkFont(size=10)
    F_CALC    = ctk.CTkFont(size=14, weight="bold")
    F_MONO    = ctk.CTkFont(size=11, family="Consolas")

# ── Treeview style ────────────────────────────────────────────────────────────
_style_ready = False

def _init_style():
    global _style_ready
    if _style_ready:
        return
    _style_ready = True
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("CT.Treeview",
        background="#1e2128", foreground="#dce4ee",
        rowheight=28, fieldbackground="#1e2128",
        borderwidth=0, font=("Segoe UI", 10))
    s.configure("CT.Treeview.Heading",
        background="#1a5276", foreground="white",
        font=("Segoe UI", 10, "bold"), relief="flat")
    s.map("CT.Treeview",
        background=[("selected", "#1f618d")],
        foreground=[("selected", "white")])


def _scroll_units(event):
    """Normalize wheel events across Linux, Windows, and macOS."""
    num = getattr(event, "num", None)
    if num == 4:
        return -1
    if num == 5:
        return 1
    delta = getattr(event, "delta", 0)
    if delta == 0:
        return 0
    steps = max(1, int(abs(delta) / 120))
    return -steps if delta > 0 else steps


def _bind_wheel_scroll(widget, y_scroll=None, x_scroll=None):
    def _on_y(event):
        units = _scroll_units(event)
        if y_scroll is not None and units:
            y_scroll(units)
            return "break"
        return None

    def _on_x(event):
        units = _scroll_units(event)
        if x_scroll is not None and units:
            x_scroll(units)
            return "break"
        return None

    for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
        widget.bind(seq, _on_y, add="+")
    for seq in ("<Shift-MouseWheel>", "<Shift-Button-4>", "<Shift-Button-5>"):
        widget.bind(seq, _on_x if x_scroll is not None else _on_y, add="+")


def make_tree(parent, cols, widths, height=10):
    """Return (outer_frame, treeview)."""
    _init_style()
    outer = tk.Frame(parent, bg="#1e2128")
    outer.grid_columnconfigure(0, weight=1)
    outer.grid_rowconfigure(0, weight=1)
    tv = ttk.Treeview(outer, columns=cols, show="headings",
                      style="CT.Treeview", height=height)
    for col, w in zip(cols, widths):
        tv.heading(col, text=col)
        tv.column(col, width=w, anchor="w", stretch=True)
    sb_y = ttk.Scrollbar(outer, orient="vertical", command=tv.yview)
    sb_x = ttk.Scrollbar(outer, orient="horizontal", command=tv.xview)
    tv.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
    tv.tag_configure("e", background="#1e2128")
    tv.tag_configure("o", background="#262c3a")

    _bind_wheel_scroll(
        tv,
        y_scroll=lambda units: tv.yview_scroll(units, "units"),
        x_scroll=lambda units: tv.xview_scroll(units, "units"),
    )

    tv.grid(row=0, column=0, sticky="nsew")
    sb_y.grid(row=0, column=1, sticky="ns")
    sb_x.grid(row=1, column=0, sticky="ew")
    return outer, tv


def fill_tree(tv, rows):
    tv.delete(*tv.get_children())
    for i, r in enumerate(rows):
        tv.insert("", "end", values=r, tags=("e" if i % 2 == 0 else "o",))


# ── Physics helpers ───────────────────────────────────────────────────────────

def _churchill(Re, eps_D):
    Re = max(Re, 1.0)
    A = (-2.457 * math.log((7 / Re)**0.9 + 0.27 * eps_D))**16
    B = (37530 / Re)**16
    return 8 * ((8 / Re)**12 + (A + B)**(-1.5))**(1 / 12)


def _rho_ph(fluid, P, h):
    try:
        return PropsSI("D", "P", P, "H", h, fluid)
    except Exception:
        return None


def _mu_ph(fluid, P, h):
    try:
        return PropsSI("V", "P", P, "H", h, fluid)
    except Exception:
        return None


def cap_tube_length(fluid, P_in, h_in, P_out, G, D, roughness=1.5e-6):
    """Homogeneous EQ model, isenthalpic. Returns (L_m, choked, P_choke)."""
    eps_D  = roughness / D
    N      = 1000
    Parr   = np.linspace(P_in, P_out, N + 1)
    dP_num = (P_in - P_out) * 1e-4
    L = 0.0
    for i in range(N):
        P  = Parr[i]
        dP = abs(Parr[i + 1] - P)
        rho = _rho_ph(fluid, P, h_in)
        mu  = _mu_ph(fluid, P, h_in)
        if not rho or rho <= 0 or not mu:
            break
        rp = _rho_ph(fluid, P + dP_num, h_in) or rho
        rm = _rho_ph(fluid, P - dP_num, h_in) or rho
        d_inv = (1 / rm - 1 / rp) / (2 * dP_num) if (rp > 0 and rm > 0) else 0.0
        denom = 1.0 + G**2 * d_inv
        if denom <= 1e-6:
            return L, True, P
        Re    = G * D / mu
        f     = _churchill(Re, eps_D)
        rate  = f * G**2 / (2 * D * rho)
        if rate <= 0:
            break
        L += dP * denom / rate
    return L, False, P_out


# ── Chart helpers ─────────────────────────────────────────────────────────────
_C = {                              # shared colour palette
    "bg":    "#1e2128",  "axes":  "#262c3a",  "grid":  "#3a4050",
    "fg":    "#dce4ee",  "spine": "#4a6fa5",
    "liq":   "#4fc3f7",  "vap":   "#ef9a9a",  "cycle": "#80cbc4",
    "pt":    "#ffd54f",  "hi":    "#ff8a65",  "cop":   "#a5d6a7",
    "pwr":   "#ce93d8",
}


def _style_ax(ax):
    """Apply the shared dark theme to a matplotlib Axes."""
    ax.set_facecolor(_C["axes"])
    for sp in ax.spines.values():
        sp.set_color(_C["spine"])
    ax.tick_params(colors=_C["fg"], labelsize=8)
    ax.xaxis.label.set_color(_C["fg"])
    ax.yaxis.label.set_color(_C["fg"])
    ax.title.set_color(_C["fg"])
    ax.grid(True, color=_C["grid"], linestyle="--", alpha=0.5, linewidth=0.7)


def _sat_dome_ph(fluid, n=200):
    """P-H saturation dome.  Returns (h_liq_kJ, h_vap_kJ, P_kPa) arrays."""
    try:
        Tc = PropsSI("Tcrit", fluid)
        Tt = max(PropsSI("Ttriple", fluid) + 1.0, 160.0)
        Ts = np.linspace(Tt, Tc - 0.1, n)
        hl, hv, Ps = [], [], []
        for T in Ts:
            try:
                hl.append(PropsSI("H", "T", T, "Q", 0, fluid) / 1e3)
                hv.append(PropsSI("H", "T", T, "Q", 1, fluid) / 1e3)
                Ps.append(PropsSI("P", "T", T, "Q", 0, fluid) / 1e3)
            except Exception:
                pass
        return np.array(hl), np.array(hv), np.array(Ps)
    except Exception:
        return np.array([]), np.array([]), np.array([])


def _cap_tube_profile(fluid, P_in, h_in, P_out, G, D,
                      roughness=1.5e-6, N=500):
    """Returns (x_m, P_kPa, quality) profile arrays along the capillary tube."""
    eps_D  = roughness / D
    Parr   = np.linspace(P_in, P_out, N + 1)
    dP_num = (P_in - P_out) * 1e-4
    xs, Ps, qs = [0.0], [P_in / 1e3], []
    L = 0.0
    for i in range(N):
        P   = Parr[i]
        dP  = abs(Parr[i + 1] - P)
        rho = _rho_ph(fluid, P, h_in)
        mu  = _mu_ph(fluid, P, h_in)
        if not rho or rho <= 0 or not mu:
            break
        rp    = _rho_ph(fluid, P + dP_num, h_in) or rho
        rm    = _rho_ph(fluid, P - dP_num, h_in) or rho
        d_inv = (1 / rm - 1 / rp) / (2 * dP_num) if (rp > 0 and rm > 0) else 0.0
        denom = 1.0 + G**2 * d_inv
        if denom <= 1e-6:
            xs.append(L); Ps.append(P / 1e3)
            break
        Re   = G * D / mu
        f    = _churchill(Re, eps_D)
        rate = f * G**2 / (2 * D * rho)
        if rate <= 0:
            break
        L += dP * denom / rate
        xs.append(L); Ps.append(Parr[i + 1] / 1e3)
        try:
            q = PropsSI("Q", "P", Parr[i + 1], "H", h_in, fluid)
            qs.append(float(q) if 0 <= q <= 1 else -1.0)
        except Exception:
            qs.append(-1.0)
    return np.array(xs), np.array(Ps), np.array(qs) if qs else np.array([])


class EmbeddedChart(ctk.CTkFrame):
    """Dark-themed CTkFrame containing an embedded matplotlib figure."""

    def __init__(self, parent, figsize=(9, 4.2), **kw):
        super().__init__(parent, corner_radius=10, **kw)
        if not MPLOK:
            ctk.CTkLabel(
                self,
                text="Install matplotlib for charts:  pip install matplotlib",
                text_color="gray55",
            ).pack(pady=20)
            self._fig = self._canvas = None
            return
        self._fig    = plt.Figure(figsize=figsize, facecolor=_C["bg"])
        self._canvas = FigureCanvasTkAgg(self._fig, master=self)
        self._canvas.get_tk_widget().pack(fill="both", expand=True, padx=2, pady=2)

    def figure(self):
        return self._fig

    def redraw(self):
        if self._canvas:
            self._canvas.draw_idle()

    def clear(self):
        if self._fig:
            self._fig.clf()


# ═════════════════════════════════════════════════════════════════════════════
# PAGE CLASSES
# ═════════════════════════════════════════════════════════════════════════════

# ── Helpers shared by all pages ───────────────────────────────────────────────

def _section(parent, text):
    ctk.CTkLabel(parent, text=text, font=F_SECTION).pack(anchor="w", pady=(10, 4))


def _page_hint(parent, text: str):
    """Muted info line describing what a page does and how to use it."""
    ctk.CTkLabel(
        parent, text=text, font=F_SMALL,
        text_color="#7a8a9a", wraplength=920,
        justify="left", anchor="w",
    ).pack(anchor="w", fill="x", pady=(0, 14))


def _fluid_row(parent, default="R134a"):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(row, text="Fluid:", width=55, font=F_BODY).pack(side="left")
    var = tk.StringVar(value=default)
    ctk.CTkComboBox(row, values=ALL_FLUIDS, variable=var, width=220,
                    font=F_BODY).pack(side="left", padx=6)
    return var


def _calc_btn(parent, cmd):
    ctk.CTkButton(parent, text="  Calculate  ", font=F_CALC,
                  height=44, command=cmd,
                  fg_color="#1e5a8a", hover_color="#174d79").pack(pady=12)


def _copy_tree_to_clipboard(owner, tree):
    cols = list(tree["columns"])
    lines = ["\t".join(cols)]
    for item in tree.get_children():
        values = [str(v) for v in tree.item(item, "values")]
        lines.append("\t".join(values))
    root = owner.winfo_toplevel()
    root.clipboard_clear()
    root.clipboard_append("\n".join(lines))
    root.update_idletasks()


def _phase_display_name(phase_name):
    if not phase_name:
        return "Unknown"
    return phase_name.replace("_", " ").title()


class AppScrollablePage(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(master, **kwargs)
        self.after_idle(self._install_scroll_forwarding)

    def _install_scroll_forwarding(self):
        canvas = getattr(self, "_parent_canvas", None)
        if canvas is None:
            return

        def _page_scroll(units):
            canvas.yview_scroll(units, "units")

        self._bind_descendant_scroll(self, _page_scroll)

    def _bind_descendant_scroll(self, widget, y_scroll):
        if isinstance(widget, ttk.Treeview):
            return
        _bind_wheel_scroll(widget, y_scroll=y_scroll)
        for child in widget.winfo_children():
            self._bind_descendant_scroll(child, y_scroll)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1: State Point  (free input/output variable selection)
# ─────────────────────────────────────────────────────────────────────────────
class StatePointPage(AppScrollablePage):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="State Point Calculator", font=F_TITLE).pack(
            anchor="w", pady=(0, 6))
        _page_hint(self,
            "Enter any two independent properties (e.g. T + P for superheated state, "
            "or T + Q for a point on the saturation curve). "
            "Select the variable type, enter a value and choose its unit for each input, "
            "tick the outputs you want, then press Calculate. "
            "Hover any output checkbox for a physical definition of that property.")

        # ── Fluid ──
        fl_row = ctk.CTkFrame(self, fg_color="transparent")
        fl_row.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(fl_row, text="Fluid:", width=55, font=F_BODY).pack(side="left")
        self._fluid = tk.StringVar(value="R134a")
        ctk.CTkComboBox(fl_row, values=ALL_FLUIDS, variable=self._fluid,
                        width=220, font=F_BODY).pack(side="left", padx=6)

        # ── Two input cards ──
        card_row = ctk.CTkFrame(self, fg_color="transparent")
        card_row.pack(fill="x", pady=(0, 12))
        card_row.columnconfigure((0, 1), weight=1)

        defaults = [("T", "°C", "25"), ("P", "kPa", "770")]
        self._inputs = []   # (key_var, val_entry, unit_var, unit_cb)

        for i, (dk, du, dv) in enumerate(defaults):
            card = ctk.CTkFrame(card_row, corner_radius=10)
            card.grid(row=0, column=i, sticky="nsew",
                      padx=(0, 8) if i == 0 else 0)

            ctk.CTkLabel(card, text=f"Input {i + 1}", font=F_SECTION).grid(
                row=0, column=0, columnspan=3, sticky="w", padx=14, pady=(12, 6))

            key_var  = tk.StringVar(value=dk)
            unit_var = tk.StringVar(value=du)
            val_ent  = ctk.CTkEntry(card, width=130, font=F_BODY,
                                    placeholder_text="value")
            val_ent.insert(0, dv)
            unit_cb  = ctk.CTkComboBox(card, variable=unit_var, width=100,
                                       font=F_BODY, state="readonly")

            # Description label – updated whenever the variable selector changes
            desc_lbl = ctk.CTkLabel(card, text="", text_color="gray55",
                                    font=F_SMALL, wraplength=270,
                                    justify="left", anchor="w")
            desc_lbl.grid(row=3, column=0, columnspan=3,
                          padx=14, pady=(0, 12), sticky="w")

            ctk.CTkLabel(card, text="Variable:", width=75, anchor="w",
                         font=F_BODY).grid(row=1, column=0, padx=(14, 4), pady=4)
            key_cb = ctk.CTkComboBox(
                card, values=list(IVARS.keys()), variable=key_var,
                width=85, font=F_BODY,
                command=lambda v, uv=unit_var, uc=unit_cb, dl=desc_lbl:
                    self._refresh_units(v, uv, uc, dl))
            key_cb.grid(row=1, column=1, padx=4, pady=4, sticky="w")

            ctk.CTkLabel(card, text="Value:", width=55, anchor="w",
                         font=F_BODY).grid(row=2, column=0, padx=(14, 4), pady=4)
            val_ent.grid(row=2, column=1, padx=4, pady=4)
            unit_cb.grid(row=2, column=2, padx=(4, 14), pady=4)

            self._refresh_units(dk, unit_var, unit_cb, desc_lbl)
            unit_var.set(du)
            self._inputs.append((key_var, val_ent, unit_var, unit_cb))

        # ── Output variable checkboxes ──
        out_card = ctk.CTkFrame(self, corner_radius=10)
        out_card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(out_card, text="Output Variables", font=F_SECTION).grid(
            row=0, column=0, columnspan=7, sticky="w", padx=14, pady=(12, 6))

        self._out_vars = {}
        PER_ROW = 4
        for j, (k, name, _) in enumerate(OVARS):
            bv = tk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(out_card, text=f"{k} — {name}", variable=bv,
                                 width=190, font=F_SMALL)
            cb.grid(row=1 + j // PER_ROW, column=j % PER_ROW,
                    padx=10, pady=3, sticky="w")
            if k in VAR_DESC:
                vname, vdesc = VAR_DESC[k]
                Tooltip(cb, f"{vname}\n\n{vdesc}")
            self._out_vars[k] = bv

        btn_row = ctk.CTkFrame(out_card, fg_color="transparent")
        btn_row.grid(row=5, column=0, columnspan=PER_ROW,
                     sticky="w", padx=14, pady=(4, 12))
        ctk.CTkButton(btn_row, text="All",  width=70, height=26, font=F_SMALL,
                      command=lambda: [v.set(True)
                                       for v in self._out_vars.values()]).pack(
                          side="left", padx=(0, 6))
        ctk.CTkButton(btn_row, text="None", width=70, height=26, font=F_SMALL,
                      fg_color="gray30",
                      command=lambda: [v.set(False)
                                       for v in self._out_vars.values()]).pack(
                          side="left")

        # ── Calculate ──
        _calc_btn(self, self._calc)

        # ── Results ──
        ctk.CTkLabel(self, text="Results", font=F_SECTION).pack(
            anchor="w", pady=(0, 4))
        tf, self._tv = make_tree(self, ["Property", "Value"], [190, 530],
                                 height=13)
        tf.pack(fill="both", expand=True)

        # ── P–H Diagram ──
        ctk.CTkLabel(self, text="P–H Diagram", font=F_SECTION).pack(
            anchor="w", pady=(14, 4))
        self._chart = EmbeddedChart(self, figsize=(9, 4.2))
        self._chart.pack(fill="x", pady=(0, 12))

    def _refresh_units(self, key, unit_var, unit_cb, desc_lbl=None):
        if key not in IVARS:
            return
        units = [u for u, _ in IVARS[key][2]]
        unit_cb.configure(values=units)
        unit_var.set(units[1] if len(units) > 1 else units[0])
        if desc_lbl is not None and key in VAR_DESC:
            vname, vdesc = VAR_DESC[key]
            desc_lbl.configure(text=f"{vname} — {vdesc}")

    def _calc(self):
        fluid = self._fluid.get()
        keys, vals = [], []
        try:
            for key_var, val_ent, unit_var, _ in self._inputs:
                k   = key_var.get()
                raw = val_ent.get().strip()
                if not raw:
                    messagebox.showerror("Input Error", f"No value for {k}")
                    return
                v    = float(raw)
                fn   = {u: f for u, f in IVARS[k][2]}[unit_var.get()]
                keys.append(k)
                vals.append(fn(v))
        except (ValueError, KeyError) as e:
            messagebox.showerror("Parse Error", str(e))
            return

        if keys[0] == keys[1]:
            messagebox.showerror("Input Error",
                                 "Both inputs use the same variable")
            return

        rows = []
        for k, name, fmt in OVARS:
            if not self._out_vars[k].get():
                continue
            try:
                v = PropsSI(k, keys[0], vals[0], keys[1], vals[1], fluid)
                rows.append((name, fmt(v)))
            except Exception as e:
                rows.append((name, f"— error: {e}"))
        fill_tree(self._tv, rows)
        self._plot_ph(fluid, keys, vals)

    def _plot_ph(self, fluid, keys, vals):
        if not MPLOK:
            return
        self._chart.clear()
        fig = self._chart.figure()
        ax  = fig.add_subplot(111)
        _style_ax(ax)
        hl, hv, Ps = _sat_dome_ph(fluid)
        if len(hl):
            ax.plot(hl, Ps, color=_C["liq"], lw=1.8, label="Sat. liquid")
            ax.plot(hv, Ps, color=_C["vap"], lw=1.8, label="Sat. vapour")
            ax.fill_betweenx(Ps, hl, hv, alpha=0.07, color=_C["liq"])
        try:
            H = PropsSI("H", keys[0], vals[0], keys[1], vals[1], fluid) / 1e3
            P = PropsSI("P", keys[0], vals[0], keys[1], vals[1], fluid) / 1e3
            ax.scatter([H], [P], color=_C["pt"], s=100, zorder=5,
                       label="State point")
            ax.annotate("  state", xy=(H, P), color=_C["pt"],
                        fontsize=8, va="center")
        except Exception:
            pass
        try:
            ax.set_yscale("log")
        except Exception:
            pass
        ax.set_xlabel("Specific Enthalpy  h  [kJ/kg]")
        ax.set_ylabel("Pressure  P  [kPa]")
        ax.set_title(f"P–H Diagram  —  {fluid}")
        ax.legend(fontsize=8, facecolor=_C["axes"],
                  edgecolor=_C["spine"], labelcolor=_C["fg"])
        fig.tight_layout()
        self._chart.redraw()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2: Saturation Properties
# ─────────────────────────────────────────────────────────────────────────────
class SaturationPage(AppScrollablePage):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Saturation Properties", font=F_TITLE).pack(
            anchor="w", pady=(0, 6))
        _page_hint(self,
            "Look up properties at the liquid–vapor boundary. "
            "Use the radio buttons to fix either Temperature or Pressure, "
            "enter the value and unit, then press Calculate. "
            "Results show saturated-liquid (Q = 0, bubble point) and "
            "saturated-vapor (Q = 1, dew point) side by side. "
            "Q must be between 0 and 1; values above the critical point are not valid.")

        inp = ctk.CTkFrame(self, corner_radius=10)
        inp.pack(fill="x", pady=(0, 12))

        # Row 0: fluid + mode radios
        ctk.CTkLabel(inp, text="Fluid:", width=60, font=F_BODY).grid(
            row=0, column=0, padx=14, pady=12, sticky="w")
        self._fluid = tk.StringVar(value="R134a")
        ctk.CTkComboBox(inp, values=ALL_FLUIDS, variable=self._fluid,
                        width=200, font=F_BODY).grid(
            row=0, column=1, padx=4, pady=12, sticky="w")

        ctk.CTkLabel(inp, text="Fix by:", width=55, font=F_BODY).grid(
            row=0, column=2, padx=14, pady=12, sticky="w")
        self._mode = tk.StringVar(value="T")
        for val, txt, col in [("T", "Temperature", 3), ("P", "Pressure", 4)]:
            ctk.CTkRadioButton(
                inp, text=txt, variable=self._mode, value=val,
                command=self._mode_changed,
                font=F_BODY).grid(row=0, column=col, padx=8, pady=12)

        # Row 1: value + unit
        ctk.CTkLabel(inp, text="Value:", width=60, font=F_BODY).grid(
            row=1, column=0, padx=14, pady=(0, 12), sticky="w")
        self._val = ctk.CTkEntry(inp, width=130, font=F_BODY,
                                 placeholder_text="value")
        self._val.insert(0, "25")
        self._val.grid(row=1, column=1, padx=4, pady=(0, 12), sticky="w")
        self._unit_var = tk.StringVar(value="°C")
        self._unit_cb  = ctk.CTkComboBox(inp, variable=self._unit_var,
                                         width=100, font=F_BODY,
                                         state="readonly")
        self._unit_cb.grid(row=1, column=2, padx=4, pady=(0, 12), sticky="w")
        self._mode_changed()

        _calc_btn(self, self._calc)

        ctk.CTkLabel(self, text="Results", font=F_SECTION).pack(
            anchor="w", pady=(0, 4))
        tf, self._tv = make_tree(
            self,
            ["Property", "Liquid  (Q = 0)", "Vapor  (Q = 1)"],
            [180, 290, 290], height=14)
        tf.pack(fill="both", expand=True)

        # ── Saturation Curves ──
        ctk.CTkLabel(self, text="Saturation Curves", font=F_SECTION).pack(
            anchor="w", pady=(14, 4))
        self._chart = EmbeddedChart(self, figsize=(11, 3.8))
        self._chart.pack(fill="x", pady=(0, 12))

    def _mode_changed(self):
        key   = self._mode.get()
        units = [u for u, _ in IVARS[key][2]]
        self._unit_cb.configure(values=units)
        self._unit_var.set(units[1] if len(units) > 1 else units[0])

    def _calc(self):
        fluid = self._fluid.get()
        key   = self._mode.get()
        try:
            raw = float(self._val.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid value")
            return
        fn     = {u: f for u, f in IVARS[key][2]}[self._unit_var.get()]
        val_si = fn(raw)
        Tc = PropsSI("Tcrit", fluid)
        Pc = PropsSI("Pcrit", fluid)
        if key == "T" and val_si >= Tc:
            messagebox.showerror("Error",
                f"T = {val_si:.2f} K ≥ Tcrit = {Tc:.2f} K")
            return
        if key == "P" and val_si >= Pc:
            messagebox.showerror("Error",
                f"P = {val_si:.0f} Pa ≥ Pcrit = {Pc:.0f} Pa")
            return

        rows = []
        for k, name, fmt in OVARS:
            if k == "Q":
                continue
            try:
                liq = PropsSI(k, key, val_si, "Q", 0, fluid)
                vap = PropsSI(k, key, val_si, "Q", 1, fluid)
                rows.append((name, fmt(liq), fmt(vap)))
            except Exception:
                rows.append((name, "—", "—"))
        fill_tree(self._tv, rows)
        self._plot_sat(fluid, key, val_si)

    def _plot_sat(self, fluid, key, val_si):
        if not MPLOK:
            return
        self._chart.clear()
        fig = self._chart.figure()
        try:
            Tc    = PropsSI("Tcrit", fluid)
            Tt    = max(PropsSI("Ttriple", fluid) + 1.0, 160.0)
            Ts    = np.linspace(Tt, Tc - 0.2, 100)
            T_C   = Ts - 273.15
            Ps    = [PropsSI("P","T",T,"Q",0,fluid)/1e3 for T in Ts]
            rl    = [PropsSI("D","T",T,"Q",0,fluid)     for T in Ts]
            rv    = [PropsSI("D","T",T,"Q",1,fluid)     for T in Ts]
            dhvap = [(PropsSI("H","T",T,"Q",1,fluid) -
                      PropsSI("H","T",T,"Q",0,fluid))/1e3 for T in Ts]
        except Exception:
            self._chart.redraw(); return
        axes = [fig.add_subplot(1, 3, i+1) for i in range(3)]
        for ax in axes:
            _style_ax(ax)
        axes[0].plot(T_C, Ps,    color=_C["liq"], lw=2)
        axes[0].set_xlabel("T [°C]"); axes[0].set_ylabel("P_sat [kPa]")
        axes[0].set_title("Vapour Pressure")
        axes[1].plot(T_C, rl,    color=_C["liq"], lw=2, label="Liquid")
        axes[1].plot(T_C, rv,    color=_C["vap"], lw=2, label="Vapour")
        axes[1].set_xlabel("T [°C]"); axes[1].set_ylabel("ρ [kg/m³]")
        axes[1].set_title("Density")
        axes[1].legend(fontsize=7, facecolor=_C["axes"],
                       edgecolor=_C["spine"], labelcolor=_C["fg"])
        axes[2].plot(T_C, dhvap, color=_C["cycle"], lw=2)
        axes[2].set_xlabel("T [°C]"); axes[2].set_ylabel("ΔH_vap [kJ/kg]")
        axes[2].set_title("Latent Heat")
        try:
            T_cur = (val_si - 273.15) if key == "T" else (
                PropsSI("T","P",val_si,"Q",0,fluid) - 273.15)
            for ax in axes:
                ax.axvline(T_cur, color=_C["pt"], lw=1.2, ls="--",
                           alpha=0.85, label="Current")
        except Exception:
            pass
        fig.suptitle(f"{fluid}  —  Saturation Properties",
                     color=_C["fg"], fontsize=10)
        fig.tight_layout()
        self._chart.redraw()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3: Refrigeration Cycle
# ─────────────────────────────────────────────────────────────────────────────
class CyclePage(AppScrollablePage):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Vapor-Compression Refrigeration Cycle",
                     font=F_TITLE).pack(anchor="w", pady=(0, 6))
        _page_hint(self,
            "Models a single-stage vapor-compression cycle (1 = comp. inlet, "
            "2 = comp. exit, 3 = cond. exit, 4 = exp. valve exit). "
            "Enter the saturation temperatures at evaporator and condenser, "
            "superheat at the compressor inlet (K above sat. vapor), "
            "subcooling at condenser exit (K below sat. liquid), and isentropic efficiency. "
            "Hover any label for its engineering definition.")

        inp = ctk.CTkFrame(self, corner_radius=10)
        inp.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(inp, text="Cycle Inputs", font=F_SECTION).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=14, pady=(12, 6))

        fields = [
            ("Fluid",                 "fluid",  "R134a", FIELD_DESC["fluid"]),
            ("Evaporator temp [°C]",  "T_evap", "-10",   FIELD_DESC["T_evap"]),
            ("Condenser temp [°C]",   "T_cond", "40",    FIELD_DESC["T_cond"]),
            ("Superheat [K]",         "SH",     "5",     FIELD_DESC["SH"]),
            ("Subcooling [K]",        "SC",     "5",     FIELD_DESC["SC"]),
            ("η isentropic (comp.)",  "eta_c",  "0.75",  FIELD_DESC["eta_c"]),
        ]
        self._p = {}
        for i, (lbl, key, default, tt) in enumerate(fields):
            r, c = divmod(i, 2)
            lbl_w = ctk.CTkLabel(inp, text=lbl, anchor="w", font=F_BODY)
            lbl_w.grid(row=r + 1, column=c * 2, padx=(14, 4), pady=6, sticky="w")
            Tooltip(lbl_w, tt)
            if key == "fluid":
                var = tk.StringVar(value=default)
                ctk.CTkComboBox(inp, values=ALL_FLUIDS, variable=var,
                                width=200, font=F_BODY).grid(
                    row=r + 1, column=c * 2 + 1, padx=(0, 14), pady=6)
                self._p[key] = var
            else:
                ent = ctk.CTkEntry(inp, width=120, font=F_BODY)
                ent.insert(0, default)
                ent.grid(row=r + 1, column=c * 2 + 1, padx=(0, 14), pady=6)
                self._p[key] = ent

        _calc_btn(self, self._calc)

        ctk.CTkLabel(self, text="State Points", font=F_SECTION).pack(
            anchor="w", pady=(0, 4))
        tf1, self._tv_st = make_tree(
            self,
            ["State", "Description", "T (°C)", "P (kPa)", "H (kJ/kg)",
             "S (kJ/kg·K)", "Q"],
            [60, 170, 90, 90, 105, 120, 60], height=6)
        tf1.pack(fill="x")

        ctk.CTkLabel(self, text="Performance", font=F_SECTION).pack(
            anchor="w", pady=(10, 4))
        tf2, self._tv_pf = make_tree(self, ["Parameter", "Value"],
                                     [240, 320], height=10)
        tf2.pack(fill="both", expand=True)

        # ── P–H Diagram ──
        ctk.CTkLabel(self, text="P–H Diagram", font=F_SECTION).pack(
            anchor="w", pady=(14, 4))
        self._chart = EmbeddedChart(self, figsize=(9, 4.8))
        self._chart.pack(fill="x", pady=(0, 12))

    def _calc(self):
        fluid = self._p["fluid"].get()
        try:
            T_evap = float(self._p["T_evap"].get())
            T_cond = float(self._p["T_cond"].get())
            SH     = float(self._p["SH"].get())
            SC     = float(self._p["SC"].get())
            eta_c  = float(self._p["eta_c"].get())
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        Tev = T_evap + 273.15
        Tco = T_cond + 273.15
        Tc  = PropsSI("Tcrit", fluid)
        if Tev >= Tc or Tco >= Tc:
            messagebox.showerror(
                "Error",
                f"Temperature exceeds critical point ({Tc - 273.15:.1f} °C)")
            return

        try:
            Pev  = PropsSI("P", "T", Tev, "Q", 1, fluid)
            Pco  = PropsSI("P", "T", Tco, "Q", 1, fluid)
            T1   = Tev + SH
            H1   = PropsSI("H", "T", T1, "P", Pev, fluid)
            S1   = PropsSI("S", "T", T1, "P", Pev, fluid)
            H2s  = PropsSI("H", "P", Pco, "S", S1, fluid)
            H2   = H1 + (H2s - H1) / eta_c
            T2   = PropsSI("T", "P", Pco, "H", H2, fluid)
            S2   = PropsSI("S", "P", Pco, "H", H2, fluid)
            T2s  = PropsSI("T", "P", Pco, "S", S1, fluid)
            T3   = Tco - SC
            H3   = PropsSI("H", "T", T3, "P", Pco, fluid)
            S3   = PropsSI("S", "T", T3, "P", Pco, fluid)
            H4   = H3
            Q4   = PropsSI("Q", "P", Pev, "H", H4, fluid)
            q    = H1 - H4
            w    = H2 - H1
            qco  = H2 - H3
        except Exception as e:
            messagebox.showerror("CoolProp Error", str(e))
            return

        def qs(v):
            return f"{v:.4f}" if 0 <= v <= 1 else "—"

        states = [
            ("1",  "Comp. inlet (SH vap.)",
             f"{T1-273.15:.2f}", f"{Pev/1e3:.2f}",
             f"{H1/1e3:.3f}", f"{S1/1e3:.5f}", "—"),
            ("2s", "Isentropic exit",
             f"{T2s-273.15:.2f}", f"{Pco/1e3:.2f}",
             f"{H2s/1e3:.3f}", f"{S1/1e3:.5f}", "—"),
            ("2",  "Actual comp. exit",
             f"{T2-273.15:.2f}", f"{Pco/1e3:.2f}",
             f"{H2/1e3:.3f}", f"{S2/1e3:.5f}", "—"),
            ("3",  "Cond. exit (SC liq.)",
             f"{T3-273.15:.2f}", f"{Pco/1e3:.2f}",
             f"{H3/1e3:.3f}", f"{S3/1e3:.5f}", "0"),
            ("4",  "Exp. valve exit",
             f"{Tev-273.15:.2f}", f"{Pev/1e3:.2f}",
             f"{H4/1e3:.3f}", "—", qs(Q4)),
        ]
        fill_tree(self._tv_st, states)

        perf = [
            ("Evaporator pressure",     f"{Pev/1e3:.3f} kPa"),
            ("Condenser pressure",      f"{Pco/1e3:.3f} kPa"),
            ("Pressure ratio",          f"{Pco/Pev:.4f}"),
            ("Refrigeration effect",    f"{q/1e3:.4f} kJ/kg"),
            ("Compressor work",         f"{w/1e3:.4f} kJ/kg"),
            ("Heat rejection (cond.)",  f"{qco/1e3:.4f} kJ/kg"),
            ("COP  (cooling)",          f"{q/w:.4f}"),
            ("COP  (heat pump)",        f"{qco/w:.4f}"),
            ("Flash quality at exp.",   f"{Q4:.4f}"),
        ]
        fill_tree(self._tv_pf, perf)
        self._plot_ph(fluid, H1, H2, H2s, H3, H4, S1, Pev, Pco)

    def _plot_ph(self, fluid, H1, H2, H2s, H3, H4, S1, Pev, Pco):
        if not MPLOK:
            return
        self._chart.clear()
        fig = self._chart.figure()
        ax  = fig.add_subplot(111)
        _style_ax(ax)
        hl, hv, Ps = _sat_dome_ph(fluid)
        if len(hl):
            ax.plot(hl, Ps, color=_C["liq"], lw=1.8, label="Sat. liquid")
            ax.plot(hv, Ps, color=_C["vap"], lw=1.8, label="Sat. vapour")
            ax.fill_betweenx(Ps, hl, hv, alpha=0.07, color=_C["liq"])
        try:
            P_arr = np.linspace(Pev, Pco, 40)
            h_is  = []
            for Pp in P_arr:
                try:
                    h_is.append(PropsSI("H","P",Pp,"S",S1,fluid) / 1e3)
                except Exception:
                    h_is.append(None)
            h_ok = [h for h in h_is if h is not None]
            P_ok = [P_arr[i] / 1e3 for i, h in enumerate(h_is) if h is not None]
            ax.plot(h_ok, P_ok, color=_C["pt"], lw=1.2, ls="--",
                    alpha=0.65, label="Isentrope 1→2s")
        except Exception:
            pass
        hs = [H4, H1, H2, H3, H4]
        Pp = [Pev, Pev, Pco, Pco, Pev]
        ax.plot([h / 1e3 for h in hs], [p / 1e3 for p in Pp],
                color=_C["cycle"], lw=2.2, zorder=4, label="Cycle")
        for h, P, lbl in [(H1,Pev,"1"),(H2,Pco,"2"),(H2s,Pco,"2s"),
                          (H3,Pco,"3"),(H4,Pev,"4")]:
            ax.scatter([h/1e3], [P/1e3], color=_C["pt"], s=60, zorder=5)
            ax.annotate(f"  {lbl}", xy=(h/1e3, P/1e3), color=_C["pt"],
                        fontsize=9, fontweight="bold",
                        xytext=(3,3), textcoords="offset points")
        try:
            ax.set_yscale("log")
        except Exception:
            pass
        ax.set_xlabel("Specific Enthalpy  h  [kJ/kg]")
        ax.set_ylabel("Pressure  P  [kPa]")
        ax.set_title(f"P–H Diagram  —  {fluid}")
        ax.legend(fontsize=8, facecolor=_C["axes"],
                  edgecolor=_C["spine"], labelcolor=_C["fg"])
        fig.tight_layout()
        self._chart.redraw()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4: System Power & Flow Sizing
# ─────────────────────────────────────────────────────────────────────────────
class SizingPage(AppScrollablePage):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._last_Qcool = None
        self._last_Wel   = None
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="System Power & Flow Sizing",
                     font=F_TITLE).pack(anchor="w", pady=(0, 6))
        _page_hint(self,
            "Converts cycle performance into physical equipment sizing. "
            "Enter a target cooling capacity (kW) and the same cycle parameters as the Refrig. Cycle page. "
            "Press Calculate to get mass flow rate, compressor shaft and electrical power, and COP. "
            "Then fill in the secondary-loop fields (chilled-water ΔT, system head, pump efficiency) "
            "and press Calculate Secondary Loop to size the pump and find total system electrical draw.")

        inp = ctk.CTkFrame(self, corner_radius=10)
        inp.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(inp, text="Inputs", font=F_SECTION).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=14, pady=(12, 6))

        fields = [
            ("Fluid",                  "fluid",  "R134a", FIELD_DESC["fluid"]),
            ("Cooling capacity [kW]",  "Q_kw",   "5",     FIELD_DESC["Q_kw"]),
            ("Evap. temp [°C]",        "T_evap", "-10",   FIELD_DESC["T_evap"]),
            ("Cond. temp [°C]",        "T_cond", "40",    FIELD_DESC["T_cond"]),
            ("Superheat [K]",          "SH",     "5",     FIELD_DESC["SH"]),
            ("Subcooling [K]",         "SC",     "5",     FIELD_DESC["SC"]),
            ("η isentropic (comp.)",   "eta_c",  "0.75",  FIELD_DESC["eta_c"]),
            ("η motor",                "eta_m",  "0.92",  FIELD_DESC["eta_m"]),
        ]
        self._p = {}
        for i, (lbl, key, default, tt) in enumerate(fields):
            r, c = divmod(i, 2)
            lbl_w = ctk.CTkLabel(inp, text=lbl, anchor="w", font=F_BODY)
            lbl_w.grid(row=r + 1, column=c * 2, padx=(14, 4), pady=6, sticky="w")
            Tooltip(lbl_w, tt)
            if key == "fluid":
                var = tk.StringVar(value=default)
                ctk.CTkComboBox(inp, values=ALL_FLUIDS, variable=var,
                                width=200, font=F_BODY).grid(
                    row=r + 1, column=c * 2 + 1, padx=(0, 14), pady=6)
                self._p[key] = var
            else:
                ent = ctk.CTkEntry(inp, width=120, font=F_BODY)
                ent.insert(0, default)
                ent.grid(row=r + 1, column=c * 2 + 1, padx=(0, 14), pady=6)
                self._p[key] = ent

        _calc_btn(self, self._calc)

        ctk.CTkLabel(self, text="Refrigerant Side", font=F_SECTION).pack(
            anchor="w", pady=(0, 4))
        tf, self._tv_ref = make_tree(self, ["Parameter", "Value"],
                                     [260, 340], height=12)
        tf.pack(fill="x", pady=(0, 16))

        # ── Secondary loop ──
        sec = ctk.CTkFrame(self, corner_radius=10)
        sec.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(sec, text="Secondary Loop  (Chilled Water / Brine)",
                     font=F_SECTION).grid(
            row=0, column=0, columnspan=6, sticky="w", padx=14, pady=(12, 6))

        sec_fields = [
            ("ΔT across evap. [K]", "dT",    "5",     FIELD_DESC["dT"]),
            ("System head [m]",     "head",  "10",    FIELD_DESC["head"]),
            ("η pump",              "eta_p", "0.65",  FIELD_DESC["eta_p"]),
        ]
        self._sp = {}
        for i, (lbl, key, default, tt) in enumerate(sec_fields):
            lbl_w = ctk.CTkLabel(sec, text=lbl, anchor="w", font=F_BODY)
            lbl_w.grid(row=1, column=i * 2, padx=(14, 4), pady=(0, 12), sticky="w")
            Tooltip(lbl_w, tt)
            ent = ctk.CTkEntry(sec, width=100, font=F_BODY)
            ent.insert(0, default)
            ent.grid(row=1, column=i * 2 + 1, padx=(0, 14), pady=(0, 12))
            self._sp[key] = ent

        ctk.CTkButton(self, text="  Calculate Secondary Loop  ",
                      font=F_BODY, height=38,
                      command=self._calc_sec).pack(pady=(0, 12))

        ctk.CTkLabel(self, text="Secondary Loop Results", font=F_SECTION).pack(
            anchor="w", pady=(0, 4))
        tf2, self._tv_sec = make_tree(self, ["Parameter", "Value"],
                                      [260, 340], height=8)
        tf2.pack(fill="both", expand=True)

        # ── Performance Charts ──
        ctk.CTkLabel(self, text="Performance Charts", font=F_SECTION).pack(
            anchor="w", pady=(14, 4))
        self._chart = EmbeddedChart(self, figsize=(11, 4.2))
        self._chart.pack(fill="x", pady=(0, 12))

    def _calc(self):
        fluid = self._p["fluid"].get()
        try:
            Q_kw  = float(self._p["Q_kw"].get())
            T_evap = float(self._p["T_evap"].get())
            T_cond = float(self._p["T_cond"].get())
            SH    = float(self._p["SH"].get())
            SC    = float(self._p["SC"].get())
            eta_c = float(self._p["eta_c"].get())
            eta_m = float(self._p["eta_m"].get())
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        Q_cool = Q_kw * 1000
        Tev = T_evap + 273.15
        Tco = T_cond + 273.15
        Tc  = PropsSI("Tcrit", fluid)
        if Tev >= Tc or Tco >= Tc:
            messagebox.showerror("Error", "Temperature ≥ critical point")
            return

        try:
            Pev  = PropsSI("P", "T", Tev, "Q", 1, fluid)
            Pco  = PropsSI("P", "T", Tco, "Q", 1, fluid)
            T1   = Tev + SH
            H1   = PropsSI("H", "T", T1,  "P", Pev, fluid)
            S1   = PropsSI("S", "T", T1,  "P", Pev, fluid)
            H2s  = PropsSI("H", "P", Pco, "S", S1,  fluid)
            H2   = H1 + (H2s - H1) / eta_c
            T3   = Tco - SC
            H3   = PropsSI("H", "T", T3,  "P", Pco, fluid)
            H4   = H3
            q    = H1 - H4
            w    = H2 - H1
            qco  = H2 - H3
        except Exception as e:
            messagebox.showerror("CoolProp Error", str(e))
            return

        if q <= 0:
            messagebox.showerror(
                "Error", "Negative refrigeration effect — check temperatures")
            return

        m_dot   = Q_cool / q
        W_sh    = m_dot * w
        W_el    = W_sh / eta_m
        Q_cond  = m_dot * qco
        self._last_Qcool = Q_cool
        self._last_Wel   = W_el

        rows = [
            ("Cooling capacity",          f"{Q_cool/1000:.4f} kW"),
            ("Mass flow rate",            f"{m_dot*1000:.4f} g/s   ({m_dot:.6f} kg/s)"),
            ("Refrigeration effect",      f"{q/1000:.4f} kJ/kg"),
            ("Compressor work",           f"{w/1000:.4f} kJ/kg"),
            ("Compressor shaft power",    f"{W_sh/1000:.4f} kW"),
            ("Compressor electrical in.", f"{W_el/1000:.4f} kW"),
            ("Condenser heat rejection",  f"{Q_cond/1000:.4f} kW"),
            ("COP  (cooling)",            f"{q/w:.4f}"),
            ("COP  (heat pump)",          f"{qco/w:.4f}"),
            ("Pressure ratio",            f"{Pco/Pev:.4f}"),
            ("Evap. pressure",            f"{Pev/1000:.3f} kPa"),
            ("Cond. pressure",            f"{Pco/1000:.3f} kPa"),
        ]
        fill_tree(self._tv_ref, rows)
        self._plot(fluid, T_evap, T_cond, SH, SC, eta_c,
                   Q_cool, W_sh, W_el, Q_cond)

    def _calc_sec(self):
        if self._last_Qcool is None:
            messagebox.showinfo("Info", "Calculate the refrigerant side first")
            return
        try:
            dT    = float(self._sp["dT"].get())
            head  = float(self._sp["head"].get())
            eta_p = float(self._sp["eta_p"].get())
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        try:
            rho = PropsSI("D", "T", 278.15, "P", 101325, "Water")
            cp  = PropsSI("C", "T", 278.15, "P", 101325, "Water")
        except Exception:
            rho, cp = 999.0, 4182.0

        m_s  = self._last_Qcool / (cp * dT)
        V_s  = m_s / rho
        W_p  = rho * 9.81 * V_s * head
        W_ep = W_p / eta_p
        W_t  = (self._last_Wel or 0) + W_ep

        rows = [
            ("Secondary fluid",       "Water"),
            ("Mass flow rate",        f"{m_s*1000:.4f} g/s   ({m_s:.6f} kg/s)"),
            ("Volumetric flow rate",  f"{V_s*1000:.4f} L/s   ({V_s*3600:.4f} m³/h)"),
            ("Pump head",             f"{head:.2f} m"),
            ("Pump shaft power",      f"{W_p:.4f} W   ({W_p/1000:.4f} kW)"),
            ("Pump electrical input", f"{W_ep:.4f} W   ({W_ep/1000:.4f} kW)"),
            ("Total electrical in.",  f"{W_t/1000:.4f} kW"),
            ("System EER",            f"{self._last_Qcool/W_t:.4f}"),
        ]
        fill_tree(self._tv_sec, rows)

    def _plot(self, fluid, T_evap, T_cond, SH, SC, eta_c,
              Q_cool, W_sh, W_el, Q_cond):
        if not MPLOK:
            return
        self._chart.clear()
        fig = self._chart.figure()
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        _style_ax(ax1); _style_ax(ax2)
        try:
            Tc  = PropsSI("Tcrit", fluid)
            Tco = T_cond + 273.15
            T_arr = np.linspace(-45.0, T_cond - 3.0, 60)
            cops  = []
            for T_e in T_arr:
                try:
                    Tev  = T_e + 273.15
                    if Tev >= Tco or Tev >= Tc or Tco >= Tc:
                        cops.append(float("nan")); continue
                    Pev_ = PropsSI("P","T",Tev,"Q",1,fluid)
                    Pco_ = PropsSI("P","T",Tco,"Q",1,fluid)
                    H1_  = PropsSI("H","T",Tev+SH,"P",Pev_,fluid)
                    S1_  = PropsSI("S","T",Tev+SH,"P",Pev_,fluid)
                    H2s_ = PropsSI("H","P",Pco_,"S",S1_,fluid)
                    H2_  = H1_ + (H2s_ - H1_) / eta_c
                    H3_  = PropsSI("H","T",Tco - SC,"P",Pco_,fluid)
                    q_   = H1_ - H3_; w_ = H2_ - H1_
                    cops.append(q_ / w_ if w_ > 0 and q_ > 0 else float("nan"))
                except Exception:
                    cops.append(float("nan"))
            ax1.plot(T_arr, cops, color=_C["cop"], lw=2)
            ax1.axvline(T_evap, color=_C["pt"], lw=1.5, ls="--",
                        label=f"Current  ({T_evap:.1f} °C)")
            ax1.set_xlabel("Evap. Temperature [°C]")
            ax1.set_ylabel("COP  (Cooling)")
            ax1.set_title("COP  vs  T_evap")
            ax1.legend(fontsize=8, facecolor=_C["axes"],
                       edgecolor=_C["spine"], labelcolor=_C["fg"])
        except Exception:
            pass
        labels = ["Cooling\nCapacity", "Comp.\nShaft",
                  "Comp.\nElectrical", "Heat\nRejection"]
        values = [Q_cool / 1e3, W_sh / 1e3, W_el / 1e3, Q_cond / 1e3]
        cols   = [_C["cop"], _C["liq"], _C["pwr"], _C["hi"]]
        bars   = ax2.bar(labels, values, color=cols, alpha=0.85,
                         edgecolor=_C["spine"], linewidth=0.8)
        top = max(values) if values else 1
        for bar, val in zip(bars, values):
            ax2.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + top * 0.01,
                     f"{val:.2f}", ha="center", va="bottom",
                     color=_C["fg"], fontsize=8)
        ax2.set_ylabel("Power [kW]"); ax2.set_title("Power Breakdown")
        fig.tight_layout()
        self._chart.redraw()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5: Capillary Tube Sizing
# ─────────────────────────────────────────────────────────────────────────────
class CapTubePage(AppScrollablePage):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Capillary Tube Sizing", font=F_TITLE).pack(
            anchor="w", pady=(0, 6))
        _page_hint(self,
            "Adiabatic, homogeneous-equilibrium model (isenthalpic flow, Churchill 1977 friction factor). "
            "Mode \"Find tube length\" returns the required length for a given inner diameter — "
            "use this when the tube diameter is already chosen or stocked. "
            "Mode \"Diameter scan\" sweeps 0.5 – 3.1 mm in 0.1 mm steps to find the diameter "
            "closest to a target length. \u26a0 means the flow is choked; enlarge the tube or reduce mass flow.")

        # ── Conditions card ──
        inp = ctk.CTkFrame(self, corner_radius=10)
        inp.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(inp, text="Conditions", font=F_SECTION).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=14, pady=(12, 6))

        fields = [
            ("Fluid",                  "fluid",  "R134a",  FIELD_DESC["fluid"]),
            ("Condensing temp [°C]",   "T_cond", "40",     FIELD_DESC["T_cond"]),
            ("Subcooling [K]",         "SC",     "5",      FIELD_DESC["SC"]),
            ("Evaporating temp [°C]",  "T_evap", "-10",    FIELD_DESC["T_evap"]),
            ("Mass flow rate [kg/s]",  "m_dot",  "0.005",  FIELD_DESC["m_dot"]),
        ]
        self._p = {}
        for i, (lbl, key, default, tt) in enumerate(fields):
            r, c = divmod(i, 2)
            lbl_w = ctk.CTkLabel(inp, text=lbl, anchor="w", font=F_BODY)
            lbl_w.grid(row=r + 1, column=c * 2, padx=(14, 4), pady=6, sticky="w")
            Tooltip(lbl_w, tt)
            if key == "fluid":
                var = tk.StringVar(value=default)
                ctk.CTkComboBox(inp, values=ALL_FLUIDS, variable=var,
                                width=200, font=F_BODY).grid(
                    row=r + 1, column=c * 2 + 1, padx=(0, 14), pady=6)
                self._p[key] = var
            else:
                ent = ctk.CTkEntry(inp, width=120, font=F_BODY)
                ent.insert(0, default)
                ent.grid(row=r + 1, column=c * 2 + 1, padx=(0, 14), pady=6)
                self._p[key] = ent

        # ── Mode card ──
        mcard = ctk.CTkFrame(self, corner_radius=10)
        mcard.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(mcard, text="Mode", font=F_SECTION).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=14, pady=(12, 6))

        self._mode = tk.StringVar(value="L")
        ctk.CTkRadioButton(
            mcard, text="Find tube length  (given inner diameter)",
            variable=self._mode, value="L",
            font=F_BODY).grid(row=1, column=0, padx=14, pady=(0, 6), sticky="w")
        ctk.CTkRadioButton(
            mcard, text="Diameter scan table  (for a target length)",
            variable=self._mode, value="D",
            font=F_BODY).grid(row=1, column=1, padx=14, pady=(0, 6), sticky="w")

        val_row = ctk.CTkFrame(mcard, fg_color="transparent")
        val_row.grid(row=2, column=0, columnspan=2, sticky="w",
                     padx=14, pady=(0, 12))
        ctk.CTkLabel(val_row, text="Diameter [mm]:", font=F_BODY).pack(
            side="left")
        self._D_ent = ctk.CTkEntry(val_row, width=80, font=F_BODY)
        self._D_ent.insert(0, "0.8")
        self._D_ent.pack(side="left", padx=(4, 20))
        ctk.CTkLabel(val_row, text="Target length [m]:", font=F_BODY).pack(
            side="left")
        self._L_ent = ctk.CTkEntry(val_row, width=80, font=F_BODY)
        self._L_ent.insert(0, "2.0")
        self._L_ent.pack(side="left", padx=4)

        _calc_btn(self, self._calc)

        # ── Two result tables (one shown at a time) ──
        ctk.CTkLabel(self, text="Results", font=F_SECTION).pack(
            anchor="w", pady=(0, 4))
        self._tf_L, self._tv_L = make_tree(
            self, ["Parameter", "Value"], [240, 480], height=10)
        self._tf_D, self._tv_D = make_tree(
            self,
            ["D (mm)", "G  (kg/m²s)", "Computed L (m)", "Note"],
            [90, 140, 160, 260], height=28)
        self._tf_L.pack(fill="both", expand=True)

        # ── Profile Chart ──
        ctk.CTkLabel(self, text="Profile Chart", font=F_SECTION).pack(
            anchor="w", pady=(14, 4))
        self._chart = EmbeddedChart(self, figsize=(10, 4.2))
        self._chart.pack(fill="x", pady=(0, 12))

    # -- Helpers --
    def _get_cycle_pressures(self, fluid):
        T_cond = float(self._p["T_cond"].get())
        T_evap = float(self._p["T_evap"].get())
        SC     = float(self._p["SC"].get())
        P_in   = PropsSI("P", "T", T_cond + 273.15, "Q", 0, fluid)
        P_out  = PropsSI("P", "T", T_evap + 273.15, "Q", 1, fluid)
        T_sat  = PropsSI("T", "P", P_in, "Q", 0, fluid)
        T_in   = T_sat - SC
        h_in   = PropsSI("H", "T", T_in, "P", P_in, fluid)
        return P_in, P_out, T_in, h_in

    def _calc(self):
        fluid = self._p["fluid"].get()
        try:
            m_dot = float(self._p["m_dot"].get())
            P_in, P_out, T_in, h_in = self._get_cycle_pressures(fluid)
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e))
            return

        mode = self._mode.get()

        if mode == "L":
            try:
                D_mm = float(self._D_ent.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid diameter")
                return
            D = D_mm / 1e3
            A = math.pi * D**2 / 4
            G = m_dot / A
            rho_in = _rho_ph(fluid, P_in, h_in) or 1
            v_in   = G / rho_in
            L, choked, P_choke = cap_tube_length(fluid, P_in, h_in, P_out,
                                                  G, D)
            rows = [
                ("Refrigerant",         fluid),
                ("Cond. pressure",      f"{P_in/1000:.3f} kPa"),
                ("Evap. pressure",      f"{P_out/1000:.3f} kPa"),
                ("Pressure ratio",      f"{P_in/P_out:.3f}"),
                ("Inlet temperature",   f"{T_in - 273.15:.2f} °C"),
                ("Inlet enthalpy",      f"{h_in/1000:.4f} kJ/kg"),
                ("Mass flow rate",      f"{m_dot*1000:.4f} g/s"),
                ("Tube inner dia.",     f"{D_mm:.2f} mm"),
                ("Mass flux G",         f"{G:.2f} kg/m²s"),
                ("Inlet velocity",      f"{v_in:.4f} m/s"),
                ("Required length",     f"{L:.4f} m   ({L*100:.2f} cm)"),
                ("Flow condition",      "⚠ CHOKED — reduce flow or enlarge tube"
                                        if choked else "✓ Subcritical"),
            ]
            if choked:
                rows.append(("Choke pressure",
                              f"{P_choke/1000:.2f} kPa"))

            self._tf_D.pack_forget()
            self._tf_L.pack(fill="both", expand=True)
            fill_tree(self._tv_L, rows)
            self._plot_L(fluid, P_in, h_in, P_out, G, D)

        else:  # diameter scan
            try:
                L_target = float(self._L_ent.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid target length")
                return

            d_rows = []
            for D_mm_10 in range(5, 32):   # 0.5 mm to 3.1 mm in 0.1 mm steps
                D_mm = D_mm_10 / 10
                D    = D_mm / 1e3
                A    = math.pi * D**2 / 4
                G    = m_dot / A
                L, choked, _ = cap_tube_length(fluid, P_in, h_in, P_out, G, D)
                close = (abs(L - L_target) / max(L_target, 1e-9) < 0.05
                         if not choked else False)
                note  = ("⚠ CHOKED" if choked
                          else ("← closest match" if close else ""))
                d_rows.append((f"{D_mm:.1f}", f"{G:.0f}",
                                f"{L:.4f}", note))

            self._tf_L.pack_forget()
            self._tf_D.pack(fill="both", expand=True)
            fill_tree(self._tv_D, d_rows)
            self._plot_D(d_rows)

    def _plot_L(self, fluid, P_in, h_in, P_out, G, D):
        if not MPLOK:
            return
        self._chart.clear()
        fig = self._chart.figure()
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        _style_ax(ax1); _style_ax(ax2)
        xs, Ps, qs = _cap_tube_profile(fluid, P_in, h_in, P_out, G, D)
        ax1.plot(xs * 100, Ps, color=_C["liq"], lw=2)
        ax1.axhline(P_out / 1e3, color=_C["hi"], lw=1.2, ls="--",
                    alpha=0.7, label="P_evap")
        ax1.set_xlabel("Position [cm]"); ax1.set_ylabel("Pressure [kPa]")
        ax1.set_title("Pressure Profile")
        ax1.legend(fontsize=8, facecolor=_C["axes"],
                   edgecolor=_C["spine"], labelcolor=_C["fg"])
        if len(qs) > 0:
            x_q   = xs[1:len(qs) + 1]
            q_arr = np.where(np.array(qs) >= 0, np.array(qs, dtype=float), np.nan)
            ax2.plot(x_q * 100, q_arr, color=_C["vap"], lw=2)
            ax2.axhline(0, color=_C["liq"], lw=0.8, ls="--", alpha=0.5)
            ax2.axhline(1, color=_C["vap"], lw=0.8, ls="--", alpha=0.5)
        ax2.set_xlabel("Position [cm]"); ax2.set_ylabel("Vapour Quality")
        ax2.set_title("Quality Profile"); ax2.set_ylim(-0.05, 1.1)
        fig.tight_layout()
        self._chart.redraw()

    def _plot_D(self, d_rows):
        if not MPLOK:
            return
        self._chart.clear()
        fig = self._chart.figure()
        ax  = fig.add_subplot(111)
        _style_ax(ax)
        Dv, Lv, Dc, Lc = [], [], [], []
        for row in d_rows:
            D_mm  = float(row[0])
            L_val = float(row[2])
            note  = row[3]
            if "CHOKED" in note:
                Dc.append(D_mm); Lc.append(L_val)
            else:
                Dv.append(D_mm); Lv.append(L_val)
        if Dv:
            ax.plot(Dv, Lv, color=_C["cycle"], lw=2, marker="o", ms=5, label="OK")
        if Dc:
            ax.scatter(Dc, Lc, color=_C["hi"], s=70, marker="x",
                       lw=2, label="Choked", zorder=5)
        ax.set_xlabel("Inner Diameter  [mm]")
        ax.set_ylabel("Required Length  [m]")
        ax.set_title("Required Length  vs  Diameter")
        if Dc or Dv:
            ax.legend(fontsize=8, facecolor=_C["axes"],
                      edgecolor=_C["spine"], labelcolor=_C["fg"])
        fig.tight_layout()
        self._chart.redraw()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 6: Fluid Reference Data
# ─────────────────────────────────────────────────────────────────────────────
class FluidInfoPage(AppScrollablePage):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._sat_table_data = {col: [] for col in SAT_TABLE_COLUMNS}
        self._last_fluid = None
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Fluid Reference Data", font=F_TITLE).pack(
            anchor="w", pady=(0, 6))
        _page_hint(self,
            "Browse critical-point constants, triple-point data, normal boiling point, "
            "and a 30-row saturation table for any fluid in CoolProp's library. "
            "Select a fluid from the dropdown and press Show. "
            "Scroll right in the saturation table to see enthalpy, density, and latent-heat columns. "
            "Use the graph controls under the table to plot any two columns against each other. "
            "The four charts below trace vapour pressure, density, enthalpy, and thermal conductivity "
            "across the full saturation range.")

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(row, text="Fluid:", width=55, font=F_BODY).pack(
            side="left")
        self._fluid = tk.StringVar(value="R134a")
        ctk.CTkComboBox(row, values=ALL_FLUIDS, variable=self._fluid,
                        width=220, font=F_BODY).pack(side="left", padx=6)
        ctk.CTkButton(row, text="Show", height=36, font=F_BODY,
                      width=80, command=self._calc).pack(side="left", padx=6)

        ctk.CTkLabel(self, text="Critical & Reference Points",
                     font=F_SECTION).pack(anchor="w", pady=(0, 4))
        tf, self._tv_ref = make_tree(self, ["Property", "Value"],
                                     [250, 380], height=7)
        tf.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(self, text="Saturation Table", font=F_SECTION).pack(
            anchor="w", pady=(0, 4))
        tf2, self._tv_sat = make_tree(
            self,
            SAT_TABLE_COLUMNS,
            [70, 110, 120, 120, 120, 120, 120], height=22)
        tf2.pack(fill="both", expand=True)

        plot_ctl = ctk.CTkFrame(self, corner_radius=10)
        plot_ctl.pack(fill="x", pady=(12, 14))
        ctk.CTkLabel(plot_ctl, text="Graph Saturation Table", font=F_SECTION).grid(
            row=0, column=0, columnspan=7, sticky="w", padx=14, pady=(12, 4))
        ctk.CTkLabel(
            plot_ctl,
            text="Choose any X and Y columns from the table above, then plot the sampled saturation data.",
            font=F_SMALL, text_color="#7a8a9a").grid(
            row=1, column=0, columnspan=7, sticky="w", padx=14, pady=(0, 10))

        ctk.CTkLabel(plot_ctl, text="X axis:", font=F_BODY).grid(
            row=2, column=0, padx=(14, 4), pady=(0, 12), sticky="w")
        self._sat_x = tk.StringVar(value=SAT_TABLE_COLUMNS[0])
        ctk.CTkComboBox(
            plot_ctl, values=SAT_TABLE_COLUMNS, variable=self._sat_x,
            width=170, font=F_BODY, state="readonly").grid(
            row=2, column=1, padx=(0, 12), pady=(0, 12), sticky="w")

        ctk.CTkLabel(plot_ctl, text="Y axis:", font=F_BODY).grid(
            row=2, column=2, padx=(0, 4), pady=(0, 12), sticky="w")
        self._sat_y = tk.StringVar(value=SAT_TABLE_COLUMNS[1])
        ctk.CTkComboBox(
            plot_ctl, values=SAT_TABLE_COLUMNS, variable=self._sat_y,
            width=170, font=F_BODY, state="readonly").grid(
            row=2, column=3, padx=(0, 12), pady=(0, 12), sticky="w")

        ctk.CTkButton(
            plot_ctl, text="Plot Table", height=34, font=F_BODY,
            fg_color="#1e5a8a", hover_color="#174d79",
            command=self._plot_sat_table).grid(
            row=2, column=4, padx=(0, 8), pady=(0, 12), sticky="w")
        ctk.CTkButton(
            plot_ctl, text="Reset Charts", height=34, font=F_BODY,
            fg_color="gray25", hover_color="gray20",
            command=self._plot_reference_charts).grid(
            row=2, column=5, padx=(0, 14), pady=(0, 12), sticky="w")

        # ── Property Charts ──
        ctk.CTkLabel(self, text="Property Charts", font=F_SECTION).pack(
            anchor="w", pady=(14, 4))
        self._chart = EmbeddedChart(self, figsize=(11, 6.5))
        self._chart.pack(fill="x", pady=(0, 12))

    def _calc(self):
        fluid = self._fluid.get()
        try:
            Tc    = PropsSI("Tcrit",   fluid)
            Pc    = PropsSI("Pcrit",   fluid)
            Tt    = PropsSI("Ttriple", fluid)
            Pt    = PropsSI("ptriple", fluid)
            M     = PropsSI("M",       fluid) * 1000
            T_nbp = PropsSI("T", "P", 101325, "Q", 0, fluid)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        refs = [
            ("Molar mass",           f"{M:.4f} g/mol"),
            ("Critical temperature", f"{Tc:.4f} K   ({Tc - 273.15:.4f} °C)"),
            ("Critical pressure",    f"{Pc/1000:.3f} kPa   ({Pc/1e5:.5f} bar)"),
            ("Triple point  T",      f"{Tt:.4f} K   ({Tt - 273.15:.4f} °C)"),
            ("Triple point  P",      f"{Pt:.4f} Pa"),
            ("Normal boiling point", f"{T_nbp:.4f} K   ({T_nbp - 273.15:.4f} °C)"),
        ]
        fill_tree(self._tv_ref, refs)

        T_min = max(Tt + 1.0, 180.0)
        T_max = Tc - 0.5
        sat_rows = []
        sat_data = {col: [] for col in SAT_TABLE_COLUMNS}
        for T in np.linspace(T_min, T_max, 30):
            try:
                P   = PropsSI("P", "T", T, "Q", 0, fluid)
                rl  = PropsSI("D", "T", T, "Q", 0, fluid)
                rv  = PropsSI("D", "T", T, "Q", 1, fluid)
                hl  = PropsSI("H", "T", T, "Q", 0, fluid)
                hv  = PropsSI("H", "T", T, "Q", 1, fluid)
                row_vals = (
                    T - 273.15,
                    P / 1000,
                    rl,
                    rv,
                    hl / 1000,
                    hv / 1000,
                    (hv - hl) / 1000,
                )
                sat_rows.append((
                    f"{row_vals[0]:.2f}",
                    f"{row_vals[1]:.3f}",
                    f"{row_vals[2]:.3f}",
                    f"{row_vals[3]:.5f}",
                    f"{row_vals[4]:.3f}",
                    f"{row_vals[5]:.3f}",
                    f"{row_vals[6]:.3f}",
                ))
                for col, value in zip(SAT_TABLE_COLUMNS, row_vals):
                    sat_data[col].append(value)
            except Exception:
                pass
        self._sat_table_data = sat_data
        self._last_fluid = fluid
        fill_tree(self._tv_sat, sat_rows)
        self._plot_reference_charts()

    def _plot_sat_table(self):
        if not MPLOK:
            return
        if not any(self._sat_table_data.values()):
            messagebox.showinfo("Info", "Press Show to build the saturation table first")
            return

        x_key = self._sat_x.get()
        y_key = self._sat_y.get()
        x_vals = self._sat_table_data.get(x_key, [])
        y_vals = self._sat_table_data.get(y_key, [])
        if not x_vals or not y_vals:
            messagebox.showinfo("Info", "No saturation data available for the selected plot")
            return

        self._chart.clear()
        fig = self._chart.figure()
        ax = fig.add_subplot(111)
        _style_ax(ax)
        ax.plot(x_vals, y_vals, color=_C["cycle"], lw=2.2, marker="o", ms=4)
        ax.scatter([x_vals[0], x_vals[-1]], [y_vals[0], y_vals[-1]],
                   color=_C["pt"], s=42, zorder=5)
        ax.set_xlabel(x_key)
        ax.set_ylabel(y_key)
        fluid = self._last_fluid or self._fluid.get()
        ax.set_title(f"{fluid}  —  Saturation Table Plot")
        fig.tight_layout()
        self._chart.redraw()

    def _plot_reference_charts(self):
        fluid = self._last_fluid or self._fluid.get()
        self._plot(fluid)

    def _plot(self, fluid):
        if not MPLOK:
            return
        self._chart.clear()
        fig = self._chart.figure()
        try:
            Tc  = PropsSI("Tcrit", fluid)
            Tt  = max(PropsSI("Ttriple", fluid) + 1.0, 160.0)
            Ts  = np.linspace(Tt, Tc - 0.2, 80)
            T_C = Ts - 273.15
            Ps  = [PropsSI("P","T",T,"Q",0,fluid)/1e3  for T in Ts]
            rl  = [PropsSI("D","T",T,"Q",0,fluid)      for T in Ts]
            rv  = [PropsSI("D","T",T,"Q",1,fluid)      for T in Ts]
            hl  = [PropsSI("H","T",T,"Q",0,fluid)/1e3  for T in Ts]
            hv  = [PropsSI("H","T",T,"Q",1,fluid)/1e3  for T in Ts]
            kl  = [PropsSI("L","T",T,"Q",0,fluid)*1e3  for T in Ts]
            kv  = [PropsSI("L","T",T,"Q",1,fluid)*1e3  for T in Ts]
        except Exception:
            self._chart.redraw(); return
        axes = [fig.add_subplot(2, 2, i+1) for i in range(4)]
        for ax in axes:
            _style_ax(ax)
        axes[0].plot(T_C, Ps, color=_C["liq"], lw=2)
        axes[0].set_xlabel("T [°C]"); axes[0].set_ylabel("P_sat [kPa]")
        axes[0].set_title("Vapour Pressure")
        axes[1].plot(T_C, rl, color=_C["liq"], lw=2, label="Liquid")
        axes[1].plot(T_C, rv, color=_C["vap"], lw=2, label="Vapour")
        axes[1].set_xlabel("T [°C]"); axes[1].set_ylabel("ρ  [kg/m³]")
        axes[1].set_title("Density")
        axes[1].legend(fontsize=7, facecolor=_C["axes"],
                       edgecolor=_C["spine"], labelcolor=_C["fg"])
        axes[2].plot(T_C, hl, color=_C["liq"], lw=2, label="Liquid")
        axes[2].plot(T_C, hv, color=_C["vap"], lw=2, label="Vapour")
        axes[2].set_xlabel("T [°C]"); axes[2].set_ylabel("h  [kJ/kg]")
        axes[2].set_title("Specific Enthalpy")
        axes[2].legend(fontsize=7, facecolor=_C["axes"],
                       edgecolor=_C["spine"], labelcolor=_C["fg"])
        axes[3].plot(T_C, kl, color=_C["liq"], lw=2, label="Liquid")
        axes[3].plot(T_C, kv, color=_C["vap"], lw=2, label="Vapour")
        axes[3].set_xlabel("T [°C]"); axes[3].set_ylabel("k  [mW/m·K]")
        axes[3].set_title("Thermal Conductivity")
        axes[3].legend(fontsize=7, facecolor=_C["axes"],
                       edgecolor=_C["spine"], labelcolor=_C["fg"])
        fig.suptitle(f"{fluid}  —  Saturation Properties",
                     color=_C["fg"], fontsize=11)
        fig.tight_layout()
        self._chart.redraw()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 7: Custom Property Chart
# ─────────────────────────────────────────────────────────────────────────────
class ChartPage(AppScrollablePage):
    """Interactive chart: sweep any CoolProp property over T or P."""

    _Y_CHOICES = [
        ("P",  "Pressure [kPa]",           lambda v: v / 1e3),
        ("D",  "Density [kg/m³]",          lambda v: v),
        ("H",  "Enthalpy [kJ/kg]",         lambda v: v / 1e3),
        ("S",  "Entropy [kJ/kg·K]",        lambda v: v / 1e3),
        ("C",  "Cp [J/kg·K]",              lambda v: v),
        ("O",  "Cv [J/kg·K]",              lambda v: v),
        ("A",  "Speed of Sound [m/s]",     lambda v: v),
        ("L",  "Therm. Cond. [mW/m·K]",   lambda v: v * 1e3),
        ("V",  "Dyn. Viscosity [µPa·s]",   lambda v: v * 1e6),
    ]

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Custom Property Chart",
                     font=F_TITLE).pack(anchor="w", pady=(0, 6))
        _page_hint(self,
            "Plot any combination of thermodynamic properties against temperature or pressure. "
            "Choose a fluid, set X axis (T in °C or P in kPa) and its range, "
            "pick the phase (sat-liq = Q 0 curve, sat-vap = Q 1 curve, "
            "superheated/subcooled = 10 K / 10% offset from saturation), "
            "tick the Y properties you want (each gets its own sub-plot), then press Plot.")

        # ── Controls row ──────────────────────────────────────────────────────
        ctrl = ctk.CTkFrame(self, fg_color="transparent")
        ctrl.pack(fill="x", pady=(0, 8))

        # Fluid
        ctk.CTkLabel(ctrl, text="Fluid:", font=F_BODY).grid(
            row=0, column=0, sticky="w", padx=(0, 4))
        self._fluid_var = ctk.StringVar(value="R134a")
        ctk.CTkComboBox(ctrl, values=ALL_FLUIDS, variable=self._fluid_var,
                        width=160, font=F_BODY).grid(row=0, column=1, padx=(0, 16))

        # X axis
        ctk.CTkLabel(ctrl, text="X axis:", font=F_BODY).grid(
            row=0, column=2, sticky="w", padx=(0, 4))
        self._xvar = ctk.StringVar(value="T")
        ctk.CTkSegmentedButton(ctrl, values=["T", "P"],
                               variable=self._xvar,
                               font=F_BODY).grid(row=0, column=3, padx=(0, 16))

        # X range
        ctk.CTkLabel(ctrl, text="X min:", font=F_BODY).grid(
            row=0, column=4, sticky="w", padx=(0, 4))
        self._xmin = ctk.CTkEntry(ctrl, width=80, font=F_BODY,
                                  placeholder_text="-40")
        self._xmin.grid(row=0, column=5, padx=(0, 8))
        ctk.CTkLabel(ctrl, text="max:", font=F_BODY).grid(
            row=0, column=6, sticky="w", padx=(0, 4))
        self._xmax = ctk.CTkEntry(ctrl, width=80, font=F_BODY,
                                  placeholder_text="60")
        self._xmax.grid(row=0, column=7, padx=(0, 16))

        # Phase
        ctk.CTkLabel(ctrl, text="Phase:", font=F_BODY).grid(
            row=0, column=8, sticky="w", padx=(0, 4))
        self._phase = ctk.StringVar(value="sat-liq")
        ctk.CTkComboBox(ctrl, values=["sat-liq", "sat-vap", "superheated", "subcooled"],
                        variable=self._phase,
                        width=140, font=F_BODY).grid(row=0, column=9, padx=(0, 16))

        ctk.CTkButton(ctrl, text="Plot", width=80, font=F_SECTION,
                      command=self._plot).grid(row=0, column=10)

        # ── Y-axis property checkboxes ────────────────────────────────────────
        yrow = ctk.CTkFrame(self, fg_color="transparent")
        yrow.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(yrow, text="Y properties:", font=F_BODY).pack(
            side="left", padx=(0, 8))
        self._y_vars = {}
        defaults = {"D", "H", "L"}
        for cp_key, label, _ in self._Y_CHOICES:
            var = ctk.BooleanVar(value=(cp_key in defaults))
            self._y_vars[cp_key] = var
            ctk.CTkCheckBox(yrow, text=label, variable=var,
                            font=F_SMALL).pack(side="left", padx=6)

        # ── Chart ─────────────────────────────────────────────────────────────
        ctk.CTkLabel(self, text="Property Chart",
                     font=F_SECTION).pack(anchor="w", pady=(4, 2))
        self._chart = EmbeddedChart(self, figsize=(12, 5))
        self._chart.pack(fill="both", expand=True, pady=(0, 10))

    def _plot(self):
        if not MPLOK:
            return
        fluid  = self._fluid_var.get()
        xkey   = self._xvar.get()            # "T" or "P"
        phase  = self._phase.get()
        chosen = [(k, lbl, fn) for k, lbl, fn in self._Y_CHOICES
                  if self._y_vars[k].get()]
        if not chosen:
            return

        # Parse X range
        try:
            Tc   = PropsSI("Tcrit", fluid)
            Pc   = PropsSI("Pcrit", fluid)
            Tt   = max(PropsSI("Ttriple", fluid) + 1.0, 160.0)
            if xkey == "T":
                x_lo = float(self._xmin.get() or -40) + 273.15
                x_hi = float(self._xmax.get() or 60)  + 273.15
                x_lo = max(x_lo, Tt); x_hi = min(x_hi, Tc - 0.5)
            else:
                x_lo = float(self._xmin.get() or 100)  * 1e3
                x_hi = float(self._xmax.get() or 3000) * 1e3
                x_lo = max(x_lo, 1e3); x_hi = min(x_hi, Pc * 0.99)
        except Exception:
            return

        X = np.linspace(x_lo, x_hi, 120)

        # Build Q or fixed-P/T query inputs depending on phase
        def get_q(ph):
            return {"sat-liq": 0.0, "sat-vap": 1.0}.get(ph, None)

        def get_props(xi):
            q = get_q(phase)
            k1, v1 = xkey, xi
            if q is not None:
                k2, v2 = "Q", q
            elif phase == "superheated":
                # slightly above sat vapour enthalpy
                try:
                    Psat = PropsSI("P", xkey, xi, "Q", 1, fluid) if xkey == "T" \
                           else xi
                    Tsat = PropsSI("T", "P", Psat, "Q", 1, fluid)
                    k2, v2 = ("T", Tsat + 10) if xkey == "P" else ("P", Psat * 0.9)
                except Exception:
                    return None
            else:  # subcooled
                try:
                    Psat = PropsSI("P", xkey, xi, "Q", 0, fluid) if xkey == "T" \
                           else xi
                    Tsat = PropsSI("T", "P", Psat, "Q", 0, fluid)
                    k2, v2 = ("T", Tsat - 10) if xkey == "P" else ("P", Psat * 1.1)
                except Exception:
                    return None
            return k1, v1, k2, v2

        # Compute curves
        curves = {k: [] for k, _, _ in chosen}
        x_plot = []
        for xi in X:
            args = get_props(xi)
            if args is None:
                continue
            k1, v1, k2, v2 = args
            row_ok = True
            vals = {}
            for cp_key, _, fn in chosen:
                try:
                    raw = PropsSI(cp_key, k1, v1, k2, v2, fluid)
                    vals[cp_key] = fn(raw)
                except Exception:
                    row_ok = False
                    break
            if row_ok:
                x_plot.append(xi)
                for cp_key in vals:
                    curves[cp_key].append(vals[cp_key])

        if not x_plot:
            return

        x_axis = [xi - 273.15 if xkey == "T" else xi / 1e3 for xi in x_plot]
        x_label = "Temperature [°C]" if xkey == "T" else "Pressure [kPa]"

        self._chart.clear()
        fig = self._chart.figure()
        n = len(chosen)
        cols_wrap = min(n, 3)
        rows_wrap = (n + cols_wrap - 1) // cols_wrap
        palette = [_C["liq"], _C["vap"], _C["cycle"], _C["cop"],
                   _C["pt"],  _C["hi"],  _C["pwr"],   _C["spine"], _C["fg"]]
        for idx, (cp_key, lbl, _) in enumerate(chosen):
            ax = fig.add_subplot(rows_wrap, cols_wrap, idx + 1)
            _style_ax(ax)
            ax.plot(x_axis, curves[cp_key],
                    color=palette[idx % len(palette)], lw=2)
            ax.set_xlabel(x_label)
            ax.set_ylabel(lbl)
            ax.set_title(lbl.split(" [")[0])
        fig.suptitle(f"{fluid}  —  {phase}", color=_C["fg"], fontsize=10)
        fig.tight_layout()
        self._chart.redraw()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 8: Quick Tools
# ─────────────────────────────────────────────────────────────────────────────
class QuickToolsPage(AppScrollablePage):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Engineering Quick Tools", font=F_TITLE).pack(
            anchor="w", pady=(0, 6))
        _page_hint(self,
            "Adds fast utilities around the main thermodynamic pages. "
            "Use Unit Converter to translate between engineering units, "
            "Carnot Benchmark to compare a cycle against the reversible limit, "
            "and State Classifier to identify the phase region from T + P.")

        self._build_converter()
        self._build_carnot()
        self._build_classifier()

    def _build_converter(self):
        card = ctk.CTkFrame(self, corner_radius=10)
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text="Unit Converter", font=F_SECTION).grid(
            row=0, column=0, columnspan=6, sticky="w", padx=14, pady=(12, 6))

        self._conv_key = tk.StringVar(value="P")
        self._conv_unit = tk.StringVar(value="kPa")

        ctk.CTkLabel(card, text="Variable:", font=F_BODY).grid(
            row=1, column=0, padx=(14, 4), pady=6, sticky="w")
        ctk.CTkComboBox(
            card,
            values=["T", "P", "H", "S", "D", "U"],
            variable=self._conv_key,
            width=110,
            font=F_BODY,
            command=self._refresh_converter_units,
        ).grid(row=1, column=1, padx=(0, 10), pady=6, sticky="w")

        ctk.CTkLabel(card, text="Value:", font=F_BODY).grid(
            row=1, column=2, padx=(0, 4), pady=6, sticky="w")
        self._conv_value = ctk.CTkEntry(card, width=120, font=F_BODY)
        self._conv_value.insert(0, "101.325")
        self._conv_value.grid(row=1, column=3, padx=(0, 10), pady=6, sticky="w")

        ctk.CTkLabel(card, text="Input unit:", font=F_BODY).grid(
            row=1, column=4, padx=(0, 4), pady=6, sticky="w")
        self._conv_unit_cb = ctk.CTkComboBox(
            card,
            variable=self._conv_unit,
            width=100,
            font=F_BODY,
            state="readonly",
        )
        self._conv_unit_cb.grid(row=1, column=5, padx=(0, 14), pady=6, sticky="w")

        ctk.CTkButton(
            card,
            text="Convert",
            height=34,
            font=F_BODY,
            command=self._convert_units,
        ).grid(row=2, column=0, padx=14, pady=(0, 10), sticky="w")

        ctk.CTkButton(
            card,
            text="Copy Table",
            height=34,
            font=F_BODY,
            fg_color="gray25",
            hover_color="gray20",
            command=lambda: _copy_tree_to_clipboard(self, self._tv_conv),
        ).grid(row=2, column=1, padx=(0, 14), pady=(0, 10), sticky="w")

        tf, self._tv_conv = make_tree(card, ["Unit", "Value"], [150, 260], height=6)
        tf.grid(row=3, column=0, columnspan=6, padx=14, pady=(0, 14), sticky="nsew")
        self._refresh_converter_units(self._conv_key.get())
        self._convert_units()

    def _build_carnot(self):
        card = ctk.CTkFrame(self, corner_radius=10)
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text="Carnot Benchmark", font=F_SECTION).grid(
            row=0, column=0, columnspan=7, sticky="w", padx=14, pady=(12, 6))
        ctk.CTkLabel(
            card,
            text="Use evaporator and condenser temperatures to estimate the reversible COP limit.",
            font=F_SMALL,
            text_color="#7a8a9a",
        ).grid(row=1, column=0, columnspan=7, sticky="w", padx=14, pady=(0, 10))

        fields = [
            ("Cold side [°C]", "-10"),
            ("Hot side [°C]", "40"),
            ("Actual COP (optional)", "2.8"),
        ]
        self._carnot_entries = []
        for idx, (label, default) in enumerate(fields):
            ctk.CTkLabel(card, text=label, font=F_BODY).grid(
                row=2, column=idx * 2, padx=(14, 4), pady=6, sticky="w")
            ent = ctk.CTkEntry(card, width=110, font=F_BODY)
            ent.insert(0, default)
            ent.grid(row=2, column=idx * 2 + 1, padx=(0, 14), pady=6, sticky="w")
            self._carnot_entries.append(ent)

        ctk.CTkButton(
            card,
            text="Calculate Benchmark",
            height=34,
            font=F_BODY,
            command=self._calc_carnot,
        ).grid(row=3, column=0, padx=14, pady=(0, 10), sticky="w")

        tf, self._tv_carnot = make_tree(card, ["Metric", "Value"], [210, 240], height=6)
        tf.grid(row=4, column=0, columnspan=7, padx=14, pady=(0, 14), sticky="nsew")
        self._calc_carnot()

    def _build_classifier(self):
        card = ctk.CTkFrame(self, corner_radius=10)
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text="State Classifier", font=F_SECTION).grid(
            row=0, column=0, columnspan=8, sticky="w", padx=14, pady=(12, 6))

        ctk.CTkLabel(card, text="Fluid:", font=F_BODY).grid(
            row=1, column=0, padx=(14, 4), pady=6, sticky="w")
        self._phase_fluid = tk.StringVar(value="R134a")
        ctk.CTkComboBox(
            card,
            values=ALL_FLUIDS,
            variable=self._phase_fluid,
            width=180,
            font=F_BODY,
        ).grid(row=1, column=1, padx=(0, 10), pady=6, sticky="w")

        ctk.CTkLabel(card, text="T [°C]:", font=F_BODY).grid(
            row=1, column=2, padx=(0, 4), pady=6, sticky="w")
        self._phase_T = ctk.CTkEntry(card, width=110, font=F_BODY)
        self._phase_T.insert(0, "25")
        self._phase_T.grid(row=1, column=3, padx=(0, 10), pady=6, sticky="w")

        ctk.CTkLabel(card, text="P [kPa]:", font=F_BODY).grid(
            row=1, column=4, padx=(0, 4), pady=6, sticky="w")
        self._phase_P = ctk.CTkEntry(card, width=110, font=F_BODY)
        self._phase_P.insert(0, "770")
        self._phase_P.grid(row=1, column=5, padx=(0, 10), pady=6, sticky="w")

        ctk.CTkButton(
            card,
            text="Classify State",
            height=34,
            font=F_BODY,
            command=self._classify_state,
        ).grid(row=1, column=6, padx=(0, 14), pady=6, sticky="w")

        ctk.CTkButton(
            card,
            text="Copy Table",
            height=34,
            font=F_BODY,
            fg_color="gray25",
            hover_color="gray20",
            command=lambda: _copy_tree_to_clipboard(self, self._tv_phase),
        ).grid(row=1, column=7, padx=(0, 14), pady=6, sticky="w")

        tf, self._tv_phase = make_tree(card, ["Property", "Value"], [220, 320], height=8)
        tf.grid(row=2, column=0, columnspan=8, padx=14, pady=(0, 14), sticky="nsew")
        self._classify_state()

    def _refresh_converter_units(self, key):
        units = [unit for unit, _ in IVARS[key][2]]
        self._conv_unit_cb.configure(values=units)
        self._conv_unit.set(units[1] if len(units) > 1 else units[0])
        defaults = {
            "T": "25",
            "P": "101.325",
            "H": "250",
            "S": "1.2",
            "D": "1.2",
            "U": "220",
        }
        self._conv_value.delete(0, "end")
        self._conv_value.insert(0, defaults.get(key, "1"))

    def _convert_units(self):
        key = self._conv_key.get()
        try:
            raw = float(self._conv_value.get())
            to_si = {unit: fn for unit, fn in IVARS[key][2]}[self._conv_unit.get()]
        except (ValueError, KeyError):
            messagebox.showerror("Error", "Enter a valid value and unit")
            return

        si_value = to_si(raw)
        rows = []
        if key == "T":
            rows = [
                ("K", f"{si_value:.5f}"),
                ("°C", f"{si_value - 273.15:.5f}"),
                ("°F", f"{(si_value - 273.15) * 9 / 5 + 32:.5f}"),
            ]
        elif key == "P":
            rows = [
                ("Pa", f"{si_value:.3f}"),
                ("kPa", f"{si_value / 1e3:.6f}"),
                ("MPa", f"{si_value / 1e6:.6f}"),
                ("bar", f"{si_value / 1e5:.6f}"),
                ("psi", f"{si_value / 6894.76:.6f}"),
            ]
        elif key in {"H", "U"}:
            rows = [
                ("J/kg", f"{si_value:.5f}"),
                ("kJ/kg", f"{si_value / 1e3:.8f}"),
            ]
        elif key == "S":
            rows = [
                ("J/kg·K", f"{si_value:.6f}"),
                ("kJ/kg·K", f"{si_value / 1e3:.9f}"),
            ]
        elif key == "D":
            rows = [
                ("kg/m³", f"{si_value:.8f}"),
                ("g/L", f"{si_value:.8f}"),
            ]
        fill_tree(self._tv_conv, rows)

    def _calc_carnot(self):
        try:
            cold_c = float(self._carnot_entries[0].get())
            hot_c = float(self._carnot_entries[1].get())
        except ValueError:
            messagebox.showerror("Error", "Cold and hot temperatures must be numeric")
            return

        cold_k = cold_c + 273.15
        hot_k = hot_c + 273.15
        if cold_k <= 0 or hot_k <= cold_k:
            messagebox.showerror("Error", "Hot side must be above cold side and both must be above absolute zero")
            return

        cop_cooling = cold_k / (hot_k - cold_k)
        cop_heating = hot_k / (hot_k - cold_k)
        rows = [
            ("Temperature lift", f"{hot_c - cold_c:.3f} K"),
            ("Carnot COP (cooling)", f"{cop_cooling:.5f}"),
            ("Carnot COP (heating)", f"{cop_heating:.5f}"),
            ("Ideal work per unit cooling", f"{1 / cop_cooling:.5f} kW/kW"),
        ]

        actual_raw = self._carnot_entries[2].get().strip()
        if actual_raw:
            try:
                actual_cop = float(actual_raw)
                if actual_cop > 0:
                    rows.append(("Second-law efficiency", f"{actual_cop / cop_cooling:.5f}"))
                    rows.append(("Carnot gap", f"{(1 - actual_cop / cop_cooling) * 100:.2f} %"))
            except ValueError:
                pass
        fill_tree(self._tv_carnot, rows)

    def _classify_state(self):
        fluid = self._phase_fluid.get()
        try:
            T_si = float(self._phase_T.get()) + 273.15
            P_si = float(self._phase_P.get()) * 1e3
        except ValueError:
            messagebox.showerror("Error", "Temperature and pressure must be numeric")
            return

        try:
            phase_name = _phase_display_name(CP.PhaseSI("T", T_si, "P", P_si, fluid))
        except Exception:
            phase_name = "Unavailable"

        rows = [("Phase region", phase_name)]
        for key, label, fmt in [
            ("D", "Density", OVARS[2][2]),
            ("H", "Enthalpy", OVARS[3][2]),
            ("S", "Entropy", OVARS[4][2]),
            ("C", "Cp", OVARS[6][2]),
            ("A", "Speed of Sound", OVARS[9][2]),
            ("L", "Thermal Conductivity", OVARS[10][2]),
            ("V", "Dynamic Viscosity", OVARS[11][2]),
        ]:
            try:
                value = PropsSI(key, "T", T_si, "P", P_si, fluid)
                rows.append((label, fmt(value)))
            except Exception:
                rows.append((label, "—"))

        try:
            quality = PropsSI("Q", "T", T_si, "P", P_si, fluid)
            q_text = f"{quality:.6f}" if 0 <= quality <= 1 else "—"
        except Exception:
            q_text = "—"
        rows.append(("Vapor quality", q_text))

        try:
            Tc = PropsSI("Tcrit", fluid)
            Pc = PropsSI("Pcrit", fluid)
            rows.append(("Reduced temperature", f"{T_si / Tc:.6f}"))
            rows.append(("Reduced pressure", f"{P_si / Pc:.6f}"))
        except Exception:
            pass

        fill_tree(self._tv_phase, rows)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 9: How To
# ─────────────────────────────────────────────────────────────────────────────
class HowToPage(AppScrollablePage):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="How To Use This App", font=F_TITLE).pack(
            anchor="w", pady=(0, 6))
        _page_hint(self,
            "This page is the operator guide for the calculator. "
            "It explains which page to use, which inputs are physically valid, "
            "and a practical workflow for moving from a quick state lookup to cycle sizing.")

        self._add_section(
            "Recommended Workflow",
            "1. Start with State Point when you know any two independent properties.\n"
            "2. Use Saturation to inspect bubble-point and dew-point limits before building a cycle.\n"
            "3. Move to Refrig. Cycle to compute state points 1-4 and COP.\n"
            "4. Use System Sizing after the thermodynamic cycle is stable to size mass flow, compressor power, and pump load.\n"
            "5. Finish with Capillary Tube or Property Charts for component design and sensitivity checks."
        )

        self._add_section(
            "Choosing Inputs",
            "State Point requires two independent properties. Good pairs include T + P, T + Q, P + Q, P + H, and P + S.\n"
            "Do not enter the same variable twice. Quality Q is only valid inside the two-phase region and must remain between 0 and 1.\n"
            "When working near the critical point, saturation pages and quality-based calculations can fail because liquid and vapor merge into one phase."
        )

        self._add_section(
            "Cycle Modeling Tips",
            "Evaporator and condenser inputs are saturation temperatures, not line temperatures.\n"
            "Superheat is added at the compressor inlet to protect the compressor from liquid carryover.\n"
            "Subcooling is removed from the condenser exit to reduce flash gas and increase refrigeration effect.\n"
            "If refrigeration effect becomes negative or COP looks unreasonable, the first checks should be temperature lift, isentropic efficiency, and whether subcooling exceeds the available condensing margin."
        )

        self._add_section(
            "Quick Tools",
            "Unit Converter translates engineering units without leaving the app.\n"
            "Carnot Benchmark estimates the reversible COP limit for a given hot and cold side temperature pair, which is useful for checking whether an actual COP is plausible.\n"
            "State Classifier uses T + P to report the phase region and key transport properties for a quick sanity check before detailed calculations."
        )

        self._add_section(
            "Charts And Reference Data",
            "Fluid Reference shows critical properties, triple-point data, and a sampled saturation table.\n"
            "Property Charts sweep a selected property over temperature or pressure to reveal trends.\n"
            "Use the P-H diagrams on State Point and Refrig. Cycle pages to confirm whether a point lies inside the dome, in the superheated region, or in the subcooled-liquid region."
        )

        self._add_section(
            "Troubleshooting",
            "If a table row shows an error, the property pair may be outside the valid range for that fluid.\n"
            "If a saturation query fails, check that temperature is below the critical temperature and pressure is below the critical pressure.\n"
            "If capillary flow is marked choked, reduce mass flow, increase diameter, or relax the pressure drop target.\n"
            "If charts are blank, install matplotlib because plotting is optional in this app."
        )

    def _add_section(self, title, body):
        card = ctk.CTkFrame(self, corner_radius=10)
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text=title, font=F_SECTION).pack(
            anchor="w", padx=14, pady=(12, 6))
        ctk.CTkLabel(
            card,
            text=body,
            font=F_BODY,
            wraplength=940,
            justify="left",
            anchor="w",
        ).pack(anchor="w", fill="x", padx=14, pady=(0, 12))


# ═════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═════════════════════════════════════════════════════════════════════════════

NAV_ITEMS = [
    ("howto",     "How To"),
    ("state",     "State Point"),
    ("sat",       "Saturation"),
    ("cycle",     "Refrig. Cycle"),
    ("sizing",    "System Sizing"),
    ("captube",   "Capillary Tube"),
    ("fluidinfo", "Fluid Reference"),
    ("charts",    "Property Charts"),
    ("tools",     "Quick Tools"),
]

PAGE_MAP = {
    "howto":     HowToPage,
    "state":     StatePointPage,
    "sat":       SaturationPage,
    "cycle":     CyclePage,
    "sizing":    SizingPage,
    "captube":   CapTubePage,
    "fluidinfo": FluidInfoPage,
    "charts":    ChartPage,
    "tools":     QuickToolsPage,
}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        _init_fonts()   # must come after CTk.__init__ creates the root window
        self.title("CoolProp Thermodynamic Calculator")
        self.geometry("1360x900")
        self.minsize(1060, 720)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_main()
        self._show("state")

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=215, corner_radius=0,
                          fg_color=("#1c1c1c", "#1c1c1c"))
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_rowconfigure(len(NAV_ITEMS) + 3, weight=1)

        ctk.CTkLabel(
            sb, text="CoolProp",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#a0a8b0", "#a0a8b0")).grid(
            row=0, column=0, padx=20, pady=(24, 2))
        ctk.CTkLabel(
            sb, text="Thermodynamic Calculator",
            font=ctk.CTkFont(size=10),
            text_color="gray40").grid(
            row=1, column=0, padx=20, pady=(0, 22))

        self._nav = {}
        for i, (key, label) in enumerate(NAV_ITEMS, start=2):
            btn = ctk.CTkButton(
                sb, text=label, anchor="w", width=195, height=38,
                corner_radius=4, font=ctk.CTkFont(size=12),
                fg_color="transparent",
                hover_color=("#2d2d2d", "#2d2d2d"),
                text_color=("#c0c8d0", "#c0c8d0"),
                command=lambda k=key: self._show(k))
            btn.grid(row=i, column=0, padx=10, pady=3)
            self._nav[key] = btn

        # Divider
        ctk.CTkFrame(sb, height=1, fg_color="gray30").grid(
            row=len(NAV_ITEMS) + 2, column=0, sticky="ew",
            padx=14, pady=10)

        ver = (CP.__version__ if hasattr(CP, "__version__") else "")
        ctk.CTkLabel(sb, text=f"CoolProp  {ver}",
                     font=ctk.CTkFont(size=10),
                     text_color="gray45").grid(
            row=len(NAV_ITEMS) + 4, column=0, padx=10, pady=(0, 12))

    # ── Main area ─────────────────────────────────────────────────────────────
    def _build_main(self):
        self._main = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self._main.grid(row=0, column=1, sticky="nsew", padx=14, pady=14)
        self._main.grid_columnconfigure(0, weight=1)
        self._main.grid_rowconfigure(0, weight=1)
        # Pages are built lazily on first visit to keep startup fast.
        self._pages = {k: None for k in PAGE_MAP}

    def _show(self, key: str):
        for k, btn in self._nav.items():
            btn.configure(fg_color="transparent")
        self._nav[key].configure(fg_color=("#1a4060", "#1a4060"))
        for pg in self._pages.values():
            if pg is not None:
                pg.grid_remove()
        pg = self._pages[key]
        if pg is None:
            pg = PAGE_MAP[key](self._main)
            pg.grid(row=0, column=0, sticky="nsew")
            self._pages[key] = pg
        else:
            pg.grid()


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
