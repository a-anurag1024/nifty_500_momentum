import pandas as pd
import nifty_500_momentum.static.indicators as ind
from nifty_500_momentum.static.strategies.base import MomentumStrategy, StaticScoutResult


class ReversalHunterStrategy(MomentumStrategy):
    """
    Target: MACD Crossover from low RSI
    """
    def analyze(self, df: pd.DataFrame) -> StaticScoutResult:
        macd_df = ind.calculate_macd(df)
        rsi = ind.calculate_rsi(df)
        
        try:
            # Using clean column names from our new indicators.py
            l_macd = macd_df['MACD'].iloc[-1]
            l_signal = macd_df['Signal'].iloc[-1]
            l_hist = macd_df['Histogram'].iloc[-1]
            prev_hist = macd_df['Histogram'].iloc[-2]
            l_rsi = rsi.iloc[-1]
        except IndexError:
            return StaticScoutResult(
                pass_filter=False,
                metrics={},
                reason="Data Error"
            )

        pass_filter = False
        reason = "No Signal"

        # Logic: Histogram turned positive (Crossover) AND RSI is recovering
        if l_hist > 0 and prev_hist < 0:
            if 40 < l_rsi < 60: # Sweet spot for entry
                pass_filter = True
                reason = "Fresh MACD Crossover"
            else:
                reason = "RSI too high/low"

        
        return StaticScoutResult(
            pass_filter=pass_filter,
            metrics={'MACD_Hist': round(l_hist, 2), 'RSI': round(l_rsi, 2)},
            reason=reason
        )