from typing import Any, Dict

from pydantic import BaseModel, Field

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import KataSettings


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

    def validate_result(self, result: Dict[str, Any]) -> bool:
        """Validates that the evaluator pattern worked correctly"""
        # Check we have a valid result object
        if not result or not isinstance(result.data, EvaluatorResult):
            return False

        # Check we have attempts
        if not result.data.attempts or len(result.data.attempts) == 0:
            return False

        # Check each attempt
        last_score = -1
        for attempt in result.data.attempts:
            if not isinstance(attempt, OptimizationAttempt):
                return False
            if attempt.attempt_number < 1:
                return False
            if not attempt.result or len(attempt.result) == 0:
                return False

            # Check evaluation
            if not isinstance(attempt.evaluation, Evaluation):
                return False
            if not 0 <= attempt.evaluation.score <= 1:
                return False
            if not attempt.evaluation.feedback or len(attempt.evaluation.feedback) == 0:
                return False
            if not attempt.evaluation.suggestions:  # Empty list is ok for final attempt
                if attempt != result.data.attempts[-1]:
                    return False

            # Scores should generally improve
            if attempt.evaluation.score < last_score:
                return False
            last_score = attempt.evaluation.score

        # Check final results
        if not result.data.final_result or len(result.data.final_result) == 0:
            return False
        if not 0 <= result.data.final_score <= 1:
            return False
        # Final score should match best attempt
        if result.data.final_score != last_score:
            return False

        return True
