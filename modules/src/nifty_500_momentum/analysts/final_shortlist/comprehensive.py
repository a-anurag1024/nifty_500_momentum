from pydantic import BaseModel, Field
from typing import List, Dict

from .base import BaseFinalShortlist
from nifty_500_momentum.analysts.analyzers.comprehensive import ComprehensiveMomentumAnalysis


class ComprehensiveFinalShortlist(BaseFinalShortlist):
    def shortlist(self, 
                  results: Dict[str, ComprehensiveMomentumAnalysis],
                  conviction_threshold: float = 5,
                  sentiment_threshold: float = 0.1,
                  top_n: int = 5):
        """
        Returns a ranked dictionary of final shortlisted tickers and their details.
        """
        final_shortlist: Dict[int, str] = {}
        ranked_tickers = sorted(results.items(), key=lambda x: x[1].conviction_score, reverse=True)
        # remove tickers below thresholds
        filtered_tickers = [(ticker, analysis) for ticker, analysis in ranked_tickers 
                            if analysis.conviction_score >= conviction_threshold 
                            and analysis.sentiment_score >= sentiment_threshold][:top_n]
        for rank, (ticker, analysis) in enumerate(filtered_tickers, start=1):
            final_shortlist[rank] = ticker
        return final_shortlist