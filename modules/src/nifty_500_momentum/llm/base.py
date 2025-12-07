from abc import ABC, abstractmethod
from typing import List, Dict, Any, Type, Generic, TypeVar
from pydantic import BaseModel
import time

from .logger import LLMLogger


class SimpleLLMInput(BaseModel):
    system_prompt: str
    user_prompt: str


class SimpleLLMOutput(BaseModel):
    text: str


class StructuredLLMInput(BaseModel):
    messages: List[Dict[str, str]]  # [{"role": "...", "content": "..."}]


T = TypeVar("T", bound=BaseModel)


class BaseLLM(ABC):
    """
    Extended abstract LLM base class with:
    - Retry with exponential backoff
    - Structured logging layer
    """

    def __init__(self, provider_name: str, model: str, max_retries: int = 3):
        self.provider_name = provider_name
        self.model = model
        self.max_retries = max_retries
        self.logger = LLMLogger()

    # ------------------------------------------------------
    # Retry Wrapper
    # ------------------------------------------------------
    def _with_retries(self, func, *args, **kwargs):
        """Retry wrapper with exponential backoff."""
        delay = 1
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries:
                    raise e
                time.sleep(delay)
                delay *= 2  # exponential
        # unreachable

    # ------------------------------------------------------
    # Logging utility
    # ------------------------------------------------------
    def _log(self, *, interaction_type, input_data, output_data, usage=None):
        self.logger.log({
            "provider": self.provider_name,
            "model": self.model,
            "interaction_type": interaction_type,
            "input": input_data,
            "output": output_data,
            "usage": usage or {},
        })

    # ------------------------------------------------------
    # Abstract methods
    # ------------------------------------------------------
    @abstractmethod
    def generate_simple(self, inp: BaseModel) -> BaseModel:
        pass

    @abstractmethod
    def generate_structured(self, inp: BaseModel, output_model: Type[T]) -> T:
        pass
