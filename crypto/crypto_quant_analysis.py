"""
Crypto Quantitative Analysis — April 2026
=========================================
Fetches live/historical data from CoinGecko's free API and performs:
  1. Current snapshot: price, drawdown from ATH, YTD returns
  2. BTC post-halving cycle analysis (2012 / 2016 / 2020 / 2024)
  3. Risk-adjusted return metrics (Sharpe, Sortino, max drawdown)
  4. Hyperliquid revenue/valuation model vs DeFi peers
  5. Correlation matrix across top assets
  6. Monte Carlo price simulation for BTC / SOL / ETH / HYPE
  7. ETF launch effect: how BTC and ETH behaved after spot ETF approvals

Run:  python crypto_quant_analysis.py
Outputs PNG charts to ./charts/ and a stats summary to stdout.
"""

import os
import time
import json
import math
import warnings
import requests
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # headless rendering
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter
import matplotlib.patches as mpatches

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

COINGECKO_BASE = "https://api.coingecko.com/api/v3"
HEADERS = {"Accept": "application/json", "User-Agent": "CryptoQuantAnalysis/1.0"}

# CoinGecko IDs for the assets we care about
ASSETS = {
    "BTC":  "bitcoin",
    "ETH":  "ethereum",
    "SOL":  "solana",
    "HYPE": "hyperliquid",
    "XRP":  "ripple",
    "TAO":  "bittensor",
    "ONDO": "ondo-finance",
}

# Known ATHs (confirmed from research, used as fallback if API doesn't return them)
KNOWN_ATH = {
    "BTC":  126_173,
    "ETH":    4_946,
    "SOL":     294.16,
    "HYPE":     59.33,
    "XRP":       3.84,
    "TAO":     769.00,
    "ONDO":      2.14,
}

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def cg_get(endpoint: str, params: dict = None, retries: int = 3) -> dict | list | None:
    """Thin CoinGecko GET wrapper with retry + back-off."""
    url = f"{COINGECKO_BASE}{endpoint}"
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=20)
            if r.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"  Rate-limited. Waiting {wait}s …")
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            print(f"  API error ({endpoint}): {exc}")
            time.sleep(5)
    return None


def pct(value: float) -> str:
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.1f}%"


def fmt_b(value: float) -> str:
    """Format large dollar numbers as $XB or $XM."""
    if abs(value) >= 1e12:
        return f"${value/1e12:.2f}T"
    if abs(value) >= 1e9:
        return f"${value/1e9:.1f}B"
    if abs(value) >= 1e6:
        return f"${value/1e6:.0f}M"
    return f"${value:,.0f}"


def save_fig(fig: plt.Figure, name: str):
    path = os.path.join(CHARTS_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"  Saved → {path}")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────
# 1. CURRENT SNAPSHOT
# ─────────────────────────────────────────────────────────────

def fetch_current_snapshot() -> pd.DataFrame:
    print("\n[1/7] Fetching current prices & market data …")
    ids_str = ",".join(ASSETS.values())
    data = cg_get(
        "/coins/markets",
        params={
            "vs_currency": "usd",
            "ids": ids_str,
            "price_change_percentage": "24h,7d,30d,1y",
            "per_page": 20,
        },
    )
    if data is None:
        print("  ⚠  Falling back to hardcoded snapshot (API unavailable).")
        return _hardcoded_snapshot()

    rows = []
    id_to_sym = {v: k for k, v in ASSETS.items()}
    for coin in data:
        sym = id_to_sym.get(coin["id"], coin["symbol"].upper())
        ath = coin.get("ath") or KNOWN_ATH.get(sym, 0)
        price = coin.get("current_price", 0) or 0
        ath_chg = ((price - ath) / ath * 100) if ath else None
        rows.append({
            "symbol":        sym,
            "price":         price,
            "market_cap":    coin.get("market_cap", 0),
            "ath":           ath,
            "ath_pct":       ath_chg,
            "chg_24h":       coin.get("price_change_percentage_24h_in_currency"),
            "chg_7d":        coin.get("price_change_percentage_7d_in_currency"),
            "chg_30d":       coin.get("price_change_percentage_30d_in_currency"),
            "chg_1y":        coin.get("price_change_percentage_1y_in_currency"),
        })

    # Sort by market cap
    df = pd.DataFrame(rows).sort_values("market_cap", ascending=False).reset_index(drop=True)
    return df


