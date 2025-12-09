from pydantic import BaseModel 
from typing import List, Dict

from nifty_500_momentum.static.shortlister import Strategies
from .news_filters import SelectNewsFilterStrategy
from .news_model import NewsArticle


class AnalystState(BaseModel):
    run_id: str
    analysis_id: str
    shortlisting_strategy: Strategies
    news_filters: List[SelectNewsFilterStrategy]
    
    filtered_news: Dict[str, List[NewsArticle]] = {}  # ticker -> list of news article dicts
    analysis_results: Dict[str, BaseModel] = {}  # ticker -> analysis result