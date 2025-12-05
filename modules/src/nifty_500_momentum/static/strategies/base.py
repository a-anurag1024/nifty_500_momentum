from abc import ABC, abstractmethod
import pandas as pd

class MomentumStrategy(ABC):
    @abstractmethod
    def analyze(self, df: pd.DataFrame) -> dict:
        pass





