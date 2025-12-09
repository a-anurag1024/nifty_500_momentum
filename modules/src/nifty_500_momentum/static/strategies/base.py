from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd
from pydantic import BaseModel

class StaticScoutResult(BaseModel):
    pass_filter: bool
    metrics: Dict[str, float] = {}
    reason: str = ""

class MomentumStrategy(ABC):
    @abstractmethod
    def analyze(self, df: pd.DataFrame) -> StaticScoutResult:
        pass





