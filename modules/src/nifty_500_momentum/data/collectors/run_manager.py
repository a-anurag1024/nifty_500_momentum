from pydantic import BaseModel
from datetime import datetime
import os
from nifty_500_momentum.data.config import DataConfig
from .stocks_collector import StocksDataCollector, StocksDataCollectorInputs
from .news_collector import NewsDataCollector, NewsDataCollectorInputs
from enum import Enum

"""
Run Manager
---------------
Compatible with local storage. Would require Different implementation for cloud storage.
"""

class RunManagerConfig(BaseModel):
    base_save_dir: str
    
class PipelineType(str, Enum):
    STOCK = "stock"
    NEWS = "news"

class DataRunConfig(BaseModel):
    run_id: str
    pipeline: PipelineType
    created_at: datetime
    status: str
    inputs: BaseModel
    data_config: DataConfig
    
    
class RunManager:
    def __init__(self, config: RunManagerConfig) -> None:
        self.config = config
        self.base_logs_dir = config.base_save_dir + "/logs"
        self.base_data_dir = config.base_save_dir + "/data"
        self.base_runs_dir = config.base_save_dir + "/runs"
        os.makedirs(self.base_logs_dir, exist_ok=True)
        os.makedirs(self.base_data_dir, exist_ok=True)
        os.makedirs(self.base_runs_dir, exist_ok=True)
    
    def run(self, run_config: DataRunConfig):
        import logging
        import json
        from pathlib import Path
        import signal
        import sys

        # 1. Initialize logging
        log_file = Path(self.base_logs_dir) / f"run_{run_config.run_id}_{run_config.pipeline.value}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
        )
        logging.info(f"Starting data collection run: {run_config.run_id} | Pipeline: {run_config.pipeline}")

        # 2. Select DataCollector class based on pipeline
        collector = None
        print(Path(self.base_data_dir) / run_config.run_id)
        data_config = DataConfig(data_dir=Path(self.base_data_dir) / run_config.run_id,
                                 stock_api_sleep=run_config.data_config.stock_api_sleep,
                                 news_api_sleep=run_config.data_config.news_api_sleep,
                                 cache_expiry_hours=run_config.data_config.cache_expiry_hours,
                                 stock_file_ext=run_config.data_config.stock_file_ext,
                                 news_file_ext=run_config.data_config.news_file_ext)
        data_config.setup_directories()
        if run_config.pipeline == PipelineType.STOCK:
            collector = StocksDataCollector(data_config=data_config)
        elif run_config.pipeline == PipelineType.NEWS:
            collector = NewsDataCollector(data_config=data_config)
        else:
            logging.error(f"Unknown pipeline: {run_config.pipeline}")
            run_config.status = "failed"
            return

        # 3. Safe stop mechanism and metadata update
        run_metadata_path = Path(self.base_runs_dir) / f"{run_config.run_id}_{run_config.pipeline.value}.json"
        stop_flag = {"stopped": False}

        def handle_stop(signum, frame):
            logging.warning("Received stop signal. Marking run as stopped.")
            stop_flag["stopped"] = True
            run_config.status = "stopped"
            with open(run_metadata_path, 'w') as f:
                json.dump(run_config.model_dump(), f, default=str, indent=2)
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_stop)
        signal.signal(signal.SIGTERM, handle_stop)

        try:
            run_config.status = "running"
            with open(run_metadata_path, 'w') as f:
                json.dump(run_config.model_dump(), f, default=str, indent=2)
            # Run the collector (assuming .collect method)
            collector.collect(run_config.inputs)
            run_config.status = "completed"
            logging.info("Data collection completed successfully.")
        except Exception as e:
            run_config.status = "failed"
            logging.error(f"Data collection failed: {e}")
        finally:
            with open(run_metadata_path, 'w') as f:
                json.dump(run_config.model_dump(), f, default=str, indent=2)
            logging.info(f"Run metadata saved to {run_metadata_path}")