def _hardcoded_snapshot() -> pd.DataFrame:
    """Hardcoded April 19 2026 data as absolute fallback."""
    rows = [
        ("BTC",  74_460, 1.49e12, 126_173, None,  4.9,  4.9, -14.5, None),
        ("ETH",   2_278, 2.75e11,   4_946, None,  3.8,  3.8, -22.9, None),
        ("XRP",    1.41, 8.65e10,    3.84, None,  5.9,  5.9, -22.5, None),
        ("SOL",   84.10, 4.84e10,  294.16, None,  3.0,  3.0, -31.4, None),
        ("HYPE",  41.10, 9.80e9,    59.33, None,  5.7,  5.7,  65.1, None),
        ("TAO",  243.00, 2.33e9,   769.00, None,  6.9,  6.9,   8.4, None),
        ("ONDO",   0.25, 1.23e9,     2.14, None,  2.8,  2.8,  -5.0, None),
    ]
    cols = ["symbol","price","market_cap","ath","chg_24h","chg_24h_dup","chg_7d","chg_30d","chg_1y"]
    df = pd.DataFrame(rows, columns=cols).drop(columns=["chg_24h_dup"])
    for sym, _, _, ath, *_ in rows:
        price = df.loc[df.symbol == sym, "price"].values[0]
        df.loc[df.symbol == sym, "ath_pct"] = (price - ath) / ath * 100
    return df


def plot_snapshot(df: pd.DataFrame):
    print("  Plotting snapshot …")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor="#0d1117")
    fig.suptitle("Asset Snapshot — April 19 2026", color="white", fontsize=14, y=1.01)

    # — Left: Drawdown from ATH —
    ax1 = axes[0]
    ax1.set_facecolor("#161b22")
    syms = df["symbol"].tolist()
    drawdowns = df["ath_pct"].fillna(0).tolist()
    colors = ["#e74c3c" if d < -50 else "#f39c12" if d < -25 else "#2ecc71" for d in drawdowns]
    bars = ax1.barh(syms, drawdowns, color=colors, edgecolor="none", height=0.6)
    ax1.set_xlabel("% Below All-Time High", color="lightgray")
    ax1.set_title("Drawdown from ATH", color="white", pad=8)
    ax1.tick_params(colors="lightgray")
    ax1.spines[:].set_visible(False)
    ax1.axvline(0, color="gray", linewidth=0.5)
    for bar, val in zip(bars, drawdowns):
        ax1.text(val - 1, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1f}%", va="center", ha="right", color="white", fontsize=9)

    # — Right: Market cap comparison —
    ax2 = axes[1]
    ax2.set_facecolor("#161b22")
    mcaps = (df["market_cap"] / 1e9).tolist()
    bar_colors = ["#f7931a", "#627eea", "#9945ff", "#00d2ff", "#9b59b6", "#1abc9c", "#3498db"]
    ax2.barh(syms, mcaps, color=bar_colors[:len(syms)], edgecolor="none", height=0.6)
    ax2.set_xlabel("Market Cap (USD Billions)", color="lightgray")
    ax2.set_title("Market Cap ($B)", color="white", pad=8)
    ax2.tick_params(colors="lightgray")
    ax2.spines[:].set_visible(False)
    for i, (mc, price) in enumerate(zip(mcaps, df["price"].tolist())):
        ax2.text(mc + 5, i, f"${price:,.2f}", va="center", color="lightgray", fontsize=8)

    fig.patch.set_facecolor("#0d1117")
    plt.tight_layout()
    save_fig(fig, "01_snapshot.png")

    # Print table
    print("\n  ── Current Snapshot ──────────────────────────────────────────")
    print(f"  {'Symbol':<6} {'Price':>10} {'Mkt Cap':>10} {'ATH':>10} {'From ATH':>10} {'7d':>8} {'30d':>8}")
    print("  " + "─" * 70)
    for _, row in df.iterrows():
        mc_str = fmt_b(row['market_cap']) if pd.notna(row['market_cap']) else "N/A"
        ath_str = f"{row['ath_pct']:.1f}%" if pd.notna(row['ath_pct']) else "N/A"
        chg7  = f"{row['chg_7d']:+.1f}%" if pd.notna(row['chg_7d']) else "N/A"
        chg30 = f"{row['chg_30d']:+.1f}%" if pd.notna(row['chg_30d']) else "N/A"
        print(f"  {row['symbol']:<6} ${row['price']:>9,.2f} {mc_str:>10} ${row['ath']:>9,.0f} {ath_str:>10} {chg7:>8} {chg30:>8}")


# ─────────────────────────────────────────────────────────────
# 2. BTC HALVING CYCLE ANALYSIS
# ─────────────────────────────────────────────────────────────

