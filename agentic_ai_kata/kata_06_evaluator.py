from typing import Any, Dict
from dataclasses import dataclass
from openai import AsyncOpenAI

from pydantic import BaseModel, Field

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import settings


@dataclass
class Deps:
    openai: AsyncOpenAI


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
    1. How to evaluate LLM outputs
    2. How to iteratively improve results
    3. How to determine stopping conditions
    """

    def __init__(self):
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.deps = Deps(openai=self.openai)
        self.agent = self._create_agent()

    def run(self) -> Any:
        """Demonstrates the evaluator-optimizer pattern"""
        # TODO: Implement evaluator-optimizer pattern
        raise NotImplementedError("This kata is not yet implemented")

    def _validate_attempt(
        self, attempt: OptimizationAttempt, last_score: float
    ) -> tuple[bool, float]:
        """Validates a single optimization attempt"""
        if not isinstance(attempt, OptimizationAttempt):
            return False, last_score
        if attempt.attempt_number < 1:
            return False, last_score
        if not attempt.result or len(attempt.result) == 0:
            return False, last_score

        # Check evaluation
        if not isinstance(attempt.evaluation, Evaluation):
            return False, last_score
        if not 0 <= attempt.evaluation.score <= 1:
            return False, last_score
        if not attempt.evaluation.feedback or len(attempt.evaluation.feedback) == 0:
            return False, last_score

        # Scores should generally improve
        if attempt.evaluation.score < last_score:
            return False, last_score

        return True, attempt.evaluation.score

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
            is_valid, new_score = self._validate_attempt(attempt, last_score)
            if not is_valid:
                return False
            last_score = new_score

        # Check final results
        if not result.data.final_result or len(result.data.final_result) == 0:
            return False
        if not 0 <= result.data.final_score <= 1:
            return False
        # Final score should match best attempt
        if result.data.final_score != last_score:
            return False

        return True
