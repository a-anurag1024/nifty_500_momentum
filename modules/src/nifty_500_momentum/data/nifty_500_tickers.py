import pandas as pd
import requests
import io
import logging

"""
UNIVERSE MODULE
---------------
Fetches the official list of Nifty 500 stocks from NSE website.
"""

def get_nifty500_tickers() -> dict:
    """
    Fetches the latest Nifty 500 ticker list from NSE Archives.
    Returns a dictionary: {'Company Name': 'TICKER.NS'}
    Example: {'Reliance Industries Ltd.': 'RELIANCE.NS'}
    """
    url = "https://nsearchives.nseindia.com/content/indices/ind_nifty500list.csv"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        logging.info("Fetching Nifty 500 list from NSE...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Read CSV from memory
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        
        # Verify required columns exist
        required_cols = ['Company Name', 'Symbol']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"CSV format changed. Expected columns {required_cols} not found.")
            
        ticker_map = {}
        
        for index, row in df.iterrows():
            company_name = row['Company Name'].strip()
            symbol = row['Symbol'].strip()
            
            # Format for Yahoo Finance (add .NS suffix)
            # Some symbols might already have suffixes, handle carefully
            #formatted_symbol = f"{symbol}.NS"
            
            #ticker_map[company_name] = formatted_symbol
            ticker_map[symbol] = company_name
            
        logging.info(f"Successfully loaded {len(ticker_map)} tickers.")
        return ticker_map

    except Exception as e:
        logging.error(f"Error fetching Nifty 500 list: {e}")
        logging.warning("Falling back to Top 10 Stocks for demo...")
        return get_fallback_tickers()


def get_full_index_info() -> pd.DataFrame:
    """Fetches the full Nifty 500 index information as a DataFrame."""
    url = "https://nsearchives.nseindia.com/content/indices/ind_nifty500list.csv"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        logging.info("Fetching full Nifty 500 index information from NSE...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        logging.info(f"Successfully loaded full index info with {len(df)} entries.")
        return df

    except Exception as e:
        logging.error(f"Error fetching full Nifty 500 index info: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure
    

def get_fallback_tickers() -> dict:
    """Returns top 10 Nifty stocks as a fallback dictionary if scraping fails."""
    return {
        "Reliance Industries Ltd.": "RELIANCE.NS",
        "Tata Consultancy Services Ltd.": "TCS.NS",
        "HDFC Bank Ltd.": "HDFCBANK.NS",
        "Infosys Ltd.": "INFY.NS",
        "ICICI Bank Ltd.": "ICICIBANK.NS",
        "Hindustan Unilever Ltd.": "HINDUNILVR.NS",
        "State Bank of India": "SBIN.NS",
        "Bharti Airtel Ltd.": "BHARTIARTL.NS",
        "ITC Ltd.": "ITC.NS",
        "Kotak Mahindra Bank Ltd.": "KOTAKBANK.NS"
    }

# Example usage
if __name__ == "__main__":
    tickers = get_nifty500_tickers()
    
    # Print first 5 items to verify
    for i, (name, symbol) in enumerate(tickers.items()):
        if i >= 5: break
        print(f"{name}: {symbol}")