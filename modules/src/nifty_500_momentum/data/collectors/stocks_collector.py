from pydantic import BaseModel
from typing import Dict
import json

from .base_collector import DataCollector


class StocksDataCollectorInputs(BaseModel):
    all_tickers: bool = True
    tickers: Dict[str, str] = {}
    period: str = "2y"
    force_refresh: bool = False


class StocksDataCollector(DataCollector):
    def collect(self, inputs: StocksDataCollectorInputs) -> None:
        if inputs.all_tickers:
            from nifty_500_momentum.data.nifty_500_tickers import get_nifty500_tickers
            tickers = get_nifty500_tickers()
        else:
            tickers = inputs.tickers
        
        with open(self.data_config.data_dir / "tickers.json", "w") as f:
            json.dump(tickers, f, indent=4)
            
        period = inputs.period
        force_refresh = inputs.force_refresh
        
        self.data_manager.collect_stock_universe(
            tickers=tickers,
            period=period,
            force_refresh=force_refresh
        )