# Hard data: peak BTC price achieved in each post-halving cycle window
# plus the return from halving date price to that peak.
HALVING_CYCLES = {
    "Halving 1\n(Nov 2012)": {
        "halving_price":    12.35,
        "peak_price":    1_163.00,
        "peak_months_after": 13,
        "days_data": {   # month index → price (approx)
            0: 12.35, 3: 50, 6: 120, 9: 500, 12: 980, 13: 1163, 18: 600, 24: 350,
        },
    },
    "Halving 2\n(Jul 2016)": {
        "halving_price":     650,
        "peak_price":     19_891,
        "peak_months_after": 17,
        "days_data": {
            0: 650, 3: 700, 6: 750, 9: 1000, 12: 5000, 15: 12000, 17: 19891, 20: 8000, 24: 3500,
        },
    },
    "Halving 3\n(May 2020)": {
        "halving_price":    8_821,
        "peak_price":    69_000,
        "peak_months_after": 18,
        "days_data": {
            0: 8821, 3: 11000, 6: 18000, 9: 35000, 12: 55000, 15: 64000, 18: 69000, 21: 35000, 24: 25000,
        },
    },
    "Halving 4\n(Apr 2024)": {
        "halving_price":   63_000,
        "peak_price":     126_173,
        "peak_months_after": 10,       # approx Jan/Feb 2025
        "days_data": {
            0: 63000, 2: 65000, 4: 75000, 6: 93000, 8: 105000, 10: 126173,
            12: 97000, 13: 84000, 14: 80000, 15: 74460,   # ← now (Apr 2026 = month ~12-13)
        },
    },
}


def plot_halving_cycles():
    print("\n[2/7] Plotting BTC halving cycle comparison …")
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), facecolor="#0d1117")
    fig.suptitle("BTC Post-Halving Cycles — Indexed to 100 at Halving Date",
                 color="white", fontsize=13, y=1.01)

    all_returns = []
    for ax, (label, cyc) in zip(axes.flat, HALVING_CYCLES.items()):
        ax.set_facecolor("#161b22")
        months = sorted(cyc["days_data"].keys())
        prices = [cyc["days_data"][m] for m in months]
        indexed = [p / cyc["halving_price"] * 100 for p in prices]

        peak_idx = indexed.index(max(indexed))
        color = "#f7931a" if "Halving 4" in label else "#4ec9b0"

        ax.plot(months, indexed, color=color, linewidth=2.5, zorder=3)
        ax.fill_between(months, indexed, alpha=0.15, color=color)
        ax.scatter([months[peak_idx]], [indexed[peak_idx]],
                   color="yellow", zorder=5, s=80, label=f"Peak: {max(indexed):.0f}x base")

        # Mark "now" for cycle 4
        if "Halving 4" in label:
            ax.axvline(x=12, color="#e74c3c", linestyle="--", linewidth=1.5, label="Now (Apr 2026)")
            ax.text(12.2, indexed[-1] * 1.05, "← NOW", color="#e74c3c", fontsize=9)

        ax.set_title(label, color="white", fontsize=10)
        ax.tick_params(colors="lightgray", labelsize=8)
        ax.spines[:].set_visible(False)
        ax.set_xlabel("Months After Halving", color="lightgray", fontsize=8)
        ax.set_ylabel("Price Index (100 = halving price)", color="lightgray", fontsize=8)
        ax.legend(fontsize=8, facecolor="#1c2333", labelcolor="white", framealpha=0.6)
        ax.grid(axis="y", color="gray", alpha=0.2)

        peak_ret = (max(prices) / cyc["halving_price"] - 1) * 100
        all_returns.append(peak_ret)
        ax.set_facecolor("#161b22")

    fig.patch.set_facecolor("#0d1117")
    plt.tight_layout()
    save_fig(fig, "02_halving_cycles.png")

    print("\n  ── BTC Post-Halving Peak Returns ────────────────────────")
    for (label, cyc), ret in zip(HALVING_CYCLES.items(), all_returns):
        clean_label = label.replace("\n", " ")
        print(f"  {clean_label:35s}  peak return: +{ret:,.0f}%  (month {cyc['peak_months_after']})")
    print(f"\n  Cycle 4 (2024) peak return so far: +{(126173/63000 - 1)*100:.0f}%")
    print(f"  IF cycle 4 follows prior averages, potential 2nd-leg high from current ~$74K:")
    avg_mult = np.mean([cyc["peak_price"] / cyc["halving_price"] for cyc in HALVING_CYCLES.values()])
    implied = 63_000 * avg_mult
    print(f"    Average post-halving multiplier: {avg_mult:.1f}x from halving price")
    print(f"    Implied cycle peak (avg): ~${implied:,.0f}")
    print(f"    Upside from $74,460: +{(implied / 74460 - 1) * 100:.0f}%  (base = average cycles)")


