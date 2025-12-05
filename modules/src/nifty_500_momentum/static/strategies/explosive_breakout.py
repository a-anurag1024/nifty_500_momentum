import pandas as pd
import nifty_500_momentum.static.indicators as ind
from nifty_500_momentum.static.strategies.base import MomentumStrategy


class ExplosiveBreakoutStrategy(MomentumStrategy):
    """
    Target: High Volume Spike + High Speed
    """
    def analyze(self, df: pd.DataFrame) -> dict:
        rvol = ind.calculate_relative_volume(df)
        roc = ind.calculate_roc(df)
        rsi = ind.calculate_rsi(df)
        
        try:
            # Check latest values
            l_rvol = rvol.iloc[-1]
            l_roc = roc.iloc[-1]
            l_rsi = rsi.iloc[-1]
        except IndexError:
            return {'pass_filter': False, 'reason': "Data Error"}

        pass_filter = False
        reason = "Momentum weak"

        # Logic: Volume > 2x average AND moved > 10% in 10 days
        if l_rvol > 2.0 and l_roc > 10.0:
            if l_rsi < 85: # Not too extended
                pass_filter = True
                reason = "Explosive Vol & Speed"
            else:
                reason = "Overbought (RSI > 85)"

        return {
            'pass_filter': pass_filter,
            'metrics': {'RVOL': round(l_rvol, 2), 'ROC': round(l_roc, 2)},
            'reason': reason
        }