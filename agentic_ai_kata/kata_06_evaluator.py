from typing import Any

from pydantic import BaseModel, Field

from agentic_ai_katabase import KataBase
from agentic_ai_katasettings import KataSettings


class Evaluation(BaseModel):
    """An evaluation of an attempt"""

    score: float = Field(description="Score for this attempt (0-1)")
    feedback: str = Field(description="Detailed feedback on what to improve")
    suggestions: list[str] = Field(description="Specific suggestions for improvement")


class OptimizationAttempt(BaseModel):
    """A single optimization attempt"""

    attempt_number: int = Field(description="Which attempt this is")
    result: str = Field(description="The result being evaluated")
    evaluation: Evaluation = Field(description="Evaluation of this attempt")


class EvaluatorResult(BaseModel):
    """Overall result from the evaluator-optimizer process"""

    attempts: list[OptimizationAttempt] = Field(description="All optimization attempts")
    final_result: str = Field(description="The best result achieved")
    final_score: float = Field(description="Score of the final result")


class EvaluatorKata(KataBase):
    """
    Kata 06: Evaluator-Optimizer Pattern

    This kata demonstrates:
    1. How to use one LLM to evaluate another's output
    2. How to iteratively improve results
    3. How to know when to stop optimizing
    """

    def __init__(self):
        self.settings = KataSettings()

    def run(self) -> Any:
        """Demonstrates the evaluator-optimizer pattern"""
        # TODO: Implement evaluator-optimizer pattern
        raise NotImplementedError("This kata is not yet implemented")