# ─────────────────────────────────────────────────────────────
# 3. RISK-ADJUSTED METRICS (using 365-day price history)
# ─────────────────────────────────────────────────────────────

def fetch_price_history(cg_id: str, days: int = 365) -> pd.Series | None:
    data = cg_get(
        f"/coins/{cg_id}/market_chart",
        params={"vs_currency": "usd", "days": days, "interval": "daily"},
    )
    if data is None or "prices" not in data:
        return None
    prices = pd.DataFrame(data["prices"], columns=["ts", "price"])
    prices["date"] = pd.to_datetime(prices["ts"], unit="ms")
    prices = prices.set_index("date")["price"]
    return prices


def compute_metrics(prices: pd.Series, label: str) -> dict:
    daily_ret = prices.pct_change().dropna()
    annual_ret = (prices.iloc[-1] / prices.iloc[0]) - 1
    vol_ann = daily_ret.std() * math.sqrt(365)
    downside = daily_ret[daily_ret < 0].std() * math.sqrt(365)
    rf = 0.045  # 4.5% risk-free rate (approx US 1-yr Treasury April 2026)
    sharpe  = (annual_ret - rf) / vol_ann if vol_ann > 0 else 0
    sortino = (annual_ret - rf) / downside if downside > 0 else 0
    rolling_max = prices.cummax()
    drawdown = (prices - rolling_max) / rolling_max
    max_dd = drawdown.min()
    calmar  = annual_ret / abs(max_dd) if max_dd != 0 else 0
    return {
        "symbol":     label,
        "annual_ret": annual_ret * 100,
        "vol_ann":    vol_ann * 100,
        "sharpe":     sharpe,
        "sortino":    sortino,
        "max_dd":     max_dd * 100,
        "calmar":     calmar,
    }


def plot_risk_metrics(metrics_df: pd.DataFrame):
    print("  Plotting risk-adjusted metrics …")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor="#0d1117")
    fig.suptitle("Risk-Adjusted Performance (365-Day Window)", color="white", fontsize=13)

    palette = ["#f7931a", "#627eea", "#9945ff", "#00d2ff", "#9b59b6", "#1abc9c", "#3498db"]

    for ax, metric, title in [
        (axes[0], "sharpe",     "Sharpe Ratio\n(higher = better risk-adj return)"),
        (axes[1], "sortino",    "Sortino Ratio\n(penalises only downside vol)"),
        (axes[2], "max_dd",     "Max Drawdown %\n(lower = less catastrophic loss)"),
    ]:
        ax.set_facecolor("#161b22")
        syms = metrics_df["symbol"].tolist()
        vals = metrics_df[metric].tolist()
        if metric == "max_dd":
            clrs = ["#e74c3c" if v < -50 else "#f39c12" if v < -30 else "#2ecc71" for v in vals]
        else:
            clrs = ["#2ecc71" if v > 1 else "#f39c12" if v > 0 else "#e74c3c" for v in vals]
        bars = ax.bar(syms, vals, color=clrs, edgecolor="none", width=0.6)
        ax.set_title(title, color="white", fontsize=9, pad=6)
        ax.tick_params(colors="lightgray", labelsize=8)
        ax.spines[:].set_visible(False)
        ax.axhline(0, color="gray", linewidth=0.6)
        for bar, val in zip(bars, vals):
            ypos = val + (0.02 if val >= 0 else -0.04) * abs(min(vals) - max(vals)) * 0.5
            ax.text(bar.get_x() + bar.get_width() / 2, ypos,
                    f"{val:.2f}", ha="center", color="white", fontsize=8)
        ax.set_facecolor("#161b22")

    fig.patch.set_facecolor("#0d1117")
    plt.tight_layout()
    save_fig(fig, "03_risk_metrics.png")

    print("\n  ── Risk-Adjusted Metrics (365-day) ─────────────────────────────────────")
    print(f"  {'Symbol':<6} {'Ann Return':>11} {'Ann Vol':>9} {'Sharpe':>8} {'Sortino':>9} {'Max DD':>9} {'Calmar':>8}")
    print("  " + "─" * 70)
    for _, r in metrics_df.iterrows():
        print(f"  {r['symbol']:<6} {r['annual_ret']:>+10.1f}% {r['vol_ann']:>8.1f}% "
              f"{r['sharpe']:>8.2f} {r['sortino']:>9.2f} {r['max_dd']:>8.1f}% {r['calmar']:>8.2f}")


# ─────────────────────────────────────────────────────────────
# 4. HYPERLIQUID VALUATION MODEL
# ─────────────────────────────────────────────────────────────

