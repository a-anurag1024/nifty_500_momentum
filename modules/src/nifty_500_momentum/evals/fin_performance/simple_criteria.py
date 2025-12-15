import pandas as pd 
from typing import Dict 

from .base_criteria import WinCriteria


class SimpleReturnCriteria(WinCriteria):
    """
    Basic Win: Is Price(T+n) > Price(T+0)?
    """
    def evaluate(self, prices: pd.Series) -> Dict[str, float]:
        if len(prices) < 2:
            return {'is_win': 0.0, 'magnitude': 0.0, 'details': 'Insufficient Data'}
            
        start_price = prices.iloc[0]
        end_price = prices.iloc[-1]
        
        # Calculate Percentage Return
        ret = (end_price - start_price) / start_price
        
        return {
            'is_win': 1.0 if ret > 0 else 0.0,
            'magnitude': ret,
            'details': f"Return: {round(ret*100, 2)}%"
        }