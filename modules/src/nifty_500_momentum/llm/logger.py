import json
import os
from datetime import datetime
from typing import Any, Dict

from anyio import Path



class LLMLogger:
    LOG_FILE = Path(os.getenv("LLM_LOG_DIR", "logs/llm_logs.jsonl"))

    def __init__(self):
        os.makedirs("logs", exist_ok=True)

    def log(self, record: Dict[str, Any]):
        """Append one JSON log entry per line."""
        record["timestamp"] = datetime.utcnow().isoformat()
        with open(self.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
