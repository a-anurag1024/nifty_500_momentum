from typing import Type, TypeVar
from pydantic import BaseModel
from openai import OpenAI

from .base import (
    BaseLLM,
    SimpleLLMInput,
    SimpleLLMOutput,
    StructuredLLMInput,
)

T = TypeVar("T", bound=BaseModel)



class OpenAILLM(BaseLLM):
    """
    Concrete implementation using OpenAI Responses API.
    Includes:
    - logging
    - retry
    """

    def __init__(self, model="gpt-4.1", max_retries=3):
        super().__init__(provider_name="openai", model=model, max_retries=max_retries)
        self.client = OpenAI()  # uses OPENAI_API_KEY

    # ----------------------------------------------------
    # SIMPLE RESPONSE
    # ----------------------------------------------------
    def generate_simple(self, inp: SimpleLLMInput) -> SimpleLLMOutput:
        def _call():
            return self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": inp.system_prompt},
                    {"role": "user",   "content": inp.user_prompt},
                ],
            )

        response = self._with_retries(_call)
        output_text = response.output_text

        # logging
        self._log(
            interaction_type="simple",
            input_data=inp.model_dump(),
            output_data={"text": output_text},
            usage=response.usage.model_dump() if response.usage else {},
        )

        return SimpleLLMOutput(text=output_text)

    # ----------------------------------------------------
    # STRUCTURED RESPONSE
    # ----------------------------------------------------
    def generate_structured(self, inp: StructuredLLMInput, output_model: Type[T]) -> T:

        def _call():
            return self.client.responses.create(
                model=self.model,
                input=inp.messages,
                response_format=output_model,
            )

        response = self._with_retries(_call)

        parsed = response.output_parsed  # already validated

        # logging
        self._log(
            interaction_type="structured",
            input_data=inp.model_dump(),
            output_data=parsed.model_dump(),
            usage=response.usage.model_dump() if response.usage else {},
        )

        return parsed