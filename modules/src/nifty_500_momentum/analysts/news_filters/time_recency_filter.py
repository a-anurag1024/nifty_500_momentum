from typing import List
from datetime import datetime, timedelta
import logging

from .filter import NewsFilterStrategy
from ..news_model import NewsArticle


class TimeRecencyFilter(NewsFilterStrategy):
    """
    STRATEGY 1: TIME FILTER
    -----------------------
    Keeps articles published within the last 'hours' window.
    """
    def __init__(self, 
                 hours: int = 48):
        self.hours = hours

    def apply(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        cutoff = datetime.now() - timedelta(hours=self.hours)
        filtered = []
        
        for article in articles:
            if article.published_dt and article.published_dt >= cutoff:
                filtered.append(article)
            else:
                if not article.published_dt:
                    logging.warning(f"Article '{article.title}' has no published_dt ({article.published_dt}); excluding from time filter.")
        
        logging.info(f"  [Time Filter] Kept {len(filtered)}/{len(articles)} articles (Last {self.hours}h)")
        return filtered