from typing import Dict, List

from ..base_workflow import BaseWorkflow 
from ..news_filters import NewsFilterEngine, NewsArticle

from nifty_500_momentum.static.shortlister import StaticShortlistResult
from nifty_500_momentum.analysts.analyzers import ComprehensiveAnalyzer, ComprehensiveMomentumAnalysis, AnalyzerInput

import logging

class StraightforwardWorkflow(BaseWorkflow):
    
    def _run(self, state):
        
        # Step-0: Fetch Data
        shortlist_data = self.data_manager.storage.load_shortlist(state.shortlisting_strategy.value)
        tickers_company_names = self.data_manager.storage.load_tickers()
        shortlist_data = StaticShortlistResult(**shortlist_data)
        tickers = shortlist_data.shortlisted_tickers
        tickers_news_data = {}
        logging.info(f">>> Fetching news data for {len(tickers)} shortlisted tickers...")
        for ticker in tickers:
            company_name = tickers_company_names[ticker]
            query = f"{state.NEWS_QUERY_PREFIX} {company_name} {state.NEWS_QUERY_SUFFIX}".strip()
            news_data = self.data_manager.storage.load_news(query)
            tickers_news_data[ticker] = news_data
        
        # Step-1: Apply news filters 
        logging.info(">>> Applying news filters...")
        news_filter_engine = NewsFilterEngine(state.news_filters)
        tickers_filtered_news: Dict[str, List[NewsArticle]] = {}
        for ticker, news_articles in tickers_news_data.items():
            filtered_articles = news_filter_engine.run(news_articles)
            tickers_filtered_news[ticker] = filtered_articles
        state.filtered_news = tickers_filtered_news
        
        # Step-2: Run the Analysis
        analyzer = ComprehensiveAnalyzer()
        for ticker, news_articles in tickers_filtered_news.items():
            logging.info(f">>> Analyzing ticker: {ticker} with {len(news_articles)} news articles.")
            inp = AnalyzerInput(static_results=shortlist_data.tickers_results[ticker], 
                                news_data=news_articles)
            results = analyzer.analyze(inp)
            state.analysis_results[ticker] = results
            self._save_state(state)
        
        # TODO: Step-3: Final Shortlisting 
        
        
        # TODO: Step-4: Summary creation
        
        return state