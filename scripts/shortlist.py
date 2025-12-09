from datetime import datetime
from pathlib import Path
from nifty_500_momentum.static.shortlister import Shortlister, ShortlisterConfig, Strategies
from nifty_500_momentum.data.config import DataConfig

# --- Options ---
RUN_ID = "run_1"
STRATEGY = Strategies.ANY
SHORTLIST_ID = f"shortlist_{STRATEGY.value}"

BASE_SAVE_DIR = Path("data")  # Change as needed

# DataConfig options
DATA_CONFIG = DataConfig(
    data_dir=BASE_SAVE_DIR / "data" / RUN_ID,
    stock_api_sleep=5.0,
    news_api_sleep=5.0,
    cache_expiry_hours=24,
    stock_file_ext=".parquet",
    news_file_ext=".json"
)

# ShortlisterConfig options
SHORTLISTER_CONFIG = ShortlisterConfig(
    shortlist_id=SHORTLIST_ID,
    strategy=STRATEGY,  # Change strategy as needed
    data_config=DATA_CONFIG
)

if __name__ == "__main__":
    shortlister = Shortlister(SHORTLISTER_CONFIG)
    shortlister.shortlist()
