from pydantic import BaseModel
from abc import ABC, abstractmethod
from nifty_500_momentum.data.config import DataConfig
from nifty_500_momentum.data.manager import DataManager


class DataCollector(ABC):
    def __init__(self, data_config: DataConfig):
        self.data_config = data_config
        self.data_manager = DataManager(config=data_config)
        
    
    @abstractmethod
    def collect(self, inputs: BaseModel) -> None:
        pass
    