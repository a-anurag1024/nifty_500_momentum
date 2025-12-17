from datetime import datetime
from pathlib import Path
import json
from nifty_500_momentum.data.config import DataConfig
from nifty_500_momentum.data.manager import DataManager
from nifty_500_momentum.data.collectors.run_manager import (
    RunManager, RunManagerConfig, DataRunConfig, PipelineType
)
from nifty_500_momentum.data.collectors.stocks_collector import StocksDataCollectorInputs
from nifty_500_momentum.static.shortlister import Strategies

from nifty_500_momentum.evals.fin_performance.evaluator import (
    PerformanceEvaluator,
    MomentumContinuationCriteria
)


# --- Options for running the financial performance evaluation ---
### NOTE: The script must be run after HORIZON_DAYS after the DATE_OF_PICK

RUN_ID = "run_1"
STRATEGY = Strategies.ANY
ANALYSIS_ID = f"{RUN_ID}_{STRATEGY.value}"
DATE_OF_PICK = "2025-12-07"
HORIZON_DAYS = 5

# Config for Nuanced Performance Evaluation
MAX_DRAWDOWN_TOLERANCE = -0.02



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


# --- Options for collecting (new data) to backtest ---

NEW_RUN_ID = f"{RUN_ID}_eval"

# DataConfig options
COLLECT_DATA_CONFIG = DataConfig(
    data_dir=BASE_SAVE_DIR / "data" / NEW_RUN_ID,         # Base data directory for this run
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
    base_save_dir=str(BASE_SAVE_DIR)     # Base directory for all outputs
)

# DataRunConfig options
DATA_RUN_CONFIG = DataRunConfig(
    run_id=NEW_RUN_ID,
    pipeline=PipelineType.STOCK,
    created_at=datetime.now(),
    status="initialized",
    inputs=COLLECTOR_INPUTS,
    data_config=COLLECT_DATA_CONFIG
)


if __name__ == "__main__":
    # --- Run the collection ---
    print(f">> Collecting New Data to Backtest")
    run_manager = RunManager(RUN_MANAGER_CONFIG)
    run_manager.run(DATA_RUN_CONFIG)
    
    
    # --- Run the Evaluation ---
    print(f">> Running the Evaluations")
    dm = DataManager(config=EVAL_DATA_CONFIG) 
    
    analyst_state = dm.storage.load_analyst_state(analysis_id=ANALYSIS_ID)
    conv_threshold = analyst_state['conviction_threshold']
    sent_threshold = analyst_state['sentiment_threshold']
    tickers_with_static_signals = set()
    selected_tickers = set()
    for ticker, results in analyst_state['analysis_results'].items():
        if results["sentiment_score"] >= sent_threshold and results["conviction_score"] >= conv_threshold:
            selected_tickers.add(ticker)
        tickers_with_static_signals.add(ticker)
    rejected_tickers = tickers_with_static_signals - selected_tickers
            

    # Initialize Evaluator
    dm = DataManager(config=COLLECT_DATA_CONFIG)
    evaluator = PerformanceEvaluator(dm)

    # Define nuanced criteria
    nuanced_criteria = MomentumContinuationCriteria(max_drawdown_tolerance=MAX_DRAWDOWN_TOLERANCE)

    # Run Eval
    report = evaluator.evaluate_batch(
        pick_date=DATE_OF_PICK,  
        selected_tickers=list(selected_tickers),
        rejected_tickers=list(rejected_tickers),
        criteria=nuanced_criteria,
        horizon_days=HORIZON_DAYS
    )

    print("\n--- FINAL REPORT ---")
    #print(report['metrics'])
    print(f"-- eval_date: {report['metrics']['eval_date']}")
    print(f"-- horizon_days: {report['metrics']['horizon_days']}")
    print("--- Win Rate ---")
    print(f"-- win_rate_selected: {report['metrics']['win_rate_selected']}%")
    print(f"-- win_rate_rejected: {report['metrics']['win_rate_rejected']}%")
    print("--- Return Quality ---")
    print(f"-- consistency_spread: {report['metrics']['consistency_spread']}%")
    print(f"-- median_return_selected: {report['metrics']['median_return_selected']}%")
    print(f"-- median_return_rejected: {report['metrics']['median_return_rejected']}%")
    print(f"-- median_alpha: {report['metrics']['median_alpha']}%")
    print("--- Risk Profile ---")
    print(f"-- volatility_selected: {report['metrics']['volatility_selected']}%")
    print(f"-- volatility_rejected: {report['metrics']['volatility_rejected']}%")
    print(f"-- risk_reduction: {report['metrics']['risk_reduction']}%")
    
    with open(BASE_SAVE_DIR / "data" / RUN_ID / f"{ANALYSIS_ID}_fin_performance_report.txt", "w") as f:
        json.dump(report, f, indent=4)