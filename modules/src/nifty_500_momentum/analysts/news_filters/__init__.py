from typing import List, Dict, Any
from pydantic import BaseModel

from ..news_model import NewsArticle
from .filter import NewsFilterStrategy
from .time_recency_filter import TimeRecencyFilter
from .source_blacklist_filter import SourceBlacklistFilter


# Registry to map string names to classes
STRATEGY_MAP = {
    "TimeRecencyFilter": TimeRecencyFilter,
    "SourceBlacklistFilter": SourceBlacklistFilter
}

class SelectNewsFilterStrategy(BaseModel):
    strategy_name: str
    config: Dict[str, Any] = {}


class NewsFilterEngine:
    """
    CONTEXT CLASS
    -------------
    Orchestrates the filtering process by chaining multiple strategies.
    """
    def __init__(self, strategy_configs: List[Dict[str, Any]]):
        """
        Args:
            strategy_configs: List of dicts, e.g.:
            [
                {"name": "TimeRecencyFilter", "params": {"hours": 24}},
                {"name": "SourceBlacklistFilter", "params": {"blacklisted_sources": ["Fool"]}}
            ]
        """
        self.strategies: List[NewsFilterStrategy] = []
        self._initialize_strategies(strategy_configs)

    def _initialize_strategies(self, configs: List[SelectNewsFilterStrategy]):
        for config in configs:
            strat_name = config.strategy_name
            params = config.config
            
            if strat_name in STRATEGY_MAP:
                strategy_class = STRATEGY_MAP[strat_name]
                try:
                    # Dynamically instantiate the strategy with kwargs
                    instance = strategy_class(**params)
                    self.strategies.append(instance)
                except TypeError as e:
                    print(f"Error initializing {strat_name}: {e}")
            else:
                print(f"Warning: Strategy '{strat_name}' not found in registry.")

    def run(self, raw_data: List[dict]) -> List[NewsArticle]:
        # 1. Convert raw dicts to Pydantic Models (Validation Layer)
        articles = [NewsArticle(**item) for item in raw_data]
        
        # 2. Apply all strategies sequentially
        for strategy in self.strategies:
            if not articles: break # Stop if filtered down to zero
            articles = strategy.apply(articles)
            
        return articles