
# Momentum Filtering Strategies — Conceptual Framework

This document explains the **four momentum filtering strategies** used in the static scouting layer.  
Each strategy combines **multiple momentum indicators** to identify *specific momentum regimes* rather than relying on a single signal.

The goal is **not prediction**, but **classification**:
> “What *type* of momentum is this stock currently exhibiting?”

---

## Why Multi-Indicator Momentum Strategies?

Single indicators often fail because:
- Momentum can appear **fast but fragile**
- Or **slow but persistent**
- Or **early but noisy**

Each strategy below targets a **distinct market behavior** by combining:
- **Speed (ROC)**
- **Participation (Volume)**
- **Trend structure (SMA, ADX)**
- **Cycle shifts (MACD, RSI)**
- **Long-term persistence (12M momentum)**

---

## 1. Explosive Breakout Strategy  
**Target:** Sudden, high-energy price expansion

### Momentum Regime
This strategy captures **short-term explosive momentum**, typically seen when:
- Fresh news hits the market
- Institutions suddenly accumulate
- A stock breaks out of consolidation

---

### Indicators Used
- **Relative Volume (RVOL)** → Confirms abnormal participation
- **Rate of Change (ROC)** → Measures speed of price movement
- **RSI** → Filters overly stretched moves

---

### Conceptual Logic
A breakout is considered *explosive* when:
1. **Volume expands sharply**  
   → Indicates conviction and liquidity
2. **Price moves rapidly over a short window**  
   → Confirms momentum acceleration
3. **Momentum is not yet exhausted**  
   → Avoids late-stage FOMO entries

---

### Why This Works
- Volume confirms that price movement is **not random**
- ROC ensures the move has **real velocity**
- RSI guardrail avoids **blow-off tops**

---

### Typical Use Case
- Short-term watchlists
- Momentum continuation plays
- News-driven breakouts

---

### Key Risk
- Highly sensitive to **event noise**
- Can fail if volume spike is speculative rather than institutional

---

## 2. Golden Momentum Strategy  
**Target:** Long-term momentum leaders

### Momentum Regime
This strategy identifies **structural winners** — stocks that have:
- Outperformed over long horizons
- Sustained institutional interest
- Strong relative strength across market cycles

---

### Indicators Used
- **12-Month Momentum (excluding last month)** → Persistence filter
- **200-day SMA** → Long-term trend confirmation

---

### Conceptual Logic
A stock qualifies when:
1. **It has delivered strong returns over the past year**  
   → Captures momentum persistence
2. **It trades above its long-term trend**  
   → Confirms structural uptrend
3. **Recent mean reversion noise is ignored**  
   → Improves robustness

---

### Why This Works
- Academic research strongly supports **12-month momentum**
- Excluding the last month reduces **short-term reversal bias**
- 200 SMA filters out weak or decaying leaders

---

### Typical Use Case
- Medium to long-term portfolios
- Factor investing
- Momentum ranking systems

---

### Key Risk
- Slow reaction to regime changes
- Underperforms during sharp market reversals

---

## 3. Trend Surfer Strategy  
**Target:** Clean, sustained uptrends

### Momentum Regime
This strategy captures **orderly trending stocks** — not explosive, not early, but *reliably trending*.

---

### Indicators Used
- **50-day SMA** → Intermediate trend
- **200-day SMA** → Structural trend
- **ADX** → Trend strength filter

---

### Conceptual Logic
A stock is considered a trend candidate when:
1. **Price > SMA50 > SMA200**  
   → Strong bullish structure
2. **ADX exceeds a strength threshold**  
   → Confirms trend is real, not noise

---

### Why This Works
- Moving average alignment captures **trend hierarchy**
- ADX prevents false signals in range-bound markets
- Focuses on *quality of trend*, not speed

---

### Typical Use Case
- Swing trading
- Trend-following systems
- Low-noise momentum selection

---

### Key Risk
- Enters late in fast-moving stocks
- Misses early breakout phases

---

## 4. Reversal Hunter Strategy  
**Target:** Early momentum reversals

### Momentum Regime
This strategy identifies **transition phases** — when a stock shifts from:
> Weak → Neutral → Emerging strength

---

### Indicators Used
- **MACD Histogram** → Momentum cycle shift
- **RSI** → Momentum recovery zone

---

### Conceptual Logic
A reversal is considered valid when:
1. **MACD histogram flips from negative to positive**  
   → Momentum inflection point
2. **RSI is in a neutral recovery zone**  
   → Avoids oversold traps and overbought entries

---

### Why This Works
- MACD captures **rate-of-change in trend**
- RSI confirms momentum is **recovering, not stretched**
- Combination reduces false early entries

---

### Typical Use Case
- Bottoming patterns
- Early trend discovery
- Mean reversion → momentum transition

---

### Key Risk
- Higher false positives
- Requires confirmation from future price action

---

## Strategy Comparison Matrix

| Strategy | Momentum Type | Time Horizon | Best Market Condition |
|--------|--------------|-------------|-----------------------|
| Explosive Breakout | Fast, short-term | Days–Weeks | High volatility, news |
| Golden Momentum | Persistent | Months | Trending markets |
| Trend Surfer | Stable trend | Weeks–Months | Low noise trends |
| Reversal Hunter | Early transition | Days–Weeks | Post-correction |

---

## Final Takeaway

These strategies are **complementary, not competing**.

Each answers a different question:
- *Is momentum explosive?*
- *Is it persistent?*
- *Is it stable?*
- *Is it just beginning?*

By running all four filters in parallel, the system avoids the classic mistake of treating **all momentum as the same phenomenon**.


