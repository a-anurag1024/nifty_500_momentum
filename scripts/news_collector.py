from datetime import datetime
from pathlib import Path
from nifty_500_momentum.data.config import DataConfig
from nifty_500_momentum.data.collectors.run_manager import (
    RunManager, RunManagerConfig, DataRunConfig, PipelineType
)
from nifty_500_momentum.static.shortlister import Strategies
from nifty_500_momentum.data.collectors.news_collector import NewsDataCollectorInputs
import json

# --- Options ---
RUN_ID = "run_1"
STRATEGY = Strategies.ANY
SHORTLIST_ID = f"shortlist_{STRATEGY.value}"
BASE_SAVE_DIR = Path("data")

QUERY_PREFIX = ""
QUERY_POSTFIX = "News"

# DataConfig options
DATA_CONFIG = DataConfig(
    data_dir=BASE_SAVE_DIR / "data" / RUN_ID,
    stock_api_sleep=5.0,
    news_api_sleep=5.0,
    cache_expiry_hours=24,
    stock_file_ext=".parquet",
    news_file_ext=".json"
)

# Fetch shortlisted tickers from shortlist file
shortlist_path = DATA_CONFIG.data_dir / f"{SHORTLIST_ID}.json"
with open(shortlist_path, "r") as f:
    shortlist_data = json.load(f)
tickers = [item for item in shortlist_data.get("shortlisted_tickers", [])]

# NewsDataCollectorInputs options
NEWS_COLLECTOR_INPUTS = NewsDataCollectorInputs(
    tickers=tickers,
    query_prefix=QUERY_PREFIX,
    query_postfix=QUERY_POSTFIX,
    force_refresh=False
)

# RunManagerConfig options
RUN_MANAGER_CONFIG = RunManagerConfig(
    base_save_dir=str(BASE_SAVE_DIR)
)

# DataRunConfig options
DATA_RUN_CONFIG = DataRunConfig(
    run_id=RUN_ID,
    pipeline=PipelineType.NEWS,
    created_at=datetime.now(),
    status="initialized",
    inputs=NEWS_COLLECTOR_INPUTS,
    data_config=DATA_CONFIG
)

if __name__ == "__main__":
    run_manager = RunManager(RUN_MANAGER_CONFIG)
    run_manager.run(DATA_RUN_CONFIG)
