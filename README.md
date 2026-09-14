# LaunchTower — Momentum + Quality Factor Research Report
**Date:** 2026-09-16 · **Universe:** 109 US large-caps · **Data:** yfinance (public, adjusted close)

> ⚠️ **Honesty first.** This is a transparent, reproducible research tool built from public data. It is **not** investment advice, and it does **not** promise returns. We include our own backtest — including the months where the signal lost money — because a factor model you can't see the failure cases of is not a model, it's a sales pitch.

---

## 1. What this is (and isn't)

**Is:** a 2-factor cross-sectional screen — 12-month momentum + low-volatility quality — applied to 109 US large-caps, fully reproducible from public data with ~15 lines of core logic.

**Is not:** a black box, an ML model, a "proprietary alpha" feed, or a return guarantee. The composite is simply:

```
composite = 0.5 · z(12m return) + 0.5 · z(−annualized vol)
```

z-scores are cross-sectional (mean 0, std 1) on the current universe. Rank 1 = highest composite.

---

## 2. The backtest — including where it lost

We backtested the long top-20% / short bottom-20% of the composite, monthly rebalance, 24 periods over ~3 years (2023 → 2026), 109 tickers.

| Metric | Value |
|---|---|
| Avg top-20% forward return | **+2.63% / month** |
| Avg bottom-20% forward return | **+3.21% / month** |
| **Avg long-short spread** | **−0.58% / month** |
| Spread positive | **13 of 24 months** |
| Best month (LS) | +12.41% (2025-12-31) |
| Worst month (LS) | −21.49% (2026-07-31) |

**Read this honestly:** over this window the naive long-short version of the signal did **not** produce a positive edge. That is a real result, not a bug. It means:

- The signal is a **ranking/screening tool**, not a standalone alpha source.
- It is most useful as a **universe filter and risk overlay** (e.g., "which names have momentum *and* acceptable vol?"), not as a buy/sell oracle.
- Any product that sold this as "guaranteed alpha" would be lying. We don't.

This is the difference between a research tool and a scam, and it's why we publish the losing months.

---

## 3. Current screen (2026-09-16)

**Top 10 (highest composite):**

| # | Ticker | 12m Return | Ann. Vol | Composite |
|---|--------|-----------|----------|-----------|
| 1 | **MU** | +597.7% | 81.5% | **+1.838** |
| 2 | WDC | +371.5% | 80.2% | +0.740 |
| 3 | STX | +333.6% | 74.8% | +0.675 |
| 4 | VLO | +151.5% | 36.1% | +0.654 |
| 5 | JNJ | +54.5% | 19.2% | +0.560 |
| 6 | MPC | +121.6% | 34.2% | +0.549 |
| 7 | PSX | +103.3% | 30.9% | +0.534 |
| 8 | INTC | +315.6% | 79.5% | +0.478 |
| 9 | FDX | +73.8% | 28.3% | +0.446 |
| 10 | TGT | +78.6% | 30.6% | +0.418 |

**Bottom 10 (lowest composite):**

| # | Ticker | 12m Return | Ann. Vol | Composite |
|---|--------|-----------|----------|-----------|
| 100 | PLTR | +0.3% | 60.8% | −0.665 |
| 101 | NOW | −28.3% | 56.8% | −0.716 |
| 102 | RKT | −36.9% | 57.6% | −0.777 |
| 103 | ORCL | −53.7% | 57.2% | −0.853 |
| 104 | ZS | −41.0% | 63.1% | −0.925 |
| 105 | HOOD | −4.2% | 72.0% | −0.946 |
| 106 | COIN | −44.4% | 70.7% | −1.116 |
| 107 | RBLX | −65.7% | 67.1% | −1.139 |
| 108 | MRNA | +492.2% | 192.2% | −1.226 |
| 109 | **SMCI** | −8.7% | 91.4% | **−1.412** |

**What stands out:**
- **Memory/storage is the momentum story** — MU, WDC, STX lead on 12m returns (HBM/DRAM cycle).
- **Refiners + defensives are the quality story** — VLO, MPC, PSX, JNJ sit high on low vol.
- **MRNA is the designed outlier** — +492% 12m return but 192% vol drags it to #108. The composite is doing exactly what it's built to do: penalize lottery-ticket vol.
- **SMCI is the clearest "avoid"** — bottom on both legs.

---

## 4. How to reproduce every number

```bash
pip install yfinance pandas numpy
python launchtower_factor_screen_2026-09-16.py
```

The script pulls 2 years of adjusted closes for the universe, computes 1m/3m/6m/12m returns, annualized vol, max drawdown, distance from 52w high, z-scores the 12m return (momentum) and negated vol (quality), averages them, and ranks. Config knobs at the top: universe, lookback, weights.

---

## 5. What's in the full pack

- **Full 109-ticker CSV** — all columns: raw factors, z-scores, composite, rank
- **This dated research report** — including the backtest with its losing months
- **Runnable Python script** — exact code to regenerate every number
- **Backtest results CSV** — 24 rebalance periods, top/bottom forward returns, long-short spread

**No subscription. No email gate. No "add to cart" upsell. One-time purchase.**

---

*LaunchTower — independent market-data desk. Data: yfinance (public). All figures regenerated from live data at generation time. Not investment advice; past performance does not guarantee future results.*
