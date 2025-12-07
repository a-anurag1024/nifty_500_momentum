from pathlib import Path
import pandas as pd
import json
import hashlib
from nifty_500_momentum.data.interfaces import StorageBackend
from nifty_500_momentum.data.config import DATA_CONFIG, DataConfig

import logging

class LocalStorage(StorageBackend):
    def __init__(self, config: DataConfig = DATA_CONFIG) -> None:
        self.config = config
    
    def _get_stock_path(self, ticker: str) -> Path:
        safe_ticker = ticker.replace(".NS", "").replace(".BO", "")
        return self.config.stock_data_dir / f"{safe_ticker}{self.config.stock_file_ext}"

    def _get_news_path(self, query: str) -> Path:
        # Create a safe filename hash from the query
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return self.config.news_data_dir / f"{query_hash}{self.config.news_file_ext}"

    # --- Stock Methods ---
    def save_stock(self, ticker: str, df: pd.DataFrame):
        path = self._get_stock_path(ticker)
        # Parquet preserves index (dates) and types better than CSV
        df.to_parquet(path)
        logging.info(f"Saved {ticker} to {path}")

    def load_stock(self, ticker: str) -> pd.DataFrame:
        path = self._get_stock_path(ticker)
        if not path.exists():
            raise FileNotFoundError(f"No stored data for {ticker}. Run collection first.")
        return pd.read_parquet(path)

    # --- News Methods ---
    def save_news(self, query: str, news_items: list):
        path = self._get_news_path(query)
        data = {
            "query": query,
            "timestamp": pd.Timestamp.now().isoformat(),
            "articles": news_items
        }
        with path.open('w') as f:
            json.dump(data, f, indent=4)

    def load_news(self, query: str) -> list:
        path = self._get_news_path(query)
        if not path.exists():
            return None
            
        with path.open('r') as f:
            data = json.load(f)
            
        # Basic Cache Check
        stored_time = pd.Timestamp(data['timestamp'])
        if (pd.Timestamp.now() - stored_time).total_seconds() / 3600 > self.config.cache_expiry_hours:
            return None # Cache expired
            
        return data['articles']