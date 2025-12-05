import pandas as pd
import nifty_500_momentum.static.indicators as ind
from nifty_500_momentum.static.strategies.base import MomentumStrategy


class GoldenMomentumStrategy(MomentumStrategy):
    """
    Target: 12M Momentum Leaders
    """
    def analyze(self, df: pd.DataFrame) -> dict:
        mom_12m = ind.calculate_momentum_12m_1m(df)
        sma200 = ind.calculate_sma(df, 200)
        
        try:
            price = df['Close'].iloc[-1]
            l_mom = mom_12m.iloc[-1]
            l_sma200 = sma200.iloc[-1]
        except IndexError:
            return {'pass_filter': False, 'reason': "Data Error"}

        if pd.isna(l_mom):
            return {'pass_filter': False, 'reason': "New Listing (<1yr)"}

        pass_filter = False
        reason = "Low 12M Momentum"

        if l_mom > 0.20 and price > l_sma200:
            pass_filter = True
            reason = "High 12M Relative Strength"

        return {
            'pass_filter': pass_filter,
            'metrics': {'12M_Mom': f"{round(l_mom*100)}%"},
            'reason': reason
        }