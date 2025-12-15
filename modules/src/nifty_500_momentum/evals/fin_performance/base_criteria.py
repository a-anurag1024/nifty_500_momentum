from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd


class WinCriteria(ABC):
    """
    Abstract Strategy for defining what constitutes a 'Win' or 'Loss'
    over a lookahead period.
    """
    @abstractmethod
    def evaluate(self, prices: pd.Series) -> Dict[str, float]:
        """
        Args:
            prices: Series of 'Close' prices starting from the recommendation date (T+0 to T+n).
        Returns:
            dict: {'is_win': 1.0/0.0, 'magnitude': float, 'details': str}
        """
        pass