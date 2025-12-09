from abc import ABC, abstractmethod 
from typing import List, Dict, Any
from pydantic import BaseModel

from nifty_500_momentum.data.config import DataConfig
from nifty_500_momentum.data.manager import DataManager

from .state import AnalystState


class BaseWorkflowConfig(BaseModel):
    data_config: DataConfig


class BaseWorkflow(ABC):
    def __init__(self, config: BaseWorkflowConfig):
        self.config = config
        self.data_manager = DataManager(config=config.data_config)
        
        
    @abstractmethod
    def _run(self, state: AnalystState) -> AnalystState:
        pass
    
    
    def _save_state(self, state: AnalystState) -> None:
        self.data_manager.storage.save_analyst_state(state.analysis_id, state.model_dump(mode='json'))
    
    def run(self, state: AnalystState) -> AnalystState:
        final_state = self._run(state)
        self._save_state(final_state)
        return final_state