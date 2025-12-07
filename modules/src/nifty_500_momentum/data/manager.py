import time
import pandas as pd
import logging
import numpy as np
from typing import List, Optional
from nifty_500_momentum.data.config import DATA_CONFIG, DataConfig
from nifty_500_momentum.data.interfaces import StockDataSource, NewsDataSource, StorageBackend
from nifty_500_momentum.data.sources import YFinanceSource, GoogleNewsRSSSource
from nifty_500_momentum.data.storage import LocalStorage

class DataManager:
    def __init__(
        self,
        *,
        config: DataConfig = DATA_CONFIG,
        stock_api: Optional[StockDataSource] = None,
        news_api: Optional[NewsDataSource] = None,
        storage: Optional[StorageBackend] = None,
    ) -> None:
        self.config = config
        self.stock_api: StockDataSource = stock_api or YFinanceSource()
        self.news_api: NewsDataSource = news_api or GoogleNewsRSSSource()
        self.storage: StorageBackend = storage or LocalStorage(config)
        logging.basicConfig(level=logging.INFO)

    # --- Pipeline 1: Stock Data Collection ---
    def collect_stock_universe(self, 
                               tickers: List[str], 
                               period: str = "2y",
                               force_refresh: bool = False) -> None:
        """
        Iterates through list of tickers, fetches data, and saves to storage.
        Includes Rate Limiting.
        """
        logging.info(f"Starting collection for {len(tickers)} stocks...")
        
        success_count = 0
        
        for i, ticker in enumerate(tickers):
            try:
                if not force_refresh:
                    try:
                        _ = self.storage.load_stock(ticker)
                        logging.info(f"[{i+1}/{len(tickers)}] {ticker} already exists. Skipping.")
                        success_count += 1
                        continue
                    except FileNotFoundError:
                        pass
                logging.info(f"[{i+1}/{len(tickers)}] Fetching {ticker}...")
                
                df = self.stock_api.fetch_history(ticker, period)
                
                if not df.empty:
                    self.storage.save_stock(ticker, df)
                    logging.info("Done.")
                    success_count += 1
                else:
                    logging.warning("Empty Data.")
                
                # Rate Limiting
                time.sleep(self.config.stock_api_sleep + np.random.uniform(0, 3))
                
            except Exception as e:
                logging.error(f"Failed: {e}")
                
        logging.info(f"Collection Complete. Success: {success_count}/{len(tickers)}")

    # --- Pipeline 2: Stock Data Retrieval ---
    def get_stock_data(self, ticker: str) -> pd.DataFrame:
        """
        Fetches stock data from LOCAL STORAGE.
        Raises error if data is missing (forcing user to run collection).
        """
        try:
            return self.storage.load_stock(ticker)
        except FileNotFoundError:
            # Custom error handling or re-raising
            logging.error(f"ERROR: Data for {ticker} not found locally.")
            logging.info(f"Tip: Run 'collect_stock_universe(['{ticker}'])' first.")
            return pd.DataFrame()

    # --- Pipeline 3: News Data (Fetch + Cache) ---
    def get_news_for_stock(self, 
                           ticker: str, 
                           company_name: str = "",
                           custom_query: str|None = None,
                           force_refresh: bool = False) -> list:
        """
        Fetches news for a stock. 
        1. Checks Cache
        2. If missing/expired -> Calls API -> Saves to Cache
        """
        # Construct a search query (e.g., "Tata Motors stock news")
        query = custom_query if custom_query else f"{company_name if company_name else ticker} stock news India"
        
        # 1. Try Cache
        cached_data = self.storage.load_news(query)
        if cached_data and not force_refresh:
            logging.info(f"Loaded news for {ticker} from cache.")
            return cached_data
            
        # 2. Fetch from API
        logging.info(f"Fetching fresh news for {ticker}...")
        news_items = self.news_api.fetch_news(query)
        
        # 3. Save to Cache
        if news_items:
            self.storage.save_news(query, news_items)
            
        return news_items

"""
# --- Example Usage (If running this file directly) ---
if __name__ == "__main__":
    dm = DataManager()
    
    # 1. Collect Data
    my_watchlist = ["RELIANCE", "TCS", "INFY"]
    dm.collect_stock_universe(my_watchlist)
    
    # 2. Fetch Data for Analysis
    df = dm.get_stock_data("RELIANCE")
    print(f"Loaded Reliance Data: {df.shape}")
    
    # 3. Get News
    news = dm.get_news_for_stock("RELIANCE", "Reliance Industries")
    print(f"Found {len(news)} news articles.")
"""