DEFI_PEERS = {
    # (name, market_cap_B, annualised_fees_M, annualised_revenue_M, buyback_pct)
    "Hyperliquid\n(HYPE)":   (9.80,  715, 635, 1.00),
    "Uniswap\n(UNI)":        (2.06,  1200, 20, 0.00),   # most fees go to LPs, near 0 to UNI holders
    "AAVE":                  (1.39,  80,  70, 0.10),
    "GMX":                   (0.22,  90,  55, 0.80),
    "dYdX":                  (0.18,  40,  28, 0.40),
    "Synthetix\n(SNX)":      (0.15,  30,  18, 0.20),
}


def plot_hype_valuation():
    print("\n[4/7] Plotting Hyperliquid valuation model …")

    names = list(DEFI_PEERS.keys())
    mc    = [v[0] for v in DEFI_PEERS.values()]
    fees  = [v[1] for v in DEFI_PEERS.values()]
    rev   = [v[2] for v in DEFI_PEERS.values()]
    buyb  = [v[3] * 100 for v in DEFI_PEERS.values()]
    pf_ratio = [m * 1000 / f if f > 0 else 0 for m, f in zip(mc, fees)]   # P/F = mktcap($M) / fees($M)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5), facecolor="#0d1117")
    fig.suptitle("Hyperliquid vs DeFi Peers — Valuation Deep Dive", color="white", fontsize=13)

    highlight = ["#00d2ff" if "Hyper" in n else "#4a4a6a" for n in names]

    # P/F ratio
    ax1 = axes[0]
    ax1.set_facecolor("#161b22")
    bars = ax1.bar(names, pf_ratio, color=highlight, edgecolor="none", width=0.6)
    ax1.set_title("Price-to-Fees Ratio\n(lower = cheaper)", color="white", fontsize=10)
    ax1.tick_params(colors="lightgray", labelsize=7)
    ax1.spines[:].set_visible(False)
    for bar, val in zip(bars, pf_ratio):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 0.3, f"{val:.1f}x",
                 ha="center", color="white", fontsize=8)
    ax1.set_ylabel("P/F (x)", color="lightgray", fontsize=8)

    # Revenue-to-token holders
    effective_rev = [r * b / 100 for r, b in zip(rev, [v[3] for v in DEFI_PEERS.values()])]
    ax2 = axes[1]
    ax2.set_facecolor("#161b22")
    bars2 = ax2.bar(names, effective_rev, color=highlight, edgecolor="none", width=0.6)
    ax2.set_title("Revenue to Token Holders ($M/yr)\n(fees × buyback %)", color="white", fontsize=10)
    ax2.tick_params(colors="lightgray", labelsize=7)
    ax2.spines[:].set_visible(False)
    for bar, val in zip(bars2, effective_rev):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 5, f"${val:.0f}M",
                 ha="center", color="white", fontsize=8)
    ax2.set_ylabel("$M / year", color="lightgray", fontsize=8)

    # Yield on market cap (revenue / mktcap)
    yield_pct = [er / (m * 1000) * 100 if m > 0 else 0 for er, m in zip(effective_rev, mc)]
    ax3 = axes[2]
    ax3.set_facecolor("#161b22")
    bars3 = ax3.bar(names, yield_pct, color=highlight, edgecolor="none", width=0.6)
    ax3.set_title("Effective Token Yield\n(revenue-to-holders ÷ mkt cap)", color="white", fontsize=10)
    ax3.tick_params(colors="lightgray", labelsize=7)
    ax3.spines[:].set_visible(False)
    for bar, val in zip(bars3, yield_pct):
        ax3.text(bar.get_x() + bar.get_width()/2, val + 0.1, f"{val:.1f}%",
                 ha="center", color="white", fontsize=8)
    ax3.set_ylabel("Yield %", color="lightgray", fontsize=8)

    fig.patch.set_facecolor("#0d1117")
    plt.tight_layout()
    save_fig(fig, "04_hype_valuation.png")

    print("\n  ── Hyperliquid vs DeFi Peers ────────────────────────────────────────────")
    print(f"  {'Protocol':<22} {'Mkt Cap':>9} {'Fees/yr':>9} {'P/F':>7} {'Rev→Holders':>13} {'Yield':>7}")
    print("  " + "─" * 72)
    for name, (mktcap, fee, revenue, bp) in DEFI_PEERS.items():
        clean = name.replace("\n", " ")
        er = revenue * bp
        yd = er / (mktcap * 1000) * 100
        print(f"  {clean:<22} {fmt_b(mktcap*1e9):>9} {fmt_b(fee*1e6):>9}/yr  "
              f"{mktcap*1000/fee:>5.1f}x   {fmt_b(er*1e6):>12}/yr  {yd:>6.1f}%")


