import yfinance as yf
import pandas as pd
from nifty_500_momentum.data.interfaces import StockDataSource


class YFinanceSource(StockDataSource):
    def fetch_history(self, ticker: str, period: str = "2y") -> pd.DataFrame:
        """
        Fetches data from Yahoo Finance.
        Handles the '.NS' suffix logic for Indian markets if missing.
        """
        # Auto-append .NS for Indian stocks if not present
        if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
            ticker = f"{ticker}.NS"
            
        try:
            # group_by='ticker' ensures we get a flat dataframe for a single ticker
            ticker_obj = yf.Ticker(ticker)
            df = ticker_obj.history(period=period)
            
            if df.empty:
                raise ValueError(f"No data found for {ticker}")
                
            # Clean up columns (Remove Dividends/Splits if not needed)
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            return df
            
        except Exception as e:
            print(f"Error fetching {ticker} from YFinance: {e}")
            return pd.DataFrame()