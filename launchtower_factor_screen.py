#!/usr/bin/env python3
"""
LaunchTower — Momentum + Quality Factor Screen (2026-09-16)
Reproducible from public data. NOT investment advice.

Model: composite = 0.5 * z(12m return) + 0.5 * z(-annualized vol)
z-scores are cross-sectional (mean 0, std 1) on the current universe.

Usage:
    pip install yfinance pandas numpy
    python launchtower_factor_screen_2026-09-16.py
"""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import yfinance as yf

# ---------------- CONFIG ----------------
UNIVERSE = [
    "AAPL","MSFT","NVDA","AMD","MU","INTC","META","GOOGL","AMZN","TSLA",
    "VLO","MPC","PSX","XOM","CVX","COP","OXY","HOOD","COIN","ZS",
    "MRNA","SMCI","AVGO","QCOM","TXN","NOW","CRM","ORCL","ADBE","INTU",
    "PLTR","SNOW","DASH","RBLX","UBER","ABNB","SHOP","PYPL","V",
    "MA","JPM","GS","MS","BAC","WFC","C","BLK","SCHW","AXP","SPGI","MCO",
    "UNH","LLY","JNJ","MRK","ABBV","PFE","BMY","TMO","DHR","ISRG","VRTX","AMGN",
    "CAT","DE","GE","BA","LMT","RTX","NOC","HON","EMR","ETN","PH","MMM","UPS","FDX",
    "COST","WMT","HD","LOW","TGT","NKE","SBUX","MCD","CMG","YUM","LULU","TJX","ROST",
    "DIS","NFLX","CMCSA","TMUS","VZ","T","RKT","TTWO","EA","BIDU","PDD","BABA",
    "TSM","ASML","AMAT","KLAC","LRCX","ON","WDC","STX","WMT","ROST",
]
UNIVERSE = list(dict.fromkeys(UNIVERSE))  # dedupe, keep order
LOOKBACK_DAYS = 252          # 12-month momentum lookback
MOM_WEIGHT = 0.5             # weight on momentum leg
QUAL_WEIGHT = 0.5            # weight on quality (low-vol) leg
# ----------------------------------------

def zscore(s: pd.Series) -> pd.Series:
    return (s - s.mean()) / s.std()

def main():
    print(f"Pulling {len(UNIVERSE)} tickers, 2y adjusted close ...")
    close = yf.download(UNIVERSE, period="2y", interval="1d",
                        auto_adjust=True, progress=False)["Close"]
    close = close.dropna(axis=1, thresh=int(0.6 * len(close)))  # drop sparse
    print(f"Valid tickers: {close.shape[1]}  |  last date: {close.index[-1].date()}")

    last = close.index[-1]
    ret1  = close.pct_change(21).loc[last]
    ret3  = close.pct_change(63).loc[last]
    ret6  = close.pct_change(126).loc[last]
    ret12 = close.pct_change(LOOKBACK_DAYS).loc[last]
    vol   = close.pct_change().rolling(LOOKBACK_DAYS).std().loc[last] * np.sqrt(252)
    hi52  = close.rolling(LOOKBACK_DAYS).max().loc[last]
    dist_hi = close.loc[last] / hi52 - 1
    mdd   = (close / close.cummax() - 1).rolling(LOOKBACK_DAYS).min().loc[last]

    df = pd.DataFrame({
        "ret1": ret1, "ret3": ret3, "ret6": ret6, "ret12": ret12,
        "vol": vol, "dist_hi": dist_hi, "mdd": mdd,
    }).dropna()

    df["z_mom"] = zscore(df["ret12"])
    df["z_q"]   = zscore(-df["vol"])
    df["composite"] = MOM_WEIGHT * df["z_mom"] + QUAL_WEIGHT * df["z_q"]
    df = df.sort_values("composite", ascending=False).reset_index()
    df["rank"] = range(1, len(df) + 1)

    out = "launchtower_screen.csv"
    df.to_csv(out, index=False)
    print(f"\nSaved {out} ({len(df)} rows)\n")
    print("TOP 10:")
    print(df.head(10)[["rank","index","ret12","vol","composite"]].to_string(index=False))
    print("\nBOTTOM 10:")
    print(df.tail(10)[["rank","index","ret12","vol","composite"]].to_string(index=False))

    print("\nNOTE: This is a transparent screening tool, not a return guarantee.")
    print("See the dated research report for the full backtest (incl. losing months).")

if __name__ == "__main__":
    main()
