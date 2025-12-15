from typing import Dict 
import pandas as pd 

from .base_criteria import WinCriteria


class MomentumContinuationCriteria(WinCriteria):
    """
    Nuanced Win: Did the momentum SUSTAIN?
    Win if:
    1. End Return is Positive AND
    2. Max Drawdown during the period < 3% (didn't crash and recover)
    This filters out volatile 'lucky' picks.
    """
    def __init__(self, max_drawdown_tolerance: float = -0.03):
        self.dd_tol = max_drawdown_tolerance

    def evaluate(self, prices: pd.Series) -> Dict[str, float]:
        if len(prices) < 2:
            return {'is_win': 0.0, 'magnitude': 0.0}
            
        start_price = prices.iloc[0]
        end_price = prices.iloc[-1]
        total_ret = (end_price - start_price) / start_price
        
        # Calculate Max Drawdown from T+0
        # Drawdown = (Min Price in window - Start Price) / Start Price
        min_price = prices.min()
        drawdown = (min_price - start_price) / start_price
        
        is_sustained = (total_ret > 0) and (drawdown > self.dd_tol)
        
        return {
            'is_win': 1.0 if is_sustained else 0.0,
            'magnitude': total_ret,
            'details': f"Ret: {round(total_ret*100, 1)}%, MaxDD: {round(drawdown*100, 1)}%"
        }