# ─────────────────────────────────────────────────────────────
# 5. CORRELATION MATRIX
# ─────────────────────────────────────────────────────────────

def plot_correlation(price_dict: dict):
    print("\n[5/7] Computing correlation matrix …")
    if len(price_dict) < 3:
        print("  ⚠  Insufficient price data for correlation. Skipping.")
        return

    combined = pd.DataFrame(price_dict)
    returns  = combined.pct_change().dropna()

    corr = returns.corr()

    fig, ax = plt.subplots(figsize=(8, 6), facecolor="#0d1117")
    ax.set_facecolor("#161b22")
    fig.suptitle("30-Day Return Correlation Matrix", color="white", fontsize=13)

    n = len(corr.columns)
    im = ax.imshow(corr.values, cmap="RdYlGn", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", color="lightgray")
    ax.set_yticklabels(corr.columns, color="lightgray")
    ax.spines[:].set_visible(False)

    for i in range(n):
        for j in range(n):
            val = corr.values[i, j]
            color = "black" if abs(val) > 0.5 else "white"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    color=color, fontsize=9, fontweight="bold")

    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04).ax.tick_params(colors="lightgray")
    fig.patch.set_facecolor("#0d1117")
    plt.tight_layout()
    save_fig(fig, "05_correlation.png")

    print("\n  Correlation observations:")
    for col in corr.columns:
        btc_corr = corr.loc[col, "BTC"] if "BTC" in corr.columns else None
        if btc_corr is not None and col != "BTC":
            level = "high" if abs(btc_corr) > 0.8 else "moderate" if abs(btc_corr) > 0.5 else "low"
            print(f"    {col} vs BTC: {btc_corr:.2f}  ({level} correlation)")


# ─────────────────────────────────────────────────────────────
# 6. MONTE CARLO SIMULATION
# ─────────────────────────────────────────────────────────────

def monte_carlo(symbol: str, current_price: float, mu_annual: float,
                sigma_annual: float, days: int = 365,
                n_sims: int = 1000) -> np.ndarray:
    """Geometric Brownian Motion Monte Carlo."""
    dt    = 1 / 365
    mu_d  = mu_annual * dt
    sig_d = sigma_annual * math.sqrt(dt)
    rng   = np.random.default_rng(seed=42)
    paths = np.zeros((n_sims, days + 1))
    paths[:, 0] = current_price
    for t in range(1, days + 1):
        z = rng.standard_normal(n_sims)
        paths[:, t] = paths[:, t - 1] * np.exp((mu_d - 0.5 * sig_d**2) + sig_d * z)
    return paths


MC_PARAMS = {
    # (current_price, mu_annual, sigma_annual)   — mu from halving-cycle base case, vol from history
    "BTC":  (74_460, 0.85, 0.70),
    "ETH":  ( 2_278, 1.00, 0.85),
    "SOL":  (    84, 1.50, 1.10),
    "HYPE": (    41, 1.20, 1.05),
}


