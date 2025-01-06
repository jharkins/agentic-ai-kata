from typing import Any, Dict
from dataclasses import dataclass
from openai import AsyncOpenAI

from pydantic import BaseModel, Field

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import settings


@dataclass
class Deps:
    openai: AsyncOpenAI


class ParallelResult(BaseModel):
    """A result from a parallel execution"""

    task_id: str = Field(description="ID of the parallel task")
    result: str = Field(description="Result from this parallel execution")
    confidence: float = Field(description="Confidence score for this result")


class VotingResult(BaseModel):
    """Result from parallel execution with voting"""

    parallel_results: list[ParallelResult] = Field(description="All parallel results")
    winning_result: str = Field(description="The result that won the vote")
    vote_confidence: float = Field(description="Confidence in the winning result")


class ParallelKata(KataBase):
    """
    Kata 04: Parallel Processing Pattern

    This kata demonstrates:
    1. How to run parallel LLM calls
    2. How to implement voting mechanisms
    3. How to aggregate results
    """

    def __init__(self):
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.deps = Deps(openai=self.openai)
        self.agent = self._create_agent()

    def run(self) -> Any:
        """Demonstrates the parallelization pattern"""
        # TODO: Implement parallelization pattern
        raise NotImplementedError("This kata is not yet implemented")

    def validate_result(self, result: Dict[str, Any]) -> bool:
        """Validates that the parallelization pattern worked correctly"""
        # Check we have a valid result object
        if not result or not isinstance(result.data, VotingResult):
            return False

        # Check we have parallel results
        if (
            not result.data.parallel_results or len(result.data.parallel_results) < 2
        ):  # Need at least 2 for voting
            return False

        # Check each parallel result
        for pr in result.data.parallel_results:
            if not isinstance(pr, ParallelResult):
                return False
            if not pr.task_id or len(pr.task_id) == 0:
                return False
            if not pr.result or len(pr.result) == 0:
                return False
            if not 0 <= pr.confidence <= 1:
                return False

        # Check voting results
        if not result.data.winning_result or len(result.data.winning_result) == 0:
            return False
        if not 0 <= result.data.vote_confidence <= 1:
            return False

        return True
