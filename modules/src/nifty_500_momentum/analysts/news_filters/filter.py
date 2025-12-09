from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime, timedelta
from ..news_model import NewsArticle


class NewsFilterStrategy(ABC):
    """
    Abstract Base Strategy.
    Any new filter must implement the `apply` method.
    """
    @abstractmethod
    def apply(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        pass



