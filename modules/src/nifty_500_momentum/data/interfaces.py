from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict

class StockDataSource(ABC):
    """Interface for fetching stock market data."""
    
    @abstractmethod
    def fetch_history(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """Should return a DataFrame with Index=Date, Cols=[Open, High, Low, Close, Volume]"""
        pass

class NewsDataSource(ABC):
    """Interface for fetching news data."""
    
    @abstractmethod
    def fetch_news(self, query: str, lookback_days: int = 7) -> List[Dict]:
        """Should return a list of dicts: [{'title':..., 'link':..., 'pubDate':...}]"""
        pass

class StorageBackend(ABC):
    """Interface for saving/loading data."""
    
    @abstractmethod
    def save_stock(self, ticker: str, df: pd.DataFrame):
        pass
        
    @abstractmethod
    def load_stock(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def save_news(self, query: str, news_items: List[Dict]):
        pass
    
    @abstractmethod
    def load_news(self, query: str) -> List[Dict]:
        pass