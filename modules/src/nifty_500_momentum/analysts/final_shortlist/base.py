from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel 

from nifty_500_momentum.llm import llm, StructuredLLMInput


class BaseFinalShortlist(ABC):
    """
    Abstract Base Strategy.
    Any new FinalShortlist must implement the `shortlist` method.
    """
    def __init__(self):
        self.llm = llm
    
    @abstractmethod
    def shortlist(self, results: Dict[str, Any], **kwargs) -> Dict[int, str]:
        """
        Returns a ranked dictionary of final shortlisted tickers and their details.
        """
        pass