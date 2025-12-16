from datetime import datetime
from pathlib import Path
from nifty_500_momentum.data.config import DataConfig
from nifty_500_momentum.data.manager import DataManager
from dotenv import load_dotenv

# load the environment variables from the .env file
ENV_FILE = Path(".env")
load_dotenv(dotenv_path=ENV_FILE)

from nifty_500_momentum.static.shortlister import Strategies

from nifty_500_momentum.evals.laaj.judge import LLMJudge, LLMJudgeEval


# --- Options for running the agent performance evaluation ---

RUN_ID = "run_1"
STRATEGY = Strategies.ANY
ANALYSIS_ID = f"{RUN_ID}_{STRATEGY.value}"
number_of_sample_checks = 20


# Base directory for saving logs, data, and runs
BASE_SAVE_DIR = Path("data")  # Change as needed

EVAL_DATA_CONFIG = DataConfig(
    data_dir=BASE_SAVE_DIR / "data" / RUN_ID,         # Base data directory for this run
    stock_api_sleep=5.0,                              # Sleep between API calls (seconds)
    news_api_sleep=5.0,                               # Sleep for news API (not used here)
    cache_expiry_hours=24,                            # Cache expiry for news (not used here)
    stock_file_ext=".parquet",                        # File extension for stock data
    news_file_ext=".json"                             # File extension for news data
)


if __name__ == "__main__":
    # --- Run the collection ---
    
    # --- Run the Evaluation ---
    print(f">> Running the Evaluations")
    dm = DataManager(config=EVAL_DATA_CONFIG) 
    
    judge = LLMJudge(data_manager=dm,
                     num_of_samples_checks=number_of_sample_checks)

    # Run Eval
    report = judge.evaluate_performance(analysis_id=ANALYSIS_ID,
                                        strategy_name=STRATEGY.value)

    print("\n--- FINAL REPORT ---")
    print(report)
    print(report["summary"])