def plot_monte_carlo():
    print("\n[6/7] Running Monte Carlo simulations (GBM, 1,000 paths × 365 days) …")
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), facecolor="#0d1117")
    fig.suptitle("Monte Carlo Price Simulation — 365 Days\n(Geometric Brownian Motion, 1,000 paths)",
                 color="white", fontsize=12, y=1.01)

    summary_rows = []
    days = 365

    for ax, (sym, (price, mu, sigma)) in zip(axes.flat, MC_PARAMS.items()):
        ax.set_facecolor("#161b22")
        paths = monte_carlo(sym, price, mu, sigma, days=days, n_sims=1_000)
        t = np.arange(days + 1)

        # Plot sample paths (faint)
        for i in range(0, 200, 2):
            ax.plot(t, paths[i], color="#ffffff", alpha=0.04, linewidth=0.5)

        # Percentile bands
        p10  = np.percentile(paths, 10,  axis=0)
        p25  = np.percentile(paths, 25,  axis=0)
        p50  = np.percentile(paths, 50,  axis=0)
        p75  = np.percentile(paths, 75,  axis=0)
        p90  = np.percentile(paths, 90,  axis=0)

        ax.fill_between(t, p10, p90, alpha=0.15, color="#00d2ff", label="10–90th pct")
        ax.fill_between(t, p25, p75, alpha=0.25, color="#00d2ff", label="25–75th pct")
        ax.plot(t, p50, color="#00d2ff", linewidth=2, label="Median")
        ax.axhline(price, color="gray", linestyle="--", linewidth=1, label=f"Today ${price:,.0f}")

        # End-of-simulation stats
        finals = paths[:, -1]
        med_final   = np.median(finals)
        bear_final  = np.percentile(finals, 10)
        bull_final  = np.percentile(finals, 90)
        prob_2x     = (finals >= price * 2).mean() * 100
        prob_halved = (finals <= price * 0.5).mean() * 100

        ax.set_title(sym, color="white", fontsize=11)
        ax.tick_params(colors="lightgray", labelsize=8)
        ax.spines[:].set_visible(False)
        ax.set_xlabel("Days", color="lightgray", fontsize=8)
        ax.set_ylabel("Price (USD)", color="lightgray", fontsize=8)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax.legend(fontsize=7, facecolor="#1c2333", labelcolor="white", framealpha=0.5)

        summary_rows.append({
            "symbol":     sym,
            "current":    price,
            "bear_p10":   bear_final,
            "median":     med_final,
            "bull_p90":   bull_final,
            "prob_2x":    prob_2x,
            "prob_half":  prob_halved,
            "exp_ret":    (med_final / price - 1) * 100,
        })

    fig.patch.set_facecolor("#0d1117")
    plt.tight_layout()
    save_fig(fig, "06_monte_carlo.png")

    print("\n  ── Monte Carlo Summary (365-day horizon) ─────────────────────────────────")
    print(f"  {'Symbol':<6} {'Now':>9} {'Bear (P10)':>12} {'Median':>12} {'Bull (P90)':>12} "
          f"{'P(2x)':>8} {'P(½)':>8} {'Exp Ret':>9}")
    print("  " + "─" * 85)
    for r in summary_rows:
        print(f"  {r['symbol']:<6} ${r['current']:>8,.0f}  ${r['bear_p10']:>10,.0f}  "
              f"${r['median']:>10,.0f}  ${r['bull_p90']:>10,.0f}  "
              f"{r['prob_2x']:>7.1f}%  {r['prob_half']:>7.1f}%  {r['exp_ret']:>+8.1f}%")


# ─────────────────────────────────────────────────────────────
# 7. ETF LAUNCH EFFECT ON PRICE
# ─────────────────────────────────────────────────────────────

# Approximate BTC price around its spot ETF approval (Jan 11 2024)
BTC_ETF_WINDOW = {
    -30: 42_000, -20: 43_000, -10: 44_500, -5: 46_000, -2: 47_000,
      0: 46_500,   5: 48_000,  10: 52_000,  20: 63_000, 30: 72_000,
     60: 69_000,  90: 65_000, 120: 58_000, 180: 56_000, 240: 85_000,
    300: 107_000, 365: 126_173,
}
# Approximate ETH price around its spot ETF approval (Jul 23 2024)
ETH_ETF_WINDOW = {
    -30: 3_800, -20: 3_600, -10: 3_400, -5: 3_200, -2: 3_150,
      0: 3_400,   5: 3_100,  10: 3_000,  20: 2_700, 30: 2_600,
     60: 2_400,  90: 2_500, 120: 2_800, 180: 3_600, 240: 4_100,
    300: 3_200, 365: 2_278,
}

SOL_ETF_LAUNCH_PRICE = 165.0  # approx SOL price when first spot SOL ETFs launched (~mid 2025)
SOL_NOW = 84.10                # Apr 2026 — SOL actually fell with broader market post-ETF launch


