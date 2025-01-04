from typing import Any, Dict

from pydantic import BaseModel, Field

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import KataSettings


class ChainStep(BaseModel):
    """A single step in a chain of prompts"""

    prompt: str = Field(description="The prompt for this step")
    response: str = Field(description="The response from the LLM")
    next_step: str | None = Field(description="The next step to take, if any")


class ChainResult(BaseModel):
    """Result from a chain of prompts"""

    steps: list[ChainStep] = Field(description="The steps in the chain")
    final_result: str = Field(description="The final result after all steps")


class ChainingKata(KataBase):
    """
    Kata 02: Prompt Chaining Pattern

    This kata demonstrates:
    1. How to decompose tasks into multiple LLM calls
    2. How to chain prompts together with optional gating/checks
    3. How to handle errors and retries in chains
    """

    def __init__(self):
        self.settings = KataSettings()

    def run(self) -> Any:
        """Demonstrates the prompt chaining pattern"""
        # TODO: Implement prompt chaining pattern
        raise NotImplementedError("This kata is not yet implemented")

    def validate_result(self, result: Dict[str, Any]) -> bool:
        """Validates that the chaining pattern worked correctly"""
        # Check we have a valid result object
        if not result or not isinstance(result.data, ChainResult):
            return False

        # Check we have steps
        if (
            not result.data.steps or len(result.data.steps) < 2
        ):  # Need at least 2 steps for a chain
            return False

        # Check each step is valid
        for step in result.data.steps:
            if not isinstance(step, ChainStep):
                return False
            if not step.prompt or not step.response:
                return False
            # All steps except last should have a next_step
            if step != result.data.steps[-1] and not step.next_step:
                return False

        # Check we have a final result
        if not result.data.final_result or len(result.data.final_result) == 0:
            return False

        return True
