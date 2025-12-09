from typing import List
import logging

from .filter import NewsFilterStrategy
from ..news_model import NewsArticle



class SourceBlacklistFilter(NewsFilterStrategy):
    """
    STRATEGY 2: BLACKLIST FILTER
    ----------------------------
    Removes articles from low-quality or subscription-walled sources.
    Matches partial strings (e.g., 'Fool' matches 'Motley Fool').
    """
    def __init__(self, 
                 blacklisted_sources: List[str] = []):
        self.blacklist = [s.lower() for s in blacklisted_sources]

    def apply(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        filtered = []
        
        for article in articles:
            # Check if any blacklisted term is in the source name
            source_lower = article.source.lower()
            is_blacklisted = any(b in source_lower for b in self.blacklist)
            
            if not is_blacklisted:
                filtered.append(article)
                
        logging.info(f"  [Source Filter] Kept {len(filtered)}/{len(articles)} articles")
        return filtered