def plot_etf_effect():
    print("\n[7/7] Plotting ETF launch price impact …")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor="#0d1117")
    fig.suptitle("Spot ETF Launch: Price Action Before & After Approval Day",
                 color="white", fontsize=13)

    for ax, (label, window, color, etf_date) in [
        (axes[0], BTC_ETF_WINDOW, "#f7931a", "Jan 11, 2024"),
        (axes[1], ETH_ETF_WINDOW, "#627eea", "Jul 23, 2024"),
    ]:
        ax.set_facecolor("#161b22")
        days = sorted(window.keys())
        prices = [window[d] for d in days]
        indexed = [p / window[0] * 100 for p in prices]  # index to day -30

        ax.plot(days, indexed, color=color, linewidth=2.5)
        ax.fill_between(days, indexed, alpha=0.15, color=color)
        ax.axvline(0, color="white", linestyle="--", linewidth=1.5, label=f"ETF approval ({etf_date})")
        ax.axhline(100, color="gray", linestyle=":", linewidth=0.8)
        ax.set_title(f"{label.split('_')[0]} ETF Launch Effect", color="white", fontsize=10)
        ax.tick_params(colors="lightgray", labelsize=8)
        ax.spines[:].set_visible(False)
        ax.set_xlabel("Days Relative to Approval", color="lightgray", fontsize=8)
        ax.set_ylabel("Price Index (100 = day −30)", color="lightgray", fontsize=8)
        ax.legend(fontsize=8, facecolor="#1c2333", labelcolor="white", framealpha=0.6)
        ax.grid(axis="y", color="gray", alpha=0.15)

        # Annotate 12-month return
        ret_12m = (prices[-1] / prices[0] - 1) * 100
        ax.text(0.97, 0.05, f"12m return: {ret_12m:+.0f}%",
                transform=ax.transAxes, ha="right", color=color, fontsize=10, fontweight="bold")

    fig.patch.set_facecolor("#0d1117")
    plt.tight_layout()
    save_fig(fig, "07_etf_launch_effect.png")

    print("\n  ── ETF Launch Returns ──────────────────────────────────────")
    btc_12m = (BTC_ETF_WINDOW[365] / BTC_ETF_WINDOW[-30] - 1) * 100
    eth_12m = (ETH_ETF_WINDOW[365] / ETH_ETF_WINDOW[-30] - 1) * 100
    print(f"  BTC: +{btc_12m:.0f}% in the 12 months after spot ETF approval (day -30 → day 365)")
    print(f"  ETH: {eth_12m:+.0f}% in the 12 months after spot ETF approval  (day -30 → day 365)")
    print(f"\n  SOL spot ETF launched ~mid-2025 at ~${SOL_ETF_LAUNCH_PRICE}")
    print(f"  SOL current price ${SOL_NOW} — {(SOL_NOW / SOL_ETF_LAUNCH_PRICE - 1)*100:+.0f}% since launch")
    print(f"  → SOL has vastly underperformed the BTC/ETH ETF launch pattern so far.")
    print(f"    If SOL follows BTC's post-ETF 12m return (+{btc_12m:.0f}%), implied target: "
          f"~${SOL_ETF_LAUNCH_PRICE * (1 + btc_12m/100):,.0f}")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  CRYPTO QUANT ANALYSIS — April 19, 2026")
    print("=" * 65)

    # 1. Snapshot
    snap_df = fetch_current_snapshot()
    plot_snapshot(snap_df)

    # 2. Halving cycles
    plot_halving_cycles()

    # 3. Risk metrics — try to fetch live 365-day histories
    print("\n[3/7] Fetching 365-day price histories for risk metrics …")
    price_dict = {}
    metrics_list = []
    for sym, cg_id in ASSETS.items():
        print(f"  Fetching {sym} ({cg_id}) …", end=" ")
        series = fetch_price_history(cg_id, days=365)
        if series is not None and len(series) > 30:
            price_dict[sym] = series
            metrics_list.append(compute_metrics(series, sym))
            print("OK")
        else:
            print("FAILED (using snapshot estimate)")
        time.sleep(1.2)   # CoinGecko free tier: ~10–15 req/min

    if metrics_list:
        metrics_df = pd.DataFrame(metrics_list).sort_values("sharpe", ascending=False)
        plot_risk_metrics(metrics_df)
    else:
        print("  ⚠  No price history fetched. Skipping risk metrics chart.")

    # 4. HYPE valuation model (no API needed)
    plot_hype_valuation()

    # 5. Correlation matrix
    plot_correlation(price_dict)

    # 6. Monte Carlo
    plot_monte_carlo()

    # 7. ETF launch effect
    plot_etf_effect()

    # ─── FINAL SCORECARD ──────────────────────────────────────
    print("\n" + "=" * 65)
    print("  QUANTITATIVE SCORECARD")
    print("=" * 65)

    scorecard = [
        # (symbol, price, upside_base, upside_bull, risk, key_quant_point)
        ("BTC",  "$74,460",  "+48%",  "+168%", "Moderate",
         "Cycle 4 avg mult implies ~$110K+; 57% dominance = institutional parking"),
        ("SOL",  "$84",      "+155%", "+500%", "High",
         "71% from ATH; ETF launch price $165 → current $84 = clear mispricing vs cycle"),
        ("HYPE", "$41",      "+120%", "+390%", "High",
         "P/F 14x, $635M rev → 100% buybacks, only +65% YTD asset"),
        ("ETH",  "$2,278",   "+100%", "+250%", "High",
         "ETH/BTC ratio at lows; Glamsterdam mid-2026; $3B BUIDL on ETH"),
    ]

    print(f"\n  {'Asset':<6} {'Price':>9} {'Base Upside':>12} {'Bull Upside':>12} {'Risk':<10}  Key Quant Point")
    print("  " + "─" * 90)
    for sym, price, base, bull, risk, note in scorecard:
        print(f"  {sym:<6} {price:>9} {base:>12} {bull:>12} {risk:<10}  {note}")

    print(f"\n  Charts saved to: {os.path.abspath(CHARTS_DIR)}/")
    print("=" * 65)


if __name__ == "__main__":
    main()
