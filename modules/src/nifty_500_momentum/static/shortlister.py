from pydantic import BaseModel 
from enum import Enum
from pandas import DataFrame
import json
from pathlib import Path
from datetime import datetime
import logging

from nifty_500_momentum.static import static_momentum_strategies
from nifty_500_momentum.data.manager import DataManager, DataConfig


class Strategies(str, Enum):
    EXPLOSIVE_BREAKOUT = "explosive_breakout"
    GOLDEN_MOMENTUM = "golden_momentum"
    REVERSAL_HUNTER = "reversal_hunter"
    TREND_SURFER = "trendsurfer"

    # Ensemble strategies
    ANY = "any"
    ALL = "all"
    

class ShortlisterConfig(BaseModel):
    shortlist_id: str
    strategy: Strategies
    data_config: DataConfig
    
    
    
class Shortlister:
    def __init__(self, config: ShortlisterConfig) -> None:
        self.config = config
        self.data_manager = DataManager(config=config.data_config)
        
        
    def analyze_momentum(self, 
                         ticker: str,
                         strategy: Strategies) -> dict:
        try:
            if strategy == Strategies.ANY:
                results = {}
                passes = []
                for strat in [s for s in Strategies if s not in (Strategies.ANY, Strategies.ALL)]:
                    res = self.analyze_momentum(ticker, strat)
                    results[strat.value] = res
                    passes.append(res.get("pass_filter", False))
                return {"pass_filter": any(passes), "details": results}
            elif strategy == Strategies.ALL:
                results = {}
                passes = []
                for strat in [s for s in Strategies if s not in (Strategies.ANY, Strategies.ALL)]:
                    res = self.analyze_momentum(ticker, strat)
                    results[strat.value] = res
                    passes.append(res.get("pass_filter", False))
                return {"pass_filter": all(passes), "details": results}
            else:
                try:
                    df = self.data_manager.get_stock_data(ticker)
                except Exception as e:
                    logging.error(f"Error fetching data for {ticker}: {e}. Skipping.")
                    return {"pass_filter": False, "error": str(e)}
                static_momentum_strat = static_momentum_strategies.get(strategy)
                return static_momentum_strat.analyze(df)
        except Exception as e:
            print(f"Error analyzing momentum for {ticker} with strategy {strategy}: {e}")
            return {}
    
    
    def shortlist(self):
        # Locate tickers.json
        tickers_path = self.config.data_config.data_dir / "tickers.json"
        if not tickers_path.exists():
            raise FileNotFoundError(f"tickers.json not found at {tickers_path}")

        # Read tickers
        with open(tickers_path, "r") as f:
            tickers = json.load(f)
        tickers = list(tickers.keys())

        results = []
        shortlisted_tickers = []
        for ticker in tickers:
            result = self.analyze_momentum(ticker, self.config.strategy)
            results.append({
                "ticker": ticker,
                "result": result
            })
            if result.get("pass_filter", False):
                shortlisted_tickers.append(ticker)

        # Prepare metadata
        metadata = {
            "shortlist_id": self.config.shortlist_id,
            "strategy": self.config.strategy.value,
            "data_config": self.config.data_config.model_dump(mode="json"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "num_tickers": len(tickers),
            "num_shortlisted": len(shortlisted_tickers)
        }

        output = {
            "metadata": metadata,
            "shortlisted_tickers": shortlisted_tickers,
            "results": results
        }

        # Save results as JSON in same directory as tickers.json
        out_path = tickers_path.parent / f"{self.config.shortlist_id}.json"
        with open(out_path, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Shortlist saved to {out_path}")