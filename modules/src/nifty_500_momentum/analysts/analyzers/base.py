from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel 

from nifty_500_momentum.static.shortlister import StaticScoutResult
from nifty_500_momentum.analysts.news_model import NewsArticle
from nifty_500_momentum.llm import llm, StructuredLLMInput



class AnalyzerInput(BaseModel):
    static_results: StaticScoutResult
    news_data: List[NewsArticle]


class BaseAnalyzer(ABC):
    """
    Abstract Base Strategy.
    Any new analyzer must implement the `analyze` method.
    """
    def __init__(self):
        self.llm = llm
    
    @abstractmethod
    def analyze(self, data: AnalyzerInput) -> Any:
        pass