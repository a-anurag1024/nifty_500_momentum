import feedparser
import urllib.parse
from nifty_500_momentum.data.interfaces import NewsDataSource

import logging

class GoogleNewsRSSSource(NewsDataSource):
    def fetch_news(self, query: str, lookback_days: int = 7) -> list:
        """
        Fetches news from Google News RSS.
        """
        base_url = "https://news.google.com/rss/search"
        
        # Build search query params
        # ceid=IN:en sets region to India, Language to English
        params = {
            "q": f"{query} when:{lookback_days}d",
            "hl": "en-IN",
            "gl": "IN",
            "ceid": "IN:en"
        }
        
        encoded_query = urllib.parse.urlencode(params)
        final_url = f"{base_url}?{encoded_query}"
        
        try:
            feed = feedparser.parse(final_url)
            news_items = []
            
            for entry in feed.entries:
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published,
                    "source": entry.source.title if 'source' in entry else "Google News"
                })
                
            return news_items
            
        except Exception as e:
            logging.error(f"Error fetching news for {query}: {e}")
            return []