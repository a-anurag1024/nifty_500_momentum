import pandas as pd
import nifty_500_momentum.static.indicators as ind
from nifty_500_momentum.static.strategies.base import MomentumStrategy, StaticScoutResult


class TrendSurferStrategy(MomentumStrategy):
    """
    Target: Steady Uptrend (SMA 200) + Strong ADX
    """
    def analyze(self, df: pd.DataFrame) -> StaticScoutResult:
        sma50 = ind.calculate_sma(df, 50)
        sma200 = ind.calculate_sma(df, 200)
        adx_df = ind.calculate_adx(df)
        
        try:
            price = df['Close'].iloc[-1]
            l_sma50 = sma50.iloc[-1]
            l_sma200 = sma200.iloc[-1]
            l_adx = adx_df['ADX'].iloc[-1]
        except IndexError:
            return StaticScoutResult(
                pass_filter=False,
                metrics={},
                reason="Data Error"
            )

        pass_filter = False
        reason = "Trend Weak"

        if price > l_sma50 > l_sma200 and l_adx > 25:
            pass_filter = True
            reason = "Steady Uptrend (ADX > 25)"

        return StaticScoutResult(
            pass_filter=pass_filter,
            metrics={'ADX': round(l_adx, 2), 'SMA_Diff': round(l_sma50 - l_sma200, 2)},
            reason=reason
        )