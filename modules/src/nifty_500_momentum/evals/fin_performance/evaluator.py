import pandas as pd 
from typing import List, Dict
import numpy as np

from nifty_500_momentum.data.manager import DataManager
from .base_criteria import WinCriteria
from .simple_criteria import SimpleReturnCriteria
from .nuanced_criteria import MomentumContinuationCriteria


class PerformanceEvaluator:
    def __init__(self, dm: DataManager):
        self.dm = dm

    def _fetch_future_data(self, ticker: str, start_date: str, days: int = 5) -> pd.Series:
        """
        Fetches stock data for the [start_date, start_date + days] window.
        Uses DataManager but forces a fresh fetch if needed or queries specific dates.
        Note: DataManager usually fetches 'history'. We assume it has the data.
        """
        # Load the full dataframe from storage
        try:
            df = self.dm.get_stock_data(ticker)
            if df.empty: return pd.Series()
            
            # Filter for the specific date window
            # Ensure index is datetime
            if not isinstance(df.index, pd.DatetimeIndex):
                df.index = pd.to_datetime(df.index)
            
            start_dt = pd.to_datetime(start_date)
            # Add business days buffer roughly
            end_dt = start_dt + pd.Timedelta(days=days + 5)
            
            # Localize timestamps to match df.index timezone if needed
            if df.index.tz is not None:
                start_dt = start_dt.tz_localize(df.index.tz)
                end_dt = end_dt.tz_localize(df.index.tz)
            
            mask = (df.index >= start_dt) & (df.index <= end_dt)
            window = df.loc[mask, 'Close']
            
            # Return exactly 'days' amount of data if possible
            return window.head(days + 1) # T0 + 5 days = 6 data points
            
        except Exception as e:
            print(f"Eval Data Error {ticker}: {e}")
            return pd.Series()

    def evaluate_batch(self, 
                       pick_date: str, 
                       selected_tickers: List[str], 
                       rejected_tickers: List[str],
                       criteria: WinCriteria = SimpleReturnCriteria(),
                       horizon_days: int = 5) -> Dict:
        
        results = {
            'selected_performance': [],
            'rejected_performance': [],
            'metrics': {}
        }
        
        # 1. Evaluate Selected (The "Alpha")
        sel_returns = []
        sel_wins = 0
        
        print(f"--- Evaluating Selected ({len(selected_tickers)}) ---")
        for ticker in selected_tickers:
            prices = self._fetch_future_data(ticker, pick_date, horizon_days)
            res = criteria.evaluate(prices)
            
            results['selected_performance'].append({
                'ticker': ticker,
                'result': res
            })
            if res['magnitude'] != 0: # Only count valid data
                sel_returns.append(res['magnitude'])
                sel_wins += res['is_win']

        # 2. Evaluate Rejected (The "Control Group")
        rej_returns = []
        rej_wins = 0
        
        print(f"--- Evaluating Rejected ({len(rejected_tickers)}) ---")
        for ticker in rejected_tickers:
            prices = self._fetch_future_data(ticker, pick_date, horizon_days)
            res = criteria.evaluate(prices)
            
            results['rejected_performance'].append({
                'ticker': ticker,
                'result': res
            })
            if res['magnitude'] != 0:
                rej_returns.append(res['magnitude'])
                rej_wins += res['is_win']

        # 3. Compute Aggregate Metrics
        def get_stats(returns, wins):
            if not returns: return 0, 0, 0, 0
            return (
                np.mean(returns) * 100,      # Mean %
                np.median(returns) * 100,    # Median % (Resistant to outliers)
                np.std(returns) * 100,       # Volatility (Risk)
                (wins / len(returns)) * 100  # Win Rate %
            )

        sel_mean, sel_median, sel_vol, sel_win_rate = get_stats(sel_returns, sel_wins)
        rej_mean, rej_median, rej_vol, rej_win_rate = get_stats(rej_returns, rej_wins)

        # 4. Construct The Narrative Report
        metrics = {
            'eval_date': pick_date,
            'horizon_days': horizon_days,
            
            # 1. Consistency (Win Rate)
            'win_rate_selected': round(sel_win_rate, 2),
            'win_rate_rejected': round(rej_win_rate, 2),
            'consistency_spread': round(sel_win_rate - rej_win_rate, 2),
            
            # 2. Return Quality (Median is better than Mean)
            'median_return_selected': round(sel_median, 2),
            'median_return_rejected': round(rej_median, 2),
            'median_alpha': round(sel_median - rej_median, 2),
            
            # 3. Risk Profile (Volatility)
            'volatility_selected': round(sel_vol, 2),
            'volatility_rejected': round(rej_vol, 2),
            'risk_reduction': round(rej_vol - sel_vol, 2), # Positive = Good (Selected is safer)          
        }
        
        results['metrics'] = metrics
        return results