from typing import Any, Dict

from pydantic import BaseModel, Field

from ..base import KataBase
from ..settings import KataSettings


class AugmentedResult(BaseModel):
    """Result from an augmented LLM that includes context used"""

    response: str = Field(description="The LLM's response")
    context_used: list[str] = Field(description="The context pieces that were used")
    tool_calls: list[str] = Field(description="The tools that were called")


class AugmentedKata(KataBase):
    """
    Kata 01: Augmented LLM Pattern

    This kata demonstrates:
    1. How to augment LLM calls with retrieval
    2. How to integrate tools into LLM responses
    3. How to maintain memory across interactions
    """

    def __init__(self):
        self.settings = KataSettings()

    def run(self) -> Any:
        """Demonstrates the augmented LLM pattern"""
        # TODO: Implement augmented LLM pattern
        raise NotImplementedError("This kata is not yet implemented")
