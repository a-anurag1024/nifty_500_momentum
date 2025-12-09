from pydantic import BaseModel
from typing import Dict, List
import json
import time 
import numpy as np

from .base_collector import DataCollector


class NewsDataCollectorInputs(BaseModel):
    tickers: List[str] = []
    query_prefix: str = ""
    query_postfix: str = ""
    force_refresh: bool = False


class NewsDataCollector(DataCollector):
    def collect(self, inputs: NewsDataCollectorInputs) -> None:
        company_names = self.data_manager.storage.load_tickers()
            
        for ticker in inputs.tickers:
            try:
                company_name = company_names[ticker]
            except KeyError:
                raise ValueError(f"Ticker {ticker} not found in tickers.json")
            self.data_manager.get_news_for_stock(
                ticker=ticker,
                company_name=company_name,
                custom_query=f"{inputs.query_prefix} {company_name} {inputs.query_postfix}".strip(),
                force_refresh=inputs.force_refresh
            )
            time.sleep(self.data_config.news_api_sleep + np.random.uniform(0, 4))