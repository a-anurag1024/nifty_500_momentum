from pydantic import BaseModel, Field


class LLMJudgeEval(BaseModel):
    grade: int = Field(..., description="1-10, where 10 is perfect reasoning")
    critique: str = Field(..., description="Explanation of the grade")
    correct_driver: str = Field(..., description="What the driver SHOULD have been, if they got it wrong")