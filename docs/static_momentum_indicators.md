# Static Momentum Indicators — Theory & Interpretation

This document explains the **theoretical foundation** behind the static momentum indicators used in the project.  
For each indicator, we describe **how it is calculated conceptually** and **why it is useful** for momentum-based analysis.  
No implementation details or code are included.

---

## 1. Relative Strength Index (RSI)

### What it Measures
RSI is a **bounded momentum oscillator** that measures the speed and magnitude of recent price changes to evaluate whether a stock is **overbought or oversold**.

### How It Is Calculated (Conceptually)
- Price changes are separated into **gains** and **losses**.
- Average gains and average losses are smoothed using **Wilder’s exponential smoothing**.
- The ratio of average gains to average losses (RS) is transformed into a bounded index between **0 and 100**.

### Why It Is Useful
- Captures **short-term momentum exhaustion**.
- Helps identify **potential reversals** when price moves too fast.
- Common interpretation:
  - RSI > 70 → Overbought
  - RSI < 30 → Oversold

### Limitations
- Can stay overbought/oversold for long periods in **strong trends**.
- Prone to **false signals** in volatile mid- and small-cap stocks.

---

## 2. Moving Average Convergence Divergence (MACD)

### What it Measures
MACD measures **trend-following momentum** by comparing short-term and long-term price trends.

### How It Is Calculated (Conceptually)
- Compute two **exponentially weighted moving averages (EMAs)** of price:
  - A faster EMA (short-term)
  - A slower EMA (long-term)
- The difference between them forms the **MACD line**.
- A smoothed EMA of the MACD line forms the **signal line**.
- The **histogram** shows the distance between MACD and signal line.

### Why It Is Useful
- Identifies **trend direction** and **momentum shifts**.
- MACD crossovers indicate potential **trend initiation or weakening**.
- Histogram helps visualize **momentum acceleration or deceleration**.

### Limitations
- Lagging indicator (derived from moving averages).
- Less effective in **sideways markets**.

---

## 3. Simple Moving Average (SMA)

### What it Measures
SMA measures the **average price over a fixed lookback period**, smoothing out short-term fluctuations.

### How It Is Calculated (Conceptually)
- Take the arithmetic mean of closing prices over a fixed window.

### Why It Is Useful
- Helps identify **overall trend direction**.
- Widely used as:
  - Dynamic support/resistance
  - Trend filter (price above SMA → bullish bias)

### Limitations
- Reacts slowly to price changes.
- Gives equal weight to old and recent prices.

---

## 4. Exponential Moving Average (EMA)

### What it Measures
EMA is a **trend-following indicator** similar to SMA but more sensitive to recent price changes.

### How It Is Calculated (Conceptually)
- Uses exponential weighting so **recent prices influence the average more** than older prices.

### Why It Is Useful
- Responds faster to trend changes than SMA.
- Preferred in momentum systems where **early detection** matters.
- Forms the backbone of indicators like MACD.

### Limitations
- Still a lagging indicator.
- Can generate noise in choppy markets.

---

## 5. Rate of Change (ROC)

### What it Measures
ROC measures **percentage price change over a fixed period**, representing pure price momentum.

### How It Is Calculated (Conceptually)
- Compare the current price with the price `n` periods ago.
- Express the difference as a percentage.

### Why It Is Useful
- Direct measure of **price acceleration**.
- Helps identify **breakouts** and **momentum bursts**.
- Useful for ranking stocks by short-term strength.

### Limitations
- Extremely sensitive to volatility.
- Can spike due to one-off price moves.

---

## 6. Average Directional Index (ADX) with +DI and −DI

### What it Measures
ADX measures the **strength of a trend**, while +DI and −DI indicate **trend direction**.

### How It Is Calculated (Conceptually)
- True Range (TR) measures volatility-adjusted price movement.
- Directional Movement (+DM, −DM) captures upward vs downward pressure.
- These components are smoothed using **Wilder’s method**.
- +DI and −DI show dominance of buyers or sellers.
- ADX summarizes **trend strength**, independent of direction.

### Why It Is Useful
- Distinguishes between **trending** and **non-trending** markets.
- High ADX → Strong trend (bullish or bearish).
- Low ADX → Range-bound or noisy market.

### Limitations
- Does not indicate direction by itself.
- Lagging due to smoothing.

---

## 7. Relative Volume (RVOL)

### What it Measures
Relative Volume compares current trading volume to its recent average, indicating **unusual market participation**.

### How It Is Calculated (Conceptually)
- Divide current volume by a moving average of historical volume.

### Why It Is Useful
- Confirms whether price moves are **institutionally supported**.
- High relative volume + price breakout → stronger conviction.
- Helps filter out **low-liquidity false breakouts**.

### Limitations
- Volume spikes can occur due to **news-driven noise**.
- Less reliable in illiquid stocks.

---

## 8. 12-Month Momentum Excluding the Last Month (12M–1M)

### What it Measures
This indicator measures **long-term price momentum** while avoiding short-term mean reversion effects.

### How It Is Calculated (Conceptually)
- Compare price from ~12 months ago to price from ~1 month ago.
- Exclude the most recent month to reduce short-term reversal bias.

### Why It Is Useful
- Strongly supported by **academic finance literature**.
- Captures **persistent trend behavior** driven by fundamentals and institutional flows.
- Commonly used in **factor investing and momentum strategies**.

### Limitations
- Slow to react to regime changes.
- Less effective during sharp market reversals.

---

## Summary Table

| Indicator | Captures | Strength | Weakness |
|--------|--------|--------|--------|
| RSI | Short-term momentum | Fast signals | False positives in trends |
| MACD | Trend + momentum | Trend shifts | Lagging |
| SMA | Trend direction | Stability | Slow |
| EMA | Trend direction | Responsiveness | Noise |
| ROC | Price acceleration | Breakout detection | Volatility sensitivity |
| ADX | Trend strength | Trend validation | Directionless |
| Relative Volume | Participation | Signal confirmation | Event noise |
| 12M–1M Momentum | Long-term trend | Robust factor | Slow reaction |

---
