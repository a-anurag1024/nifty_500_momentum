from pydantic import BaseModel 
from enum import Enum
from typing import Dict
from pandas import DataFrame
import json
from pathlib import Path
from datetime import datetime
import logging

from nifty_500_momentum.static import static_momentum_strategies, StaticScoutResult
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


class StaticShortlistResult(BaseModel):
    shortlist_id: str
    strategy: Strategies
    data_config: DataConfig
    timestamp: datetime
    num_tickers: int
    num_shortlisted: int
    
    shortlisted_tickers: list[str]
    tickers_results: Dict[str, StaticScoutResult]
    
    
class Shortlister:
    def __init__(self, config: ShortlisterConfig) -> None:
        self.config = config
        self.data_manager = DataManager(config=config.data_config)
        
        
    def analyze_momentum(self, 
                         ticker: str,
                         strategy: Strategies) -> StaticScoutResult:
        try:
            if strategy == Strategies.ANY:
                passes = []
                metrics = {}
                reasons = ""
                for strat in [s for s in Strategies if s not in (Strategies.ANY, Strategies.ALL)]:
                    res = self.analyze_momentum(ticker, strat)
                    metrics.update(res.metrics)
                    passes.append(res.pass_filter)
                    reasons += res.reason + "; "
                return StaticScoutResult(
                    pass_filter=any(passes),
                    metrics=metrics,
                    reason=reasons
                )
            elif strategy == Strategies.ALL:
                passes = []
                metrics = {}
                reasons = ""
                for strat in [s for s in Strategies if s not in (Strategies.ANY, Strategies.ALL)]:
                    res = self.analyze_momentum(ticker, strat)
                    metrics.update(res.metrics)
                    passes.append(res.pass_filter)
                    reasons += res.reason + "; "
                return StaticScoutResult(
                    pass_filter=all(passes),
                    metrics=metrics,
                    reason=reasons
                )
            else:
                try:
                    df = self.data_manager.get_stock_data(ticker)
                except Exception as e:
                    logging.error(f"Error fetching data for {ticker}: {e}. Skipping.")
                    return StaticScoutResult(
                        pass_filter=False,
                        metrics={},
                        reason="Data fetch error"
                    )
                static_momentum_strat = static_momentum_strategies.get(strategy)
                return static_momentum_strat.analyze(df)
        except Exception as e:
            print(f"Error analyzing momentum for {ticker} with strategy {strategy}: {e}")
            return StaticScoutResult(
                pass_filter=False,
                metrics={},
                reason="Analysis error"
            )
    
    
    def shortlist(self):
        tickers = list(self.data_manager.storage.load_tickers().keys())

        results = {}
        shortlisted_tickers = []
        for ticker in tickers:
            result = self.analyze_momentum(ticker, self.config.strategy)
            results[ticker] = result
            if result.pass_filter:
                shortlisted_tickers.append(ticker)

        # Save results
        output = StaticShortlistResult(
            shortlist_id=self.config.shortlist_id,
            strategy=self.config.strategy,
            data_config=self.config.data_config,
            timestamp=datetime.utcnow(),
            num_tickers=len(tickers),
            num_shortlisted=len(shortlisted_tickers),
            shortlisted_tickers=shortlisted_tickers,
            tickers_results=results
        )
        self.data_manager.storage.save_shortlist(
            strategy_name=self.config.strategy.value,
            results=output.model_dump(mode="json")
        )