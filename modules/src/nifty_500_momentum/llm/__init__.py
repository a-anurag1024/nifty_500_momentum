from typing import Type
import os
from .base import BaseLLM
from .openai import OpenAILLM
# from your_anthropic_impl import AnthropicLLM
# from your_groq_impl import GroqLLM


class LLMFactory:
    _registry: dict[str, Type[BaseLLM]] = {
        "openai": OpenAILLM,
        # "anthropic": AnthropicLLM,
        # "groq": GroqLLM,
    }

    @staticmethod
    def create(provider: str, **kwargs) -> BaseLLM:
        provider = provider.lower()
        if provider not in LLMFactory._registry:
            raise ValueError(f"Unknown LLM provider: {provider}")
        return LLMFactory._registry[provider](**kwargs)


DEFAULT_LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
DEFAULT_LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-nano")
    
llm: BaseLLM = LLMFactory.create(
    provider=DEFAULT_LLM_PROVIDER,
    model=DEFAULT_LLM_MODEL
)
