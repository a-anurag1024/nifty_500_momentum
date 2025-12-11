import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
import os
from dotenv import load_dotenv

# load the environment variables from the .env file
ENV_FILE = Path(".env")
load_dotenv(dotenv_path=ENV_FILE)

from nifty_500_momentum.analysts.base_workflow import BaseWorkflowConfig
from nifty_500_momentum.analysts.news_filters import SelectNewsFilterStrategy
from nifty_500_momentum.analysts.state import AnalystState
from nifty_500_momentum.analysts.workflows.straightforward import StraightforwardWorkflow
from nifty_500_momentum.data.config import DataConfig
from nifty_500_momentum.static.shortlister import Strategies


RUN_ID = "run_1"
BASE_SAVE_DIR = Path("data")


CONFIG: Dict[str, Any] = {
    # Identifiers
    "run_id": RUN_ID,
    "analysis_id": None,  # If None, defaults to "{run_id}_{shortlisting_strategy}"

    # Data + workflow settings
    "shortlisting_strategy": Strategies.ANY,  # See Strategies enum for options
    "data_dir": BASE_SAVE_DIR / "data" / RUN_ID,
    "news_query_prefix": "",
    "news_query_suffix": "News",
    "log_level": "INFO",

    # Optional overrides for DataConfig
    "data_config_overrides": {
        "stock_api_sleep": 5.0,
        "news_api_sleep": 5.0,
        "cache_expiry_hours": 1024,
    },

    # News filter chain (order matters)
    "news_filter_strategies": [
        {"strategy_name": "TimeRecencyFilter", "config": {"hours": 180}},
        {"strategy_name": "SourceBlacklistFilter", "config": {"blacklisted_sources": ["The Motley Fool"]}},
    ],
    
    # Analysis thresholds
    "conviction_threshold": 5.0,
    "sentiment_threshold": 0.1,
    "top_n_final_shortlist": 5,
}


def build_data_config(cfg: Dict[str, Any]) -> DataConfig:
    overrides = dict(cfg.get("data_config_overrides", {}))
    overrides["data_dir"] = Path(cfg["data_dir"]).resolve()
    data_config = DataConfig(**overrides)
    data_config.setup_directories()
    return data_config


def build_news_filters(filter_cfg: List[Dict[str, Any]]) -> List[SelectNewsFilterStrategy]:
    return [
        SelectNewsFilterStrategy(
            strategy_name=entry["strategy_name"],
            config=entry.get("config", {}),
        )
        for entry in filter_cfg
    ]


def resolve_analysis_id(cfg: Dict[str, Any]) -> str:
    if cfg.get("analysis_id"):
        return cfg["analysis_id"]
    return f"{cfg['run_id']}_{cfg['shortlisting_strategy']}"


def main() -> None:
    log_level = getattr(logging, str(CONFIG["log_level"]).upper(), logging.INFO)
    logging.basicConfig(level=log_level)

    data_config = build_data_config(CONFIG)
    workflow_config = BaseWorkflowConfig(data_config=data_config)

    strategy = CONFIG["shortlisting_strategy"]
    news_query_prefix = CONFIG["news_query_prefix"]
    news_query_suffix = CONFIG["news_query_suffix"]
    analysis_id = resolve_analysis_id(CONFIG)
    news_filters = build_news_filters(CONFIG.get("news_filter_strategies", []))

    state = AnalystState(
        run_id=CONFIG["run_id"],
        analysis_id=analysis_id,
        shortlisting_strategy=strategy,
        NEWS_QUERY_PREFIX=news_query_prefix,
        NEWS_QUERY_SUFFIX=news_query_suffix,
        news_filters=news_filters,
        conviction_threshold=CONFIG["conviction_threshold"],
        sentiment_threshold=CONFIG["sentiment_threshold"],
        top_n_final_shortlist=CONFIG["top_n_final_shortlist"],
        filtered_news={},
        analysis_results={},
    )

    workflow = StraightforwardWorkflow(config=workflow_config)
    final_state = workflow.run(state)

    report_path = data_config.data_dir / f"report_{final_state.analysis_id}.json"
    logging.info("Workflow complete. Analyst report saved to %s", report_path)


if __name__ == "__main__":
    main()
