with open('coolprop_gui.py', encoding='utf-8') as f:
    lines = f.readlines()

def ins(n, block):
    lines.insert(n - 1, block)

# ── Insert in REVERSE order (bottom first) so earlier line numbers stay valid ──

# 6) FluidInfoPage._plot()  before line 1368
ins(1368, """
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
        axes[0].set_xlabel("T [\u00b0C]"); axes[0].set_ylabel("P_sat [kPa]")
        axes[0].set_title("Vapour Pressure")
        axes[1].plot(T_C, rl, color=_C["liq"], lw=2, label="Liquid")
        axes[1].plot(T_C, rv, color=_C["vap"], lw=2, label="Vapour")
        axes[1].set_xlabel("T [\u00b0C]"); axes[1].set_ylabel("\u03c1  [kg/m\u00b3]")
        axes[1].set_title("Density")
        axes[1].legend(fontsize=7, facecolor=_C["axes"],
                       edgecolor=_C["spine"], labelcolor=_C["fg"])
        axes[2].plot(T_C, hl, color=_C["liq"], lw=2, label="Liquid")
        axes[2].plot(T_C, hv, color=_C["vap"], lw=2, label="Vapour")
        axes[2].set_xlabel("T [\u00b0C]"); axes[2].set_ylabel("h  [kJ/kg]")
        axes[2].set_title("Specific Enthalpy")
        axes[2].legend(fontsize=7, facecolor=_C["axes"],
                       edgecolor=_C["spine"], labelcolor=_C["fg"])
        axes[3].plot(T_C, kl, color=_C["liq"], lw=2, label="Liquid")
        axes[3].plot(T_C, kv, color=_C["vap"], lw=2, label="Vapour")
        axes[3].set_xlabel("T [\u00b0C]"); axes[3].set_ylabel("k  [mW/m\u00b7K]")
        axes[3].set_title("Thermal Conductivity")
        axes[3].legend(fontsize=7, facecolor=_C["axes"],
                       edgecolor=_C["spine"], labelcolor=_C["fg"])
        fig.suptitle(f"{fluid}  \u2014  Saturation Properties",
                     color=_C["fg"], fontsize=11)
        fig.tight_layout()
        self._chart.redraw()
""")

# 5) CapTubePage._plot_L() + _plot_D()  before line 1277
ins(1277, """
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
""")

# 4) SizingPage._plot()  before line 1093
ins(1093, """
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
                        label=f"Current  ({T_evap:.1f} \u00b0C)")
            ax1.set_xlabel("Evap. Temperature [\u00b0C]")
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
""")

# 3) CyclePage._plot_ph()  before line 893
ins(893, """
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
                    alpha=0.65, label="Isentrope 1\u21922s")
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
        ax.set_title(f"P\u2013H Diagram  \u2014  {fluid}")
        ax.legend(fontsize=8, facecolor=_C["axes"],
                  edgecolor=_C["spine"], labelcolor=_C["fg"])
        fig.tight_layout()
        self._chart.redraw()
""")

# 2) SaturationPage._plot_sat()  before line 746
ins(746, """
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
        axes[0].set_xlabel("T [\u00b0C]"); axes[0].set_ylabel("P_sat [kPa]")
        axes[0].set_title("Vapour Pressure")
        axes[1].plot(T_C, rl,    color=_C["liq"], lw=2, label="Liquid")
        axes[1].plot(T_C, rv,    color=_C["vap"], lw=2, label="Vapour")
        axes[1].set_xlabel("T [\u00b0C]"); axes[1].set_ylabel("\u03c1 [kg/m\u00b3]")
        axes[1].set_title("Density")
        axes[1].legend(fontsize=7, facecolor=_C["axes"],
                       edgecolor=_C["spine"], labelcolor=_C["fg"])
        axes[2].plot(T_C, dhvap, color=_C["cycle"], lw=2)
        axes[2].set_xlabel("T [\u00b0C]"); axes[2].set_ylabel("\u0394H_vap [kJ/kg]")
        axes[2].set_title("Latent Heat")
        try:
            T_cur = (val_si - 273.15) if key == "T" else (
                PropsSI("T","P",val_si,"Q",0,fluid) - 273.15)
            for ax in axes:
                ax.axvline(T_cur, color=_C["pt"], lw=1.2, ls="--",
                           alpha=0.85, label="Current")
        except Exception:
            pass
        fig.suptitle(f"{fluid}  \u2014  Saturation Properties",
                     color=_C["fg"], fontsize=10)
        fig.tight_layout()
        self._chart.redraw()
""")

# 1) StatePointPage._plot_ph()  before line 643
ins(643, """
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
        ax.set_title(f"P\u2013H Diagram  \u2014  {fluid}")
        ax.legend(fontsize=8, facecolor=_C["axes"],
                  edgecolor=_C["spine"], labelcolor=_C["fg"])
        fig.tight_layout()
        self._chart.redraw()
""")

with open('coolprop_gui.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Done. Total lines: {len(lines)}")
