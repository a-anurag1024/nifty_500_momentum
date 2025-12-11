from pydantic import BaseModel 
from typing import List, Dict, Any

from nifty_500_momentum.static.shortlister import Strategies
from .news_filters import SelectNewsFilterStrategy
from .news_model import NewsArticle


class AnalystState(BaseModel):
    run_id: str
    analysis_id: str
    shortlisting_strategy: Strategies
    NEWS_QUERY_PREFIX: str 
    NEWS_QUERY_SUFFIX: str 
    news_filters: List[SelectNewsFilterStrategy]
    conviction_threshold: float = 5.0
    sentiment_threshold: float = 0.1
    top_n_final_shortlist: int = 5
    
    
    filtered_news: Dict[str, List[NewsArticle]] = {}  # ticker -> list of news article dicts
    analysis_results: Dict[str, Any] = {}  # ticker -> analysis result
    final_shortlist: Dict[int, str] = {}  # rank -> ticker