from datetime import datetime
from nifty_500_momentum.data.config import DataConfig
from nifty_500_momentum.data.collectors.run_manager import (
    RunManager, RunManagerConfig, DataRunConfig, PipelineType
)
from nifty_500_momentum.data.collectors.stocks_collector import StocksDataCollectorInputs

# --- Options ---

RUN_ID = "run_1"

# Base directory for saving logs, data, and runs
BASE_SAVE_DIR = "data"  # Change as needed

# DataConfig options
DATA_CONFIG = DataConfig(
    data_dir=BASE_SAVE_DIR,         # Base data directory for this run
    stock_api_sleep=5.0,            # Sleep between API calls (seconds)
    news_api_sleep=5.0,             # Sleep for news API (not used here)
    cache_expiry_hours=24,          # Cache expiry for news (not used here)
    stock_file_ext=".parquet",      # File extension for stock data
    news_file_ext=".json"           # File extension for news data
)

# StocksDataCollectorInputs options
COLLECTOR_INPUTS = StocksDataCollectorInputs(
    all_tickers=True,               # Collect all Nifty 500 tickers
    tickers={},                     # Or specify a subset: {"Reliance Industries Ltd.": "RELIANCE.NS"}
    period="2y",                    # Data period to collect
    force_refresh=False             # Force refresh even if data exists
)

# RunManagerConfig options
RUN_MANAGER_CONFIG = RunManagerConfig(
    base_save_dir=BASE_SAVE_DIR     # Base directory for all outputs
)

# DataRunConfig options
DATA_RUN_CONFIG = DataRunConfig(
    run_id=RUN_ID,
    pipeline=PipelineType.STOCK,
    created_at=datetime.now(),
    status="initialized",
    inputs=COLLECTOR_INPUTS,
    data_config=DATA_CONFIG
)

# --- Run the collection ---
if __name__ == "__main__":
    run_manager = RunManager(RUN_MANAGER_CONFIG)
    run_manager.run(DATA_RUN_CONFIG)